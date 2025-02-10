from typing import Annotated
from fastapi import APIRouter, Depends, Request
from sqlmodel import Session
from uudex_server.models.participant_models import Participant, ParticipantCreate
from uudex_server.services.database_service import get_db_session
from uudex_server.repos import participant_repositories as pr
from uudex_server.endpoints import SessionAndUser

participants_router = APIRouter(prefix="/participants")
participant_router = APIRouter(prefix="/participant")


@participants_router.get("/")
async def get_all_participants(
        common: Annotated[SessionAndUser, Depends(SessionAndUser)]) -> list[Participant]:

    #session: Annotated[Session, Depends(get_db_session)]) -> list[Participant]:
    participants: list[Participant] = await pr.select_all_participants(session=common.session)
    return participants


@participants_router.post("/", operation_id="create_participant")
async def create_participant(participant_create: ParticipantCreate,
                             session: Annotated[Session, Depends(get_db_session)]) -> Participant:

    part: Participant(**participant_create.model_dump())
    part2 = await pr.ParticipantRepository(session=session).create(part)

    return part2
