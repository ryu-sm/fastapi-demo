from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool


from configs import pg_settings


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


pg_pool_manager = PgPoolManager(
    pg_settings.dsn, pool_min_size=pg_settings.POOL_MIN_SIZE, pool_max_size=pg_settings.POOL_MAX_SIZE
)
