import pytest
import uuid
from sqlmodel import Session

import uudex_server.models as m
from uudex_server.models.subscription_subject_models import SubscriptionSubject, SubscriptionSubjectCreate, SubscriptionSubjectDelete
from uudex_server.repos import ParticipantRepository, EndpointRepository, SubscriptionRepository, SubjectRepository, \
    DatasetRepository, DatasetDefinitionRepository
from uudex_server.repos.subscription_subject_repository import SubscriptionSubjectRepository
from uudex_server.models.subscription_models import Subscription
from uudex_server.models.subject_models import Subject


@pytest.fixture(name="participant", scope="function")
@pytest.mark.asyncio
async def participant_fixture(session: Session,
                              participant_repo: ParticipantRepository) -> m.Participant:
    participant_create = m.ParticipantCreate(participant_uuid=str(uuid.uuid4()),
                                             participant_short_name="short1",
                                             participant_long_name="long1",
                                             description="desc1",
                                             root_org_sw="Y",
                                             active_sw="Y")
    created_participant = await participant_repo.create(session, participant_create)
    return created_participant


@pytest.fixture(name="dataset", scope="function")
@pytest.mark.asyncio
async def dataset_fixture(session: Session, participant: m.Participant, subject: m.Subject,
                          dataset_repo: DatasetRepository) -> m.Dataset:
    dataset_create = m.DatasetCreate(dataset_uuid=str(uuid.uuid4()),
                                     dataset_name="Test Dataset",
                                     description="This is a test description",
                                     properties="{}",
                                     payload=b"",
                                     payload_size=0,
                                     payload_md5_hash="md5hash",
                                     payload_compression_algorithm="algorithm",
                                     version_number=1,
                                     owner_participant_id=participant.participant_id,
                                     subject_id=subject.subject_id)
    created_dataset = await dataset_repo.create(session, dataset_create)
    return created_dataset


@pytest.fixture(name="endpoint", scope="function")
@pytest.mark.asyncio
async def endpoint_fixture(session: Session, participant: m.Participant,
                           endpoint_repo: EndpointRepository) -> m.EndPoint:
    endpoint = m.EndPointCreate(endpoint_uuid="uuid1",
                                endpoint_user_name="user1",
                                certificate_dn="dn1",
                                description="desc1",
                                uudex_administrator_sw="Y",
                                participant_administrator_sw="Y",
                                participant_id=participant.participant_id)
    created_endpoint = await endpoint_repo.create(session, endpoint)
    return created_endpoint


@pytest.fixture(name="subscription", scope="function")
@pytest.mark.asyncio
async def subscription_fixture(session: Session, endpoint: m.EndPoint,
                               subscription_repo: SubscriptionRepository):
    subscription_create = Subscription(subscription_uuid=str(uuid.uuid4()),
                                       subscription_name="Test Subscription",
                                       subscription_state="ACTIVE",
                                       description="This is a test subscription",
                                       owner_endpoint_id=endpoint.endpoint_id)
    created_subscription = subscription_repo.create(session, subscription_create)
    return created_subscription


@pytest.fixture(name="subject")
@pytest.mark.asyncio
async def subject_fixture(session: Session, participant: m.Participant, dataset: m.Dataset,
                          subject_repo: SubjectRepository):
    subject_create = m.SubjectCreate(
        subject_uuid="uuid1",
        subject_name="name1",
        dataset_instance_key="key1",
        subscription_type="sub_type1",
        fulfillment_types_available="fulfillment1",
        full_queue_behavior="behavior1",
        max_queue_size_kb=1000,
        max_message_count=10,
        priority=1,
        backing_exchange_name="exchange1",
        owner_participant_id=participant.participant_id,
        dataset_definition_id=dataset.dataset_id,
    )
    created_subject = await subject_repo.create(session, subject_create)
    return created_subject


@pytest.mark.asyncio
async def setup_subscription_and_subject(session: Session, participant_repo: ParticipantRepository,
                                         subject_repo: SubjectRepository,
                                         endpoint_repo: EndpointRepository,
                                         subscription_repo: SubscriptionRepository,
                                         dataset_definition_repo: DatasetDefinitionRepository):
    dataset_definition_create = m.DatasetDefinitionCreate(
        dataset_definition_uuid=str(uuid.uuid4()),
        dataset_definition_name="Test Dataset Definition",
        description="This is a test description")
    created_dataset_definition = await dataset_definition_repo.create(
        session, dataset_definition_create)

    participant_create = m.ParticipantCreate(participant_uuid=str(uuid.uuid4()),
                                             participant_short_name="short1",
                                             participant_long_name="long1",
                                             description="desc1",
                                             root_org_sw="Y",
                                             active_sw="Y")
    created_participant = await participant_repo.create(session, participant_create)

    subject_create = m.SubjectCreate(
        subject_uuid="uuid1",
        subject_name="name1",
        dataset_instance_key="key1",
        subscription_type="sub_type1",
        fulfillment_types_available="fulfillment1",
        full_queue_behavior="behavior1",
        max_queue_size_kb=1000,
        max_message_count=10,
        priority=1,
        backing_exchange_name="exchange1",
        owner_participant_id=created_participant.participant_id,
        dataset_definition_id=created_dataset_definition.dataset_definition_id
    #dataset_definition_id=dataset.dataset_id,
    )
    created_subject = await subject_repo.create(session, subject_create)

    endpoint = m.EndPointCreate(endpoint_uuid="uuid1",
                                endpoint_user_name="user1",
                                certificate_dn="dn1",
                                description="desc1",
                                uudex_administrator_sw="Y",
                                participant_administrator_sw="Y",
                                participant_id=created_participant.participant_id)
    created_endpoint = await endpoint_repo.create(session, endpoint)

    subscription_create = Subscription(subscription_uuid=str(uuid.uuid4()),
                                       subscription_name="Test Subscription",
                                       subscription_state="ACTIVE",
                                       description="This is a test subscription",
                                       owner_endpoint_id=created_endpoint.endpoint_id)
    created_subscription = await subscription_repo.create(session, subscription_create)

    return created_subject, created_subscription


@pytest.mark.asyncio
async def test_create_subscription_subject(
        subscription_subject_repo: SubscriptionSubjectRepository, session: Session,
        participant_repo: ParticipantRepository, subject_repo: SubjectRepository,
        endpoint_repo: EndpointRepository, subscription_repo: SubscriptionRepository,
        dataset_definition_repo: DatasetDefinitionRepository):
    created_subject, created_subscription = await setup_subscription_and_subject(
        session,
        participant_repo=participant_repo,
        subject_repo=subject_repo,
        endpoint_repo=endpoint_repo,
        subscription_repo=subscription_repo,
        dataset_definition_repo=dataset_definition_repo)
    subscription_subject_create = SubscriptionSubjectCreate(
        subscription_id=created_subscription.subscription_id,
        subject_id=created_subject.subject_id,
        preferred_fulfillment_type="DATA_PUSH",
        backing_queue_name="what is this")
    created_subscription_subject = await subscription_subject_repo.create(
        session, subscription_subject_create)
    assert created_subscription_subject.subscription_id == created_subscription.subscription_id
    assert created_subscription_subject.subject_id == created_subject.subject_id

    # Check relationships
    # assert created_subscription_subject.subscription is not None
    # assert created_subscription_subject.subscription.subscription_name == "Test Subscription"
    # assert created_subscription_subject.subject is not None
    # assert created_subscription_subject.subject.subject_name == "Test Subject"


@pytest.mark.asyncio
async def test_select_all_subscription_subjects(
        subscription_subject_repo: SubscriptionSubjectRepository, session: Session,
        participant_repo: ParticipantRepository, subject_repo: SubjectRepository,
        endpoint_repo: EndpointRepository, subscription_repo: SubscriptionRepository,
        dataset_definition_repo: DatasetDefinitionRepository):
    created_subject, created_subscription = await setup_subscription_and_subject(
        session,
        participant_repo=participant_repo,
        subject_repo=subject_repo,
        endpoint_repo=endpoint_repo,
        subscription_repo=subscription_repo,
        dataset_definition_repo=dataset_definition_repo)
    subscription_subject_create = SubscriptionSubjectCreate(
        subscription_id=created_subscription.subscription_id,
        subject_id=created_subject.subject_id,
        preferred_fulfillment_type="DATA_PUSH",
        backing_queue_name="what is this")
    created_subscription_subject = await subscription_subject_repo.create(
        session, subscription_subject_create)
    subscription_subjects = await subscription_subject_repo.select_all(session)
    assert isinstance(subscription_subjects, list)


@pytest.mark.asyncio
async def test_select_by_fields(subscription_subject_repo: SubscriptionSubjectRepository,
                                session: Session, participant_repo: ParticipantRepository,
                                subject_repo: SubjectRepository, endpoint_repo: EndpointRepository,
                                subscription_repo: SubscriptionRepository,
                                dataset_definition_repo: DatasetDefinitionRepository):
    created_subject, created_subscription = await setup_subscription_and_subject(
        session,
        participant_repo=participant_repo,
        subject_repo=subject_repo,
        endpoint_repo=endpoint_repo,
        subscription_repo=subscription_repo,
        dataset_definition_repo=dataset_definition_repo)
    subscription_subject_create = SubscriptionSubjectCreate(
        subscription_id=created_subscription.subscription_id,
        subject_id=created_subject.subject_id,
        preferred_fulfillment_type="DATA_PUSH",
        backing_queue_name="what is this")
    created_subscription_subject = await subscription_subject_repo.create(
        session, subscription_subject_create)
    selected_subscription_subject = await subscription_subject_repo.select_by_fields(
        session,
        subscription_id=created_subscription.subscription_id,
        subject_id=created_subject.subject_id)
    assert selected_subscription_subject is not None
    assert selected_subscription_subject.subscription_id == created_subscription.subscription_id


@pytest.mark.asyncio
async def test_delete_subscription_subject(
        subscription_subject_repo: SubscriptionSubjectRepository, session: Session,
        participant_repo: ParticipantRepository, subject_repo: SubjectRepository,
        endpoint_repo: EndpointRepository, subscription_repo: SubscriptionRepository,
        dataset_definition_repo: DatasetDefinitionRepository):
    created_subject, created_subscription = await setup_subscription_and_subject(
        session,
        participant_repo=participant_repo,
        subject_repo=subject_repo,
        endpoint_repo=endpoint_repo,
        subscription_repo=subscription_repo,
        dataset_definition_repo=dataset_definition_repo)
    subscription_subject_create = SubscriptionSubjectCreate(
        subscription_id=created_subscription.subscription_id,
        subject_id=created_subject.subject_id,
        preferred_fulfillment_type="DATA_PUSH",
        backing_queue_name="what is this")
    created_subscription_subject = await subscription_subject_repo.create(
        session, subscription_subject_create)
    subscription_subject_remove = SubscriptionSubjectDelete(
        subscription_subject_id=created_subscription_subject.subscription_subject_id)
    await subscription_subject_repo.delete(session, subscription_subject_remove)
    deleted_subscription_subject = await subscription_subject_repo.select_by_id(
        session, created_subscription_subject.subscription_subject_id)
    assert deleted_subscription_subject is None
