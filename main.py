from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import auth

app = FastAPI(title="Registration service")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


def include_routers(app: FastAPI):
    app.include_router(auth)


include_routers(app)
