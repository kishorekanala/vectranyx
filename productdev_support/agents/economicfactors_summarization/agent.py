import os
import glob
from bs4 import BeautifulSoup
from google.adk.agents.llm_agent import Agent

# Define the paths
BASE_DIR = "/Users/kishore/myprojects/vectranyx/reports/marketresearch/businessareaanalysis"
OUTPUT_FILE = os.path.join(BASE_DIR, "businessareas_economicfactors_summary.html")

def parse_all_factors():
    """
    Scans the marketresearch/businessareaanalysis directory for HTML files,
    parses their vector registries, and extracts Business Area, Industry Sector,
    Macroeconomic Factors, and Microeconomic Factors.
    """
    html_files = glob.glob(os.path.join(BASE_DIR, "*.html"))
    results = []
    
    for filepath in html_files:
        filename = os.path.basename(filepath)
        # Skip index.html and our summary file itself
        if filename in ["index.html", "businessareas_economicfactors_summary.html"]:
            continue
            
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
                
            registry_sec = soup.find("section", class_="vector-registry")
            if not registry_sec:
                # If no vector-registry section, skip or log it
                continue
                
            bus_area = ""
            ind_sector = ""
            macro = ""
            micro = ""
            
            # Find all divs containing spans and strongs/ps
            divs = registry_sec.find_all("div")
            for div in divs:
                span = div.find("span")
                if not span:
                    continue
                label = span.get_text(strip=True).lower()
                
                strong = div.find("strong")
                p = div.find("p")
                if strong:
                    val = strong.get_text(strip=True)
                elif p:
                    val = p.get_text(strip=True)
                else:
                    val = div.get_text(strip=True)
                    span_val = span.get_text(strip=True)
                    if val.startswith(span_val):
                        val = val[len(span_val):].strip()
                
                # Clean up leading bullet points
                val = val.lstrip("•").strip()
                
                if "business area" in label or "component area" in label:
                    bus_area = val
                elif "industry sector" in label:
                    ind_sector = val
                elif "macroeconomic" in label:
                    macro = val
                elif "microeconomic" in label:
                    micro = val
            
            # If we didn't extract values properly, try fallback based on sibling patterns or paragraphs
            if not bus_area and not ind_sector:
                continue
                
            results.append({
                "file": filename,
                "business_area": bus_area,
                "industry_sector": ind_sector,
                "macro_factors": macro,
                "micro_factors": micro
            })
        except Exception as e:
            print(f"Error parsing {filename}: {e}", flush=True)
            
    # Sort results by Industry Sector first, then Business Area
    results.sort(key=lambda x: (x["industry_sector"], x["business_area"]))
    return results

def generate_summary_html() -> str:
    """
    Invokes parsing of all files and outputs a premium glassmorphic HTML summary table.
    """
    records = parse_all_factors()
    if not records:
        return "Error: No data records parsed from sector HTML files."
        
    # Build HTML rows
    rows_html = ""
    for r in records:
        rows_html += f"""
                <tr>
                    <td class="col-business">{r['business_area']}</td>
                    <td class="col-sector">{r['industry_sector']}</td>
                    <td class="col-macro">{r['macro_factors']}</td>
                    <td class="col-micro">{r['micro_factors']}</td>
                </tr>"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Economic Factors Summarization Registry</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-dark: hsl(222, 24%, 6%);
            --bg-grid: hsl(222, 24%, 9%);
            --card-bg: rgba(15, 23, 42, 0.65);
            --card-border: rgba(255, 255, 255, 0.08);
            --text-primary: hsl(210, 40%, 98%);
            --text-secondary: hsl(215, 25%, 72%);
            --text-muted: hsl(215, 16%, 50%);
            --accent-cyan: hsl(190, 80%, 45%);
            --accent-mist: hsl(185, 45%, 65%);
            --accent-glow: rgba(6, 182, 212, 0.15);
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
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.07) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(6, 182, 212, 0.04) 0px, transparent 50%);
            background-attachment: fixed;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        header {{
            text-align: center;
            margin-bottom: 3rem;
            position: relative;
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
            font-size: 2.8rem;
            font-weight: 700;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.75rem;
            letter-spacing: -0.5px;
        }}
        .subtitle {{
            color: var(--text-secondary);
            font-weight: 300;
            font-size: 1.1rem;
            max-width: 800px;
            margin: 0 auto 2rem auto;
        }}
        
        /* Control bar with Search */
        .control-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            gap: 1.5rem;
            flex-wrap: wrap;
        }}
        .search-container {{
            position: relative;
            flex-grow: 1;
            max-width: 500px;
        }}
        .search-input {{
            width: 100%;
            padding: 0.8rem 1.2rem 0.8rem 2.8rem;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--card-border);
            border-radius: 30px;
            color: var(--text-primary);
            font-family: var(--font-inter);
            font-size: 0.95rem;
            outline: none;
            transition: all 0.3s ease;
        }}
        .search-input:focus {{
            border-color: var(--accent-cyan);
            box-shadow: 0 0 15px var(--accent-glow);
        }}
        .search-icon {{
            position: absolute;
            left: 1.1rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
        }}
        .stats-badge {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--card-border);
            padding: 0.6rem 1.2rem;
            border-radius: 30px;
            font-size: 0.88rem;
            color: var(--text-secondary);
            font-family: var(--font-outfit);
            font-weight: 500;
        }}
        
        /* Glassmorphic Table Container */
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
            font-size: 0.82rem;
            letter-spacing: 0.5px;
            color: var(--text-primary);
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
            padding: 1.2rem 1rem;
            cursor: pointer;
            user-select: none;
            position: relative;
            transition: color 0.3s ease;
        }}
        th:hover {{
            color: var(--accent-mist);
        }}
        th::after {{
            content: " ↕";
            font-size: 0.75rem;
            opacity: 0.5;
            margin-left: 5px;
            position: relative;
        }}
        td {{
            padding: 1.2rem 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            color: var(--text-secondary);
            font-size: 0.92rem;
            font-weight: 300;
            line-height: 1.5;
            vertical-align: top;
        }}
        tr:hover td {{
            background: rgba(255, 255, 255, 0.01);
            color: var(--text-primary);
        }}
        
        .col-business {{
            font-weight: 500;
            color: var(--text-primary);
            width: 25%;
        }}
        .col-sector {{
            color: var(--accent-cyan);
            font-weight: 500;
            width: 20%;
        }}
        .col-macro {{
            width: 27%;
        }}
        .col-micro {{
            width: 28%;
        }}
        
        /* Empty results row style */
        .no-results {{
            display: none;
            text-align: center;
            padding: 3rem;
            color: var(--text-muted);
            font-size: 1.1rem;
        }}
        
        /* Floating Back button */
        .back-button {{
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--text-secondary);
            text-decoration: none;
            font-family: var(--font-outfit);
            font-weight: 500;
            font-size: 0.9rem;
            border: 1px solid var(--card-border);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.02);
            transition: all 0.3s ease;
        }}
        .back-button:hover {{
            color: var(--text-primary);
            border-color: var(--accent-cyan);
            background: rgba(6, 182, 212, 0.05);
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <a href="index.html" class="back-button">
                <span>←</span> Central Portal
            </a>
            <span class="badge">Consolidated Asset Intelligence</span>
            <h1>Business Areas & Economic Factors Summary</h1>
            <p class="subtitle">A cross-sector registry analyzing systemic macroeconomic factors and operational microeconomic risks across key asset business areas.</p>
        </header>
        
        <div class="control-bar">
            <div class="search-container">
                <span class="search-icon">🔍</span>
                <input type="text" id="search-input" class="search-input" placeholder="Search by business area, sector, or factors..." onkeyup="filterTable()">
            </div>
            <div class="stats-badge" id="stats-badge">
                Showing {len(records)} Business Areas
            </div>
        </div>
        
        <div class="registry-card">
            <table id="summary-table">
                <thead>
                    <tr>
                        <th onclick="sortTable(0)" style="width: 25%;">Business Area</th>
                        <th onclick="sortTable(1)" style="width: 20%;">Industry Sector</th>
                        <th onclick="sortTable(2)" style="width: 27%;">Macroeconomic Factors</th>
                        <th onclick="sortTable(3)" style="width: 28%;">Microeconomic Factors</th>
                    </tr>
                </thead>
                <tbody id="table-body">
                    {rows_html}
                </tbody>
            </table>
            <div id="no-results-msg" class="no-results">
                No matching business areas found.
            </div>
        </div>
    </div>

    <script>
        function filterTable() {{
            const input = document.getElementById("search-input");
            const filter = input.value.toLowerCase();
            const tbody = document.getElementById("table-body");
            const trs = tbody.getElementsByTagName("tr");
            let visibleCount = 0;
            
            for (let i = 0; i < trs.length; i++) {{
                const tds = trs[i].getElementsByTagName("td");
                let match = false;
                for (let j = 0; j < tds.length; j++) {{
                    if (tds[j].textContent.toLowerCase().includes(filter)) {{
                        match = true;
                        break;
                    }}
                }}
                if (match) {{
                    trs[i].style.display = "";
                    visibleCount++;
                }} else {{
                    trs[i].style.display = "none";
                }}
            }}
            
            // Update match count stats
            const stats = document.getElementById("stats-badge");
            stats.textContent = `Showing ${{visibleCount}} of {len(records)} Business Areas`;
            
            // Show no results message if none found
            const noResults = document.getElementById("no-results-msg");
            if (visibleCount === 0) {{
                noResults.style.display = "block";
            }} else {{
                noResults.style.display = "none";
            }}
        }}

        let sortDirections = [true, true, true, true];
        function sortTable(colIndex) {{
            const table = document.getElementById("summary-table");
            const tbody = document.getElementById("table-body");
            const rows = Array.from(tbody.querySelectorAll("tr"));
            const descending = !sortDirections[colIndex];
            
            rows.sort((rowA, rowB) => {{
                const cellA = rowA.getElementsByTagName("td")[colIndex].textContent.trim();
                const cellB = rowB.getElementsByTagName("td")[colIndex].textContent.trim();
                return cellA.localeCompare(cellB) * (descending ? -1 : 1);
            }});
            
            // Clear existing rows
            while (tbody.firstChild) {{
                tbody.removeChild(tbody.firstChild);
            }}
            
            // Append sorted rows
            rows.forEach(row => tbody.appendChild(row));
            
            // Toggle directions
            sortDirections[colIndex] = !sortDirections[colIndex];
        }}
    </script>
</body>
</html>"""
    
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(html_content)
        return f"Successfully generated summary table with {len(records)} records at {OUTPUT_FILE}."
    except Exception as e:
        return f"Error writing summary HTML file: {str(e)}"

# Setup the ADK agent
root_agent = Agent(
    model='gemini-2.5-flash',
    name='economicfactors_summarization_agent',
    description='An ADK agent that parses all sector market research files and generates a single-page HTML report summarizing macroeconomic and microeconomic factor vectors.',
    instruction="""
    You are the Senior Macroeconomic Analyst and Intelligence Compiler.
    Your objective is to read the sector market research HTML files in the `marketresearch/businessareaanalysis/` directory and compile their B2B vector factor registry information into a clean, consolidated HTML file named `businessareas_economicfactors_summary.html`.
    
    When executing:
    1. Call the `generate_summary_html` tool to parse all HTML files in `reports/marketresearch/businessareaanalysis/` and compile the factors into a structured table.
    2. Read the results of the execution and output a clean Markdown summary report of the sectors and business areas compiled.
    """,
    tools=[
        generate_summary_html
    ]
)
