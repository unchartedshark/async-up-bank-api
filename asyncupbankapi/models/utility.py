# Ping Classes
from uuid import UUID
from pydantic import BaseModel, root_validator


class Ping(BaseModel):
    id: UUID
    statusEmoji: str

    @ root_validator(pre=True)
    def __extract_data(cls, v: dict):
        return v["meta"]

    def __str__(self) -> str:
        """Return the representation of the Ping."""
        return f"<Ping '{self.id}': {self.statusEmoji}>"