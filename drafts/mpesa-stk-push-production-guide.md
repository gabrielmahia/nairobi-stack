---
title: "M-Pesa STK Push in Python: A Production Guide"
date: 2026-03-19
labels: [BUILD, MPESA, PYTHON, AFRICA]
---

There are tutorials that show you how to get an STK Push working in a sandbox. This is not that. This is the guide I wish existed when I was putting M-Pesa into production for the first time — covering the parts that break in real conditions: token expiry, callback verification, network timeouts, and what the Daraja docs quietly omit.

---

## What STK Push actually does

When you trigger an STK Push, Safaricom sends a payment prompt to a customer's phone. The customer enters their PIN. Safaricom processes the payment and sends a callback to your server with the result.

Three things can go wrong at every step. Most tutorials cover the happy path. This covers what happens when the network drops, the customer ignores the prompt, or Safaricom's callback server behaves unexpectedly.

---

## The token problem

Daraja OAuth tokens expire after one hour. If you generate a token at startup and cache it indefinitely, your integration will fail silently after the first hour.

The right pattern is not to cache by time. It is to cache the token, catch the 401, and regenerate:

```python
import requests, base64, time

class DarajaAuth:
    def __init__(self, consumer_key: str, consumer_secret: str, env: str = "sandbox"):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.base_url = (
            "https://api.safaricom.co.ke" if env == "production"
            else "https://sandbox.safaricom.co.ke"
        )
        self._token: str | None = None
        self._expires_at: float = 0

    def get_token(self) -> str:
        # Refresh 60 seconds before expiry
        if self._token and time.time() < self._expires_at - 60:
            return self._token
        credentials = base64.b64encode(
            f"{self.consumer_key}:{self.consumer_secret}".encode()
        ).decode()
        response = requests.get(
            f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials",
            headers={"Authorization": f"Basic {credentials}"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        self._token = data["access_token"]
        self._expires_at = time.time() + int(data["expires_in"])
        return self._token
```

The `-60` buffer handles clock skew between your server and Safaricom's. Without it, you will occasionally get a valid-looking token that fails on the very next request.

---

## The password

The STK Push password is not your consumer secret. It is a base64-encoded string assembled from three values at the moment of the request:

```python
import base64
from datetime import datetime

def generate_password(shortcode: str, passkey: str) -> tuple[str, str]:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    raw = f"{shortcode}{passkey}{timestamp}"
    password = base64.b64encode(raw.encode()).decode()
    return password, timestamp
```

The timestamp must match the one in your request payload exactly. Generate both together and use both.

---

## The STK Push request

```python
def stk_push(
    auth: DarajaAuth,
    phone: str,
    amount: int,
    shortcode: str,
    passkey: str,
    callback_url: str,
    reference: str,
    description: str,
) -> dict:
    password, timestamp = generate_password(shortcode, passkey)
    
    # Normalise phone: 07XXXXXXXX → 2547XXXXXXXX
    if phone.startswith("0"):
        phone = "254" + phone[1:]
    elif phone.startswith("+"):
        phone = phone[1:]
    
    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",  # or CustomerBuyGoodsOnline for till
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": callback_url,
        "AccountReference": reference[:12],  # max 12 chars
        "TransactionDesc": description[:13],  # max 13 chars
    }
    
    response = requests.post(
        f"{auth.base_url}/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers={"Authorization": f"Bearer {auth.get_token()}"},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()
```

Two things the docs understate: `AccountReference` is silently truncated in some environments if it exceeds 12 characters. `TransactionDesc` silently breaks the request if it exceeds 13. Truncate both yourself before sending.

---

## The callback

Safaricom posts to your `CallBackURL` with a result object. The structure differs between success and failure, and the nesting is deeper than you expect:

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/mpesa/callback")
async def mpesa_callback(request: Request):
    body = await request.json()
    stk_callback = body["Body"]["stkCallback"]
    
    merchant_request_id = stk_callback["MerchantRequestID"]
    checkout_request_id = stk_callback["CheckoutRequestID"]
    result_code = stk_callback["ResultCode"]
    result_desc = stk_callback["ResultDesc"]
    
    if result_code == 0:
        # Payment succeeded — extract metadata
        items = stk_callback["CallbackMetadata"]["Item"]
        metadata = {item["Name"]: item.get("Value") for item in items}
        
        amount        = metadata.get("Amount")
        receipt_number = metadata.get("MpesaReceiptNumber")
        phone         = metadata.get("PhoneNumber")
        transaction_date = metadata.get("TransactionDate")
        
        # Store and fulfil
        ...
    else:
        # Payment failed or cancelled
        # result_code 1032 = user cancelled
        # result_code 1037 = timeout
        # result_code 2001 = wrong PIN
        ...
    
    # Always return 200 to Safaricom regardless of your processing result
    # If you return a non-200, they will retry the callback
    return {"ResultCode": 0, "ResultDesc": "Accepted"}
```

The last point is critical. Safaricom retries callbacks if they don't receive a 200. Process asynchronously, return 200 immediately, and handle failures in your own retry queue.

---

## Verifying the callback is from Safaricom

The sandbox does not send security headers. Production does. Use a pre-shared secret in the callback URL itself as a minimum:

```python
import hmac, hashlib

SECRET = "your-webhook-secret"

@app.post("/mpesa/callback/{token}")
async def mpesa_callback(token: str, request: Request):
    # Constant-time comparison to prevent timing attacks
    expected = hmac.new(SECRET.encode(), digestmod=hashlib.sha256).hexdigest()
    if not hmac.compare_digest(token, expected):
        return Response(status_code=403)
    ...
```

In production, also validate the source IP against [Safaricom's published ranges](https://developer.safaricom.co.ke/docs#ip-whitelisting).

---

## Querying transaction status

Do not rely solely on callbacks. Customers close apps, connections drop, and callbacks occasionally fail. Always implement a status query:

```python
def query_stk_status(
    auth: DarajaAuth,
    shortcode: str,
    passkey: str,
    checkout_request_id: str,
) -> dict:
    password, timestamp = generate_password(shortcode, passkey)
    
    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "CheckoutRequestID": checkout_request_id,
    }
    
    response = requests.post(
        f"{auth.base_url}/mpesa/stkpushquery/v1/query",
        json=payload,
        headers={"Authorization": f"Bearer {auth.get_token()}"},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()
```

A `ResultCode` of `0` means confirmed. Query 30 seconds after initiating the push if no callback has arrived. Stop querying after 2 minutes — if no result by then, treat as failed and let the customer retry.

---

## The parts Safaricom's docs don't cover clearly

**Phone number format:** The API accepts `2547XXXXXXXX` but silently rejects `+2547XXXXXXXX`. Normalise before sending.

**Amount must be an integer:** Passing `100.0` will fail silently in some environments. Cast to `int`.

**Sandbox phone numbers:** In the sandbox, only the number `254708374149` triggers a successful flow. Any other number will time out or return an error. This is not documented.

**CallbackURL must be HTTPS:** HTTP callback URLs are silently rejected in production. During development, use [ngrok](https://ngrok.com) or [smee.io](https://smee.io).

**Shortcode types:** If you use a till number (buy goods), `TransactionType` must be `CustomerBuyGoodsOnline` and `PartyB` must be the till number, not the head office shortcode. The error message when you get this wrong — "Invalid Shortcode" — does not tell you which shortcode is wrong.

---

## If you want this as an MCP server

All of the above is wrapped in [mpesa-mcp](https://github.com/gabrielmahia/mpesa-mcp) — an MCP server that gives AI agents access to M-Pesa and Africa's Talking. Install with `pip install mpesa-mcp`. The server handles token management, phone normalisation, and error parsing so you don't have to.

For the raw Python SDK: [daraja-v3](https://pypi.org/project/daraja-v3/). For test doubles that let you build without a Safaricom account: [daraja-mock](https://pypi.org/project/daraja-mock/).

---

*Gabriel Mahia builds decision infrastructure for East Africa. Engineering blog: [aikungfu.dev](https://aikungfu.dev). Portfolio: [gabrielmahia.github.io](https://gabrielmahia.github.io).*
