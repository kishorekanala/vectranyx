# Business Plan Evaluation (BPE) Agent Specification

## BPE Agent Overview:

BPE Agent analyzes business plan provided as input, evaluates it based on specified factors, provides report that contains evaluation scores for various factors and one overall score. The evaluation score(s) will be used by 

## BPE Agent 


This specification defines the auditable criteria, evaluation workflow, deliverables, scoring rubric, and evidence requirements for assessing investor- or lender-grade business plans. The spec is intended for use by the `business_plan_generator` and downstream evaluation agents to produce consistent, reproducible, and defensible recommendations (Fund / Do Not Fund).

## 1. Overview
- Purpose: Provide a structured, auditable framework to evaluate business plans across strategic, commercial, operational, financial, legal/regulatory, and ESG dimensions.
- Scope: Early-stage ventures through growth-stage SMEs whose plans include product/market descriptions, financial projections (3–5 years), and a funding ask.
- Output: A standardized evaluation report including: executive scorecard, auditable checklist, narrative findings, gap remediation plan, recommended funding decision and conditional terms.

## 2. Auditable Items (Primary Checklist)
Each item below must be evidenced, timestamped, and traceable (file, URL or cited data source).

1. Key Assumptions & Targets
   - List explicit assumptions (market size, growth rates, conversion, average selling price, unit economics, margin assumptions, customer acquisition cost (CAC), churn, retention).
   - Target dates for milestones (MVP, pilot, commercialization, break-even).
   - Source documentation for assumptions (market reports, competitor pricing, pilot results, LOIs).

2. Alignment with Market Trends
   - Trend fit analysis for business area and sub-area (demand drivers, regulatory tailwinds, technology adoption curves).
   - Comparative product-portfolio mapping vs. leading incumbents and new entrants.
   - Evidence: industry reports, public filings, trade publications, citation links.

3. Business Viability
   - TAM/SAM/SOM calculations, explicit methodology and data sources.
   - Competitive landscape (direct/indirect competitors) and defensibility analysis.
   - Customer validation: pilot outcomes, letters of intent (LOIs), pre-orders, reference customers.
   - Operational feasibility: manufacturing/fulfilment readiness, supplier maturity.

4. ESG Considerations
   - Carbon footprint exposure and materiality (scope 1/2/3 estimates where applicable).
   - Labor and supply-chain compliance: worker safety, modern slavery, material sourcing policies.
   - Governance: board structure, audit controls, conflicts of interest, disclosure practices.

5. Ethical Review
   - Alignment with ethical business practices and social impact statements.
   - Risks of harmful uses, bias, or negative externalities; mitigation controls.

6. National Security & Strategic Risk
   - Dual‑use technology exposure and export control risk.
   - Critical infrastructure dependencies and concentration by geography or supplier.
   - Foreign investment/ownership risk and related regulatory constraints.

7. Legal & Regulatory Compliance
   - Required licenses, permits, certifications and their status (applied/approved/expired).
   - IP: ownership, patents filed/granted, trade secrets, open-source dependencies and license compliance.
   - Potential IP infringement risks and clearance searches.

8. Exit Criteria & Repayment Clarity
   - Defined exit pathways (M&A, IPO, buyback) or loan repayment schedule and waterfall.
   - Illustrative capitalization table post-funding with dilution scenarios.

9. Timeline & Milestones
   - Realistic milestone schedule with dependencies and critical path.
   - Milestone acceptance criteria and measurable KPIs per milestone.

10. Team Competence vs. Scope
    - Key-person CVs, past outcomes, domain experience and functional coverage.
    - Identified capability gaps and hiring plan with timelines and cost estimates.

11. Funding Request & Use of Proceeds
    - Detailed breakdown of funding ask: capex, opex, GTM, working capital, contingency.
    - Funding tranche triggers and expected KPIs to unlock subsequent tranches.

12. Risk Management Plan
    - Enumerated material risks (market, technical, operational, regulatory, financial) and mitigations.
    - Contingency plans and stress scenarios.

13. Dependencies
    - Supplier and ecosystem dependencies (single-source suppliers, critical components, software platforms).
    - Data, cloud, and third-party integrations with SLAs and fallback options.

14. Team Structure & Expertise
    - Organizational chart, reporting lines, R&R for key functions (engineering, ops, sales, finance, legal).
    - Training, retention, and incentive mechanisms (equity, options plans).

15. Gaps & Recommendations
    - Actionable remediation steps, priority, estimated cost and timeline.

## 3. Additional Evaluation Dimensions
- Unit Economics & Sensitivity
  - Contribution margin, gross margin, CAC payback period, LTV/CAC, break-even analysis.
  - Sensitivity analysis across ±20–50% changes in price, volume, input costs, and conversion rates.

- Financial Projections Validation
  - P&L, cashflow, and balance sheet consistency checks, assumptions reconciliation, and top-down vs bottom-up alignment.
  - Liquidity runway under base and stress cases, covenant analysis, and debt servicing projections (DSCR, ICR).

- Scalability & Go-to-Market Readiness
  - Channel strategy, sales funnel metrics (lead gen cost, conversion rates), and partnerships.
  - Production scalability, lead times, and inventory policies.

- Supply Chain Resilience
  - Single-source risks, lead-time volatility, onshoring/offshoring exposure, customs/tariff sensitivities.

- Data Privacy & Cybersecurity
  - Data handling practices, compliance with GDPR/local privacy laws, security posture, incident response plan.

- Regulatory & Standards Compliance
  - Product certifications (CE, BIS, ISI, ISO), environmental clearances, sector-specific regulatory hurdles.

- Insurance & Liability Coverage
  - Product liability, directors & officers (D&O), professional indemnity and business interruption coverage.

## 4. Scoring & Decision Rules
- Score each major pillar (Strategic, Market, Team, Technical, Financial, Legal/Compliance, ESG) on a 0–5 scale.
- Weighting (suggested): Strategic 15%, Market 15%, Team 20%, Technical 15%, Financial 20%, Legal/Compliance 10%, ESG 5%.
- Compute weighted aggregate score and map to discrete recommendation:
  - 4.5–5.0: Strong Fund (Recommend terms, low conditions)
  - 3.5–4.49: Fund with Conditions (Milestone-based tranches)
  - 2.5–3.49: Consider (Requires remediation; limited or staged funding)
  - <2.5: Do Not Fund
- Provide rationale for the decision and list conditions required for funding (if any).

## 5. Evidence & Deliverables
- Mandatory documents to collect:
  - Full business plan and financial model (spreadsheet)
  - Founders’ CVs and corporate incorporation documents
  - IP evidence (patent filings, assignment agreements)
  - Customer evidence (LOIs, pilot reports, purchase orders)
  - Supplier agreements and material terms
  - Regulatory approvals or application receipts
- Deliverables from evaluation:
  - `evaluation_summary.md` (executive summary + recommendation)
  - `auditable_checklist.json` (structured checklist with evidence links)
  - `gap_remediation_plan.md` (action items with owners and ETA)

## 6. Workflow & Responsibilities
1. Ingest: Acquire business plan, projections, and supporting docs.
2. Triage: Quick risk screen to identify fatal regulatory or national security blockers.
3. Detailed Analysis: Deep-dive across pillars, run sensitivity tests, and verify assumptions.
4. Synthesis: Produce executive scorecard, narrative findings, and funding recommendation.
5. QA & Sign-off: Review by senior analyst and legal counsel (where applicable).
6. Store: Save evaluation artifacts to the project repository under `reports/businessevaluation/` and `reports/risk_evaluations/` as appropriate.

## 7. Automation & Integration Notes
- Where possible, automate data validation using:
  - Registry lookups (e.g., `reports/marketresearch/businessareas/`) for industry baselines.
  - Financial model sanity checks and formula validation.
  - IP and regulatory status lookups via external APIs or scripted scrapers (with consent).
- Produce machine-readable outputs (`auditable_checklist.json`) to drive downstream monitoring agents.

## 8. Templates & Checklists
- Include standard templates for:
  - `assumptions_register.xlsx` (assumption, value, source, confidence)
  - `milestone_template.md` (milestone, acceptance criteria, owner, due date)
  - `auditable_checklist.json` schema example (field definitions)

## 9. Security and Sensitivity
- Handle PII and sensitive financial information per company policies. Store sensitive artifacts in encrypted storage or access-controlled folders.

## 10. Next Steps
- Use this spec to adapt the `business_plan_generator` output so the agent also returns the `evaluation_summary.md` and `auditable_checklist.json` when requested.
- Optionally implement a scoring subagent to produce standardized scores and conditional term sheets.

---

Document version: 1.0
Author: Product / Evaluation Team
Date: 2026-06-13
