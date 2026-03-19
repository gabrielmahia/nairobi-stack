# Live Data APIs for East Africa Builders

The APIs below are **free, keyless, and production-reliable**. All are used across the nairobi-stack app suite. Each entry includes TTL recommendation, graceful fallback pattern, and real usage example.

---

## Exchange rates — open.er-api.com

**URL:** `https://open.er-api.com/v6/latest/{BASE_CURRENCY}`  
**Key required:** No  
**Rate limit:** None (fair use)  
**Update frequency:** Daily  
**TTL recommendation:** 3600s (1 hour)

```python
@st.cache_data(ttl=3600)
def fetch_kes_rate():
    try:
        with urllib.request.urlopen(
            "https://open.er-api.com/v6/latest/USD", timeout=6
        ) as r:
            d = json.loads(r.read())
        return {"kes": round(d["rates"]["KES"], 2), "live": True}
    except Exception:
        return {"kes": 129.0, "live": False}   # hardcoded fallback
```

**Corridors available:** All ISO 4217 currencies. USD→KES, GBP→KES, EUR→KES, CAD→KES, AED→KES all confirmed working.  
**Use in:** Remittance comparison, SACCO real return (dividend minus inflation), diaspora giving, chama FX context.

---

## Weather & rainfall — Open-Meteo

**URL:** `https://api.open-meteo.com/v1/forecast`  
**Key required:** No  
**Rate limit:** 10,000 calls/day (generous)  
**Update frequency:** Hourly  
**TTL recommendation:** 3600s

```python
@st.cache_data(ttl=3600)
def fetch_county_weather(lat: float, lon: float, county: str):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&daily=precipitation_sum,temperature_2m_max"
        f"&current=precipitation,temperature_2m,relative_humidity_2m"
        f"&forecast_days=7&timezone=Africa%2FNairobi"
    )
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            d = json.loads(r.read())
        precip_7d = d["daily"]["precipitation_sum"]
        return {
            "precip_7d":    precip_7d,
            "precip_total": round(sum(precip_7d), 1),
            "drought_signal": sum(precip_7d) < 5,   # < 5mm/week
            "flood_signal":   sum(precip_7d) > 80,  # > 80mm/week
            "live": True,
        }
    except Exception:
        return {"live": False}
```

**All 47 county coordinates** are in the [openresilience repo](https://github.com/gabrielmahia/openresilience/blob/main/app.py) — copy the `KENYA_COUNTIES` dict.  
**Useful parameters:** `precipitation_sum`, `temperature_2m_max`, `et0_fao_evapotranspiration` (evapotranspiration — drought signal), `weathercode`.  
**Use in:** Flood risk platforms, drought monitoring, agricultural price forecasting (rain → crop supply signal).

---

## NDMA drought alerts — ndma.go.ke RSS

**URL:** `https://www.ndma.go.ke/feed/`  
**Key required:** No  
**Update frequency:** When NDMA publishes (typically weekly during drought periods)  
**TTL recommendation:** 7200s (2 hours)

```python
@st.cache_data(ttl=7200)
def fetch_ndma_alerts():
    try:
        req = urllib.request.Request(
            "https://www.ndma.go.ke/feed/",
            headers={"User-Agent": "your-app/1.0"},
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            root = ET.fromstring(r.read())
        items = []
        for item in root.findall(".//item")[:5]:
            items.append({
                "title":   item.findtext("title", "").strip(),
                "link":    item.findtext("link",  "").strip(),
                "date":    item.findtext("pubDate", "").strip()[:16],
                "summary": re.sub(r"<[^>]+>", "", item.findtext("description","")).strip()[:180],
            })
        return items
    except Exception:
        return []
```

**Signal value:** NDMA publishes monthly drought updates by county. "Drought conditions worsening" correlates with food price spikes 4–6 weeks later (useful for JuaMazao/mazao-intel).  
**Use in:** Flood/drought platforms, food price tools (leading indicator), macro analysis (commodity pressure).

---

## Controller of Budget — cob.go.ke RSS

**URL:** `https://cob.go.ke/feed/`  
**Key required:** No  
**Update frequency:** When COB publishes (typically monthly or event-driven)  
**TTL recommendation:** 3600s

```python
@st.cache_data(ttl=3600)
def fetch_cob_live():
    try:
        req = urllib.request.Request(
            "https://cob.go.ke/feed/",
            headers={"User-Agent": "your-app/1.0"},
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            root = ET.fromstring(r.read())
        return [
            {
                "title":   item.findtext("title","").strip(),
                "link":    item.findtext("link", "").strip(),
                "date":    item.findtext("pubDate","").strip()[:16],
                "summary": re.sub(r"<[^>]+>","", item.findtext("description","")).strip()[:180],
            }
            for item in root.findall(".//item")[:5]
            if item.findtext("title","").strip()
        ]
    except Exception:
        return []
```

**What it contains:** Budget implementation reviews, county compliance alerts, IBEC session outcomes, exchequer approval updates.  
**Use in:** Budget tracker apps, CDF watchdog tools, chama apps where members are county employees (salary compliance signal).

---

## World Bank Open Data — api.worldbank.org

**URL:** `https://api.worldbank.org/v2/country/KE/indicator/{CODE}?format=json&mrv=1`  
**Key required:** No  
**Update frequency:** Annual (most indicators)  
**TTL recommendation:** 86400s (24 hours)  
**Important:** Use `timeout=15` — the API is occasionally slow.

```python
@st.cache_data(ttl=86400)
def fetch_kenya_macro():
    INDICATORS = {
        "FP.CPI.TOTL.ZG":    ("Inflation", "%"),
        "NY.GDP.PCAP.CD":    ("GDP per capita", "USD"),
        "SL.UEM.TOTL.ZS":   ("Unemployment", "%"),
        "SI.RMT.COST.OB.ZS": ("Remittance cost to KE", "%"),
    }
    results = {}
    for code, (label, unit) in INDICATORS.items():
        try:
            url = f"https://api.worldbank.org/v2/country/KE/indicator/{code}?format=json&mrv=1"
            with urllib.request.urlopen(url, timeout=15) as r:
                d = json.loads(r.read())
            entries = [e for e in (d[1] if len(d)>1 else []) if e.get("value")]
            if entries:
                results[code] = {
                    "label": label, "unit": unit,
                    "value": round(entries[0]["value"], 2),
                    "year":  entries[0].get("date","?"),
                }
        except Exception:
            pass
    return results
```

**Key indicators for East Africa:**

| Indicator code | What it measures | Use case |
|---|---|---|
| `FP.CPI.TOTL.ZG` | Inflation (CPI %) | SACCO real return: dividend% minus inflation% |
| `NY.GDP.PCAP.CD` | GDP per capita (USD) | Economic context |
| `SL.UEM.TOTL.ZS` | Unemployment (%) | Labour market context |
| `SL.UEM.1524.ZS` | Youth unemployment (%) | Education/career tools |
| `SE.SEC.ENRR` | Secondary school enrolment | Education platforms |
| `SI.RMT.COST.OB.ZS` | Avg remittance cost to Kenya | Remittance comparison (5.26%, G20 target: 3%) |
| `BX.TRF.PWKR.DT.GD.ZS` | Remittances as % of GDP | Diaspora impact context |

---

## Kenya legal bodies — RSS feeds

Three Kenyan legal organisations publish reliable RSS:

| Organisation | URL | Update cadence |
|---|---|---|
| Law Society of Kenya | `https://www.lsk.or.ke/feed/` | Weekly |
| FIDA Kenya | `https://fidakenya.org/feed/` | Monthly |
| Judiciary Kenya | `https://judiciary.go.ke/feed/` | Weekly |

```python
@st.cache_data(ttl=7200)
def fetch_legal_updates():
    sources = {
        "LSK":       "https://www.lsk.or.ke/feed/",
        "FIDA Kenya": "https://fidakenya.org/feed/",
        "Judiciary":  "https://judiciary.go.ke/feed/",
    }
    all_items = []
    for source, url in sources.items():
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "your-app/1.0"})
            with urllib.request.urlopen(req, timeout=8) as r:
                root = ET.fromstring(r.read())
            for item in root.findall(".//item")[:3]:
                title = item.findtext("title","").strip()
                if title:
                    all_items.append({
                        "source": source,
                        "title":  title,
                        "link":   item.findtext("link","").strip(),
                        "date":   item.findtext("pubDate","").strip()[:16],
                    })
        except Exception:
            pass
    return sorted(all_items, key=lambda x: x["date"], reverse=True)[:8]
```

---

## WFP Kenya food prices — HDX

**URL:** `https://data.humdata.org/dataset/wfp-food-prices-for-kenya`  
**CSV direct:** `https://data.humdata.org/datastore/...` (see [mazao-intel app.py](https://github.com/gabrielmahia/mazao-intel/blob/main/app.py) for exact URL)  
**Key required:** No  
**Update frequency:** Monthly  
**TTL recommendation:** 21600s (6 hours)

Covers: maize, beans, wheat flour, cooking oil, sugar across 50+ Kenyan markets.  
License: CC BY IGO 3.0 — attribution required.

---

## Graceful fallback pattern (standard)

All live data functions in the nairobi-stack follow this contract:

```python
@st.cache_data(ttl=3600)
def fetch_something():
    try:
        # ... real API call ...
        return {"value": result, "live": True}
    except Exception:
        return {"value": FALLBACK_VALUE, "live": False}
```

**Rules:**
1. Never raise — always return a typed value
2. Return `{"live": True/False}` so UI can label the source
3. Use `st.cache_data` with explicit TTL — don't hit APIs on every rerender
4. Set `timeout=` explicitly — default is no timeout, which hangs Streamlit on cold starts
5. Include `User-Agent` header — some servers block requests without one

**UI labelling:**
```python
result = fetch_something()
if result["live"]:
    st.caption("📡 Live · source-name · updated every Xh")
else:
    st.caption("📋 Fallback · last known value")
```

---

*Part of the [nairobi-stack](https://github.com/gabrielmahia/nairobi-stack) East Africa engineering guide.*
