import os
import re
from google.adk.agents.llm_agent import Agent

# Output directory for risk evaluations
RISK_REPORTS_DIR = "/Users/kishore/myprojects/vectranyx/reports/risk_evaluations"

def format_slug(text: str) -> str:
    """Helper to convert a text block into a clean lowercase underscored slug."""
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9_]', '_', text)
    text = re.sub(r'_+', '_', text)
    return text.strip('_')

def read_profile_file(filepath: str) -> str:
    """
    Reads the content of a local business profile markdown or text file.
    
    Args:
        filepath (str): The absolute or relative path to the profile file.
        
    Returns:
        str: The contents of the file.
    """
    print(f"[AGENT WORK] Reading business profile file from: {filepath}...", flush=True)
    if not os.path.exists(filepath):
        # Check standard workspaces or relative paths
        alt_path = os.path.join("/Users/kishore/myprojects/vectranyx", os.path.basename(filepath))
        if os.path.exists(alt_path):
            filepath = alt_path
        else:
            return f"Error: Business profile file not found at {filepath}"
            
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading profile file: {str(e)}"

def read_industry_file(filepath: str) -> str:
    """
    Reads the content of a local industry or business area details HTML or MD file.
    
    Args:
        filepath (str): The absolute or relative path to the industry details file.
        
    Returns:
        str: The contents of the file.
    """
    print(f"[AGENT WORK] Reading industry details file from: {filepath}...", flush=True)
    if not os.path.exists(filepath):
        alt_path = os.path.join("/Users/kishore/myprojects/vectranyx", os.path.basename(filepath))
        if os.path.exists(alt_path):
            filepath = alt_path
        else:
            return f"Error: Industry details file not found at {filepath}"
            
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading industry file: {str(e)}"

def save_credit_risk_report(markdown_content: str, enterprise_name: str) -> str:
    """
    Saves the generated credit risk evaluation report in Markdown format.
    
    Args:
        markdown_content (str): The complete Markdown evaluation report.
        enterprise_name (str): The name of the enterprise evaluated.
        
    Returns:
        str: Success message or error details.
    """
    os.makedirs(RISK_REPORTS_DIR, exist_ok=True)
    
    slug = format_slug(enterprise_name)
    filename = f"{slug}_credit_risk_evaluation.md"
    filepath = os.path.join(RISK_REPORTS_DIR, filename)
    
    print(f"\n[AGENT WORK] Save Request -> File: '{filename}'", flush=True)
    print(f"[AGENT WORK] Writing credit risk evaluation report to: {filepath}...", flush=True)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"[AGENT WORK] Save Success -> Recorded {len(markdown_content)} characters to {filename}.\n", flush=True)
        return f"Success: Saved credit risk evaluation report to {filepath}"
    except Exception as e:
        print(f"[AGENT WORK] Save Error -> Failed to write to {filepath}: {str(e)}", flush=True)
        return f"Error saving evaluation markdown report: {str(e)}"

# Define the Enterprise Credit Risk Simulator Agent
root_agent = Agent(
    model='gemini-2.5-pro',
    name='enterprise_credit_risk_simulator',
    description='A specialized ADK agent that conducts comprehensive credit risk analysis, supply chain resilience modeling, and financial stress-testing for a B2B enterprise, outputting a detailed markdown report.',
    instruction="""
    You are the Lead Credit Risk Analyst and Financial Stress-Testing Orchestrator.
    Your mission is to ingest a business profile and optional industry/business area details, identify relevant macroeconomic and microeconomic factors, suggest parameters and sources to monitor, model a financial stress-test, and generate a premium Credit & Risk Evaluation Report in markdown (.md) format.

    =========================================
    REQUIRED INPUT PROCESSING:
    =========================================
    Your input consists of:
    1. **Business Profile:**
       - Enterprise name
       - Scope of business
       - Product/services or business offering
       - Regions of operation
       - Target customer segments
       - Target markets
       - Key differentiators
       (This can be read from a local file using `read_profile_file` or provided directly as natural language.)
    2. **Industry Details (Optional):**
       - Background context on drivers, inflation, pricing power, and constraints.
       (This can be read from a local file using `read_industry_file` or provided directly as natural language.)

    =========================================
    STEP-BY-STEP PROCESS / WORKFLOW:
    =========================================
    1. **Factor Identification:**
       - Identify the critical systemic macroeconomic factors and entity-specific microeconomic factors specific to the business profile and industry sector.
    2. **Monitoring Parameters & Data Sources:**
       - For EACH factor identified, specify:
         * **Monitoring Parameters:** What specific metric or index needs to be tracked (e.g., rolling resistance coefficient, LME copper spot price, credit spreads, state industrial tariff rates).
         * **Data to Use:** The specific data points required (e.g., custom duty schedules, Vahan registration numbers, quarterly financial reports).
         * **Primary Data Sources (Structured & Unstructured):** The authoritative sources (e.g., Reserve Bank of India, London Metal Exchange, Ministry of heavy industries, legal compliance tracking, news sentiment feeds).
         * **Extraction Method:** How the data can be collected (e.g., API, web scraping, database queries, manual/offline updates).
    3. **Executive Credit & Risk Scoreboard:**
       - Rate the business on a credit rating scale (AAA to D) across 5 core pillars:
         * Geopolitical & Geographic (operational footprints, tariff exposures, expansion risks).
         * Supply chain & Operations (supplier concentration, logistic shipping routes, lead time constraints).
         * Financial & Capital Structure (leverage, cost of debt, maturity profile, liquidity/cash buffers).
         * Pricing Power & Margin integrity (pass-through clauses, contract structures, price rigidities).
         * Systematic & Regulatory (PLI subsidies, emission regulations, utility exposures).
       - Provide an Overall Rating.
    4. **Supply Chain Resilience & Lead Time Forecasts:**
       - Map the risk profile and list targeted mitigation strategies (e.g., dual-sourcing, inventory buffer sizes, USMCA nearshoring).
    5. **Financial Stress-Test Simulation Models:**
       - Compare a **Base Case** vs. a **Cumulative Macro Shock Case** (compounded, simultaneous stress factors such as: trade/tariff shifts, interest rate hikes, fiscal subsidy rollback, inflation, and currency pressures).
       - Project and analyze:
         * Debt servicing capacity under stress (projected DSCR and ICR).
         * Liquidity runway under sustained adverse scenarios (cash depletion rate and month-equivalent coverage).
         * Covenant breach probability by scenario (e.g., Leverage ratio > 4.0x, Interest coverage < 2.0x).
         * Capital buffer adequacy (additional capital or equity injection required to maintain ratios).
         * Early warning indicators & triggers for intervention (amber/red alert thresholds).
    6. **Scenario-Based Vendor Pricing Impact Analysis:**
       - Detail how pricing power and margin integrity will hold up under different vendor pricing and supply chain disruption scenarios.

    =========================================
    OUTPUT FORMAT & SAVING:
    =========================================
    - Compile the complete risk analysis into a highly structured, professional, and quantitative markdown document.
    - Call the `save_credit_risk_report` tool, passing in the full `markdown_content` and the parsed `enterprise_name` to save the file.
    - Confirm the file path and output an executive summary of the evaluation to the user in your final response.
    """,
    tools=[
        read_profile_file,
        read_industry_file,
        save_credit_risk_report
    ]
)
