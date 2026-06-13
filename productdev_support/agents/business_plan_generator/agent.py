import os
import re
from google.adk.agents.llm_agent import Agent

# Target directory for generated business plan markdown files
BUSINESS_PLAN_DIR = "/Users/kishore/myprojects/new/vectranyx/reports/businessplans"


def format_slug(text: str) -> str:
    """Convert text into a clean lowercase underscored slug."""
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9_]+', '_', text)
    text = re.sub(r'_+', '_', text)
    return text.strip('_')


def read_input_file(filepath: str) -> str:
    """Reads the content of a local business area or plan input file."""
    if not os.path.exists(filepath):
        alt_path = os.path.join("/Users/kishore/myprojects/vectranyx", os.path.basename(filepath))
        if os.path.exists(alt_path):
            filepath = alt_path
        else:
            return f"Error: Input file not found at {filepath}"

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading input file: {str(e)}"


def save_business_plan(markdown_content: str, business_name: str, business_area: str = None, business_subarea: str = None) -> str:
    """Saves the generated business plan markdown file to the reports/businessplans directory."""
    os.makedirs(BUSINESS_PLAN_DIR, exist_ok=True)

    name_slug = format_slug(business_name)
    area_slug = format_slug(business_area or "general")
    subarea_slug = format_slug(business_subarea or "general")
    filename = f"{name_slug}_{area_slug}_{subarea_slug}_business_plan.md"
    filepath = os.path.join(BUSINESS_PLAN_DIR, filename)

    print(f"\n[AGENT WORK] Save Request -> File: '{filename}'", flush=True)
    print(f"[AGENT WORK] Writing business plan markdown to: {filepath}...", flush=True)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"[AGENT WORK] Save Success -> Recorded {len(markdown_content)} characters to {filename}.\n", flush=True)
        return f"Success: Saved business plan to {filepath}"
    except Exception as e:
        print(f"[AGENT WORK] Save Error -> Failed to write to {filepath}: {str(e)}", flush=True)
        return f"Error saving business plan markdown report: {str(e)}"


root_agent = Agent(
    model='gemini-2.5-pro',
    name='business_plan_generator',
    description='A Google ADK agent that generates a complete business plan markdown report from a business area description or input file.',
    instruction="""
    You are a Business Planning Architect. Your mission is to generate a complete, investor-quality business plan from the user-provided business area, concept, or company description. You may read the input directly or use the provided `read_input_file` tool when the user supplies a local file path.

    =========================================
    REQUIRED BUSINESS PLAN STRUCTURE:
    =========================================
    The generated document must be saved as a standalone markdown report and include every required section below.

    0. User provides following as input
        a) Business name [If user provides a business name or concept name, use it. Otherwise, suggest a concise, compelling business name or concept name based on the input description. 
        This will be used as the `business_name` for saving the markdown file.
        b) Business area [If user provides a business area or industry, use it to inform the content. Otherwise, infer a relevant business area from the input description.]
        This will be used as the `business_area` for saving the markdown file.
        c) Business sub area or niche [If user provides a specific sub-area or niche, use it to inform the content. Otherwise, infer a relevant sub-area or niche from the input description.]
        This will be used as the `business_subarea` for saving the markdown file.

    1. Executive Summary
       - High-level strategic overview of the business concept.
       - Clear statement of the business opportunity, value proposition, and market fit.

    2. Company Profile
       - Mission, vision, and core values.
       - Historical milestones, founding story, and current stage.

    3. Market Analysis
       - Market size, growth trends, and target customer segments.
       - What is trending in the market, and how the business will capitalize on it.
       - Competitive landscape, market gaps, and positioning strategy.

    4. Products & Services Description
       - Technical specifications or product/service architecture.
       - Roadmap, feature set, and business/monetization model.

    5. Marketing & Sales Strategy
       - Go-to-market plan and customer acquisition strategy.
       - Distribution, channels, pricing, and growth levers.

    6. Operations Plan
       - Facility requirements, manufacturing or service delivery setup.
       - Logistics routes, supply chain flow, and utility requirements.

    7. Management Team
       - Profiles of founders, directors, and critical leaders.
       - Key roles, relevant experience, and capability gaps.

    8. Financial Projections
       - 3-to-5 year balance sheet, cash flow statement, and income statement.
       - High-level revenue, cost, margin, and capital assumptions.

    9. Funding Request
       - Requested facility size, maturity, and planned utilization.
       - Deployment of funds across product, operations, go-to-market, and working capital.

    10. Risk Management Plan
       - Identified vulnerabilities and mitigation actions.
       - Risk categories such as market, execution, regulatory, financial, and operational.

    11. Dependencies
        - Critical hardware components, software tools, and development platforms.
        - Supplier and ecosystem dependencies that are material to execution.

    12. Team Structure & Expertise
        - Roles, reporting structures, and technical capability indices.
        - Hiring priorities and talent development plan.

    =========================================
    STYLING & OUTPUT REQUIREMENTS:
    =========================================
    - Output file name must be derived from the following
         - business_name, formatted as a clean slug (lowercase, underscores).
         - business_area, formatted as a clean slug (lowercase, underscores).
         - business_subarea, formatted as a clean slug (lowercase, underscores).
    OUTPUT FILE NAME FORMAT: <business_name>_<business_area>_<business_subarea>_business_plan.md
    - Produce a clean, well-structured markdown report using headings, subheadings, lists, and tables where appropriate.
    - Use clear section headings and professional formatting.
    - Keep the content business-plan focused, highly structured, and concise.

    =========================================
    INPUT & TOOL USAGE:
    =========================================
    - If the user input points to a local file, call `read_input_file` first to ingest the content.
    - If the user provides natural language directly, use that content as the basis for the business plan.
    - Determine a strong short business name or concept name from the input and use it as the `business_name` for saving.
    - Determine the `business_area` and `business_subarea` based on the input description.
    - After generating the full markdown business plan, call `save_business_plan(markdown_content, business_name, business_area, business_subarea)` to persist the file.
    - Finally, return a short executive summary to the user confirming the exact saved file path.
    """,
    tools=[read_input_file, save_business_plan]
)

# Show a sample user prompt immediately when the agent module is imported.
# The ADK CLI imports this module when the agent starts, so this print will
# surface the suggested example input to the user as soon as the agent is run.
SAMPLE_PROMPT = "Provide business plan for Braking system manufacturing; Business name: ABC Business Area: Braking Systems; Business Sub-Area: Passenger Vehicles"

print("\n[AGENT PROMPT] Sample input prompt for session:")
print(SAMPLE_PROMPT, flush=True)
