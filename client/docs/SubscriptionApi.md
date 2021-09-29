# uudex_client.SubscriptionApi

All URIs are relative to *https://localhost/v1/uudex*

Method | HTTP request | Description
------------- | ------------- | -------------
[**attach_subscription_subject**](SubscriptionApi.md#attach_subscription_subject) | **POST** /subscriptions/{subscription_uuid}/subjects | Attach a single Subject to the given Subscription
[**consume_subscription**](SubscriptionApi.md#consume_subscription) | **GET** /subscriptions/{subscription_uuid}/consume | Consumes the subscription and returns one or more pending messages from message broker
[**create_subscription**](SubscriptionApi.md#create_subscription) | **POST** /subscriptions | Create a single Subscription
[**delete_subscription**](SubscriptionApi.md#delete_subscription) | **DELETE** /subscriptions/{subscription_uuid} | Delelete a Subscription
[**detach_subscription_subject**](SubscriptionApi.md#detach_subscription_subject) | **DELETE** /subscriptions/{subscription_uuid}/subjects/{subscription_subject_id} | Detach a Subject from the given Subscription
[**get_subscription**](SubscriptionApi.md#get_subscription) | **GET** /subscriptions/{subscription_uuid} | Gets a single Subscription
[**get_subscription_subjects**](SubscriptionApi.md#get_subscription_subjects) | **GET** /subscriptions/{subscription_uuid}/subjects | Returns a collection of all Subjects attached to the given Subscription
[**get_subscriptions**](SubscriptionApi.md#get_subscriptions) | **GET** /subscriptions | Returns a collection of the invoker&#x27;s Subscriptions
[**update_subscription**](SubscriptionApi.md#update_subscription) | **PATCH** /subscriptions/{subscription_uuid} | Update a single Subscription

# **attach_subscription_subject**
> SubscriptionSubject attach_subscription_subject(subscription_uuid, body=body)

Attach a single Subject to the given Subscription

The invoker must own the Subscription.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubscriptionApi()
subscription_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
body = uudex_client.SubscriptionSubject() # SubscriptionSubject |  (optional)

try:
    # Attach a single Subject to the given Subscription
    api_response = api_instance.attach_subscription_subject(subscription_uuid, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubscriptionApi->attach_subscription_subject: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subscription_uuid** | [**str**](.md)|  | 
 **body** | [**SubscriptionSubject**](SubscriptionSubject.md)|  | [optional] 

### Return type

[**SubscriptionSubject**](SubscriptionSubject.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **consume_subscription**
> list[MessageConsumeResp] consume_subscription(subscription_uuid)

Consumes the subscription and returns one or more pending messages from message broker

Invoker must have the SUBSCRIBE privilege on the the Subjects in the Subscription OR own the Subjects in the subscription. 

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubscriptionApi()
subscription_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Consumes the subscription and returns one or more pending messages from message broker
    api_response = api_instance.consume_subscription(subscription_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubscriptionApi->consume_subscription: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subscription_uuid** | [**str**](.md)|  | 

### Return type

[**list[MessageConsumeResp]**](MessageConsumeResp.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_subscription**
> Subscription create_subscription(body=body)

Create a single Subscription

Create a single Subscription for the invoker.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubscriptionApi()
body = uudex_client.Subscription() # Subscription |  (optional)

try:
    # Create a single Subscription
    api_response = api_instance.create_subscription(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubscriptionApi->create_subscription: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Subscription**](Subscription.md)|  | [optional] 

### Return type

[**Subscription**](Subscription.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_subscription**
> delete_subscription(subscription_uuid)

Delelete a Subscription

The invoker must own the Subscription.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubscriptionApi()
subscription_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Delelete a Subscription
    api_instance.delete_subscription(subscription_uuid)
except ApiException as e:
    print("Exception when calling SubscriptionApi->delete_subscription: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subscription_uuid** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **detach_subscription_subject**
> detach_subscription_subject(subscription_uuid, subscription_subject_id)

Detach a Subject from the given Subscription

The invoker must own the Subscription.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubscriptionApi()
subscription_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
subscription_subject_id = 'subscription_subject_id_example' # str | 

try:
    # Detach a Subject from the given Subscription
    api_instance.detach_subscription_subject(subscription_uuid, subscription_subject_id)
except ApiException as e:
    print("Exception when calling SubscriptionApi->detach_subscription_subject: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subscription_uuid** | [**str**](.md)|  | 
 **subscription_subject_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_subscription**
> Subscription get_subscription(subscription_uuid)

Gets a single Subscription

The invoker must own the Subscription.  A UUDEX Admin may get any Subscription.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubscriptionApi()
subscription_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Gets a single Subscription
    api_response = api_instance.get_subscription(subscription_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubscriptionApi->get_subscription: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subscription_uuid** | [**str**](.md)|  | 

### Return type

[**Subscription**](Subscription.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_subscription_subjects**
> list[SubscriptionSubject] get_subscription_subjects(subscription_uuid)

Returns a collection of all Subjects attached to the given Subscription

The invoker must own the Subscription.  A UUDEX Admin may get any Subscription's Subjects.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubscriptionApi()
subscription_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # Returns a collection of all Subjects attached to the given Subscription
    api_response = api_instance.get_subscription_subjects(subscription_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubscriptionApi->get_subscription_subjects: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subscription_uuid** | [**str**](.md)|  | 

### Return type

[**list[SubscriptionSubject]**](SubscriptionSubject.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_subscriptions**
> list[SubscriptionEnriched] get_subscriptions()

Returns a collection of the invoker's Subscriptions

The invoker must own the Subscription.  A UUDEX Admin will get a collection of all Subscriptions in the system.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubscriptionApi()

try:
    # Returns a collection of the invoker's Subscriptions
    api_response = api_instance.get_subscriptions()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubscriptionApi->get_subscriptions: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[SubscriptionEnriched]**](SubscriptionEnriched.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_subscription**
> Subscription update_subscription(subscription_uuid, body=body)

Update a single Subscription

The invoker must own the Subscription.

### Example
```python
from __future__ import print_function
import time
import uudex_client
from uudex_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uudex_client.SubscriptionApi()
subscription_uuid = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
body = uudex_client.Subscription() # Subscription |  (optional)

try:
    # Update a single Subscription
    api_response = api_instance.update_subscription(subscription_uuid, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubscriptionApi->update_subscription: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subscription_uuid** | [**str**](.md)|  | 
 **body** | [**Subscription**](Subscription.md)|  | [optional] 

### Return type

[**Subscription**](Subscription.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

