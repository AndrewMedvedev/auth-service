from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from ..controllers import AuthControl
from ..core.constants import PATH_ENDPOINT
from ..core.schemas import UserSchema

auth = APIRouter(prefix=f"{PATH_ENDPOINT}", tags=["auth"])


@auth.post("/registration")
async def registration(schema: UserSchema) -> JSONResponse:
    result = await AuthControl().registration(schema)
    return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)


@auth.post("/authentication")
async def authentication(schema: UserSchema) -> JSONResponse:
    result = await AuthControl().authentication(schema)
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)
