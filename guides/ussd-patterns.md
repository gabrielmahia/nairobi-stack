# USSD Design Patterns for East Africa

USSD (Unstructured Supplementary Service Data) is the session protocol that powers M-Pesa's `*737#` menu. It's synchronous, stateless on the network side, and works on every phone — no smartphone, no data plan, no app required.

## How it works

1. User dials a shortcode (`*384*123#`)
2. Telco opens a session to your HTTP endpoint
3. Your endpoint returns text (max 182 chars)
4. User responds with a number
5. Repeat until session ends (`END` response) or times out (~180 seconds)

Your endpoint must respond in **under 3 seconds** or the session drops.

## Session structure

Africa's Talking sends a `POST` with:
```
sessionId=session_abc123
serviceCode=*384*123#
phoneNumber=+254712345678
networkCode=Safaricom
text=          ← empty on first request, accumulates inputs on subsequent ones
```

`text` accumulates: `""` → `"1"` → `"1*2"` → `"1*2*500"` as the user navigates deeper.

## Response format

```python
def handle_ussd(session_id, phone, text):
    inputs = text.split("*") if text else []
    
    if not inputs or inputs == [""]:
        # First screen
        return "CON Welcome to MyApp\n1. Check balance\n2. Send money\n0. Exit"
    
    if inputs[0] == "1":
        balance = get_balance(phone)
        return f"END Your balance is KES {balance}"  # END = close session
    
    if inputs[0] == "2":
        if len(inputs) == 1:
            return "CON Enter recipient phone number:\n(Format: 07XXXXXXXX)"
        if len(inputs) == 2:
            return f"CON Enter amount (KES):\nSending to {inputs[1]}"
        if len(inputs) == 3:
            # Confirm
            return f"CON Confirm send KES {inputs[2]} to {inputs[1]}?\n1. Yes\n2. No"
        if len(inputs) == 4 and inputs[3] == "1":
            # Execute
            do_transfer(phone, inputs[1], int(inputs[2]))
            return f"END Sent KES {inputs[2]} to {inputs[1]}. Receipt: #{generate_receipt()}"
        return "END Cancelled."
    
    return "END Goodbye."
```

## Design rules

**Navigation:**
- `0` always goes back one level (never use 0 for a forward action)
- `00` goes to main menu
- `9` is conventionally "more options" (pagination)
- Keep options ≤ 5 per screen

**Text limits:**
- 182 characters total per screen (including `CON ` or `END ` prefix)
- No markdown, no formatting — plain text only
- Test on actual feature phone displays (smaller than you think)

**Session management:**
- Sessions time out in ~180 seconds — don't design flows that take longer
- Store session state server-side by `sessionId` (Redis or SQLite TTL cache)
- Assume the user will abandon halfway — design for re-entry

**Language:**
- Lead with Kiswahili option on first screen for government/NGO apps
- Keep language selection persistent via phone number in your DB

## Production considerations

**Africa's Talking USSD setup:**
1. Purchase a shortcode (Kenya: KES 50,000/year for dedicated, or share a premium one)
2. Register with Communications Authority of Kenya (CA)
3. AT handles the shortcode routing to your HTTP endpoint
4. Your endpoint must be on HTTPS in production

**Latency budget:**
- Network (AT to your server): ~200ms
- Your response time: target <500ms, hard limit 3000ms
- Total: <3 seconds or session drops

**Testing:**
Africa's Talking has a USSD simulator at [sandbox.africastalking.com](https://sandbox.africastalking.com). Use it before testing on a real handset.

**FastAPI example endpoint:**

```python
from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.post("/ussd", response_class=PlainTextResponse)
async def ussd_handler(
    sessionId: str = Form(...),
    serviceCode: str = Form(...),
    phoneNumber: str = Form(...),
    text: str = Form(default=""),
):
    inputs = text.split("*") if text else []
    response = handle_ussd(sessionId, phoneNumber, inputs)
    return response
```

## Common patterns from production

**Pattern: Progressive data collection**
```
Screen 1: CON What are you registering for?
          1. Water access point
          2. Medical case
          3. School attendance

Screen 2: CON Enter the location description:
          (max 2 sentences)

Screen 3: CON Confirm?
          1. Yes — submit
          2. No — start over
```

**Pattern: Balance check with PIN**
```
Screen 1: CON Enter your 4-digit PIN:
Screen 2: END Balance: KES 12,450. Last transaction: KES 500 received from 0722...
```

**Pattern: Kiswahili/English toggle**
```
Screen 1: CON Hello / Habari
          1. English
          2. Kiswahili
```
Store language preference against `phoneNumber` in your DB.
