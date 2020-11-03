from ..asyncUpBankApi import Client, NotAuthorizedException
import asyncio

# use the environment variable UP_TOKEN
client = Client("up:yeah:bzDy7AB2yckyBDcqaUPJOru7d5jX4o9eHrWbNoGobxRUyvoIqCYgh23Nb68INjrYOGkjIgD50PDAviIIcczXXg8FxzPwy6dzyOxlgju8ZJwor4j0q6ziTbWKOfKa3M9g")

# optionally check the token is valid
async def main():
    accounts = await client.accounts()

    # list accounts
    async for account in accounts:
        print(account)

        # list transactions for account
        async for transaction in account.transactions():
            print(transaction)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())