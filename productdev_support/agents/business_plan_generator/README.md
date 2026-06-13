# Business Plan Generator Agent

The `business_plan_generator` is an AI agent built on the Google Agent Development Kit (ADK). It generates a complete investor-quality business plan in markdown format from a user-provided business concept, company description, or local file input.

The generated report is saved under `/reports/businessplans/` using a clean slug derived from the business name.

---

## 🏗️ Core Workflow

1. Ingests the user input or reads a local input file using the `read_input_file` tool.
2. Extracts the business name / concept name to use as the saved filename slug.
3. Builds a full business plan containing:
   - Executive Summary
   - Company Profile
   - Products & Services Description
   - Marketing & Sales Strategy
   - Operations Plan
   - Management Team
   - Financial Projections
   - Funding Request
   - Risk Management Plan
   - Dependencies
   - Team Structure & Expertise
4. Saves the report using `save_business_plan(markdown_content, business_name)`.
5. Returns an executive summary and saved file path to the user.

---

## 🛠️ Tool Integrations

* `read_input_file(filepath)` – Reads local business area or plan input files.
* `save_business_plan(html_content, business_name)` – Writes the generated HTML report to `/reports/businessplans/`.

---

## 🚀 Usage

```bash
cd /Users/kishore/myprojects/vectranyx/productdev_support/agents
adk run business_plan_generator
```

### Prompt Examples

* Provide natural language input directly:

```text
[user]: Provide business plan for Braking system manufacturing; Business name: ABC Business Area: Braking Systems; Business Sub-Area: Passenger Vehicles
[user]: Create a business plan for a premium telematics subscription service for EV fleet operators in India.
```
Note: When the agent is started with `adk run business_plan_generator`, it prints the sample prompt above to the console so you can copy/paste or edit it for the session.

* Provide a local file path:

```text
[user]: /Users/kishore/myprojects/vectranyx/braking_systems_sample_profile.md
```
