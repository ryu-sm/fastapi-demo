from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app import utils
from app import models
from app import consts

router = APIRouter()


@router.post("/login")
async def basic_login(data: models.BasicLoginInfo):
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": utils.parse_msg("E0102")})
