# uudex_client.RoleApi

All URIs are relative to *https://localhost/v1/uudex*

Method | HTTP request | Description
------------- | ------------- | -------------
[**auth_create_role**](RoleApi.md#auth_create_role) | **POST** /auth/roles | Create a single Role
[**auth_delete_role**](RoleApi.md#auth_delete_role) | **DELETE** /auth/roles/{role_uuid} | Delete a single Role
[**auth_get_all_roles**](RoleApi.md#auth_get_all_roles) | **GET** /auth/roles | Return a collection of all Roles in the system
[**auth_get_role**](RoleApi.md#auth_get_role) | **GET** /auth/roles/{role_uuid} | Get a single Role
[**auth_get_role_endpoints**](RoleApi.md#auth_get_role_endpoints) | **GET** /auth/roles/{role_uuid}/endpoints | Returns all Endpoints that have been granted the given Role
[**auth_grant_role**](RoleApi.md#auth_grant_role) | **POST** /auth/roles/{role_uuid}/endpoints | Grant role to the given Endpoint
[**auth_update_role**](RoleApi.md#auth_update_role) | **PATCH** /auth/roles/{role_uuid} | Update a single Role

# **auth_create_role**
> Role auth_create_role(body=body)

Create a single Role

Only a UUDEX Admin can create a role.  The invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.RoleApi()
body = uudex_client.Role() # Role |  (optional)

try:
    # Create a single Role
    api_response = api_instance.auth_create_role(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RoleApi->auth_create_role: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Role**](Role.md)|  | [optional] 

### Return type

[**Role**](Role.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_delete_role**
> auth_delete_role(role_uuid)

Delete a single Role

The invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.RoleApi()
role_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Delete a single Role
    api_instance.auth_delete_role(role_uuid)
except ApiException as e:
    print("Exception when calling RoleApi->auth_delete_role: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_uuid** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_get_all_roles**
> list[Role] auth_get_all_roles()

Return a collection of all Roles in the system

This endpoint open to to all users on the system

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.RoleApi()

try:
    # Return a collection of all Roles in the system
    api_response = api_instance.auth_get_all_roles()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RoleApi->auth_get_all_roles: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Role]**](Role.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_get_role**
> Role auth_get_role(role_uuid)

Get a single Role

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.RoleApi()
role_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Get a single Role
    api_response = api_instance.auth_get_role(role_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RoleApi->auth_get_role: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_uuid** | [**str**](.md)|  | 

### Return type

[**Role**](Role.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_get_role_endpoints**
> list[Endpoint] auth_get_role_endpoints(role_uuid)

Returns all Endpoints that have been granted the given Role

The invoker must have the either the ParticipantAdmin role or the RoleAdmin role.  A UUDEX Admin may invoke this call without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.RoleApi()
role_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Returns all Endpoints that have been granted the given Role
    api_response = api_instance.auth_get_role_endpoints(role_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RoleApi->auth_get_role_endpoints: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_uuid** | [**str**](.md)|  | 

### Return type

[**list[Endpoint]**](Endpoint.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_grant_role**
> EndpointUuid auth_grant_role(role_uuid, body=body)

Grant role to the given Endpoint

The invoker must belong to the same Participant as the Endpoint it's granting the role to AND the invoker must have the either the ParticipantAdmin role or the RoleAdmin role.  A UUDEX Admin may invoke this call without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.RoleApi()
role_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
body = uudex_client.EndpointUuid() # EndpointUuid |  (optional)

try:
    # Grant role to the given Endpoint
    api_response = api_instance.auth_grant_role(role_uuid, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RoleApi->auth_grant_role: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_uuid** | [**str**](.md)|  | 
 **body** | [**EndpointUuid**](EndpointUuid.md)|  | [optional] 

### Return type

[**EndpointUuid**](EndpointUuid.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_update_role**
> Role auth_update_role(role_uuid, body=body)

Update a single Role

The invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.RoleApi()
role_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
body = uudex_client.Role() # Role |  (optional)

try:
    # Update a single Role
    api_response = api_instance.auth_update_role(role_uuid, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RoleApi->auth_update_role: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_uuid** | [**str**](.md)|  | 
 **body** | [**Role**](Role.md)|  | [optional] 

### Return type

[**Role**](Role.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

