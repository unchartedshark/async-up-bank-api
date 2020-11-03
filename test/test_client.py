from os import getenv
import pytest
import sys, os

# So we can do the import
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from asyncupbankapi import Client

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
