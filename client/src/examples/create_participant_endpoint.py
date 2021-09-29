from __future__ import print_function
from pprint import pprint
import logging
import os
import base64
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
endpoint_configuration = uudex_client.Configuration()
pnnl_configuration = uudex_client.Configuration()
# Ensure "pnnl_demo" and "endpoint_demo" entries are added into uudex_client.ini
configurator.set_values(pnnl_configuration, "pnnl_demo")
configurator.set_values(endpoint_configuration, "endpoint_demo")

endpoint_configuration.verify_ssl = False
endpoint_configuration.assert_hostname = False
#print(f"configuration: {endpoint_configuration.verify_ssl}, {endpoint_configuration.assert_hostname}, {endpoint_configuration.host}")

pnnl_configuration.verify_ssl = False
pnnl_configuration.assert_hostname = False
#print(f"configuration: {pnnl_configuration.verify_ssl}, {pnnl_configuration.assert_hostname}, {pnnl_configuration.host}")

pnnl_client = uudex_client.ApiClient(pnnl_configuration)
subject_acl_api = uudex_client.SubjectAclApi(pnnl_client)


def create_certs(cert_name):
    cwd = f"{os.path.expanduser('~')}/easyrsa"
    easyrsa_path = f"{cwd}/easyrsa"
    cmd = [easyrsa_path, 'build-client-full', cert_name, 'nopass']
    results = subprocess.run(cmd, cwd=cwd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if results.returncode != 0:
        raise RuntimeError(f"Error executing command: {cmd}")
    else:
        print(f"{results.stdout.decode('utf-8')}")


def get_participant_uuid(client, participant_name):
    participant_api = uudex_client.ParticipantApi(client)
    participant_uuid = None
    try:
        # Return a collection all Participants in the system
        participants = participant_api.admin_get_all_participants()
        #pprint(participants)
        for participant in participants:
            if participant.participant_short_name == participant_name:
                participant_uuid = participant.participant_uuid
                break
    except ApiException as e:
        print("Exception when calling ParticipantApi->admin_get_all_participants: %s\n" % e)
    return participant_uuid


def get_endpoint_uuid(client, endpoint_user_name):
    endpoint_api = uudex_client.EndpointApi(client)
    endpoint_uuid = None

    try:
        # Return a collection of all Endpoints in the system
        endpoints = endpoint_api.admin_get_all_endpoints()
        for endpoint in endpoints:
            if endpoint.endpoint_user_name == endpoint_user_name:
                endpoint_uuid = endpoint.endpoint_uuid
                break
    except ApiException as e:
        print("Exception when calling EndpointApi->admin_get_all_endpoints: %s\n" % e)
    return endpoint_uuid


def get_dataset_def_uuid(client, dataset_def_name):
    dataset_def_api = uudex_client.DatasetDefinitionApi(client)
    dataset_def_uuid = None

    # Get the uuid matching the dataset definition uuid
    try:
        print(f"Checking if dataset definition exists: {dataset_def_name}")
        # Returns a collection of all Datasets Definitions in the system
        dataset_defs = dataset_def_api.get_all_dataset_definitions()

        for dataset_def in dataset_defs:
            if dataset_def.dataset_definition_name == dataset_def_name:
                dataset_def_uuid = dataset_def.dataset_definition_uuid
                break
    except ApiException as e:
        print("Exception when calling DatasetDefinitionApi->get_all_dataset_definitions: %s\n" % e)
    return dataset_def_uuid


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


def create_new_participant(client, participant_short_name):
    participant_uuid = None
    participant_api = uudex_client.ParticipantApi(client)
    try:
        body = uudex_client.Participant(participant_short_name=participant_short_name, participant_long_name="ACME-Org",
                                        description="ACME Organization", root_org_sw="N", active_sw="Y")
        # Create a single Participant
        participant = participant_api.admin_create_participant(body=body)
        #pprint(participant)
        participant_uuid = participant.participant_uuid
    except ApiException as e:
        print("Exception when calling ParticipantApi->admin_create_participant: %s\n" % e)
    return participant_uuid


def create_new_endpoint(client, endpoint_user_name, participant_uuid):
    endpoint_uuid = None
    endpoint_api = uudex_client.EndpointApi(client)
    body = uudex_client.Endpoint(endpoint_user_name=endpoint_user_name, certificate_dn=endpoint_user_name,
                                 description="ACME Publisher Endpoint", active_sw="Y",
                                 uudex_administrator_sw="N",
                                 participant_administrator_sw="N",
                                 participant_uuid=participant_uuid)  # Endpoint |  (optional)

    try:
        # Create a single Endpoint
        endpoint = endpoint_api.admin_create_endpoint(body=body)
        endpoint_uuid = endpoint.endpoint_uuid
        #pprint(endpoint)
    except ApiException as e:
        print("Exception when calling EndpointApi->admin_create_endpoint: %s\n" % e)
    return endpoint_uuid


def create_dataset_definition_uuid(client, dataset_def_name):
    dataset_def_api = uudex_client.DatasetDefinitionApi(client)
    dataset_def_uuid = None
    # Create dataset definition
    body = uudex_client.DatasetDefinition(
        dataset_definition_name=dataset_def_name,
        description="test dataset definition")  # DatasetDefinition |  (optional)
    try:
        print("Creating dataset definition::")
        # Create a single Dataset Definition
        dataset_definition = dataset_def_api.admin_create_dataset_definition(body=body)
        dataset_def_uuid = dataset_definition.dataset_definition_uuid
    except ApiException as e:
        print("Exception when calling DatasetDefinitionApi->admin_create_dataset_definition: %s\n" % e)
    return dataset_def_uuid


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


def grant_subject_acl(client, subject_uuid, privilege_name, grant_scope_name):
    subject_acl_api = uudex_client.SubjectAclApi(client)
    body = uudex_client.SubjectAcl(privilege_name=privilege_name,
                                   grant_scope_name=grant_scope_name,
                                   participant_uuid_list=[None])  # SubjectAcl |  (optional)

    try:
        # Grant a privilege to the Subject's ACL. Caller must own Subject.
        api_response = subject_acl_api.grant_subject_acl_privilege(subject_uuid, body=body)
        #pprint(api_response)
    except ApiException as e:
        print("Exception when calling SubjectAclApi->grant_subject_acl_privilege: %s\n" % e)


def consume_subscription(client, subscription_name):
    subscription_api = uudex_client.SubscriptionApi(client)
    subscription_uuid = get_subscription_uuid(client, subscription_name)

    try:
        print(f"Consuming subscription message:: {subscription_uuid}")
        # Consumes and returns one or more pending messages from message broker
        api_response = subscription_api.consume_subscription(subscription_uuid)
        #pprint(api_response)
    except ApiException as e:
        print("Exception when calling SubscriptionApi->consume_subscription: %s\\n" % e)


def publish_message(client, subject_uuid):
    subject_api = uudex_client.SubjectApi(client)
    msg = "- 1235 - test - test - abc"
    for i in range(0, 4):
        message_payload1 = f"Message {i + 1}: {msg}"
        print(f"Publishing: {message_payload1}")
        resp = subject_api.publish_message(subject_uuid,
                                           body={"message": message_payload1})
        #pprint(resp)


def find_subject_acl(client, subject_uuid, privilege_name, grant_scope_name):
    subject_acl_api = uudex_client.SubjectAclApi(client)
    found = False
    try:
        # Return all ACLs attached to the given Subject. Caller must own Subject.
        acls = subject_acl_api.get_subject_acls(subject_uuid)
        for acl in acls:
            if acl.privilege_name == privilege_name and acl.grant_scope_name == grant_scope_name:
                found = True
                break
    except ApiException as e:
        print("Exception when calling SubjectAclApi->get_subject_acls: %s\n" % e)
    return found


def test_new_endpoint(endpoint_user_name):
    # Create a new "ACME-Org" Participant
    print("Create a new ACME-Org Participant")
    participant_short_name = "ACME-Org"
    participant_uuid = get_participant_uuid(pnnl_client, participant_short_name)
    if participant_uuid is None:
        participant_uuid = create_new_participant(pnnl_client, participant_short_name)

    # Create Endpoint Certificate
    #endpoint_user_name = f"{uuid}-ACME-Publisher"
    print(f"EP name: {endpoint_user_name}")
    # try:
    #     create_certs(uuid, endpoint_user_name)
    # except RuntimeError:
    #     exit(-1)

    print(f"Create a new endpoint {endpoint_user_name} for ACME-Org Participant")
    # Create new endpoint for "ACME-Org" Participant
    endpoint_uuid = get_endpoint_uuid(pnnl_client, endpoint_user_name)
    if endpoint_uuid is None:
        endpoint_uuid = create_new_endpoint(pnnl_client, endpoint_user_name, participant_uuid)

    endpoint_client = uudex_client.ApiClient(endpoint_configuration)
    dataset_def_name = "ACME-Dataset-Def"
    dataset_def_uuid = get_dataset_def_uuid(pnnl_client, dataset_def_name)
    if dataset_def_uuid is None:
        dataset_def_uuid = create_dataset_definition_uuid(pnnl_client, dataset_def_name)

    if endpoint_uuid is not None:
        # Create new subject as ACME-Publisher endpoint
        print(f"Create new subject as {endpoint_user_name} endpoint")
        subject_name_filter = "ACME-Subject"
        subscription_name = "ACME-Subscription"

        subject_uuid = discover_subject_uuid(endpoint_client, subject_name_filter)
        if subject_uuid is None:
            subject_uuid = create_subject(endpoint_client, subject_name_filter, dataset_def_uuid)

        print(f"Add new ACL constraints (Subscribe, AllowAll and Doscover, AllowAll) to new subject as {endpoint_user_name} endpoint")
        # Add ACL constraints to the subject as ACME-Publisher endpoint
        subscribe_allow_all = find_subject_acl(endpoint_client, subject_uuid, "SUBSCRIBE", "ALLOW_ALL")
        discover_allow_all = find_subject_acl(endpoint_client, subject_uuid, "DISCOVER", "ALLOW_ALL")
        if not subscribe_allow_all:
            grant_subject_acl(endpoint_client, subject_uuid, "SUBSCRIBE", "ALLOW_ALL")
        if not discover_allow_all:
            grant_subject_acl(endpoint_client, subject_uuid, "DISCOVER", "ALLOW_ALL")

        print(f"Publish to the subject as {endpoint_user_name} Endpoint")
        # Publish to the subject as "ACME-Publisher" Endpoint
        publish_message(endpoint_client, subject_uuid)


def main():
    # Create the parser
    my_parser = argparse.ArgumentParser(description='Test new endpoint')

    # Add the arguments
    my_parser.add_argument('testcase_type',
                           type=str,
                           help='Testcase type: TEST_NEW_ENDPOINT, CREATE_CERTS')

    my_parser.add_argument('endpoint_name',
                           type=str,
                           help='Endpoint Name')

    # uid = '5ba2fe42-8391-11eb-9ebf-080027051813'
    # Execute the parse_args() method
    args = my_parser.parse_args()

    testcase_type = args.testcase_type
    endpoint_name = args.endpoint_name

    print(testcase_type, endpoint_name)
    if testcase_type == "TEST_NEW_ENDPOINT":
        test_new_endpoint(endpoint_name)
    elif testcase_type == "CREATE_CERTS":
        import uuid
        uid = str(uuid.uuid4())[0:12]
        cert_name = f"{uid}-ACME-Publisher"
        print(f"UUID: {cert_name}")
        create_certs(cert_name)


if __name__ == "__main__":
    main()
