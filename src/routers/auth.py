from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from ..constants import PATH_ENDPOINT
from ..controllers import AuthControl
from ..schemas import UserSchema

auth = APIRouter(prefix=f"{PATH_ENDPOINT}authorization", tags=["authorization"])


@auth.post("/registration")
async def registration(schema: UserSchema) -> JSONResponse:
    result = await AuthControl().registration(schema)
    return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)


@auth.post("/login")
async def login(schema: UserSchema) -> JSONResponse:
    result = await AuthControl().login_email(schema)
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)
