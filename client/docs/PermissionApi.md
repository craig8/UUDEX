# uudex_client.PermissionApi

All URIs are relative to *https://localhost/v1/uudex*

Method | HTTP request | Description
------------- | ------------- | -------------
[**auth_get_permissions**](PermissionApi.md#auth_get_permissions) | **GET** /auth/permissions/{object_uuid} | Returns a collection of all explicit and implicit permissions granted to an object
[**auth_grant_permission**](PermissionApi.md#auth_grant_permission) | **POST** /auth/permissions | Creates a permission by granting a privilege on a Subject to an object
[**auth_revoke_permission**](PermissionApi.md#auth_revoke_permission) | **DELETE** /auth/permissions/{privilege}/subject/{subject_uuid}/target/{object_uuid} | Remove a permission by revoking a privilege on a Subject from an object

# **auth_get_permissions**
> list[Permission] auth_get_permissions(object_uuid, object_type)

Returns a collection of all explicit and implicit permissions granted to an object

1. For object_uuid of type Subject the invoker must have the ParticipantAdmin role or the SubjectAdmin role.  2. For object_uuid of type Group the invoker must be a Group Manager for the group.  3. For object_uuid of type Role the invoker must have the RoleAdmin role.  4. For object_uuid of type Endpoint or type Participant the invoker must have the ParticipantAdmin role   5. A UUDEX Admin may invoke this call without restrictions. 

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.PermissionApi()
object_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | The UUID of either an Endpoint, a Participant, a Group , a Role or a Subject.
object_type = 'object_type_example' # str | The object type of the object_uuid param.  This code can be s, r, g, e or p, which represents Subject, Role, Group, Endpoint or Participant, respectively

try:
    # Returns a collection of all explicit and implicit permissions granted to an object
    api_response = api_instance.auth_get_permissions(object_uuid, object_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PermissionApi->auth_get_permissions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **object_uuid** | [**str**](.md)| The UUID of either an Endpoint, a Participant, a Group , a Role or a Subject. | 
 **object_type** | **str**| The object type of the object_uuid param.  This code can be s, r, g, e or p, which represents Subject, Role, Group, Endpoint or Participant, respectively | 

### Return type

[**list[Permission]**](Permission.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_grant_permission**
> Permission auth_grant_permission(body=body)

Creates a permission by granting a privilege on a Subject to an object

The privilege may be either 'SUBSCRIBE', 'PUBLISH', 'MANAGE', or 'DISCOVER'  The target of the privilege grant (i.e., the object) can be either a role, a group, an endpoint or a participant.    The invoker must have either the ParticipantAdmin role or the SubjectAdmin role.  A UUDEX Admin may invoke this call without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.PermissionApi()
body = uudex_client.Permission() # Permission |  (optional)

try:
    # Creates a permission by granting a privilege on a Subject to an object
    api_response = api_instance.auth_grant_permission(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PermissionApi->auth_grant_permission: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Permission**](Permission.md)|  | [optional] 

### Return type

[**Permission**](Permission.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_revoke_permission**
> auth_revoke_permission(privilege, subject_uuid, object_uuid, object_type, except_modifier_override)

Remove a permission by revoking a privilege on a Subject from an object

The invoker must have the ParticipantAdmin role or the SubjectAdmin role.  A UUDEX Admin may invoke this call without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.PermissionApi()
privilege = 'privilege_example' # str | The privilege to revoke
subject_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | The Subject to revoke the privilege from
object_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | The target object that the privilege will be revoked from
object_type = 'object_type_example' # str | The object type of the object_uuid param.  This code can be r, g, e or p, which represents Role, Group, Endpoint or Participant, respectively
except_modifier_override = 'except_modifier_override_example' # str | Specifies if the allow_except modifier applies to this permission.  Essentially inverts the permission rule and allows everyone (ie, public group) the applicable privilege EXCEPT the target of this grant.  See the UUDEX security design documents for details.

try:
    # Remove a permission by revoking a privilege on a Subject from an object
    api_instance.auth_revoke_permission(privilege, subject_uuid, object_uuid, object_type, except_modifier_override)
except ApiException as e:
    print("Exception when calling PermissionApi->auth_revoke_permission: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **privilege** | **str**| The privilege to revoke | 
 **subject_uuid** | [**str**](.md)| The Subject to revoke the privilege from | 
 **object_uuid** | [**str**](.md)| The target object that the privilege will be revoked from | 
 **object_type** | **str**| The object type of the object_uuid param.  This code can be r, g, e or p, which represents Role, Group, Endpoint or Participant, respectively | 
 **except_modifier_override** | **str**| Specifies if the allow_except modifier applies to this permission.  Essentially inverts the permission rule and allows everyone (ie, public group) the applicable privilege EXCEPT the target of this grant.  See the UUDEX security design documents for details. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

