import os
import pytest
import pandas as pd
from src.processing import process_mileage_data
from src.visual import generate_fuel_capacity_chart

@pytest.fixture
def mock_mileage_results():
    return [
        {
            "data": {
                "combined_mpg": 25.5,
                "fuel_tank_capacity": "15.8 gal",
                "make_model_trim": {
                    "msrp": 35000,
                    "make_model": {
                        "name": "Model S",
                        "make": {
                            "name": "Tesla"
                        }
                    }
                }
            }
        },
        {
            "data": {
                "combined_mpg": None,
                "fuel_tank_capacity": "18.5",
                "make_model_trim": {
                    "msrp": 28000,
                    "make_model": {
                        "name": "Outback",
                        "make": {
                            "name": "Subaru"
                        }
                    }
                }
            }
        }
    ]

def test_process_mileage_data(mock_mileage_results, tmp_path):
    target_ids = [1001, 1002]
    output_csv = tmp_path / "test_mileage.csv"
    
    df = process_mileage_data(
        target_ids=target_ids, 
        mileage_results=mock_mileage_results, 
        output_filename=str(output_csv)
    )
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ["Vehicle Name", "Combined MPG", "MSRP", "Fuel Tank Capacity"]
    
    # Check data extraction and regex parsing
    assert df.iloc[0]["Vehicle Name"] == "Tesla Model S"
    assert df.iloc[0]["Fuel Tank Capacity"] == 15.8
    assert df.iloc[0]["Combined MPG"] == 25.5
    
    assert df.iloc[1]["Vehicle Name"] == "Subaru Outback"
    assert df.iloc[1]["Fuel Tank Capacity"] == 18.5
    assert pd.isna(df.iloc[1]["Combined MPG"]) or df.iloc[1]["Combined MPG"] is None
    
    # Assert CSV was written
    assert os.path.exists(str(output_csv))

def test_generate_fuel_capacity_chart(mock_mileage_results, tmp_path):
    target_ids = [1001, 1002]
    
    df = process_mileage_data(
        target_ids=target_ids, 
        mileage_results=mock_mileage_results, 
        output_filename=os.devnull
    )
    
    output_jpeg = tmp_path / "test_chart.jpeg"
    
    # Assert the visual module runs without throwing errors and generates the JPEG
    generate_fuel_capacity_chart(
        df=df,
        output_filename=str(output_jpeg)
    )
    
    assert os.path.exists(str(output_jpeg))
