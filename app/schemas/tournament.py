from datetime import datetime

from pydantic import BaseModel


class TournamentSchema(BaseModel):
    name: str
    max_players: int
    start_at: datetime


class TournamentSchemaReturn(TournamentSchema):
    id: int
    registered_players: int
