from contextlib import asynccontextmanager

from fastapi import FastAPI

from configs import basic_settings


from app.routers import router_auths


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: befor sartup
    yield
    # TODO: after startup


app = FastAPI(docs_url=None, redoc_url=None, root_path=f"/api/v{basic_settings.VERSION}", lifespan=lifespan)

app.include_router(router_auths)


if __name__ == "__main__":
    from uvicorn import run

    run("main:app", host="0.0.0.0", port=8000, reload=True)
