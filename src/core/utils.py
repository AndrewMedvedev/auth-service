from typing import Any

import hashlib
import hmac

import bcrypt

from .constants import BYTES_SECRET_KEY_HASH, GOOD_STATUS_CODE
from .exeptions import NotFoundHTTPError


class Hash:
    @staticmethod
    def get_password_hash(password: str) -> str:
        peppered_password = hmac.new(
            BYTES_SECRET_KEY_HASH, password.encode("utf-8"), hashlib.sha256
        ).digest()
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(peppered_password, salt)
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        peppered_password = hmac.new(
            BYTES_SECRET_KEY_HASH, password.encode("utf-8"), hashlib.sha256
        ).digest()
        return bcrypt.checkpw(peppered_password, hashed_password.encode("utf-8"))


async def valid_answer(response: Any) -> dict:
    if response.status != GOOD_STATUS_CODE:
        raise NotFoundHTTPError
    return await response.json()
