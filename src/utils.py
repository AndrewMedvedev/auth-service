import hashlib
import hmac

import bcrypt

from .constants import BYTES_SECRET_KEY_HASH


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
