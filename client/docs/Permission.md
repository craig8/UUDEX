# Permission

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**subject_uuid** | **str** | The subject to receive the privilege grant | 
**privilege** | **str** | One of PUBLISH, SUBSCRIBE, or DISCOVER | 
**object_uuid** | **str** | The UUID of the object | 
**object_type** | **str** | The type code of the object represented in the object_uuid field.  This code can be &#x27;s&#x27;, &#x27;r&#x27;, &#x27;g&#x27;, &#x27;e&#x27; or &#x27;p&#x27;, which represents &#x27;Subject&#x27;, &#x27;Role&#x27;, &#x27;Group&#x27;, &#x27;Endpoint&#x27; or &#x27;Participant&#x27;, respectively | 
**except_modifier_override** | **str** | Specifies if the allow_except modifier applies to this permission.  Essentially inverts the permission rule and allows everyone (ie, public group) the applicable privilege EXCEPT the target of this grant.  See the UUDEX security design documents for details. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

