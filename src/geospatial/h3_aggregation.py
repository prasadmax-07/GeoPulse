
import pandas as pd
import h3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "synthetic" / "gps_mobility_data.csv"

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "h3_mobility_aggregation.csv"


def main():

    print("Loading GPS dataset...")

    df = pd.read_csv(INPUT_FILE)

    print("Total GPS records:", len(df))

    print("\nGenerating H3 indexes...")

    df["h3_index"] = df.apply(
        lambda row: h3.latlng_to_cell(
            row["Latitude"],
            row["Longitude"],
            9
        ),
        axis=1
    )

    print("H3 indexing completed!")

    print("\nAggregating mobility data...")

    aggregation = df.groupby("h3_index").agg(
        total_pings=("h3_index", "count"),
        unique_devices=("DeviceID", "nunique"),
        avg_latitude=("Latitude", "mean"),
        avg_longitude=("Longitude", "mean")
    ).reset_index()

    aggregation = aggregation.sort_values(
        by="total_pings",
        ascending=False
    )

    aggregation.to_csv(OUTPUT_FILE, index=False)

    print("\n========== H3 ANALYSIS REPORT ==========")
    print("Total GPS records:", len(df))
    print("Unique H3 cells:", df["h3_index"].nunique())

    print("\nTop 10 high-mobility cells:")
    print(aggregation.head(10).to_string(index=False))

    print("\nOutput saved:", OUTPUT_FILE)

    print("\nH3 spatial aggregation completed!")


if __name__ == "__main__":
    main()
