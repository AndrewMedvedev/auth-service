from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from ..controllers.vk import VKControl
from ..core.constants import PATH_ENDPOINT
from ..core.schemas import VKCallbackSchema

vk = APIRouter(prefix=f"{PATH_ENDPOINT}/vk", tags=["vk"])


@vk.get("/link")
async def vk_generate_url() -> JSONResponse:
    content = await VKControl().generate_url()
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@vk.post("/registration")
async def vk_registration(schema: VKCallbackSchema) -> JSONResponse:
    content = await VKControl().registration(schema)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)


@vk.post("/authentication")
async def vk_authentication(schema: VKCallbackSchema) -> JSONResponse:
    content = await VKControl().authentication(schema)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)
