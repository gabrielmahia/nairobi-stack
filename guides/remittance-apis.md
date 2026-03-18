# Remittance APIs — Sending Money to Kenya

The diaspora-to-Kenya corridor is one of the world's top 10 remittance flows.
Kenya received ~$4.2B in diaspora remittances in 2023 (CBK data). The API landscape
is fragmented — here's what each provider actually offers developers.

---

## Provider summary

| Provider | API available? | Kenya corridor | M-Pesa delivery | Notes |
|----------|---------------|----------------|-----------------|-------|
| Wise (TransferWise) | ✅ Yes | ✅ Yes | ❌ Bank only | Best rate, slowest |
| Sendwave | ❌ No public API | ✅ Yes | ✅ Yes | Consumer-only |
| Remitly | ✅ Yes (partner only) | ✅ Yes | ✅ Yes | Requires partnership agreement |
| WorldRemit | ✅ Limited | ✅ Yes | ✅ Yes | B2B via WorldRemit Business |
| Western Union | ✅ Partner API | ✅ Yes | ✅ Yes | High fees, ubiquitous pickup |
| Pesalink | ✅ Yes (CBK) | 🇰🇪 Kenya only | Bank-to-bank | Kenya interbank only |

**Practical recommendation for diaspora apps:** Use a rate aggregation approach (see
[remit-lens](https://github.com/gabrielmahia/remit-lens)) — compare mid-market rate + fee
across providers and deep-link to the provider for the actual transaction.
No public API gives you real-time executable rates for all corridors.

---

## True cost formula

```
true_cost_pct = (fee / send_amount * 100) + (1 - provider_rate / mid_market_rate) * 100
```

Use the ECB (Frankfurter API) or Open Exchange Rates for the mid-market rate.
`open.er-api.com/v6/latest/{currency}` is free for personal/low-volume use.

---

## What to tell your users

- "Zero fee" providers always have a wider spread — their cost is hidden in the rate
- Fastest isn't cheapest — Sendwave is ~10min, Wise is 1-3 days but often 1-2% cheaper
- M-Pesa delivery is available from most providers for Kenya specifically
- The most money reaches the family via Wise for large amounts, Sendwave for small amounts

---

*See [remit-lens](https://remit-lens.streamlit.app) — a live aggregator built from this research.*
