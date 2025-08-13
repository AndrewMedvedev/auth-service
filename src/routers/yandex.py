from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from ..controllers.yandex import YandexControl
from ..core.constants import PATH_ENDPOINT
from ..core.schemas import YandexCallbackSchema

yandex = APIRouter(prefix=f"{PATH_ENDPOINT}/yandex", tags=["yandex"])


@yandex.get("/link")
async def yandex_generate_url() -> JSONResponse:
    content = await YandexControl().generate_url()
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@yandex.post("/registration")
async def yandex_registration(schema: YandexCallbackSchema) -> JSONResponse:
    content = await YandexControl().registration(schema)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)


@yandex.post("/authentication")
async def yandex_authentication(schema: YandexCallbackSchema) -> JSONResponse:
    content = await YandexControl().authentication(schema)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)
