import psycopg
from typing import Optional
from models import UserResponse, UserInDB, ProjectData

class UserRepository:
    def __init__(self, connection: psycopg.AsyncConnection):
        self.conn = connection

    async def create_user(self, username: str, password_hash: str) -> Optional[UserResponse]:
        """Create a new user in the database"""
        try:
            async with self.conn.transaction():
                async with self.conn.cursor() as cursor:
                    await cursor.execute(
                        "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id, username",
                        (username, password_hash)
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
                return UserInDB(id=row[0], username=row[1], password_hash=row[2])
            return None

    async def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """Get user by ID"""
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "SELECT id, username FROM users WHERE id = %s",
                (user_id,)
            )
            row = await cursor.fetchone()
            if row:
                return UserResponse(id=row[0], username=row[1])
            return None
        
class ProjectRepository:
    def __init__(self, connection: psycopg.AsyncConnection):
        self.conn = connection

    async def create_project(self, project: ProjectData, user_id: int) -> None:
        async with self.conn.transaction():
            async with self.conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO projects (name, description, user_id) VALUES (%s, %s, %s)",
                    (project.name, project.description, user_id)
                )

    async def get_project_by_id(self, project_id: int, user_id: int) -> Optional[ProjectData]:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "SELECT name, description FROM projects WHERE id = %s AND user_id = %s",
                (project_id, user_id)
            )
            row = await cursor.fetchone()
            if row:
                return ProjectData(name=row[0], description=row[1])
            return None
        
    async def get_projects_by_user_id(self, user_id: int) -> list[ProjectData]:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "SELECT name, description FROM projects WHERE user_id = %s",
                (user_id,)
            )
            rows = await cursor.fetchall()
            return [ProjectData(name=row[0], description=row[1]) for row in rows]