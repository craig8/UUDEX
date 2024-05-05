import ssl
from pprint import pprint
from typing import Optional
from threading import Lock
from pathlib import Path

from uudex_api_client.api.participants import get_all_participants
from uudex_api_client.api.subjects import get_all_subjects
from uudex_api_client.client import Client as APIClient
from uudex_api_client.models import Participant, Subject # , Dataset
from functools import lru_cache

from .sessions import SessionId
from .certificates import Certificate, get_certificates, get_ca_certificate_path, get_session_certificate, set_session_certificate



base_url = "https://localhost/api"

# Mapping of certificate path to api client
client_cache: dict[str, APIClient] = {}
session_to_client: dict[SessionId, str] = {}

#api_client_lock = Lock()

def __api_client__ (session_id: SessionId) -> APIClient:
    #api_client_lock.acquire()

    current_cert = get_session_certificate(session_id)
    keypath = current_cert.key_path.as_posix()

    # context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
    # context.load_cert_chain(keyfile=current_cert.key_path.as_posix(),
    #                         certfile=current_cert.crt_path.as_posix())
    # context.load_verify_locations(cafile=get_ca_certificate_path().as_posix())
    # # Create a new api client
    # api_client = APIClient(base_url=base_url, verify_ssl=context)

    api_client = client_cache.get(keypath, None)
    if not api_client:
        # Create context for the connection to the server.
        context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
        context.load_cert_chain(keyfile=current_cert.key_path.as_posix(),
                                certfile=current_cert.crt_path.as_posix())
        context.load_verify_locations(cafile=get_ca_certificate_path().as_posix())
        # Create a new api client
        api_client = APIClient(base_url=base_url, verify_ssl=context)
        client_cache[keypath] = api_client

    return api_client



def get_participants(session_id: SessionId) -> list[Participant]:
    return get_all_participants.sync(client=__api_client__(session_id=session_id)) or []


def get_subjects(session_id: SessionId) -> list[Subject]:
    from http.client import HTTPSConnection
    certs = get_certificates()
    current_cert = certs[0]
    context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
    context.load_cert_chain(keyfile=current_cert.key_path.as_posix(),
                            certfile=current_cert.crt_path.as_posix())
    context.load_verify_locations(cafile=get_ca_certificate_path().as_posix())

    conn = HTTPSConnection("localhost", context=context)
    conn.request('GET', '/api/subjects')
    resp = conn.getresponse()
    print(resp.status, resp.reason)

    return get_all_subjects.sync(client=__api_client__(session_id=session_id)) or []

# def get_datasets() -> list[Dataset]:
#     pass

#    return get_all_subjects_subjects_get.sync(client = __api_client__) or []

#    return get_all_subjects_subjects_get.sync(client=__api_client__) or []
