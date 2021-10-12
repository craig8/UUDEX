# uudex_client.SubjectApi

All URIs are relative to *https://localhost/v1/uudex*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_subject**](SubjectApi.md#create_subject) | **POST** /subjects | Creates a Subject if the calling participant is authorized
[**delete_subject**](SubjectApi.md#delete_subject) | **DELETE** /subjects/{subject_uuid} | Delete a single Subject the invoker is authorized to use
[**discover_subjects**](SubjectApi.md#discover_subjects) | **GET** /subjects/discover | Returns a collection of Subjects the calling endpoint is authorized to view.  Optionally filter by subject name.
[**get_subject**](SubjectApi.md#get_subject) | **GET** /subjects/{subject_uuid} | Get a single Subject the invoker is authorized to use
[**get_subjects**](SubjectApi.md#get_subjects) | **GET** /subjects | Return a collection of Subjects
[**publish_message**](SubjectApi.md#publish_message) | **POST** /subjects/{subject_uuid}/publish | Publishes one or more messages
[**update_subject**](SubjectApi.md#update_subject) | **PATCH** /subjects/{subject_uuid} | Update a single Subject the invoker is authorized to use

# **create_subject**
> Subject create_subject(body=body)

Creates a Subject if the calling participant is authorized

The invoker must have either the ParticipantAdmin role or the SubjectAdmin role.  The ability of a non-admin invoker to create a Subject is also determined by any defined Subject Policy rules.  See the UUDEX documentation for further discussion.  A UUDEX Admin may create a Subject without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubjectApi()
body = uudex_client.Subject() # Subject |  (optional)

try:
    # Creates a Subject if the calling participant is authorized
    api_response = api_instance.create_subject(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubjectApi->create_subject: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Subject**](Subject.md)|  | [optional] 

### Return type

[**Subject**](Subject.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_subject**
> delete_subject(subject_uuid)

Delete a single Subject the invoker is authorized to use

The invoker must have either the ParticipantAdmin role or the SubjectAdmin role AND the Subject must be owned by the invoker's Participant.  A UUDEX Admin may delete any Subject without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubjectApi()
subject_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Delete a single Subject the invoker is authorized to use
    api_instance.delete_subject(subject_uuid)
except ApiException as e:
    print("Exception when calling SubjectApi->delete_subject: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subject_uuid** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **discover_subjects**
> list[SubjectDiscovered] discover_subjects()

Returns a collection of Subjects the calling endpoint is authorized to view.  Optionally filter by subject name.

Returns a collection of Subjects the calling endpoint is authorized to view.  Authorized to view is defined as the invoker having been granted the DISCOVER privilege to the Subjects. 

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubjectApi()

try:
    # Returns a collection of Subjects the calling endpoint is authorized to view.  Optionally filter by subject name.
    api_response = api_instance.discover_subjects()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubjectApi->discover_subjects: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[SubjectDiscovered]**](SubjectDiscovered.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_subject**
> SubjectEnriched get_subject(subject_uuid)

Get a single Subject the invoker is authorized to use

The Subject must be owned by the invoker's Participant.  Invoker must have the SubjectAdmin role or the ParticipantAdmin role.  A UUDEX Admin may get any Subject in the system.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubjectApi()
subject_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Get a single Subject the invoker is authorized to use
    api_response = api_instance.get_subject(subject_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubjectApi->get_subject: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subject_uuid** | [**str**](.md)|  | 

### Return type

[**SubjectEnriched**](SubjectEnriched.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_subjects**
> list[SubjectEnriched] get_subjects()

Return a collection of Subjects

Gets all Subjects owned by the invoker's Participant.  Invoker must have the SubjectAdmin role or the ParticipantAdmin role.  A UUDEX Admin may get all Subjects in the system.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubjectApi()

try:
    # Return a collection of Subjects
    api_response = api_instance.get_subjects()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubjectApi->get_subjects: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[SubjectEnriched]**](SubjectEnriched.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **publish_message**
> MessagePublishResp publish_message(subject_uuid, body=body)

Publishes one or more messages

Invoker must have the SUBSCRIBE privilege on the the Subject or own the Subject. 

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubjectApi()
subject_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
body = [uudex_client.MessagePublish()] # list[MessagePublish] |  (optional)

try:
    # Publishes one or more messages
    api_response = api_instance.publish_message(subject_uuid, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubjectApi->publish_message: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subject_uuid** | [**str**](.md)|  | 
 **body** | [**list[MessagePublish]**](MessagePublish.md)|  | [optional] 

### Return type

[**MessagePublishResp**](MessagePublishResp.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_subject**
> Subject update_subject(subject_uuid, body=body)

Update a single Subject the invoker is authorized to use

The invoker must have either the ParticipantAdmin role or the SubjectAdmin role AND the Subject must be owned by the invoker's Participant.  A UUDEX Admin may update any Subject without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubjectApi()
subject_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
body = uudex_client.Subject() # Subject |  (optional)

try:
    # Update a single Subject the invoker is authorized to use
    api_response = api_instance.update_subject(subject_uuid, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubjectApi->update_subject: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subject_uuid** | [**str**](.md)|  | 
 **body** | [**Subject**](Subject.md)|  | [optional] 

### Return type

[**Subject**](Subject.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

