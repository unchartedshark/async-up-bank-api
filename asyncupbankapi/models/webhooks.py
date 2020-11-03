# Webhook Classes
from typing import List, Optional
from pydantic import BaseModel, root_validator
from asyncupbankapi.const import BASE_URL, PAGE_SIZE, WebhookDeliveryStatus, WebhookEventType
from asyncupbankapi.models.baseModels import Pagination, RelatedUUIDObject, RelatedUUIDObjectWithoutLinks, TypeandUUID, RelatedLinks, Self
from datetime import datetime


class WebhookAttributes(BaseModel):
    url: str
    description: Optional[str] = None
    secretKey: Optional[str] = None
    createdAt: datetime


class WebhookRelationship(BaseModel):
    logs: RelatedLinks


class WebhookEventAttributes(BaseModel):
    eventType: WebhookEventType
    createdAt: datetime


class WebhookEventRelationships(BaseModel):
    webhook: RelatedUUIDObject


class WebhookEvent(TypeandUUID):
    attributes: WebhookEventAttributes
    relationships: WebhookEventRelationships


class WebhookLogRequest(BaseModel):
    body: str


class WebhookLogResponse(BaseModel):
    statusCode: int
    body: str


class WebhookLogAttributes(BaseModel):
    request: WebhookLogRequest
    response: WebhookLogResponse
    deliveryStatus: WebhookDeliveryStatus
    createdAt: datetime


class WebhookLogRelationships(BaseModel):
    webhookEvent: RelatedUUIDObjectWithoutLinks


class WebhookLog(TypeandUUID):
    attributes: WebhookLogAttributes
    relationships: WebhookLogRelationships


class WebhookLogs(Pagination):
    data: List[WebhookLog] = []


class Webhook(TypeandUUID):
    attributes: WebhookAttributes
    relationships: WebhookRelationship
    links: Self

    @ root_validator(pre=True)
    def __extract_data(cls, v: dict):
        if "data" in v:
            return v["data"]
        return v

    def __str__(self) -> str:
        """Return the representation of the webhook."""
        if self.attributes.description:
            return f"<Webhook '{self.id}': {self.attributes.url} ({self.attributes.description})>"
        return f"<Webhook '{self.id}': {self.attributes.url}>"

    async def delete(self) -> None:
        """Delete the webhook"""
        assert self._session
        await self._session.delete(f"{BASE_URL}/webhooks/{self.id}")

    async def logs(self, limit: Optional[int] = None, page_size: Optional[int] = None) -> WebhookLogs:
        """Returns a list of logs assoicated to this webhook.

        :param limit: maximum number of records to return (set to None for all records)
        :param page_size: number of records to fetch in each request (max 100)"""

        if limit and page_size and limit < page_size:
            page_size = limit

        params = {}

        if page_size:
            params.update({PAGE_SIZE: str(page_size)})

        assert self._session
        return WebhookLogs(data=await self._session.get(self.relationships.logs.links.related), session=self._session, limit=limit)

    async def ping(self) -> WebhookEvent:
        """Pings a webhook by its unique id."""
        assert self._session
        return WebhookEvent.parse_obj(await self._session.post(f"{BASE_URL}/webhooks/{self.id}/ping"))


class Webhooks(Pagination):
    data: List[Webhook] = []
