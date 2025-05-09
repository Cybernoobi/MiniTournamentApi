from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.exceptions import TournamentNotFound, TournamentFull, TournamentEmailAlreadyRegistered
from app.schemas.tournament import TournamentSchema, TournamentSchemaReturn
from app.schemas.user import UserSchema
from app.services.tournament import TournamentManager

router = APIRouter(prefix="/tournaments")


@router.post("/", status_code=status.HTTP_201_CREATED, name='Создание турнира', response_model=dict[str, str])
async def create_tournament(tournament: TournamentSchema, db: AsyncSession = Depends(get_db)):
    """Создание турнира"""
    try:
        await TournamentManager(session=db).create_tournament(
            name=tournament.name,
            max_players=tournament.max_players,
            start_at=tournament.start_at
        )
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{tournament_id}", name='Информации о турнире')
async def get_tournament(tournament_id: int, db: AsyncSession = Depends(get_db)) -> TournamentSchemaReturn:
    """Получение информации о турнире"""
    try:
        return await TournamentManager(session=db).get_tournament(tournament_id)

    except TournamentNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Турнир не найден')


@router.post("/{tournament_id}/register", name='Регистрация в турнире')
async def register_to_tournament(tournament_id: int, user: UserSchema, db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """Регистрация в турнире"""
    try:
        await TournamentManager(session=db).register_player(tournament_id, user.email)
        return {"status": "success"}

    except TournamentNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Турнир не найден')

    except TournamentFull:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Турнир полон')

    except TournamentEmailAlreadyRegistered:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Этот email уже зарегистрирован в этом турнире')
