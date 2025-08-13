from ..settings import settings

PATH_ENDPOINT = "/api/v1"
MIN_STATUS_CODE = 100
GOOD_STATUS_CODE = 200
BYTES_SECRET_KEY_HASH = bytes(settings.secret_settings.secret_key_hash, "utf-8")
