# Account Classes
from typing import List
from asyncupbankapi.models.transactions import Transactions
from asyncupbankapi.models.baseModels import Money, RelatedLinks, Self, TypeandUUID, Pagination
from asyncupbankapi.const import AccountType
from pydantic import BaseModel, root_validator
from datetime import datetime


class AccountAttributes(BaseModel):
    displayName: str
    accountType: AccountType
    balance: Money
    createdAt: datetime


class AccountRelationship(BaseModel):
    transactions: RelatedLinks


class Account(TypeandUUID):
    attributes: AccountAttributes
    relationships: AccountRelationship
    links: Self

    @ root_validator(pre=True)
    def __extract_data(cls, v: dict):
        if "data" in v:
            return v["data"]
        return v

    def __str__(self) -> str:
        """Return the representation of the account."""
        return f"<Account '{self.attributes.displayName}' ({self.attributes.accountType}): {self.attributes.balance.value} {self.attributes.balance.currencyCode}>"

    async def transactions(self) -> Transactions:
        return Transactions(
            data=await self._session.get(self.relationships.transactions.links.related),
            session=self._session)


class Accounts(Pagination):
    data: List[Account] = []
