# M-Pesa Integration Guide

Safaricom M-Pesa (Daraja API) is the payment backbone of Kenya. 40M+ active users, 
~99% smartphone and feature phone penetration in Kenya. It is the Stripe of East Africa — 
except Stripe took years to enter Kenya, and M-Pesa is already there.

---

## Daraja API versions

| Version | Status | What you use it for |
|---------|--------|---------------------|
| Daraja v2 | Deprecated | Legacy — do not use for new integrations |
| Daraja v3 | Current | STK Push, B2C, C2B, account balance, reversals |

Always use v3. Daraja v2 endpoints still work but Safaricom will break them eventually.

---

## Getting credentials

1. Register at [developer.safaricom.co.ke](https://developer.safaricom.co.ke)
2. Create an app → get Consumer Key + Consumer Secret
3. For STK Push: get the **Lipa Na M-Pesa Online (LNM) Passkey** from your shortcode settings
4. For B2C: get your **initiator name** and generate a **Security Credential** (encrypted password)

**Sandbox shortcode**: `174379`  
**Sandbox passkey**: `bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919`

---

## Authentication

Daraja uses OAuth2 client credentials. Tokens expire after 3600 seconds.
Cache them — don't request a new token on every API call.

```python
import base64, json, urllib.request

def get_token(consumer_key, consumer_secret, sandbox=True):
    base = "https://sandbox.safaricom.co.ke" if sandbox else "https://api.safaricom.co.ke"
    credentials = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()
    req = urllib.request.Request(
        f"{base}/oauth/v1/generate?grant_type=client_credentials",
        headers={"Authorization": f"Basic {credentials}"}
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["access_token"]
```

Or use the SDK: [github.com/gabrielmahia/mpesa-python](https://github.com/gabrielmahia/mpesa-python)

```python
from mpesa import MpesaClient
client = MpesaClient(consumer_key="...", consumer_secret="...", shortcode="174379", passkey="...", sandbox=True)
```

---

## STK Push (Lipa Na M-Pesa)

The most common integration. A payment prompt appears on the customer's phone.

```python
result = client.stk_push(
    phone="0712345678",        # normalised automatically to 254712345678
    amount=500,                # KES integer — M-Pesa does not do decimal amounts
    reference="Order-001",     # max 12 alphanumeric chars
    description="Coffee",      # shown to customer, max 13 chars
    callback_url="https://yourapp.com/mpesa/callback",
)
print(result.checkout_request_id)  # save this — use to query status
```

**What happens next:**
1. Customer sees a push notification → opens it → enters M-Pesa PIN
2. Safaricom POSTs to your `callback_url` with success or failure
3. If callback never arrives (network issues), poll `stk_query(checkout_request_id)`

### Handling the callback

```python
def handle_stk_callback(body: dict):
    result = MpesaClient.parse_stk_callback(body)
    if result["paid"]:
        # result["mpesa_receipt"]  — your audit trail
        # result["amount"]         — what was actually paid
        # result["phone"]          — who paid
        fulfill_order(result["mpesa_receipt"])
    else:
        # result["result_code"] "1032" = user cancelled
        # result["result_code"] "1037" = timed out
        handle_failure(result["result_code"])
```

---

## Common M-Pesa result codes

| Code | Meaning | What to do |
|------|---------|------------|
| `0` | Success | Fulfill order |
| `1` | Insufficient balance | Tell customer to top up |
| `1032` | Cancelled by user | Show cancellation screen |
| `1037` | DS timeout — timed out | Offer to retry |
| `2001` | Wrong credentials | Check your consumer key/secret |
| `17` | M-Pesa system internal error | Retry after 30s |
| `26` | System busy | Retry with exponential backoff |

---

## Phone number normalisation

M-Pesa requires the `2547XXXXXXXX` format (12 digits, no leading +). 
Your users will enter it in every possible format:

```python
def normalise_phone(raw: str) -> str:
    """0712345678 / +254712345678 / 712345678 → 254712345678"""
    cleaned = re.sub(r"[\s\-\(\)]", "", raw).lstrip("+")
    if cleaned.startswith("07"): return "254" + cleaned[1:]
    if cleaned.startswith("7") and len(cleaned) == 9: return "254" + cleaned
    return cleaned  # assume already normalised
```

---

## Sandbox → production checklist

- [ ] Swap `sandbox=True` to `sandbox=False`
- [ ] Replace sandbox credentials with production Consumer Key/Secret
- [ ] Replace sandbox shortcode `174379` with your production shortcode
- [ ] Replace sandbox passkey with your production LNM passkey
- [ ] Your `callback_url` must be HTTPS (not HTTP) in production
- [ ] `callback_url` must be publicly accessible — localhost won't work
- [ ] Test with a real phone number and a small amount (KES 1) before going live

---

## Gotchas

**Amount must be an integer.** M-Pesa does not accept KES 99.50. Round up or use KES 100.

**AccountReference max 12 chars.** Longer strings are silently truncated, causing reconciliation headaches.

**Callbacks are not guaranteed.** Network issues between Safaricom and your server are common. Always implement `stk_query` polling as a fallback.

**One active token per app.** Requesting a new token doesn't invalidate the old one, but if you request many tokens rapidly you can hit rate limits. Cache tokens until 60 seconds before expiry.

**Sandbox numbers.** In sandbox, only Safaricom-registered test numbers will trigger the STK push. Use `+254708374149` as the test number.
