from asyncupbankapi import Client
import pytest


@pytest.mark.asyncio
async def test_client_by_environment() -> None:
    client = Client()
    assert client


@pytest.mark.asyncio
async def test_client_by_token() -> None:
    client = Client("FAKE TOKEN")
    assert client


@pytest.mark.asyncio
async def test_ping() -> None:
    client = Client()
    assert await client.ping()
