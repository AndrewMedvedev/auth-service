import typing as t

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.core.exeptions import (
    BadRequestHTTPError,
    BaseHTTPError,
    HTTPException,
    InternalHTTPError,
    JSONError,
)
from src.routers import router

app = FastAPI(title="Registration service")


@app.exception_handler(Exception)
def handler(
    _request: Request,
    exception: t.Union[
        Exception,
        BaseException,
    ],
    description: t.Optional[str] = None,
) -> JSONResponse:
    if isinstance(exception, HTTPException):
        exception = BaseHTTPError(str(exception), exception.status_code)
    if isinstance(exception, BaseHTTPError):
        pass
    elif isinstance(exception, (AttributeError, ValueError, KeyError, TypeError)):
        description = description if description is not None else str(exception)
        exception = BadRequestHTTPError()

    else:
        exception = InternalHTTPError()

    return JSONResponse(
        content=JSONError.create(exception, description).to_dict(),
        status_code=exception.code,
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


def include_routers(app: FastAPI):
    app.include_router(router)


include_routers(app)
