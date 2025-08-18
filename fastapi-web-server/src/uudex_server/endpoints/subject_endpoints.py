from fastapi import APIRouter, Depends, HTTPException

from uudex_server.core import get_settings
from uudex_server.core.dependencies import SessionDep, UserDep
from uudex_server.models.subject_models import Subject, SubjectCreate
from uudex_server.repos import subscription_and_subject_repositories as pr
from uudex_server.services.message_services import create_broker_service
from uudex_server.services.message_services.base import UUDEXBrokerService

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
async def get_all_subjects(session: SessionDep) -> list[Subject]:
    repo = pr.SubjectRepository(session)
    return await repo.select_all()


@subjects_router.post("/", operation_id="create_subject")
async def create_subject(
    subject: SubjectCreate,
    session: SessionDep,
    user: UserDep,
    broker: UUDEXBrokerService = Depends(
        lambda: create_broker_service(get_settings().messagebus_connection)
    ),
) -> Subject:
    subject.owner_participant_id = user.endpoint.participant_id
    subject.dataset_definition_id = 1

    # Convert SubjectCreate to Subject
    subject_data = subject.model_dump()
    db_subject = Subject(**subject_data)

    repo = pr.SubjectRepository(session)
    subj: Subject = await repo.create(db_subject)
    broker.create_subject(subject_name=subj.subject_name, subject_uuid=subj.subject_uuid)
    return subj


@subject_router.get("/{subject_id}")
async def get_subject_by_id(subject_id: int, session: SessionDep) -> Subject:
    subject: Subject | None = await pr.select_subject_by_id(session=session, subject_id=subject_id)
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject


@subjects_router.get("/discover", operation_id="discover_subjects")
async def discover_subjects(session: SessionDep, user: UserDep) -> list[Subject]:
    """
    Discover subjects that the authenticated user is authorized to view.

    Returns subjects based on:
    - Admin users: All subjects
    - Regular users: Only subjects owned by their participant
    """
    repo = pr.SubjectRepository(session)

    if user.is_admin():
        # Admin users can see all subjects
        return await repo.select_all()
    else:
        # Regular users can only see subjects owned by their participant
        # Access participant_id safely by merging the endpoint into current session
        endpoint = await session.merge(user.endpoint)
        participant_id = endpoint.participant_id

        # Get subjects owned by the user's participant
        subjects = await pr.select_all_subjects(session=session, participant_id=participant_id)
        return subjects


@subjects_router.post("/{subject_uuid}/publish", operation_id="publish_messages_to_subject")
async def publish_messages_to_subject(
    subject_uuid: str, messages: list[str], session: SessionDep, user: UserDep
) -> None:
    # TODO: Implement message publishing logic
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
