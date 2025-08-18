from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.subject_queue_info import SubjectQueueInfo
from ...models.http_validation_error import HTTPValidationError
from typing import Dict
from typing import cast



def _get_kwargs(
    subject_uuid: str,

) -> Dict[str, Any]:
    

    

    

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/subject/{subject_uuid}/queue-info".format(subject_uuid=subject_uuid,),
    }


    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[HTTPValidationError, SubjectQueueInfo]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SubjectQueueInfo.from_dict(response.json())



        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())



        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[HTTPValidationError, SubjectQueueInfo]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    subject_uuid: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[Union[HTTPValidationError, SubjectQueueInfo]]:
    """ Get Subject Queue Info

     Get detailed queue information for a subject.

    Args:
        subject_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SubjectQueueInfo]]
     """


    kwargs = _get_kwargs(
        subject_uuid=subject_uuid,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    subject_uuid: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[Union[HTTPValidationError, SubjectQueueInfo]]:
    """ Get Subject Queue Info

     Get detailed queue information for a subject.

    Args:
        subject_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SubjectQueueInfo]
     """


    return sync_detailed(
        subject_uuid=subject_uuid,
client=client,

    ).parsed

async def asyncio_detailed(
    subject_uuid: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[Union[HTTPValidationError, SubjectQueueInfo]]:
    """ Get Subject Queue Info

     Get detailed queue information for a subject.

    Args:
        subject_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SubjectQueueInfo]]
     """


    kwargs = _get_kwargs(
        subject_uuid=subject_uuid,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    subject_uuid: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[Union[HTTPValidationError, SubjectQueueInfo]]:
    """ Get Subject Queue Info

     Get detailed queue information for a subject.

    Args:
        subject_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SubjectQueueInfo]
     """


    return (await asyncio_detailed(
        subject_uuid=subject_uuid,
client=client,

    )).parsed
