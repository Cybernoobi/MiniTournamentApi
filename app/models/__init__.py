from datetime import datetime
from typing import Annotated

from sqlalchemy import func, JSON
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import DeclarativeBase, mapped_column, declared_attr


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"


int_pk = Annotated[int, mapped_column(primary_key=True)]
str_uniq = Annotated[str, mapped_column(unique=True)]
list_str = Annotated[list[str], mapped_column(MutableList.as_mutable(JSON), default=list)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]


from .tournament import Tournament