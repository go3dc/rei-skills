# Property Comper

An agent-stack-agnostic valuation engine that automatically discovers comparable sales ("comps"), analyzes recent market transactions, documents selection rationales, and calculates After Repair Values (ARV) for target properties.

## Flexible API Integration
This module dynamically adapts to whatever API or model provider your agent stack uses (such as Hermes Agent running Anthropic Claude Haiku, OpenRouter, or OpenAI). It automatically checks environment variables (`ANTHROPIC_API_KEY`, `ANTHROPIC_TOKEN`, `OPENROUTER_API_KEY`, `OPENAI_API_KEY`, or `OPENAI_BASE_URL`) at runtime.

## Key Features
* **Autonomous Comp Discovery:** Eliminates manual comp searches by instructing AI models to retrieve comparable sales matching location, age, layout, and square footage criteria.
* **Selection Rationale Documentation:** Every selected comp includes a clear justification detailing why it served as an effective market benchmark.
* **Per-Project Markdown & CSV Reports:** Writes standalone report files (`comps_<address>.md` and `comps_<address>.csv`) directly to the `reports/` folder for every property.
* **Master Pipeline Synchronization:** Updates the `arv` field across the dataset and outputs `comped_deals.csv` for downstream consumption by `buy-box-filter` and `deal-ranker`.

## Setup & Execution
1. Copy `config.example.py` to `config.py`.
2. Configure search radius, max sale age, and report output preferences in `config.py`.
3. Launch the engine:
   ```bash
   python main.py
