from sqlmodel import Session, select
from uudex_server.models import Participant


def select_all_participants(session: Session) -> list[Participant]:
    statement = select(Participant)
    res = session.exec(statement=statement)
    return res


async def select_participant_by_id(session: Session, participant_id: int) -> Participant:
    statement = select(Participant).where(Participant.participant_id == participant_id)
    res = session.exec(statement=statement)
    return res.first()
