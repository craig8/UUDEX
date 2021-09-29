from __future__ import print_function
from pprint import pprint
import logging
import os
import argparse
import urllib3
import subprocess
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from client_wrapper import UudexThinWrapper
from create_certs import create_client_certs

LOG_FORMAT = ('%(levelname) -9s %(asctime)s  %(name) -55s %(funcName) '
              '-35s %(lineno) -4d: %(message)s')
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


def get_participant(uudex_wrapper, site, participant_name):
    participant_uuid = None
    try:
        participants = uudex_wrapper.get_participants(site)
        for participant in participants:
            if participant.participant_short_name == participant_name:
                participant_uuid = participant.participant_uuid
                break
    except Exception as e:
        logger.error(f"Error getting participant UUID: {e}")
    return participant_uuid


def get_dataset_definition(uudex_wrapper, site, dataset_definition_name):
    dataset_def_uuid = None

    try:
        dataset_defs = uudex_wrapper.get_dataset_defintions(site)
        for dataset_def in dataset_defs:
            if dataset_def.dataset_definition_name == dataset_definition_name:
                dataset_def_uuid = dataset_def.dataset_definition_uuid
                break
    except Exception as e:
        logger.error(f"Error getting Dataset definition UUID: {e}")
    return dataset_def_uuid


def create_endpoint(uudex_wrapper, site, endpoint_name, description, participant_uuid):
    endpoint_uuid = None
    try:
        endpoints = uudex_wrapper.get_endpoints(site)
        for endpoint in endpoints:
            if endpoint.endpoint_user_name == endpoint_name:
                endpoint_uuid = endpoint.endpoint_uuid
                break
        if endpoint_uuid is None:
            endpoint_uuid = uudex_wrapper.create_endpoint(site, endpoint_name, description, participant_uuid)
    except Exception as e:
        logger.error(f"Error creating new endpoint: {endpoint_name}: {e}")
    return endpoint_uuid


def create_subject(uudex_wrapper, site, subject_name, subject_description, dataset_def_uuid):
    subject_uuid = None
    try:
        subjects = uudex_wrapper.get_discoverable_subjects(site)
        for sub in subjects:
            if sub.subject_name == subject_name:
                subject_uuid = sub.subject_uuid
                break

        if subject_uuid is None:
            subject = uudex_wrapper.create_subject(site, subject_name,
                                                   subject_name, subject_description,
                                                   "MEASUREMENT_VALUES",
                                                   "DATA_PUSH", dataset_def_uuid)
            subject_uuid = subject.subject_uuid
    except Exception as e:
        logger.error(f"Error creating new subject: {subject_name}: {e}")
    return subject_uuid


def create_subscription_subject(uudex_wrapper, site, subject_uuid, subscription_uuid):
    subscription_subject_uuid = None
    subscription_subjects = None
    try:
        if subscription_subjects is None and subscription_subject_uuid is None:
            sub = uudex_wrapper.attach_subject(site, subscription_uuid, subject_uuid, preferred_fulfillment_type='DATA_PUSH')
            subscription_subject_uuid = sub.subscription_subject_uuid
    except Exception as e:
        logger.error(f"Error subscription to subject: {e}")
    return subscription_subject_uuid


def get_subscription_uuid(uudex_wrapper, site, subscription_name):
    subscription_uuid = None
    try:
        subscriptions = uudex_wrapper.get_subscriptions(site)
        for subscription in subscriptions:
            if subscription.subscription_name == subscription_name:
                subscription_uuid = subscription.subscription_uuid
                break
    except Exception as e:
        logger.error(f"Error subscription to subject: {e}")
    return subscription_uuid


def create_subscription(uudex_wrapper, site, subscription_name):
    subscription_uuid = None
    try:
        subs = uudex_wrapper.get_subscriptions(site)
        if subs:
            for sub in subs:
                if sub.subscription_name == subscription_name:
                    subscription_uuid = sub.subscription_uuid
                    break
        if not subs or subscription_uuid is None:
            subscription = uudex_wrapper.create_subscription(site, subscription_name)
            subscription_uuid = subscription.subscription_uuid
    except Exception as e:
        logger.error(f"Error creating subscription by name: {subscription_name}: {e}")
    return subscription_uuid

def on_publish_message(uudex_wrapper, site, subject_uuid):
    msg = f"- 1235 - test - test - abc-{subject_uuid}"
    messages = []
    for i in range(0, 4):
        messages.append(f"Message {i + 1}: {msg}")
    try:
        uudex_wrapper.publish_message(site, subject_uuid, messages)
    except Exception as e:
        logger.error(f"Error publishing message to {site}: {e}")


def find_subject_acl(acls, privilege_name, grant_scope_name):
    found = False
    for acl in acls:
        if acl.privilege_name == privilege_name and acl.grant_scope_name == grant_scope_name:
            found = True
            break
    return found


def on_acl(uudex_wrapper, site, subject_uuid, participant_uuid):
    try:
        acls = uudex_wrapper.get_subject_acls(site, subject_uuid)
        # Add ACL constraints to the subject as ACME-Publisher endpoint
        subscribe_allow_all = find_subject_acl(acls, "SUBSCRIBE", "ALLOW_ALL")
        discover_allow_all = find_subject_acl(acls, "DISCOVER", "ALLOW_ALL")
        #print(f"subject: {subject_uuid}, ACLS: {acls}, SUBSCRIBE_ALL: {subscribe_allow_all}, DISCOVER_ALL: {discover_allow_all}")
        if not subscribe_allow_all:
            new_acls = uudex_wrapper.grant_acl(site, subject_uuid, "SUBSCRIBE", "ALLOW_ALL", [None])
        if not discover_allow_all:
            new_acls = uudex_wrapper.grant_acl(site, subject_uuid, "DISCOVER", "ALLOW_ALL", [None])
    except Exception as e:
        logger.error(f"Error setting acl for subject: {subject_uuid}: {e}")


def test_multi_subscribers(sites):
    uudex_wrapper = UudexThinWrapper(sites=sites)

    admin_site = sites[0]
    sub1_site = sites[1]
    sub2_site = sites[2]
    sub3_site = sites[3]
    pub1_site = sites[4]
    pub2_site = sites[5]

    participant_uuid = get_participant(uudex_wrapper, admin_site, "ACME-Org")
    dataset_definition_name = "ACME-Dataset-Def"
    dataset_definition_uuid = get_dataset_definition(uudex_wrapper, admin_site, dataset_definition_name)
    print(f"dataset definition uuid: {dataset_definition_uuid}")

    # Create 5 endpoints to represent 3 subscribers and 2 publishers
    subscriber1_uuid = create_endpoint(uudex_wrapper, admin_site, "a665130b-cc5-Subscriber1", "Subscriber 1", participant_uuid)
    subscriber2_uuid = create_endpoint(uudex_wrapper, admin_site, "47d754e7-4e7-Subscriber2", "Subscriber 2", participant_uuid)
    subscriber3_uuid = create_endpoint(uudex_wrapper, admin_site, "38ccc890-2b3-Subscriber3", "Subscriber 3", participant_uuid)
    publisher1_uuid = create_endpoint(uudex_wrapper, admin_site, "49756789-e1f-Publisher1", "Publisher 1", participant_uuid)
    publisher2_uuid = create_endpoint(uudex_wrapper, admin_site, "37c97b2a-6c7-Publisher2", "Publisher 2", participant_uuid)

    print(f"Endpoint uuid: {subscriber1_uuid}, {subscriber2_uuid}, {subscriber3_uuid}, {publisher1_uuid}, {publisher2_uuid}")

    # Create 2 subjects "A" and "B" using publisher 1 and publisher 2 endpoints
    sub1_uuid = create_subject(uudex_wrapper, pub1_site, "A", "Subject A", dataset_definition_uuid)
    sub2_uuid = create_subject(uudex_wrapper, pub2_site, "B", "Subject B", dataset_definition_uuid)

    # Add ACL constraints to the subjects with "DISCOVER_ALL" and "SUBSCRIBER_ALL" properties
    on_acl(uudex_wrapper, pub1_site, sub1_uuid, participant_uuid)
    on_acl(uudex_wrapper, pub2_site, sub2_uuid, participant_uuid)

    # Creates subscriptions for all subscribers
    subscription1_uuid = create_subscription(uudex_wrapper, sub1_site, "SubscriptionAlpha")
    subscription2_uuid = create_subscription(uudex_wrapper, sub2_site, "SubscriptionBeta")
    subscription3_uuid = create_subscription(uudex_wrapper, sub3_site, "SubscriptionGamma")
    subscription4_uuid = create_subscription(uudex_wrapper, sub3_site, "SubscriptionAlphaX")

    # Subscriber 1 and 2 subscribe to subject "A" and Subscriber 3 subscribes to both "A" and "B"
    create_subscription_subject(uudex_wrapper, sub1_site, sub1_uuid, subscription1_uuid)
    create_subscription_subject(uudex_wrapper, sub2_site, sub1_uuid, subscription2_uuid)
    create_subscription_subject(uudex_wrapper, sub3_site, sub2_uuid, subscription3_uuid)
    create_subscription_subject(uudex_wrapper, sub3_site, sub1_uuid, subscription3_uuid)

    # Publisher 1 publishes message to Subject A
    # Publisher 2 publishes to Subject B
    on_publish_message(uudex_wrapper, pub1_site, sub1_uuid)
    on_publish_message(uudex_wrapper, pub2_site, sub2_uuid)

    import time

    # Subscriber 1 consumes from message corresponding to Subject A immediately.
    # Subscriber 2 consumes from message corresponding to Subject A after 10 seconds.
    # Subscriber 3 consumes message corresponding to both A and afte 30 seconds.

    # This demonstrates that a unique queue is created for every subscription and messages are
    # pulled from the queue based on subscriber's consume request
    messages1 = uudex_wrapper.consume_subscription(sub1_site, subscription1_uuid)
    time.sleep(10)
    messages2 = uudex_wrapper.consume_subscription(sub2_site, subscription2_uuid)
    time.sleep(10)
    messages3 = uudex_wrapper.consume_subscription(sub3_site, subscription3_uuid)
    messages4 = uudex_wrapper.consume_subscription(sub3_site, subscription4_uuid)

    #
    print(f"Consume message1: {messages1}")
    print(f"Consume message2: {messages2}")
    print(f"Consume message3: {messages3}")
    print(f"Consume message4: {messages4}")


def main():
    # Create the parser
    my_parser = argparse.ArgumentParser(description='Test multiple subscribers')

    # Add the arguments
    my_parser.add_argument('testcase_type',
                           type=str,
                           help='Testcase type: MULTI_SUB, CREATE_CERTS')

    args = my_parser.parse_args()

    testcase_type = args.testcase_type

    if testcase_type == "MULTI_SUB":
        sites = ['PNNL@pnnl', 'sub1@pnnl', 'sub2@pnnl', 'sub3@pnnl', 'pub1@pnnl', 'pub2@pnnl']
        test_multi_subscribers(sites)
    elif testcase_type == "CREATE_CERTS":
        import uuid
        uid = str(uuid.uuid4())[0:12]
        cert_name = f"{uid}-Publisher2"
        print(f"Cert name : {cert_name}")
        create_client_certs(cert_name)


if __name__ == "__main__":
    main()
