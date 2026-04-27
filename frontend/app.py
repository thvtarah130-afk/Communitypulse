import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# --- CONFIG ---
API_URL = "http://localhost:8000"
st.set_page_config(
    page_title="Community Insight & Volunteer Matching",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    :root {
        --primary: #2ecc71;
        --secondary: #3498db;
        --dark: #2c3e50;
        --light: #ecf0f1;
    }
    
    .main {
        background-color: #f8f9fa;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 5px solid var(--primary);
        transition: transform 0.2s;
    }
    
    .card:hover {
        transform: translateY(-5px);
    }
    
    .urgency-high { border-left-color: #e74c3c; }
    .urgency-medium { border-left-color: #f39c12; }
    .urgency-low { border-left-color: #2ecc71; }
    
    .metric-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .sidebar .sidebar-content {
        background-color: var(--dark);
    }
    
    h1, h2, h3 {
        color: var(--dark);
        font-family: 'Inter', sans-serif;
    }
    
    .stButton>button {
        background-color: var(--secondary);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #2980b9;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# --- HELPERS ---
def get_data(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
    return []

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3062/3062337.png", width=100)
    st.title("Community Pulse")
    st.markdown("---")
    page = st.radio("Navigation", ["📊 Dashboard", "📤 Data Upload", "🧑‍🤝‍🧑 Volunteers", "🎯 Matching Results", "🤖 AI Assistant"])
    st.markdown("---")
    st.info("AI-powered community insights and volunteer optimization system.")

# --- DASHBOARD PAGE ---
if page == "📊 Dashboard":
    st.title("Community Insights Dashboard")
    
    needs = get_data("needs")
    volunteers = get_data("volunteers")
    
    if not needs:
        st.warning("No data available. Please upload community records first.")
    else:
        df_needs = pd.DataFrame(needs)
        
        # Top Row Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Needs", len(df_needs))
        with col2:
            high_urgency = len(df_needs[df_needs['urgency'] == 'high'])
            st.metric("High Urgency", high_urgency, delta=f"{high_urgency/len(df_needs)*100:.1f}%", delta_color="inverse")
        with col3:
            total_people = df_needs['people_affected'].sum()
            st.metric("People Affected", f"{total_people:,}")
        with col4:
            st.metric("Volunteers", len(volunteers))
            
        st.markdown("---")
        
        # Charts Row
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("Needs by Category")
            fig_pie = px.pie(df_needs, names='issue_type', 
                             color_discrete_sequence=px.colors.qualitative.Pastel,
                             hole=0.4)
            fig_pie.update_layout(showlegend=True, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with c2:
            st.subheader("Urgency Levels")
            urgency_counts = df_needs['urgency'].value_counts().reindex(['low', 'medium', 'high']).fillna(0)
            fig_bar = px.bar(x=urgency_counts.index, y=urgency_counts.values, 
                             color=urgency_counts.index,
                             color_discrete_map={'high': '#e74c3c', 'medium': '#f39c12', 'low': '#2ecc71'})
            fig_bar.update_layout(xaxis_title="Urgency", yaxis_title="Count", showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
            
        st.markdown("---")
        
        # Top 5 Urgent Needs
        st.subheader("🔥 Top 5 Critical Needs")
        top_5 = df_needs.head(5)
        for _, row in top_5.iterrows():
            urgency_class = f"urgency-{row['urgency']}"
            st.markdown(f"""
            <div class="card {urgency_class}">
                <div style="display: flex; justify-content: space-between;">
                    <h3>{row['issue_type'].title()} - {row['location']}</h3>
                    <span style="background: {'#ffebee' if row['urgency'] == 'high' else '#fff3e0' if row['urgency'] == 'medium' else '#e8f5e9'}; 
                                 padding: 0.2rem 0.8rem; border-radius: 20px; font-weight: bold;">
                        {row['urgency'].upper()}
                    </span>
                </div>
                <p>{row['description']}</p>
                <div style="font-size: 0.9rem; color: #666;">
                    👥 <b>{row['people_affected']}</b> people affected | 📍 Lat: {row['lat']:.4f}, Lon: {row['lon']:.4f}
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- DATA UPLOAD PAGE ---
elif page == "📤 Data Upload":
    st.title("Data Aggregation & Input")
    
    tab1, tab2 = st.tabs(["批量上传 (CSV)", "手动输入 (Manual)"])
    
    with tab1:
        st.info("Upload CSV files containing community survey data or NGO reports.")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file:
            if st.button("Process & Upload Data"):
                with st.spinner("Analyzing and cleaning data..."):
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                    res = requests.post(f"{API_URL}/upload-data", files=files)
                    if res.status_code == 200:
                        st.success(res.json()["message"])
                        st.balloons()
                    else:
                        st.error("Failed to upload data.")
                        
        st.markdown("### Sample CSV Format")
        st.code("location,lat,lon,issue_type,description,urgency,people_affected\nBrooklyn,40.6782,-73.9442,health,Need for medical supplies,high,150")

    with tab2:
        st.subheader("Add a New Community Need")
        with st.form("need_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                loc = st.text_input("Location Name")
                lat = st.number_input("Latitude", format="%.6f", value=40.7128)
                itype = st.selectbox("Issue Type", ["auto", "health", "food", "education", "infrastructure", "other"])
            with col2:
                urg = st.selectbox("Urgency", ["low", "medium", "high"])
                lon = st.number_input("Longitude", format="%.6f", value=-74.0060)
                people = st.number_input("People Affected", min_value=1, value=1)
            
            desc = st.text_area("Detailed Description")
            
            submit = st.form_submit_button("Submit Record")
            
            if submit:
                payload = {
                    "location": loc, "lat": lat, "lon": lon, "issue_type": itype,
                    "description": desc, "urgency": urg, "people_affected": people
                }
                res = requests.post(f"{API_URL}/add-need", json=payload)
                if res.status_code == 200:
                    st.success("Community need successfully added!")
                else:
                    st.error("Error adding record.")

# --- VOLUNTEERS PAGE ---
elif page == "🧑‍🤝‍🧑 Volunteers":
    st.title("Volunteer Management")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Register Volunteer")
        with st.form("vol_form", clear_on_submit=True):
            v_name = st.text_input("Name")
            v_skills = st.text_input("Skills (comma separated)")
            v_avail = st.selectbox("Availability", ["Full-time", "Weekends", "Mon-Wed", "Evenings"])
            v_loc = st.text_input("Location")
            v_lat = st.number_input("Latitude", format="%.6f", value=40.7128)
            v_lon = st.number_input("Longitude", format="%.6f", value=-74.0060)
            
            v_submit = st.form_submit_button("Add Volunteer")
            if v_submit:
                payload = {
                    "name": v_name, "skills": v_skills, "availability": v_avail,
                    "location": v_loc, "lat": v_lat, "lon": v_lon
                }
                res = requests.post(f"{API_URL}/add-volunteer", json=payload)
                if res.status_code == 200:
                    st.success(f"Volunteer {v_name} registered!")
                else:
                    st.error("Error registering volunteer.")
                    
    with col2:
        st.subheader("Current Volunteer Pool")
        vols = get_data("volunteers")
        if vols:
            df_vols = pd.DataFrame(vols)
            st.dataframe(df_vols[['name', 'skills', 'availability', 'location']], use_container_width=True)
        else:
            st.info("No volunteers registered yet.")

# --- MATCHING PAGE ---
elif page == "🎯 Matching Results":
    st.title("Smart Volunteer Matching")
    
    st.markdown("""
    This engine uses an **AI-driven algorithm** to match volunteers to the most critical needs based on:
    - **Skill Alignment** (Match volunteer skills to issue types)
    - **Geographic Proximity** (Minimize travel distance)
    - **Urgency Priority** (Focus on high-urgency areas)
    """)
    
    if st.button("🚀 Calculate Optimal Matches"):
        with st.spinner("Running matching algorithm..."):
            time.sleep(1) # Visual effect
            matches = get_data("match")
            if matches:
                st.session_state['matches'] = matches
                st.success(f"Found {len(matches)} optimal assignments!")
            else:
                st.warning("Could not find suitable matches with current data.")
                
    if 'matches' in st.session_state:
        matches = st.session_state['matches']
        
        # Get details for visualization
        needs = get_data("needs")
        vols = get_data("volunteers")
        
        if needs and vols:
            need_dict = {n['id']: n for n in needs}
            vol_dict = {v['id']: v for v in vols}
            
            display_data = []
            for m in matches:
                n = need_dict.get(m['issue_id'])
                v = vol_dict.get(m['volunteer_id'])
                if n and v:
                    display_data.append({
                        "Match Score": f"{m['score']:.1f}%",
                        "Volunteer": v['name'],
                        "Assigned Task": f"{n['issue_type'].title()} at {n['location']}",
                        "Urgency": n['urgency'].upper(),
                        "Skills Used": v['skills']
                    })
            
            df_matches = pd.DataFrame(display_data)
            
            # Highlight Areas Lacking Volunteers
            all_issue_ids = [n['id'] for n in needs]
            matched_issue_ids = [m['issue_id'] for m in matches]
            unmatched_issues = [need_dict[iid] for iid in all_issue_ids if iid not in matched_issue_ids and need_dict[iid]['urgency'] == 'high']
            
            if unmatched_issues:
                st.error("⚠️ **Critical areas lacking volunteers:**")
                for ui in unmatched_issues[:3]:
                    st.write(f"- **{ui['location']}**: {ui['issue_type']} ({ui['people_affected']} affected)")
            
            st.markdown("---")
            st.subheader("Assignment List")
            st.table(df_matches)
            
            # Map Visualization
            st.subheader("Geographic Distribution of Matches")
            map_data = []
            for m in matches:
                n = need_dict.get(m['issue_id'])
                if n:
                    map_data.append(n)
            
            if map_data:
                df_map = pd.DataFrame(map_data)
                fig_map = px.scatter_mapbox(df_map, lat="lat", lon="lon", hover_name="location", 
                                            hover_data=["issue_type", "urgency"],
                                            color="urgency", size="people_affected",
                                            color_discrete_map={'high': '#e74c3c', 'medium': '#f39c12', 'low': '#2ecc71'},
                                            zoom=10, height=500)
# --- AI ASSISTANT PAGE ---
elif page == "🤖 AI Assistant":
    st.title("🤖 Gemini AI Assistant")
    st.markdown("""
    Ask anything about the community needs, volunteer matches, or geographic hotspots. 
    The AI has access to the current database context.
    """)
    
    from chatbot import get_chat_response
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I help you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Fetch context
            needs = get_data("needs")
            vols = get_data("volunteers")
            context = f"Needs: {needs[:10]}... Volunteers: {vols[:10]}..." # Limit context size
            
            with st.spinner("Thinking..."):
                response = get_chat_response(prompt, context)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
