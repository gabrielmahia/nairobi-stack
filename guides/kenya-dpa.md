# Kenya Data Protection Act (2019) — Developer Guide

The Kenya Data Protection Act 2019 (DPA) mirrors GDPR in structure but is enforced
by the **Office of the Data Protection Commissioner (ODPC)** — a Kenyan body, not the EU.

This matters: Kenyan enforcement is light compared to GDPR, but registration is mandatory
and liability is real. Don't skip compliance because you think nobody is watching.

---

## Who it applies to

Any person or organisation that **determines the purpose and means** of processing
personal data of Kenyan citizens — regardless of whether you're based in Kenya.

Diaspora builders: if you collect personal data from Kenyan users, the DPA applies to you.

---

## Registration

**All data controllers and processors must register with the ODPC.**

- Register at: [odpc.go.ke](https://odpc.go.ke)
- Fee: KES 10,000 per year
- Renewal: annual
- Non-registration: fine of up to KES 3M or 2 years imprisonment

---

## What counts as personal data

Name, ID number, phone number, location data, M-Pesa transaction records, health data,
biometric data, online identifiers (IP addresses, cookies), employment records.

**Aggregate / anonymised data** that cannot be used to identify an individual is not personal data.

---

## Key obligations at a glance

**Consent:** Must be freely given, specific, informed, and unambiguous. A pre-ticked box is not consent.

**Purpose limitation:** Collect only what you need. Don't use data for a different purpose than stated.

**Storage limitation:** Don't keep data longer than necessary. Define and document your retention policy.

**Data subject rights — you must respond within 21 days:**
- Right to access (give them their data)
- Right to rectification (fix incorrect data)
- Right to erasure (delete their data)
- Right to portability (export in machine-readable format)
- Right to object (to processing for direct marketing, profiling)

**Breach notification:**
- Notify ODPC within 72 hours of becoming aware of a breach
- Notify affected persons within 7 days

---

## Practical compliance for a Streamlit app

```python
# In your app — collect consent explicitly before any data collection
import streamlit as st

if "consent_given" not in st.session_state:
    st.session_state.consent_given = False

if not st.session_state.consent_given:
    st.info("We collect your county and report details to improve water alerts for Kenya.")
    if st.button("I agree to data collection as described in our Privacy Policy"):
        st.session_state.consent_given = True
        st.rerun()
    st.stop()
```

---

## Cross-border data transfers

Personal data cannot leave Kenya unless:
1. The destination country has adequate data protection (EU, UK qualify; USA does not by default)
2. The transfer is covered by a contract with the data importer
3. The data subject explicitly consents

If you store Kenyan user data on US-based servers (AWS us-east-1, Streamlit Cloud),
technically you need either consent or contractual protection. In practice, add a
disclosure in your privacy policy.

---

## Resources

- [ODPC registration portal](https://odpc.go.ke)
- [DPA full text](http://kenyalaw.org/kl/fileadmin/pdfdownloads/Acts/2019/TheDataProtectionAct__No24of2019.pdf)
- Legal aid for compliance questions: [Kituo cha Sheria](https://kituochasheria.or.ke)
