# uudex_client.DatasetDefinitionApi

All URIs are relative to *https://localhost/v1/uudex*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_dataset_definition**](DatasetDefinitionApi.md#create_dataset_definition) | **POST** /dataset-definitions | Create a single Dataset Definition
[**delete_dataset_definition**](DatasetDefinitionApi.md#delete_dataset_definition) | **DELETE** /dataset-definitions/{dataset_definition_uuid} | Delete a single Dataset
[**get_all_dataset_definitions**](DatasetDefinitionApi.md#get_all_dataset_definitions) | **GET** /dataset-definitions | Returns a collection of all Datasets Definitions in the system
[**get_dataset_definition**](DatasetDefinitionApi.md#get_dataset_definition) | **GET** /dataset-definitions/{dataset_definition_uuid} | Returns a single Dataset Definition
[**update_dataset_definition**](DatasetDefinitionApi.md#update_dataset_definition) | **PATCH** /dataset-definitions/{dataset_definition_uuid} | Update a single Dataset Definition

# **create_dataset_definition**
> DatasetDefinition create_dataset_definition(body=body)

Create a single Dataset Definition

The invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.DatasetDefinitionApi()
body = uudex_client.DatasetDefinition() # DatasetDefinition |  (optional)

try:
    # Create a single Dataset Definition
    api_response = api_instance.create_dataset_definition(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetDefinitionApi->create_dataset_definition: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DatasetDefinition**](DatasetDefinition.md)|  | [optional] 

### Return type

[**DatasetDefinition**](DatasetDefinition.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_dataset_definition**
> delete_dataset_definition(dataset_definition_uuid)

Delete a single Dataset

The invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.DatasetDefinitionApi()
dataset_definition_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Delete a single Dataset
    api_instance.delete_dataset_definition(dataset_definition_uuid)
except ApiException as e:
    print("Exception when calling DatasetDefinitionApi->delete_dataset_definition: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_definition_uuid** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_dataset_definitions**
> list[DatasetDefinition] get_all_dataset_definitions()

Returns a collection of all Datasets Definitions in the system

This endpoint open to to all users on the system 

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.DatasetDefinitionApi()

try:
    # Returns a collection of all Datasets Definitions in the system
    api_response = api_instance.get_all_dataset_definitions()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetDefinitionApi->get_all_dataset_definitions: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[DatasetDefinition]**](DatasetDefinition.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_dataset_definition**
> DatasetDefinition get_dataset_definition(dataset_definition_uuid)

Returns a single Dataset Definition

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.DatasetDefinitionApi()
dataset_definition_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Returns a single Dataset Definition
    api_response = api_instance.get_dataset_definition(dataset_definition_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetDefinitionApi->get_dataset_definition: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_definition_uuid** | [**str**](.md)|  | 

### Return type

[**DatasetDefinition**](DatasetDefinition.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_dataset_definition**
> DatasetDefinition update_dataset_definition(dataset_definition_uuid, body=body)

Update a single Dataset Definition

The invoker must be a UUDEX Admin otherwise the call will fail.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.DatasetDefinitionApi()
dataset_definition_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
body = uudex_client.DatasetDefinition() # DatasetDefinition |  (optional)

try:
    # Update a single Dataset Definition
    api_response = api_instance.update_dataset_definition(dataset_definition_uuid, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetDefinitionApi->update_dataset_definition: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_definition_uuid** | [**str**](.md)|  | 
 **body** | [**DatasetDefinition**](DatasetDefinition.md)|  | [optional] 

### Return type

[**DatasetDefinition**](DatasetDefinition.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

