from __future__ import print_function

import base64
from pprint import pprint
import logging
import argparse
#
import uudex_client
from uudex_client.rest import ApiException
from uudex_client import configurator

#
#
LOG_FORMAT = ('%(levelname) -9s %(asctime)s  %(name) -55s %(funcName) '
              '-35s %(lineno) -4d: %(message)s')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
#

configuration = uudex_client.Configuration()
configurator.set_values(configuration, "pnnl_dev_local")

client = uudex_client.ApiClient(configuration)
subject_api = uudex_client.SubjectApi(client)
subscription_api = uudex_client.SubscriptionApi(client)

# ----------------------------------------------------------------------------------------------
# Testcase 1: Subject with Queue Total Size Constraints and Block Publish
# Publish data > 10kb in 3 kb chunks
# Testcase 2: Subject with Queue Total Size Constraints and Delete Old
# Publish data > 10kb in 3 kb chunks
# Testcase 3: Queue Message Number Constraints and Block Publish
# Publish 4 messages
# Testcase 4: Queue Message Number Constraints and Delete Old
# Publish 4 messages
# ----------------------------------------------------------------------------------------------

testcase_inputs = {"QS_BN": {"SUBSCRIPTON_NAME": "test new_subscription"},
                   "QS_PO": {"SUBSCRIPTON_NAME": "qs_purge_old_subscription"},
                   "MS_BN":  {"SUBSCRIPTON_NAME": "mc_block_new_subscription"},
                   "MS_PO":  {"SUBSCRIPTON_NAME": "mc_purge_old_new_subscription"}}


def run_test(testcase_type):
    try:
        subscription_name = testcase_inputs[testcase_type]["SUBSCRIPTON_NAME"]
        subscription_uuid = None
        subject_uuid = None
        try:
            # Returns a collection of the calling endpoint's Subscriptions
            subscriptions = subscription_api.get_subscriptions()
            for subscription in subscriptions:
                if subscription.subscription_name == subscription_name:
                    subscription_uuid = subscription.subscription_uuid
                    print(f"Found subscription_uuid: {subscription_uuid}")
                    break
        except ApiException as e:
            print("Exception when calling SubscriptionApi->get_subscriptions: %s\n" % e)

        try:
            subscription_subjects = subscription_api.get_subscription_subjects(subscription_uuid)
            if len(subscription_subjects) > 0:
                subject_uuid = subscription_subjects[0].subject_uuid
                print(f"subject uuid: {subject_uuid}")
        except ApiException as e:
            print("Exception when calling SubscriptionApi->get_subscription_subjects: %s\n" % e)

        if testcase_type == "QUEUE_SIZE_BLOCK_NEW" or testcase_type == "QUEUE_SIZE_PURGE_OLD":
            msg = "UUDEX describes a communications architecture and protocol suite used to allow organizations to exchange data and information necessary for reliable and secure operations of an energy delivery system. It can also be used within an organization to facilitate movement of data between control centers.  UUDEX does not consider data exchange between a control center and field equipment, or data exchanges within field sites. Data transferred using UUDEX is described using a modeling language that allow for flexibility and expandability. Models can be developed for existing electric power system data communications, following the Common Information Model (CIM, or IEC 61970), that allows different computer systems to transfer power system information between them without knowing the internal structures of the communications partner.  By using a model-based architecture, modifications and additions can be designed and implemented with minimal impact to any existing data transfers. Using common names from the CIM also allow different systems to be able to coordinate exchanged data with minimal manual coordination, which will significantly reduce the resources and time necessary to modify existing communications links, or add new logical connections. The model-based approach also allows UUDEX to be expanded to serve as a transport for other data by either adopting existing modes (e.g., STIX/TAXII), or creating new models (e.g., RCIS). Models could be widely disseminated (e.g., OE-417 reporting), or used by a specific group of connections (e.g., in a regional market). For organizations in the electricity sector, Figure 1 shows a high-level overview of the potential uses of UUDEX between electric sector organizations described by the NERC functional model. In the figure, the solid lines show logical communications that take place between the control centers or centralized control systems of various organizations that are within scope of UUDEX, while the dashed lines show communications between organization’s control centers and field devices which are out of scope for UUDEX. Not all communications interactions are shown in the figure, but it is clear that a significant number of existing communications interactions could make use of UUDEX. UUDEX could be applied to communications within other energy sectors, such as oil and gas delivery systems in a similar manner. UUDEX can also be used for communications between utility organizations and other non-utility organizations, including government organizations and commercial enterprises. For example, UUDEX could be used for communications between a utility organization and its Information Sharing and Analysis Center (ISAC), the E-ISAC for the electricity sector. It could also be used to communication event and outage information to the Department of Energy (DOE) following the requirements of the OE-417 reporting criteria.  It could be used to coordinate information dissemination about line outage."
        else:
            msg = "- 1235 - test - test - abc"

        for i in range(0, 4):
            message_payload1 = f"Message {i+1}: {msg}"

            if isinstance(message_payload1, str):
                b64_payload1 = message_payload1.encode("utf-8")
            else:
                b64_payload1 = message_payload1

            b64_payload1 = base64.b64encode(b64_payload1)\
                .decode("utf-8")

            print(f"b64_payload1: {message_payload1}")

            resp = subject_api.publish_message(subject_uuid,
                                               body={"message": message_payload1})
            #pprint(resp)

    except Exception as e:
        print("Exception: %s\n" % e)


def main():
    # Create the parser
    my_parser = argparse.ArgumentParser(description='Run Queue performance metrics tests')

    # Add the arguments
    my_parser.add_argument('testcase_type',
                           type=str,
                           help='Testcase type: QS_BN, QS_PO, MS_BN, MS_PO')

    # Execute the parse_args() method
    args = my_parser.parse_args()
    test_types = ["QS_BN, QS_PO, MS_BN, MS_PO"]

    testcase_type = args.testcase_type

    if testcase_type not in test_types:
        print(f"Wrong input. It should be {test_types}")
        exit()

    run_test(testcase_type)


if __name__ == "__main__":
    main()
