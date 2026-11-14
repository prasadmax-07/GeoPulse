
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from itertools import combinations

PROJECT_ROOT = Path(__file__).resolve().parents[2]

STORE_FILE = PROJECT_ROOT / "data/synthetic/store_locations.csv"
OUTPUT_DIR = PROJECT_ROOT / "data/processed"
REPORT_DIR = PROJECT_ROOT / "reports/overlap"

EARTH_RADIUS_M = 6371000


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in metres."""

    lat1, lon1, lat2, lon2 = np.radians(
        [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1) * np.cos(lat2)
        * np.sin(dlon / 2) ** 2
    )

    return 2 * EARTH_RADIUS_M * np.arcsin(np.sqrt(a))


def calculate_overlap_area(radius, distance):
    """Calculate intersection area of two equal-radius circles."""

    if distance >= 2 * radius:
        return 0.0

    if distance <= 0:
        return np.pi * radius ** 2

    overlap = (
        2 * radius ** 2 * np.arccos(distance / (2 * radius))
        - (distance / 2)
        * np.sqrt(4 * radius ** 2 - distance ** 2)
    )

    return overlap


def main():

    stores = pd.read_csv(STORE_FILE)

    results = []

    # Compare stores only within the same geographical zone
    for zone, zone_stores in stores.groupby("LocationZone"):

        zone_stores = zone_stores.to_dict("records")

        for store_a, store_b in combinations(zone_stores, 2):

            radius_a = float(store_a["CatchmentRadius_m"])
            radius_b = float(store_b["CatchmentRadius_m"])

            # This implementation assumes equal catchment radii
            if not np.isclose(radius_a, radius_b):
                raise ValueError(
                    "Stores must have equal catchment radii."
                )

            distance = haversine_distance(
                store_a["Latitude"],
                store_a["Longitude"],
                store_b["Latitude"],
                store_b["Longitude"]
            )

            overlap_area = calculate_overlap_area(
                radius_a, distance
            )

            single_area = np.pi * radius_a ** 2

            overlap_percentage = (
                overlap_area / single_area
            ) * 100

            results.append({
                "LocationZone": zone,
                "StoreID_1": store_a["StoreID"],
                "StoreName_1": store_a["StoreName"],
                "StoreID_2": store_b["StoreID"],
                "StoreName_2": store_b["StoreName"],
                "Distance_m": round(distance, 2),
                "Overlap_Area_sq_m": round(overlap_area, 2),
                "Overlap_Percentage": round(
                    overlap_percentage, 2
                )
            })

    # Convert results into a DataFrame
    overlap_df = pd.DataFrame(results)

    if overlap_df.empty:
        raise ValueError("No same-zone store pairs found.")

    # Rank store pairs by overlap
    overlap_df = overlap_df.sort_values(
        "Overlap_Percentage",
        ascending=False
    ).reset_index(drop=True)

    overlap_df["Overlap_Rank"] = (
        overlap_df.index + 1
    )

    # Create output directories
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Save CSV
    output_file = OUTPUT_DIR / "store_catchment_overlap.csv"
    overlap_df.to_csv(output_file, index=False)

    # Create visualization
    plt.figure(figsize=(11, 6))

    pair_labels = (
        overlap_df["StoreID_1"]
        + " vs "
        + overlap_df["StoreID_2"]
    )

    plt.bar(
        pair_labels,
        overlap_df["Overlap_Percentage"]
    )

    plt.title("Store Catchment Area Overlap by Store Pair")
    plt.xlabel("Store Pair")
    plt.ylabel("Overlap (% of one store's catchment area)")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    chart_file = REPORT_DIR / "catchment_overlap.png"

    plt.savefig(chart_file, dpi=300)
    plt.close()

    # Display results
    print("\n========== GEOPULSE CATCHMENT OVERLAP ==========")

    print(f"\nTotal stores analyzed: {len(stores)}")
    print(f"Store pairs compared: {len(overlap_df)}")

    print("\nCatchment Overlap Results:")
    print(overlap_df.to_string(index=False))

    print("\nHighest Overlap Pair:")
    print(overlap_df.iloc[0].to_string())

    print("\nGenerated Files:")
    print(output_file)
    print(chart_file)

    print("\n========== OVERLAP ANALYSIS COMPLETED ==========")


if __name__ == "__main__":
    main()
