import base64

import uudex_client
from uudex_client import configurator
from uudex_client.rest import ApiException

class UudexThinWrapper():

    def __init__(self, sites):
        self.clients = {}
        self.configurations = {}

        for item in sites:
          configuration = uudex_client.Configuration()
          configurator.set_values(configuration, item)
          client = uudex_client.ApiClient(configuration)
          self.clients[item] = client
          self.configurations[item] = configuration


    def get_parent_participant(self, connection):
        participant_api = uudex_client.ParticipantApi(self.clients[connection])
        participant = participant_api.get_parent_participant()
        return participant

    def get_discoverable_subjects(self, connection):
        subject_api = uudex_client.SubjectApi(self.clients[connection])
        subjects = subject_api.discover_subjects()
        return subjects

    def get_subscriptions(self, connection):
        try:
          subscription_api = uudex_client.SubscriptionApi(self.clients[connection])
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
        subject_api = uudex_client.SubjectApi(self.clients[connection])
        pub_resp = subject_api.publish_message(subject_uuid, body=message_list)
        return pub_resp

    def consume_subscription(self, connection, subscription_uuid):
        subscription_api = uudex_client.SubscriptionApi(self.clients[connection])
        messages = subscription_api.consume_subscription(subscription_uuid)
        return messages


    def get_subject_acls(self, connection, subject_uuid):
        try:
          subject_acl_api = uudex_client.SubjectAclApi(self.clients[connection])
          acls = subject_acl_api.get_subject_acls(subject_uuid)
          return acls
        except ApiException as e:
          return []

    def get_participants(self, connection):

        participant_api = uudex_client.ParticipantApi(self.clients[connection])
        p = participant_api.admin_get_all_participants()
        return p

    def grant_acl(self, connection, subject_uuid, privilege_name, grant_scope_name, participant_uuid_list):
        subject_acl_api = uudex_client.SubjectAclApi(self.clients[connection])
        # try:
        #     subject_acl_api.revoke_subject_acl_privilege(subject_uuid, privilege_name)
        # except Exception as e:
        #     print("Error revoke_subject_acl_privilege")
        #     pass

        body = uudex_client.SubjectAcl(privilege_name=privilege_name, grant_scope_name=grant_scope_name,
                                       participant_uuid_list=participant_uuid_list)
        print(f"SubjectAcl: {body}")
        return subject_acl_api.grant_subject_acl_privilege(subject_uuid, body=body)


    def create_subject(self, connection, subject_name, instance_key, desc, sub_type, fulfillment_type, dataset_definition_uuid):
        subject_api = uudex_client.SubjectApi(self.clients[connection])
        body = uudex_client.Subject(subject_name=subject_name, dataset_instance_key=instance_key,
                                    description=desc, subscription_type=sub_type,
                                    fulfillment_types_available = fulfillment_type,
                                    dataset_definition_uuid = dataset_definition_uuid)
        return subject_api.create_subject(body=body)

    def publish_file(self, connection, subject_uuid, message, dataset_name, description):
        uudex_publisher = uudex_client.publish_helper.UudexPublisher(self.configurations[connection])
        created_dataset = uudex_publisher.publish(subject_uuid, message, dataset_name=dataset_name, description=description)
        return created_dataset

    def get_subscriptions(self, connection):
        subscription_api = uudex_client.SubscriptionApi(self.clients[connection])
        subscriptions = None

        try:
            # Returns a collection of the calling endpoint's Subscriptions
            subscriptions = subscription_api.get_subscriptions()
        except ApiException as e:
            print("Exception when calling SubscriptionApi->get_subscriptions: %s\n" % e)
        return subscriptions

    def create_subscription(self, connection, subscription_name):
        subscription_api = uudex_client.SubscriptionApi(self.clients[connection])
        body = uudex_client.Subscription(subscription_name=subscription_name, subscription_state='ACTIVE')
        subscription = subscription_api.create_subscription(body=body)
        return subscription

    def attach_subject(self, connection, subscription_uuid, subject_uuid, preferred_fulfillment_type='DATA_NOTIFY'):
        subscription_api = uudex_client.SubscriptionApi(self.clients[connection])
        body = uudex_client.SubscriptionSubject(subject_uuid=subject_uuid,
                                                preferred_fulfillment_type=preferred_fulfillment_type)
        subscription_api.attach_subscription_subject(subscription_uuid, body=body)

    def get_datasets(self, connection, subject_uuid):
        try:
          dataset_api = uudex_client.DatasetApi(self.clients[connection])
          return dataset_api.get_datasets(subject_uuid=subject_uuid, search_expression=None, participant_uuid=None)
        except ApiException as e:
          return []

    def get_dataset_payload(self, connection, dataset_uuid):
        dataset_api = uudex_client.DatasetApi(self.clients[connection])
        dataset = dataset_api.get_dataset(dataset_uuid)
        b64_blob = dataset.payload
        if isinstance(b64_blob, str):
          b64_blob = b64_blob.encode("utf-8")  # if string, turn it into byte array first
        blob = base64.b64decode(b64_blob)
        return blob

    def create_subject_policy(self, connection, dataset_def_uuid, full_queue_behavior=None, max_message_count=None, max_queue_size_kb=None):
        policy = None
        body = uudex_client.SubjectPolicy(action="ALLOW",
                                          full_queue_behavior=full_queue_behavior,
                                          max_message_count=max_message_count,
                                          max_queue_size_kb=max_queue_size_kb,
                                          dataset_definition_uuid=dataset_def_uuid)

        try:
            #print(f"Creating subject policy::{body}")
            subject_policy_api = uudex_client.SubjectPolicyApi(self.clients[connection])
            # Creates a Subject Policy and attaches it to given Participant
            policy = subject_policy_api.admin_create_subject_policy(body=body)
            #pprint(api_response)
        except ApiException as e:
            print("Exception when calling SubjectPolicyApi->admin_create_subject_policy: %s\n" % e)
        return policy

    def get_dataset_defintions(self, connection):
        dataset_defs = []
        dataset_def_api = uudex_client.DatasetDefinitionApi(self.clients[connection])
        try:
            # Returns a collection of all Datasets Definitions in the system
            dataset_defs = dataset_def_api.get_all_dataset_definitions()
        except ApiException as e:
            print("Exception when calling DatasetDefinitionApi->get_all_dataset_definitions: %s\n" % e)
        return dataset_defs

    def create_dataset_definition(self, connection, definition_name, definition_description):
        dataset_def_uuid = None
        # Create dataset definition
        body = uudex_client.DatasetDefinition(dataset_definition_name=definition_name,
                                              description=definition_description) # DatasetDefinition |  (optional)
        try:
            #print("Creating dataset definition::")
            dataset_def_api = uudex_client.DatasetDefinitionApi(self.clients[connection])
            # Create a single Dataset Definition
            dataset_definition = dataset_def_api.admin_create_dataset_definition(body=body)
            dataset_def_uuid = dataset_definition.dataset_definition_uuid
        except ApiException as e:
            print("Exception when calling DatasetDefinitionApi->admin_create_dataset_definition: %s\n" % e)
        return dataset_def_uuid

    def get_admin_subjects(self, connection):
        subjects = []
        try:
            subject_api = uudex_client.SubjectApi(self.clients[connection])
            # Returns a collection of Subjects the calling endpoint is authorized to view.
            # Optionally filter by subject name.
            subjects = subject_api.admin_get_all_subjects()
        except ApiException as e:
            print("Exception when calling SubjectApi->discover_subjects: %s\n" % e)
        return subjects

    def create_subject_with_q_behavior(self, connection, subject_name, instance_key, desc, sub_type, fulfillment_type,
                                       dataset_definition_uuid, owner_participant_uuid, full_queue_behavior,
                                       max_queue_size_kb=None, max_message_count=None):
        subject_api = uudex_client.SubjectApi(self.clients[connection])
        if max_queue_size_kb is not None:
            body = uudex_client.Subject(subject_name=subject_name, dataset_instance_key=instance_key,
                                    description=desc, subscription_type=sub_type,
                                    fulfillment_types_available = fulfillment_type,
                                    full_queue_behavior=full_queue_behavior,
                                    max_queue_size_kb=max_queue_size_kb,
                                    dataset_definition_uuid=dataset_definition_uuid,
                                    owner_participant_uuid=owner_participant_uuid)
        elif max_message_count is not None:
            body = uudex_client.Subject(subject_name=subject_name, dataset_instance_key=instance_key,
                                    description=desc, subscription_type=sub_type,
                                    fulfillment_types_available = fulfillment_type,
                                    full_queue_behavior=full_queue_behavior,
                                    max_message_count=max_message_count,
                                    dataset_definition_uuid=dataset_definition_uuid,
                                    owner_participant_uuid=owner_participant_uuid)
        return subject_api.create_subject(body=body)

    def delete_policy(self, connection, subject_policy_uuid):
        try:
            subject_policy_api = uudex_client.SubjectPolicyApi(self.clients[connection])
            # Delete a single Subject Policy
            subject_policy_api.admin_delete_subject_policy(subject_policy_uuid)
        except ApiException as e:
            print("Exception when calling SubjectPolicyApi->admin_delete_subject_policy: %s\n" % e)

    def delete_subscription(self, connection, subscription_uuid):
        subscription_api = uudex_client.SubscriptionApi(self.clients[connection])
        try:
            # Delete an endpoint's Subscription
            subscription_api.delete_subscription(subscription_uuid)
        except ApiException as e:
            print("Exception when calling SubscriptionApi->delete_subscription: %s\n" % e)

    def delete_subject(self, connection, subject_uuid):
        subject_api = uudex_client.SubjectApi(self.clients[connection])
        try:
            # Delete subject
            subject_api.admin_delete_subject(subject_uuid)
        except ApiException as e:
            print("xception when calling SubjectApi->admin_delete_subject: %s\n" % e)

    def revoke_subject_acl(self, connection, subject_uuid, priviledge_name):
        subject_acl_api = uudex_client.SubjectAclApi(self.clients[connection])
        try:
            # Revoke a privilege from the Subject's ACL. Caller must own Subject.
            subject_acl_api.revoke_subject_acl_privilege(subject_uuid, priviledge_name)
        except ApiException as e:
            pass
            #print("Exception when calling SubjectAclApi->revoke_subject_acl_privilege: %s\n" % e)

    def create_participant(self, connection, participant_short_name, participant_long_name, description):
        participant_uuid = None
        participant_api = uudex_client.ParticipantApi(self.clients[connection])
        try:
            body = uudex_client.Participant(participant_short_name=participant_short_name,
                                            participant_long_name=participant_long_name,
                                            description=description, root_org_sw="N", active_sw="Y")
            # Create a single Participant
            participant = participant_api.admin_create_participant(body=body)
            participant_uuid = participant.participant_uuid
        except ApiException as e:
            print("Exception when calling ParticipantApi->admin_create_participant: %s\n" % e)
        return participant_uuid

    def get_endpoints(self, connection):
        endpoints = []
        try:
            endpoint_api = uudex_client.EndpointApi(self.clients[connection])
            # Return a collection of all Endpoints in the system
            endpoints = endpoint_api.admin_get_all_endpoints()
        except ApiException as e:
            print("Exception when calling EndpointApi->admin_get_all_endpoints: %s\n" % e)
        return endpoints

    def create_endpoint(self, connection, endpoint_user_name, endpoint_description, participant_uuid, active_sw='Y',
                        uudex_administrator_sw='N', participant_administrator_sw='N'):
        endpoint_uuid = None
        endpoint_api = uudex_client.EndpointApi(self.clients[connection])
        body = uudex_client.Endpoint(endpoint_user_name=endpoint_user_name, certificate_dn=endpoint_user_name,
                                     description=endpoint_description, active_sw=active_sw,
                                     uudex_administrator_sw=uudex_administrator_sw,
                                     participant_administrator_sw=participant_administrator_sw,
                                     participant_uuid=participant_uuid)  # Endpoint |  (optional)

        try:
            # Create a single Endpoint
            endpoint = endpoint_api.admin_create_endpoint(body=body)
            endpoint_uuid = endpoint.endpoint_uuid
        except ApiException as e:
            print("Exception when calling EndpointApi->admin_create_endpoint: %s\n" % e)
        return endpoint_uuid

    def get_subscription_subjects(self, connection, subscription_uuid):
        subscription_api = uudex_client.SubscriptionApi(self.clients[connection])
        subscription_subjects = None
        try:
            # Returns a collection of Subjects attached to the calling endpoint's given Subscription
            subscription_subjects = subscription_api.get_subscription_subjects(subscription_uuid)
        except ApiException as e:
            print("Exception when calling SubscriptionApi->get_subscription_subjects: %s\n" % e)

        return subscription_subjects