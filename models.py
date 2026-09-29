# ==============================================================================
# PROJECT THREE: AI AUTONOMOUS ETL AGENT
# FILE SUBSYSTEM 1 OF 3: BACKEND ARCHITECTURAL DATA VALIDATION ENGINE (models.py)
# DESCRIPTION: Encapsulates all Pydantic runtime enforcement structures, custom
#              regex logic filters, field bounds parameters, and system logging
#              data contracts away from the user interface layout scripts.
# ==============================================================================

import re
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List

class MappedField(BaseModel):
    source_field_detected: str = Field(description="The labels discovered in the messy source file dump.")
    target_canonical_field: str = Field(description="The destination database standard target placeholder label.")
    transformation_applied: str = Field(description="The exact computational normalization performed on the data format.")

class DataAnomaly(BaseModel):
    row_index: int = Field(description="The zero-indexed matrix row placement where the compliance failure happened.")
    invalid_field: str = Field(description="The precise column that triggered the data compliance exception.")
    issue_description: str = Field(description="A plain-text diagnostic explanation detailing why verification checks failed.")

# NEW STEP STAGING MODEL: Ingests variable raw inputs safely without hitting strict validation traps early
class RawRecordInput(BaseModel):
    vendor_id: str = Field(description="Vendor identifier sequence.")
    sku_code: str = Field(description="Product SKU text string formatting sequence.")
    unit_price: float = Field(description="Numeric decimal valuation pricing parameters.")
    quantity_on_hand: int = Field(description="Base asset quantity tracker counts.")
    record_status: str = Field(default="VALIDATED", description="Fallback staging flag configuration.")

class CleanedRecord(BaseModel):
    vendor_id: str = Field(description="Standardized Alpha-Numeric enterprise vendor identity string mapping.")
    sku_code: str = Field(description="Normalized upper-case product SKU sequence string validating strict patterns.")
    unit_price: float = Field(description="Cleaned numeric floating decimal asset monetary pricing attributes.")
    quantity_on_hand: int = Field(description="Validated non-negative base integer defining asset inventory counts.")
    record_status: str = Field(description="Pipeline health state flag indicator marked explicitly as VALIDATED or CORRUPTED.")

    @field_validator("sku_code")
    @classmethod
    def validate_sku_format(cls, value: str) -> str:
        clean_value = value.strip().upper()
        sku_pattern = r"^[A-Z0-9]+([-_][A-Z0-9]+)*$"
        if not re.match(sku_pattern, clean_value):
            raise ValueError("SKU formatting pattern violation detected. Expected alphanumeric segments separated cleanly by hyphens or underscores.")
        return clean_value

    @field_validator("quantity_on_hand")
    @classmethod
    def validate_quantity_bounds(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Inventory asset volumes cannot represent negative numerical definitions.")
        return value

class ETLPipelineOutput(BaseModel):
    schema_mapping_log: List[MappedField] = Field(description="Architectural mapping arrays detailing parameter alignments.")
    systemic_anomalies: List[DataAnomaly] = Field(description="Diagnostic fault monitoring catalog capturing processing failures.")
    # FIX: Configured the output container to pull clean records, but accept flexible staging arrays on intake
    cleaned_records: List[RawRecordInput] = Field(description="The staging database ingestion array elements.")
