import os
import re
import sys
import math
import asyncio
import logging
import httpx
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

from src.client import AsyncCarAPIClient, MaxRetriesExceededError
from src.models.schemas import MileageResponse
from src.processing import process_mileage_data
from src.visual import generate_fuel_capacity_chart

# Configure structured, professional logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# User: Swap this out for your actual full name as per assessment instructions
YOUR_FULL_NAME = "FirstName_LastName"

async def main():
    load_dotenv()
    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key or api_key == "your_api_key_here":
        logger.error("CRITICAL: RAPIDAPI_KEY is not configured in the environment.")
        sys.exit(1)

    async with AsyncCarAPIClient(api_key=api_key) as client:
        # ---------------------------------------------------------
        # Question 1: Exterior Colors
        # ---------------------------------------------------------
        logger.info("Executing Question 1: Fetching exterior colors for Tesla Model S 2018")
        try:
            q1_data = await client.get_exterior_colors(make="Tesla", model="Model S", year=2018)
            colors_list = q1_data.get("data", [])
            unique_colors = set()
            for color in colors_list:
                color_name = color.get("name") if isinstance(color, dict) else color
                if color_name:
                    unique_colors.add(color_name)
            print(f"\n---> Question 1 (Unique Colors Count): {len(unique_colors)}\n")
        except MaxRetriesExceededError as e:
            logger.error(f"Question 1 Failed: {e}")
        except httpx.HTTPStatusError as e:
            logger.error(f"Question 1 Blocked by API: {e.response.status_code} {e.response.text}")

        # ---------------------------------------------------------
        # Question 2: Subaru Outback Introduction Year
        # ---------------------------------------------------------
        logger.info("Executing Question 2: Fetching available years for Subaru Outback")
        try:
            q2_data = await client.get_years(make="Subaru", model="Outback")
            years_list = q2_data.get("data", [])
            parsed_years = []
            for y in years_list:
                if isinstance(y, dict) and "year" in y:
                    parsed_years.append(int(y["year"]))
                elif isinstance(y, (int, str)):
                    parsed_years.append(int(y))
            if parsed_years:
                print(f"---> Question 2 (Subaru Outback Intro Year): {min(parsed_years)}\n")
            else:
                logger.warning("Question 2: No years found.")
        except MaxRetriesExceededError as e:
            logger.error(f"Question 2 Failed: {e}")
        except httpx.HTTPStatusError as e:
            logger.error(f"Question 2 Blocked by API: {e.response.status_code} {e.response.text}")

        # ---------------------------------------------------------
        # Question 3: Average Curb Weight
        # ---------------------------------------------------------
        logger.info("Executing Question 3: Fetching bodies for Toyota Yaris 2019")
        try:
            q3_data = await client.get_bodies(make="Toyota", model="Yaris", year=2019)
            bodies = q3_data.get("data", [])
            curb_weights = []
            for body in bodies:
                if "curb_weight" in body and body["curb_weight"]:
                    cw = body["curb_weight"]
                    if isinstance(cw, (int, float)):
                        curb_weights.append(float(cw))
                    elif isinstance(cw, str):
                        match = re.search(r"[\d\.]+", cw)
                        if match:
                            curb_weights.append(float(match.group()))
            if curb_weights:
                avg_weight = sum(curb_weights) / len(curb_weights)
                print(f"---> Question 3 (Avg Curb Weight rounded up): {math.ceil(avg_weight)}\n")
            else:
                logger.warning("Question 3: No curb_weight data found.")
        except MaxRetriesExceededError as e:
            logger.error(f"Question 3 Failed: {e}")
        except httpx.HTTPStatusError as e:
            logger.error(f"Question 3 Blocked by API: {e.response.status_code} {e.response.text}")

        # ---------------------------------------------------------
        # Question 4: Mileage Data Frame (Concurrent Fetch & Process)
        # ---------------------------------------------------------
        target_ids = [7559, 7081, 8542, 6968, 6363]
        logger.info(f"Executing Question 4: Fetching mileage data concurrently for IDs {target_ids}")
        
        # Concurrently fetch all mileage data for max I/O throughput
        mileage_tasks = [client.get_mileage(vid) for vid in target_ids]
        mileage_results = await asyncio.gather(*mileage_tasks, return_exceptions=True)

        # Delegate validation, structuring, and export to processing module
        df = process_mileage_data(
            target_ids=target_ids, 
            mileage_results=mileage_results, 
            output_filename=f"mileage_{YOUR_FULL_NAME}.csv"
        )

        # ---------------------------------------------------------
        # Question 5: Professional Bar Chart
        # ---------------------------------------------------------
        logger.info("Executing Question 5: Generating professional horizontal bar chart")
        
        # Delegate visualization generation and export to visual module
        generate_fuel_capacity_chart(
            df=df, 
            output_filename=f"fuel_capacity_chart_{YOUR_FULL_NAME}.jpeg"
        )
        
        logger.info("All assessment questions executed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
