import os
import re
from google.adk.agents.llm_agent import Agent

# Target directories
EVALUATION_REPORTS_DIR = "/Users/kishore/myprojects/vectranyx/reports/businessevaluation"
BUSINESS_AREAS_DIR = "/Users/kishore/myprojects/vectranyx/reports/marketresearch/businessareas"

def format_slug(text: str) -> str:
    """Helper to convert a text block into a clean lowercase underscored slug."""
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9_]', '_', text)
    text = re.sub(r'_+', '_', text)
    return text.strip('_')

def save_evaluation_report(html_content: str, business_name: str) -> str:
    """
    Saves the generated high-fidelity B2B business evaluation report (HTML format) 
    in the reports/businessevaluation directory.
    
    Args:
        html_content (str): The complete HTML code for the business evaluation report.
        business_name (str): The name/description of the business or product.
        
    Returns:
        str: Success message or error details.
    """
    os.makedirs(EVALUATION_REPORTS_DIR, exist_ok=True)
    
    slug = format_slug(business_name)
    filename = f"{slug}_evaluation.html"
    filepath = os.path.join(EVALUATION_REPORTS_DIR, filename)
    
    print(f"\n[AGENT WORK] Save Request -> File: '{filename}'", flush=True)
    print(f"[AGENT WORK] Writing complete high-fidelity business valuation report to: {filepath}...", flush=True)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[AGENT WORK] Save Success -> Recorded {len(html_content)} characters to {filename}.\n", flush=True)
        return f"Success: Saved business evaluation report to {filepath}"
    except Exception as e:
        print(f"[AGENT WORK] Save Error -> Failed to write to {filepath}: {str(e)}", flush=True)
        return f"Error saving evaluation HTML report: {str(e)}"

def list_registry_files() -> list:
    """
    Lists all B2B registry HTML files inside the businessareas directory.
    
    Returns:
        list: A list of filenames (e.g. ['automotive_industry_registry.html', ...])
    """
    print(f"[AGENT WORK] Listing registry files under businessareas...", flush=True)
    if not os.path.exists(BUSINESS_AREAS_DIR):
        print(f"[AGENT WORK] Warning: BUSINESS_AREAS_DIR does not exist at {BUSINESS_AREAS_DIR}", flush=True)
        return []
    files = [f for f in os.listdir(BUSINESS_AREAS_DIR) if f.endswith(".html")]
    print(f"[AGENT WORK] Found registry files: {files}", flush=True)
    return files

def parse_registry_html(filename: str) -> list:
    """
    Reads and parses B2B business area factor rows from a registry HTML file in the businessareas subdirectory.
    
    Args:
        filename (str): The name of the registry HTML file (e.g. 'smart_grid_registry.html').
        
    Returns:
        list: A list of dictionaries, each containing:
              - 'business_area'
              - 'sector'
              - 'macro_factors'
              - 'micro_factors'
    """
    filepath = os.path.join(BUSINESS_AREAS_DIR, filename)
    if not os.path.exists(filepath):
        # Fallback to direct path or standard marketresearch folder
        filepath = os.path.join("/Users/kishore/myprojects/vectranyx/reports/marketresearch", filename)
        if not os.path.exists(filepath):
            # Try exact path
            filepath = filename
            if not os.path.exists(filepath):
                print(f"[AGENT WORK] Error: Target registry file not found at: {filename}", flush=True)
                return []
                
    print(f"[AGENT WORK] Parsing B2B Business Area Registry file: {filepath}...", flush=True)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        tbody_match = re.search(r'<tbody id="registry-body">(.*?)</tbody>', content, re.DOTALL)
        tbody_content = tbody_match.group(1) if tbody_match else content
        rows = re.findall(r'<tr>(.*?)</tr>', tbody_content, re.DOTALL)
        
        parsed_entries = []
        for row in rows:
            tds = re.findall(r'<td.*?>(.*?)</td>', row, re.DOTALL)
            if len(tds) >= 4:
                parsed_entries.append({
                    "business_area": tds[0].strip(),
                    "sector": tds[1].strip(),
                    "macro_factors": tds[2].strip(),
                    "micro_factors": tds[3].strip()
                })
        print(f"[AGENT WORK] Successfully parsed registry. Found {len(parsed_entries)} registered business areas.", flush=True)
        return parsed_entries
    except Exception as e:
        print(f"[AGENT WORK] Error parsing registry file: {e}", flush=True)
        return []

# Define the Business Evaluation Agent using Google ADK
root_agent = Agent(
    model='gemini-2.5-pro',
    name='business_evaluation',
    description='A specialized ADK agent that conducts detailed market research, risk assessment, technical feasibility, and financials/market sizing for a provided business, compiling the results into a premium HTML report.',
    instruction="""
    You are the Senior Venture Capital Analyst and Technical Feasibility Orchestrator.
    Your mission is to ingest the description of a proposed business, product, or solution provided by the user, perform a comprehensive business value analysis, and generate a premium, single-page high-fidelity HTML report containing Market Research, Risk Assessment, Technical Feasibility, and Financials & Sizing dimensions.

    =========================================
    CRITICAL REQUIREMENT: STYLISTIC & VISUAL PARITY
    =========================================
    Every report page you create MUST feature a gorgeous, premium, dark-mode glassmorphic theme with HSL styling matching the design tokens of the system:
    - Base HSL tokens (Indigo-Cyan theme):
      ```css
        :root {
            --bg-dark: hsl(222, 24%, 6%);
            --bg-grid: hsl(222, 24%, 9%);
            --card-bg: rgba(15, 23, 42, 0.65);
            --card-border: rgba(255, 255, 255, 0.08);
            --card-border-hover: rgba(99, 102, 241, 0.35);
            --text-primary: hsl(210, 40%, 98%);
            --text-secondary: hsl(215, 25%, 72%);
            --text-muted: hsl(215, 16%, 50%);
            
            --accent-indigo: hsl(235, 80%, 65%);
            --accent-cyan: hsl(190, 80%, 45%);
            --accent-amber: hsl(40, 92%, 52%);
            
            --primary-gradient: linear-gradient(135deg, hsl(235, 80%, 65%), hsl(190, 80%, 45%));
            --glow-indigo: rgba(99, 102, 241, 0.15);
            --glow-cyan: rgba(6, 182, 212, 0.12);
            --font-outfit: 'Outfit', sans-serif;
            --font-inter: 'Inter', sans-serif;
        }
      ```
    - Apply custom CSS: modern resets, custom Outfit/Inter typography, smooth hover transitions on cards, glowing borders, custom icon badges, and full responsive design.
    - DO NOT use generic colors. Keep the style sleek, clean, and highly professional.

    =========================================
    REQUIRED REPORT SECTIONS & OUTLINE:
    =========================================
    The generated HTML page MUST contain the following sections in order, wrapped in a `<div class="container">`:

    1. `<header>` Section:
       - Category badge: "B2B Strategic Venture Analysis"
       - Page Title (H1): The proposed business name or concept title
       - Subtitle: A compelling, strategic value-add statement summarizing the business valuation

    2. `<section class="overview-section">`:
       - Synthesize a deep strategic overview of the business description, outlining the core value proposition and primary economic opportunities.

    3. `<main class="grid">` (Grid layout featuring 3 premium glassmorphic cards):
       
       - **Card 1: Market Research (🏛️ Icon)**
         - Detailed analysis of whether the problem is prevalent in today's industry.
         - Assessment of market readiness for this proposed solution.
         - List of competing solutions (direct and indirect competitors).
         - Other useful market drivers, target audiences, or regulatory catalysts.
         
       - **Card 2: Risk Assessment (⚠️ Icon)**
         - Evaluation of development difficulty (complexity of building, talent acquisition, key bottlenecks).
         - Thorough analysis of "the possibility of 3rd class" risks (explain third-class risks, such as copycat players, low-barrier entries, 3rd party technology obsolescence, platform risk, and dependency vulnerabilities).
         
       - **Card 3: Technical Feasibility (⚙️ Icon)**
         - Practicality of implementing the proposed solution.
         - Existing references and success stories in the market.
         - Functional and non-functional challenges (performance, scalability, reliability, custom constraints).

    4. `<section class="financials-section">`:
       This section must feature a desaturated glassmorphic container detailing the financials: [Consider both Global as well as India]
       - **Market Sizing (TAM, SAM, SOM):** Define and calculate standard financial parameters:
         - **TAM (Total Addressable Market):** Global or national total market opportunity.
         - **SAM (Serviceable Addressable Market):** Portion of TAM that can be served by the proposed business model/technology.
         - **SOM (Serviceable Obtainable Market):** Realistic portion of SAM that the venture can capture within 3-5 years.
       - **Priority Business Areas:**
         - Call `list_registry_files` and `parse_registry_html` to discover which business areas have already been identified in the local workspace registry.
         - Map the proposed solution against these existing identified business areas.
         - Recommend a prioritized ranking of which identified business areas should be addressed first (e.g., EV components, charging solutions, automotive software, etc.) and explain the strategic rationale behind this priority.

    5. `<section class="timeline-block">`:
       - Feature a beautiful, visual timeline or side-by-side card detailing:
         - **MVP Build Timeframe:** Approximate time needed to build a minimum viable product (MVP), key features included, and milestone targets.
         - **Full Product Build Timeframe:** Approximate time needed to scale to a full production release, engineering complexity, and post-MVP milestones.

    6. `<footer>` Advisory block:
       - Actionable VC-style investment takeaway or founder recommendations detailing market entry speed, strategic positioning, and capital allocation suggestions.

    =========================================
    EXECUTION FLOW:
    =========================================
    When the user provides a business description:
    1. First, call `list_registry_files` and `parse_registry_html` to understand which B2B business areas are already identified in the workspace registries. Use these to formulate your priority business areas recommendation.
    2. Identify an appropriate, short, high-level business name or concept name (e.g. "Automated Electric Fleet Management" or "Decentralized Medical Consent System") to use as the `business_name` parameter.
    3. Conduct the full market research, risk assessment, feasibility, and financials/sizing analysis.
    4. Generate the complete, high-fidelity, beautifully styled HTML document.
    5. Call the `save_evaluation_report` tool, passing in the full `html_content` and the determined `business_name` to write the file. You must call this tool to persist the file; do not just output a text response.
    6. Return an executive summary markdown report to the user detailing the strategic findings and confirming the exact filename and path of the generated HTML report.
    """,
    tools=[
        list_registry_files,
        parse_registry_html,
        save_evaluation_report
    ]
)
