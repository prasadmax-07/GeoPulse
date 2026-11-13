
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

HOURLY_FILE = PROJECT_ROOT / "data/processed/hourly_store_footfall.csv"
SUMMARY_FILE = PROJECT_ROOT / "data/processed/store_catchment_summary.csv"

OUTPUT_DIR = PROJECT_ROOT / "reports/footfall"


def main():

    hourly = pd.read_csv(HOURLY_FILE)
    store_summary = pd.read_csv(SUMMARY_FILE)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("\n========== GEOPULSE HOURLY FOOTFALL ANALYSIS ==========")

    # Hourly activity matrix
    hourly_matrix = hourly.pivot_table(
        index="Hour",
        columns="StoreName",
        values="GPS_Pings",
        aggfunc="sum",
        fill_value=0
    ).reindex(range(24), fill_value=0)

    # Peak activity hour for every store
    peak_activity = (
        hourly.loc[
            hourly.groupby("StoreID")["GPS_Pings"].idxmax()
        ][["StoreID", "StoreName", "Hour", "GPS_Pings"]]
        .rename(columns={
            "Hour": "Peak_Hour",
            "GPS_Pings": "Peak_Hour_Pings"
        })
    )

    # Store activity ranking
    store_ranking = store_summary[
        ["StoreID", "StoreName", "LocationZone", "Total_GPS_Pings"]
    ].copy()

    store_ranking = store_ranking.sort_values(
        "Total_GPS_Pings", ascending=False
    )

    store_ranking["Activity_Rank"] = range(
        1, len(store_ranking) + 1
    )

    final_report = store_ranking.merge(
        peak_activity,
        on=["StoreID", "StoreName"],
        how="left"
    )

    # Save CSV reports
    hourly_matrix.to_csv(
        OUTPUT_DIR / "hourly_traffic_matrix.csv"
    )

    final_report.to_csv(
        OUTPUT_DIR / "store_peak_activity_report.csv",
        index=False
    )

    # Chart 1: Hourly traffic comparison
    plt.figure(figsize=(14, 7))

    for store in hourly_matrix.columns:
        plt.plot(
            hourly_matrix.index,
            hourly_matrix[store],
            marker="o",
            linewidth=1.5,
            label=store
        )

    plt.title("Hourly GPS Activity Across Retail Stores")
    plt.xlabel("Hour of Day")
    plt.ylabel("GPS Pings Within 500m")
    plt.xticks(range(24))
    plt.grid(True, alpha=0.3)
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "hourly_store_traffic.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()

    # Chart 2: Store activity ranking
    plt.figure(figsize=(12, 6))

    plt.bar(
        store_ranking["StoreName"],
        store_ranking["Total_GPS_Pings"]
    )

    plt.title("Total GPS Activity by Retail Store")
    plt.xlabel("Retail Store")
    plt.ylabel("Total GPS Pings Within 500m")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "store_traffic_ranking.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()

    print("\nStore Activity Ranking:")
    print(store_ranking.to_string(index=False))

    print("\nPeak Activity Hours:")
    print(peak_activity.to_string(index=False))

    print("\nGenerated Files:")
    print("1. hourly_traffic_matrix.csv")
    print("2. store_peak_activity_report.csv")
    print("3. hourly_store_traffic.png")
    print("4. store_traffic_ranking.png")

    print("\n========== FOOTFALL ANALYSIS COMPLETED ==========")


if __name__ == "__main__":
    main()
