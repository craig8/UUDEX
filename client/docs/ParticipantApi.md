# uudex_client.ParticipantApi

All URIs are relative to *https://localhost/v1/uudex*

Method | HTTP request | Description
------------- | ------------- | -------------
[**auth_create_participant**](ParticipantApi.md#auth_create_participant) | **POST** /auth/participants | Create a single Participant
[**auth_create_participant_contact**](ParticipantApi.md#auth_create_participant_contact) | **POST** /auth/participants/{participant_uuid}/contacts | Create a single Participant Contact
[**auth_delete_participant**](ParticipantApi.md#auth_delete_participant) | **DELETE** /auth/participants/{participant_uuid} | Delete a single Participant
[**auth_delete_participant_contact**](ParticipantApi.md#auth_delete_participant_contact) | **DELETE** /auth/participants/{participant_uuid}/contacts/{contact_id} | Delete a single Contact for the Participant
[**auth_get_all_participant_contacts**](ParticipantApi.md#auth_get_all_participant_contacts) | **GET** /auth/participants/{participant_uuid}/contacts | Return a collection of all Contacts for given Participant
[**auth_get_all_participant_groups**](ParticipantApi.md#auth_get_all_participant_groups) | **GET** /auth/participants/{participant_uuid}/groups | Returns a collection of groups the Participant is a member of
[**auth_get_all_participants**](ParticipantApi.md#auth_get_all_participants) | **GET** /auth/participants | Return a collection of all Participants in the system
[**auth_get_participant**](ParticipantApi.md#auth_get_participant) | **GET** /auth/participants/{participant_uuid} | Get a single Participant
[**auth_get_participant_contact**](ParticipantApi.md#auth_get_participant_contact) | **GET** /auth/participants/{participant_uuid}/contacts/{contact_id} | Get a single Contact for the Participant
[**auth_update_participant**](ParticipantApi.md#auth_update_participant) | **PATCH** /auth/participants/{participant_uuid} | Update a single Participant
[**auth_update_participant_contact**](ParticipantApi.md#auth_update_participant_contact) | **PATCH** /auth/participants/{participant_uuid}/contacts/{contact_id} | Update a single Contact for the Participant
[**get_parent_participant**](ParticipantApi.md#get_parent_participant) | **GET** /auth/participants/parent | Returns the calling Endpoint&#x27;s parent Participant

# **auth_create_participant**
> Participant auth_create_participant(body=body)

Create a single Participant

The invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.ParticipantApi()
body = uudex_client.Participant() # Participant |  (optional)

try:
    # Create a single Participant
    api_response = api_instance.auth_create_participant(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ParticipantApi->auth_create_participant: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Participant**](Participant.md)|  | [optional] 

### Return type

[**Participant**](Participant.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_create_participant_contact**
> Contact auth_create_participant_contact(participant_uuid, body=body)

Create a single Participant Contact

The invoker must be belong to the same Participant it is attempting to create a Contact for AND it must have the ParticipantAdmin role.  A UUDEX Admin may create any Contact for any Participant.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.ParticipantApi()
participant_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
body = uudex_client.Contact() # Contact |  (optional)

try:
    # Create a single Participant Contact
    api_response = api_instance.auth_create_participant_contact(participant_uuid, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ParticipantApi->auth_create_participant_contact: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **participant_uuid** | [**str**](.md)|  | 
 **body** | [**Contact**](Contact.md)|  | [optional] 

### Return type

[**Contact**](Contact.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_delete_participant**
> auth_delete_participant(participant_uuid)

Delete a single Participant

The invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.ParticipantApi()
participant_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Delete a single Participant
    api_instance.auth_delete_participant(participant_uuid)
except ApiException as e:
    print("Exception when calling ParticipantApi->auth_delete_participant: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **participant_uuid** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_delete_participant_contact**
> auth_delete_participant_contact(participant_uuid, contact_id)

Delete a single Contact for the Participant

The invoker must be belong to the same Participant it is attempting to delete the Contact for AND it must have the ParticipantAdmin role.  A UUDEX Admin may delete any Contact for any Participant.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.ParticipantApi()
participant_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
contact_id = 56 # int | 

try:
    # Delete a single Contact for the Participant
    api_instance.auth_delete_participant_contact(participant_uuid, contact_id)
except ApiException as e:
    print("Exception when calling ParticipantApi->auth_delete_participant_contact: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **participant_uuid** | [**str**](.md)|  | 
 **contact_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_get_all_participant_contacts**
> list[Contact] auth_get_all_participant_contacts(participant_uuid)

Return a collection of all Contacts for given Participant

The invoker must be belong to the same Participant it is attempting to get the Contacts for AND it must have the ParticipantAdmin role.  A UUDEX Admin may get the Contacts for any Participant.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.ParticipantApi()
participant_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Return a collection of all Contacts for given Participant
    api_response = api_instance.auth_get_all_participant_contacts(participant_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ParticipantApi->auth_get_all_participant_contacts: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **participant_uuid** | [**str**](.md)|  | 

### Return type

[**list[Contact]**](Contact.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_get_all_participant_groups**
> list[GenericAuthObject] auth_get_all_participant_groups(participant_uuid)

Returns a collection of groups the Participant is a member of

The invoker must belong to the Participant it is passing in AND it must have the ParticipantAdmin role.  A UUDEX Admin may invoke this call without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.ParticipantApi()
participant_uuid = 'participant_uuid_example' # str | 

try:
    # Returns a collection of groups the Participant is a member of
    api_response = api_instance.auth_get_all_participant_groups(participant_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ParticipantApi->auth_get_all_participant_groups: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **participant_uuid** | **str**|  | 

### Return type

[**list[GenericAuthObject]**](GenericAuthObject.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_get_all_participants**
> list[Participant] auth_get_all_participants()

Return a collection of all Participants in the system

The invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.ParticipantApi()

try:
    # Return a collection of all Participants in the system
    api_response = api_instance.auth_get_all_participants()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ParticipantApi->auth_get_all_participants: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Participant]**](Participant.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_get_participant**
> Participant auth_get_participant(participant_uuid)

Get a single Participant

The invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.ParticipantApi()
participant_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Get a single Participant
    api_response = api_instance.auth_get_participant(participant_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ParticipantApi->auth_get_participant: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **participant_uuid** | [**str**](.md)|  | 

### Return type

[**Participant**](Participant.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_get_participant_contact**
> Contact auth_get_participant_contact(participant_uuid, contact_id)

Get a single Contact for the Participant

The invoker must be belong to the same Participant it is attempting to get the Contact for AND it must have the ParticipantAdmin role.  A UUDEX Admin may get any Contact for any Participant.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.ParticipantApi()
participant_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
contact_id = 56 # int | 

try:
    # Get a single Contact for the Participant
    api_response = api_instance.auth_get_participant_contact(participant_uuid, contact_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ParticipantApi->auth_get_participant_contact: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **participant_uuid** | [**str**](.md)|  | 
 **contact_id** | **int**|  | 

### Return type

[**Contact**](Contact.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_update_participant**
> Participant auth_update_participant(participant_uuid, body=body)

Update a single Participant

The invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.ParticipantApi()
participant_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
body = uudex_client.Participant() # Participant |  (optional)

try:
    # Update a single Participant
    api_response = api_instance.auth_update_participant(participant_uuid, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ParticipantApi->auth_update_participant: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **participant_uuid** | [**str**](.md)|  | 
 **body** | [**Participant**](Participant.md)|  | [optional] 

### Return type

[**Participant**](Participant.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_update_participant_contact**
> Contact auth_update_participant_contact(participant_uuid, contact_id, body=body)

Update a single Contact for the Participant

The invoker must be belong to the same Participant it is attempting to update the Contact for AND it must have the ParticipantAdmin role.    A UUDEX Admin may update any Contact for any Participant.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.ParticipantApi()
participant_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
contact_id = 56 # int | 
body = uudex_client.Contact() # Contact |  (optional)

try:
    # Update a single Contact for the Participant
    api_response = api_instance.auth_update_participant_contact(participant_uuid, contact_id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ParticipantApi->auth_update_participant_contact: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **participant_uuid** | [**str**](.md)|  | 
 **contact_id** | **int**|  | 
 **body** | [**Contact**](Contact.md)|  | [optional] 

### Return type

[**Contact**](Contact.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_parent_participant**
> ParticipantEnriched get_parent_participant()

Returns the calling Endpoint's parent Participant

Returns the invoker's parent Participant

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.ParticipantApi()

try:
    # Returns the calling Endpoint's parent Participant
    api_response = api_instance.get_parent_participant()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ParticipantApi->get_parent_participant: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ParticipantEnriched**](ParticipantEnriched.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

