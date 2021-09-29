from __future__ import print_function
from pprint import pprint
import logging
import os
import argparse
import subprocess
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import uudex_client
from uudex_client.rest import ApiException
from uudex_client import configurator

LOG_FORMAT = ('%(levelname) -9s %(asctime)s  %(name) -55s %(funcName) '
              '-35s %(lineno) -4d: %(message)s')
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
#
pnnl_configuration = uudex_client.Configuration()
configurator.set_values(pnnl_configuration, "pnnl_demo")


pnnl_configuration.verify_ssl = False
pnnl_configuration.assert_hostname = False
print(f"configuration: {pnnl_configuration.verify_ssl}, {pnnl_configuration.assert_hostname}, {pnnl_configuration.host}")

pnnl_client = uudex_client.ApiClient(pnnl_configuration)
subject_acl_api = uudex_client.SubjectAclApi(pnnl_client)


def get_subscription_uuid(client, subscription_name):
    subscription_api = uudex_client.SubscriptionApi(client)
    subscription_uuid = None

    try:
        print(f"Checking if subscription exists: {subscription_name}")
        # Returns a collection of the calling endpoint's Subscriptions
        subscriptions = subscription_api.get_subscriptions()
        for subscription in subscriptions:
            if subscription.subscription_name == subscription_name:
                subscription_uuid = subscription.subscription_uuid
                print(f"Found subscription_uuid: {subscription_uuid}")
                break
    except ApiException as e:
        print("Exception when calling SubscriptionApi->get_subscriptions: %s\n" % e)
    return subscription_uuid


def discover_subject_uuid(client, subject_name_filter):
    subject_api = uudex_client.SubjectApi(client)
    subject_uuid = None

    try:
        # Returns a collection of Subjects the calling endpoint is authorized to view.
        # Optionally filter by subject name.
        subjects = subject_api.discover_subjects()
        for sub in subjects:
            if sub.subject_name == subject_name_filter:
                subject_uuid = sub.subject_uuid
                subject = sub
                # print(f"Found subject: {subject_uuid}, {sub}")
                break
    except ApiException as e:
        print("Exception when calling SubjectApi->admin_get_all_subjects: %s\n" % e)
    return subject_uuid

def create_subject(client, subject_name_filter, dataset_def_uuid):
    subject_api = uudex_client.SubjectApi(client)
    subject_uuid = None
    body = uudex_client.Subject(subject_name=subject_name_filter,
                                dataset_instance_key=subject_name_filter,
                                subscription_type="MEASUREMENT_VALUES",
                                description="test subject desc",
                                fulfillment_types_available="DATA_PUSH",
                                dataset_definition_uuid=dataset_def_uuid)  # Subject |  (optional)
    try:
        print("Creating subject::")
        # Creates a Subject if the calling participant is authorized
        subject = subject_api.create_subject(body=body)
        # pprint(subject)
        subject_uuid = subject.subject_uuid
    except ApiException as e:
        print("Exception when calling SubjectApi->create_subject: %s\\n" % e)
    return subject_uuid


def create_subscription(client, subscription_name):
    subscription_api = uudex_client.SubscriptionApi(client)
    subscription_uuid = None
    try:
        print("Creating new subscription::")
        # Create a single Subscription for the endpoint
        body = uudex_client.Subscription(subscription_name=subscription_name,
                                         subscription_state="ACTIVE")  # Subscription | (optional)
        subscription = subscription_api.create_subscription(body=body)
        # pprint(subscription)
        subscription_uuid = subscription.subscription_uuid
    except ApiException as e:
        print("Exception when calling SubscriptionApi->create_subscription: %s\n" % e)
    return subscription_uuid


def consume_subscription(client, subscription_name):
    subscription_api = uudex_client.SubscriptionApi(client)
    subscription_uuid = get_subscription_uuid(client, subscription_name)

    try:
        print(f"Consuming subscription message:: {subscription_uuid}")
        # Consumes and returns one or more pending messages from message broker
        api_response = subscription_api.consume_subscription(subscription_uuid)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SubscriptionApi->consume_subscription: %s\\n" % e)


def test_new_endpoint_consumer():
    subject_name_filter = "ACME-Subject"
    subscription_name = "ACME-Subscription"
    print("Discover subject as PNNL endpoint")
    # Discover subject as PNNL endpoint
    subject_uuid = discover_subject_uuid(pnnl_client, subject_name_filter)
    # Create subscription to the subject as PNNL endpoint
    subscription_uuid = get_subscription_uuid(pnnl_client, subscription_name)
    if subscription_uuid is None:
        subscription_uuid = create_subscription(pnnl_client, subscription_name)
    print("Create new subscription subject as PNNL endpoint")
    # Create new subscription subject as PNNL endpoint
    try:
        subscription_api = uudex_client.SubscriptionApi(pnnl_client)
        # Returns a collection of Subjects attached to the calling endpoint's given Subscription
        subscription_subjects = subscription_api.get_subscription_subjects(subscription_uuid)
        if len(subscription_subjects) <= 0:
            print(f"Creating new subscription_subject: ")
            subscription_subject = uudex_client.SubscriptionSubject(subject_uuid=subject_uuid,
                                                                    subject_name=subject_name_filter,
                                                                    preferred_fulfillment_type="DATA_PUSH") # SubscriptionSubject |  (optional)
            try:
                print(f"Attaching subscription {subscription_uuid} to subject:: {subscription_subject}")
                # Attach a single Subject to an endpoint's given Subscription
                api_response = subscription_api.attach_subscription_subject(subscription_uuid,
                                                                            body=subscription_subject)
                #pprint(api_response)
            except ApiException as e:
                print("Exception when calling SubscriptionApi->attach_subscription_subject: %s\n" % e)
        else:
            #print(f"Found subscription_subject")
            found = True
            subscription_subject = subscription_subjects[0]
    except ApiException as e:
        print("Exception when calling SubscriptionApi->get_subscription_subjects: %s\n" % e)

    print("Subscribe to the subject as standard PNNL Endpoint")
    # Subscribe to the subject as standard PNNL Endpoint
    consume_subscription(pnnl_client, subscription_name)


if __name__ == "__main__":
    test_new_endpoint_consumer()
