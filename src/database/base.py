from typing import Annotated

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import ARRAY, Boolean, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[
    datetime,
    mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
]

uuid_pk = Annotated[UUID, mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)]

bool_null = Annotated[bool, mapped_column(Boolean, nullable=False, default=False)]

int_null = Annotated[int, mapped_column(nullable=False, unique=True)]

str_null = Annotated[str, mapped_column(nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]
str_uniq = Annotated[str, mapped_column(unique=True)]

list_str = Annotated[list[str], mapped_column(ARRAY(String))]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[uuid_pk]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
