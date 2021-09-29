from __future__ import print_function

import json
import logging
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import uudex_client
from uudex_client import configurator
from uudex_client.rest import ApiException

LOG_FORMAT = ('%(levelname) -9s %(asctime)s  %(name) -55s %(funcName) '
              '-35s %(lineno) -4d: %(message)s')
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

pnnl_configuration = uudex_client.Configuration()
configurator.set_values(pnnl_configuration, "PNNL@pnnl")
pnnl_configuration.verify_ssl = False
pnnl_configuration.assert_hostname = False
pnnl_client = uudex_client.ApiClient(pnnl_configuration)


def get_parent_participant_uuid(client):
    parent_participant_uuid = None
    # create an instance of the API class
    api_instance = uudex_client.ParticipantApi(client)

    try:
        # Returns the calling Endpoint's parent Participant
        parent_participant = api_instance.get_parent_participant()
        parent_participant_uuid = parent_participant.participant_uuid
    except ApiException as e:
        print("Exception when calling ParticipantApi->get_parent_participant: %s\n" % e)
    return parent_participant_uuid


def get_participant_uuid(client, participant_name):
    participant_api = uudex_client.ParticipantApi(client)
    participant_uuid = None
    try:
        # Return a collection all Participants in the system
        participants = participant_api.auth_get_all_participants()

        for participant in participants:
            if participant.participant_short_name == participant_name:
                participant_uuid = participant.participant_uuid
                break
    except ApiException as e:
        print("Exception when calling ParticipantApi->admin_get_all_participants: %s\n" % e)
    return participant_uuid


def create_participant_if_not_found(client, participant_short_name, participant_long_name, description):
    #participant_uuid = get_participant_uuid(client, participant_short_name)
    participant_uuid = None
    if participant_uuid is None:
        participant_api = uudex_client.ParticipantApi(client)
        try:
            body = uudex_client.Participant(participant_short_name=participant_short_name,
                                            participant_long_name=participant_long_name,
                                            description=description,
                                            active_sw="Y")
            # Create a single Participant
            participant = participant_api.auth_create_participant(body=body)
            participant_uuid = participant.participant_uuid
        except ApiException as e:
            print("Exception when calling ParticipantApi->admin_create_participant: %s\n" % e)
    return participant_uuid


def create_dataset_definition_if_not_found(client, definition_name, description):
    dataset_def_uuid = get_dataset_definition(client, definition_name)
    if dataset_def_uuid is None:
        # Create dataset definition
        body = uudex_client.DatasetDefinition(dataset_definition_name=definition_name,
                                              description=description)  # DatasetDefinition |  (optional)
        try:
            # print("Creating dataset definition::")
            dataset_def_api = uudex_client.DatasetDefinitionApi(client)
            # Create a single Dataset Definition
            dataset_definition = dataset_def_api.create_dataset_definition(body=body)
            dataset_def_uuid = dataset_definition.dataset_definition_uuid
        except ApiException as e:
            print("Exception when calling DatasetDefinitionApi->create_dataset_definition: %s\n" % e)
    return dataset_def_uuid


def create_subject_if_not_found(client, subject_name, subject_description, dataset_def_uuid):
    subject_uuid = discover_subject_uuid(client, subject_name)
    if subject_uuid is None:
        try:
            subject_api = uudex_client.SubjectApi(client)

            body = uudex_client.Subject(subject_name=subject_name, dataset_instance_key=subject_name,
                                        description=subject_description, subscription_type="MEASUREMENT_VALUES",
                                        fulfillment_types_available="DATA_PUSH",
                                        dataset_definition_uuid=dataset_def_uuid)
            subject = subject_api.create_subject(body=body)
            subject_uuid = subject.subject_uuid
        except Exception as e:
            logger.error(f"Error creating new subject: {subject_name}: {e}")
    return subject_uuid


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
                break
    except ApiException as e:
        print("Exception when calling SubjectApi->admin_get_all_subjects: %s\n" % e)
    return subject_uuid


def get_dataset_definition(client, name):
    dataset_def_uuid = None
    dataset_def_api = uudex_client.DatasetDefinitionApi(client)
    try:
        dataset_defs = dataset_def_api.get_all_dataset_definitions()
        for dataset_def in dataset_defs:
            if dataset_def.dataset_definition_name == name:
                dataset_def_uuid = dataset_def.dataset_definition_uuid
                break
    except ApiException as e:
        print("Exception when calling DatasetDefinitionApi->get_all_dataset_definitions: %s\n" % e)
    return dataset_def_uuid

def delete_dataset(client, dataset_uuid):
    # create an instance of the API class
    api_instance = uudex_client.DatasetApi(client)
    publish_message = False  # bool | Whether to also publish a notice message to the parent subject (optional)

    try:
        # Delete the Dataset and optionally publish a notification message
        api_instance.delete_dataset(dataset_uuid, publish_message=publish_message)
    except ApiException as e:
        print("Exception when calling DatasetApi->delete_dataset: %s\n" % e)

def create_dataset(client, subject_uuid):
    # create an instance of the API class
    api_instance = uudex_client.DatasetApi(client)
    properties = {'signature':'repudiation'}
    import json
    properties_string = json.dumps(properties)
    payload = "on repudiation"

    if isinstance(payload, str):
        b64_payload = payload.encode("utf-8")
    else:
        b64_payload = payload

    import base64
    b64_payload = base64.b64encode(b64_payload).decode("utf-8")
    body = uudex_client.Dataset(dataset_name="dummy",
                                description="testing search expression",
                                properties=properties_string,
                                payload=b64_payload,
                                payload_compression_algorithm='NONE',
                                subject_uuid=subject_uuid)  # Dataset |  (optional)

    try:
        # Create a single Dataset in the given Subject and optionally publish a message that contains the Dataset
        api_response = api_instance.create_dataset(body=body)
        return api_response.dataset_uuid
    except ApiException as e:
        print("Exception when calling DatasetApi->create_dataset: %s\n" % e)
        return None


def get_datasets(client, subject_uuid, search_expression, participant_uuid):
    # create an instance of the API class
    api_instance = uudex_client.DatasetApi(client)
    datasets = None
    try:
        if search_expression == "":
            # Returns a collection of all the Datasets applied to given search parameters
            datasets = api_instance.get_datasets(subject_uuid,
                                                 participant_uuid=participant_uuid)
        else:
            # Returns a collection of all the Datasets applied to given search parameters
            datasets = api_instance.get_datasets(subject_uuid,
                                                 search_expression=search_expression,
                                                 participant_uuid=participant_uuid)
    except ApiException as e:
        print("Exception when calling DatasetApi->get_datasets: %s\n" % e)
    return datasets

def get_permissions(client, object_uuid):
    # create an instance of the API class
    api_instance = uudex_client.PermissionApi(client)
    object_type = "p"  # str | The object type of the object_uuid param.  This code can be \"s\", \"r\", \"g\", \"e\" or \"p\", which represents \"Subject\", \"Role\", \"Group\", \"Endpoint\" or \"Participant\", respectively

    permissions = None
    try:
        # Returns a collection of all explicit and implicit permissions granted to an object
        permissions = api_instance.auth_get_permissions(object_uuid, object_type)
    except ApiException as e:
        print("Exception when calling PermissionApi->auth_get_permissions: %s\n" % e)
    return permissions


def grant_permission_if_not_present(client, subject_uuid, privilege, object_uuid, object_type):
    permissions = get_permissions(client, object_uuid)
    granted = None
    if permissions is not None:
        # create an instance of the API class
        api_instance = uudex_client.PermissionApi(client)
        body = uudex_client.Permission(subject_uuid, privilege, object_uuid, object_type, "N")  # Permission |  (optional)

        try:
            # Creates a permission by granting a privilege on a Subject to an object
            granted = api_instance.auth_grant_permission(body=body)
        except ApiException as e:
            print("Exception when calling PermissionApi->auth_grant_permission: %s\n" % e)
    return granted


def get_all_roles(client):
    # create an instance of the API class
    api_instance = uudex_client.RoleApi(client)

    try:
        # Return a collection of all Roles in the system
        roles = api_instance.auth_get_all_roles()
    except ApiException as e:
        print("Exception when calling RoleApi->auth_get_all_roles: %s\n" % e)


def get_subject_policies(client, action, max_queue_size_kb, participant_uuid, dataset_definition_uuid):
    # create an instance of the API class
    subject_policy_api = uudex_client.SubjectPolicyApi(client)
    policy_uuid = None
    try:
        # Returns a collection of Subject Policies
        policies = subject_policy_api.get_subject_policies()
        for policy in policies:
            if policy.action == action and policy.max_queue_size_kb == max_queue_size_kb \
                and policy.target_participant_uuid == participant_uuid \
                    and policy.dataset_definition_uuid == dataset_definition_uuid:
                policy_uuid = policy.subject_policy_uuid
    except ApiException as e:
        print("Exception when calling SubjectPolicyApi->get_subject_policies: %s\n" % e)
    return policy_uuid


def create_subject_policy_if_not_present(client, action, max_queue_size_kb, participant_uuid, dataset_definition_uuid):
    policy_uuid = get_subject_policies(client, action, max_queue_size_kb, None, dataset_definition_uuid)
    if policy_uuid is None:
        # create an instance of the API class
        subject_policy_api = uudex_client.SubjectPolicyApi(client)
        body = uudex_client.SubjectPolicy(action=action,
                                          max_queue_size_kb=max_queue_size_kb,
                                          target_participant_uuid=None,
                                          dataset_definition_uuid=dataset_definition_uuid)  # SubjectPolicy |  (optional)

        try:
            # Creates a Subject Policy and attaches it to given Participant
            policy_uuid = subject_policy_api.create_subject_policy(body=body)
        except ApiException as e:
            print("Exception when calling SubjectPolicyApi->create_subject_policy: %s\n" % e)
    return policy_uuid


def test_datasets():
    # Get your parent participant
    participant_uuid = get_parent_participant_uuid(pnnl_client)
    print(f"participant uuid:{participant_uuid}")
    if participant_uuid is not None:
        # Get Dataset def id matching dataset definition name
        dataset_definition_name = "Test-Dataset-Def"
        dataset_def_uuid = create_dataset_definition_if_not_found(pnnl_client, dataset_definition_name, "Test Dataset Definition")
        if dataset_def_uuid is not None:
            # Create new subject if not existing
            subject_name = "SubjectForDatasetQuery"
            subject_uuid = create_subject_if_not_found(pnnl_client, subject_name, "Subject For DatasetQuery", dataset_def_uuid)
            if subject_uuid is not None:
                policy_uuid = create_subject_policy_if_not_present(pnnl_client, "ALLOW", 10, participant_uuid, dataset_def_uuid)
                if policy_uuid is not None:
                    # Set PUBLISH permission for subject and participant
                    granted = grant_permission_if_not_present(pnnl_client, subject_uuid, "PUBLISH", participant_uuid, "p")
                    if granted:
                        # Create dataset for the subject
                        dataset_uuid = create_dataset(pnnl_client, subject_uuid)
                        # search_expression = ""
                        # datasets = get_datasets(pnnl_client, subject_uuid, search_expression, participant_uuid)
                        # print(f"Datasets without search: {datasets}\n")
                        # Get dataset using search expression
                        # search_dict = {'description': 'testing search expression'}
                        search_dict = {'description': 'testing search expression', 'properties': {'signature': 'repudiation'}}
                        # #search_dict = {'properties': {'signature': 'htyuu'}}
                        search_expression = json.dumps(search_dict) #str | Contains a custom query expression that applies a filter based on key/value properties (optional)
                        new_datasets = get_datasets(pnnl_client,
                                                subject_uuid,
                                                search_expression,
                                                participant_uuid)
                        print(f"Datasets with search expression: {new_datasets}")
                        #delete_dataset(pnnl_client, dataset_uuid)


def main():
    test_datasets()


if __name__ == "__main__":
    main()
