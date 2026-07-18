# REI Skills

A centralized library of automation tools, scripts, and AI agent frameworks for real estate market intelligence. This repository is designed to be a community-driven resource for automated data collection, deal sorting, and lead qualification.

## Available Skills

| Skill | Description | Status |
| :--- | :--- | :--- |
| **[mls-web-scraper](mls-web-scraper/)** | Daily real estate listing scraper (Zillow/Redfin/Trulia/Compass). | Active |
| **[mls-deal-finder](mls-deal-finder/)** | API-driven real estate listing ingestion tool powered by paid Apify client data streams. | Active |
| **[distressed-lead-monitor](distressed-lead-monitor/)** | Public records monitoring utility pulling direct county pre-foreclosure, tax lien, and probate database entries via open-data API networks. | Active |
| **[property-comper](property-comper/)** | Automated ARV and comping engine using local market data. | Active |
| **[inbound-lead-agent](inbound-lead-agent/)** | Conversational AI agent prompt suite to pre-qualify motivated sellers. | Active |
| **[buy-box-filter](buy-box-filter/)** | Smart soft-filter that tags all property leads matching custom location, zip codes, and size metrics without deleting outlier data. | Active |
| **[deal-ranker](deal-ranker/)** | Advanced engine that calculates MAO and prioritizes deals into a 4-tier pipeline using a 100-point buy box scoring algorithm. | Active |

---

## 🛠️ Repository Philosophy
* **Modular Design:** Each skill is self-contained in its own directory with its own specific dependencies, code configuration patterns, and documentation.
* **Resilience:** All engineering scripts prioritize task persistence (the ability to resume after an error), soft-filtering defaults, and comprehensive execution logging.
* **Community-First:** Tools are provided "as-is" for educational and personal investment workflow optimization.

## ⚠️ Important Disclaimer
**Use these tools at your own risk.** 
* **Compliance and Terms of Service:** Automated data collection may violate the Terms of Service (ToS) of certain platforms. You are solely responsible for ensuring your usage complies with the policies of the platforms you query, local municipal laws, and marketing regulations.
* **No Support or Warranty:** These tools are provided completely free of charge. **There is absolutely no expectation of support, training, or technical assistance.** I cannot provide help with individual software setups, API debugging, local Python environments, or custom modifications. Please do not submit support requests or issues for individual usage help.

## How to Contribute
If you would like to add a new skill to the library:
1. Create a new folder in the root directory (e.g., `/new-skill-name`).
2. Include the necessary source code, a `requirements.txt`, and a dedicated `README.md` for that specific tool (ensuring no numeric tracking or skill numbers are utilized in the headers).
3. Open a **Pull Request** to have it indexed in the main table above.

---
*Created for the community.*
