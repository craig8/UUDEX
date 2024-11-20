import uuid

import pytest
import uudex_server.models as m
import uudex_server.repos as repo
from sqlmodel import Session

from uudex_server.repos import SubscriptionRepository, ParticipantRepository


@pytest.mark.asyncio
async def setup_participant(session: Session,
                            participant_repo: ParticipantRepository) -> m.Participant:
    participant = m.ParticipantCreate(participant_uuid=str(uuid.uuid4()),
                                      participant_short_name="short1",
                                      participant_long_name="long1",
                                      description="desc1",
                                      root_org_sw="Y",
                                      active_sw="Y")

    created_participant = await participant_repo.create(session, participant)

    return created_participant


@pytest.mark.asyncio
async def test_create_subscription(session: Session, subscription_repo: SubscriptionRepository,
                                   participant_repo: ParticipantRepository):
    created_participant = await setup_participant(session=session,
                                                  participant_repo=participant_repo)
    subscription = m.SubscriptionCreate(subscription_uuid="uuid1",
                                        subscription_name="name1",
                                        subscription_state="active",
                                        owner_endpoint_id=created_participant.participant_id)
    result = await subscription_repo.create(session, subscription)
    assert result.subscription_uuid == "uuid1"


@pytest.mark.asyncio
async def test_select_subscription_by_id(session: Session,
                                         subscription_repo: SubscriptionRepository,
                                         participant_repo: ParticipantRepository):
    created_participant = await setup_participant(session=session,
                                                  participant_repo=participant_repo)
    subscription = m.SubscriptionCreate(subscription_uuid="uuid1",
                                        subscription_name="name1",
                                        subscription_state="active",
                                        owner_endpoint_id=created_participant.participant_id)
    created_subscription = await subscription_repo.create(session, subscription)
    result = await subscription_repo.select_by_id(session, created_subscription.subscription_id)
    assert result is not None
    assert result.subscription_uuid == "uuid1"


@pytest.mark.asyncio
async def test_update_subscription(session: Session, subscription_repo: SubscriptionRepository,
                                   participant_repo: ParticipantRepository):
    created_participant = await setup_participant(session=session,
                                                  participant_repo=participant_repo)
    subscription = m.SubscriptionCreate(subscription_uuid="uuid1",
                                        subscription_name="name1",
                                        subscription_state="active",
                                        owner_endpoint_id=created_participant.participant_id)
    created_subscription = await subscription_repo.create(session, subscription)
    created_subscription.subscription_name = "updated_name"
    result = await subscription_repo.update(session, created_subscription)
    assert result.subscription_name == "updated_name"


@pytest.mark.asyncio
async def test_delete_subscription(session: Session, subscription_repo: SubscriptionRepository,
                                   participant_repo: ParticipantRepository):
    created_participant = await setup_participant(session=session,
                                                  participant_repo=participant_repo)
    subscription = m.SubscriptionCreate(subscription_uuid="uuid1",
                                        subscription_name="name1",
                                        subscription_state="active",
                                        owner_endpoint_id=created_participant.participant_id)
    created_subscription = await subscription_repo.create(session, subscription)
    subscription_remove = m.SubscriptionDelete(
        subscription_id=created_subscription.subscription_id)
    await subscription_repo.delete(session, subscription_remove)
    result = await subscription_repo.select_by_id(session, created_subscription.subscription_id)
    assert result is None


@pytest.mark.asyncio
async def test_select_user_subscriptions(session: Session, authenticated_user: m.AuthenticatedUser,
                                         subscription_repo: SubscriptionRepository):
    subscription = m.SubscriptionCreate(subscription_uuid="uuid1",
                                        subscription_name="name1",
                                        subscription_state="active",
                                        owner_endpoint_id=authenticated_user.endpoint.endpoint_id)
    await subscription_repo.create(session, subscription)
    result = await subscription_repo.select_user_subscriptions(session, authenticated_user)
    assert len(result) > 0
    assert result[0].subscription_uuid == "uuid1"
    assert result[0].owner_endpoint_id == authenticated_user.endpoint.endpoint_id


@pytest.mark.asyncio
async def test_select_admin_subscriptions(session: Session,
                                          subscription_repo: SubscriptionRepository,
                                          participant_repo: ParticipantRepository):
    created_participant = await setup_participant(session=session,
                                                  participant_repo=participant_repo)
    subscription = m.SubscriptionCreate(subscription_uuid="uuid1",
                                        subscription_name="name1",
                                        subscription_state="active",
                                        owner_endpoint_id=created_participant.participant_id)
    await subscription_repo.create(session, subscription)
    result = await subscription_repo.select_admin_subscriptions(session)
    assert len(result) > 0
    assert result[0].subscription_uuid == "uuid1"


@pytest.mark.asyncio
async def test_select_subscription_by_uuid(session: Session,
                                           subscription_repo: SubscriptionRepository,
                                           participant_repo: ParticipantRepository):
    created_participant = await setup_participant(session=session,
                                                  participant_repo=participant_repo)
    subscription = m.SubscriptionCreate(subscription_uuid="uuid1",
                                        subscription_name="name1",
                                        subscription_state="active",
                                        owner_endpoint_id=created_participant.participant_id)
    await subscription_repo.create(session, subscription)
    result = await subscription_repo.select_subscription_by_uuid(session, "uuid1")
    assert result is not None
    assert result.subscription_uuid == "uuid1"
