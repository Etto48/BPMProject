import psycopg
from typing import Optional
from models import ProjectInDB, RiskInDB, UserResponse, UserInDB, Project

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
                        return ProjectInDB(id=projectId[0], title=project.title, description=project.description, currentStep=0)
                    return None
        except psycopg.IntegrityError:
            return None

    async def get_project_by_id(self, projectId: int, userId: int) -> Optional[ProjectInDB]:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "SELECT title, description, current_step FROM projects WHERE id = %s AND user_id = %s",
                (projectId, userId)
            )
            row = await cursor.fetchone()
            if row:
                return ProjectInDB(id=projectId, title=row[0], description=row[1], currentStep=row[2])
            return None

    async def get_projects_by_user_id(self, userId: int) -> list[ProjectInDB]:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "SELECT id, title, description, current_step FROM projects WHERE user_id = %s",
                (userId,)
            )
            rows = await cursor.fetchall()
            return [ProjectInDB(id=row[0], title=row[1], description=row[2], currentStep=row[3]) for row in rows]


    async def get_project_risks(self, projectId: int, userId: int) -> Optional[list[RiskInDB]]:
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
            return None

    async def add_project_risks(self, projectId, userId, risks_data):
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
                            raise Exception("Failed to insert risk")
                    return inserted_risks
        except Exception as e:
            return None