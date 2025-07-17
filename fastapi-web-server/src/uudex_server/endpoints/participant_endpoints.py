from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uudex_server.models.participant_models import Participant, ParticipantCreate
from uudex_server.services.database_service import get_db
from uudex_server.repos import participant_repositories as pr
from uudex_server.models.common_types import YNSwitch

participants_router = APIRouter(prefix="/participants")
participant_router = APIRouter(prefix="/participant")


@participants_router.get("/")
async def get_all_participants(session: AsyncSession = Depends(get_db)) -> list[Participant]:
    repo = pr.ParticipantRepository(session)
    return await repo.select_all()


@participants_router.post("/", operation_id="create_participant")
async def create_participant(
    participant_create: ParticipantCreate, session: AsyncSession = Depends(get_db)) -> Participant:
    db_participant = Participant(**participant_create.model_dump())
    repo = pr.ParticipantRepository(session)
    return await repo.create(db_participant)
