import os
import re
from google.adk.agents.llm_agent import Agent

# Target directory for generated and updated HTML files in this phase
MARKET_RESEARCH_DIR = "/Users/kishore/myprojects/vectranyx/reports/marketresearch/businessareaanalysis"
BUSINESS_AREAS_DIR = "/Users/kishore/myprojects/vectranyx/reports/marketresearch/businessareas"

def format_slug(text: str) -> str:
    """Helper to convert a text block into a clean underscored slug."""
    text = text.strip().lower()
    # replace any non-alphanumeric character with underscore
    text = re.sub(r'[^a-z0-9_]', '_', text)
    # compress multiple underscores into a single underscore
    text = re.sub(r'_+', '_', text)
    return text.strip('_')

def save_html_page(html_content: str, business_area: str, sector: str) -> str:
    """
    Saves the generated B2B market research HTML page in the businessareaanalysis directory,
    automatically generating a standard combined filename in the format: [business_area]___[sector].html
    
    Args:
        html_content (str): The complete HTML code matching air_gas_draft_systems.html structure.
        business_area (str): The B2B business area name (e.g. 'Advanced Logic & Memory Wafer Fabrication').
        sector (str): The primary industry sector (e.g. 'Semiconductor Fabrication / High-Tech Manufacturing').
        
    Returns:
        str: Success message or path of the file, or an error.
    """
    os.makedirs(MARKET_RESEARCH_DIR, exist_ok=True)
    
    comp_slug = format_slug(business_area)
    sect_slug = format_slug(sector)
    filename = f"{comp_slug}___{sect_slug}.html"
    filepath = os.path.join(MARKET_RESEARCH_DIR, filename)
    
    print(f"\n[AGENT WORK] Save Request -> File: '{filename}'", flush=True)
    print(f"[AGENT WORK] Writing complete high-fidelity glassmorphism HTML page to: {filepath}...", flush=True)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[AGENT WORK] Save Success -> Recorded {len(html_content)} characters to {filename}.\n", flush=True)
        return f"Success: Saved sector research page to {filepath}"
    except Exception as e:
        print(f"[AGENT WORK] Save Error -> Failed to write to {filepath}: {str(e)}", flush=True)
        return f"Error saving HTML file: {str(e)}"

def read_existing_analysis(business_area: str, sector: str) -> str:
    """
    Reads the content of an existing B2B sector page inside the businessareaanalysis directory
    by programmatically resolving the combined filename in the format: [business_area]___[sector].html
    
    Args:
        business_area (str): The B2B business area name.
        sector (str): The primary industry sector.
        
    Returns:
        str: The content of the file, or an empty string if it does not exist.
    """
    comp_slug = format_slug(business_area)
    sect_slug = format_slug(sector)
    filename = f"{comp_slug}___{sect_slug}.html"
    filepath = os.path.join(MARKET_RESEARCH_DIR, filename)
    
    print(f"[AGENT WORK] Inspecting businessareaanalysis for existing page: '{filename}'...", flush=True)
    if os.path.exists(filepath):
        try:
            print(f"[AGENT WORK] Existing file found. Loading contents for comparison & smart merge...", flush=True)
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"[AGENT WORK] Error reading existing file: {str(e)}", flush=True)
            return f"Error reading file: {str(e)}"
    print(f"[AGENT WORK] No existing page found. Initializing a new premium B2B page from scratch...", flush=True)
    return ""

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
                
    print(f"[AGENT WORK] Parsing B2B Business Area Vector Registry file: {filepath}...", flush=True)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Find registry body segment
        tbody_match = re.search(r'<tbody id="registry-body">(.*?)</tbody>', content, re.DOTALL)
        tbody_content = tbody_match.group(1) if tbody_match else content
        
        # Extract rows
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

def list_existing_research_pages() -> str:
    """
    Retrieves the list of existing market research HTML pages in the businessareaanalysis directory.
    
    Returns:
        str: A string summarizing all existing sector pages for structural / style consistency.
    """
    print(f"[AGENT WORK] Querying list of existing sector pages under businessareaanalysis...", flush=True)
    if not os.path.exists(MARKET_RESEARCH_DIR):
        return "No businessareaanalysis directory found."
    
    files = [f for f in os.listdir(MARKET_RESEARCH_DIR) if f.endswith(".html")]
    return f"Existing Sector Pages in businessareaanalysis ({len(files)} total):\n" + "\n".join(sorted(files))

# Define the Market Research HTML Generator Agent using Google ADK
root_agent = Agent(
    model='gemini-2.5-pro',
    name='business_economic_analysis',
    description='A specialized ADK agent that generates premium B2B market research sector HTML pages inside businessareaanalysis by scanning businessareas directory, matching the exact styling structure of air_gas_draft_systems.html and intelligently merging details for existing pages.',
    instruction="""
    You are the Lead B2B Industry Research and Capital Orchestration Officer.
    Your objective is to scan the available HTML registry files inside the `marketresearch/businessareas/` directory by calling the `list_registry_files` tool. Then, for each registry file found, call `parse_registry_html` to parse all B2B business areas registered inside its table. For each registered business area parsed, generate or update a distinct, gorgeous B2B market research sector HTML page inside the `businessareaanalysis/` directory.

    =========================================
    CRITICAL REQUIREMENT: ABSOLUTE STYLISTIC & VISUAL PARITY
    =========================================
    Every page you create or update MUST match the exact premium visual layout, HSL design tokens, desaturated dark theme, custom icons, glassmorphism CSS styling, and grid structures of `marketresearch/air_gas_draft_systems.html`.
    Do NOT use generic hex colors like #1a1a1a or #bb86fc. You MUST use the desaturated mist-cyan theme and layout from air_gas_draft_systems.html verbatim.

    Every output HTML page must contain the following EXACT CSS block inside the `<head>` tag:
    ```css
        /* Curated HSL Design Tokens (Sleek Mist Cyan Theme) */
        :root {
            --bg-dark: hsl(185, 20%, 5%);
            --bg-grid: hsl(185, 20%, 8%);
            --card-bg: rgba(15, 23, 42, 0.65);
            --card-border: rgba(255, 255, 255, 0.07);
            --card-border-hover: rgba(6, 182, 212, 0.35);
            --text-primary: hsl(210, 40%, 98%);
            --text-secondary: hsl(215, 25%, 72%);
            --text-muted: hsl(215, 16%, 50%);
            
            --accent-mist: hsl(185, 45%, 65%);
            --accent-cyan: hsl(190, 80%, 45%);
            --accent-amber: hsl(40, 92%, 52%);
            
            --primary-gradient: linear-gradient(135deg, hsl(185, 45%, 65%), hsl(190, 80%, 45%));
            --glow-mist: rgba(6, 182, 212, 0.15);
            --glow-cyan: rgba(34, 211, 238, 0.12);
            --glow-amber: rgba(245, 158, 11, 0.12);
            
            --font-outfit: 'Outfit', sans-serif;
            --font-inter: 'Inter', sans-serif;
        }

        /* Reset & Base Styles */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-dark);
            color: var(--text-primary);
            font-family: var(--font-inter);
            line-height: 1.6;
            padding: 2rem 1.5rem;
            min-height: 100vh;
            background-image: 
                radial-gradient(at 0% 0%, rgba(6, 182, 212, 0.07) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(34, 211, 238, 0.03) 0px, transparent 50%);
            background-attachment: fixed;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        /* Header Layout */
        header {
            margin-bottom: 3.5rem;
            text-align: center;
            position: relative;
        }

        .category-badge {
            display: inline-block;
            background: rgba(6, 182, 212, 0.1);
            border: 1px solid rgba(6, 182, 212, 0.2);
            color: var(--accent-mist);
            padding: 0.4rem 1.2rem;
            border-radius: 50px;
            font-family: var(--font-outfit);
            font-weight: 600;
            font-size: 0.85rem;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }

        h1 {
            font-family: var(--font-outfit);
            font-size: 2.8rem;
            font-weight: 700;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.75rem;
            letter-spacing: -0.5px;
        }

        .subtitle {
            color: var(--text-secondary);
            font-size: 1.15rem;
            font-weight: 300;
            max-width: 750px;
            margin: 0 auto;
        }

        /* Overview Section */
        .overview-section {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 3rem;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }

        .overview-title {
            font-family: var(--font-outfit);
            font-size: 1.4rem;
            color: var(--text-primary);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .overview-title::before {
            content: "";
            display: inline-block;
            width: 4px;
            height: 20px;
            background: var(--primary-gradient);
            border-radius: 2px;
        }

        .overview-text {
            color: var(--text-secondary);
            font-size: 1.05rem;
            font-weight: 300;
        }

        /* Responsive Driver Grid (3 Cards) */
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2rem;
            margin-bottom: 4rem;
        }

        /* High-End Glassmorphic Cards */
        .card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 2.2rem;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            backdrop-filter: blur(12px);
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25);
        }

        .card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            transition: opacity 0.3s ease;
        }

        /* Card-Specific Accents */
        .card-mandates::before { background: var(--accent-mist); }
        .card-mandates { box-shadow: 0 15px 35px rgba(0,0,0,0.25), inset 0 0 20px var(--glow-mist); }

        .card-wear::before { background: var(--accent-cyan); }
        .card-wear { box-shadow: 0 15px 35px rgba(0,0,0,0.25), inset 0 0 20px var(--glow-cyan); }

        .card-auxiliary::before { background: var(--accent-amber); }
        .card-auxiliary { box-shadow: 0 15px 35px rgba(0,0,0,0.25), inset 0 0 20px var(--glow-amber); }

        /* Card Hover States with Subtle Scale and Border Glow */
        .card:hover {
            transform: translateY(-6px);
            border-color: var(--card-border-hover);
            box-shadow: 0 25px 45px rgba(0, 0, 0, 0.4);
        }

        /* Card Header & Badges */
        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.5rem;
        }

        .card-icon {
            font-size: 2rem;
        }

        .card-badge {
            font-family: var(--font-outfit);
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            padding: 0.25rem 0.8rem;
            border-radius: 20px;
            letter-spacing: 0.5px;
        }

        .badge-mist { background: rgba(6, 182, 212, 0.1); color: var(--accent-mist); border: 1px solid rgba(6, 182, 212, 0.2); }
        .badge-cyan { background: rgba(34, 211, 238, 0.1); color: var(--accent-cyan); border: 1px solid rgba(34, 211, 238, 0.2); }
        .badge-amber { background: rgba(245, 158, 11, 0.1); color: var(--accent-amber); border: 1px solid rgba(245, 158, 11, 0.2); }

        /* Card Typography */
        .card-title {
            font-family: var(--font-outfit);
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 1rem;
            letter-spacing: -0.2px;
        }

        .card-desc {
            color: var(--text-secondary);
            font-size: 0.95rem;
            font-weight: 300;
            margin-bottom: 1.5rem;
            flex-grow: 1;
        }

        /* Strategic Highlights */
        .strategic-highlight {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1rem;
            margin-top: auto;
        }

        .strategic-title {
            font-family: var(--font-outfit);
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-primary);
            text-transform: uppercase;
            margin-bottom: 0.4rem;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .strategic-desc {
            font-size: 0.85rem;
            color: var(--text-secondary);
            font-weight: 300;
        }

        /* Financial Advisory Footer Block */
        .advisory-block {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.5), rgba(15, 23, 42, 0.5));
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 2.5rem;
            backdrop-filter: blur(10px);
            box-shadow: 0 20px 45px rgba(0, 0, 0, 0.3);
            text-align: center;
        }

        .advisory-badge {
            display: inline-block;
            background: rgba(6, 182, 212, 0.1);
            border: 1px solid rgba(6, 182, 212, 0.2);
            color: var(--accent-mist);
            font-family: var(--font-outfit);
            font-weight: 600;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            padding: 0.35rem 1rem;
            border-radius: 30px;
            margin-bottom: 1.25rem;
        }

        .advisory-title {
            font-family: var(--font-outfit);
            font-size: 1.8rem;
            color: var(--text-primary);
            margin-bottom: 1rem;
        }

        .advisory-text {
            color: var(--text-secondary);
            font-size: 1.05rem;
            font-weight: 300;
            max-width: 850px;
            margin: 0 auto;
            line-height: 1.7;
        }

        /* Responsive Breakpoints */
        @media (max-width: 768px) {
            h1 { font-size: 2.2rem; }
            body { padding: 1.5rem 1rem; }
            .grid { grid-template-columns: 1fr; }
            .card { padding: 1.8rem; }
        }
    ```

    =========================================
    STRICT HTML LAYOUT STRUCTURE (IN ORDER):
    =========================================
    Every output file must feature this precise element nesting, classes, and styles:

    1. `<div class="container">` wrapping the entire page.
    2. `<header>` Layout:
       ```html
       <header>
           <span class="category-badge">[Industry Sector (e.g. Semiconductor Fabrication / OSAT)]</span>
           <h1>[Business Area]</h1>
           <p class="subtitle">[Compelling dynamic descriptive tagline of factors]</p>
       </header>
       ```
    3. `<section class="overview-section">` Layout:
       ```html
       <section class="overview-section">
           <h2 class="overview-title">Business Area Context</h2>
           <p class="overview-text">
               [Deep industry context paragraph. Synthesize how the systemic/public drivers, physical operating load drivers, and operating cost/penalty drivers interact to influence Tier-1/Tier-2 capital deployment.]
           </p>
       </section>
       ```
    4. `<main class="grid">` Layout with 3 high-end glassmorphism driver cards:
       - **Card 1 (Systemic / Policy Catalyst)**:
         ```html
         <div class="card card-mandates">
             <div class="card-header">
                 <span class="card-icon">🏛️</span>
                 <span class="card-badge badge-mist">Systemic Catalyst</span>
             </div>
             <h3 class="card-title">[Title of Policy/Systemic Catalyst]</h3>
             <p class="card-desc">
                 [High-density description of sovereign incentives, trade policies, or macro market shifts.]
             </p>
             <div class="strategic-highlight">
                 <h4 class="strategic-title">⚡ CapEx Implication</h4>
                 <p class="strategic-desc">[Clear, quantitative-feeling B2B CapEx implication text.]</p>
             </div>
         </div>
         ```
       - **Card 2 (Physical / Operating Load)**:
         ```html
         <div class="card card-wear">
             <div class="card-header">
                 <span class="card-icon">⚙️</span>
                 <span class="card-badge badge-cyan">Physical Load</span>
             </div>
             <h3 class="card-title">[Title of Physical/Operating Load Driver]</h3>
             <p class="card-desc">
                 [High-density description of equipment parameters, raw material loads, or engineering demands.]
             </p>
             <div class="strategic-highlight">
                 <h4 class="strategic-title">⚡ CapEx Implication</h4>
                 <p class="strategic-desc">[Clear, quantitative-feeling physical CapEx implication text.]</p>
             </div>
         </div>
         ```
       - **Card 3 (Operating Cost / Penalty)**:
         ```html
         <div class="card card-auxiliary">
             <div class="card-header">
                 <span class="card-icon">⚡</span>
                 <span class="card-badge badge-amber">Operating Penalty</span>
             </div>
             <h3 class="card-title">[Title of Cost / Auxiliary Load Penalty]</h3>
             <p class="card-desc">
                 [High-density description of operating penalties, energy tariffs, or talent scarcity costs.]
             </p>
             <div class="strategic-highlight">
                 <h4 class="strategic-title">⚡ CapEx Implication</h4>
                 <p class="strategic-desc">[Clear, quantitative-feeling operating cost CapEx implication text.]</p>
             </div>
         </div>
         ```
    5. `<footer class="advisory-block">` Layout:
       ```html
       <footer class="advisory-block">
           <span class="advisory-badge">Strategic Takeaway</span>
           <h2 class="advisory-title">B2B Vendor & Investment Summary</h2>
           <p class="advisory-text">
               [Actionable advisory takeaway detailing which products/capabilities command pricing premiums and what capital financing structures are standard for this segment.]
           </p>
       </footer>
       ```
    6. **Institutional Lenders & Capital Partners** block (`<section class="lending-section">`):
       This section must feature the exact inline styling below, containing 4 glassmorphism cards. Set all quantitative metrics to **N/A** (NO placeholders, NO dummy numbers):
       ```html
       <section class="lending-section" style="background: rgba(15, 23, 42, 0.4); border: 1px solid var(--card-border); border-radius: 20px; padding: 2.2rem; margin-top: 3rem; backdrop-filter: blur(10px); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);">
           <h3 style="font-family: var(--font-outfit); font-size: 1.4rem; color: var(--text-primary); margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
               🏦 Active Institutional Lenders & Financiers
           </h3>
           <p style="color: var(--text-secondary); font-size: 0.95rem; font-weight: 300; line-height: 1.6; margin-bottom: 1.5rem;">
               The following leading financial institutions, developmental agencies, and commercial banks actively provide project debt, credit limits, and working capital solutions to Tier-1/Tier-2 suppliers and asset operators in the <strong>[Business Area]</strong> space.
           </p>
           <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
               <!-- Card 1: Key Lenders & Market Shares -->
               <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 12px; padding: 1.25rem;">
                   <h4 style="font-family: var(--font-outfit); font-size: 1.05rem; color: var(--text-primary); margin-bottom: 1rem; display: flex; align-items: center; gap: 0.4rem;">
                       🏢 Primary Sources & Market Share
                   </h4>
                   <ul style="list-style: none; padding: 0; margin: 0;">
                       <li style="margin-bottom: 0.75rem; border-bottom: 1px solid rgba(255, 255, 255, 0.03); padding-bottom: 0.5rem;">
                           <strong style="color: var(--text-primary); font-size: 0.9rem;">[Lender 1 (e.g., EXIM Bank of India)]</strong><br>
                           <span style="font-size: 0.78rem; color: var(--text-muted);">Est. Market Share: </span>
                           <span style="font-size: 0.78rem; color: var(--text-secondary); opacity: 0.75; font-weight: 500;">N/A (Proprietary / Private Exposure)</span>
                       </li>
                       <li style="margin-bottom: 0.75rem; border-bottom: 1px solid rgba(255, 255, 255, 0.03); padding-bottom: 0.5rem;">
                           <strong style="color: var(--text-primary); font-size: 0.9rem;">[Lender 2 (e.g., State Bank of India)]</strong><br>
                           <span style="font-size: 0.78rem; color: var(--text-muted);">Est. Market Share: </span>
                           <span style="font-size: 0.78rem; color: var(--text-secondary); opacity: 0.75; font-weight: 500;">N/A (Proprietary / Private Exposure)</span>
                       </li>
                       <li style="margin-bottom: 0.75rem; border-bottom: 1px solid rgba(255, 255, 255, 0.03); padding-bottom: 0.5rem;">
                           <strong style="color: var(--text-primary); font-size: 0.9rem;">[Lender 3 (e.g., HDFC Bank)]</strong><br>
                           <span style="font-size: 0.78rem; color: var(--text-muted);">Est. Market Share: </span>
                           <span style="font-size: 0.78rem; color: var(--text-secondary); opacity: 0.75; font-weight: 500;">N/A (Proprietary / Private Exposure)</span>
                       </li>
                       <li style="margin-bottom: 0.75rem;">
                           <strong style="color: var(--text-primary); font-size: 0.9rem;">[Lender 4 (e.g., Power Finance Corporation or ADB)]</strong><br>
                           <span style="font-size: 0.78rem; color: var(--text-muted);">Est. Market Share: </span>
                           <span style="font-size: 0.78rem; color: var(--text-secondary); opacity: 0.75; font-weight: 500;">N/A (Proprietary / Private Exposure)</span>
                       </li>
                   </ul>
               </div>
               <!-- Card 2: Preferred Products -->
               <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 12px; padding: 1.25rem;">
                   <h4 style="font-family: var(--font-outfit); font-size: 1.05rem; color: var(--text-primary); margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.4rem;">
                       💼 Financing Instruments
                   </h4>
                   <ul style="list-style: none; padding: 0; font-size: 0.88rem; color: var(--text-secondary); line-height: 1.5;">
                       <li style="margin-bottom: 0.5rem;">• <strong>Project Debt Consortia:</strong> Non-recourse debt structured against long-term off-take agreements.</li>
                       <li style="margin-bottom: 0.5rem;">• <strong>Structured Trade Credit:</strong> Working capital and supply chain financing for critical components.</li>
                       <li>• <strong>Guarantees & LC:</strong> Letters of Credit and bank guarantees to secure equipment deliveries from global OEMs.</li>
                   </ul>
               </div>
               <!-- Card 3: Key Underwriting Benchmarks -->
               <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 12px; padding: 1.25rem;">
                   <h4 style="font-family: var(--font-outfit); font-size: 1.05rem; color: var(--text-primary); margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.4rem;">
                       📊 Underwriting Benchmarks
                   </h4>
                   <ul style="list-style: none; padding: 0; font-size: 0.88rem; color: var(--text-secondary); line-height: 1.5;">
                       <li style="margin-bottom: 0.5rem;">• <strong>Min. DSCR:</strong> N/A (Transaction-Specific / Underwriter Discretionary)</li>
                       <li style="margin-bottom: 0.5rem;">• <strong>Cash Escrow:</strong> Compulsory routing of off-taker collections with DSRA reserves.</li>
                       <li>• <strong>Security Package:</strong> Charge on immovable property, plant equipment, and stock reserves.</li>
                   </ul>
               </div>
               <!-- Card 4: Quantitative Capital Parameters -->
               <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 12px; padding: 1.25rem;">
                   <h4 style="font-family: var(--font-outfit); font-size: 1.05rem; color: var(--text-primary); margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.4rem;">
                       📈 Quantitative Capital Parameters
                   </h4>
                   <ul style="list-style: none; padding: 0; font-size: 0.88rem; color: var(--text-secondary); line-height: 1.5;">
                       <li style="margin-bottom: 0.5rem;">• <strong>Interest Rate:</strong> N/A (Subject to Benchmark Rate & Credit Risk Assessment)</li>
                       <li style="margin-bottom: 0.5rem;">• <strong>Standard Facility Size:</strong> N/A (Case-by-Case / Project Scale Dependent)</li>
                       <li style="margin-bottom: 0.5rem;">• <strong>Target Debt-to-Equity:</strong> N/A (Capital Structure & Credit Rating Dependent)</li>
                       <li>• <strong>Loan Maturity Tenure:</strong> N/A (Facility & Asset Life Cycle Dependent)</li>
                   </ul>
               </div>
           </div>
       </section>
       ```
    7. **B2B Vector Intelligence Registry** block (`<section class="vector-registry">`):
       This section details the Business Area, Sector, Macro systemic factors, and Micro entity-specific factors in a gorgeous CSS grid exactly as follows:
       ```html
       <section class="vector-registry" style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px; padding: 1.5rem; margin-bottom: 2rem; backdrop-filter: blur(10px);">
           <h3 style="font-family: var(--font-outfit); font-size: 1.1rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-primary); margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
               📋 B2B Intelligence Vector Registry
           </h3>
           <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem;">
               <div>
                   <span style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); display: block; margin-bottom: 0.25rem;">Business Area</span>
                   <strong style="font-family: var(--font-outfit); font-size: 1.05rem; color: var(--text-primary);">[Business Area]</strong>
               </div>
               <div>
                   <span style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); display: block; margin-bottom: 0.25rem;">Industry Sector</span>
                   <strong style="font-family: var(--font-outfit); font-size: 1.05rem; color: var(--text-primary);">[Industry Sector]</strong>
               </div>
               <div>
                   <span style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); display: block; margin-bottom: 0.25rem;">Macroeconomic Factors (Systemic)</span>
                   <p style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.4; font-weight: 300;">[Semicolon-separated macroeconomic factors...]</p>
               </div>
               <div>
                   <span style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); display: block; margin-bottom: 0.25rem;">Microeconomic Factors (Entity-Specific)</span>
                   <p style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.4; font-weight: 300;">[Semicolon-separated microeconomic factors...]</p>
               </div>
           </div>
       </section>
       ```
    8. **B2B Glossary & factor breakdown** block (`<section class="glossary-section">`):
       This section must feature a desaturated dark glassmorphic grid with two clean columns (Systemic Macroeconomic Terms and Entity-Specific Microeconomic Terms) detailed using styled lists as follows:
       ```html
       <section class="glossary-section" style="background: rgba(15, 23, 42, 0.45); border: 1px solid var(--card-border); border-radius: 20px; padding: 2.2rem; margin-top: 3rem; backdrop-filter: blur(10px); box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);">
           <h3 style="font-family: var(--font-outfit); font-size: 1.4rem; color: var(--text-primary); margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
               📚 B2B Glossary & Factor Breakdown
           </h3>
           <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2.5rem;">
               
               <!-- Macroeconomic Terms Explained -->
               <div>
                   <h4 style="font-family: var(--font-outfit); font-size: 1.1rem; color: var(--accent-mist); margin-bottom: 1.25rem; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;">
                       Systemic Macroeconomic Terms
                   </h4>
                   <ul style="list-style: none;">
                       <li style="margin-bottom: 1.25rem; border-bottom: 1px solid rgba(255, 255, 255, 0.03); padding-bottom: 0.75rem;">
                           <strong style="color: var(--text-primary); display: block; font-size: 0.95rem; font-family: var(--font-outfit); margin-bottom: 0.25rem;">[Term 1 (e.g. Production Linked Incentive)]</strong>
                           <span style="font-size: 0.88rem; color: var(--text-secondary); font-weight: 300; line-height: 1.5; display: block;">[Comprehensive professional definition...]</span>
                       </li>
                       <li style="margin-bottom: 1.25rem; border-bottom: 1px solid rgba(255, 255, 255, 0.03); padding-bottom: 0.75rem;">
                           <strong style="color: var(--text-primary); display: block; font-size: 0.95rem; font-family: var(--font-outfit); margin-bottom: 0.25rem;">[Term 2]</strong>
                           <span style="font-size: 0.88rem; color: var(--text-secondary); font-weight: 300; line-height: 1.5; display: block;">[Comprehensive professional definition...]</span>
                       </li>
                       <!-- Add other systemic factors mentioned in registry or overview -->
                   </ul>
               </div>

               <!-- Microeconomic Terms Explained -->
               <div>
                   <h4 style="font-family: var(--font-outfit); font-size: 1.1rem; color: var(--accent-mist); margin-bottom: 1.25rem; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;">
                       Entity-Specific Microeconomic Terms
                   </h4>
                   <ul style="list-style: none;">
                       <li style="margin-bottom: 1.25rem; border-bottom: 1px solid rgba(255, 255, 255, 0.03); padding-bottom: 0.75rem;">
                           <strong style="color: var(--text-primary); display: block; font-size: 0.95rem; font-family: var(--font-outfit); margin-bottom: 0.25rem;">[Term 1 (e.g. Upfront CapEx)]</strong>
                           <span style="font-size: 0.88rem; color: var(--text-secondary); font-weight: 300; line-height: 1.5; display: block;">[Comprehensive professional definition...]</span>
                       </li>
                       <li style="margin-bottom: 1.25rem; border-bottom: 1px solid rgba(255, 255, 255, 0.03); padding-bottom: 0.75rem;">
                           <strong style="color: var(--text-primary); display: block; font-size: 0.95rem; font-family: var(--font-outfit); margin-bottom: 0.25rem;">[Term 2]</strong>
                           <span style="font-size: 0.88rem; color: var(--text-secondary); font-weight: 300; line-height: 1.5; display: block;">[Comprehensive professional definition...]</span>
                       </li>
                       <!-- Add other entity-specific factors mentioned in registry or overview -->
                   </ul>
               </div>

           </div>
       </section>
       ```

    =========================================
    SMART MERGE & ENRICH PROTOCOL:
    =========================================
    Before writing any HTML page:
    1. Formulate the dynamic lowercase underscored filename corresponding to BOTH the Business Area and the Industry Sector, joined by three underscores `___` (i.e. `[business_area]___[sector].html`).
       Replace all spaces, slashes, ampersands, and special characters inside each part with single underscores before combining them.
    2. Call `read_existing_analysis` to check if this page already exists inside the `businessareaanalysis` folder.
    3. IF the page already exists:
       - Read the existing HTML content.
       - Proactively compare the new component details with the existing page content.
       - Merge the details: combine the Business Area Context sentences, extend/expand the CapEx drivers (or add cards/drivers if new ones are found), update the registered lenders if new ones are relevant, append new entries to the registry section, and integrate new terms into the glossary section.
       - Maintain the exact CSS styles, classes, HSL colors, and DOM structure of the `air_gas_draft_systems.html` template during the merge.
       - Save the merged page back to `/businessareaanalysis/`.
    4. IF the page does not exist:
       - Generate the complete high-fidelity page from scratch using the template above, and save it in `/businessareaanalysis/`.

    When invoked, you must:
    1. First, call `list_registry_files` to discover all registry files inside the `businessareas` directory.
    2. For each registry file, call `parse_registry_html` to extract all the registered B2B business areas.
    3. For each registered business area parsed, you MUST call 'read_existing_analysis' to inspect existing content, and then you MUST call 'save_html_page' to write the generated/merged high-fidelity B2B HTML page. You must call the save tool sequentially for EACH AND EVERY parsed business area. Do NOT skip calling the save tool or simply output a text summary without actually writing the files.
    4. Return a clean, premium executive report to the user summarizing the files successfully updated or created inside `/businessareaanalysis/`.
    """,
    tools=[
        list_registry_files,
        parse_registry_html,
        read_existing_analysis,
        save_html_page,
        list_existing_research_pages
    ]
)
