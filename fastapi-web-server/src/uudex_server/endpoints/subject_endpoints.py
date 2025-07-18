from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlalchemy.ext.asyncio import AsyncSession

from uudex_server.models.subject_models import Subject, SubjectCreate
from uudex_server.services.database_service import get_db_session, get_db
from uudex_server.services.authentication_service import get_request_user
from uudex_server.models.authenticated_user import AuthenticatedUser
#from uudex_server.services.authentication_service import get_auth_service
from uudex_server.repos import subscription_and_subject_repositories as pr
#from uudex_server import Settings, get_settings
from uudex_server.services.message_services.base import UUDEXBrokerService
from uudex_server.services.message_services import create_broker_service
from uudex_server.models.core_datatypes import Message

from . import SessionAndUser
from ..models.subject_models import Subject, SubjectCreate
from ..services.database_service import get_db_session
from ..services.authentication_service import get_request_user
from ..models.authenticated_user import AuthenticatedUser
from ..repos import subscription_and_subject_repositories as pr
from ..core import Settings, get_settings
from ..services.message_services.base import UUDEXBrokerService
from ..services.message_services import create_broker_service
from ..models.core_datatypes import Message

subjects_router = APIRouter(prefix="/subjects")
subject_router = APIRouter(prefix="/subject")

# Create v1 parent router
v1_router = APIRouter(prefix="/v1", tags=["v1"])
v1_router.include_router(subjects_router, tags=["v1", "subjects"])
v1_router.include_router(subject_router, tags=["v1", "subjects"])

# @subject_router.post("/", operation_id="create_subject")
# async def create_subject(session: Annotated[Session, Depends(get_db_session)],
#         user: Annotated[AuthenticatedUser, Depends(get_request_user)],
#         subject: SubjectCreate) -> Subject:
#     return await pr.create_subject(session=session, user=user, subject=subject)


@subjects_router.get("/", operation_id="get_all_subjects")
async def get_all_subjects(session: AsyncSession = Depends(get_db)) -> list[Subject]:
    repo = pr.SubjectRepository(session)
    return await repo.select_all()


@subjects_router.post("/", operation_id="create_subject")
async def create_subject(
    subject: SubjectCreate,
    session: AsyncSession = Depends(get_db),
    broker: UUDEXBrokerService = Depends(
        lambda: create_broker_service(get_settings().messagebus_connection)),
    user: AuthenticatedUser = Depends(get_request_user)
) -> Subject:
    subject.owner_participant_id = user.endpoint.participant_id
    subject.dataset_definition_id = 1

    #subj = Subject(**subject.dict())
    #subjectsubj.owner_participant_id = user.endpoint.participant_id
    #subj.dataset_definition_id = 1 # AGC-INFO - This is a placeholder until we have a dataset definition
    subj: Subject = await pr.create_subject(session=session, subject=subject)
    broker.create_subject(subject_name=subj.subject_name, subject_uuid=subj.subject_uuid)
    return subj


@subject_router.get("/{subject_id}")
async def get_subject_by_id(subject_id: int,
                            session: Annotated[Session, Depends(get_db_session)]) -> Subject:
    subject: Subject = await pr.select_subject_by_id(session=session, subject_id=subject_id)
    return subject


@subjects_router.post("/{subject_uuid}/publish", operation_id="publish_messages_to_subject")
async def publish_messages_to_subject(
        subject_uuid: str, messages: list[str], session: Annotated[Session,
                                                                   Depends(get_db_session)],
        user: Annotated[AuthenticatedUser, Depends(get_request_user)]) -> None:
    pass


# @subject_router.get("/me")
# async def get_subject_by_id() -> Participant:
#     subject = Participant(
#         subject_id=1,
#         subject_uuid="1",
#         subject_short_name="me",
#         subject_long_name="me",
#         description="me",
#         root_org_sw="Y",
#         active_sw="Y",
#     )
#     return subject
#     # subject: Participant = await pr.select_subject_by_id(session=session, subject_id=subject_id)
#     # return subject
