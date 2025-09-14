from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict, List, Optional

from psycopg import AsyncConnection, AsyncTransaction, IsolationLevel
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

from configs import pg_settings


class PgConnSession:
    def __init__(self, *, conn: AsyncConnection, tx: AsyncTransaction):
        self._conn = conn
        self._tx = tx

    async def fetch_all(self, sql: str) -> List[Dict[str, Any]]:

        async with self._conn.cursor() as cur:
            try:
                await cur.execute(sql)
                return await cur.fetchall()
            except Exception:
                # TODO: sql debug
                raise

    async def fetch_one(self, sql: str) -> Optional[Dict[str, Any]]:

        async with self._conn.cursor() as cur:
            try:
                await cur.execute(sql)
                return await cur.fetchone()
            except Exception:
                # TODO: sql debug
                raise

    async def fetch_val(self, sql: str) -> Any:

        async with self._conn.cursor() as cur:
            try:
                await cur.execute(sql)
                row = await cur.fetchone()
                return None if row is None else next(iter(row.values()))
            except Exception:
                # TODO: sql debug
                raise

    async def execute(self, sql: str) -> Any:

        async with self._conn.cursor() as cur:
            try:
                await cur.execute(sql)
                return cur.statusmessage
            except Exception:
                # TODO: sql debug
                raise

    async def executemany(self, sql: str) -> Any:

        async with self._conn.cursor() as cur:
            try:
                await cur.executemany(sql)
                return cur.statusmessage
            except Exception:
                # TODO: sql debug
                raise

    async def rollback(self, exc):
        await self._tx.__aexit__(type(exc), exc, exc.__traceback__)


class PgPoolManager:
    def __init__(self, dsn, /, *, pool_min_size: int = 1, pool_max_size: int = 10):
        self.__dsn = dsn
        self.__pool_min_size = pool_min_size
        self.__pool_max_size = pool_max_size
        self.__apool = None

    async def open(self):
        if self.__apool is None:

            self.__apool = AsyncConnectionPool(
                conninfo=self.__dsn,
                min_size=self.__pool_min_size,
                max_size=self.__pool_max_size,
                kwargs={"row_factory": dict_row},
                num_workers=1,
                open=False,
            )

            try:
                await self.__apool.open()
            except Exception as ex:
                # TODO: write log to aws
                print(f"postgres open error {ex}")
                raise

    async def close(self):
        if self.__apool is not None:
            try:
                await self.__apool.close()
            except Exception as ex:
                # TODO: write log to aws
                print(f"postgres close error {ex}")
                raise

    @asynccontextmanager
    async def tx(
        self, *, isolation: IsolationLevel = IsolationLevel.READ_COMMITTED, readonly: bool = False
    ) -> AsyncIterator[PgConnSession]:
        if self.__apool is None:
            await self.open()

        conn_cm = self.__apool.connection()
        conn = await conn_cm.__aenter__()

        await conn.set_isolation_level(isolation)
        await conn.set_read_only(readonly)

        tx_cm = conn.transaction()
        await tx_cm.__aenter__()

        try:
            yield PgConnSession(conn, tx_cm)
        except Exception as exc:
            await tx_cm.__aexit__(type(exc), exc, exc.__traceback__)
            raise
        else:
            await tx_cm.__aexit__(None, None, None)
        finally:
            await conn_cm.__aexit__(None, None, None)


pg_pool_manager = PgPoolManager(
    pg_settings.dsn, pool_min_size=pg_settings.POOL_MIN_SIZE, pool_max_size=pg_settings.POOL_MAX_SIZE
)
