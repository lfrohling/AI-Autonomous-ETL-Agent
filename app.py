# PROJECT THREE: AI AUTONOMOUS ETL AGENT (MERMAID WORKFLOW LINK IN REPOSITORY README)
# LAYOUT DIAGRAM DEFINITION LOCATED IN REPOSITORY README

import streamlit as st
import pandas as pd
import json
import re
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List, Optional
from google import genai
from google.genai import types

st.set_page_config(page_title="Project 3: AI Autonomous ETL Agent", page_icon="⚙️", layout="wide")

if "etl_results" not in st.session_state:
    st.session_state.etl_results = None

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
        clean_value = value.strip().upper()
        sku_pattern = r"^[A-Z0-9]+([-_][A-Z0-9]+)*$"
        if not re.match(sku_pattern, clean_value):
            raise ValueError("SKU formatting pattern violation detected. Expected alphanumeric sequence segments separated cleanly by hyphens or underscores.")
        return clean_value

    @field_validator("quantity_on_hand")
    @classmethod
    def validate_quantity_bounds(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Inventory asset volumes cannot represent negative numerical definitions.")
        return value

class ETLPipelineOutput(BaseModel):
    schema_mapping_log: List[MappedField] = Field(description="Architectural ledger detailing how the source fields matched enterprise schemas.")
    systemic_anomalies: List[DataAnomaly] = Field(description="Comprehensive catalog of semantic and physical input validation failures.")
    cleaned_records: List[CleanedRecord] = Field(description="The resulting sanitized inventory database entities.")

st.sidebar.header("ETL System Control Panel")
recruiter_mode = st.sidebar.toggle(label="Recruiter Simulator Mode", value=True, help="When active, this bypasses live Gemini 3.5 execution and yields static structural responses to evaluate system routing mechanics safely.")

if recruiter_mode:
    st.sidebar.success("Simulator Active: Quota Protected")
else:
    st.sidebar.warning("Live API Enabled: Consuming Quota (20 Requests per Day Limit)")

def process_autonomous_etl(raw_data_string: str) -> ETLPipelineOutput:
    if recruiter_mode:
        return ETLPipelineOutput(
            schema_mapping_log=[
                MappedField(source_field_detected="Vndr-Code", target_canonical_field="vendor_id", transformation_applied="Isolated alphaprefix and cast to clean string."),
                MappedField(source_field_detected="ItemCost", target_canonical_field="unit_price", transformation_applied="Removed stray dollar signs and parsed to numeric floating decimal.")
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
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=api_key)
        prompt = f"You are an enterprise autonomous data ETL pipeline tool. Ingest the following unorganized vendor data: {raw_data_string} Your instructions: Discover schema relationships and map matching columns into: vendor_id, sku_code, unit_price, quantity_on_hand. Output valid JSON parameters."
        
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
        
        for index, record in enumerate(raw_output.cleaned_records):
            try:
                CleanedRecord.model_validate(record.model_dump())
                validated_records.append(record)
            except ValidationError as ve:
                record.record_status = "CORRUPTED"
                validated_records.append(record)
                for err in ve.errors():
                    raw_output.systemic_anomalies.append(
                        DataAnomaly(row_index=index, invalid_field=str(err["loc"]), issue_description=f"Type guard violation: {err['msg']}")
                    )
        raw_output.cleaned_records = validated_records
        return raw_output
        
    except Exception as e:
        st.error(f"ETL Execution Interrupted: {str(e)}")
        st.info("Portfolio Tip: Flip on Recruiter Simulator Mode to demonstrate mock outputs.")
        return None

st.title("AI Autonomous ETL Agent")
st.caption("Project 3 Portfolio Build - Real world Business ROI Engine Modeling Complex Schema Alignments via Gemini 3.5 Flash")

default_messy_dump = "Vndr-Code | StockKeepingUnit | ItemCost | Qty\nVND-901 | PRM-BLK-XL | $124.50 | 42\nVND-901 | SKU_123_ABC | $89.99 | 0\nVND-804 | ILLEGAL SKU! | 0.00 | -5"

default_no_header_dump = "VND-901 | PRM-BLK-XL | $124.50 | 42\nVND-901 | SKU_123_ABC | $89.99 | 0\nVND-804 | BAD SKU #1 | 0.00 | -5"

with st.form("etl_pipeline_form"):
    input_text = st.text_area("Raw Vendor Data Dump (Headers Optional - AI Will Auto-Discover Columns)", value=default_no_header_dump, height=150)
    submit_button = st.form_submit_button("Execute Pipeline")
    
    if submit_button:
        with st.spinner("Extracting, transforming, and validating dataset..."):
            st.session_state.etl_results = process_autonomous_etl(input_text)


if st.session_state.etl_results:
    res = st.session_state.etl_results
    
    tab1, tab2, tab3 = st.tabs(["Cleaned Records", "Schema Mapping Log", "Systemic Anomalies"])
    
    with tab1:
        if res.cleaned_records:
            df_clean = pd.DataFrame([r.model_dump() for r in res.cleaned_records])
            st.dataframe(df_clean, use_container_width=True)
        else:
            st.info("No records produced.")
            
    with tab2:
        if res.schema_mapping_log:
            df_map = pd.DataFrame([m.model_dump() for m in res.schema_mapping_log])
            st.dataframe(df_map, use_container_width=True)
        else:
            st.info("No schema mapping records logged.")
            
    with tab3:
        if res.systemic_anomalies:
            df_anom = pd.DataFrame([a.model_dump() for a in res.systemic_anomalies])
            st.dataframe(df_anom, use_container_width=True)
            st.warning("Data anomalies were recorded in the source files during mapping cycles.")
        else:
            st.success("Zero architectural or semantic errors identified within the data structure.")
