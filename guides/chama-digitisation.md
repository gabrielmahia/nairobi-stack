# Chama Digitisation Guide

A chama is a self-organised savings and investment group. Kenya has over 300,000 registered chamas managing an estimated KES 300B+ in informal capital. They range from small welfare groups (12 members, KES 500/month each) to diaspora investment clubs (50 members, $500/month each, managing real estate portfolios across Nairobi).

The core mechanism is the ROSCA (Rotating Savings and Credit Association): each member contributes a fixed amount each round, one member receives the entire pot, and the rotation continues until everyone has received once. Then a new cycle begins.

---

## Domain model

The core entities:

```
Chama (the group)
  └── Members (participants with a seat in the rotation)
  └── Cycles (one complete rotation — everyone receives once)
        └── Rounds (one meeting — one person receives the pot)
              └── Contributions (one payment by one member)
```

See [github.com/gabrielmahia/chama-protocol](https://github.com/gabrielmahia/chama-protocol) for a complete implementation.

```python
from chama.models import Chama, Member, Cycle, Round

chama = Chama(name="Umoja Investment Group")
chama.add_member(Member("Jane Wanjiku", "0712345678", seat=1))
chama.add_member(Member("John Kamau",  "0723456789", seat=2))
chama.add_member(Member("Mary Achieng","0734567890", seat=3))

# Jane receives first (seat=1), then John (seat=2), then Mary (seat=3)
cycle = Cycle(number=1, contribution_amount=5_000, start_date=date.today())
```

---

## M-Pesa integration pattern

The contribution flow:
1. Member pays via STK Push to the chama's M-Pesa paybill
2. M-Pesa webhook fires with receipt number
3. Record contribution with `ledger.record_contribution(..., receipt="NLJ7RT61SV")`
4. When round is fully collected, disburse to recipient via B2C

```python
from mpesa import MpesaClient
from chama.ledger import Ledger

client = MpesaClient(consumer_key="...", consumer_secret="...", shortcode="...", passkey="...")

# Collect contribution from member
stk = client.stk_push(
    phone=member.phone,
    amount=cycle.contribution_amount,
    reference=f"C{cycle.number}R{round_number}",  # max 12 chars
    description="Chama contribution",
    callback_url="https://yourapp.com/mpesa/callback",
)

# On callback:
def handle_contribution_callback(body: dict):
    payment = MpesaClient.parse_stk_callback(body)
    if payment["paid"]:
        ledger.record_contribution(
            member_id=...,
            cycle=1,
            round_number=...,
            amount=payment["amount"],
            receipt=payment["mpesa_receipt"],
        )
        
        # Check if round is fully collected and disburse
        summary = ledger.round_summary(1, round_number)
        if summary.is_disbursable:
            disburse_to_recipient(summary.recipient)

def disburse_to_recipient(recipient):
    client.b2c(
        phone=recipient.receive_phone,   # mpesa_number if set, else phone
        amount=summary.expected_pot,
        remarks=f"Chama pot — Cycle {cycle.number} Round {round_number}",
        callback_url="https://yourapp.com/mpesa/b2c/callback",
    )
```

---

## Handling the hard cases

### Member misses a contribution
Different chamas have different rules. Common approaches:
- Grace period: allow payment until the *next* round's meeting date
- Fines: KES 100–500 per missed contribution (add to welfare fund)
- Suspension: suspended members don't receive the pot

```python
ledger.mark_missed(member_id, cycle=1, round_number=3)
chama.welfare_fund_kes += 200  # fine goes to welfare fund
```

### Member exits mid-cycle
The cleanest approach: they continue receiving contributions from remaining members but are removed from the rotation for future cycles. Their seat is freed after their scheduled receiving round.

### Diaspora multi-currency chamas
Common pattern: members in London, Dallas, Toronto send GBP/USD/CAD → converted to KES → pooled. Use a remittance provider (Wise preferred for low spread) → disburse to recipient in KES via M-Pesa.

---

## Governance and transparency

The chama's constitution defines rules. Digitising a chama without the constitution leads to disputes. Before writing code, capture:

- Contribution amount per round
- Meeting frequency (weekly, bi-weekly, monthly)
- Rotation order determination (seniority, lottery, volunteering)
- Late payment rules and fines
- Welfare fund rules
- Exit and re-entry rules
- Quorum requirements for decisions

---

## Legal structure

Chamas can register as:
- **Unregistered** (common for small groups — no legal standing, but simpler)
- **Self-help group** — registered with Ministry of Labour & Social Protection
- **Investment club** — registered with CMA for groups trading securities
- **Company Limited by Guarantee** — for larger investment chamas
- **SACCO** — regulated by SASRA (Sacco Societies Regulatory Authority) for chamas offering credit

Most digitisation projects work with unregistered or self-help groups. Get legal advice before building anything that holds or invests member funds formally.
