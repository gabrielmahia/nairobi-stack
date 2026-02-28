# Regulatory Landscape — Kenya Tech

Building a commercial product in Kenya means navigating several regulatory bodies. This guide summarises the most relevant ones for software products.

---

## Communications Authority of Kenya (CA)

**What they regulate:** Telecommunications, internet, broadcasting, postal services.  
**Relevant to you if:** You provide SMS/USSD services, operate a shortcode, run a VoIP service, or collect personal data via telecommunications channels.

### Shortcode registration
If you want your own SMS shortcode (e.g. 21600), you apply through the CA.
Shared shortcodes (via Africa's Talking, Safaricom bulk SMS) don't require direct CA registration — your provider handles it.

**Alphanumeric Sender ID:** Register through your SMS provider. They handle CA compliance.

---

## Central Bank of Kenya (CBK)

**What they regulate:** Financial services, payment systems, forex.  
**Relevant to you if:** You process payments, hold user funds, operate a remittance platform, or provide SACCO/credit services.

### Payment Service Provider licence
If your product processes payments (not just integrates with M-Pesa via a licensed PSP), you need a PSP licence from CBK.

**Key point:** Integrating with M-Pesa via Daraja does NOT make you a payment service provider. Safaricom is the PSP. You're a merchant using their API. No CBK licence required for standard Daraja integration.

If you're building: remittance service, forex exchange, mobile lending, digital wallet (holding user funds) — CBK licence required.

### Relevant regulations
- National Payment System Act 2011
- National Payment System Regulations 2014
- CBK Digital Credit Provider Regulations 2022 (digital lending)

---

## Capital Markets Authority (CMA)

**What they regulate:** Securities, derivatives, investment advisors, stockbrokers.  
**Relevant to you if:** Your product gives investment advice, manages portfolios, or facilitates securities transactions.

**Key point:** A trading terminal that analyses market data is not regulated by CMA. A product that executes trades on behalf of users, or manages their money, requires CMA licensing.

---

## Data Protection Act (Kenya, 2019)

Modelled on GDPR. Enforced by the **Office of the Data Protection Commissioner (ODPC)**.

### Key obligations

**Data controller registration:** If you process personal data of Kenyan citizens, you must register with the ODPC. Annual registration fee: KES 10,000.

**Lawful basis for processing:** You must have one of: consent, contract, legal obligation, vital interests, public interest, or legitimate interests.

**Data subject rights:** Users have the right to access, correct, delete, port, and object to processing of their personal data. You must have a mechanism to respond to these requests within 21 days.

**Cross-border transfers:** Personal data of Kenyan citizens cannot be transferred to countries without adequate data protection unless the user explicitly consents or a contract is in place.

### Practical compliance checklist
- [ ] Privacy policy published and linked from your app
- [ ] Consent collected before processing personal data
- [ ] Data retention policy defined (don't keep data longer than needed)
- [ ] ODPC registration submitted
- [ ] Data breach notification procedure: 72 hours to notify ODPC, 7 days for affected persons
- [ ] Contact point for data subject requests documented

---

## Kenya Revenue Authority (KRA)

**Relevant to you if:** You're generating revenue in Kenya.

If your platform collects payments in KES, you're subject to Kenyan tax:
- **Value Added Tax (VAT):** 16% on digital services above KES 5M annual threshold
- **Digital Service Tax (DST):** 1.5% of gross transaction value for digital marketplace operators
- **Corporate Income Tax / Withholding Tax:** If incorporated in Kenya

---

## Practical notes for diaspora builders

If you're incorporated in the USA but serving Kenyan users:
- ODPC registration is still required if you process Kenyan personal data
- DST may apply for Kenyan-origin transactions even for a foreign entity
- For payment processing, partner with a Kenya-incorporated entity or use a licensed PSP (Safaricom M-Pesa, Pesalink, etc.)

**Get a Kenyan lawyer for anything involving financial services.** The above is a summary, not legal advice.
