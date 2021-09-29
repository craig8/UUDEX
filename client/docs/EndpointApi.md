# uudex_client.EndpointApi

All URIs are relative to *https://localhost/v1/uudex*

Method | HTTP request | Description
------------- | ------------- | -------------
[**auth_create_endpoint**](EndpointApi.md#auth_create_endpoint) | **POST** /auth/endpoints | Create a single Endpoint
[**auth_delete_endpoint**](EndpointApi.md#auth_delete_endpoint) | **DELETE** /auth/endpoints/{endpoint_uuid} | Delete an Endpoint
[**auth_get_all_endpoint_groups**](EndpointApi.md#auth_get_all_endpoint_groups) | **GET** /auth/endpoints/{endpoint_uuid}/groups | Returns a collection of groups the Endpoint is a member of
[**auth_get_all_endpoint_roles**](EndpointApi.md#auth_get_all_endpoint_roles) | **GET** /auth/endpoints/{endpoint_uuid}/roles | Returns a collection of Roles the Endpoint is a member of
[**auth_get_all_endpoints**](EndpointApi.md#auth_get_all_endpoints) | **GET** /auth/endpoints | Return a collection of all Endpoints in the system
[**auth_get_endpoint**](EndpointApi.md#auth_get_endpoint) | **GET** /auth/endpoints/{endpoint_uuid} | Get a single Endpoint
[**auth_update_endpoint**](EndpointApi.md#auth_update_endpoint) | **PATCH** /auth/endpoints/{endpoint_uuid} | Update a single Endpoint
[**get_peer_endpoints**](EndpointApi.md#get_peer_endpoints) | **GET** /auth/endpoints/peers | Returns a collection of all peer Endpoints in the calling Endpoint&#x27;s Participant (organization)

# **auth_create_endpoint**
> Endpoint auth_create_endpoint(body=body)

Create a single Endpoint

Create an Endpoint for the Participant that the invoker belongs to. The invoker must have the ParticipantAdmin role.  A UUDEX Administrator may create any Endpoint for any Participant.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.EndpointApi()
body = uudex_client.Endpoint() # Endpoint |  (optional)

try:
    # Create a single Endpoint
    api_response = api_instance.auth_create_endpoint(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EndpointApi->auth_create_endpoint: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Endpoint**](Endpoint.md)|  | [optional] 

### Return type

[**Endpoint**](Endpoint.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_delete_endpoint**
> auth_delete_endpoint(endpoint_uuid)

Delete an Endpoint

The Endpoint must belong to the same Participant the invoker belongs to AND the invoker must have the ParticipantAdmin role.    A UUDEX Admin may delete any Endpoint.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.EndpointApi()
endpoint_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Delete an Endpoint
    api_instance.auth_delete_endpoint(endpoint_uuid)
except ApiException as e:
    print("Exception when calling EndpointApi->auth_delete_endpoint: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **endpoint_uuid** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_get_all_endpoint_groups**
> list[GenericAuthObject] auth_get_all_endpoint_groups(endpoint_uuid)

Returns a collection of groups the Endpoint is a member of

The Endpoint must belong to the same Participant as the invoker AND the invoker must have the ParticipantAdmin role.  A UUDEX Admin may invoke this call without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.EndpointApi()
endpoint_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Returns a collection of groups the Endpoint is a member of
    api_response = api_instance.auth_get_all_endpoint_groups(endpoint_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EndpointApi->auth_get_all_endpoint_groups: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **endpoint_uuid** | [**str**](.md)|  | 

### Return type

[**list[GenericAuthObject]**](GenericAuthObject.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_get_all_endpoint_roles**
> list[GenericAuthObject] auth_get_all_endpoint_roles(endpoint_uuid)

Returns a collection of Roles the Endpoint is a member of

The Endpoint must belong to the same Participant as the invoker AND the invoker must have either the ParticipantAdmin role or the RoleAdmin role.  A UUDEX Admin may invoke this call without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.EndpointApi()
endpoint_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Returns a collection of Roles the Endpoint is a member of
    api_response = api_instance.auth_get_all_endpoint_roles(endpoint_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EndpointApi->auth_get_all_endpoint_roles: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **endpoint_uuid** | [**str**](.md)|  | 

### Return type

[**list[GenericAuthObject]**](GenericAuthObject.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_get_all_endpoints**
> list[Endpoint] auth_get_all_endpoints()

Return a collection of all Endpoints in the system

The invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.EndpointApi()

try:
    # Return a collection of all Endpoints in the system
    api_response = api_instance.auth_get_all_endpoints()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EndpointApi->auth_get_all_endpoints: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Endpoint]**](Endpoint.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_get_endpoint**
> Endpoint auth_get_endpoint(endpoint_uuid)

Get a single Endpoint

The Endpoint must belong to the same Participant the invoker belongs to.  A UUDEX Admin may get any Endpoint.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.EndpointApi()
endpoint_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Get a single Endpoint
    api_response = api_instance.auth_get_endpoint(endpoint_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EndpointApi->auth_get_endpoint: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **endpoint_uuid** | [**str**](.md)|  | 

### Return type

[**Endpoint**](Endpoint.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_update_endpoint**
> Endpoint auth_update_endpoint(endpoint_uuid, body=body)

Update a single Endpoint

The Endpoint must belong to the same Participant the invoker belongs to AND the invoker must have the ParticipantAdmin role.    A UUDEX Admin may update any Endpoint.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.EndpointApi()
endpoint_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
body = uudex_client.Endpoint() # Endpoint |  (optional)

try:
    # Update a single Endpoint
    api_response = api_instance.auth_update_endpoint(endpoint_uuid, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EndpointApi->auth_update_endpoint: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **endpoint_uuid** | [**str**](.md)|  | 
 **body** | [**Endpoint**](Endpoint.md)|  | [optional] 

### Return type

[**Endpoint**](Endpoint.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_peer_endpoints**
> list[Endpoint] get_peer_endpoints()

Returns a collection of all peer Endpoints in the calling Endpoint's Participant (organization)

Returns a collection of peer Endpoints that are part of the invoker's Participant.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.EndpointApi()

try:
    # Returns a collection of all peer Endpoints in the calling Endpoint's Participant (organization)
    api_response = api_instance.get_peer_endpoints()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EndpointApi->get_peer_endpoints: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Endpoint]**](Endpoint.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

