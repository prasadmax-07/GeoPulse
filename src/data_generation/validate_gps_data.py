
import pandas as pd
from pathlib import Path

# Load generated GPS dataset
project_root = Path(__file__).resolve().parents[2]

file_path = (
    project_root
    / "data"
    / "synthetic"
    / "gps_mobility_data.csv"
)

df = pd.read_csv(file_path)

print("\n========== GEOPULSE DATA QUALITY REPORT ==========")

# 1. Dataset dimensions
print("\n1. Dataset Shape:")
print(df.shape)

# 2. Missing values
print("\n2. Missing Values:")
print(df.isnull().sum())

# 3. Duplicate records
print("\n3. Duplicate Records:")
print(df.duplicated().sum())

# 4. Unique devices
print("\n4. Unique Devices:")
print(df["DeviceID"].nunique())

# 5. Latitude validation
print("\n5. Invalid Latitude Records:")
print(((df["Latitude"] < -90) | (df["Latitude"] > 90)).sum())

# 6. Longitude validation
print("\n6. Invalid Longitude Records:")
print(((df["Longitude"] < -180) | (df["Longitude"] > 180)).sum())

# 7. Timestamp validation
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

print("\n7. Timestamp Range:")
print("Start:", df["Timestamp"].min())
print("End:", df["Timestamp"].max())

# 8. Location distribution
print("\n8. Location Zone Distribution:")
print(df["LocationZone"].value_counts())

# 9. Hourly traffic distribution
print("\n9. Hourly Traffic Distribution:")
print(df["Timestamp"].dt.hour.value_counts().sort_index())

print("\n========== VALIDATION COMPLETED ==========")
