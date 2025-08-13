from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, bool_null, list_str, str_null, str_null_true, str_uniq


class UserModel(Base):
    __tablename__ = "users"

    password: Mapped[str_null]
    email: Mapped[str_null]
    email_verify: Mapped[bool_null]


class IdentityProviderModel(Base):
    __tablename__ = "identity_providers"

    name: Mapped[str_uniq]
    type: Mapped[str]
    scopes: Mapped[list_str]


class UserIdentityModel(Base):
    __tablename__ = "user_identities"

    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), unique=False, nullable=True)
    provider_id: Mapped[UUID] = mapped_column(ForeignKey("identity_providers.id"), unique=False)
    provider_user_id: Mapped[str_uniq]
    email: Mapped[str_null_true]

    __table_args__ = (UniqueConstraint("provider_user_id", name="identity_uq"),)
