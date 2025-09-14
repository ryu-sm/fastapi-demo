from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app import utils
from app import models
from app import consts
from app import crud


from app.dependencies.database import get_pg_pool, PgPoolManager

router = APIRouter()


@router.post("/user")
async def new_user(data: models.NewUser, pg_pool: PgPoolManager = Depends(get_pg_pool)):

    async with pg_pool.tx() as conn:
        try:
            user = await crud.query_user_with_email(conn, email=data.email)

            if user:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "email is registed."})

            new_user_id = await crud.insert_user(conn, data)

            return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "created ok."})
        except Exception as ex:
            print(ex)
            await conn.rollback(ex)
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "system"})
