import psycopg
from typing import Optional
from models import UserResponse

class UserDB:
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

    async def get_user_by_username(self, username: str) -> Optional[tuple]:
        """Get user by username, returns (id, username, password_hash)"""
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "SELECT id, username, password_hash FROM users WHERE username = %s",
                (username,)
            )
            return await cursor.fetchone()

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