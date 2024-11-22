from sqlmodel import Session

import uudex_server.models as m
from uudex_server.repos import Repository


class ParticipantRepository(Repository[m.Participant]):

    def __init__(self, session: Session):
        super().__init__(m.Participant, session=session, id_field="participant_id")


class ParticipantVisibilityRepository(Repository[m.ParticipantVisibility]):

    def __init__(self, session: Session):
        super().__init__(m.Participant, session=session, id_field="exposed_by_id")
