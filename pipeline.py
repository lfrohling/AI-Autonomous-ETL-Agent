# ==============================================================================
# PROJECT THREE: AI AUTONOMOUS ETL AGENT
# FILE SUBSYSTEM 2 OF 3: THE PROCESSING PIPELINE CORE ENGINE (pipeline.py)
# DESCRIPTION: Orchestrates transactional record validation cycles, handles
#              structured JSON content generation, and intercepts row-level exceptions.
# ==============================================================================

import streamlit as st
import pandas as pd
from google import genai
from google.genai import types
from pydantic import ValidationError

# Bring in our data contract components cleanly from models.py
from models import MappedField, DataAnomaly, CleanedRecord, ETLPipelineOutput

def run_etl_pipeline(raw_data_string: str, recruiter_mode: bool) -> ETLPipelineOutput:
    """Executes structural data parsing via Mock Simulator or Live GenAI endpoints."""
    
    # --- PROCESS LOOP A: RECRUITER SIMULATION FALLBACK TRACKING ---
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

    # --- PROCESS LOOP B: LIVE PRODUCTION GOOGLE GENAI INFERENCE ENGINE ---
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
        
        # ROW-BY-ROW ISOLATION LOOP: Intercepts single malformed strings without dropping execution
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
