from __future__ import annotations

from typing import Literal

from abc import ABC, abstractmethod
from urllib.parse import urlencode
from uuid import UUID, uuid4

from authlib.common.security import generate_token
from authlib.oauth2.rfc7636 import create_s256_code_challenge
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    SecretStr,
    field_serializer,
    field_validator,
    validate_email,
)

from ..settings import settings
from .exeptions import BadRequestHTTPError
from .utils import Hash


class UserSchema(BaseModel):
    email: EmailStr
    password: SecretStr

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if validate_email(value):
            return value.lower()
        raise BadRequestHTTPError(message="wrong email")

    @field_serializer("password")
    @classmethod
    def serialize_secret(cls, value: SecretStr) -> str:
        return Hash.get_password_hash(value.get_secret_value())


class IdentityProviderSchema(BaseModel):
    name: str
    type: str
    scopes: list[str]


class UserIdentitySchema(BaseModel):
    provider_id: UUID | None = None
    provider_user_id: str
    email: str

    @field_serializer("email")
    @classmethod
    def serialize_email(cls, value: str) -> str:
        return value.lower()


class UserResponse(BaseModel):
    id: UUID
    password: str


class Codes(BaseModel):
    state: str
    code_verifier: str
    code_challenge: str

    @classmethod
    def generate(cls) -> Codes:
        verifier = generate_token(64)
        return cls(
            state=str(uuid4()),
            code_verifier=verifier,
            code_challenge=create_s256_code_challenge(verifier),
        )


class VKRedirectSchema(BaseModel):
    client_id: str = settings.vk_settings.vk_app_id
    redirect_uri: str = settings.vk_settings.vk_redirect_uri

    def to_url(self, state: str, code_challenge: str) -> str:
        query = urlencode({
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "state": state,
            "scope": "email",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        })
        return f"{settings.vk_settings.vk_auth_url}?{query}"


class YandexRedirectSchema(BaseModel):
    client_id: str = settings.yandex_settings.yandex_app_id

    def to_url(self, state: str, code_challenge: str) -> str:
        query = urlencode({
            "client_id": self.client_id,
            "response_type": "code",
            "state": state,
            "scope": "login:info login:email",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        })
        return f"{settings.yandex_settings.yandex_auth_url}?{query}"


class BaseCallbackSchema(BaseModel, ABC):
    code: str
    state: str

    @abstractmethod
    def to_dict(self, code_verifier: str) -> dict: ...


class YandexCallbackSchema(BaseCallbackSchema):
    def to_dict(self, code_verifier: str) -> dict:
        return {
            "grant_type": "authorization_code",
            "code": self.code,
            "client_id": settings.yandex_settings.yandex_app_id,
            "client_secret": settings.yandex_settings.yandex_app_secret,
            "code_verifier": code_verifier,
        }


class VKCallbackSchema(BaseCallbackSchema):
    device_id: str

    def to_dict(self, code_verifier: str) -> dict:
        return {
            "grant_type": "authorization_code",
            "code": self.code,
            "code_verifier": code_verifier,
            "client_id": settings.vk_settings.vk_app_id,
            "device_id": self.device_id,
            "redirect_uri": settings.vk_settings.vk_redirect_uri,
            "state": self.state,
        }


class VKGetDataSchema(BaseModel):
    access_token: str
    user_id: str = Field(exclude=True)
    client_id: str = settings.vk_settings.vk_app_id


class YandexGetDataSchema(BaseModel):
    oauth_token: str
    format: Literal["json"] = "json"
