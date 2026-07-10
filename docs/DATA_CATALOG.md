# Data Catalog — the index of the railroad

Machine-derived map linking each open dataset to the MCP server it backs and the
evaluation suite that measures agents using it. Source of truth: `catalog.json`.

**16 datasets · 16 on Kaggle · 10 wired to a server · eval via [kipimo](https://huggingface.co/spaces/gmahia/kipimo-leaderboard)**

| Dataset | HuggingFace | Kaggle | Backs server |
|---|---|---|---|
| kenya-civic-data | [HF](https://huggingface.co/datasets/gmahia/kenya-civic-data) | [Kaggle](https://www.kaggle.com/datasets/gmahia/kenya-civic-data) | `county-mcp` |
| swahili-civic-nlp | [HF](https://huggingface.co/datasets/gmahia/swahili-civic-nlp) | [Kaggle](https://www.kaggle.com/datasets/gmahia/swahili-civic-nlp) | `tafsiri-mcp` |
| kenya-agricultural-qa | [HF](https://huggingface.co/datasets/gmahia/kenya-agricultural-qa) | [Kaggle](https://www.kaggle.com/datasets/gmahia/kenya-agricultural-qa) | `kilimo-mcp` |
| kenya-legal-nlp | [HF](https://huggingface.co/datasets/gmahia/kenya-legal-nlp) | [Kaggle](https://www.kaggle.com/datasets/gmahia/kenya-legal-nlp) | `fomu-mcp` |
| kenya-mcp-data | [HF](https://huggingface.co/datasets/gmahia/kenya-mcp-data) | [Kaggle](https://www.kaggle.com/datasets/gmahia/kenya-mcp-data) | `reli-cli` |
| military-strategy-classics | [HF](https://huggingface.co/datasets/gmahia/military-strategy-classics) | [Kaggle](https://www.kaggle.com/datasets/gmahia/military-strategy-classics) | — |
| philosophy-classics-structured | [HF](https://huggingface.co/datasets/gmahia/philosophy-classics-structured) | [Kaggle](https://www.kaggle.com/datasets/gmahia/philosophy-classics-structured) | — |
| african-kingdoms-history | [HF](https://huggingface.co/datasets/gmahia/african-kingdoms-history) | [Kaggle](https://www.kaggle.com/datasets/gmahia/african-kingdoms-history) | — |
| east-africa-agricultural-pd | [HF](https://huggingface.co/datasets/gmahia/east-africa-agricultural-pd) | [Kaggle](https://www.kaggle.com/datasets/gmahia/east-africa-agricultural-pd) | `kilimo-mcp` |
| swahili-historical-corpus-pd | [HF](https://huggingface.co/datasets/gmahia/swahili-historical-corpus-pd) | [Kaggle](https://www.kaggle.com/datasets/gmahia/swahili-historical-corpus-pd) | `tafsiri-mcp` |
| east-africa-health-historical-pd | [HF](https://huggingface.co/datasets/gmahia/east-africa-health-historical-pd) | [Kaggle](https://www.kaggle.com/datasets/gmahia/east-africa-health-historical-pd) | `afya-mcp` |
| east-africa-legal-historical-pd | [HF](https://huggingface.co/datasets/gmahia/east-africa-legal-historical-pd) | [Kaggle](https://www.kaggle.com/datasets/gmahia/east-africa-legal-historical-pd) | `haki-ya-kazi-mcp` |
| africa-historical-maps-pd | [HF](https://huggingface.co/datasets/gmahia/africa-historical-maps-pd) | [Kaggle](https://www.kaggle.com/datasets/gmahia/africa-historical-maps-pd) | — |
| africa-open-climate-data | [HF](https://huggingface.co/datasets/gmahia/africa-open-climate-data) | [Kaggle](https://www.kaggle.com/datasets/gmahia/africa-open-climate-data) | `wapimaji-mcp` |
| africa-historical-photos-pd | [HF](https://huggingface.co/datasets/gmahia/africa-historical-photos-pd) | [Kaggle](https://www.kaggle.com/datasets/gmahia/africa-historical-photos-pd) | — |
| africa-expired-patents-pd | [HF](https://huggingface.co/datasets/gmahia/africa-expired-patents-pd) | [Kaggle](https://www.kaggle.com/datasets/gmahia/africa-expired-patents-pd) | — |

## How to use this

1. **Find data** for your domain (agriculture, health, legal, climate, civic).
2. **Find the server** it backs — `pip install <server>` exposes it to AI agents.
3. **Measure your agent** against [kipimo](https://github.com/gabrielmahia/kipimo).

Railroad, not train: any builder can go dataset → server → eval without the original authors.