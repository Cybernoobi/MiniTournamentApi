from sqlalchemy.orm import Mapped

from . import Base, int_pk, created_at, list_str


class Tournament(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    max_players: Mapped[int]
    reg_emails: Mapped[list_str]

    created_at: Mapped[created_at]
    start_at: Mapped[created_at]
