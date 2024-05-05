from typing import Annotated
from fastapi import APIRouter, Depends, Request
from sqlmodel import Session
from uudex_server.models.participant_models import Participant
from uudex_server.services.database_service import get_db_session
from uudex_server.repos import participant_repository as pr

participants_router = APIRouter(prefix="/participants")
participant_router = APIRouter(prefix="/participant")


@participants_router.get("/")
async def get_all_participants(
        session: Annotated[Session, Depends(get_db_session)]) -> list[Participant]:
    participants: list[Participant] = pr.select_all_participants(session=session)
    return participants


@participant_router.get("/me")
async def get_participant_by_id() -> Participant:
    participant = Participant(
        participant_id=1,
        participant_uuid="1",
        participant_short_name="me",
        participant_long_name="me",
        description="me",
        root_org_sw="Y",
        active_sw="Y",
    )
    return participant
    # participant: Participant = await pr.select_participant_by_id(session=session, participant_id=participant_id)
    # return participant


@participant_router.get("/{participant_id}")
async def get_participant_by_id(
        participant_id: int, session: Annotated[Session, Depends(get_db_session)]) -> Participant:
    participant: Participant = await pr.select_participant_by_id(session=session,
                                                                 participant_id=participant_id)
    return participant
