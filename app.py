# =========================================================
# PROJECT #3: AI AUTONOMOUS ETL AGENT
# DOCUMENTATION: [MERMAID DIAGRAM INSERTED HERE]
# =========================================================
import streamlit as st
import pandas as pd
import json
from pydantic import BaseModel, Field
from typing import List, Optional
from google import genai
from google.genai import types

# ---------------------------------------------------------
# STAGE 1: SYSTEM ENVIRONMENT & ARCHITECTURE SETUP
# ---------------------------------------------------------
st.set_page_config(
    page_title="Project 3: Autonomous B2B Data Validation and ETL Mapping Agent",
    page_icon="⚙️",
    layout="wide"
)

if "etl_results" not in st.session_state:
    st.session_state.etl_results = None

# ---------------------------------------------------------
# STAGE 2: PYDANTIC ORCHESTRATION COMPLIANCE SCHEMAS
# ---------------------------------------------------------
class MappedField(BaseModel):
    source_field_detected: str = Field(description="The name of the header found in the messy source data.")
    target_canonical_field: str = Field(description="The matching enterprise target standard name (e.g., vendor_id, unit_price).")
    transformation_applied: str = Field(description="The exact data scrubbing modification performed (e.g., Stripped currency symbols, parsed string to ISO-8601).")

class DataAnomaly(BaseModel):
    row_index: int = Field(description="Zero-indexed row placement where the anomaly occurred.")
    invalid_field: str = Field(description="The column name containing the logical error.")
    issue_description: str = Field(description="The explanation of the anomaly (e.g., negative inventory count, missing email domain, mismatched data types).")

class CleanedRecord(BaseModel):
    vendor_id: str = Field(description="Standardized Alpha-Numeric ID string.")
    sku_code: str = Field(description="Normalized upper-case product SKU sequence.")
    unit_price: float = Field(description="Cleaned numeric floating decimal price value.")
    quantity_on_hand: int = Field(description="Validated non-negative integer asset volume count.")
    record_status: str = Field(description="Mark either 'VALIDATED' or 'CORRUPTED'.")

class ETLPipelineOutput(BaseModel):
    schema_mapping_log: List[MappedField] = Field(description="Architectural ledger detailing how the source fields matched enterprise schemas.")
    systemic_anomalies: List[DataAnomaly] = Field(description="Comprehensive catalog of semantic and physical input validation failures.")
    cleaned_records: List[CleanedRecord] = Field(description="The resulting sanitized inventory database entities.")

# ---------------------------------------------------------
# STAGE 3: SIDEBAR CONTROL PANEL & API GUARDRAILS
# ---------------------------------------------------------
st.sidebar.header("ETL System Control Panel")

recruiter_mode = st.sidebar.toggle(
    label="Recruiter Simulator Mode",
    value=True,
    help="When active, this bypasses live Gemini 3.5 execution and yields static structural responses to evaluate system routing mechanics safely."
)

if recruiter_mode:
    st.sidebar.success("Simulator Active: Quota Protected")
else:
    st.sidebar.warning("Live API Enabled: Consuming Quota (20 RPM/Day Limit)")

# ---------------------------------------------------------
# STAGE 4: AUTONOMOUS MAPPING & VALIDATION PIPELINE ENGINE
# ---------------------------------------------------------
def process_autonomous_etl(raw_data_string: str) -> ETLPipelineOutput:
    """Ingests messy vendor raw content dumps and models them into a unified ETL structure framework."""
    if recruiter_mode:
        return ETLPipelineOutput(
            schema_mapping_log=[
                MappedField(source_field_detected="Vndr-Code", target_canonical_field="vendor_id", transformation_applied="Isolated alphaprefix and cast to clean string."),
                MappedField(source_field_detected="ItemCost", target_canonical_field="unit_price", transformation_applied="Removed stray dollar signs and parsed to numeric floating decimal.")
            ],
            systemic_anomalies=[
                DataAnomaly(row_index=2, invalid_field="quantity_on_hand", issue_description="Detected a string literal BACKORDERED inside an expected integer field bounds.")
            ],
            cleaned_records=[
                CleanedRecord(vendor_id="VND-901", sku_code="PRM-BLK-XL", unit_price=124.50, quantity_on_hand=42, record_status="VALIDATED"),
                CleanedRecord(vendor_id="VND-901", sku_code="PRM-WHT-MD", unit_price=89.99, quantity_on_hand=0, record_status="VALIDATED"),
                CleanedRecord(vendor_id="VND-804", sku_code="ERR-SKU-99", unit_price=0.00, quantity_on_hand=0, record_status="CORRUPTED")
            ]
        )
    
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are an enterprise-grade autonomous data ETL engineering pipeline tool.
        Ingest the following unorganized, chaotic vendor input dump:
        ---
        {raw_data_string}
        ---
        Your mandate:
        1. Discover data relationships and map messy column variants into our target canonical schema:
           - Target Canonical Fields: vendor_id, sku_code, unit_price, quantity_on_hand
        2. Identify and flag semantic row errors (e.g., text found within numbers, missing codes, negative value bounds).
        3. Parse the valid outputs into strict compliance variables. Reject trailing spaces and formatting artifacts.
        """
        
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ETLPipelineOutput,
                temperature=0.1,
            ),
        )
        return ETLPipelineOutput.model_validate_json(response.text)
        
    except Exception as e:
        st.error(f"ETL Execution Interrupted: {str(e)}")
        st.info("Portfolio Tip: Flip on Recruiter Simulator Mode to demonstrate mock system outputs immediately.")
        return None

# ---------------------------------------------------------
# STAGE 5: UI ORCHESTRATION LAYER & FORM ATOM
# ---------------------------------------------------------
st.title("Autonomous B2B Data Validation and ETL Mapping Agent")
st.caption("Project 3 Portfolio Build - Real-world Business ROI Engine Modeling Complex Schema Alignments via Gemini 3.5 Flash")

default_messy_dump = """Vndr-Code | StockKeepingUnit | ItemCost | Qty_Avail
VND-901   | PRM-BLK-XL       | $124.50  | 42
VND-901   | PRM-WHT-MD       | $89.99   | 0
VND-804   | ERR-SKU-99       | FREE     | BACKORDERED"""

with st.form("etl_pipeline_form"):
    st.subheader("Source Data Ingestion Window")
    st.text("Drop messy CSV data fragments, pipe-delimited values, or mismatched vendor tables below:")
    
    raw_input = st.text_area(
        label="Raw System Extract String Dump",
        value=default_messy_dump,
        height=180,
        placeholder="Paste text blocks extracted from raw logistics data streams..."
    )
    
    execute_button = st.form_submit_button("Execute Autonomous Schema Alignment", type="primary")

if execute_button:
    if not raw_input.strip():
        st.warning("Data submission container is empty. Please enter raw content to align.")
    else:
        with st.spinner("Analyzing columns, verifying constraints, and generating structural records..."):
            pipeline_payload = process_autonomous_etl(raw_input)
            if pipeline_payload:
                st.session_state.etl_results = pipeline_payload

# ---------------------------------------------------------
# STAGE 6: DISCRETE SCHEMATIC PRESENTATION LAYER
# ---------------------------------------------------------
if st.session_state.etl_results:
    st.write("---")
    st.success("Data Ingestion Sequence Complete")
    
    tab1, tab2, tab3 = st.tabs(["Cleaned Canonical Records", "Header Mapping Log", "Systemic Anomalies Log"])
    
    with tab1:
        st.subheader("Database Ready Outputs")
        records = [r.model_dump() for r in st.session_state.etl_results.cleaned_records]
        if records:
            df_clean = pd.DataFrame(records)
            st.dataframe(df_clean, use_container_width=True)
            
            csv_data = df_clean.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Export Sanitized CSV to ERP System",
                data=csv_data,
                file_name="canonical_etl_export.csv",
                mime="text/csv"
            )
        else:
            st.info("No records successfully survived validation layers.")
            
    with tab2:
        st.subheader("Schema Resolution Matrix")
        mappings = [m.model_dump() for m in st.session_state.etl_results.schema_mapping_log]
        if mappings:
            st.table(mappings)
        else:
            st.info("No explicit schema mutations were required.")
            
    with tab3:
        st.subheader("Integrity Enforcement Summary")
        anomalies = [a.model_dump() for a in st.session_state.etl_results.systemic_anomalies]
        if anomalies:
            st.warning(f"Detected anomalies inside source formatting parameters.")
            st.table(anomalies)
        else:
            st.success("Zero architectural or value constraints violated across incoming streams.")
