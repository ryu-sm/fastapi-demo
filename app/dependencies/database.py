from app.core import pg_pool_manager, PgPoolManager, PgConnSession


async def get_pg_pool() -> PgPoolManager:

    await pg_pool_manager.open()

    return pg_pool_manager
