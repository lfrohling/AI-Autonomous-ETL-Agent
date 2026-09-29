# ==============================================================================
# PROJECT THREE: AI AUTONOMOUS ETL AGENT
# APPLICATION ARCHITECTURE: STREAMLIT + PYDANTIC + GOOGLE GENAI STRUCTURED LOGIC
# ==============================================================================

# Part One

import streamlit as st
import pandas as pd
import json
import re
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List, Optional
from google import genai
from google.genai import types

# ==============================================================================
# SECTION 1: SYSTEM AND PAGE CONFIGURATION INITIALIZATION
# ==============================================================================
# Sets up the wide web container layout viewport, sets page tab properties,
# and establishes persistence for the pipeline execution state variables.

st.set_page_config(
    page_title="Project 3: AI Autonomous ETL Agent", 
    page_icon="⚙️", 
    layout="wide"
)

if "etl_results" not in st.session_state:
    st.session_state.etl_results = None


# ==============================================================================
# SECTION 2: PYDANTIC LOGICAL COMPLIANCE VALIDATION DATA SCHEMA MODELS
# ==============================================================================
# Establishes runtime data models with programmatic constraints, 
# regex validations, and type-guard parameters to intercept malformed vendor inputs.

class MappedField(BaseModel):
    source_field_detected: str = Field(description="The name of the header found in the messy source data.")
    target_canonical_field: str = Field(description="The matching enterprise target standard name like vendor_id or unit_price.")
    transformation_applied: str = Field(description="The exact data scrubbing modification performed on the data format.")

class DataAnomaly(BaseModel):
    row_index: int = Field(description="Zero-indexed row placement where the validation anomaly occurred.")
    invalid_field: str = Field(description="The column name containing the logical error structure.")
    issue_description: str = Field(description="The explanation of why the entry data failed validation parameters.")

class CleanedRecord(BaseModel):
    vendor_id: str = Field(description="Standardized Alpha-Numeric ID string sequence.")
    sku_code: str = Field(description="Normalized upper-case product SKU sequence validation format.")
    unit_price: float = Field(description="Cleaned numeric floating decimal price value parameters.")
    quantity_on_hand: int = Field(description="Validated non-negative integer asset volume count numbers.")
    record_status: str = Field(description="Mark either VALIDATED or CORRUPTED based on field rules.")

    @field_validator("sku_code")
    @classmethod
    def validate_sku_format(cls, value: str) -> str:
        """
        Regex Type-Guard Validator: Enforces alphanumeric SKU segments 
        separated by hyphens or underscores (e.g., PRM-BLK-XL or SKU_123_ABC).
        """
        clean_value = value.strip().upper()
        sku_pattern = r"^[A-Z0-9]+([-_][A-Z0-9]+)*$"
        if not re.match(sku_pattern, clean_value):
            raise ValueError("SKU formatting pattern violation detected. Expected alphanumeric sequence segments separated cleanly by hyphens or underscores.")
        return clean_value

    @field_validator("quantity_on_hand")
    @classmethod
    def validate_quantity_bounds(cls, value: int) -> int:
        """
        Value Boundary Type-Guard Validator: Explicitly prevents inventory asset
        volumes from representing negative numbers under corporate tracking rules.
        """
        if value < 0:
            raise ValueError("Inventory asset volumes cannot represent negative numerical definitions.")
        return value

class ETLPipelineOutput(BaseModel):
    schema_mapping_log: List[MappedField] = Field(description="Architectural ledger detailing how the source fields matched enterprise schemas.")
    systemic_anomalies: List[DataAnomaly] = Field(description="Comprehensive catalog of semantic and physical input validation failures.")
    cleaned_records: List[CleanedRecord] = Field(description="The resulting sanitized inventory database entities.")


# ==============================================================================
# SECTION 3: SYSTEM RUNTIME SIDEBAR CONTROL PANELS
# ==============================================================================
# Renders platform switch mechanics to toggle between local offline mock 
# simulation testing and active production API calls, safeguarding request token limits.

st.sidebar.header("ETL System Control Panel")

recruiter_mode = st.sidebar.toggle(
    label="Recruiter Simulator Mode", 
    value=True, 
    help="When active, this bypasses live Gemini 3.5 execution and yields static structural responses to evaluate system routing mechanics safely."
)

if recruiter_mode:
    st.sidebar.success("Simulator Active: Quota Protected")
else:
    st.sidebar.warning("Live API Enabled: Consuming Quota (20 Requests per Day Limit)")



# Part Two

# ==============================================================================
# SECTION 4: CORE ETL PIPELINE EXECUTION LOOPS AND INTERCEPTION
# ==============================================================================
# Manages raw text parsing, structural Gemini 3.5 Flash schema mapping constraints,
# and isolated row-level transaction iteration loops to handle database payload conversions.

def process_autonomous_etl(raw_data_string: str) -> ETLPipelineOutput:
    # --- SUB-BLOCK 4A: RECRUITER SIMULATION FALLBACK TRACKING ---
    if recruiter_mode:
        return ETLPipelineOutput(
            schema_mapping_log=[
                MappedField(source_field_detected="Vendor ID Code", target_canonical_field="vendor_id", transformation_applied="Isolated alphaprefix and cast to clean string."),
                MappedField(source_field_detected="Product SKU", target_canonical_field="sku_code", transformation_applied="Parsed formatting string patterns against alphanumeric rules."),
                MappedField(source_field_detected="Item Price", target_canonical_field="unit_price", transformation_applied="Removed stray currency symbols and cast to float decimals."),
                MappedField(source_field_detected="Asset Qty", target_canonical_field="quantity_on_hand", transformation_applied="Parsed text to non-negative numerical integer sequences.")
            ],
            systemic_anomalies=[
                DataAnomaly(row_index=2, invalid_field="quantity_on_hand", issue_description="Value bounds violation: Inventory quantity cannot be a negative value (Found: -5).")
            ],
            cleaned_records=[
                CleanedRecord(vendor_id="VND-901", sku_code="PRM-BLK-XL", unit_price=124.50, quantity_on_hand=42, record_status="VALIDATED"),
                CleanedRecord(vendor_id="VND-901", sku_code="SKU_123_ABC", unit_price=89.99, quantity_on_hand=0, record_status="VALIDATED"),
                CleanedRecord(vendor_id="VND-804", sku_code="UNKN-SKU-99", unit_price=0.00, quantity_on_hand=0, record_status="CORRUPTED")
            ]
        )

    # --- SUB-BLOCK 4B: LIVE PRODUCTION GOOGLE GENAI EXECUTION ENGINE ---
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=api_key)
        
        prompt = (
            f"You are an enterprise autonomous data ETL pipeline tool. Ingest the following "
            f"tabular inventory dataset:\n{raw_data_string}\n\nYour instructions: Discover schema "
            f"relationships from the column layout and automatically map values into their correct target fields: "
            f"vendor_id, sku_code, unit_price, quantity_on_hand. Output a single valid JSON structure matching schema rules."
        )
        
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json", 
                response_schema=ETLPipelineOutput, 
                temperature=0.1
            ),
        )
        
        raw_output = ETLPipelineOutput.model_validate_json(response.text)
        validated_records = []
        
        # --- SUB-BLOCK 4C: ISOLATED TRANSACTION VALIDATION LOOP ---
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


# ==============================================================================
# SECTION 5: FRONT-END INTERACTIVE USER INTERACTION GRID INPUT SCREEN
# ==============================================================================
# Displays layout titles, prompts, and configures an advanced interactive tabular data editor
# grid component placed independently outside form blocks to fully preserve cloud interface memory states.

st.title("AI Autonomous ETL Agent")
st.caption("Project 3 Portfolio Build - Real world Business ROI Engine Modeling Complex Schema Alignments via Gemini 3.5 Flash")

st.write("Enter Vendor Record Rows Below (Data is Automatically Segregated into Structured Columns)")

# Define the base data frame properties clearly
template_input_data = pd.DataFrame([
    {"Vendor ID Code": "VND-901", "Product SKU": "PRM-BLK-XL", "Item Price": "$124.50", "Asset Qty": "42"},
    {"Vendor ID Code": "VND-901", "Product SKU": "SKU_123_ABC", "Item Price": "$89.99", "Asset Qty": "0"},
    {"Vendor ID Code": "VND-804", "Product SKU": "BAD SKU #1", "Item Price": "0.00", "Asset Qty": "25"},
    {"Vendor ID Code": "VND-101", "Product SKU": "PRM-BLU-SM", "Item Price": "$89.00", "Asset Qty": "-12"}
])

# FIXED DECOUPLING ELEMENT: Placed completely outside form limits to remove cell state modification errors
edited_df = st.data_editor(
    template_input_data,
    key="vendor_data_grid",
    use_container_width=True,
    help="Edit individual grid cells directly. Data auto-segregates dynamically upon execution."
)

with st.form("etl_pipeline_form"):
    # The unified form wrapper now encloses ONLY the processing submit trigger to insulate live executions
    submit_button = st.form_submit_button("Execute Pipeline")
    
    if submit_button:
        with st.spinner("Extracting, transforming, and validating dataset..."):
            raw_csv_string = edited_df.to_csv(index=False)
            st.session_state.etl_results = process_autonomous_etl(raw_csv_string)


# ==============================================================================
# SECTION 6: WORKSPACE DISPLAY MONITOR TABS AND EXPORT SYSTEM
# ==============================================================================
# Renders processing results in categorized tab structures, provides live alerts for tracking
# processing failures, and mounts dynamic download export utilities.

if st.session_state.etl_results:
    res = st.session_state.etl_results
    
    tab1, tab2, tab3 = st.tabs(["Cleaned Records", "Schema Mapping Log", "Systemic Anomalies"])
    
    # --- SUB-BLOCK 6A: SANITIZED RECORD DISPLAY AND DOWNLOAD ARRAYS ---
    with tab1:
        if res.cleaned_records:
            df_clean = pd.DataFrame([r.model_dump() for r in res.cleaned_records])
            st.dataframe(df_clean, use_container_width=True)
            
            csv_clean = df_clean.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Export Cleaned Records to CSV",
                data=csv_clean,
                file_name="cleaned_inventory_records.csv",
                mime="text/csv"
            )
        else:
            st.info("No records produced.")
            
    # --- SUB-BLOCK 6A: STRUCTURAL AI ALIGNMENT OPERATION AUDIT LOGS ---
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
            
    # --- SUB-BLOCK 6C: EXCEPTION ANALYTICS DISPATCH LOG LEDGERS ---
    with tab3:
        if res.systemic_anomalies:
            df_anom = pd.DataFrame([a.model_dump() for a in res.systemic_anomalies])
            st.dataframe(df_anom, use_container_width=True)
            st.warning("Data anomalies were recorded in the source files during mapping cycles.")
        else:
            st.success("Zero architectural or semantic errors identified within the data structure.")
