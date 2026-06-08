# Business Evaluation Agent

The `business_evaluation` agent is an AI agent built on the Google Agent Development Kit (ADK). It ingests a natural language description of a business, product, or solution, performs an in-depth venture-capital-style strategic analysis, and generates a premium, high-fidelity business valuation report.

The generated report is saved as an HTML file inside the `/reports/businessevaluation/` folder, utilizing a modern, desaturated dark HSL glassmorphism theme.

---

## 🏗️ Core Workflow

```mermaid
graph TD
    Input[📄 Business Description Prompt] -->|1. Ingest| Agent[⚙️ Business Evaluation Agent]
    Agent -->|2. Scan Registries| Scan[📋 Check Existing Business Areas]
    Scan -->|3. Analyze| Evaluation[🧠 Strategic VC Review]
    Evaluation -->|4. Evaluate MR| MR[🏛️ Market Research]
    Evaluation -->|5. Evaluate Risk| Risk[⚠️ Risk Assessment]
    Evaluation -->|6. Evaluate Feasibility| Feas[⚙️ Technical Feasibility]
    Evaluation -->|7. Evaluate Financials| Fin[📊 TAM / SAM / SOM & Prioritization]
    MR -->|8. Compile Report| Report[✨ High-Fidelity HSL HTML Page]
    Risk -->|8. Compile Report| Report
    Feas -->|8. Compile Report| Report
    Fin -->|8. Compile Report| Report
    Report -->|9. Save| SaveFile[💾 Save Report to reports/businessevaluation/]
    
    style Input fill:#e0f7fa,stroke:#00acc1,stroke-width:1px;
    style Agent fill:#fff3e0,stroke:#ff9800,stroke-width:2px;
    style SaveFile fill:#ffebee,stroke:#c62828,stroke-width:2px;
```

1. **Ingestion:** Receives the business description from the user prompt.
2. **Registry Scanning:** Calls workspace tools to identify previously registered business areas in the project environment.
3. **Analysis:** Evaluates the concept across four major pillars:
   - **Market Research:** Examines problem prevalence, market readiness, target audiences, and competing solutions.
   - **Risk Assessment:** Investigates development complexity, bottlenecks, and "the possibility of 3rd class" (copycats, platform lock-in, low-barrier competition, 3rd party dependency/obsolescence risks).
   - **Technical Feasibility:** Investigates implementation practicality, functional/non-functional challenges, market references, and build timelines for MVP vs Full Product.
   - **Financials & Sizing:** Details TAM, SAM, and SOM metrics, and ranks existing identified business areas to target for initial integration.
4. **Report Compilation:** Synthesizes the findings into a sleek, responsive HTML document.
5. **Saving:** Automatically names the output using the slug format `[business_name]_evaluation.html` and saves it to `/reports/businessevaluation/`.

---

## 🛠️ Tool Integrations

* **`list_registry_files()`**: Discover existing B2B registry files inside the `/reports/marketresearch/businessareas/` directory.
* **`parse_registry_html(filename)`**: Extract registered business area and sector details to cross-reference priority areas.
* **`save_evaluation_report(html_content, business_name)`**: Saves the generated HTML content as a standalone, styled file under `/Users/kishore/myprojects/vectranyx/reports/businessevaluation/`.

---

## 🚀 Usage

Navigate to the `agents` folder and invoke the agent using the ADK CLI:

```bash
cd /Users/kishore/myprojects/vectranyx/productdev_support/agents
adk run business_evaluation
```

### Prompt Example:

```text
[user]: Evaluate a business idea for a decentralized logistics network in India that connects independent truckers with cargo shippers through real-time spot auctioning, eliminating broker margins and optimizing fleet utilization.
```

---

## 📂 Directory Layout

* [agent.py](file:///Users/kishore/myprojects/vectranyx/productdev_support/agents/business_evaluation/agent.py): Core ADK agent definition, registry parsing, and HTML saving tools.
* [.env](file:///Users/kishore/myprojects/vectranyx/productdev_support/agents/business_evaluation/.env): API credentials and environment configurations.
* [dotenvexample](file:///Users/kishore/myprojects/vectranyx/productdev_support/agents/business_evaluation/dotenvexample): Example environment configurations template.
