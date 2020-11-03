# Category Classes
from typing import List, Optional

from asyncupbankapi.models.baseModels import RelatedObject, RelatedObjects, Self, TypeAndId
from pydantic import BaseModel, root_validator


class CategoryAttributes(BaseModel):
    name: str


class CategoryRelationship(BaseModel):
    parent: RelatedObject
    children: RelatedObjects


class Category(TypeAndId):
    attributes: CategoryAttributes
    relationships: CategoryRelationship
    links: Optional[Self] = None

    @ root_validator(pre=True)
    def __extract_data(cls, v: dict):
        if "data" in v:
            return v["data"]
        return v

    def __str__(self) -> str:
        """Return the representation of the Category."""
        return f"<Category '{self.attributes.name}'>"


class Categories(BaseModel):
    data: List[Category] = []
    links: Optional[Self] = None
