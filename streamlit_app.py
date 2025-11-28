import json
import os
import streamlit as st
from pathlib import Path
from datetime import datetime
import uuid
from src.services.orchestrator import Orchestrator
from src.models.profile import StudentProfile
from main import load_config, load_programs

st.set_page_config(page_title="SG Education Counselor", layout="wide")

# Initialize request history file
def save_request_history(profile, result):
    """Save request to history file for admin panel"""
    history_dir = Path("data")
    history_dir.mkdir(exist_ok=True)
    history_file = history_dir / "request_history.json"
    
    # Load existing history
    history = []
    if history_file.exists():
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        except:
            history = []
    
    # Add new record
    record = {
        "metadata": {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "session_id": str(uuid.uuid4())
        },
        "profile": profile.model_dump(),
        "result": result
    }
    history.append(record)
    
    # Save updated history
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

# Helper functions to format agent outputs
def display_programs(data):
    """Format institutional data agent output - NEW AI counselor reasoning"""
    st.markdown("### 🎓 AI Counselor Program Recommendations")
    
    # Show data source badge
    data_source = data.get("data_source", "unknown")
    if data_source == "ai_counselor_reasoning":
        st.success("🧠 AI Education Counselor analyzed your profile with curated university data")
    elif data_source == "fallback_simple_ranking":
        st.info("📊 Basic matching used (AI counselor unavailable)")
    
    programs = data.get("programs", [])
    if not programs:
        st.info("No program recommendations available.")
        return
    
    for i, prog in enumerate(programs[:5], 1):
        reasoning_type = prog.get("reasoning_type", "unknown")
        badge = "🧠 AI Counseled" if reasoning_type == "ai_counselor_reasoning" else "📊 Basic Match"
        expanded = (i == 1)
        
        title = prog.get("title", "Unknown Program")
        institution = prog.get("institution", "Unknown")
        
        with st.expander(f"#{i} {badge} - {title} @ {institution}", expanded=expanded):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**🏫 Institution:** {institution}")
                st.markdown(f"**📚 Level:** {prog.get('level', 'N/A')}")
                
                # Show AI counselor reasoning
                if prog.get("fit_reasoning"):
                    st.markdown("**🧠 Why This Fits You:**")
                    st.info(prog.get("fit_reasoning"))
                
                if prog.get("career_alignment"):
                    st.markdown("**💼 Career Potential:**")
                    st.success(prog.get("career_alignment"))
                
                # Academic requirements
                if prog.get("academic_requirements"):
                    st.markdown("**📋 Requirements:**")
                    st.markdown(prog.get("academic_requirements"))
            
            with col2:
                # Tuition fees
                fees = prog.get("tuition_fees", {})
                if isinstance(fees, dict):
                    citizen = fees.get("singapore_citizen", "N/A")
                    st.metric("Tuition (Citizen)", citizen)
                else:
                    st.metric("Tuition", fees if fees else "N/A")
                
                # Career outcomes
                outcomes = prog.get("career_outcomes", {})
                if isinstance(outcomes, dict) and outcomes.get("median_salary"):
                    st.metric("Median Salary", outcomes.get("median_salary"))

def display_career(data):
    """Format career guidance agent output"""
    st.markdown("### 💼 Career Pathways")
    
    suggestions = data.get("career_suggestions", [])
    if not suggestions:
        st.info("No career suggestions available.")
        return
    
    for career in suggestions:
        with st.expander(f"🎯 {career.get('title', 'Career Path')}", expanded=True):
            st.markdown(f"**Description:** {career.get('description', 'N/A')}")
            
            skills = career.get("required_skills", [])
            if skills:
                st.markdown("**Required Skills:**")
                st.write(" • " + "\n • ".join(skills))
            
            outlook = career.get("outlook", {})
            if outlook:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Demand", outlook.get("demand", "N/A"))
                with col2:
                    st.metric("Salary Range", outlook.get("salary_range", "N/A"))

def display_financial_aid(data):
    """Format financial aid agent output"""
    st.markdown("### 💰 Financial Assistance")
    
    options = data.get("aid_options", [])
    if not options:
        st.info("No financial aid options available.")
        return
    
    for aid in options:
        with st.expander(f"💵 {aid.get('name', 'Financial Aid')}", expanded=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**Type:** {aid.get('type', 'N/A')}")
                st.markdown(f"**Eligibility:** {aid.get('eligibility', 'N/A')}")
                st.markdown(f"**How to Apply:** {aid.get('application_process', 'N/A')}")
            with col2:
                amount = aid.get("amount", "Varies")
                st.metric("Amount", amount)

def display_admission(data):
    """Format admission advisor agent output"""
    st.markdown("### 📅 Admission Guidance")
    
    timeline = data.get("timeline", [])
    if timeline:
        st.markdown("**📆 Application Timeline:**")
        for item in timeline:
            st.markdown(f"- **{item.get('date', 'TBD')}**: {item.get('task', 'N/A')}")
    
    requirements = data.get("requirements", [])
    if requirements:
        st.markdown("**📋 Requirements:**")
        for req in requirements:
            st.markdown(f"- {req}")
    
    tips = data.get("tips", [])
    if tips:
        st.markdown("**💡 Application Tips:**")
        for tip in tips:
            st.info(tip)

def display_skills(data):
    """Format skill gap agent output"""
    st.markdown("### 🎯 Skills Analysis")
    
    current = data.get("current_skills", [])
    if current:
        st.markdown("**✅ Current Strengths:**")
        cols = st.columns(3)
        for i, skill in enumerate(current):
            with cols[i % 3]:
                st.success(f"✓ {skill}")
    
    gaps = data.get("skill_gaps", [])
    if gaps:
        st.markdown("**📚 Skills to Develop:**")
        for gap in gaps:
            with st.expander(f"🎓 {gap.get('skill', 'Skill')}", expanded=True):
                st.markdown(f"**Importance:** {gap.get('importance', 'N/A')}")
                st.markdown(f"**How to Learn:** {gap.get('learning_resources', 'N/A')}")

def display_scholarships(data):
    """Format scholarship matcher agent output"""
    st.markdown("### 🏆 Scholarship Opportunities")
    
    scholarships = data.get("scholarships", [])
    if not scholarships:
        st.info("No scholarship matches found.")
        return
    
    for scholarship in scholarships:
        with st.expander(f"🎓 {scholarship.get('name', 'Scholarship')}", expanded=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**Provider:** {scholarship.get('provider', 'N/A')}")
                st.markdown(f"**Eligibility:** {scholarship.get('eligibility', 'N/A')}")
                st.markdown(f"**Deadline:** {scholarship.get('deadline', 'N/A')}")
            with col2:
                value = scholarship.get("value", "N/A")
                st.metric("Value", value)

def display_interview(data):
    """Format interview prep agent output"""
    st.markdown("### 🗣️ Interview Preparation")
    
    questions = data.get("sample_questions", [])
    if questions:
        st.markdown("**❓ Common Interview Questions:**")
        for i, q in enumerate(questions, 1):
            with st.expander(f"Question {i}: {q.get('question', 'N/A')}", expanded=False):
                st.markdown(f"**💡 Suggested Approach:** {q.get('tips', 'N/A')}")
    
    tips = data.get("general_tips", [])
    if tips:
        st.markdown("**✨ General Tips:**")
        for tip in tips:
            st.info(tip)

def display_learning_path(data):
    """Format learning path agent output"""
    st.markdown("### 📖 Learning Roadmap")
    
    phases = data.get("learning_phases", [])
    if not phases:
        st.info("No learning path available.")
        return
    
    for i, phase in enumerate(phases, 1):
        with st.expander(f"Phase {i}: {phase.get('title', 'Learning Phase')}", expanded=(i==1)):
            st.markdown(f"**Duration:** {phase.get('duration', 'N/A')}")
            st.markdown(f"**Goals:** {phase.get('goals', 'N/A')}")
            
            resources = phase.get("resources", [])
            if resources:
                st.markdown("**📚 Resources:**")
                for resource in resources:
                    st.markdown(f"- {resource}")

def display_web_search(data):
    """Format web search agent output"""
    st.markdown("### 🌐 Real-Time University Search Results")
    
    if not data.get("enabled", True):
        st.warning("🔌 Web search is disabled. Enable Google Custom Search API for real-time results.")
        return
    
    results = data.get("search_results", [])
    if not results:
        st.info("No web search results found.")
        return
    
    # Display stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Results Found", data.get("total_results_found", 0))
    with col2:
        st.metric("Queries Used", data.get("queries_used", 0))
    
    st.markdown("---")
    
    # Display search results
    for i, result in enumerate(results[:8], 1):
        with st.expander(f"🔗 {result.get('title', 'Result')}", expanded=(i<=3)):
            st.markdown(f"**🌐 Link:** [{result.get('display_link', 'Link')}]({result.get('link', '#')})")
            st.markdown(f"**📝 Description:** {result.get('snippet', 'No description available.')}")
            st.caption(f"🔍 Query: {result.get('query', 'N/A')}")
    
    # Generate LLM summary if genai_client is available
    summary = data.get("llm_summary", "")
    if summary:
        st.markdown("---")
        st.markdown("### 🤖 AI Summary")
        st.info(summary)
    else:
        st.markdown("---")
        st.caption("💡 Tip: Click on the links above to view detailed program information directly from university websites.")

# Agent display function mapping
agent_display_functions = {
    "institutional_data": display_programs,
    "career_guidance": display_career,
    "financial_aid": display_financial_aid,
    "admission_advisor": display_admission,
    "skill_gap": display_skills,
    "scholarship_matcher": display_scholarships,
    "interview_prep": display_interview,
    "learning_path": display_learning_path,
    "web_search": display_web_search
}

# Singapore-specific data for better UX
SINGAPORE_INTERESTS = [
    # Tech & Engineering  
    "Computer Science & AI", "Data Science & Analytics", "Software Engineering",
    "Cybersecurity", "Information Systems", "Electrical Engineering",
    
    # Business & Finance
    "Business Administration", "Finance & Banking", "Accounting",
    "Marketing", "FinTech", "Real Estate",
    
    # Sciences
    "Biomedical Sciences", "Biotechnology", "Life Sciences",
    "Chemistry", "Physics", "Mathematics",
    
    # Arts & Humanities
    "Psychology", "Law", "Communications", 
    "Design", "Architecture", "Social Work"
]

SINGAPORE_STRENGTHS = [
    "Analytical Thinking", "Problem Solving", "Mathematics",
    "Programming", "Communication", "Leadership",
    "Research", "Creativity", "Teamwork",
    "Technical Skills", "Critical Thinking", "Languages"
]

st.title("🇸� Singapore Education Counselor AI")
st.caption("Intelligent multi-agent system powered by real-time university data")

config = load_config()
programs = load_programs()

if "data_store" not in st.session_state:
    st.session_state["data_store"] = {
        "programs": programs,
        "financial_aid": [
            {"name": "Need-Based Bursary", "tags": ["need"], "approx_amount": 2000},
            {"name": "Merit Scholarship", "tags": ["merit"], "approx_amount": 5000},
        ],
    }

with st.sidebar:
    st.header("📋 Your Profile")
    
    # Core Profile
    st.subheader("🎯 What are you interested in?")
    selected_interests = st.multiselect(
        "Select 1-3 areas of interest",
        options=SINGAPORE_INTERESTS,
        help="Choose specific fields you want to study",
        max_selections=3
    )
    
    if len(selected_interests) < 1:
        st.info("👆 Please select at least 1 interest to continue")
    elif len(selected_interests) > 3:
        st.warning("⚠️ Too many interests may give unfocused results")
    
    st.divider()
    
    st.subheader("💪 Your Key Strengths")
    selected_strengths = st.multiselect(
        "Select your top strengths (optional)",
        options=SINGAPORE_STRENGTHS,
        help="These help us match you with suitable programs",
        max_selections=3
    )
    
    st.divider()
    
    st.subheader("🎓 Education Details")
    
    current_level = st.selectbox(
        "Current Education Level",
        [
            "Secondary (O-Level / N-Level)",
            "Junior College (A-Level)",
            "Polytechnic Diploma",
            "IB Diploma",
            "Bachelor's Degree",
            "Other"
        ],
        help="Your highest completed or current education level"
    )
    
    target_level = st.selectbox(
        "Target Education Level", 
        [
            "Diploma / Advanced Diploma",
            "Bachelor's Degree",
            "Master's Degree",
            "PhD / Doctoral"
        ],
        index=1,
        help="What level of education are you pursuing?"
    )
    
    st.divider()
    
    st.subheader("💰 Financial Situation")
    
    citizenship = st.selectbox(
        "Citizenship Status",
        [
            "Singapore Citizen",
            "Singapore PR",
            "International Student (ASEAN)",
            "International Student (Non-ASEAN)"
        ],
        help="This affects tuition grant eligibility"
    )
    
    budget = st.selectbox(
        "Annual Budget for Tuition", 
        [
            "< S$10,000 (Need substantial financial aid)",
            "S$10,000 - S$20,000 (Need some support)",
            "S$20,000 - S$40,000 (Moderate budget)",
            "> S$40,000 (Flexible budget)"
        ],
        index=1,
        help="Estimate of what you can afford per year"
    )
    
    st.divider()
    
    st.subheader("📍 Other Preferences")
    
    start_timeline = st.selectbox(
        "When do you plan to start?",
        ["2025 (Next intake)", "2026", "2027", "Flexible"]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        part_time_ok = st.checkbox("Open to part-time")
    with col2:
        online_ok = st.checkbox("Open to online/hybrid")
    
    st.divider()
    
    # Validate before enabling button
    can_submit = len(selected_interests) >= 1 and len(selected_interests) <= 3
    
    run_btn = st.button(
        "🚀 Get AI Guidance", 
        type="primary", 
        use_container_width=True,
        disabled=not can_submit,
        help="Select 1-3 interests to enable"
    )

if run_btn:
    if not selected_interests:
        st.error("⚠️ Please select at least one interest to get personalized guidance.")
    else:
        # Build constraints from structured inputs
        constraints = []
        if part_time_ok:
            constraints.append("part-time options preferred")
        if online_ok:
            constraints.append("online/hybrid learning acceptable")
        constraints.append(f"citizenship: {citizenship}")
        constraints.append(f"start timeline: {start_timeline}")
        constraints.append(f"current level: {current_level}")
        
        # Extract budget category from selection
        if "< S$10,000" in budget:
            budget_cat = "low"
        elif "S$10,000 - S$20,000" in budget:
            budget_cat = "moderate"
        elif "S$20,000 - S$40,000" in budget:
            budget_cat = "moderate-high"
        else:
            budget_cat = "high"
        
        # Extract target level
        if "Diploma" in target_level:
            target_lvl = "diploma"
        elif "Bachelor" in target_level:
            target_lvl = "degree"
        elif "Master" in target_level:
            target_lvl = "postgrad"
        else:
            target_lvl = "phd"
        
        profile = StudentProfile(
            name="Singapore Student",  # Generic since we removed the field
            interests=selected_interests,
            strengths=selected_strengths if selected_strengths else ["General"],
            constraints=constraints,
            target_level=target_lvl,
            budget_category=budget_cat,
        )
        
        with st.spinner("🤖 AI agents analyzing your profile with live data..."):
            orch = Orchestrator(config, st.session_state["data_store"])
            result = orch.run(profile)
            
            # Save to history for admin panel
            try:
                save_request_history(profile, result)
            except Exception as e:
                # Don't break user flow if logging fails
                st.warning(f"⚠️ History logging failed: {e}")
        
        st.success("✅ Analysis complete!")
        
        # Display agent outputs in organized tabs - Only 3 core agents
        st.subheader("📊 AI Counselor Analysis Results")
        
        agent_tabs = st.tabs([
            "📚 Programs", 
            "💼 Career", 
            "💰 Financial Aid"
        ])
        
        agent_mapping = {
            "institutional_data": 0,
            "career_guidance": 1,
            "financial_aid": 2
        }
        
        for agent_name, payload in result["agents"].items():
            tab_idx = agent_mapping.get(agent_name)
            if tab_idx is None:
                continue  # Skip agents not in 3-agent system
            
            with agent_tabs[tab_idx]:
                display_func = agent_display_functions.get(agent_name)
                if display_func:
                    display_func(payload)
                else:
                    st.json(payload)
        
        if "summary" in result:
            st.subheader("📝 AI-Generated Guidance Summary")
            st.markdown(result["summary"])
        
        # Program ranking table
        if "institutional_data" in result["agents"]:
            suggestions = result["agents"]["institutional_data"].get("program_suggestions", [])
            rows = []
            for s in suggestions:
                prog = s.get("program", {})
                expl = s.get("explanation", {})
                rows.append({
                    "Program": prog.get("program"),
                    "Institution": prog.get("institution"),
                    "Score": s.get("score"),
                    "Reason": expl.get("reason"),
                    "Matched Keywords": ",".join(expl.get("matched_keywords", [])),
                })
            st.subheader("Ranked Program Suggestions")
            st.table(rows)

st.markdown("---")
st.caption("Hackathon demo – extend with real data sources & advanced retrieval.")

