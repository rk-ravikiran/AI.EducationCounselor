import streamlit as st
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="Admin Panel - Request History", layout="wide")

# Main admin panel
st.title("🔧 Admin Panel - Request History")
st.markdown("---")

# Load request history
history_file = Path("data/request_history.json")

if not history_file.exists():
    st.warning("📂 No request history found yet. History will be saved once users submit requests.")
    st.stop()

try:
    with open(history_file, "r", encoding="utf-8") as f:
        history = json.load(f)
except Exception as e:
    st.error(f"❌ Error loading history: {e}")
    st.stop()

if not history:
    st.info("📭 No requests recorded yet.")
    st.stop()

# Convert to DataFrame for better display
records = []
for record in history:
    profile = record.get("profile", {})
    metadata = record.get("metadata", {})
    result = record.get("result", {})
    
    # Count recommendations
    agents = result.get("agents", {})
    num_programs = len(agents.get("institutional_data", {}).get("programs", []))
    num_careers = len(agents.get("career_guidance", {}).get("career_suggestions", []))
    num_aid = len(agents.get("financial_aid", {}).get("aid_options", []))
    
    records.append({
        "Timestamp": metadata.get("timestamp", "N/A"),
        "Session ID": metadata.get("session_id", "N/A")[:8],
        "Interests": ", ".join(profile.get("interests", [])),
        "Target Level": profile.get("target_level", "N/A"),
        "Budget": profile.get("budget_category", "N/A"),
        "Programs": num_programs,
        "Careers": num_careers,
        "Aid Options": num_aid,
    })

df = pd.DataFrame(records)

# Stats overview
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Total Requests", len(history))
with col2:
    st.metric("🎓 Avg Programs/Request", f"{df['Programs'].mean():.1f}")
with col3:
    st.metric("💼 Avg Careers/Request", f"{df['Careers'].mean():.1f}")
with col4:
    st.metric("💰 Avg Aid/Request", f"{df['Aid Options'].mean():.1f}")

st.markdown("---")

# Filters
st.subheader("🔍 Filters")
col1, col2 = st.columns(2)

with col1:
    filter_interest = st.multiselect(
        "Filter by Interest",
        options=sorted(set([interest for record in history for interest in record.get("profile", {}).get("interests", [])])),
        default=[]
    )

with col2:
    filter_level = st.multiselect(
        "Filter by Target Level",
        options=sorted(set([record.get("profile", {}).get("target_level", "N/A") for record in history])),
        default=[]
    )

# Apply filters
filtered_records = records
if filter_interest:
    filtered_records = [r for i, r in enumerate(records) if any(interest in history[i].get("profile", {}).get("interests", []) for interest in filter_interest)]

if filter_level:
    filtered_records = [r for i, r in enumerate(records) if history[i].get("profile", {}).get("target_level") in filter_level]

# Display filtered table
st.subheader(f"📋 Request History ({len(filtered_records)} records)")
filtered_df = pd.DataFrame(filtered_records)
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# Detailed view
st.markdown("---")
st.subheader("🔎 View Request Details")

request_options = [f"{r['Timestamp']} - {r['Session ID']}" for r in filtered_records]
if request_options:
    selected = st.selectbox("Select a request to view details:", request_options)
    
    if selected:
        idx = request_options.index(selected)
        original_idx = records.index(filtered_records[idx])
        selected_record = history[original_idx]
        
        tab1, tab2, tab3 = st.tabs(["📝 Profile", "🤖 Results", "📄 Raw JSON"])
        
        with tab1:
            st.json(selected_record.get("profile", {}))
        
        with tab2:
            result = selected_record.get("result", {})
            
            # Summary
            if "summary" in result:
                st.markdown("**AI Summary:**")
                st.info(result["summary"])
            
            # Agent outputs
            agents = result.get("agents", {})
            
            if "institutional_data" in agents:
                st.markdown("**🎓 Programs Recommended:**")
                for prog in agents["institutional_data"].get("programs", [])[:3]:
                    st.write(f"- {prog.get('title')} @ {prog.get('institution')}")
            
            if "career_guidance" in agents:
                st.markdown("**💼 Career Suggestions:**")
                for career in agents["career_guidance"].get("career_suggestions", [])[:3]:
                    st.write(f"- {career.get('title')}")
            
            if "financial_aid" in agents:
                st.markdown("**💰 Financial Aid Options:**")
                for aid in agents["financial_aid"].get("aid_options", [])[:3]:
                    st.write(f"- {aid.get('name')}")
        
        with tab3:
            st.json(selected_record)

# Export functionality
st.markdown("---")
st.subheader("📥 Export Data")
col1, col2 = st.columns(2)

with col1:
    if st.button("💾 Download History as JSON"):
        st.download_button(
            label="⬇️ Download JSON",
            data=json.dumps(history, indent=2),
            file_name=f"request_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

with col2:
    if st.button("📊 Download Summary as CSV"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name=f"request_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
