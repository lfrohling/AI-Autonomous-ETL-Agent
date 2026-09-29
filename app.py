# ==============================================================================
# PROJECT THREE: AI AUTONOMOUS ETL AGENT
# FILE SUBSYSTEM: FRONT-END RENDERING USER INTERFACE ENGINE (app.py - PART 1)
# DESCRIPTION: Manages the core presentation workspace tabs, interactive data
#              grid operations, simulation toggle nodes, and CSV export loops.
# ==============================================================================

# Part One

import streamlit as st
import pandas as pd
from google import genai
from google.genai import types
from pydantic import ValidationError

# NATIVE SYSTEM INTEGRATION LAYER:
# Imports the full suite of specialized architectural validation components and data contracts
# directly from models.py to decouple presentation loops completely from parsing models.
from models import MappedField, DataAnomaly, CleanedRecord, ETLPipelineOutput

# ------------------------------------------------------------------------------
# LAYOUT INITIALIZATION CONTEXT BLOCKS
# ------------------------------------------------------------------------------
# Configures global screen space bounds for a wide professional presentation layout
# and initializes the local interactive web session state tracking variables.
st.set_page_config(
    page_title="Project 3: AI Autonomous ETL Agent", 
    page_icon="⚙️", 
    layout="wide"
)

if "etl_results" not in st.session_state:
    st.session_state.etl_results = None

# ------------------------------------------------------------------------------
# SIDEBAR RUNTIME CONTROL ENVIRONMENT PANEL
# ------------------------------------------------------------------------------
# Mounts explicit user switches to prevent credential leaking, isolate workflows, 
# and safely demonstrate execution routing features to hiring managers without depleting key tokens.
st.sidebar.header("ETL System Control Panel")

recruiter_mode = st.sidebar.toggle(
    label="Recruiter Simulator Mode", 
    value=True, 
    help="When active, this completely bypasses live external AI server calls to protect daily request limits while yielding structural response sets."
)

if recruiter_mode:
    st.sidebar.success("Simulator Active: Quota Protected")
else:
    st.sidebar.warning("Live API Enabled: Consuming Quota (20 Requests per Day Limit)")

# ------------------------------------------------------------------------------
# PROCESSING ENGINE: LOGICAL ASYNC SCHEDULER OPERATIONS
# ------------------------------------------------------------------------------
# Orchestrates transactional record validation cycles, transforms interface variables, 
# and uses individual try-except blocks to catch row-level exceptions smoothly.
def process_autonomous_etl(raw_data_string: str) -> ETLPipelineOutput:
    
    # SYSTEM PATH A: DETERMINISTIC FALLBACK MOCK DATA INJECTION
    if recruiter_mode:
        return ETLPipelineOutput(
            schema_mapping_log=[
                MappedField(source_field_detected="Vendor ID Code", target_canonical_field="vendor_id", transformation_applied="Isolated alphaprefix and cast to clean string."),
                MappedField(source_field_detected="Product SKU", target_canonical_field="sku_code", transformation_applied="Parsed formatting string patterns against alphanumeric rules."),
                MappedField(source_field_detected="Item Price", target_canonical_field="unit_price", transformation_applied="Removed stray currency symbols and cast to float decimals."),
                MappedField(source_field_detected="Asset Qty", target_canonical_field="quantity_on_hand", transformation_applied="Parsed text to non-negative numerical integer sequences.")
            ],
            systemic_anomalies=[
                DataAnomaly(row_index=3, invalid_field="quantity_on_hand", issue_description="Value bounds violation: Inventory quantity cannot be a negative value (Found: -12)."),
                DataAnomaly(row_index=2, invalid_field="sku_code", issue_description="Type guard violation: SKU formatting pattern violation detected. Expected alphanumeric sequence segments separated cleanly by hyphens or underscores.")
            ],
            cleaned_records=[
                CleanedRecord(vendor_id="VND-901", sku_code="PRM-BLK-XL", unit_price=124.50, quantity_on_hand=42, record_status="VALIDATED"),
                CleanedRecord(vendor_id="VND-901", sku_code="SKU_123_ABC", unit_price=89.99, quantity_on_hand=0, record_status="VALIDATED"),
                CleanedRecord(vendor_id="VND-804", sku_code="UNKN-SKU-99", unit_price=0.00, quantity_on_hand=25, record_status="CORRUPTED"),
                CleanedRecord(vendor_id="VND-101", sku_code="PRM-BLU-SM", unit_price=89.00, quantity_on_hand=0, record_status="CORRUPTED")
            ]
        )

    # SYSTEM PATH B: LIVE INFERENCE TRANSACTION PROCESSING LOGIC
    try:
        # Accesses secure credentials safely from the host environment vault block
        api_key = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=api_key)
        
        prompt = (
            f"You are an enterprise autonomous data ETL pipeline tool. Ingest the following "
            f"tabular inventory dataset:\n{raw_data_string}\n\nYour instructions: Discover schema "
            f"relationships from the column layout and automatically map values into their correct target fields: "
            f"vendor_id, sku_code, unit_price, quantity_on_hand. Output a single valid JSON structure matching schema rules."
        )
        
        # Requests structured JSON formatting output that strictly maps to the data output contract model
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json", 
                response_schema=ETLPipelineOutput, 
                temperature=0.1
            ),
        )
        
        # Validates base response schema attributes completely
        raw_output = ETLPipelineOutput.model_validate_json(response.text)
        validated_records = []
        
        # ROW-BY-ROW ISOLATION LOOP MECHANISM:
        # Iterates over individual row models sequentially. If a specific index row contains 
        # bad data, it converts its status to CORRUPTED and logs the precise error metrics 
        # inside the monitoring ledger, preventing complete application failure.
        for index, record in enumerate(raw_output.cleaned_records):
            try:
                CleanedRecord.model_validate(record.model_dump())
                validated_records.append(record)
            except ValidationError as ve:
                record.record_status = "CORRUPTED"
                validated_records.append(record)
                for err in ve.errors():
                    raw_output.systemic_anomalies.append(
                        DataAnomaly(
                            row_index=index, 
                            invalid_field=str(err["loc"] if err["loc"] else "Field"), 
                            issue_description=f"Type guard violation: {err['msg']}"
                        )
                    )
                    
        raw_output.cleaned_records = validated_records
        return raw_output
        
    except Exception as e:
        st.error(f"ETL Execution Interrupted: {str(e)}")
        st.info("Portfolio Tip: Flip on Recruiter Simulator Mode to demonstrate mock outputs safely.")
        return None


# Part Two

# ==============================================================================
# SECTION 5: FRONT-END USER CORE WORKSPACE SCREEN DESIGN
# ==============================================================================
# Renders presentation titles, application descriptors, captions, and text blocks.
st.title("AI Autonomous ETL Agent")
st.caption("Project 3 Portfolio Build - Real world Business ROI Engine Modeling Complex Schema Alignments via Gemini 3.5 Flash")

st.write("Enter Vendor Record Rows Below (Data is Automatically Segregated into Structured Columns)")

# Baseline testing dataframe profile (Contains 2 fully clear rows, and 2 target validation error tests)
template_input_data = pd.DataFrame([
    {"Vendor ID Code": "VND-901", "Product SKU": "PRM-BLK-XL", "Item Price": "$124.50", "Asset Qty": "42"},
    {"Vendor ID Code": "VND-901", "Product SKU": "SKU_123_ABC", "Item Price": "$89.99", "Asset Qty": "0"},
    {"Vendor ID Code": "VND-804", "Product SKU": "BAD SKU #1", "Item Price": "0.00", "Asset Qty": "25"},
    {"Vendor ID Code": "VND-101", "Product SKU": "PRM-BLU-SM", "Item Price": "$89.00", "Asset Qty": "-12"}
])

# CRITICAL SCREEN DESIGN REFACTOR:
# Placed completely independent and above the form statement box. This avoids state mutations, 
# enables spreadsheet data cell typing changes, and stops page-load TypeError framework crashes.
edited_df = st.data_editor(
    template_input_data,
    key="vendor_data_grid",
    use_container_width=True,
    help="Edit individual grid cells directly. Data auto-segregates dynamically upon execution."
)

# Unified isolated form block safely contains ONLY the standalone pipeline submission trigger execution button
with st.form("etl_pipeline_form"):
    submit_button = st.form_submit_button("Execute Pipeline")
    
    if submit_button:
        with st.spinner("Extracting, transforming, and validating dataset..."):
            # flattens row configurations into clean flat CSV raw data text strings for processing
            raw_csv_string = edited_df.to_csv(index=False)
            st.session_state.etl_results = process_autonomous_etl(raw_csv_string)

# ------------------------------------------------------------------------------
# ANALYTICS WORKSPACE: DISPLAY TABS PANELS & SPREADSHEET DISPATCH EXPORTERS
# ------------------------------------------------------------------------------
# Evaluates existing database states and splits information fields across tabbed grid segments.
if st.session_state.etl_results:
    res = st.session_state.etl_results
    
    tab1, tab2, tab3 = st.tabs(["Cleaned Records", "Schema Mapping Log", "Systemic Anomalies"])
    
    # WORKSPACE SUB-BLOCK A: COMPLIANT RECORD MATRICES & EXPORTERS
    with tab1:
        if res.cleaned_records:
            df_clean = pd.DataFrame([r.model_dump() for r in res.cleaned_records])
            st.dataframe(df_clean, use_container_width=True)
            
            # Converts the pandas table block cleanly into downloadable text array files instantly
            csv_clean = df_clean.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Export Cleaned Records to CSV",
                data=csv_clean,
                file_name="cleaned_inventory_records.csv",
                mime="text/csv"
            )
        else:
            st.info("No records produced.")
            
    # WORKSPACE SUB-BLOCK B: AI HEURISTIC MAPPING TRACE LOG RECORDS
    with tab2:
        if res.schema_mapping_log:
            df_map = pd.DataFrame([m.model_dump() for m in res.schema_mapping_log])
            st.dataframe(df_map, use_container_width=True)
            
            csv_map = df_map.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Export Schema Mapping Log to CSV",
                data=csv_map,
                file_name="schema_mapping_log.csv",
                mime="text/csv"
            )
        else:
            st.info("No schema mapping records logged.")
            
    # WORKSPACE SUB-BLOCK C: EXCEPTION LEDGER GRAPH RECORDS & ALERTS
    with tab3:
        if res.systemic_anomalies:
            df_anom = pd.DataFrame([a.model_dump() for a in res.systemic_anomalies])
            st.dataframe(df_anom, use_container_width=True)
            st.warning("Data anomalies were recorded in the source files during mapping cycles.")
        else:
            st.success("Zero architectural or semantic errors identified within the data structure.")
