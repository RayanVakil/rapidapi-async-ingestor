import re
from typing import Any, Optional
from pydantic import BaseModel, field_validator

class Make(BaseModel):
    """Schema for extracting the vehicle make name."""
    name: str

class MakeModel(BaseModel):
    """Schema for extracting the vehicle model name."""
    name: str
    make: Make

class MakeModelTrim(BaseModel):
    """Schema for extracting the MSRP and nested make/model data."""
    msrp: Optional[float] = None
    make_model: MakeModel

class MileageData(BaseModel):
    """
    Schema for the core mileage data object.
    Validates combined_mpg, fuel_tank_capacity, and the nested make_model_trim tree.
    """
    combined_mpg: Optional[float] = None
    fuel_tank_capacity: float
    make_model_trim: MakeModelTrim

    @field_validator("fuel_tank_capacity", mode="before")
    @classmethod
    def parse_fuel_tank_capacity(cls, value: Any) -> float:
        """
        Strips any non-numeric text (e.g., 'gal', 'L') from fuel_tank_capacity 
        and casts it to a float. Handles missing/empty values gracefully.
        """
        if isinstance(value, (int, float)):
            return float(value)
        
        if isinstance(value, str):
            match = re.search(r"[\d\.]+", value)
            if match:
                return float(match.group())
                
        return 0.0

class MileageResponse(BaseModel):
    """Root schema for the /api/mileages response payload."""
    data: MileageData

    @field_validator("data", mode="before")
    @classmethod
    def extract_first_item(cls, value: Any) -> Any:
        """
        Defensively extracts the first item if the API returns a list under 'data',
        ensuring robust schema mapping to a single MileageData object.
        """
        if isinstance(value, list) and len(value) > 0:
            return value[0]
        return value
