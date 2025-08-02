from sqlalchemy.orm import Mapped

from .db_configs import Base, bool_null, str_null, uuid_pk


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid_pk]
    password: Mapped[str_null]
    email: Mapped[str_null]
    email_verify: Mapped[bool_null]
