import streamlit as st
from groq import Groq
import os

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BuildWise AI",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a1628, #0d2137, #0f2744);
    min-height: 100vh;
}

[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04);
    border-right: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
}

.build-header {
    background: linear-gradient(135deg, rgba(6,182,212,0.2), rgba(16,185,129,0.2));
    border: 1px solid rgba(6,182,212,0.35);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
}

.build-header h1 {
    background: linear-gradient(90deg, #38bdf8, #34d399, #facc15);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -1px;
}

.build-header p {
    color: rgba(255,255,255,0.6);
    font-size: 1.1rem;
    margin-top: 0.5rem;
}

.result-box {
    background: rgba(10,22,40,0.9);
    border: 1px solid rgba(56,189,248,0.25);
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 1rem;
    color: #e2e8f0;
    line-height: 1.8;
    white-space: pre-wrap;
    font-size: 0.95rem;
}

.stat-card {
    background: rgba(6,182,212,0.08);
    border: 1px solid rgba(6,182,212,0.2);
    border-radius: 14px;
    padding: 1.25rem;
    text-align: center;
}

.stat-card h3 {
    color: #38bdf8;
    font-size: 1.8rem;
    font-weight: 800;
    margin: 0;
}

.stat-card p {
    color: rgba(255,255,255,0.5);
    font-size: 0.8rem;
    margin: 0.25rem 0 0;
}

.stButton > button {
    background: linear-gradient(135deg, #0891b2, #0d9488) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
    width: 100%;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #0e7490, #0f766e) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(6,182,212,0.4) !important;
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] > div,
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

label, .stMarkdown p {
    color: rgba(255,255,255,0.82) !important;
}

.metric-badge {
    display: inline-block;
    background: rgba(56,189,248,0.15);
    border: 1px solid rgba(56,189,248,0.35);
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-size: 0.8rem;
    color: #38bdf8;
    font-weight: 600;
    margin: 0.2rem;
}

.section-title {
    color: #38bdf8;
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    border-left: 4px solid #38bdf8;
    padding-left: 0.75rem;
}

div[data-testid="stTabs"] button {
    color: rgba(255,255,255,0.6) !important;
    font-weight: 600 !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #38bdf8 !important;
    border-bottom-color: #38bdf8 !important;
}

[data-testid="stSlider"] > div > div > div {
    background: #0891b2 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Groq Client ───────────────────────────────────────────────────────────────
MODEL = "llama-3.3-70b-versatile"

def call_ai(prompt: str, system: str = "You are BuildWise, an expert AI construction planning engineer.") -> str:
    api_key = st.session_state.get("groq_api_key", "")
    if not api_key:
        return "⚠️ Please enter your Groq API key in the sidebar."
    try:
        client = Groq(api_key=api_key)
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            max_tokens=2000,
            temperature=0.4,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="color:#38bdf8;font-size:1.1rem;font-weight:700;margin-bottom:1rem;">⚙️ Configuration</div>', unsafe_allow_html=True)
    groq_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    if groq_key:
        st.session_state["groq_api_key"] = groq_key

    st.markdown("---")
    st.markdown("""
    <div style='color:rgba(255,255,255,0.5); font-size:0.8rem;'>
    <b style='color:#38bdf8'>Model:</b> llama-3.3-70b-versatile<br><br>
    <b style='color:#38bdf8'>Features:</b><br>
    💰 Cost Estimation<br>
    📦 Resource Planning<br>
    📅 Schedule Generation<br>
    📐 Blueprint Insights<br>
    🔧 Project Optimization<br>
    💬 Construction Assistant
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<span class="metric-badge">Llama 3.3-70B</span><span class="metric-badge">Groq</span>', unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="build-header">
    <h1>🏗️ BuildWise AI</h1>
    <p>Generative AI–Powered Construction Planning Platform</p>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs(["💰 Cost Estimation", "📦 Resource Planning", "📅 Schedule Generation", "📐 Blueprint Insights", "🔧 Project Optimization", "💬 Construction AI"])

# ── Tab 1: Cost Estimation ────────────────────────────────────────────────────
with tabs[0]:
    st.markdown('<div class="section-title">💰 AI Cost Estimator</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        proj_type = st.selectbox("Project Type", ["Residential Building", "Commercial Complex", "Industrial Facility", "Road/Infrastructure", "Bridge", "Hospital", "School/College", "Shopping Mall"])
        location = st.text_input("Project Location", placeholder="e.g. Mumbai, Maharashtra")
    with col2:
        area = st.number_input("Total Area (sq ft)", min_value=100, max_value=10000000, value=5000, step=100)
        floors = st.number_input("Number of Floors", min_value=1, max_value=200, value=3, step=1)
    with col3:
        quality = st.selectbox("Construction Quality", ["Economy", "Standard", "Premium", "Luxury"])
        currency = st.selectbox("Currency", ["INR (₹)", "USD ($)", "EUR (€)", "GBP (£)"])

    special_req = st.text_area("Special Requirements / Features", placeholder="e.g. basement parking, swimming pool, solar panels, smart home systems...", height=80)

    if st.button("💰 Generate Cost Estimate", key="cost"):
        with st.spinner("Calculating detailed cost estimate..."):
            prompt = f"""Generate a detailed construction cost estimate for the following project:

Project Type: {proj_type}
Location: {location}
Total Area: {area} sq ft
Number of Floors: {floors}
Quality Grade: {quality}
Currency: {currency}
Special Requirements: {special_req if special_req else 'None'}

Provide a COMPREHENSIVE breakdown including:
1. Executive Summary (Total Estimated Cost with min-max range)
2. Cost Breakdown by Category:
   - Foundation & Earthwork
   - Structure (RCC/Steel)
   - Brickwork & Masonry
   - Plumbing & Sanitation
   - Electrical Work
   - Flooring
   - Doors & Windows
   - Painting & Finishing
   - HVAC / Air Conditioning
   - External Development
   - Contingency (10%)
3. Cost per sq ft analysis
4. Material Cost vs Labour Cost Split
5. Equipment & Machinery Costs
6. Regulatory & Approval Costs
7. Timeline Impact on Cost
8. Cost Saving Recommendations

Format as a professional cost estimate report with a clear table."""
            result = call_ai(prompt, system="You are a senior quantity surveyor and construction cost estimator with 20+ years of experience. Provide accurate, data-backed cost estimates.")
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

# ── Tab 2: Resource Planning ──────────────────────────────────────────────────
with tabs[1]:
    st.markdown('<div class="section-title">📦 Resource Planning Engine</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        rp_project = st.text_input("Project Name & Type", placeholder="e.g. Skyline Tower - 20-floor Residential")
        rp_duration = st.number_input("Project Duration (months)", min_value=1, max_value=120, value=18)
        rp_budget = st.text_input("Total Budget", placeholder="e.g. ₹5 Crore, $500,000")
    with col2:
        rp_workers = st.number_input("Expected Workforce Size", min_value=5, max_value=5000, value=50)
        rp_location = st.text_input("Site Location", placeholder="e.g. Pune, Maharashtra")
        rp_special = st.text_area("Key Project Constraints", placeholder="e.g. monsoon season, restricted hours, union rules...", height=80)

    if st.button("📦 Generate Resource Plan", key="resource"):
        with st.spinner("Generating comprehensive resource plan..."):
            prompt = f"""Create a detailed resource planning document for:

Project: {rp_project}
Duration: {rp_duration} months
Total Budget: {rp_budget}
Workforce Size: {rp_workers} workers
Location: {rp_location}
Constraints: {rp_special if rp_special else 'None'}

Include:
1. Human Resources Plan
   - Skilled workers breakdown by trade (masons, electricians, plumbers, carpenters, etc.)
   - Management hierarchy (site engineer, foreman, supervisor)
   - Monthly workforce requirements per phase
2. Material Resources
   - Primary materials list with quantities (cement, steel, bricks, sand, aggregate, etc.)
   - Procurement strategy and timing
   - Material storage requirements
3. Equipment & Machinery
   - Required equipment list with durations
   - Own vs rent decision matrix
4. Sub-contractor Requirements
5. Resource Leveling Strategy
6. Risk Mitigation for Resource Shortages
7. Resource Cost Summary Table

Make it structured and actionable for a project manager."""
            result = call_ai(prompt)
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

# ── Tab 3: Schedule Generation ────────────────────────────────────────────────
with tabs[2]:
    st.markdown('<div class="section-title">📅 Project Schedule Generator</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        sc_project = st.text_input("Project Description", placeholder="e.g. 5-floor commercial building, 15,000 sqft")
        sc_start = st.date_input("Project Start Date")
        sc_months = st.number_input("Total Duration (months)", min_value=1, max_value=120, value=12)
    with col2:
        sc_method = st.selectbox("Scheduling Method", ["CPM (Critical Path Method)", "Gantt Chart Based", "Agile / Phased Approach", "Fast-Track"])
        sc_shifts = st.selectbox("Work Shifts", ["Single Shift (8h)", "Double Shift (16h)", "Round-the-Clock (24h)"])
        sc_constraints = st.text_area("Constraints / Milestones", placeholder="e.g. structure by month 4, handover by Dec...", height=80)

    if st.button("📅 Generate Project Schedule", key="schedule"):
        with st.spinner("Building your project schedule..."):
            prompt = f"""Generate a detailed construction project schedule for:

Project: {sc_project}
Start Date: {sc_start}
Total Duration: {sc_months} months
Scheduling Method: {sc_method}
Work Shifts: {sc_shifts}
Constraints & Milestones: {sc_constraints if sc_constraints else 'None'}

Provide:
1. Project Phases Overview with % completion targets
2. Detailed Activity Schedule (Week-by-week for first month, then month-by-month):
   - Pre-construction (approvals, design finalization, mobilization)
   - Substructure (foundation, basement)
   - Superstructure (columns, beams, slabs floor by floor)
   - External Works (facade, roofing)
   - Internal Works (partition, plumbing, electrical, HVAC)
   - Finishing Works (flooring, painting, fixtures)
   - Commissioning & Handover
3. Key Milestones with dates
4. Critical Path Activities (activities with zero float)
5. Buffer Time Allocation
6. Weather/Seasonal Risk Windows
7. Inspection & QA Checkpoints
8. A simple text-based Gantt representation

Be precise with timelines and dependencies."""
            result = call_ai(prompt)
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

# ── Tab 4: Blueprint Insights ─────────────────────────────────────────────────
with tabs[3]:
    st.markdown('<div class="section-title">📐 Blueprint & Design Insights</div>', unsafe_allow_html=True)
    st.info("Describe your blueprint or upload design specifications to get AI-powered insights, optimization suggestions, and compliance checks.", icon="📐")

    col1, col2 = st.columns(2)
    with col1:
        bp_type = st.selectbox("Blueprint Type", ["Floor Plan", "Structural Drawing", "Electrical Layout", "Plumbing/MEP", "Foundation Plan", "Elevation Drawing", "Site Plan"])
        bp_area = st.text_input("Total Area / Dimensions", placeholder="e.g. 50m x 40m, G+4 floors")
    with col2:
        bp_purpose = st.selectbox("Building Purpose", ["Residential", "Commercial", "Industrial", "Healthcare", "Educational", "Mixed Use"])
        bp_standard = st.selectbox("Building Code / Standard", ["IS Codes (India)", "ASTM (USA)", "BS (UK)", "Eurocode (EU)", "IBC (International)"])

    bp_description = st.text_area("Describe your design / Layout Details", placeholder="Describe the layout, key spaces, structural elements, unusual features, or paste plan notes...", height=150)

    if st.button("📐 Analyze Blueprint", key="blueprint"):
        with st.spinner("Analyzing design and generating insights..."):
            prompt = f"""Analyze the following construction blueprint/design and provide expert insights:

Blueprint Type: {bp_type}
Area/Dimensions: {bp_area}
Building Purpose: {bp_purpose}
Building Code: {bp_standard}
Design Description:
{bp_description}

Provide:
1. Design Assessment Summary
2. Structural Analysis Points
   - Load-bearing elements evaluation
   - Span recommendations
   - Foundation requirements
3. Space Utilization Analysis (efficiency score and recommendations)
4. Building Code Compliance Check ({bp_standard})
   - Setback requirements
   - FAR/FSI compliance
   - Fire safety requirements
   - Accessibility (ADA/barrier-free)
5. MEP (Mechanical, Electrical, Plumbing) Considerations
6. Sustainability & Green Building Recommendations
7. Potential Design Issues / Red Flags
8. Optimization Suggestions (cost savings, efficiency improvements)
9. Recommended Structural System
10. Material Specifications recommended

Be technical yet practical."""
            result = call_ai(prompt, system="You are a senior structural engineer and architect with expertise in construction design, building codes, and sustainable building practices.")
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

# ── Tab 5: Project Optimization ───────────────────────────────────────────────
with tabs[4]:
    st.markdown('<div class="section-title">🔧 Project Optimization Engine</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        opt_project = st.text_area("Project Description & Current Status", placeholder="Describe your project, what work is done, current issues...", height=120)
        opt_budget_used = st.slider("Budget Consumed (%)", 0, 100, 40)
    with col2:
        opt_timeline = st.slider("Timeline Consumed (%)", 0, 100, 35)
        opt_delay = st.number_input("Current Delay (weeks)", min_value=0, max_value=52, value=2)
        opt_issues = st.text_area("Current Issues / Pain Points", placeholder="e.g. material shortage, labour conflicts, weather delays, design changes...", height=120)

    if st.button("🔧 Optimize Project", key="optimize"):
        with st.spinner("Analyzing and generating optimization strategies..."):
            prompt = f"""Perform a comprehensive construction project optimization analysis:

Project: {opt_project}
Budget Consumed: {opt_budget_used}%
Timeline Consumed: {opt_timeline}%
Current Delay: {opt_delay} weeks
Issues: {opt_issues if opt_issues else 'None reported'}

Provide:
1. Project Health Dashboard
   - Schedule Performance Index (SPI)
   - Cost Performance Index (CPI) 
   - Overall Project Health Score (0-100)
   - Red/Yellow/Green status indicators
2. Root Cause Analysis of Delays/Issues
3. Crash Program Options (accelerating the schedule)
   - Fast-tracking opportunities
   - Resource reallocation strategies
   - Overtime and additional shift plans
4. Cost Recovery Strategies
5. Risk Register (top 5 risks with mitigation)
6. Immediate Action Plan (next 4 weeks)
7. 90-Day Recovery Roadmap
8. Stakeholder Communication Recommendations
9. Technology Solutions to Implement
10. Revised Completion Forecast

Be data-driven and actionable."""
            result = call_ai(prompt, system="You are a senior construction project manager and PMP-certified professional with expertise in project recovery and optimization.")
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

# ── Tab 6: Construction AI Chat ────────────────────────────────────────────────
with tabs[5]:
    st.markdown('<div class="section-title">💬 Construction AI Assistant</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:rgba(255,255,255,0.5); font-size:0.9rem;">Ask anything about construction planning, engineering, materials, codes, or project management.</p>', unsafe_allow_html=True)

    if "build_chat" not in st.session_state:
        st.session_state.build_chat = []

    for msg in st.session_state.build_chat:
        if msg["role"] == "user":
            st.markdown(f"""<div style="background:rgba(8,145,178,0.2);border:1px solid rgba(8,145,178,0.3);border-radius:12px;padding:0.75rem 1rem;margin:0.5rem 0;color:#e2e8f0;">
            <b style="color:#38bdf8">You:</b> {msg['content']}</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:0.75rem 1rem;margin:0.5rem 0;color:#e2e8f0;">
            <b style="color:#34d399">BuildWise AI:</b> {msg['content']}</div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Ask your construction question...", placeholder="e.g. What mix ratio for M25 concrete? How to manage monsoon delays?", key="build_input", label_visibility="collapsed")
    with col2:
        send = st.button("Send →", key="build_send")

    if send and user_input:
        st.session_state.build_chat.append({"role": "user", "content": user_input})
        history_prompt = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.build_chat[-6:]])
        with st.spinner("Generating response..."):
            response = call_ai(
                history_prompt,
                system="You are BuildWise, an expert AI construction engineer and project planner. Provide accurate, technical, and actionable advice on construction, engineering, materials, codes, project management, and cost optimization."
            )
        st.session_state.build_chat.append({"role": "assistant", "content": response})
        st.rerun()

    if st.button("🗑️ Clear Chat", key="build_clear"):
        st.session_state.build_chat = []
        st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:rgba(255,255,255,0.3); font-size:0.8rem; padding:1rem 0;">
    🏗️ BuildWise AI — Powered by <b style="color:#38bdf8">llama-3.3-70b-versatile</b> via Groq &nbsp;|&nbsp; Built with Streamlit
</div>
""", unsafe_allow_html=True)
