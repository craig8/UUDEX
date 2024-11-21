from sqlmodel import Session, select
from uudex_server.models import EndPoint

from uudex_server.models.endpoint_models import EndPoint
from uudex_server.repos import Repository


class EndpointRepository(Repository[EndPoint]):

    def __init__(self, session: Session):
        super().__init__(EndPoint, session=session, id_field="endpoint_id")

    async def select_endpoint_by_certificate_dn(self, session: Session,
                                                certificate_dn: str) -> EndPoint | None:
        statement = select(EndPoint).where(EndPoint.certificate_dn == certificate_dn)
        res = session.exec(statement=statement)
        return res.first()
