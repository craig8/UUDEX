# uudex_client.DatasetApi

All URIs are relative to *https://localhost/v1/uudex*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_dataset**](DatasetApi.md#create_dataset) | **POST** /datasets | Create a single Dataset in the given Subject and optionally publish a message that contains the Dataset
[**delete_dataset**](DatasetApi.md#delete_dataset) | **DELETE** /datasets/{dataset_uuid} | Delete the Dataset and optionally publish a notification message
[**get_dataset**](DatasetApi.md#get_dataset) | **GET** /datasets/{dataset_uuid} | Returns a single Dataset
[**get_datasets**](DatasetApi.md#get_datasets) | **GET** /datasets | Returns a collection of Datasets, given the passed search parameters
[**update_dataset**](DatasetApi.md#update_dataset) | **PATCH** /datasets/{dataset_uuid} | Update the Dataset and optionally publish a notification message

# **create_dataset**
> DatasetEnriched create_dataset(body=body)

Create a single Dataset in the given Subject and optionally publish a message that contains the Dataset

The invoker must have the PUBLISH privilege to the Subject containing the dataset OR the Subject that will contain the Dataset must be owned by the invoker's Participant.  A UUDEX Admin may create a dataset without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.DatasetApi()
body = uudex_client.Dataset() # Dataset |  (optional)

try:
    # Create a single Dataset in the given Subject and optionally publish a message that contains the Dataset
    api_response = api_instance.create_dataset(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetApi->create_dataset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Dataset**](Dataset.md)|  | [optional] 

### Return type

[**DatasetEnriched**](DatasetEnriched.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_dataset**
> delete_dataset(dataset_uuid, publish_message=publish_message)

Delete the Dataset and optionally publish a notification message

The owner of the Subject containing the Dataset must be the invoker's Participant OR the invoker must have been granted the MANAGE privilege to the Subject containing the Dataset.  A UUDEX Admin may delete any Dataset.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.DatasetApi()
dataset_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
publish_message = true # bool | Whether to also publish a notice message to the parent subject (optional)

try:
    # Delete the Dataset and optionally publish a notification message
    api_instance.delete_dataset(dataset_uuid, publish_message=publish_message)
except ApiException as e:
    print("Exception when calling DatasetApi->delete_dataset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_uuid** | [**str**](.md)|  | 
 **publish_message** | **bool**| Whether to also publish a notice message to the parent subject | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_dataset**
> DatasetEnriched get_dataset(dataset_uuid)

Returns a single Dataset

The invoker must have the SUBSCRIBE privilege to the Subject containing the dataset OR the Subject containing the Dataset must be owned by the invoker's Participant.  A UUDEX Admin may get any dataset.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.DatasetApi()
dataset_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Returns a single Dataset
    api_response = api_instance.get_dataset(dataset_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetApi->get_dataset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_uuid** | [**str**](.md)|  | 

### Return type

[**DatasetEnriched**](DatasetEnriched.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_datasets**
> list[DatasetEnriched] get_datasets(subject_uuid, search_expression=search_expression, participant_uuid=participant_uuid)

Returns a collection of Datasets, given the passed search parameters

The invoker must have the SUBSCRIBE privilege to the Subject containing the fetched Datasets OR the Subjects containing the Datasets must be owned by the invoker's Participant.  A UUDEX Admin may get Datasets in any Subject without restrictions.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.DatasetApi()
subject_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | Subject to search
search_expression = 'search_expression_example' # str | Contains a custom query expression that applies a filter based on key/value properties (optional)
participant_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | Limit search to datasets owned by this Participant (optional)

try:
    # Returns a collection of Datasets, given the passed search parameters
    api_response = api_instance.get_datasets(subject_uuid, search_expression=search_expression, participant_uuid=participant_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetApi->get_datasets: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subject_uuid** | [**str**](.md)| Subject to search | 
 **search_expression** | **str**| Contains a custom query expression that applies a filter based on key/value properties | [optional] 
 **participant_uuid** | [**str**](.md)| Limit search to datasets owned by this Participant | [optional] 

### Return type

[**list[DatasetEnriched]**](DatasetEnriched.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_dataset**
> DatasetEnriched update_dataset(dataset_uuid, body=body, publish_message=publish_message)

Update the Dataset and optionally publish a notification message

The owner of the Subject that contains the Dataset must be the invoker's Participant OR the invoker must have been granted the MANAGE privilege to the Subject containing the Dataset.  A UUDEX Admin may update any Dataset.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.DatasetApi()
dataset_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
body = uudex_client.Dataset() # Dataset |  (optional)
publish_message = true # bool | Whether to also publish a notice message to the parent subject (optional)

try:
    # Update the Dataset and optionally publish a notification message
    api_response = api_instance.update_dataset(dataset_uuid, body=body, publish_message=publish_message)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetApi->update_dataset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_uuid** | [**str**](.md)|  | 
 **body** | [**Dataset**](Dataset.md)|  | [optional] 
 **publish_message** | **bool**| Whether to also publish a notice message to the parent subject | [optional] 

### Return type

[**DatasetEnriched**](DatasetEnriched.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

