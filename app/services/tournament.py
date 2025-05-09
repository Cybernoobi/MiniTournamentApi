from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import TournamentEmailAlreadyRegistered, TournamentFull, TournamentNotFound
from app.models.tournament import Tournament
from app.schemas.tournament import TournamentSchemaReturn


class TournamentManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_tournament(self, name: str, max_players: int, start_at: str | datetime):
        tournament = Tournament(name=name, max_players=max_players, start_at=datetime.fromisoformat(str(start_at)))
        self.session.add(tournament)
        await self.session.commit()

    async def get_tournament(self, tournament_id: int) -> TournamentSchemaReturn:
        result = await self.session.execute(
            select(Tournament).where(Tournament.id == tournament_id)
        )

        if res := result.scalar_one_or_none():
            res.registered_players = len(res.reg_emails)
            return TournamentSchemaReturn(**res.__dict__)
        else:
            raise TournamentNotFound

    async def register_player(self, tournament_id: int, email: str):
        result = await self.session.execute(
            select(Tournament).where(Tournament.id == tournament_id)
        )

        tournament: Tournament = result.scalar_one_or_none()

        if tournament is None:
            raise TournamentNotFound

        if email in tournament.reg_emails:
            raise TournamentEmailAlreadyRegistered()

        if len(tournament.reg_emails) >= tournament.max_players:
            raise TournamentFull()

        tournament.reg_emails.append(email)
        await self.session.commit()
