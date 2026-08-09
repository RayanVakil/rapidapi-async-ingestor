import logging
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

logger = logging.getLogger(__name__)

def generate_fuel_capacity_chart(df: pd.DataFrame, output_filename: str = "fuel_capacity_chart_FirstName_LastName.jpeg") -> None:
    """
    Generates a professional, enterprise-grade horizontal bar chart from the mileage DataFrame.
    Automatically highlights the vehicle with the largest fuel tank capacity.
    """
    if df.empty:
        logger.error("Dataframe is empty, cannot generate visualization.")
        return

    # Sort in ascending order of Fuel Tank Capacity for a clean horizontal cascade
    df_sorted = df.sort_values(by="Fuel Tank Capacity", ascending=True).reset_index(drop=True)
    
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid", font_scale=1.1)

    # Sharp Teal for the highlight, Muted Navy for the rest
    highlight_color = "#F05A28" 
    muted_color = "#34495E"     

    # Programmatically identify the bar with the largest fuel tank capacity
    max_idx = df_sorted["Fuel Tank Capacity"].idxmax()
    colors_palette = [highlight_color if i == max_idx else muted_color for i in range(len(df_sorted))]

    # Generate the horizontal bar plot (x and y swapped compared to vertical)
    ax = sns.barplot(
        x="Fuel Tank Capacity", 
        y="Vehicle Name", 
        data=df_sorted, 
        hue="Vehicle Name",
        palette=colors_palette,
        legend=False
    )

    # Professional axis labeling and titling
    ax.set_title("Fuel Tank Capacity by Vehicle", fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel("Fuel Tank Capacity (Gallons)", fontsize=12, labelpad=10)
    ax.set_ylabel("Vehicle Name", fontsize=12, labelpad=10)

    # Remove top and right spines as requested
    sns.despine(top=True, right=True)
    
    plt.tight_layout()

    # Export as high-DPI JPEG
    plt.savefig(output_filename, format="jpeg", dpi=300)
    logger.info(f"Visualization complete. Chart exported to {output_filename}")
