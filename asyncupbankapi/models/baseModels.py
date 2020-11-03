# Common Classes
from __future__ import annotations
from pydantic import BaseModel, root_validator, validator, PrivateAttr
from yarl import URL
from uuid import UUID
from typing import AsyncIterator, Awaitable, Iterator, Optional, List, Union
from asyncupbankapi.const import PAGE_SIZE
from asyncupbankapi.httpSession import HttpSession
import asyncio


class Self(BaseModel):
    self: URL

    class Config:
        arbitrary_types_allowed = True

    @validator('*', pre=True)
    def _create_url(cls, v):
        if v:
            return URL(v, encoded=True)


class Related(BaseModel):
    related: URL

    class Config:
        arbitrary_types_allowed = True

    @validator('*', pre=True)
    def _create_url(cls, v):
        if v:
            return URL(v, encoded=True)


class RelatedLinks(BaseModel):
    links: Related


class RelatedObjectData(BaseModel):
    type: str
    id: str


class RelatedUUIDObjectData(BaseModel):
    type: str
    id: UUID


class RelatedObject(BaseModel):
    data: Optional[RelatedObjectData] = None
    links: Optional[Related] = None


class RelatedUUIDObject(BaseModel):
    data: Optional[RelatedUUIDObjectData] = None
    links: Optional[Related] = None


class RelatedUUIDObjectWithoutLinks(BaseModel):
    data: Optional[RelatedUUIDObjectData] = None


class RelatedObjects(BaseModel):
    data: List[RelatedObjectData] = []
    links: Optional[Related] = None


class TagsRelationship(BaseModel):
    data: List[RelatedObjectData] = []
    links: Optional[Self] = None


class PaginationLinks(BaseModel):
    prev: Optional[URL] = None
    next: Optional[URL] = None

    class Config:
        arbitrary_types_allowed = True

    @validator('*', pre=True)
    def _create_url(cls, v):
        if v:
            return URL(v, encoded=True)


class Money(BaseModel):
    currencyCode: str
    value: float
    valueInBaseUnits: int


class TypeInternal():
    session: Optional[HttpSession] = None


class Type(BaseModel):
    type: str
    _session: HttpSession = PrivateAttr()

    def __init__(self, session: Optional[HttpSession] = None, **data: dict, ) -> None:
        super().__init__(**data)
        if session:
            self._session = session

    class Config:
        arbitrary_types_allowed = True

    @ root_validator(pre=True)
    def __extract_data(cls, v: dict) -> dict:
        if "data" in v:
            return v["data"]
        return v

    def _set_session(self, session: Optional[HttpSession] = None):
        if session:
            self._session = session


class TypeandUUID(Type):
    id: UUID


class TypeAndId(Type):
    id: str

# Pagination
class Pagination(BaseModel):
    links: PaginationLinks
    data: List[Type]
    _next_page: Optional[Awaitable[dict]] = PrivateAttr(default=None)
    _limit: Optional[int] = PrivateAttr(default=None)
    _session: HttpSession = PrivateAttr(default=None)

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, data: dict, session: HttpSession, limit: Optional[int] = None) -> None:
        super().__init__(**data)
        self._session = session
        self._limit = limit
        for i in self.data:
            i._session = self._session

    async def __getitem__(self, index: Union[int, slice]) -> Union[Type, Pagination._Slice]:
        assert isinstance(index, (int, slice))
        if isinstance(index, int):
            await self._fetch_to(index)
            return self.data[index]
        return Pagination._Slice(self, index)

    async def __aiter__(self) -> AsyncIterator:
        for element in self.data:
            yield element
        while self.has_next:
            new_elements = await self.next()
            for element in new_elements:
                yield element

    @ property
    def count(self) -> int:
        return len(self.data)

    @ property
    def has_next(self) -> bool:
        if not self.links.next:
            return False
        if self._limit:
            return self.count < self._limit
        return True

    async def _fetch_to(self, index) -> None:
        while len(self.data) <= index and self.has_next:
            await self.next()

    async def next(self) -> List:
        assert self._session

        if self._next_page:
            response = await self._next_page
        else:
            # First call fetch the next page
            response = await self._session.get(self.__get_next_url())

        data = self.__class__(
            response, self._session, self._limit)

        self.links = data.links

        # Queue up the next page if we need to
        if self.has_next:
            self._next_page = asyncio.create_task(self._session.get(
                self.__get_next_url(len(data.data))))

        self.data += data.data

        return data.data

    def __get_next_url(self, new_records: int = 0) -> URL:
        # Next must exist otherwise something is wrong..
        assert self.links.next

        url = self.links.next

        # If there is a limit see if we have hit it.
        if self._limit:
            page_size = url.query.get(PAGE_SIZE)
            # Page Size MUST exist otherwise something is wrong..
            assert page_size
            records = self.count + new_records
            diff = records + int(page_size) - self._limit
            if diff > 0:
                # Only load what we need to on the next page load
                limit_to = abs(records - self._limit)
                return url.update_query({PAGE_SIZE: limit_to})
        return url

    class _Slice():
        def __init__(self, _list: Pagination, _slice: slice) -> None:
            self.__list = _list
            self.__start = _slice.start or 0
            self.__end = _slice.stop
            self.__step = _slice.step or 1

        def __iter__(self) -> Iterator:
            index = self.__start
            while self.__end and index < self.__end:
                if self.__list.count > index or self.__list.has_next:
                    yield self.__list[index]
                    index += self.__step
                else:
                    return
