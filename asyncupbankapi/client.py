from __future__ import annotations
from datetime import datetime
from typing import Dict, Optional, Union
from uuid import UUID
from yarl import URL
from asyncupbankapi.httpSession import HttpSession
from asyncupbankapi.const import BASE_URL, PAGE_SIZE
from asyncupbankapi.models.accounts import Account, Accounts
from asyncupbankapi.models.categories import Category, Categories
from asyncupbankapi.models.tags import Tags
from asyncupbankapi.models.transactions import Transaction, Transactions
from asyncupbankapi.models.utility import Ping
from asyncupbankapi.models.webhooks import Webhook, WebhookEvent, WebhookLogs, Webhooks


class Client:
    def __init__(self, token: Optional[str] = None) -> None:
        """UP Bank API Client.

        :param token: UP Bank Token if not provided fetches "UP_TOKEN" from environment variables
        """
        self._session = HttpSession(token)
        self.webhook = WebhookAdapter(self._session)

    async def close(self) -> None:
        await self._session.close()

    async def ping(self) -> Ping:
        """Returns the users unique id and emoji and will raise an exception if the token is not valid."""
        return Ping.parse_obj(await self._session.get(f"{BASE_URL}/util/ping"))

    async def accounts(
        self, limit: Optional[int] = None, page_size: int = None,
    ) -> Accounts:
        """Returns a list of the users accounts.

        :param limit: maximum number of records to return (set to None for all transactions)
        :param page_size: number of records to fetch in each request (max 100)
        """
        params = {}

        if limit and page_size and limit < page_size:
            page_size = limit

        if page_size:
            params.update({PAGE_SIZE: str(page_size)})

        return Accounts(
            data=await self._session.get(f"{BASE_URL}/accounts", params=params),
            session=self._session,
            limit=limit)

    async def account(self, account_id: UUID) -> Account:
        """Returns a single account by its unique account id."""
        return Account(
            data=await self._session.get(f"{BASE_URL}/accounts/{account_id}"),
            session=self._session)

    async def transactions(
        self,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
        status: Optional[str] = None,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        category: Optional[str] = None,
        tag: Optional[str] = None
    ) -> Transactions:
        """Returns transactions for a specific account or all accounts.

        :param limit maximum number of records to return (set to None for all transactions)
        :param page_size number of records to fetch in each request (max 100)
        :param status:
        :param since:
        :param until:
        :param category:
        :param tag:
        :param account_id: optionally supply a unique id of the account to fetch transactions from
        """
        if limit and page_size and limit < page_size:
            page_size = limit

        params = {}

        if page_size:
            params.update({PAGE_SIZE: str(page_size)})
        if status:
            params.update({"filter[status]": status})
        if since:
            params.update({"filter[since]": since.astimezone().isoformat()})
        if until:
            params.update({"filter[until]": until.astimezone().isoformat()})
        if category:
            params.update({"filter[category]": category})
        if tag:
            params.update({"filter[tag]": tag})

        return Transactions(
            data=await self._session.get(f"{BASE_URL}/transactions", params=params),
            session=self._session,
            limit=limit)

    async def transaction(self, transaction_id: UUID) -> Transaction:
        """Returns a single transaction by its unique id."""
        return Transaction(
            data=await self._session.get(f"{BASE_URL}/transactions/{transaction_id}"),
            session=self._session)

    async def categories(self, parent: Optional[str] = None) -> Categories:
        """Returns a list of cateogries."""
        if parent:
            return Categories.parse_obj(await self._session.get(f"{BASE_URL}/categories", params={"filter[parent": parent}))
        return Categories.parse_obj(await self._session.get(f"{BASE_URL}/categories"))

    async def category(self, category_id: str) -> Category:
        """Returns a single Category by its unique id."""
        return Category.parse_obj(await self._session.get(f"{BASE_URL}/categories/{category_id}"))

    async def tags(self) -> Tags:
        """Retrieve a list of all tags currently in use. The returned list is paginated and can be scrolled by following the next and prev links where present. Results are ordered lexicographically. The transactions relationship for each tag exposes a link to get the transactions with the given tag."""
        return Tags.parse_obj(await self._session.get(f"{BASE_URL}/tags"))

    async def webhooks(self, limit: Optional[int] = None, page_size: Optional[int] = None) -> Webhooks:
        """Returns a list of the users webhooks.

        :param limit: maximum number of records to return (set to None for all records)
        :param page_size: number of records to fetch in each request (max 100)
        """
        if limit and page_size and limit < page_size:
            page_size = limit

        params = {}

        if page_size:
            params.update({PAGE_SIZE: str(page_size)})

        return Webhooks(
            data=await self._session.get(f"{BASE_URL}/webhooks", params=params),
            session=self._session,
            limit=limit)


class WebhookAdapter:
    def __init__(self, session: HttpSession):
        self._session = session

    async def __call__(self, webhook_id: UUID) -> Webhook:
        """Returns a single webhook by its unique id.

        :param webhook_id: The unique identfier of the webhook."""
        return await self.get(webhook_id)

    async def get(self, webhook_id: UUID) -> Webhook:
        """Returns a single webhook by its unique id.

        :param webhook_id: The unique identfier of the webhook."""
        return Webhook(
            data=await self._session.get(f"{BASE_URL}/webhooks/{webhook_id}"),
            session=self._session)

    async def create(self, url: URL, description: Optional[str] = None) -> Webhook:
        """Create a new webhook with the given URL.

        :param url: The URL that this webhook should post events to. This must be a valid HTTP or HTTPS URL that does not exceed 300 characters in length.
        :param description: An optional description for this webhook, up to 64 characters in length.
        """

        # Build the input requests payload.
        attributes: Dict[str, Union[str, URL]]
        attributes = {}
        attributes.update({"url": url})

        if description:
            attributes.update({"description": description})

        data = {}

        data.update({"attributes": attributes})

        payload = {}
        payload.update({"data": data})

        return Webhook(data=await self._session.post(f"{BASE_URL}/webhooks", payload=payload), session=self._session)

    async def logs(self, webhook_id: UUID, limit: Optional[int] = None, page_size: Optional[int] = None) -> WebhookLogs:
        """Returns a list of webhook logs.

        :param webhook_id: The unique identfier of the webhook.
        :param limit: maximum number of records to return (set to None for all records)
        :param page_size: number of records to fetch in each request (max 100)"""

        if limit and page_size and limit < page_size:
            page_size = limit

        params = {}

        if page_size:
            params.update({PAGE_SIZE: str(page_size)})

        return WebhookLogs(data=await self._session.get(f"{BASE_URL}/webhooks/{webhook_id}/logs"), session=self._session, limit=limit)

    async def ping(self, webhook_id: str) -> WebhookEvent:
        """Pings a webhook by its unique id."""
        return WebhookEvent.parse_obj(await self._session.post(f"{BASE_URL}/webhooks/{webhook_id}/ping"))

    async def delete(self, webhook_id: UUID) -> None:
        """Delete a single webhook by its unique id."""
        await self._session.delete(f"{BASE_URL}webhooks/{webhook_id}")
