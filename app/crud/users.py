from uuid import UUID
from app.core import PgConnSession

from app import models


async def query_user_with_email(conn: PgConnSession, email: str) -> dict:
    sql = f"""
    SELECT
        id,
        username,
        email
    FROM
        users
    WHERE
        email = '{email}';
    """
    return await conn.fetch_one(sql)


async def insert_user(conn: PgConnSession, user: models.NewUser) -> UUID:
    sql = f"""
    INSERT INTO users (username, email) VALUES ('{user.username}', '{user.email}')
    RETURNING id;
    """
    return await conn.fetch_val(sql)
