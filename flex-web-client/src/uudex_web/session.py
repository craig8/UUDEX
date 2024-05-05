from __future__ import annotations
import atexit
import logging
import os
import time
from typing import Any, Callable, Dict, List, Optional
import urllib.parse
from enum import Enum
from attr import dataclass
from contextlib import contextmanager
import requests

from uudex_api_client import Client
#import uudex_client
#from uudex_client import configurator

__client__: Optional[Client] = None
_log = logging.getLogger(__name__)


@dataclass
class TimedResponse:
    perftime: float
    response: Any


def initialize(client: Client):
    global __client__
    if __client__ is not None:
        raise ValueError("Reinitializing client why are we doing that?")
    __client__ = client

    atexit.register(__cleanup_client__)


def __cleanup_client__():
    global __client__
    __client__ = None


@contextmanager
def client_wrapper() -> Client:
    import os
    for env, value in os.environ.items():
        print(env, value)

    if __client__ is None:
        raise ValueError("Initialize must be called before this method.")

    yield __client__

    #return __client__


def time_request(participant: str, fn: Callable, *args, **kwargs) -> TimedResponse:
    before = time.perf_counter()
    results = fn(*args, **kwargs)
    after = time.perf_counter()
    return TimedResponse(after - before, results)


class ClientApi:

    def __init__(self, site_users: List[str]):
        """Initialize the client api.

        Args:
            all_clients: All available client strings.  Theses must be unique
        """
        self._all_users = site_users
        self._configurations = {}
        self._clients: Dict[str, uudex_client.ApiClient] = {}
        self._local_site: Optional[str] = None

        for item in self._all_users:
            configuration = uudex_client.Configuration()
            configuration.host = "https://127.0.0.1:5000/v1/uudex"
            # configurator.set_values(configuration, item)
            client = uudex_client.ApiClient(configuration)
            self._clients[item] = client
            self._configurations[item] = configuration

    @property
    def user_list(self) -> List[str]:
        return self._all_users

    @property
    def local_site(self) -> str:
        return self._local_site

    @local_site.setter
    def local_site(self, value: str):
        if self._local_site is not None:
            raise ValueError(f"Local site can not be reset!")
        self._local_site = value

    def get_parent_participant(self, connection):
        participant_api = uudex_client.ParticipantApi(self._clients[connection])
        participant = participant_api.get_parent_participant()
        return participant

    def get_discoverable_subjects(self, connection):
        subject_api = uudex_client.SubjectApi(self._clients[connection])
        subjects = subject_api.discover_subjects()
        return subjects

    def get_subscriptions(self, connection):
        try:
            subscription_api = uudex_client.SubscriptionApi(self._clients[connection])
            subscriptions = subscription_api.get_subscriptions()
            return subscriptions
        except ApiException as e:
            if e.status == 404:
                return []
            else:
                raise e

    def publish_message(self, connection, subject_uuid, messages):
        message_list = []
        for message in messages:
            pub_message = uudex_client.MessagePublish(message)
            message_list.append(pub_message)
        subject_api = uudex_client.SubjectApi(self._clients[connection])
        pub_resp = subject_api.publish_message(subject_uuid, body=message_list)
        return pub_resp

    def consume_subscription(self, connection, subscription_uuid):
        subscription_api = uudex_client.SubscriptionApi(self._clients[connection])
        messages = subscription_api.consume_subscription(subscription_uuid)
        return messages

    def consume_subscription(self, connection, subscription_uuid):
        subscription_api = uudex_client.SubscriptionApi(self._clients[connection])
        messages = subscription_api.consume_subscription(subscription_uuid)
        return messages

    def get_subject_acls(self, connection, subject_uuid):
        try:
            subject_acl_api = uudex_client.SubjectAclApi(self._clients[connection])
            acls = subject_acl_api.get_subject_acls(subject_uuid)
            return acls
        except ApiException as e:
            return []

    def get_participants(self, connection):
        participant_api = uudex_client.ParticipantApi(self._clients[connection])
        p = participant_api.admin_get_all_participants()
        return p

    def grant_acl(
        self,
        connection,
        subject_uuid,
        privilege_name,
        grant_scope_name,
        participant_uuid_list,
    ):
        subject_acl_api = uudex_client.SubjectAclApi(self._clients[connection])
        try:
            subject_acl_api.revoke_subject_acl_privilege(subject_uuid, privilege_name)
        except Exception as e:
            pass

        body = uudex_client.SubjectAcl(
            privilege_name=privilege_name,
            grant_scope_name=grant_scope_name,
            participant_uuid_list=participant_uuid_list,
        )
        return subject_acl_api.grant_subject_acl_privilege(subject_uuid, body=body)

    def create_subject(
        self,
        connection,
        subject_name,
        instance_key,
        desc,
        sub_type,
        fulfillment_type,
        dataset_definition_uuid,
    ):
        subject_api = uudex_client.SubjectApi(self._clients[connection])
        body = uudex_client.Subject(
            subject_name=subject_name,
            dataset_instance_key=instance_key,
            description=desc,
            subscription_type=sub_type,
            fulfillment_types_available=fulfillment_type,
            dataset_definition_uuid=dataset_definition_uuid,
        )
        return subject_api.create_subject(body=body)

    def publish_file(self, connection, subject_uuid, message, dataset_name, description):
        uudex_publisher = uudex_client.publish_helper.UudexPublisher(
            self.configurations[connection])
        created_dataset = uudex_publisher.publish(subject_uuid,
                                                  message,
                                                  dataset_name=dataset_name,
                                                  description=description)
        return created_dataset

    def create_subscription(self, connection, subscription_name):
        subscription_api = uudex_client.SubscriptionApi(self._clients[connection])
        body = uudex_client.Subscription(subscription_name=subscription_name,
                                         subscription_state="ACTIVE")
        subscription = subscription_api.create_subscription(body=body)
        return subscription

    def attach_subject(self, connection, subscription_uuid, subject_uuid):
        subscription_api = uudex_client.SubscriptionApi(self._clients[connection])
        body = uudex_client.SubscriptionSubject(subject_uuid=subject_uuid,
                                                preferred_fulfillment_type="DATA_NOTIFY")
        subscription_api.attach_subscription_subject(subscription_uuid, body=body)

    def get_datasets(self, connection, subject_uuid):
        try:
            dataset_api = uudex_client.DatasetApi(self._clients[connection])
            return dataset_api.get_datasets(subject_uuid=subject_uuid,
                                            search_expression=None,
                                            participant_uuid=None)
        except ApiException as e:
            return []

    def get_dataset_payload(self, connection, dataset_uuid):
        dataset_api = uudex_client.DatasetApi(self._clients[connection])
        dataset = dataset_api.get_dataset(dataset_uuid)
        b64_blob = dataset.payload
        if isinstance(b64_blob, str):
            b64_blob = b64_blob.encode("utf-8")    # if string, turn it into byte array first
        blob = base64.b64decode(b64_blob)
        return blob

    def get_new_subject_api(self, connection):
        return uudex_client.SubjectApi(self._clients[connection])

    def get_new_dataset_api(self, connection):
        return uudex_client.DatasetApi(self._clients[connection])

    def get_new_subject_acl_api(self, connection):
        return uudex_client.SubjectAclApi(self._clients[connection])

    def get_new_subscription_api(self, connection):
        return uudex_client.SubscriptionApi(self._clients[connection])


backend_session = requests.Session()
ADMIN_URL = ""


class SaveRequestMethod(Enum):
    POST = "POST"
    PUT = "PUT"


def setup_backend_session():
    global backend_session, ADMIN_URL

    if not ADMIN_URL:
        backend_session.cert = (os.getenv("2030_5_CLIENT_CERT"), os.getenv("2030_5_CLIENT_KEY"))
        backend_session.verify = os.getenv("2030_5_CA_CERT")
        ADMIN_URL = f"https://{os.getenv('2030_5_HOST')}:{os.getenv('2030_5_PORT')}/admin"


def list_endpoint(endpoint: str, start: int = 0, after: int = 0, limit: int = 0) -> str:
    setup_backend_session()
    base_url = ADMIN_URL
    while endpoint.startswith('/'):
        endpoint = endpoint[1:]
    endpoint = urllib.parse.quote(endpoint)
    endpoint += f"?s={start}&a={after}&l={limit}"
    return f"{base_url}/{endpoint}"


def list_parameters(start: int = 0, after: int = 0, limit: int = 0):
    return dict(s=start, a=after, l=limit)


def endpoint(endpoint: str) -> str:
    setup_backend_session()
    base_url = ADMIN_URL
    while endpoint.startswith('/'):
        endpoint = endpoint[1:]
    endpoint = urllib.parse.quote(endpoint)
    return f"{base_url}/{endpoint}"


def get_der_list() -> m.DERList:
    href = endpoint('der')
    list_params = list_parameters()
    return xml_to_dataclass(backend_session.get(href, params=list_params).text)


def send_der(item: m.DER) -> m.DER:
    item_xml = dataclass_to_xml(item)

    if item.href:
        _log.debug("PUTTING data")
        response = backend_session.put(endpoint('der'), data=item_xml)
    else:
        _log.debug("POSTING data")
        response = backend_session.post(endpoint('der'), data=item_xml)

    _log.debug(response.text)

    return xml_to_dataclass(response.text)


def get_enddevice_list() -> m.EndDeviceList:
    href = endpoint('enddevice')
    list_params = list_parameters()
    return xml_to_dataclass(backend_session.get(href, params=list_params).text)


def send_enddevice(item: m.EndDevice) -> m.EndDevice:
    item_xml = dataclass_to_xml(item)

    if item.href:
        _log.debug("PUTTING data")
        response = backend_session.put(endpoint('enddevices'), data=item_xml)
    else:
        _log.debug("POSTING data")
        response = backend_session.post(endpoint('enddevices'), data=item_xml)

    _log.debug(response.text)

    return xml_to_dataclass(response.text)


def get_fsa_list() -> m.FunctionSetAssignmentsList:
    href = endpoint('fsa')
    list_params = list_parameters()
    return xml_to_dataclass(backend_session.get(href, params=list_params).text)


def send_fsa(fsa: m.FunctionSetAssignments) -> m.FunctionSetAssignments:
    item_xml = dataclass_to_xml(fsa)

    if fsa.href:
        _log.debug("PUTTING data")
        response = backend_session.put(endpoint('fsa'), data=item_xml)
    else:
        _log.debug("POSTING data")
        response = backend_session.post(endpoint('fsa'), data=item_xml)

    _log.debug(response.text)

    return xml_to_dataclass(response.text)


def get_program_list() -> m.DERProgramList:
    href = endpoint('programs')
    list_params = list_parameters()
    return xml_to_dataclass(backend_session.get(href, params=list_params).text)


def send_program(program: m.DERProgram) -> m.DERProgram:
    slug = "programs"
    item = program
    item_xml = dataclass_to_xml(program)

    if item.href:
        _log.debug(f"PUTTING {item.__class__.__name__} data: {item_xml}")
        response = backend_session.put(endpoint(slug), data=item_xml)
    else:
        _log.debug(f"POSTING {item.__class__.__name__} data: {item_xml}")
        response = backend_session.post(endpoint(slug), data=item_xml)

    _log.debug(response.text)

    return xml_to_dataclass(response.text)


def get_control_list() -> m.DERControlList:
    href = endpoint('controls')
    list_params = list_parameters()
    return xml_to_dataclass(backend_session.get(href, params=list_params).text)


def send_control(control: m.DERControl) -> m.DERControl:
    slug = "controls"
    item = control
    item_xml = dataclass_to_xml(control)

    if item.href:
        _log.debug(f"PUTTING {item.__class__.__name__} data: {item_xml}")
        response = backend_session.put(endpoint(slug), data=item_xml)
    else:
        _log.debug(f"POSTING {item.__class__.__name__} data: {item_xml}")
        response = backend_session.post(endpoint(slug), data=item_xml)

    _log.debug(response.text)

    return xml_to_dataclass(response.text)


def get_curve_list() -> m.DERCurveList:
    href = endpoint('curves')
    list_params = list_parameters()
    return xml_to_dataclass(backend_session.get(href, params=list_params).text)


def send_curve(curve: m.DERCurve) -> m.DERCurve:
    slug = "curves"
    item = curve
    item_xml = dataclass_to_xml(curve)

    if curve.href:
        _log.debug("PUTTING data")
        response = backend_session.put(endpoint(slug), data=item_xml)
    else:
        _log.debug("POSTING data")
        response = backend_session.post(endpoint(slug), data=item_xml)

    _log.debug(response.text)

    return xml_to_dataclass(response.text)


def get_enddevice_list() -> m.EndDeviceList:
    return xml_to_dataclass(backend_session.get(endpoint('enddevices')).text)


def get_cert_list():
    certs = backend_session.get(endpoint('certs')).json()
    return certs
