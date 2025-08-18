from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from typing import Dict
from typing import cast
from ...models.http_validation_error import HTTPValidationError
from ...models.dataset_read import DatasetRead



def _get_kwargs(
    dataset_id: int,

) -> Dict[str, Any]:
    

    

    

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/dataset/{dataset_id}".format(dataset_id=dataset_id,),
    }


    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[DatasetRead, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DatasetRead.from_dict(response.json())



        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())



        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[DatasetRead, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dataset_id: int,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[Union[DatasetRead, HTTPValidationError]]:
    """ Get Dataset By Id

     Get a specific dataset by ID.
    Returns metadata only, use download endpoint for payload.
    Only returns datasets owned by the authenticated user's participant.

    Args:
        dataset_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DatasetRead, HTTPValidationError]]
     """


    kwargs = _get_kwargs(
        dataset_id=dataset_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    dataset_id: int,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[Union[DatasetRead, HTTPValidationError]]:
    """ Get Dataset By Id

     Get a specific dataset by ID.
    Returns metadata only, use download endpoint for payload.
    Only returns datasets owned by the authenticated user's participant.

    Args:
        dataset_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DatasetRead, HTTPValidationError]
     """


    return sync_detailed(
        dataset_id=dataset_id,
client=client,

    ).parsed

async def asyncio_detailed(
    dataset_id: int,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[Union[DatasetRead, HTTPValidationError]]:
    """ Get Dataset By Id

     Get a specific dataset by ID.
    Returns metadata only, use download endpoint for payload.
    Only returns datasets owned by the authenticated user's participant.

    Args:
        dataset_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DatasetRead, HTTPValidationError]]
     """


    kwargs = _get_kwargs(
        dataset_id=dataset_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    dataset_id: int,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[Union[DatasetRead, HTTPValidationError]]:
    """ Get Dataset By Id

     Get a specific dataset by ID.
    Returns metadata only, use download endpoint for payload.
    Only returns datasets owned by the authenticated user's participant.

    Args:
        dataset_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DatasetRead, HTTPValidationError]
     """


    return (await asyncio_detailed(
        dataset_id=dataset_id,
client=client,

    )).parsed
