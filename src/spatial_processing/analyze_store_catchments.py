
import pandas as pd
import numpy as np
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

GPS_FILE = PROJECT_ROOT / "data/synthetic/gps_mobility_data.csv"
STORE_FILE = PROJECT_ROOT / "data/synthetic/store_locations.csv"

OUTPUT_DIR = PROJECT_ROOT / "data/processed"

# Earth's approximate radius in metres
EARTH_RADIUS_M = 6371000


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two geographical coordinates.
    Returns distance in metres.
    """

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    )

    c = 2 * np.arcsin(np.sqrt(a))

    return EARTH_RADIUS_M * c


def main():

    # Load datasets
    gps = pd.read_csv(GPS_FILE)
    stores = pd.read_csv(STORE_FILE)

    gps["Timestamp"] = pd.to_datetime(gps["Timestamp"])

    print("\n========== GEOPULSE CATCHMENT ANALYSIS ==========")
    print(f"GPS records loaded: {len(gps)}")
    print(f"Stores loaded: {len(stores)}")

    # Match GPS records with stores in the same zone.
    # This avoids comparing unrelated geographical zones.
    merged = gps.merge(
        stores,
        on="LocationZone",
        suffixes=("_GPS", "_Store")
    )

    print(f"GPS-store comparisons: {len(merged)}")

    # Calculate geographical distance
    merged["Distance_m"] = haversine_distance(
    merged["Latitude_GPS"].values,
    merged["Longitude_GPS"].values,
    merged["Latitude_Store"].values,
    merged["Longitude_Store"].values
)

    # Identify pings inside each store's catchment radius
    catchment_pings = merged[
        merged["Distance_m"] <= merged["CatchmentRadius_m"]
    ].copy()

    # Round distance for readable output
    catchment_pings["Distance_m"] = (
        catchment_pings["Distance_m"].round(2)
    )

    # Store-wise summary
    store_summary = (
        catchment_pings.groupby(
            ["StoreID", "StoreName", "LocationZone"]
        )
        .agg(
            Total_GPS_Pings=("DeviceID", "count"),
            Unique_Devices=("DeviceID", "nunique"),
            Average_Distance_m=("Distance_m", "mean")
        )
        .reset_index()
    )

    # Include stores with zero matching pings
    store_summary = stores[
        ["StoreID", "StoreName", "LocationZone"]
    ].merge(
        store_summary,
        on=["StoreID", "StoreName", "LocationZone"],
        how="left"
    )

    store_summary[
        ["Total_GPS_Pings", "Unique_Devices"]
    ] = store_summary[
        ["Total_GPS_Pings", "Unique_Devices"]
    ].fillna(0).astype(int)

    store_summary["Average_Distance_m"] = (
        store_summary["Average_Distance_m"].round(2)
    )

    # Hourly store activity
    catchment_pings["Hour"] = (
        catchment_pings["Timestamp"].dt.hour
    )

    hourly_summary = (
        catchment_pings.groupby(
            ["StoreID", "StoreName", "Hour"]
        )
        .agg(
            GPS_Pings=("DeviceID", "count"),
            Unique_Devices=("DeviceID", "nunique")
        )
        .reset_index()
    )

    # Save outputs
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    catchment_pings.to_csv(
        OUTPUT_DIR / "store_catchment_pings.csv",
        index=False
    )

    store_summary.to_csv(
        OUTPUT_DIR / "store_catchment_summary.csv",
        index=False
    )

    hourly_summary.to_csv(
        OUTPUT_DIR / "hourly_store_footfall.csv",
        index=False
    )

    # Display results
    print("\nStore-wise Catchment Summary:")
    print(store_summary.to_string(index=False))

    print("\nTotal GPS pings inside catchments:",
          len(catchment_pings))

    print("Unique devices across all catchments:",
          catchment_pings["DeviceID"].nunique())

    print("\nOutput files generated:")
    print("1. store_catchment_pings.csv")
    print("2. store_catchment_summary.csv")
    print("3. hourly_store_footfall.csv")

    print("\n========== ANALYSIS COMPLETED ==========")


if __name__ == "__main__":
    main()
