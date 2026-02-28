# SMS Infrastructure in East Africa

SMS reaches every phone in Kenya — feature phones, smartphones, and everything in between.
For rural users, farmers, and anyone without data, SMS is the primary digital channel.

---

## Africa's Talking API

[Africa's Talking](https://africastalking.com) is the go-to SMS and USSD provider for East Africa.
Covers Kenya, Uganda, Tanzania, Ethiopia, Rwanda, Nigeria, Ghana, and more.

### Getting started

1. Create account at africastalking.com
2. Create an app → get API Key + username
3. Use `sandbox` username for testing (no charges, no real SMS)
4. Top up airtime in production → messages billed per-SMS

```python
import urllib.request, json, urllib.parse

class ATClient:
    SANDBOX_URL = "https://api.sandbox.africastalking.com/version1"
    LIVE_URL    = "https://api.africastalking.com/version1"

    def __init__(self, api_key: str, username: str, sandbox: bool = True):
        self.api_key = api_key
        self.username = username
        self.base = self.SANDBOX_URL if sandbox else self.LIVE_URL

    def send_sms(self, to: list[str], message: str, sender_id: str = "") -> dict:
        """Send SMS to one or more recipients.
        
        to: list of phone numbers in international format (+254...)
        message: max 160 chars per SMS (longer → multi-part, billed per part)
        sender_id: registered alphanumeric sender (e.g. "OpenRes") — optional
        """
        params = {
            "username": self.username,
            "to": ",".join(to),
            "message": message,
        }
        if sender_id:
            params["from"] = sender_id
        
        body = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(
            f"{self.base}/messaging",
            data=body,
            headers={
                "apiKey": self.api_key,
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
```

---

## SMS character limits and billing

| Characters | Parts | Cost |
|-----------|-------|------|
| 1–160 | 1 | 1× rate |
| 161–306 | 2 | 2× rate |
| 307–459 | 3 | 3× rate |

Keep messages under 160 characters. Every extra part costs money and may confuse the recipient.

**Kenyan pricing (Africa's Talking, 2024):** ~KES 1–2 per SMS depending on volume tier.

---

## Sender ID registration

An alphanumeric sender ID (e.g. `OpenRes`, `ParishCNT`) requires registration with the
Communications Authority of Kenya (CA) through your SMS provider. 

**Timeline:** 2–6 weeks.  
**Required:** Business registration, KRA PIN, application form.  
**Without it:** Your SMS shows from a random short number. Still works; just less branded.

---

## Bilingual message design

Kenya's official languages are English and Kiswahili. For rural and agricultural audiences,
Kiswahili significantly increases open rates and action rates.

```python
TEMPLATES = {
    "drought_alert": {
        "en": "DROUGHT ALERT: {county}. Water stress HIGH ({wsi:.0%}). Seek water sources early.",
        "sw": "TAHADHARI YA UKAME: {county}. Msongo wa maji UKO JUU ({wsi:.0%}). Tafuta maji mapema.",
    },
    "market_price": {
        "en": "Maize price: KES {price}/90kg bag in {market}. ({date})",
        "sw": "Bei ya mahindi: KES {price}/gunia la 90kg {market}. ({date})",
    },
}

def format_sms(template_key: str, lang: str = "sw", **kwargs) -> str:
    tmpl = TEMPLATES[template_key][lang]
    msg = tmpl.format(**kwargs)
    assert len(msg) <= 160, f"SMS too long: {len(msg)} chars"
    return msg
```

---

## Delivery reports

Africa's Talking sends delivery receipts to a callback URL you configure.
Always implement this — it's the only way to know if a message actually reached the handset.

Statuses: `Success`, `Failed`, `Rejected`, `Buffered` (queued for offline device)

```python
def handle_delivery_report(data: dict):
    status = data.get("status")
    phone = data.get("phoneNumber")
    if status != "Success":
        log_failed_delivery(phone, status)
        # "Buffered" = phone offline — will deliver when they come online
        # "Failed"   = number unreachable — may need to remove from list
```

---

## Rate limits and bulk sending

Africa's Talking supports bulk sends (comma-separated numbers in `to`). Max ~1000 recipients per request.
For large campaigns, paginate in batches of 500 with 1–2 second delays.

---

## Alternatives

| Provider | Coverage | Notes |
|----------|----------|-------|
| Twilio | Kenya + global | More expensive per SMS in KE; good for multi-country |
| Vonage | Kenya + global | Similar to Twilio |
| SMSLeopard | Kenya-focused | Cheaper; smaller developer ecosystem |
| Bulk SMS Kenya | Kenya only | Very cheap; no developer API worth mentioning |

For Kenya-first products, Africa's Talking is the default. Only reach for Twilio if you need unified multi-country coverage from day one.
