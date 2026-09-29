# ==============================================================================
# PROJECT THREE: AI AUTONOMOUS ETL AGENT
# FILE SUBSYSTEM 3 OF 3: FRONT-END RENDERING USER INTERFACE ENGINE (app.py)
# DESCRIPTION: Sets up the main page tabs, interactive spreadsheet editing
#              grid, download components, and memory state anchors.
# ==============================================================================

import streamlit as st
import pandas as pd

# Pull our backend engine layers and models cleanly into the presentation template
from pipeline import run_etl_pipeline

# ------------------------------------------------------------------------------
# LAYOUT INITIALIZATION CONTEXT BLOCKS
# ------------------------------------------------------------------------------
st.set_page_config(page_title="Project 3: AI Autonomous ETL Agent", page_icon="⚙️", layout="wide")

if "etl_results" not in st.session_state:
    st.session_state.etl_results = None

# ------------------------------------------------------------------------------
# SIDEBAR RUNTIME CONTROL ENVIRONMENT PANEL
# ------------------------------------------------------------------------------
st.sidebar.header("ETL System Control Panel")
recruiter_mode = st.sidebar.toggle(
    label="Recruiter Simulator Mode", 
    value=True, 
    help="When active, this completely bypasses live external AI server calls to protect daily request limits."
)

if recruiter_mode:
    st.sidebar.success("Simulator Active: Quota Protected")
else:
    st.sidebar.warning("Live API Enabled: Consuming Quota (20 Requests per Day Limit)")

# ------------------------------------------------------------------------------
# FRONT-END USER CORE WORKSPACE SCREEN DESIGN
# ------------------------------------------------------------------------------
st.title("AI Autonomous ETL Agent")
st.caption("Project 3 Portfolio Build - Real world Business ROI Engine Modeling Complex Schema Alignments via Gemini 3.5 Flash")
st.write("Enter Vendor Record Rows Below (Data is Automatically Segregated into Structured Columns)")

# FIXED MEMORY ANCHOR: Wrap baseline data inside an absolute deterministic caching ring
# This completely blocks memory mutation crashes when Streamlit reruns.
@st.cache_data
def get_immutable_input_template():
    return pd.DataFrame([
        {"Vendor ID Code": "VND-901", "Product SKU": "PRM-BLK-XL", "Item Price": "$124.50", "Asset Qty": "42"},
        {"Vendor ID Code": "VND-901", "Product SKU": "SKU_123_ABC", "Item Price": "$89.99", "Asset Qty": "0"},
        {"Vendor ID Code": "VND-804", "Product SKU": "BAD SKU #1", "Item Price": "0.00", "Asset Qty": "25"},
        {"Vendor ID Code": "VND-101", "Product SKU": "PRM-BLU-SM", "Item Price": "$89.00", "Asset Qty": "-12"}
    ])

template_input_data = get_immutable_input_template()

# Render interactive table grid outside form blocks to fully protect interface states
edited_df = st.data_editor(
    template_input_data,
    key="vendor_data_grid",
    use_container_width=True,
    help="Edit individual grid cells directly. Data auto-segregates dynamically upon execution."
)

with st.form("etl_pipeline_form"):
    submit_button = st.form_submit_button("Execute Pipeline")
    if submit_button:
        with st.spinner("Extracting, transforming, and validating dataset..."):
            raw_csv_string = edited_df.to_csv(index=False)
            # Route processing directly through our isolated pipeline engine loop
            st.session_state.etl_results = run_etl_pipeline(raw_csv_string, recruiter_mode)

# ------------------------------------------------------------------------------
# ANALYTICS WORKSPACE: DISPLAY TABS PANELS & SPREADSHEET DISPATCH EXPORTERS
# ------------------------------------------------------------------------------
if st.session_state.etl_results:
    res = st.session_state.etl_results
    tab1, tab2, tab3 = st.tabs(["Cleaned Records", "Schema Mapping Log", "Systemic Anomalies"])
    
    with tab1:
        if res.cleaned_records:
            df_clean = pd.DataFrame([r.model_dump() for r in res.cleaned_records])
            st.dataframe(df_clean, use_container_width=True)
            st.download_button(label="Export Cleaned Records to CSV", data=df_clean.to_csv(index=False).encode('utf-8'), file_name="cleaned_records.csv", mime="text/csv")
        else:
            st.info("No records produced.")
            
    with tab2:
        if res.schema_mapping_log:
            df_map = pd.DataFrame([m.model_dump() for m in res.schema_mapping_log])
            st.dataframe(df_map, use_container_width=True)
            st.download_button(label="Export Schema Mapping Log to CSV", data=df_map.to_csv(index=False).encode('utf-8'), file_name="schema_mapping_log.csv", mime="text/csv")
        else:
            st.info("No schema mapping records logged.")
            
    with tab3:
        if res.systemic_anomalies:
            df_anom = pd.DataFrame([a.model_dump() for a in res.systemic_anomalies])
            st.dataframe(df_anom, use_container_width=True)
            st.warning("Data anomalies were recorded in the source files during mapping cycles.")
        else:
            st.success("Zero architectural or semantic errors identified within the data structure.")
