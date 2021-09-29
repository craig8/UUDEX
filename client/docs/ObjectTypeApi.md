# uudex_client.ObjectTypeApi

All URIs are relative to *https://localhost/v1/uudex*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_object_type**](ObjectTypeApi.md#get_object_type) | **GET** /auth/object_type/{object_uuid} | Get object type based on a generic object UUID

# **get_object_type**
> GenericAuthObject get_object_type(object_uuid)

Get object type based on a generic object UUID

Helper function to determine what object type a generic UUID represents.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.ObjectTypeApi()
object_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | Can be the UUID of a subject, group, role, endpoint or participant.

try:
    # Get object type based on a generic object UUID
    api_response = api_instance.get_object_type(object_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ObjectTypeApi->get_object_type: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **object_uuid** | [**str**](.md)| Can be the UUID of a subject, group, role, endpoint or participant. | 

### Return type

[**GenericAuthObject**](GenericAuthObject.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

