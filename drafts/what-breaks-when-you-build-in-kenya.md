---
title: "What Breaks When You Build Software in Kenya"
date: 2026-03-19
labels: [BUILD, AFRICA, ENGINEERING]
---

I've been building software for Kenyan users for long enough to have a list of assumptions I made early that turned out to be wrong. Not theoretical concerns — actual failures, in production, that caused real inconvenience to real people.

This is that list.

---

## The network is not a background fact

Every architecture decision I make starts with this: the network is intermittent, asymmetric, and expensive. Not occasionally. Routinely.

This means:

**Loading spinners are failures.** A loading spinner that persists for more than three seconds, on a page that requires a response from your server, will cause a user to close the tab and not return. This is not a UX preference. It is what actually happens.

**Timeouts must be explicit.** Every external API call in my apps has a `timeout` parameter. `urllib.request.urlopen(url, timeout=6)`. Not because I'm being careful — because I learned the hard way that an API that takes 30 seconds to respond on a slow connection will hold a Streamlit thread indefinitely, breaking the session for that user.

**Cache aggressively.** `@st.cache_data(ttl=3600)` on every external call, even data that changes hourly. The user who triggers an API call on a slow connection should not be the one who waits for it. The cache means only the first user pays that cost.

**Degrade gracefully.** Every live data function in my apps returns a hardcoded fallback when the API fails. The app still works. It just shows yesterday's data instead of today's. Users tolerate stale data. They do not tolerate broken pages.

---

## M-Pesa is not Stripe with an African name

If you approach M-Pesa as a payment processor with a different API, you will be confused by decisions that seem arbitrary. If you understand what M-Pesa actually is — a mobile money system built for users who may not have a bank account, operating primarily on feature phones over USSD — the decisions make sense.

What this means practically:

**The payment is the phone.** When a customer receives an STK Push, they are being asked to authorise a transaction from a mobile wallet, not from a card. They may not have the money. They may be in a matatu with poor signal. They may dismiss the prompt by accident. Design for all of these.

**Callbacks are unreliable.** Safaricom will attempt to deliver a callback when a transaction completes. They will retry if your server returns a non-200. But the retry mechanism is not guaranteed, and callbacks are occasionally simply lost. Build a status query fallback. Do not fulfill orders on callback receipt alone without idempotency protection.

**The reconciliation problem is real.** For any system processing significant volume, build a daily reconciliation job that queries transaction status independently of your callback log. Gaps exist.

**The sandbox is a lie.** In the Daraja sandbox, only one phone number triggers a successful flow. Response times are faster than production. Error messages are more readable. Your integration will work perfectly in the sandbox and fail in ways you did not anticipate on the first day in production. Test with a production account in sandbox mode using your actual shortcode as early as possible.

---

## The user's phone is not a smartphone

Kenya's smartphone penetration is high in Nairobi. Outside Nairobi, it is lower. Among the specific communities my tools serve — smallholder farmers, chama members in rural areas, county field officers — the median device is a low-end Android with 1GB RAM, running Chrome on 3G.

What this means:

**JavaScript bundle size matters.** Streamlit's default bundle is large. I load CSS with `st.markdown` and avoid heavy JavaScript widgets where I can.

**Font size is not a preference.** 16px minimum body font is not about aesthetics. Text smaller than 16px on a low-res mobile screen is genuinely hard to read. I check every interface at 360px width before shipping.

**Tap targets are not a preference either.** 44px minimum tap target height. Smaller than that and users are tapping the wrong thing, getting frustrated, and leaving.

**Single-column layouts are not a limitation.** They are the correct design for mobile. Desktop enhancements are additive. I design for the 360px screen first and then ask what the 1200px screen can do additionally, not the other way around.

---

## Language is an access control decision

Kiswahili is not a feature. It is a prerequisite for reaching a significant fraction of the communities my tools are designed for.

When I build a civic tool that surfaces government data — county budgets, MP attendance, drought alerts — and that tool only exists in English, I have made a decision about who is allowed to use it. That decision is usually not intentional. It is usually the result of building for the imagined user (educated, English-speaking, urban) rather than the actual user.

Every civic tool I build is bilingual from the start. Not as a translation layer added later — as a design constraint baked in from the beginning.

This also has a practical consequence for distribution: most technical writing about Kenyan civic tech is in English. The Kiswahili SEO surface is almost entirely uncontested. A single well-written Kiswahili article about a civic tool will rank faster and higher than anything in English, for the audience that matters most.

---

## Institutions do not update their APIs

The Kenya Gazette publishes constitutional notices. Their feed returns 403. Parliament.go.ke has a documented API. It returns 404. KNBS publishes economic statistics. Their server returns 503 frequently enough that I stopped relying on it.

This is not a technical problem. It is a procurement and maintenance problem. Government APIs in Kenya are often built by contractors whose contracts end. The API is built, delivered, and then not maintained because there is no budget line for maintenance.

The practical response: do not build a critical user-facing feature on top of a government API unless you have verified that it has been reliably available for at least six months and you have a fallback for when it goes down. Seed data plus graceful degradation is not a compromise — it is the correct architecture for this environment.

The COB RSS feed, NDMA feed, LSK RSS, and FIDA RSS all work reliably. They are maintained by organisations that have operational reasons to keep them running. The more institutionally stable the organisation, the more reliable their data infrastructure tends to be.

---

## The mental model shift

Most software is built for users who have reliable infrastructure, abundant data, and devices that were recent two years ago. Building for Kenya requires consciously inverting that default: start from constrained infrastructure, and let the unconstrained case be the bonus.

This is not a limitation on what you can build. It is a different design problem. The tools I've built are not simplified versions of tools that exist elsewhere. They are tools that exist for communities that have no equivalent elsewhere, built for the actual conditions those communities operate in.

That is the interesting engineering problem. Not how to build the most feature-rich dashboard, but how to build a system that works when the network drops, that reads correctly in Kiswahili, that loads in three seconds on a mid-range Android, and that a county officer can use without a manual.

---

*Gabriel Mahia builds decision infrastructure for East Africa. Engineering blog: [aikungfu.dev](https://aikungfu.dev). Portfolio: [gabrielmahia.github.io](https://gabrielmahia.github.io). The nairobi-stack engineering guides cover M-Pesa integration, USSD patterns, SMS infrastructure, Kenya DPA, and mobile-first UX in depth: [gabrielmahia.github.io/nairobi-stack](https://gabrielmahia.github.io/nairobi-stack).*
