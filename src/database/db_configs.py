from typing import Annotated

from datetime import datetime
from uuid import uuid4

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

created_at = Annotated[datetime, mapped_column(server_default=func.now())]
uuid_pk = Annotated[UUID, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)]
str_null = Annotated[str, mapped_column(nullable=False)]
bool_null = Annotated[bool, mapped_column(nullable=False)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[created_at]
