from sqlmodel import Session, select
from uudex_server.models import EndPoint


def select_endpoint_by_certificate_dn(session: Session, certificate_dn: str) -> EndPoint:
    statement = select(EndPoint).where(EndPoint.certificate_dn == certificate_dn)
    res = session.exec(statement=statement)
    return res.first()


def select_all_endpoints(session: Session) -> list[EndPoint]:
    statement = select(EndPoint)
    res = session.exec(statement=statement)
    return res


# async def select_participant_by_id(session: Session, participant_id: int) -> EndPoint:
#     statement = select(EndPoint).where(EndPoint.participant_id == participant_id)
#     res = session.exec(statement=statement)
#     return res.first()

if __name__ == '__main__':
    from uudex_server.core.settings import get_settings
    from uudex_server.services.database_service import get_db_session

    settings = get_settings(".env-develop")
    session = get_db_session()
    endpoints = select_all_endpoints(session=session)
    for endpoint in endpoints:
        print(endpoint.model_dump_json())
