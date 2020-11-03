# Tag Classes
from typing import List
from asyncupbankapi.models.baseModels import RelatedLinks, TypeAndId, Pagination
from pydantic import BaseModel, root_validator


class TagAttributes(BaseModel):
    name: str


class TagRelationship(BaseModel):
    transactions: RelatedLinks


class Tag(TypeAndId):
    relationships: TagRelationship

    @ root_validator(pre=True)
    def __extract_data(cls, v: dict):
        if "data" in v:
            return v["data"]
        return v

    def __str__(self) -> str:
        """Return the representation of the Tag."""
        return f"<Ping '{self.id}'>"


class Tags(Pagination):
    data: List[Tag] = []