# Transaction Classes
from typing import Optional
from asyncupbankapi.const import TransactionStatus
from asyncupbankapi.models.baseModels import Money, Pagination, RelatedObject, RelatedUUIDObject, Self, TagsRelationship, TypeandUUID
from pydantic import BaseModel, root_validator
from typing import Optional, List
from datetime import datetime

class HoldInfo(BaseModel):
    amount: Money
    foreignAmount: Optional[Money] = None


class RoundUp(BaseModel):
    amount: Money
    boostPortion: Optional[Money] = None


class CashBack(BaseModel):
    description: str
    amount: Money


class TransactionAttributes(BaseModel):
    status: TransactionStatus
    rawText: Optional[str] = None
    description: str
    message: Optional[str] = None
    holdInfo: Optional[HoldInfo] = None
    roundUp: Optional[RoundUp] = None
    cashback: Optional[CashBack] = None
    amount: Money
    foreignAmount: Optional[Money] = None
    settledAt: Optional[datetime] = None
    createdAt: datetime


class TransactionRelationships(BaseModel):
    account: RelatedUUIDObject
    category: RelatedObject
    parentCategory: RelatedObject
    tags: TagsRelationship


class Transaction(TypeandUUID):
    attributes: TransactionAttributes
    relationships: TransactionRelationships
    links: Self

    @ root_validator(pre=True)
    def __extract_data(cls, v: dict):
        # Depending on if the data is being provided from an array or not data may or may not be present
        if "data" in v:
            return v["data"]
        return v

    def __str__(self) -> str:
        """Return the representation of the transaction."""
        return f"<Transaction {self.attributes.status}: {self.attributes.amount.value} {self.attributes.amount.currencyCode} [{self.attributes.description}]>"

    async def add_tags(self, tags: list) -> None:
        assert self._internal.session
        assert self.relationships.tags.links
        await self._internal.session.post(endpoint=self.relationships.tags.links.self, payload=self.__get_tag_payload(tags))

    async def delete_tags(self, tags: list) -> None:
        assert self._internal.session
        assert self.relationships.tags.links
        await self._internal.session.delete(endpoint=self.relationships.tags.links.self, payload=self.__get_tag_payload(tags))

    def __get_tag_payload(self, tags: list) -> dict:
        to_add = []
        for tag in tags:
            to_add.append({"type": "tags", "id": tag})
        return {"data": to_add}


class Transactions(Pagination):
    data: List[Transaction] = []
