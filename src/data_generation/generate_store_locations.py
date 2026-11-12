
import pandas as pd
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Output location
OUTPUT_FILE = PROJECT_ROOT / "data" / "synthetic" / "store_locations.csv"

# Simulated retail store locations
# Coordinates are placed around the same centers used in GPS generation.
stores = [
    {
        "StoreID": "STR001",
        "StoreName": "GeoPulse BKC 01",
        "LocationZone": "BKC",
        "Latitude": 19.0655,
        "Longitude": 72.8685,
        "CatchmentRadius_m": 500
    },
    {
        "StoreID": "STR002",
        "StoreName": "GeoPulse BKC 02",
        "LocationZone": "BKC",
        "Latitude": 19.0638,
        "Longitude": 72.8705,
        "CatchmentRadius_m": 500
    },
    {
        "StoreID": "STR003",
        "StoreName": "GeoPulse Fort 01",
        "LocationZone": "Fort",
        "Latitude": 18.9325,
        "Longitude": 72.8345,
        "CatchmentRadius_m": 500
    },
    {
        "StoreID": "STR004",
        "StoreName": "GeoPulse Fort 02",
        "LocationZone": "Fort",
        "Latitude": 18.9308,
        "Longitude": 72.8365,
        "CatchmentRadius_m": 500
    },
    {
        "StoreID": "STR005",
        "StoreName": "GeoPulse Andheri 01",
        "LocationZone": "Andheri",
        "Latitude": 19.1195,
        "Longitude": 72.8455,
        "CatchmentRadius_m": 500
    },
    {
        "StoreID": "STR006",
        "StoreName": "GeoPulse Andheri 02",
        "LocationZone": "Andheri",
        "Latitude": 19.1178,
        "Longitude": 72.8475,
        "CatchmentRadius_m": 500
    },
    {
        "StoreID": "STR007",
        "StoreName": "GeoPulse Powai 01",
        "LocationZone": "Powai",
        "Latitude": 19.1175,
        "Longitude": 72.9055,
        "CatchmentRadius_m": 500
    },
    {
        "StoreID": "STR008",
        "StoreName": "GeoPulse Powai 02",
        "LocationZone": "Powai",
        "Latitude": 19.1158,
        "Longitude": 72.9075,
        "CatchmentRadius_m": 500
    },
    {
        "StoreID": "STR009",
        "StoreName": "GeoPulse Dadar 01",
        "LocationZone": "Dadar",
        "Latitude": 19.0185,
        "Longitude": 72.8425,
        "CatchmentRadius_m": 500
    },
    {
        "StoreID": "STR010",
        "StoreName": "GeoPulse Dadar 02",
        "LocationZone": "Dadar",
        "Latitude": 19.0168,
        "Longitude": 72.8445,
        "CatchmentRadius_m": 500
    }
]

# Convert to DataFrame
df = pd.DataFrame(stores)

# Validate store dataset
assert df["StoreID"].is_unique, "Duplicate Store IDs found!"
assert df[["StoreID", "StoreName", "LocationZone",
           "Latitude", "Longitude"]].notnull().all().all(), \
    "Missing values found!"

assert df["Latitude"].between(-90, 90).all(), \
    "Invalid latitude values found!"

assert df["Longitude"].between(-180, 180).all(), \
    "Invalid longitude values found!"

assert (df["CatchmentRadius_m"] > 0).all(), \
    "Invalid catchment radius found!"

expected_zones = {"BKC", "Fort", "Andheri", "Powai", "Dadar"}
assert set(df["LocationZone"]) == expected_zones, \
    "Unexpected or missing location zones!"

# Create output directory if required
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Save dataset
df.to_csv(OUTPUT_FILE, index=False)

# Display results
print("\n========== GEOPULSE STORE LOCATION REPORT ==========")
print(f"\nTotal Stores: {len(df)}")
print(f"Unique Store IDs: {df['StoreID'].nunique()}")
print(f"Location Zones: {df['LocationZone'].nunique()}")

print("\nStore Distribution:")
print(df["LocationZone"].value_counts())

print("\nGenerated Store Dataset:")
print(df.to_string(index=False))

print(f"\nDataset saved successfully: {OUTPUT_FILE}")
print("\n========== STORE DATASET VALIDATION PASSED ==========")
