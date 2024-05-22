from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.subscription import Subscription
from ...types import Response


def _get_kwargs(subscription_uuid: str, ) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/subscription/{subscription_uuid}",
    }

    return _kwargs


def _parse_response(
        *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, Union["Subscription", None]]]:
    if response.status_code == HTTPStatus.OK:

        def _parse_response_200(data: object) -> Union["Subscription", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = Subscription.from_dict(data)

                return response_200_type_0
            except:    # noqa: E722
                pass
            return cast(Union["Subscription", None], data)

        response_200 = _parse_response_200(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
        *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, Union["Subscription", None]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    subscription_uuid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, Union["Subscription", None]]]:
    """Get Subscription

    Args:
        subscription_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['Subscription', None]]]
    """

    kwargs = _get_kwargs(subscription_uuid=subscription_uuid, )

    response = client.get_httpx_client().request(**kwargs, )

    return _build_response(client=client, response=response)


def sync(
    subscription_uuid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, Union["Subscription", None]]]:
    """Get Subscription

    Args:
        subscription_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['Subscription', None]]
    """

    return sync_detailed(
        subscription_uuid=subscription_uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    subscription_uuid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, Union["Subscription", None]]]:
    """Get Subscription

    Args:
        subscription_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['Subscription', None]]]
    """

    kwargs = _get_kwargs(subscription_uuid=subscription_uuid, )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    subscription_uuid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, Union["Subscription", None]]]:
    """Get Subscription

    Args:
        subscription_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['Subscription', None]]
    """

    return (await asyncio_detailed(
        subscription_uuid=subscription_uuid,
        client=client,
    )).parsed
