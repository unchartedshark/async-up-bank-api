# Async Up Bank API

This project is a async fork of jcwillox/up-bank-api. I've attempted to keep most things the same but I have changed a fair bit.

If there's any issues please let me know.

[![Project version](https://img.shields.io/pypi/v/async-up-bank-api?style=flat-square)](https://pypi.python.org/pypi/async-up-bank-api)
[![Supported python versions](https://img.shields.io/pypi/pyversions/up-bank-api?style=flat-square)](https://pypi.python.org/pypi/async-up-bank-api)
[![License](https://img.shields.io/github/license/jcwillox/up-bank-api?style=flat-square)](https://github.com/unchartedshark/async-up-bank-api/blob/master/LICENSE)
![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/unchartedshark/async-up-bank-api?style=flat-square)
[![codecov](https://codecov.io/gh/unchartedshark/async-up-bank-api/branch/master/graph/badge.svg?token=MYPJYBFCWJ)](https://codecov.io/gh/unchartedshark/async-up-bank-api)

This is an unofficial python wrapper (client) for the australian bank Up's API.

- 🕶️ [The Up Website](https://up.com.au)
- 📖 [Up API Documentation](https://developer.up.com.au)
- [Up API on Github](https://github.com/up-banking/api)

## Installation

```shell
$ pip install async-up-bank-api
```

## Usage

The code is fully typed and documented so I'd recommend just having a look at the code, or letting syntax completion take the wheel.

To use this library you will need a personal access token which can be retrieved from https://developer.up.com.au. When using this library you can either provide the token directly or use the environment variable `UP_TOKEN`.

```python
from upbankapi import Client, NotAuthorizedException
import asyncio

# use the environment variable UP_TOKEN
client = Client()

# or directly provide token
client = Client(token="MY_TOKEN")  

# optionally check the token is valid
async def main():
    try:
        user_id = await client.ping()
        print("Authorized: " + user_id)
    except NotAuthorizedException:
        print("The token is invalid")
    finally:
        await client.close()
        
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
```
## Examples

* [Accounts](#accounts)
* [Transactions](#transactions)
* [Pagination](#pagination)
* [Webhooks](#webhooks)

### Accounts

```python
async def main():
    account: Account
    transaction: Transaction

    # list accounts
    async for account in await client.accounts():
        print(account)

        # list transactions for account
        async for transaction in await account.transactions():
            print(transaction)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

>>> <Account 'Up Account' (TRANSACTIONAL): 1234.56 AUD>
>>> <Transaction SETTLED: -1.0 AUD [7-Eleven]>
>>> <Account '💰 Savings' (SAVER): 12345.67 AUD>
>>> <Transaction SETTLED: 10.0 AUD [Interest]>
```

```python
# get the unique id of an account
accounts[1].id
>>> "d7cd1152-e78a-4ad7-8202-d27cddb02a28"

# get a specific account by its unique id
savings = client.account("d7cd1152-e78a-4ad7-8202-d27cddb02a28")
savings
>>> <Account '💰 Savings' (SAVER): 12345.67 AUD>
savings.balance
>>> 12345.67
```

### Transactions

Get transactions across all accounts.
```python
>>> list( await client.transactions() )
[<Transaction SETTLED: -1.0 AUD [7-Eleven]>, <Transaction SETTLED: 10.0 AUD [Interest]>]
```
Get last 5 transactions for a given account id.
```python
SAVINGS_ID = "d7cd1152-e78a-4ad7-8202-d27cddb02a28"

list( await client.account(SAVINGS_ID).transactions(limit=5) )
>>> [<Transaction SETTLED: 10.0 AUD [Interest]>]

list( await client.transactions(account_id=SAVINGS_ID, limit=5) )
>>> [<Transaction SETTLED: 10.0 AUD [Interest]>]
```
Get a specific transaction.
```python
await client.transaction("17c577f2-ae8e-4622-90a7-87d95094c2a9")
>>> <Transaction SETTLED: -1.0 AUD [7-Eleven]>
```

### Pagination

Up's API uses pagination, this means methods in this library that return more than one record with pagination sported will return a instance inheriting from `Pagination`. This is effectively just an async iterator. 

Every `page_size` records the instance of `Pagination` will make a request for the next `page_size` records asynchronous.

A `limit` can be used to limit the maximum number of records returned, when a limit is specified the iterator will never return more than `limit` but can return less.
Using `limit=None` will return all records.
```python
transactions = await client.transactions(limit=5)

async for transaction in transactions:
    print(transactions)

print(list( transactions ))
>>> [<Transaction SETTLED: -1.0 AUD [7-Eleven]>, <Transaction SETTLED: 10.0 AUD [Interest]>]
```
`Pagination` supports **slicing**, it still returns an iterator and will fetch the records as required.

```python
transactions = await client.transactions(limit=20)
list( transactions[10:20] )
>>> [<Transaction ...>, ...]
```
> Note that while it may appear the slice `[:limit]` has the same effect as specifying a `limit`, it does not, when you specify a limit the code optimises the page size. 
> For example, using the slice `[:5]` will fetch the first 20 records and return only 5, using `limit=5` it will fetch and return the first 5 records. However, if you manually specify `page_size=5` then both options have the same effect.

### Webhooks

List users webhooks
```python
list( await client.webhooks() )
>>> [<Webhook '1c3a4fd4-6c57-4aa8-8481-cf31a46bc001': https://mywebhook.tld/c2f89ed40e26c936 (Hello World!)>]
```

Get a specific webhook
```python
await client.webhook("1c3a4fd4-6c57-4aa8-8481-cf31a46bc001")
# or equivalently
await client.webhook.get("1c3a4fd4-6c57-4aa8-8481-cf31a46bc001")
>>> <Webhook '1c3a4fd4-6c57-4aa8-8481-cf31a46bc001': https://mywebhook.tld/c2f89ed40e26c936 (Hello World!)>
```

Create a webhook
```python
await client.webhook.create("https://mywebhook.tld/c2f89ed40e26c936", description="Hello World!")
>>> <Webhook '1c3a4fd4-6c57-4aa8-8481-cf31a46bc001': https://mywebhook.tld/c2f89ed40e26c936 (Hello World!)>
```

Interacting with a webhook
```python
webhook = await client.webhook("1c3a4fd4-6c57-4aa8-8481-cf31a46bc001")

# ping the webhook
await webhook.ping()
>>> <WebhookEvent PING: webhook_id='1c3a4fd4-6c57-4aa8-8481-cf31a46bc001'>

# get the webhooks logs
list( await webhook.logs() )
>>> [<WebhookLog BAD_RESPONSE_CODE: response_code=404>]

# get the event associated with a log entry
await webhook.logs()[0].event
>>> <WebhookEvent PING: webhook_id='1c3a4fd4-6c57-4aa8-8481-cf31a46bc001'>

# delete the webhook
await webhook.delete()
```

When interacting with with a specific webhook there are two options.

For example the two code blocks below have the same result (deleting the webhook), however, the first option uses 2 requests and the second option uses only 1 request.
This is because option 1 will request the webhook details, and then send the delete request. Option 2 directly sends the delete request.
```python
# Option 1
await client.webhook("1c3a4fd4-6c57-4aa8-8481-cf31a46bc001").delete()
```
```python
# Option 2
await client.webhook.delete("1c3a4fd4-6c57-4aa8-8481-cf31a46bc001")
```
Each option can be useful depending on the use case. Option 2 is primarily useful when do not already have the Webhook object but have the id and only want to perform a single action.
