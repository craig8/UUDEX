from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from uudex_server.models.subject_models import Subject
from uudex_server.services.database_service import get_db_session
from uudex_server.repos import subject_repository as pr

subjects_router = APIRouter(prefix="/subjects")
subject_router = APIRouter(prefix="/subject")


@subjects_router.get("/")
async def get_all_subjects(session: Annotated[Session, Depends(get_db_session)]) -> list[Subject]:
    subjects: list[Subject] = pr.select_all_subjects(session=session)
    return subjects


@subject_router.get("/{subject_id}")
async def get_subject_by_id(subject_id: int,
                            session: Annotated[Session, Depends(get_db_session)]) -> Subject:
    subject: Subject = await pr.select_subject_by_id(session=session, subject_id=subject_id)
    return subject
