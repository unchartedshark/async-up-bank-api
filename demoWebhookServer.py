from typing import Optional
from fastapi import FastAPI, Header, Request
import hmac
import hashlib
import asyncio
app = FastAPI()


@app.post("/")
async def handle_webhook(request: Request, x_up_authenticity_signature: Optional[str] = Header(None)):
    if x_up_authenticity_signature is None:
        return "No auth"

    body = await request.body()
    asyncio.create_task(run_async(body, x_up_authenticity_signature))

    return "Success"


async def run_async(body: bytes, x_up_authenticity_signature: str):
    SECRET_KEY = b"RFlOErmrv9FVQxHqYk3RzC1i5BZo56RWooY4UTzaP73BnWSS6xk9os8bDLsi7nCH"

    # Check to see if this is a valid request from UP Bank.
    if not hmac.compare_digest(hmac.new(SECRET_KEY, bytes(body), hashlib.sha256).hexdigest(), x_up_authenticity_signature):
        # Bad Authentication Attempt
        return
    print(body)
