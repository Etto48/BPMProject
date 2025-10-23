import psycopg
from typing import Optional
from models import ProjectInDB, RiskInDB, TrackedScoredRisk, TrackedManagedRisk, UserResponse, UserInDB, Project

class UserRepository:
    def __init__(self, connection: psycopg.AsyncConnection):
        self.conn = connection

    async def create_user(self, username: str, passwordHash: str) -> Optional[UserResponse]:
        """Create a new user in the database"""
        try:
            async with self.conn.transaction():
                async with self.conn.cursor() as cursor:
                    await cursor.execute(
                        "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id, username",
                        (username, passwordHash)
                    )
                    row = await cursor.fetchone()
                    if row:
                        return UserResponse(id=row[0], username=row[1])
                    return None
        except psycopg.IntegrityError:
            # Username already exists
            return None

    async def get_user_by_username(self, username: str) -> Optional[UserInDB]:
        """Get user by username, returns (id, username, password_hash)"""
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "SELECT id, username, password_hash FROM users WHERE username = %s",
                (username,)
            )
            row = await cursor.fetchone()
            if row:
                return UserInDB(id=row[0], username=row[1], passwordHash=row[2])
            return None

    async def get_user_by_id(self, userId: int) -> Optional[UserResponse]:
        """Get user by ID"""
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "SELECT id, username FROM users WHERE id = %s",
                (userId,)
            )
            row = await cursor.fetchone()
            if row:
                return UserResponse(id=row[0], username=row[1])
            return None
        
class ProjectRepository:
    def __init__(self, connection: psycopg.AsyncConnection):
        self.conn = connection

    async def create_project(self, project: Project, userId: int) -> Optional[ProjectInDB]:
        try:
            async with self.conn.transaction():
                async with self.conn.cursor() as cursor:
                    await cursor.execute(
                        "INSERT INTO projects (title, description, user_id) VALUES (%s, %s, %s) RETURNING id",
                        (project.title, project.description, userId)
                    )
                    projectId = await cursor.fetchone()
                    if projectId:
                        return ProjectInDB(id=projectId[0], title=project.title, description=project.description, currentStep=0, riskScoreThreshold=0.1)
                    return None
        except psycopg.IntegrityError:
            return None

    async def get_project_by_id(self, projectId: int, userId: int) -> Optional[ProjectInDB]:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "SELECT title, description, current_step, risk_score_threshold FROM projects WHERE id = %s AND user_id = %s",
                (projectId, userId)
            )
            row = await cursor.fetchone()
            if row:
                return ProjectInDB(id=projectId, title=row[0], description=row[1], currentStep=row[2], riskScoreThreshold=row[3])
            return None

    async def get_projects_by_user_id(self, userId: int) -> list[ProjectInDB]:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "SELECT id, title, description, current_step, risk_score_threshold FROM projects WHERE user_id = %s",
                (userId,)
            )
            rows = await cursor.fetchall()
            return [ProjectInDB(id=row[0], title=row[1], description=row[2], currentStep=row[3], riskScoreThreshold=row[4]) for row in rows]


    async def get_project_risks(self, projectId: int, userId: int) -> list[RiskInDB]:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                """
                SELECT r.id, r.kind, r.title, r.description, r.impact, r.probability, r.contingency, r.fallback
                FROM risks r
                JOIN projects p ON r.project_id = p.id
                WHERE p.id = %s AND p.user_id = %s
                """,
                (projectId, userId)
            )
            rows = await cursor.fetchall()
            if rows:
                return [
                    RiskInDB(
                        id=row[0],
                        kind=row[1],
                        title=row[2],
                        description=row[3],
                        impact=row[4],
                        probability=row[5],
                        contingency=row[6],
                        fallback=row[7],
                        projectId=projectId
                    ) for row in rows
                ]
            return []

    async def add_project_risks(self, projectId, userId, risks_data) -> Optional[list[RiskInDB]]:
        try:
            async with self.conn.transaction():
                async with self.conn.cursor() as cursor:
                    # Verify project ownership
                    await cursor.execute(
                        "SELECT id FROM projects WHERE id = %s AND user_id = %s",
                        (projectId, userId)
                    )
                    project = await cursor.fetchone()
                    if not project:
                        return None  # Project not found or not owned by user

                    # Insert risks
                    inserted_risks = []
                    for risk in risks_data:
                        await cursor.execute(
                            """
                            INSERT INTO risks (project_id, kind, title, description)
                            VALUES (%s, %s, %s, %s)
                            RETURNING id, kind, title, description
                            """,
                            (projectId, risk.kind, risk.title, risk.description)
                        )
                        row = await cursor.fetchone()
                        if row:
                            inserted_risks.append(
                                RiskInDB(
                                    id=row[0],
                                    projectId=projectId,
                                    kind=row[1],
                                    title=row[2],
                                    description=row[3],
                                    impact=None,
                                    probability=None,
                                    contingency=None,
                                    fallback=None
                                )
                            )
                        else:
                            return None  # Insertion failed
                    return inserted_risks
        except psycopg.IntegrityError:
            return None
        
    async def add_project_risks_scores(self, projectId: int, userId: int, scored_risks: list[TrackedScoredRisk], riskScoreThreshold: float) -> bool:
        try:
            async with self.conn.transaction():
                async with self.conn.cursor() as cursor:
                    # Update project's risk score threshold
                    await cursor.execute(
                        """
                        UPDATE projects
                        SET risk_score_threshold = %s
                        WHERE id = %s
                        """,
                        (riskScoreThreshold, projectId)
                    )
                    # Update risks with scores
                    for risk in scored_risks:
                        await cursor.execute(
                            """
                            UPDATE risks
                            SET impact = %s, probability = %s
                            WHERE id = %s AND project_id = %s
                            """,
                            (risk.impact, risk.probability, risk.id, projectId)
                        )
                    return True
        except psycopg.IntegrityError:
            return False
        
    async def add_project_risks_plans(self, projectId: int, userId: int, managed_risks: list[TrackedManagedRisk]) -> bool:
        try:
            async with self.conn.transaction():
                async with self.conn.cursor() as cursor:
                    for risk in managed_risks:
                        await cursor.execute(
                            """
                            UPDATE risks
                            SET contingency = %s, fallback = %s
                            WHERE id = %s AND project_id = %s
                            """,
                            (risk.contingency, risk.fallback, risk.id, projectId)
                        )
                    return True
        except psycopg.IntegrityError:
            return False
        
    