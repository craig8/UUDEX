# uudex_client.GroupApi

All URIs are relative to *https://localhost/v1/uudex*

Method | HTTP request | Description
------------- | ------------- | -------------
[**auth_add_group_manager**](GroupApi.md#auth_add_group_manager) | **POST** /auth/groups/{group_uuid}/managers | Adds a Group Manager to a Group
[**auth_add_group_member**](GroupApi.md#auth_add_group_member) | **POST** /auth/groups/{group_uuid}/members | Add a member to a group
[**auth_create_group**](GroupApi.md#auth_create_group) | **POST** /auth/groups | Create a single Group
[**auth_delete_group**](GroupApi.md#auth_delete_group) | **DELETE** /auth/groups/{group_uuid} | Delete a single Group
[**auth_get_all_group_managers**](GroupApi.md#auth_get_all_group_managers) | **GET** /auth/groups/{group_uuid}/managers | Return a collection of Group Managers for the given Group
[**auth_get_all_group_members**](GroupApi.md#auth_get_all_group_members) | **GET** /auth/groups/{group_uuid}/members | Return a collection of Group Members for the given Group
[**auth_get_all_groups**](GroupApi.md#auth_get_all_groups) | **GET** /auth/groups | Return a collection of all Groups the invoker has manage rights to
[**auth_get_group**](GroupApi.md#auth_get_group) | **GET** /auth/groups/{group_uuid} | Get a single Group
[**auth_remove_group_manager**](GroupApi.md#auth_remove_group_manager) | **DELETE** /auth/groups/{group_uuid}/managers/{object_uuid} | Remove a Group Manager from a Group
[**auth_remove_group_member**](GroupApi.md#auth_remove_group_member) | **DELETE** /auth/groups/{group_uuid}/members/{object_uuid} | Remove a member from a Group
[**auth_update_group**](GroupApi.md#auth_update_group) | **PATCH** /auth/groups/{group_uuid} | Update a single Group

# **auth_add_group_manager**
> GenericAuthObject auth_add_group_manager(group_uuid, body=body)

Adds a Group Manager to a Group

The Group Manager can be an Endpoint, a Participant or another Group.  The invoker must be a Group Manager of the group.  A UUDEX Admin may invoke this call without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.GroupApi()
group_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
body = uudex_client.GenericAuthObject() # GenericAuthObject |  (optional)

try:
    # Adds a Group Manager to a Group
    api_response = api_instance.auth_add_group_manager(group_uuid, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GroupApi->auth_add_group_manager: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_uuid** | [**str**](.md)|  | 
 **body** | [**GenericAuthObject**](GenericAuthObject.md)|  | [optional] 

### Return type

[**GenericAuthObject**](GenericAuthObject.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_add_group_member**
> GenericAuthObject auth_add_group_member(group_uuid, body=body)

Add a member to a group

The invoker must be a Group Manager of the group.  May add an endpoint or a participant to a group.  A UUDEX Admin may invoke this call without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.GroupApi()
group_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
body = uudex_client.GenericAuthObject() # GenericAuthObject |  (optional)

try:
    # Add a member to a group
    api_response = api_instance.auth_add_group_member(group_uuid, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GroupApi->auth_add_group_member: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_uuid** | [**str**](.md)|  | 
 **body** | [**GenericAuthObject**](GenericAuthObject.md)|  | [optional] 

### Return type

[**GenericAuthObject**](GenericAuthObject.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_create_group**
> auth_create_group()

Create a single Group

Only a UUDEX Admin may create a group, thus the invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.GroupApi()

try:
    # Create a single Group
    api_instance.auth_create_group()
except ApiException as e:
    print("Exception when calling GroupApi->auth_create_group: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_delete_group**
> auth_delete_group(group_uuid)

Delete a single Group

Only a UUDEX Admin may delete a group.  The invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.GroupApi()
group_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Delete a single Group
    api_instance.auth_delete_group(group_uuid)
except ApiException as e:
    print("Exception when calling GroupApi->auth_delete_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_uuid** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_get_all_group_managers**
> list[GenericAuthObject] auth_get_all_group_managers(group_uuid)

Return a collection of Group Managers for the given Group

The invoker must be a Group Manager for the group.  A UUDEX Admin may invoke this call without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.GroupApi()
group_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Return a collection of Group Managers for the given Group
    api_response = api_instance.auth_get_all_group_managers(group_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GroupApi->auth_get_all_group_managers: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_uuid** | [**str**](.md)|  | 

### Return type

[**list[GenericAuthObject]**](GenericAuthObject.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_get_all_group_members**
> list[GenericAuthObject] auth_get_all_group_members(group_uuid)

Return a collection of Group Members for the given Group

The invoker must be a Group Manager of the group.  A UUDEX Admin may invoke this call without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.GroupApi()
group_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Return a collection of Group Members for the given Group
    api_response = api_instance.auth_get_all_group_members(group_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GroupApi->auth_get_all_group_members: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_uuid** | [**str**](.md)|  | 

### Return type

[**list[GenericAuthObject]**](GenericAuthObject.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_get_all_groups**
> list[Group] auth_get_all_groups()

Return a collection of all Groups the invoker has manage rights to

This call return all groups for which the invoker is a Group Manager.  A UUDEX Admin may invoke this call without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.GroupApi()

try:
    # Return a collection of all Groups the invoker has manage rights to
    api_response = api_instance.auth_get_all_groups()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GroupApi->auth_get_all_groups: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Group]**](Group.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_get_group**
> Group auth_get_group(group_uuid)

Get a single Group

The invoker must be a Group Manager for the group.  A UUDEX Admin may invoke this call without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.GroupApi()
group_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Get a single Group
    api_response = api_instance.auth_get_group(group_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GroupApi->auth_get_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_uuid** | [**str**](.md)|  | 

### Return type

[**Group**](Group.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_remove_group_manager**
> auth_remove_group_manager(group_uuid, object_uuid, object_type)

Remove a Group Manager from a Group

The invoker must be a Group Manager of the group.  A UUDEX Admin may invoke this call without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.GroupApi()
group_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
object_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | Represents the Group Manager and is the UUID of either an Endpoint, a Participant or another Group.
object_type = 'object_type_example' # str | The object type of the object_uuid param.  Can be e or p for Endpoint or Participant

try:
    # Remove a Group Manager from a Group
    api_instance.auth_remove_group_manager(group_uuid, object_uuid, object_type)
except ApiException as e:
    print("Exception when calling GroupApi->auth_remove_group_manager: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_uuid** | [**str**](.md)|  | 
 **object_uuid** | [**str**](.md)| Represents the Group Manager and is the UUID of either an Endpoint, a Participant or another Group. | 
 **object_type** | **str**| The object type of the object_uuid param.  Can be e or p for Endpoint or Participant | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_remove_group_member**
> auth_remove_group_member(group_uuid, object_uuid, object_type)

Remove a member from a Group

The invoker must be a Group Manager of the group.  A UUDEX Admin may invoke this call without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.GroupApi()
group_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
object_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | Represents the group member and is the UUID of either an Endpoint or a Participant.  Note, a group cannot be assigned to another group.
object_type = 'object_type_example' # str | The object type of the object_uuid param.  Can be e for Endpoint or p for Participant.

try:
    # Remove a member from a Group
    api_instance.auth_remove_group_member(group_uuid, object_uuid, object_type)
except ApiException as e:
    print("Exception when calling GroupApi->auth_remove_group_member: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_uuid** | [**str**](.md)|  | 
 **object_uuid** | [**str**](.md)| Represents the group member and is the UUID of either an Endpoint or a Participant.  Note, a group cannot be assigned to another group. | 
 **object_type** | **str**| The object type of the object_uuid param.  Can be e for Endpoint or p for Participant. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_update_group**
> Group auth_update_group(group_uuid, body=body)

Update a single Group

Only a UUDEX Admin may update a group thus the invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.GroupApi()
group_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
body = uudex_client.Group() # Group |  (optional)

try:
    # Update a single Group
    api_response = api_instance.auth_update_group(group_uuid, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GroupApi->auth_update_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_uuid** | [**str**](.md)|  | 
 **body** | [**Group**](Group.md)|  | [optional] 

### Return type

[**Group**](Group.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

