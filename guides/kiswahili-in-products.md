# Kiswahili in Your Product

Kiswahili is co-official with English in Kenya. For most Kenyans outside Nairobi's
professional class, it's the language of trust — the one used with family, in church,
in the market. Products that speak Kiswahili feel like they belong.

---

## Don't just translate — localise

Translation: "Water stress level is CRITICAL"  
Localisation: "Maji yatapungua sana hivi karibuni" (Water will reduce greatly soon)

The first is accurate. The second is what a neighbour would say.

---

## Key terms for civic/agricultural/financial products

| English | Kiswahili | Notes |
|---------|-----------|-------|
| Water | Maji | |
| Flood | Mafuriko | Also used metaphorically |
| Drought | Ukame | ASAL context: kiangazi (dry season) |
| Farmer | Mkulima | pl. wakulima |
| County | Kaunti | Borrowed; widely used |
| Rights | Haki | Constitutional framing |
| Law | Sheria | |
| Savings group | Chama | Culturally specific — don't translate |
| Rotating savings | Mfuko wa pamoja | Or just "chama" |
| Mobile money | Pesa ya simu | Or just "M-Pesa" |
| Send money | Tuma pesa | |
| Budget | Bajeti | Borrowed |
| Government | Serikali | |
| Alert | Tahadhari | Warning/caution |
| Emergency | Dharura | |

---

## Code-switching

Urban Kenyan users — especially under 35 — code-switch constantly between English,
Kiswahili, and Sheng. Your UI doesn't need to match this exactly, but it should feel
natural. A registration form that says "Jina lako kamili" (Your full name) reads
more warmly than "Full name" even to bilingual users.

---

## SMS character limits and Kiswahili

Standard SMS is 160 ASCII characters. Extended characters (including some Kiswahili
diacritical marks) shift the encoding to UCS-2, which halves capacity to 70 chars.
In practice: avoid ï, ö, ü in SMS. Most Kiswahili doesn't use them anyway.

---

## Auto-detection

For bilingual apps, detect language from the user's input rather than asking:

```python
SW_MARKERS = {"ni","na","ya","wa","kwa","je","haki","sheria","maji","pesa","chakula"}

def detect(text: str) -> str:
    tokens = set(text.lower().split())
    sw_hits = len(tokens & SW_MARKERS)
    return "sw" if sw_hits >= 2 else "en"
```

This is sufficient for a two-language system. Don't use `langdetect` for Kiswahili —
its training data for Swahili is weak.

---

*See [Jibu](https://jibu.streamlit.app) — bilingual civic rights assistant built on this approach.*
