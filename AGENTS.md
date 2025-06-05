# AGENTS.md – Guide for Human & AI Contributors

> **Purpose**
> Establish a single, opinionated source‑of‑truth for *all* contributors—human **and** AI agents—working on the **Model‑Context‑Protocol‑101** repository.
> Our north‑star is a beginner‑friendly, insurance‑agent‑centric demo that showcases how the Model Context Protocol (MCP) can automate everyday tasks (e.g. commission calculations, lead triage, quote generation).

---

## 1  Mission & Scope

|                      |                                                                                                                                                             |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Project Goal**     | Teach MCP fundamentals *while* shipping a production‑quality reference workflow for independent insurance agents.                                           |
| **Primary Audience** |  • Experienced Python/JS devs new to MCP  <br> • Junior developers & boot‑camp grads  <br> • "No‑code" insurance professionals curious about AI automations |
| **Out‑of‑Scope**     | Deep NLP research, enterprise policy admin systems, or advanced DevOps. Keep it simple & pedagogical.                                                       |

---

## 2  Repository Overview

```
/
├─ notebooks/          ← Interactive demos & tutorials (Jupyter)
├─ src/                ← Python packages & utilities
├─ data/               ← Version‑controlled CSV samples (small)
├─ docs/               ← Architecture diagrams, GIFs, screenshots
├─ .github/            ← Issue templates, CI, & Codex tasks
└─ AGENTS.md           ← (you are here)
```

*Everything else should map cleanly into one of the folders above.*

---

## 3  Core Agent Personas

|  ID               |  Role                                       |  Primary Responsibilities                                                                                 |  Suggested Tools      |
| ----------------- | ------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------- |
| **DEV‑AGENT**     | Author & refactor Python / JS code          |  Write PEP‑8‑compliant, typed functions. Unit tests via **pytest**.                                       |  `src/`, `notebooks/` |
| **DOCS‑AGENT**    | Maintain README, tutorials, inline comments |  Explain concepts for *non‑technical* readers. Use Markdown best‑practices.                               |  `README.md`, `docs/` |
| **DATA‑AGENT**    | Curate CSV samples & synthetic datasets     |  Ensure realistic `insurance_sales.csv` with headers: *PolicyID, Premium, Commission, LeadSource, State*. |  `data/`              |
| **VISUALS‑AGENT** | Create diagrams, GIFs, screenshots          |  Use [Mermaid](https://mermaid.js.org/) for diagrams, `gifox` or `peek` for GIF capture.                  |  `docs/`              |
| **QA‑AGENT**      | Review PRs, run CI, validate notebooks      |  Check reproducibility, linting, and human‑readability.                                                   |  GitHub Actions       |

> *Every Pull Request should tag at least **one** relevant agent persona in the description so Codex tasks can auto‑route.*

---

## 4  Workflow in 5 Steps

1. **Open an Issue** – Use the template *Feature Request / Bug / Docs*.
   *Add ➕ labels:* `insurance-demo`, `good-first-issue`, etc.
2. **Draft a Codex Task** – Inside the issue, include a *Codex‑style* prompt (see §8).
3. **Fork → Branch → Commit** – Branch naming: `feat/<short-desc>` or `fix/<short-desc>`.
4. **Pull Request & Auto‑CI** – Lint (`ruff`), tests, and notebook execution must pass.
5. **Review & Merge** – Two approvals (human or AI) + green CI = merge into `main`.

---

## 5  Coding Guidelines

* **Language :** Python ≥ 3.10
* **Style :** PEP 8 via `ruff`, 100‑char lines, Google‑style docstrings.
* **Typing :** Use *typing* module & `mypy --strict` where feasible.
* **Functions :** Keep pure; side‑effects explicit.
* **Notebooks :** Top‑cell *TL;DR* summary, numbered sections, and a `Requirements` cell.

### Example Function Skeleton

```python
from __future__ import annotations

from typing import List


def calculate_commission(premiums: List[float], rate: float = 0.10) -> float:
    """Return total commission in USD.

    Args:
        premiums: A list of policy premium amounts.
        rate: Commission rate (defaults to 10%).

    Returns:
        Total commission rounded to 2 decimals.
    """
    return round(sum(premiums) * rate, 2)
```

---

## 6  Documentation Standards

1. **README First‑Run** ⇒ Provide copy‑&‑paste commands to spin up an MCP server & run the `quick_start.ipynb`.
2. **Tutorial Flow** ⇒ *Problem → Tool → Prompt → Output* rhythm.
3. **Glossary** ⇒ Keep a growing table for terms like *MCP*, *Codex*, *Lead*, *Premium*.
4. **Screenshots** ⇒ Place in `docs/img/`, optimized (<200 KB) & referenced with relative paths.
5. **Accessibility** ⇒ Alt‑text for every image & diagram.

---

## 7  Data Guidelines

* ✅ CSV samples ≤ 1 MB, anonymised, no PII.
* ✅ Use realistic ranges (e.g. premiums \$300–\$2 500).
* ✅ Document schema in `/data/README.md`.
* 🚫 No production client data.

---

## 8  Writing Great Codex Tasks

> Codex tasks live in GitHub Issues. They are short, *actionable*, and self‑contained.

```markdown
### 🎯 Task: Add Insurance Example to Notebook

**Context**
`quick_start.ipynb` shows profit calc only. We need an insurance‑centric demo.

**Acceptance Criteria**
- [ ] New function `calculate_commission` in `src/business_tools.py`.
- [ ] Notebook cell demonstrating commission on `insurance_sales.csv`.
- [ ] Markdown explainer (≤8 lines) for non‑technical readers.

**Agent**: DEV‑AGENT
```

*Keep tasks atomic—one outcome, one agent.*  Codex will fail gracefully if given a vague, multi‑step request.

---

## 9  Commit Message Convention

```
<type>: <short summary>

<body>

Refs: #issue-number
```

*Types:* `feat`, `fix`, `docs`, `refactor`, `test`, `chore`.

Example:

```
feat: add commission calc and insurance notebook demo

Implements core use‑case for independent agents.

Refs: #42
```

---

## 10  Visual Assets

* **Diagrams** – Author in Mermaid and commit the `.mmd` *and* exported `.svg`.
* **GIFs** – Max 30 s, 720p, loop once.

> *Store large binaries via Git LFS.*

---

## 11  License & Attribution

Unless stated otherwise, this repo is released under the **MIT License**.
If you borrow third‑party code or images, credit the source in the PR description & `ATTRIBUTIONS.md`.

---

## 12  Helpful Links

* 🔗 [OpenAI Codex Overview](https://platform.openai.com/docs/codex/overview)
* 🔗 [Introducing Codex (OpenAI Blog)](https://openai.com/index/introducing-codex/)
* 📖 [Model Context Protocol (MCP) Docs](https://github.com/faster-whisper/FastMCP)  *(placeholder)*
* 🎓 [Made‑for‑Agents Prompt Engineering Cheat‑Sheet](https://github.com/prompt‑engineering/cheatsheet)  *(placeholder)*

---

### ✨ House Rules Recap

1. **Clarity over cleverness.** Write code a junior dev can grok.
2. **One PR = One Purpose.** Small is beautiful.
3. **Explain *why*, not just *what*.** Especially for insurance pros skimming docs.
4. **Automate repeatables.** If it’s manual twice, script it.
5. **Empathy wins.** Assume readers lack your context—guide them.

Happy shipping! 🚀
