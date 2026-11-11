
import numpy as np
import pandas as pd
from pathlib import Path

# -----------------------------------------
# 1. PROJECT CONFIGURATION
# -----------------------------------------

NUM_DEVICES = 10_000
PINGS_PER_DEVICE = 10
TOTAL_RECORDS = NUM_DEVICES * PINGS_PER_DEVICE

BASE_DATE = pd.Timestamp("2026-11-11")

rng = np.random.default_rng(42)

# -----------------------------------------
# 2. SIMULATED MUMBAI CITY ZONES
# -----------------------------------------

ZONES = {
    "BKC": (19.0650, 72.8690),
    "Fort": (18.9320, 72.8350),
    "Andheri": (19.1190, 72.8460),
    "Powai": (19.1170, 72.9060),
    "Dadar": (19.0180, 72.8430)
}

zone_names = np.array(list(ZONES.keys()))

# -----------------------------------------
# 3. GENERATE DEVICE IDS
# -----------------------------------------

device_ids = np.repeat(
    [f"DEV{i:05d}" for i in range(1, NUM_DEVICES + 1)],
    PINGS_PER_DEVICE
)

rng.shuffle(device_ids)

# -----------------------------------------
# 4. GENERATE TIME DISTRIBUTION
# -----------------------------------------

# Higher probability during commute hours

hour_weights = np.array([
    1, 1, 1, 1, 1, 2,
    4, 8, 12, 10, 6, 5,
    5, 5, 5, 5, 6, 9,
    12, 8, 5, 3, 2, 1
], dtype=float)

hour_weights /= hour_weights.sum()

hours = rng.choice(
    np.arange(24),
    size=TOTAL_RECORDS,
    p=hour_weights
)

minutes = rng.integers(0, 60, size=TOTAL_RECORDS)
seconds = rng.integers(0, 60, size=TOTAL_RECORDS)

timestamps = (
    BASE_DATE
    + pd.to_timedelta(hours, unit="h")
    + pd.to_timedelta(minutes, unit="m")
    + pd.to_timedelta(seconds, unit="s")
)

# -----------------------------------------
# 5. SIMULATE MOVEMENT ACROSS CITY ZONES
# -----------------------------------------

zone_probabilities = {
    "morning": [0.35, 0.20, 0.20, 0.10, 0.15],
    "afternoon": [0.25, 0.20, 0.20, 0.20, 0.15],
    "evening": [0.15, 0.15, 0.25, 0.15, 0.30],
    "night": [0.15, 0.10, 0.25, 0.25, 0.25]
}

location_zones = np.empty(TOTAL_RECORDS, dtype=object)

for hour in range(24):

    if 7 <= hour <= 10:
        period = "morning"
    elif 11 <= hour <= 16:
        period = "afternoon"
    elif 17 <= hour <= 20:
        period = "evening"
    else:
        period = "night"

    mask = hours == hour

    location_zones[mask] = rng.choice(
        zone_names,
        size=mask.sum(),
        p=zone_probabilities[period]
    )

# -----------------------------------------
# 6. GENERATE GPS COORDINATES
# -----------------------------------------

latitude = np.zeros(TOTAL_RECORDS)
longitude = np.zeros(TOTAL_RECORDS)

for zone, (center_lat, center_lon) in ZONES.items():

    mask = location_zones == zone
    count = mask.sum()

    latitude[mask] = rng.normal(
        center_lat, 0.0025, count
    )

    longitude[mask] = rng.normal(
        center_lon, 0.0030, count
    )

# -----------------------------------------
# 7. CREATE DATAFRAME
# -----------------------------------------

gps_data = pd.DataFrame({
    "DeviceID": device_ids,
    "Latitude": latitude,
    "Longitude": longitude,
    "Timestamp": timestamps,
    "LocationZone": location_zones
})

gps_data = gps_data.sort_values(
    "Timestamp"
).reset_index(drop=True)

# -----------------------------------------
# 8. EXPORT DATASET
# -----------------------------------------

project_root = Path(__file__).resolve().parents[2]

output_directory = project_root / "data" / "synthetic"
output_directory.mkdir(parents=True, exist_ok=True)

output_file = output_directory / "gps_mobility_data.csv"

gps_data.to_csv(output_file, index=False)

# -----------------------------------------
# 9. DISPLAY GENERATION SUMMARY
# -----------------------------------------

print("\n========== GEOPULSE GPS DATA GENERATOR ==========")

print(f"Total GPS Records: {len(gps_data)}")
print(f"Unique Devices: {gps_data['DeviceID'].nunique()}")

print("\nLocation-wise Record Distribution:")
print(gps_data["LocationZone"].value_counts())

print("\nMissing Values:")
print(gps_data.isnull().sum())

print("\nDataset Preview:")
print(gps_data.head())

print(f"\nDataset saved successfully at: {output_file}")

print("\n=================================================")
