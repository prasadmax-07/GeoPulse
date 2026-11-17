
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "h3_mobility_aggregation.csv"

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "maps"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "h3_hotspot_map.png"


def main():

    print("Loading H3 aggregation data...")

    df = pd.read_csv(INPUT_FILE)

    print("Total H3 cells:", len(df))

    print("\nGenerating offline hotspot visualization...")

    plt.figure(figsize=(12, 8))

    scatter = plt.scatter(
        df["avg_longitude"],
        df["avg_latitude"],
        c=df["total_pings"],
        s=df["total_pings"] * 8,
        cmap="YlOrRd",
        alpha=0.7,
        edgecolors="black",
        linewidths=0.3
    )

    plt.colorbar(scatter, label="Total GPS Pings")

    plt.title("GeoPulse - H3 Mobility Hotspot Analysis")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    plt.grid(alpha=0.3)

    plt.tight_layout()

    plt.savefig(OUTPUT_FILE, dpi=300)

    plt.close()

    print("\n========== HOTSPOT REPORT ==========")
    print("Total H3 cells:", len(df))

    print("\nTop 10 Mobility Hotspots:")
    print(
        df.sort_values(
            by="total_pings",
            ascending=False
        ).head(10).to_string(index=False)
    )

    print("\nHotspot visualization saved:", OUTPUT_FILE)
    print("\nOffline visualization completed successfully!")


if __name__ == "__main__":
    main()
