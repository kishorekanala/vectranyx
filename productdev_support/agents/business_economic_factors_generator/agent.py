import os
from google.adk.agents.llm_agent import Agent

# Target file path in the reports/marketresearch/businessareas directory
MARKET_RESEARCH_DIR = "/Users/kishore/myprojects/vectranyx/reports/marketresearch/businessareas"

DEFAULT_REGISTRY_FILE = "businessareas.html"

def read_from_file(filename: str) -> str:
    """
    Reads the content of a file.
    
    Args:
        filename (str): The name of the file to read.
        
    Returns:
        str: The content of the file.
    """
    with open(filename, 'r') as f:
        return f.read()

def register_business_area(component_area: str, sector: str, macro_factors: str, micro_factors: str, filename: str = DEFAULT_REGISTRY_FILE, page_title: str = "B2B Component Vector Registry", page_subtitle: str = "Dynamic indexing of core components, sectors, systemic macroeconomic variables, and operational microeconomic risks.") -> str:
    """
    Saves or appends the extracted B2B vector information as a row in the central HTML registry.
    
    Args:
        component_area (str): The name/specification of the business component area.
        sector (str): The primary industry sector.
        macro_factors (str): Systemic macroeconomic factors impacting the sector.
        micro_factors (str): Entity-specific microeconomic/operational factors impacting the business.
        filename (str, optional): Target filename. Defaults to 'businessareas.html'.
        page_title (str, optional): Dynamic title for the HTML page.
        page_subtitle (str, optional): Dynamic subtitle for the HTML page.
        
    Returns:
        str: Success message or error.
    """
    os.makedirs(MARKET_RESEARCH_DIR, exist_ok=True)
    filepath = os.path.join(MARKET_RESEARCH_DIR, filename)
    
    # Format the new HTML row with clean, structured elements
    new_row = f"""                    <tr>
                        <td style="font-weight: 500; color: var(--text-primary);">{component_area.strip()}</td>
                        <td style="color: var(--accent-cyan); font-weight: 500;">{sector.strip()}</td>
                        <td>{macro_factors.strip()}</td>
                        <td>{micro_factors.strip()}</td>
                    </tr>"""
    
    # If the file does not exist, build the HTML page with modern desaturated dark HSL styles
    if not os.path.exists(filepath):
        print(f"\n[AGENT WORK] Save Request -> File: '{filename}' (Creating new registry)", flush=True)
        print(f"[AGENT WORK] Writing dynamic factor registry HTML page to: {filepath}...", flush=True)
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title.strip()}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Outfit:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-dark: hsl(200, 20%, 5%);
            --bg-grid: hsl(200, 20%, 8%);
            --card-bg: rgba(15, 23, 42, 0.65);
            --card-border: rgba(255, 255, 255, 0.07);
            --text-primary: hsl(210, 40%, 98%);
            --text-secondary: hsl(215, 25%, 72%);
            --text-muted: hsl(215, 16%, 50%);
            --accent-cyan: hsl(190, 80%, 45%);
            --accent-mist: hsl(185, 45%, 65%);
            --primary-gradient: linear-gradient(135deg, hsl(185, 45%, 65%), hsl(190, 80%, 45%));
            --font-outfit: 'Outfit', sans-serif;
            --font-inter: 'Inter', sans-serif;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            background-color: var(--bg-dark);
            color: var(--text-primary);
            font-family: var(--font-inter);
            line-height: 1.6;
            padding: 3rem 1.5rem;
            min-height: 100vh;
            background-image: 
                radial-gradient(at 0% 0%, rgba(6, 182, 212, 0.07) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(34, 211, 238, 0.03) 0px, transparent 50%);
            background-attachment: fixed;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        header {{
            text-align: center;
            margin-bottom: 3rem;
        }}
        .badge {{
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
        }}
        h1 {{
            font-family: var(--font-outfit);
            font-size: 2.5rem;
            font-weight: 700;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        .subtitle {{
            color: var(--text-secondary);
            font-weight: 300;
            font-size: 1.05rem;
        }}
        .registry-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 2.2rem;
            backdrop-filter: blur(12px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25);
            overflow-x: auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}
        th {{
            font-family: var(--font-outfit);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 0.5px;
            color: var(--text-primary);
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
            padding: 1rem;
        }}
        td {{
            padding: 1.2rem 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            color: var(--text-secondary);
            font-size: 0.92rem;
            font-weight: 300;
        }}
        tr:hover td {{
            background: rgba(255, 255, 255, 0.01);
            color: var(--text-primary);
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <span class="badge">Orchestrated Registry</span>
            <h1>{page_title.strip()}</h1>
            <p class="subtitle">{page_subtitle.strip()}</p>
        </header>
        <div class="registry-card">
            <table>
                <thead>
                    <tr>
                        <th style="width: 25%;">Component Area</th>
                        <th style="width: 20%;">Industry Sector</th>
                        <th style="width: 27%;">Macroeconomic Factors (Systemic)</th>
                        <th style="width: 28%;">Microeconomic Factors (Entity-Specific)</th>
                    </tr>
                </thead>
                <tbody id="registry-body">
{new_row}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>"""
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"[AGENT WORK] Save Success -> Recorded {len(html_content)} characters to {filename}.\n", flush=True)
            return f"Success: Created new factor registry at {filepath} and registered the first business entry."
        except Exception as e:
            print(f"[AGENT WORK] Save Error -> Failed to write to {filepath}: {str(e)}", flush=True)
            return f"Error creating registry HTML: {str(e)}"
    else:
        # File exists: safely locate <tbody id="registry-body"> or </tbody> and append the row
        print(f"\n[AGENT WORK] Append Request -> File: '{filename}' (Appending component area: '{component_area}')", flush=True)
        print(f"[AGENT WORK] Reading registry file to locate table body...", flush=True)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            tbody_idx = content.find("</tbody>")
            if tbody_idx == -1:
                tbody_idx = content.find("</table>")
                
            if tbody_idx == -1:
                print(f"[AGENT WORK] Append Error -> Could not locate table body segment inside {filename}", flush=True)
                return "Error: Could not locate table body segment inside businessareas.html"
                
            new_content = content[:tbody_idx] + new_row + "\n" + content[tbody_idx:]
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"[AGENT WORK] Append Success -> Successfully appended factor vectors for '{component_area}' into {filename}.\n", flush=True)
            return f"Success: Safely appended the extracted factor vectors into {filepath}"
        except Exception as e:
            print(f"[AGENT WORK] Append Error -> Failed to write to {filepath}: {str(e)}", flush=True)
            return f"Error updating registry HTML: {str(e)}"

# Define the ADK Semantic Factor Extractor Agent
root_agent = Agent(
    model='gemini-2.5-flash',
    name='business_factor_extractor',
    description='An ADK agent that extracts systemic macro factors and entity-specific micro risks from natural language business descriptions and appends them to a dynamically generated sector registry HTML page.',
    instruction="""
    You are the Senior Industry Architect and Semantic Data Extraction Specialist.
    Your mission is to read any natural language input or file path provided by the user (which may be a specific business description, a broad industry trend, or a high-level strategic directive like sovereign manufacturing goals) and dynamically map it into highly precise B2B business area vectors.
    If file path is provided, read the file using read_from_file tool and extract the business information to create business areas in India related to the input.
    If file path is not provided, use the natural language input to create business areas in India related to the input.

    CRITICAL STEP-BY-STEP WORKFLOW:
    1. **Identify Possible Business Areas**: 
       Analyze the user's input and identify 4 to 10 distinct, concrete, and viable B2B business areas, manufacturing sub-assemblies, or service segments that are direct or indirect parts of the industry, technology, or goal described (e.g. if the user talks about "semiconductor manufacturing in India," identify segments like 'Silicon Wafer Fabrication Facilities', 'ATMP (Assembly, Testing, Marking, and Packaging) Services', and 'High-Purity Specialty Chemical & Gas Supply Chains').
       OPERATING ENVIRONMENT IS INDIA. THE BUSINESS AREAS SHOULD BE IN INDIA
       
    2. **Synthesize Factor Vectors for Each Identified Area**:
       For each identified business area, extract or synthesize the four critical factor vectors:
       - **Component Area**: The specific physical component system, machinery, or sub-assembly targeted (e.g. 'Lithography & Mask Alignment Systems', 'Cleanroom Air Handling & HVAC Internals').
       - **Identify component area as granular as possible. Granularity should depend on the areas that individual businesses are operating in [Example, braking system for various categories of vehicles like EV, ICE, Hybrid etc. and the specific braking systems for each], solar module for EV, ICE, Hybrid etc. and the specific solar modules for each, solar panels for renewable energy business and the specific solar panels for each, etc. The component area should be specific to the industry or technology described]**
       - **Industry Sector**: The parent macro sector category (e.g. 'Semiconductor Fabrication / High-Tech Manufacturing').
       - **Macroeconomic Factors (Systemic)**: Core global economic variables, sovereign mandates, capital subsidies, tariff structures, or global raw material shortages (e.g. 'Sovereign financial incentives (PLI schemes), international raw material tariff structures').
       - **Microeconomic Factors (Entity-Specific)**: Local physical wear, specialized engineer talent shortages, extreme cleanroom standard maintenance costs, or high R&D obsolescence risks (e.g. 'High upfront CapEx for lithography tooling, extreme filtration and contamination controls').

    3. **Generate Custom Output Filename & Register**:
       - Programmatically determine a highly appropriate, descriptive, and customized filename for the registry HTML page based on the user's input and content generated (e.g., if the input is about semiconductors, generate 'semiconductor_registry.html'; if it is about smart grids, generate 'smart_grid_registry.html').
       - The filename must be all lowercase, alphanumeric with underscores, and always end in '.html'.
       - Programmatically determine an appropriate, highly professional dynamic title (e.g. 'India Semiconductor Manufacturing Registry') and a detailed B2B subtitle (e.g. 'Orchestrated registry of fabrication, packaging, equipment, and supply-chain vectors') for the page.
       - For EACH identified business area, call the `register_business_area` tool, passing in its synthesized vectors, the dynamically determined custom `filename`, and the custom `page_title` and `page_subtitle` parameters (to append if the file already exists, or create it if not).
       - Write the file in /Users/kishore/myprojects/vectranyx/reports/marketresearch/businessareas folder mandatorily.

    4. **Generate Executive Report**:
       Provide a clean, comprehensive, premium HTML report to the user:
       - An introductory section explaining the strategic context of the identified business areas.
       - A beautifully structured table detailing each identified segment with its Sector, Component, Macro, and Micro vectors.
       - A formal confirmation explicitly naming the dynamic output file generated (e.g., 'Registered inside the semiconductor_registry.html database').
    """,
    tools=[
        read_from_file,
        register_business_area
    ]
)



