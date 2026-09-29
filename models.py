# ==============================================================================
# PROJECT THREE: AI AUTONOMOUS ETL AGENT - BACKEND CORE ENGINE (models.py)
# ==============================================================================

import re
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List
from google import genai
from google.genai import types

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
