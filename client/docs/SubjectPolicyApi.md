# uudex_client.SubjectPolicyApi

All URIs are relative to *https://localhost/v1/uudex*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_acl_constraint**](SubjectPolicyApi.md#create_acl_constraint) | **POST** /subject-policies/{subject_policy_uuid}/acl-constraints | Create a ACL Constraint for a given Subject Policy
[**create_subject_policy**](SubjectPolicyApi.md#create_subject_policy) | **POST** /subject-policies | Creates a Subject Policy and attaches it to given Participant
[**delete_acl_constraint**](SubjectPolicyApi.md#delete_acl_constraint) | **DELETE** /subject-policies/{subject_policy_uuid}/acl-constraints/{acl_constraint_id} | Delete a sincle ACL Constraint for a given Subject Policy
[**delete_subject_policy**](SubjectPolicyApi.md#delete_subject_policy) | **DELETE** /subject-policies/{subject_policy_uuid} | Delete a single Subject Policy
[**get_acl_constraint**](SubjectPolicyApi.md#get_acl_constraint) | **GET** /subject-policies/{subject_policy_uuid}/acl-constraints/{acl_constraint_id} | Return a single ACL Constraint for a given Subject Policy
[**get_all_acl_constraints**](SubjectPolicyApi.md#get_all_acl_constraints) | **GET** /subject-policies/{subject_policy_uuid}/acl-constraints | Return all ACL Constraints for a given Subject Policy
[**get_subject_policies**](SubjectPolicyApi.md#get_subject_policies) | **GET** /subject-policies | Returns a collection of Subject Policies
[**get_subject_policy**](SubjectPolicyApi.md#get_subject_policy) | **GET** /subject-policies/{subject_policy_uuid} | Return a single Subject Policy
[**update_subject_policy**](SubjectPolicyApi.md#update_subject_policy) | **PATCH** /subject-policies/{subject_policy_uuid} | Update a single Subject Policy

# **create_acl_constraint**
> SubjectPolicyAclConstraint create_acl_constraint(subject_policy_uuid, body=body)

Create a ACL Constraint for a given Subject Policy

The invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubjectPolicyApi()
subject_policy_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
body = uudex_client.SubjectPolicyAclConstraint() # SubjectPolicyAclConstraint |  (optional)

try:
    # Create a ACL Constraint for a given Subject Policy
    api_response = api_instance.create_acl_constraint(subject_policy_uuid, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubjectPolicyApi->create_acl_constraint: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subject_policy_uuid** | [**str**](.md)|  | 
 **body** | [**SubjectPolicyAclConstraint**](SubjectPolicyAclConstraint.md)|  | [optional] 

### Return type

[**SubjectPolicyAclConstraint**](SubjectPolicyAclConstraint.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_subject_policy**
> SubjectPolicy create_subject_policy(body=body)

Creates a Subject Policy and attaches it to given Participant

The invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubjectPolicyApi()
body = uudex_client.SubjectPolicy() # SubjectPolicy |  (optional)

try:
    # Creates a Subject Policy and attaches it to given Participant
    api_response = api_instance.create_subject_policy(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubjectPolicyApi->create_subject_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SubjectPolicy**](SubjectPolicy.md)|  | [optional] 

### Return type

[**SubjectPolicy**](SubjectPolicy.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_acl_constraint**
> delete_acl_constraint(subject_policy_uuid, acl_constraint_id)

Delete a sincle ACL Constraint for a given Subject Policy

The invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubjectPolicyApi()
subject_policy_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
acl_constraint_id = 56 # int | 

try:
    # Delete a sincle ACL Constraint for a given Subject Policy
    api_instance.delete_acl_constraint(subject_policy_uuid, acl_constraint_id)
except ApiException as e:
    print("Exception when calling SubjectPolicyApi->delete_acl_constraint: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subject_policy_uuid** | [**str**](.md)|  | 
 **acl_constraint_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_subject_policy**
> delete_subject_policy(subject_policy_uuid)

Delete a single Subject Policy

The invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubjectPolicyApi()
subject_policy_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Delete a single Subject Policy
    api_instance.delete_subject_policy(subject_policy_uuid)
except ApiException as e:
    print("Exception when calling SubjectPolicyApi->delete_subject_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subject_policy_uuid** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_acl_constraint**
> SubjectPolicyAclConstraint get_acl_constraint(subject_policy_uuid, acl_constraint_id)

Return a single ACL Constraint for a given Subject Policy

Returns the ACL Constraint for the given Subject Policy that the invoker's Participant is attached to.  A UUDEX Admin may get any given Subject Policy constraint.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubjectPolicyApi()
subject_policy_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
acl_constraint_id = 56 # int | 

try:
    # Return a single ACL Constraint for a given Subject Policy
    api_response = api_instance.get_acl_constraint(subject_policy_uuid, acl_constraint_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubjectPolicyApi->get_acl_constraint: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subject_policy_uuid** | [**str**](.md)|  | 
 **acl_constraint_id** | **int**|  | 

### Return type

[**SubjectPolicyAclConstraint**](SubjectPolicyAclConstraint.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_acl_constraints**
> list[SubjectPolicyAclConstraint] get_all_acl_constraints(subject_policy_uuid)

Return all ACL Constraints for a given Subject Policy

Returns a collection of ACL Constraints for the given Subject Policy the invoker's Participant is attached to.  A UUDEX Admin may get a collection of ACL Constraints for any given Subject Policy.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubjectPolicyApi()
subject_policy_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Return all ACL Constraints for a given Subject Policy
    api_response = api_instance.get_all_acl_constraints(subject_policy_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubjectPolicyApi->get_all_acl_constraints: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subject_policy_uuid** | [**str**](.md)|  | 

### Return type

[**list[SubjectPolicyAclConstraint]**](SubjectPolicyAclConstraint.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_subject_policies**
> list[SubjectPolicyEnriched] get_subject_policies()

Returns a collection of Subject Policies

Returns a collection of all Subject Policies the invoker's Participant is attached to.  A UUDEX Admin will get all Subject Policies in the system.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubjectPolicyApi()

try:
    # Returns a collection of Subject Policies
    api_response = api_instance.get_subject_policies()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubjectPolicyApi->get_subject_policies: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[SubjectPolicyEnriched]**](SubjectPolicyEnriched.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_subject_policy**
> SubjectPolicyEnriched get_subject_policy(subject_policy_uuid)

Return a single Subject Policy

Returns a single Subject Policy that invoker's Participant is attached to.  A UUDEX Admin may get any subject Policy.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubjectPolicyApi()
subject_policy_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Return a single Subject Policy
    api_response = api_instance.get_subject_policy(subject_policy_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubjectPolicyApi->get_subject_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subject_policy_uuid** | [**str**](.md)|  | 

### Return type

[**SubjectPolicyEnriched**](SubjectPolicyEnriched.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_subject_policy**
> SubjectPolicy update_subject_policy(subject_policy_uuid, body=body)

Update a single Subject Policy

The invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubjectPolicyApi()
subject_policy_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
body = uudex_client.SubjectPolicy() # SubjectPolicy |  (optional)

try:
    # Update a single Subject Policy
    api_response = api_instance.update_subject_policy(subject_policy_uuid, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubjectPolicyApi->update_subject_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subject_policy_uuid** | [**str**](.md)|  | 
 **body** | [**SubjectPolicy**](SubjectPolicy.md)|  | [optional] 

### Return type

[**SubjectPolicy**](SubjectPolicy.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

