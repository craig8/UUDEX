from uudex_server.models.participant_models import Participant
from uudex_server.repos import Repository


class ParticipantRepository(Repository[Participant]):

    def __init__(self):
        super().__init__(Participant, id_field="participant_id")


# async def create(session: Session, participant: ParticipantCreate) -> Participant:
#     participant = Participant(**participant.model_dump())
#     session.add(participant)
#     session.commit()
#     session.refresh(participant)
#     return participant
#
#
# async def select_all(session: Session) -> list[Participant]:
#     statement = select(Participant)
#     res = session.exec(statement=statement)
#     return list(res)
#
#
# async def select_by_id(session: Session, participant_id: int) -> Awaitable[Participant] | None:
#     statement = select(Participant).where(Participant.participant_id == participant_id)
#     res = session.exec(statement=statement)
#     return res.first()
#
# async def delete(session: Session, participant_remove: ParticipantRemove) -> None:
#     statement = _delete(Participant).where(
#         (Participant.participant_id == participant_remove.participant_id))
#     session.exec(statement)
#     session.commit()
#
#
# async def update(session: Session, participant: Participant) -> Participant:
#     session.add(participant)
#     session.commit()
#     session.refresh(participant)
#     return participant
