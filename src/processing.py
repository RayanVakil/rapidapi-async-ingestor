import logging
import pandas as pd
from typing import List, Dict, Any
from src.models.schemas import MileageResponse

logger = logging.getLogger(__name__)

def process_mileage_data(target_ids: List[int], mileage_results: List[Any], output_filename: str = "mileage_FirstName_LastName.csv") -> pd.DataFrame:
    """
    Validates raw API responses through Pydantic schemas, constructs a structured DataFrame,
    and exports it to a CSV file.
    
    The Pydantic MileageResponse model inherently handles the defensive extraction of nested 
    data and the regex-stripping of non-numeric characters from fuel_tank_capacity.
    """
    rows = []
    for vid, result in zip(target_ids, mileage_results):
        if isinstance(result, Exception):
            logger.error(f"Failed to fetch mileage for {vid}: {result}")
            continue
            
        try:
            # Type validation and string-stripping via Pydantic
            validated = MileageResponse(**result)
            data = validated.data
            
            # String concatenation for Vehicle Name
            make_name = data.make_model_trim.make_model.make.name
            model_name = data.make_model_trim.make_model.name
            vehicle_name = f"{make_name} {model_name}"
            
            rows.append({
                "Vehicle Name": vehicle_name,
                "Combined MPG": data.combined_mpg,
                "MSRP": data.make_model_trim.msrp,
                "Fuel Tank Capacity": data.fuel_tank_capacity
            })
        except Exception as e:
            logger.error(f"Failed to parse mileage data for {vid}: {e}")

    df = pd.DataFrame(rows)
    
    if not df.empty:
        df.to_csv(output_filename, index=False)
        logger.info(f"Data processing complete. Exported {len(df)} rows to {output_filename}")
    else:
        logger.warning("No valid data processed. CSV export skipped.")
        
    return df
