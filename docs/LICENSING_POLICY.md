# Licensing policy

Owner: Gabriel Mahia · Decided 2026-11-25 · Replaces the earlier rule that defaulted every repository to CC BY-NC-ND 4.0.

## The goal

The work should be useful, should earn its author credit, and should keep its commercial value. One licence cannot do all three, so each repository gets the licence that fits what it is for.

## Three tiers

| Tier | Licence | What goes here | Why |
|---|---|---|---|
| **Build on it** | **MIT** | SDKs, CLIs, MCP servers, protocols, test doubles, evaluation harnesses, kits, skills and prompt libraries, and thin reference or demo apps | These only matter if other people depend on them. Package indexes, the MCP Registry, companies and governments all expect a standard open-source licence. MIT requires every copy to keep the copyright notice, which preserves credit. |
| **Use it, don't sell it** | **PolyForm Noncommercial 1.0.0** | Flagship end-user products with commercial or partnership value: budget-sentinel, floodwatch-kenya, landwatch, mazao-intel, remit-lens, sacco-scout, remit-ai, afya-ai, diaspora-ai, taarifa-ai, jumuia, hela, jibu, kazi-ai, shule-ai, openresilience | Free for personal, research and educational use, and for charities, public research, public health and safety organisations and **government institutions**. They may also modify it for their own use. Commercial use needs a licence from the owner: contact@aikungfu.dev. |
| **Private** | No public licence (all rights reserved) | Private repositories: the foundry, the evolution lab, ops tooling, research | These are not distributed. |

Data follows its source. Our own datasets use CC BY 4.0 (for example, Kipimo's tasks), and third-party data keeps its original licence.

## Why PolyForm Noncommercial instead of CC BY-NC-ND

- Creative Commons recommends against using its licences for software. PolyForm licences were written by lawyers specifically for software.
- NoDerivatives meant that even a county government fixing a bug for its own use was in a grey area. PolyForm Noncommercial allows noncommercial changes, which makes the tools usable by the public sector while still keeping commercial rights with the owner.
- The Required Notice line has to travel with every copy, so credit is kept.

## Rules

1. **Attribution.** Every LICENSE names Gabriel Mahia. MIT repositories ask users to credit the project and link back, and keep a `CITATION.cff` where one exists.
2. **Moving a repository to a more open tier is fine.** Moving one to a more restrictive tier only affects future versions, because code already released under MIT stays MIT. Choose the tier before the first release.
3. **Consistency.** The LICENSE, `pyproject.toml` (SPDX expression), `CITATION.cff`, README badge and footer, NOTICE, and in-app captions must all name the same licence.
4. **Third-party code** keeps its own licence. Check dependency licences before adding a dependency.
5. **Contributions.** Repositories that accept contributions need a clear statement of how contributions are licensed. A contributor agreement is required before external code goes into a PolyForm repository, so commercial licences can still be granted.
6. **Changes to this policy** are made by the owner. Agents apply it but do not change it.

Not legal advice. Get a qualified lawyer's review before signing a commercial licence or partnership agreement under this policy.
