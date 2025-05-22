from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import hashlib
from dotenv import load_dotenv
import os
import uuid
from uuid import UUID


def generate_uuid():
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_table"
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        default=uuid.uuid4,
    )
    nome: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), index=True)
    senha: Mapped[str] = mapped_column(String(100))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.nome!r}, email={self.email!r}, senha={self.senha!r})"


class UserIn(User):
    def __init__(self, **kw):
        super().__init__(**kw)
