from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from uudex_server.models.subject_models import Subject
from uudex_server.services.database_service import get_db_session
from uudex_server.services.authentication_service import get_request_user
from uudex_server.models.authenticated_user import AuthenticatedUser
#from uudex_server.services.authentication_service import get_auth_service
from uudex_server.repos import subject_repository as pr

subjects_router = APIRouter(prefix="/subjects")
subject_router = APIRouter(prefix="/subject")


@subjects_router.get("/", operation_id="get_all_subjects")
async def get_all_subjects(
        session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[AuthenticatedUser, Depends(get_request_user)]) -> list[Subject]:
    subjects: list[Subject] = await pr.select_all_subjects(session=session, user=user)
    return subjects


@subject_router.get("/{subject_id}")
async def get_subject_by_id(subject_id: int,
                            session: Annotated[Session, Depends(get_db_session)]) -> Subject:
    subject: Subject = await pr.select_subject_by_id(session=session, subject_id=subject_id)
    return subject


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
