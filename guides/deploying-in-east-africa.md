# Deploying in East Africa

Infrastructure choices that seem neutral in the West have real consequences
for users in Kenya. This guide covers the practical decisions.

---

## Where to host

**Streamlit Cloud (free tier)**  
Best for: civic tools, internal dashboards, small user bases.  
Latency: ~180-300ms from Nairobi (servers in US/EU). Acceptable for most tools.  
Limits: 1GB RAM, 1 app per account on free tier, sleeps after 7 days inactive.

**Railway / Render**  
Best for: FastAPI backends, REST APIs, always-on services.  
EU regions have ~150ms latency to Nairobi. Not ideal but workable.

**AWS Cape Town (af-south-1)**  
Best for: latency-sensitive apps. ~25ms from Nairobi.  
Catch: egress pricing from af-south-1 is high. Budget carefully.

**Google Cloud (europe-west1)**  
~120ms from Nairobi. GCP has the best peering with Kenyan ISPs of the major clouds.
Firebase Realtime Database has good sub-Saharan Africa performance.

---

## Mobile data costs

Your users may be on 50MB/day bundles. This changes every design decision:
- Avoid heavy JS frameworks (React bundles > 200KB are a real barrier)
- Cache aggressively (Streamlit does this reasonably well)
- Never autoplay video or audio
- Lazy-load images; use WebP over PNG

Safaricom Zero-Rating: Safaricom zero-rates certain educational and health sites.
If your civic tool qualifies, apply at developer.safaricom.co.ke.

---

## HTTPS everywhere

M-Pesa callback URLs must be HTTPS. Most platform-as-a-service providers
(Railway, Render, Streamlit Cloud) give you HTTPS automatically.
If you run your own server: certbot + nginx, 10 minutes.

---

## Working around Streamlit sleep

Streamlit Cloud apps sleep after 7 days of inactivity. Workaround:
- Add a GitHub Actions cron that pings your app URL weekly
- Or pay for Streamlit Community Cloud+ (currently $25/month)

The portfolio health check workflow in `gabrielmahia.github.io` already pings all
apps weekly, which prevents sleeping.

---

## Environment variables and secrets

Never put credentials in code. Platform patterns:

| Platform | Secret management |
|----------|------------------|
| Streamlit Cloud | Settings → Secrets (TOML format) |
| Railway | Variables tab in project settings |
| Render | Environment tab |
| GitHub Actions | Repository → Settings → Secrets |

For local development: `.env` file + `python-dotenv`. Never commit `.env`.
