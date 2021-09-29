from __future__ import print_function
from pprint import pprint
import logging

import urllib3
import argparse

import uudex_client
from uudex_client.rest import ApiException
from uudex_client import configurator

LOG_FORMAT = ('%(levelname) -9s %(asctime)s  %(name) -55s %(funcName) '
              '-35s %(lineno) -4d: %(message)s')
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
#
configuration = uudex_client.Configuration()
configurator.set_values(configuration, "pnnl_dev_local")

client = uudex_client.ApiClient(configuration)
subscription_api = uudex_client.SubscriptionApi(client)
subject_api = uudex_client.SubjectApi(client)
data_type_api = uudex_client.DatatypeApi(client)
dataset_api = uudex_client.DatasetApi(client)
participant_api = uudex_client.ParticipantApi(client)

dataset_def_api = uudex_client.DatasetDefinitionApi(client)
subject_policy_api = uudex_client.SubjectPolicyApi(client)



# ----------------------------------------------------------------------------------------------
# Testcase 1: Subject with Queue Total Size Constraints and Block Publish
# create a subject with name = "Tester/TEST/T4.3.1.1", maxQueueSizeKB = 10kB and fullQueueBehavior = "BLOCK_NEW"
# Testcase 2: Subject with Queue Total Size Constraints and Delete Oldest
# create a subject with name = "Tester/TEST/T4.3.1.2", maxQueueSizeKB = 10kB and fullQueueBehavior = "PURGE_OLD"
# Testcase 3: Subject with Queue Message Number Constraints and Block Publish
# create a subject with name = "Tester/TEST/T4.3.2.1", maxMessageCount = 3 and fullQueueBehavior = "BLOCK_NEW"
# Testcase 4: Subject with Queue Message Number Constraints and Delete Old
# create a subject with name = "Tester/TEST/T4.3.2.2", maxMessageCount = 3 and fullQueueBehavior = "PURGE_OLD"
# ----------------------------------------------------------------------------------------------

testcase_inputs = {"QS_BN": {"DATASET_DEF_NAME": "test_dataset_def",
                                            "SUBSCRIPTON_NAME": "test new_subscription",
                                            "SUBJECT_NAME": "Tester/TEST/T4.3.1.1",
                                            "QUEUE_BEHAVIOR": "BLOCK_NEW",
                                            "QUEUE_SIZE": 10,
                                            "MSG_CNT": 0},
                   "QS_PO": {"DATASET_DEF_NAME": "qs_purge_old",
                                            "SUBSCRIPTON_NAME": "qs_purge_old_subscription",
                                            "SUBJECT_NAME": "Tester/TEST/T4.3.1.2",
                                            "QUEUE_BEHAVIOR": "PURGE_OLD",
                                            "QUEUE_SIZE": 10,
                                            "MSG_CNT": 0},
                   "MC_BN": {"DATASET_DEF_NAME": "mc_block_new",
                                            "SUBSCRIPTON_NAME": "mc_block_new_subscription",
                                            "SUBJECT_NAME": "Tester/TEST/T4.3.2.1",
                                            "QUEUE_BEHAVIOR": "BLOCK_NEW",
                                            "QUEUE_SIZE": 0,
                                            "MSG_CNT": 3},
                   "MC_PO": {"DATASET_DEF_NAME": "mc_purge_old",
                                            "SUBSCRIPTON_NAME": "mc_purge_old_new_subscription",
                                            "SUBJECT_NAME": "Tester/TEST/T4.3.2.2",
                                            "QUEUE_BEHAVIOR": "PURGE_OLD",
                                            "QUEUE_SIZE": 0,
                                            "MSG_CNT": 3}}


first_time = True


def run_test_setup(testcase_type):
    dataset_def_uuid = None
    subscription_uuid = None
    subject_policy_uuid = None

    print("Getting parent participant::")
    parent_participant = participant_api.get_parent_participant()
    #pprint(parent_participant)

    # Get the uuid matching the dataset definition uuid
    try:
        print(f"Checking if dataset definition exists: {testcase_inputs[testcase_type]['DATASET_DEF_NAME']}")
        # Returns a collection of all Datasets Definitions in the system
        dataset_defs = dataset_def_api.get_all_dataset_definitions()

        for dataset_def in dataset_defs:
            if dataset_def.dataset_definition_name == testcase_inputs[testcase_type]["DATASET_DEF_NAME"]:
                dataset_def_uuid = dataset_def.dataset_definition_uuid
                break
    except ApiException as e:
        print("Exception when calling DatasetDefinitionApi->get_all_dataset_definitions: %s\n" % e)

    #print(f"dataset_def_uuid: {dataset_def_uuid}")

    # If not found, create a new dataset definition
    if dataset_def_uuid is None:
        # Create dataset definition
        body = uudex_client.DatasetDefinition(dataset_definition_name=testcase_inputs[testcase_type]["DATASET_DEF_NAME"],
                                              description="test dataset definition") # DatasetDefinition |  (optional)
        try:
            print("Creating dataset definition::")
            # Create a single Dataset Definition
            dataset_definition = dataset_def_api.admin_create_dataset_definition(body=body)
            dataset_def_uuid = dataset_definition.dataset_definition_uuid
        except ApiException as e:
            print("Exception when calling DatasetDefinitionApi->admin_create_dataset_definition: %s\n" % e)

    global first_time
    if first_time:
        if testcase_type.startswith('QUEUE_SIZE'):
            # Create a subject policy with dataset definition id
            body = uudex_client.SubjectPolicy(action="ALLOW",
                                              full_queue_behavior=testcase_inputs[testcase_type]["QUEUE_BEHAVIOR"],
                                              max_queue_size_kb=testcase_inputs[testcase_type]["QUEUE_SIZE"],
                                              dataset_definition_uuid=dataset_def_uuid)
        else:
            body = uudex_client.SubjectPolicy(action="ALLOW",
                                              full_queue_behavior=testcase_inputs[testcase_type]["QUEUE_BEHAVIOR"],
                                              max_message_count=testcase_inputs[testcase_type]["MSG_CNT"],
                                              dataset_definition_uuid=dataset_def_uuid)

        try:
            print(f"Creating subject policy::{body}")
            # Creates a Subject Policy and attaches it to given Participant
            api_response = subject_policy_api.admin_create_subject_policy(body=body)
            #pprint(api_response)
            first_time = False
        except ApiException as e:
            print("Exception when calling SubjectPolicyApi->admin_create_subject_policy: %s\n" % e)

    subscription_uuid = get_subscription_uuid(testcase_type)
    if subscription_uuid is None:
        try:
            print("Creating new subscription::")
            # Create a single Subscription for the endpoint
            body = uudex_client.Subscription(subscription_name=testcase_inputs[testcase_type]["SUBSCRIPTON_NAME"],
                                             subscription_state="ACTIVE")  # Subscription | (optional)
            subscription = subscription_api.create_subscription(body=body)
            #pprint(subscription)
            subscription_uuid = subscription.subscription_uuid
        except ApiException as e:
            print("Exception when calling SubscriptionApi->create_subscription: %s\n" % e)

    subject_name_filter = testcase_inputs[testcase_type]["SUBJECT_NAME"]
    subject_uuid = None
    subject = None

    try:
        # Returns a collection of Subjects the calling endpoint is authorized to view.
        # Optionally filter by subject name.
        print(f"Checking if subject exists: {testcase_inputs[testcase_type]['SUBJECT_NAME']}")
        subjects = subject_api.admin_get_all_subjects()
        for sub in subjects:
            if sub.subject_name == subject_name_filter:
                subject_uuid = sub.subject_uuid
                subject = sub
                #print(f"Found subject: {subject_uuid}, {sub}")
                break
    except ApiException as e:
        print("Exception when calling SubjectApi->discover_subjects: %s\n" % e)

    if subject_uuid is None:
        body = None
        if testcase_type.startswith("QUEUE_SIZE"):
            body = uudex_client.Subject(subject_name=subject_name_filter,
                                        dataset_instance_key=subject_name_filter,
                                        subscription_type="MEASUREMENT_VALUES",
                                        full_queue_behavior=testcase_inputs[testcase_type]["QUEUE_BEHAVIOR"],
                                        max_queue_size_kb=testcase_inputs[testcase_type]["QUEUE_SIZE"],
                                        description="test subject desc",
                                        fulfillment_types_available="DATA_PUSH",
                                        dataset_definition_uuid=dataset_def_uuid,
                                        owner_participant_uuid=parent_participant.participant_uuid) # Subject |  (optional)
        else:
            body = uudex_client.Subject(subject_name=subject_name_filter,
                                        dataset_instance_key=subject_name_filter,
                                        subscription_type="MEASUREMENT_VALUES",
                                        full_queue_behavior=testcase_inputs[testcase_type]["QUEUE_BEHAVIOR"],
                                        max_message_count=testcase_inputs[testcase_type]["MSG_CNT"],
                                        description="test subject desc",
                                        fulfillment_types_available="DATA_PUSH",
                                        dataset_definition_uuid=dataset_def_uuid,
                                        owner_participant_uuid=parent_participant.participant_uuid) # Subject |  (optional)
        try:
            print("Creating subject::")
            # Creates a Subject if the calling participant is authorized
            subject = subject_api.create_subject(body=body)
            #pprint(subject)
            subject_uuid = subject.subject_uuid
        except ApiException as e:
            print("Exception when calling SubjectApi->create_subject: %s\\n" % e)

    try:
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
                pprint(api_response)
            except ApiException as e:
                print("Exception when calling SubscriptionApi->attach_subscription_subject: %s\n" % e)
        else:
            print(f"Found subscription_subjects: {subscription_subjects}")
            found = True
            subscription_subject = subscription_subjects[0]
    except ApiException as e:
        print("Exception when calling SubscriptionApi->get_subscription_subjects: %s\n" % e)


def delete_subscription(testcase_type):
    subscription_uuid = get_subscription_uuid(testcase_type)
    if subscription_uuid is not None:
        try:
            # Delete an endpoint's Subscription
            subscription_api.delete_subscription(subscription_uuid)
        except ApiException as e:
            print("Exception when calling SubscriptionApi->delete_subscription: %s\n" % e)
    else:
        print("subscription not found")


def get_subscription_uuid(testcase_type):
    subscription_name = testcase_inputs[testcase_type]["SUBSCRIPTON_NAME"]
    subscription_uuid = None

    try:
        print(f"Checking if subscription exists: {testcase_inputs[testcase_type]['SUBSCRIPTON_NAME']}")
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


def consume_subscription(testcase_type):
    subscription_uuid = get_subscription_uuid(testcase_type)

    try:
        print(f"Consuming subscription message:: {subscription_uuid}")
        # Consumes and returns one or more pending messages from message broker
        api_response = subscription_api.consume_subscription(subscription_uuid)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SubscriptionApi->consume_subscription: %s\\n" % e)


def delete_policy(policy_uuid=None):
    subject_policy_uuid = '40df0b20-d5be-46b5-9625-72291ed8945f'
    try:
        # Delete a single Subject Policy
        subject_policy_api.admin_delete_subject_policy(subject_policy_uuid)
    except ApiException as e:
        print("Exception when calling SubjectPolicyApi->admin_delete_subject_policy: %s\n" % e)


def main():
    # Create the parser
    my_parser = argparse.ArgumentParser(description='Run Queue performance metrics tests')

    # Add the arguments
    my_parser.add_argument('testcase_type',
                           type=str,
                           help='Testcase type: QS_BN, QS_PO, MS_BN, MS_PO')

    my_parser.add_argument('cmd',
                           type=str,
                           help='cmd: SETUP, DELETE_SUBSCRIPTION, CONSUME, DELETE_POLICY')

    # Execute the parse_args() method
    args = my_parser.parse_args()

    testcase_type = args.testcase_type
    testcase_cmd = args.cmd

    print(testcase_type, testcase_cmd)
    if testcase_cmd == "SETUP":
        run_test_setup(testcase_type)
    elif testcase_cmd == "DELETE_SUBSCRIPTION":
        delete_subscription(testcase_type)
    elif testcase_cmd == "CONSUME":
        consume_subscription(testcase_type)
    elif testcase_cmd == "DELETE_POLICY":
        delete_policy()


if __name__ == "__main__":
    main()
