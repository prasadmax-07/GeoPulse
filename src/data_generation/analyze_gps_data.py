
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------------
# 1. LOAD DATASET
# -----------------------------------

project_root = Path(__file__).resolve().parents[2]

file_path = (
    project_root
    / "data"
    / "synthetic"
    / "gps_mobility_data.csv"
)

df = pd.read_csv(file_path, parse_dates=["Timestamp"])

# -----------------------------------
# 2. BASIC DATA ANALYSIS
# -----------------------------------

print("\n========== GEOPULSE EDA REPORT ==========")

print("\nDataset Shape:")
print(df.shape)

print("\nDataset Information:")
print(df.info())

print("\nStatistical Summary:")
print(df.describe(include="all"))

print("\nUnique Devices:")
print(df["DeviceID"].nunique())

# Extract hour
df["Hour"] = df["Timestamp"].dt.hour

# -----------------------------------
# 3. HOURLY TRAFFIC ANALYSIS
# -----------------------------------

hourly_traffic = df.groupby("Hour").size()

print("\nHourly GPS Activity:")
print(hourly_traffic)

plt.figure(figsize=(12, 5))

hourly_traffic.plot(kind="bar")

plt.title("GeoPulse - Hourly GPS Activity")
plt.xlabel("Hour of Day")
plt.ylabel("Number of GPS Pings")
plt.xticks(rotation=0)

plt.tight_layout()

# -----------------------------------
# 4. LOCATION ZONE ANALYSIS
# -----------------------------------

zone_traffic = df["LocationZone"].value_counts()

print("\nZone-wise GPS Activity:")
print(zone_traffic)

plt.figure(figsize=(9, 5))

zone_traffic.plot(kind="bar")

plt.title("GPS Activity Across Mumbai Zones")
plt.xlabel("Location Zone")
plt.ylabel("Number of GPS Pings")
plt.xticks(rotation=0)

plt.tight_layout()

# -----------------------------------
# 5. HOURLY TRAFFIC BY ZONE
# -----------------------------------

zone_hourly = pd.crosstab(
    df["Hour"],
    df["LocationZone"]
)

print("\nHourly Traffic by Zone:")
print(zone_hourly)

plt.figure(figsize=(12, 6))

zone_hourly.plot(kind="line", marker="o")

plt.title("Hourly Mobility Patterns Across Zones")
plt.xlabel("Hour of Day")
plt.ylabel("Number of GPS Pings")
plt.xticks(range(24))
plt.legend(title="Location Zone")

plt.tight_layout()

# -----------------------------------
# 6. UNIQUE DEVICES BY ZONE
# -----------------------------------

unique_devices = (
    df.groupby("LocationZone")["DeviceID"]
    .nunique()
)

print("\nUnique Devices by Zone:")
print(unique_devices)

# -----------------------------------
# 7. SAVE VISUALIZATIONS
# -----------------------------------

output_dir = project_root / "reports" / "eda"
output_dir.mkdir(parents=True, exist_ok=True)

plt.figure(1)
plt.savefig(
    output_dir / "hourly_traffic.png",
    dpi=150,
    bbox_inches="tight"
)

plt.figure(2)
plt.savefig(
    output_dir / "zone_traffic.png",
    dpi=150,
    bbox_inches="tight"
)

plt.figure(3)
plt.savefig(
    output_dir / "zone_hourly_traffic.png",
    dpi=150,
    bbox_inches="tight"
)

print("\nEDA visualizations saved successfully!")

plt.show()

print("\n========== EDA COMPLETED ==========")
