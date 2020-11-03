from asyncupbankapi import Client
from os import getenv
import pytest
import sys
import os

# So we can do the import
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


@pytest.mark.asyncio
async def test_client_by_environment():

    client = Client()
    assert client


@pytest.mark.asyncio
async def test_client_by_token():
    client = Client("FAKE TOKEN")
    assert client


@pytest.mark.asyncio
async def test_ping():
    client = Client()
    assert await client.ping()


@pytest.mark.asyncio
async def test_accounts():
    client = Client()
    assert await client.accounts()


@pytest.mark.asyncio
async def test_transactions():
    client = Client()
    assert await client.transactions()


@pytest.mark.asyncio
async def test_webhooks():
    client = Client()
    assert await client.webhooks()
