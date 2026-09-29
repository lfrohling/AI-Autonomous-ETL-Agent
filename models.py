# ==============================================================================
# PROJECT THREE: AI AUTONOMOUS ETL AGENT
# FILE SUBSYSTEM: BACKEND ARCHITECTURAL DATA VALIDATION ENGINE (models.py)
# DESCRIPTION: Encapsulates all Pydantic runtime enforcement structures, custom
#              regex logic filters, field bounds parameters, and system logging
#              data frames away from the main user interface presentation script.
# ==============================================================================

import re
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List

# ------------------------------------------------------------------------------
# SCHEMA LOG MODEL A: SCHEMA MAPPING ADJUSTMENTS LEDGER ENTRIES
# ------------------------------------------------------------------------------
# Defines a structural database entity engineered to trace and audit exactly 
# how unorganized external vendor layout variables align with internal corporate standards.
class MappedField(BaseModel):
    source_field_detected: str = Field(
        description="The physical structural label or column text discovered in the messy source file dump."
    )
    target_canonical_field: str = Field(
        description="The matching database destination format placeholder standard entity name (e.g., vendor_id, sku_code)."
    )
    transformation_applied: str = Field(
        description="The exact computational normalization, data type cast, or text stripping modification rule performed."
    )

# ------------------------------------------------------------------------------
# SCHEMA LOG MODEL B: SYSTEMIC SYSTEM RUNTIME EXCEPTION LEDGER ENTRIES
# ------------------------------------------------------------------------------
# Defines a strict error-tracking object that logs specific, isolated data line validation
# errors for analytics tracking, ensuring full visibility into compliance failures.
class DataAnomaly(BaseModel):
    row_index: int = Field(
        description="The absolute zero-indexed matrix location placement identifier where the schema validation check failed."
    )
    invalid_field: str = Field(
        description="The precise structural object property sequence or column that triggered the data compliance exception."
    )
    issue_description: str = Field(
        description="A plain-text diagnostic explanation detailing why the parsed record failed strict backend parameter checks."
    )

# ------------------------------------------------------------------------------
# SCHEMA LOG MODEL C: CANONICAL ENTERPRISE SANITIZED DATA RECORD STRUCTURE
# ------------------------------------------------------------------------------
# The primary transactional blueprint containing strict type-guard definitions.
# This component acts as the ultimate gatekeeper for your relational tables.
class CleanedRecord(BaseModel):
    vendor_id: str = Field(
        description="Standardized Alpha-Numeric enterprise vendor tracking identity string sequence parameters."
    )
    sku_code: str = Field(
        description="Normalized upper-case product SKU sequence string validating strict formatting matching patterns."
    )
    unit_price: float = Field(
        description="Cleaned numeric floating decimal asset monetary pricing evaluation attributes."
    )
    quantity_on_hand: int = Field(
        description="Validated non-negative base integer sequence defining asset volumes physically located in storage arrays."
    )
    record_status: str = Field(
        description="Pipeline health state flag indicator marked explicitly as either VALIDATED or CORRUPTED based on field status checks."
    )

    @field_validator("sku_code")
    @classmethod
    def validate_sku_format(cls, value: str) -> str:
        """
        REGULAR EXPRESSION VALIDATION SYSTEM:
        Processes string input variables by stripping trailing whitespace, converting
        characters to uppercase, and enforcing a strict multi-segmented alphanumeric structure
        joined cleanly by hyphens or underscores (e.g., 'PRM-BLK-XL' or 'SKU_123_ABC').
        """
        clean_value = value.strip().upper()
        # Matches alphanumeric string blocks safely separated by dashes or underscores
        sku_pattern = r"^[A-Z0-9]+([-_][A-Z0-9]+)*$"
        if not re.match(sku_pattern, clean_value):
            raise ValueError(
                "SKU formatting pattern violation detected. Expected alphanumeric sequence segments separated cleanly by hyphens or underscores."
            )
        return clean_value

    @field_validator("quantity_on_hand")
    @classmethod
    def validate_quantity_bounds(cls, value: int) -> int:
        """
        VALUE BOUNDARY LIMIT TYPE-GUARD CHECK:
        Enforces asset quantity restrictions. Under corporate enterprise logic rules, 
        inventory volumes can never represent negative numerical definitions.
        """
        if value < 0:
            raise ValueError(
                "Inventory asset volumes cannot represent negative numerical definitions."
            )
        return value

# ------------------------------------------------------------------------------
# SCHEMA LOG MODEL D: CORE MASTER PIPELINE UNIFIED DATA PACKAGE CONTRACT
# ------------------------------------------------------------------------------
# Defines the absolute structured response envelope layout that contracts the 
# generative AI model outputs and manages overall transactional array conversions.
class ETLPipelineOutput(BaseModel):
    schema_mapping_log: List[MappedField] = Field(
        description="Architectural ledger arrays detailing exactly how various unstructured vendor parameters were assigned into structural standards."
    )
    systemic_anomalies: List[DataAnomaly] = Field(
        description="Comprehensive diagnostic fault monitoring catalog capturing semantic and physical layout compliance failures."
    )
    cleaned_records: List[CleanedRecord] = Field(
        description="The resulting collection array of clean, verified, and parsed inventory entity models ready for relational table streaming."
    )
