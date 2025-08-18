from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.end_point import EndPoint
from typing import Dict
from typing import cast



def _get_kwargs(
    endpoint_id: int,

) -> Dict[str, Any]:
    

    

    

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/endpoint/{endpoint_id}".format(endpoint_id=endpoint_id,),
    }


    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[EndPoint, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = EndPoint.from_dict(response.json())



        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())



        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[EndPoint, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    endpoint_id: int,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[Union[EndPoint, HTTPValidationError]]:
    """ Get Endpoint By Id

     Get a specific endpoint by ID with authorization checks.

    Args:
        endpoint_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EndPoint, HTTPValidationError]]
     """


    kwargs = _get_kwargs(
        endpoint_id=endpoint_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    endpoint_id: int,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[Union[EndPoint, HTTPValidationError]]:
    """ Get Endpoint By Id

     Get a specific endpoint by ID with authorization checks.

    Args:
        endpoint_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EndPoint, HTTPValidationError]
     """


    return sync_detailed(
        endpoint_id=endpoint_id,
client=client,

    ).parsed

async def asyncio_detailed(
    endpoint_id: int,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[Union[EndPoint, HTTPValidationError]]:
    """ Get Endpoint By Id

     Get a specific endpoint by ID with authorization checks.

    Args:
        endpoint_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EndPoint, HTTPValidationError]]
     """


    kwargs = _get_kwargs(
        endpoint_id=endpoint_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    endpoint_id: int,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[Union[EndPoint, HTTPValidationError]]:
    """ Get Endpoint By Id

     Get a specific endpoint by ID with authorization checks.

    Args:
        endpoint_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EndPoint, HTTPValidationError]
     """


    return (await asyncio_detailed(
        endpoint_id=endpoint_id,
client=client,

    )).parsed
