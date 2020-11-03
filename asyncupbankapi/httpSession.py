from json import dumps
from os import getenv
from typing import Optional

import aiohttp
from aiohttp.client_reqrep import ClientResponse
from aiohttp.hdrs import AUTHORIZATION, CONTENT_TYPE
from aiohttp.typedefs import StrOrURL

from asyncupbankapi.exceptions import (NotAuthorizedException, NotFoundException,
                                  RateLimitExceededException, UpBankException)


class HttpSession:

    def __init__(self, token: Optional[str] = None):
        """UP Bank API HTTP Session.

        :param token UP Bank Token if not provided fetches "UP_TOKEN" from environment variables
        """
        self._session = aiohttp.ClientSession(
            headers={AUTHORIZATION: f"Bearer {token if token else getenv('UP_TOKEN')}",
                     CONTENT_TYPE: "application/json"})

    async def close(self):
        await self._session.close()

    async def __handle_response(self, response: ClientResponse) -> dict:
        if response.status == 204:
            await response.wait_for_close()
            return {}

        if response.status >= 400:
            try:
                if response.content_type == "application/json":
                    data = await response.json()
                    error = data["errors"][0]
                else:
                    error = {}
            except ValueError:
                error = {}

            if response.status == 401:
                raise NotAuthorizedException(error)

            if response.status == 404:
                raise NotFoundException(response.url.path)

            if response.status == 429:
                raise RateLimitExceededException(error)

            raise UpBankException(error)

        return await response.json()

    async def get(
        self, endpoint: StrOrURL, params: Optional[dict] = None
    ) -> dict:
        """This method is used to directly interact the up bank api."""
        async with self._session.get(endpoint, params=params) as response:
            return await self.__handle_response(response)

    async def post(
        self, endpoint: StrOrURL, payload: Optional[dict] = None, params: Optional[dict] = None,
    ) -> dict:
        """This method is used to directly interact the up bank api."""
        async with self._session.post(endpoint, params=params, data=dumps(payload)) as response:
            return await self.__handle_response(response)

    async def delete(
        self, endpoint: StrOrURL, payload: Optional[dict] = None, params: Optional[dict] = None
    ) -> dict:
        """This method is used to directly interact the up bank api."""
        async with self._session.delete(endpoint, params=params, data=dumps(payload)) as response:
            return await self.__handle_response(response)
