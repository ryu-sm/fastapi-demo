from pydantic import BaseModel, Field


class BasicLoginInfo(BaseModel):
    email: str = Field(..., max_length=254)
    plan_password: str = Field(..., min_length=8, max_length=32, alias="password")
