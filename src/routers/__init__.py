from fastapi import APIRouter

from .auth import auth
from .vk import vk
from .yandex import yandex

router = APIRouter()

router.include_router(auth)
router.include_router(vk)
router.include_router(yandex)
