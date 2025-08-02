from pydantic import BaseModel, field_validator, validate_email
from sqlalchemy import UUID

from .database.models import UserModel
from .exeptions import BadRequestHTTPError
from .utils import Hash


class UserSchema(BaseModel):
    email: str
    password: str

    @property
    def to_model(self) -> UserModel:
        return UserModel(
            password=Hash.get_password_hash(self.password),
            email=self.email,
            email_verify=True,
        )

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if validate_email(value):
            return value.lower()
        raise BadRequestHTTPError(message="wrong email")


class GetUserResponse(BaseModel):
    id: UUID
    password: str
