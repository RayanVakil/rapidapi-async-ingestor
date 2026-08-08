import os
import re
import sys
import math
import asyncio
import logging
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

from src.client import AsyncCarAPIClient, MaxRetriesExceededError
from src.models.schemas import MileageResponse

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

        # ---------------------------------------------------------
        # Question 4: Mileage Data Frame
        # ---------------------------------------------------------
        target_ids = [7559, 7081, 8542, 6968, 6363]
        logger.info(f"Executing Question 4: Fetching mileage data concurrently for IDs {target_ids}")
        
        # Concurrently fetch all mileage data for max performance
        mileage_tasks = [client.get_mileage(vid) for vid in target_ids]
        mileage_results = await asyncio.gather(*mileage_tasks, return_exceptions=True)

        rows = []
        for vid, result in zip(target_ids, mileage_results):
            if isinstance(result, Exception):
                logger.error(f"Failed to fetch mileage for {vid}: {result}")
                continue
            
            try:
                # Type validation via Pydantic
                validated = MileageResponse(**result)
                data = validated.data
                vehicle_name = f"{data.make_model_trim.make_model.make.name} {data.make_model_trim.make_model.name}"
                
                rows.append({
                    "Vehicle Name": vehicle_name,
                    "Combined MPG": data.combined_mpg,
                    "MSRP": data.make_model_trim.msrp,
                    "Fuel Tank Capacity": data.fuel_tank_capacity
                })
            except Exception as e:
                logger.error(f"Failed to parse mileage data for {vid}: {e}")

        df = pd.DataFrame(rows)
        csv_filename = f"mileage_{YOUR_FULL_NAME}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"---> Question 4 (Data Frame exported to CSV): {csv_filename}\n")

        # ---------------------------------------------------------
        # Question 5: Professional Bar Chart
        # ---------------------------------------------------------
        logger.info("Executing Question 5: Generating professional bar chart")
        if df.empty:
            logger.error("Dataframe is empty, cannot generate chart.")
            return

        # Sort the bars in ascending order of Fuel Tank Capacity
        df_sorted = df.sort_values(by="Fuel Tank Capacity", ascending=True).reset_index(drop=True)
        
        # Enterprise-ready styling setup
        plt.figure(figsize=(10, 6))
        sns.set_theme(style="whitegrid", font_scale=1.1)

        # Coterie brand color (Red-Orange) for the highlight, Navy for muted
        highlight_color = "#E03C31" 
        muted_color = "#2C3E50"     

        # Programmatically identify the bar with the largest fuel tank capacity
        max_idx = df_sorted["Fuel Tank Capacity"].idxmax()
        colors_palette = [highlight_color if i == max_idx else muted_color for i in range(len(df_sorted))]

        # Generate the bar plot
        ax = sns.barplot(
            x="Vehicle Name", 
            y="Fuel Tank Capacity", 
            data=df_sorted, 
            hue="Vehicle Name",
            palette=colors_palette,
            legend=False
        )

        ax.set_title("Fuel Tank Capacity by Vehicle", fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel("Vehicle Name", fontsize=12, labelpad=10)
        ax.set_ylabel("Fuel Tank Capacity (Gallons)", fontsize=12, labelpad=10)

        # Remove top and right spines as requested
        sns.despine(top=True, right=True)
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()

        chart_filename = f"fuel_capacity_chart_{YOUR_FULL_NAME}.jpeg"
        plt.savefig(chart_filename, format="jpeg", dpi=300)
        print(f"---> Question 5 (Chart exported to JPEG): {chart_filename}\n")
        logger.info("All assessment questions executed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
