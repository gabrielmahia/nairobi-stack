# Mobile-First UX for Kenya

Building for Kenyan users requires resetting assumptions baked in by years of designing for San Francisco or London. This guide covers the realities of the Kenyan mobile market and how to design around them.

---

## The numbers (2024)

- **Smartphone penetration**: ~55% nationally; drops to ~30% in rural areas
- **Average data bundle**: 1GB/week at ~KES 50–100 — users are data-conscious
- **Primary connectivity**: 4G in Nairobi, Mombasa, Kisumu; 3G/2G in most county towns; EDGE/GPRS in rural areas
- **Screen size**: 5–6" budget Android dominates (Tecno, Infinix, Samsung A-series)
- **RAM**: 2–4GB on most devices; your PWA will be closed by the OS regularly
- **Battery**: Budget phones die by 2PM; many users ration app usage

---

## Design principles

### 1. Compress everything
Target 50KB total page weight on initial load. Images are the killer.

```python
# In Streamlit: avoid st.image() with large files
# Use optimised WebP, max 80KB per image
# For maps: load only when user requests, not on page load

# Python-side image compression
from PIL import Image
import io

def compress_for_mobile(image_path, max_kb=80):
    img = Image.open(image_path).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="WEBP", quality=65, optimize=True)
    if buf.tell() > max_kb * 1024:
        img = img.resize((img.width // 2, img.height // 2))
        buf = io.BytesIO()
        img.save(buf, format="WEBP", quality=55)
    return buf.getvalue()
```

### 2. Offline-first or SMS fallback
If your product requires connectivity to work at all, you've excluded 30–40% of your target users. Design a degraded mode:

- Cache critical data in localStorage or a service worker
- Provide SMS/USSD as an alternative access channel
- Show data timestamps so users know if they're looking at stale data

### 3. English + Kiswahili at minimum
English-only products signal "this is not for you" to a large portion of Kenyan users. Kiswahili translation increases trust, reduces drop-off, and broadens reach.

```python
STRINGS = {
    "en": {
        "water_alert": "Water stress HIGH in your area. Save water now.",
        "no_data": "No data available. Try again later.",
    },
    "sw": {
        "water_alert": "Msongo wa maji UKO JUU katika eneo lako. Hifadhi maji sasa.",
        "no_data": "Hakuna data. Jaribu tena baadaye.",
    },
}

def t(key: str, lang: str = "en") -> str:
    return STRINGS.get(lang, STRINGS["en"]).get(key, key)
```

### 4. Thumb-friendly tap targets
Minimum 48×48dp tap targets. Budget Android screens have inconsistent touch precision. Space buttons generously. Never place two tappable elements within 8dp of each other.

### 5. No bottom navigation
Bottom navigation bars work on iPhones with gesture navigation. On budget Androids with hardware home/back buttons, they collide. Use top nav or sidebar.

### 6. Reduce cognitive load for feature phone users
USSD sessions timeout after 180 seconds. Keep menus to 5–7 items. Never require typing on USSD — always offer numeric selections.

---

## Data-conscious patterns

### Show data cost estimates
```
Mzigo wa data: ~5KB
Estimated data usage: ~5KB
```

### Progressive disclosure
Don't load everything upfront. Load the list; load details only when a row is tapped.

### Explicit caching signals
Tell users when they're looking at cached data:
```
Last updated: 2 hours ago (no connection)
Ilisasishwa: saa 2 zilizopita (hakuna mtandao)
```

---

## Streamlit-specific considerations

- Use `@st.cache_data(ttl=3600)` aggressively — don't recompute on every rerun
- Avoid large DataFrames rendered with `st.dataframe()` — paginate or summarise
- Use `st.spinner()` for any operation >1s — users on 3G will wait longer than you expect in tests
- Test on your phone's hotspot, not your office WiFi

---

## Device testing

The minimum device matrix for a Kenya-targeted product:

| Device | Price range | Why |
|--------|------------|-----|
| Tecno Spark 10 (4GB RAM) | KES 10,000–15,000 | Most common budget Android |
| Samsung A15 | KES 18,000–22,000 | Step-up segment |
| iPhone (any recent) | KES 80,000+ | Urban professional segment |
| Feature phone (KaiOS) | KES 2,000–5,000 | Rural; access via USSD/SMS only |

BrowserStack has Kenyan device emulation. Physical testing with a Safaricom SIM is better.
