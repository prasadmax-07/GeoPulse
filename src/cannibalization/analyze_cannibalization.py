
import pandas as pd
from pathlib import Path
from itertools import combinations

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CATCHMENT_FILE = (
    PROJECT_ROOT / "data/processed/store_catchment_pings.csv"
)

OVERLAP_FILE = (
    PROJECT_ROOT / "data/processed/store_catchment_overlap.csv"
)

SUMMARY_FILE = (
    PROJECT_ROOT / "data/processed/store_catchment_summary.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "data/processed"
REPORT_DIR = PROJECT_ROOT / "reports/cannibalization"


def main():

    # Load datasets
    catchment = pd.read_csv(CATCHMENT_FILE)
    overlap = pd.read_csv(OVERLAP_FILE)
    summary = pd.read_csv(SUMMARY_FILE)

    print("\n========== GEOPULSE CANNIBALIZATION ANALYSIS ==========")

    # Build a unique-device set for every store
    device_groups = (
        catchment.groupby("StoreID")["DeviceID"]
        .apply(set)
        .to_dict()
    )

    store_info = (
        summary.set_index("StoreID")
        [["StoreName", "LocationZone"]]
        .to_dict("index")
    )

    results = []

    # Analyze only the store pairs already compared geometrically
    for _, pair in overlap.iterrows():

        store_a = pair["StoreID_1"]
        store_b = pair["StoreID_2"]

        devices_a = device_groups.get(store_a, set())
        devices_b = device_groups.get(store_b, set())

        shared_devices = devices_a.intersection(devices_b)
        all_devices = devices_a.union(devices_b)

        count_a = len(devices_a)
        count_b = len(devices_b)
        shared_count = len(shared_devices)

        # Percentage of each store's device population shared
        shared_pct_a = (
            shared_count / count_a * 100
            if count_a else 0
        )

        shared_pct_b = (
            shared_count / count_b * 100
            if count_b else 0
        )

        # Jaccard similarity
        jaccard = (
            shared_count / len(all_devices) * 100
            if all_devices else 0
        )

        # Percentage of the smaller device group that is shared
        smaller_store_pct = (
            shared_count / min(count_a, count_b) * 100
            if min(count_a, count_b) else 0
        )

        results.append({
            "LocationZone": pair["LocationZone"],
            "StoreID_1": store_a,
            "StoreName_1": store_info[store_a]["StoreName"],
            "StoreID_2": store_b,
            "StoreName_2": store_info[store_b]["StoreName"],
            "Geographical_Overlap_Pct": pair["Overlap_Percentage"],
            "Devices_Store_1": count_a,
            "Devices_Store_2": count_b,
            "Shared_Devices": shared_count,
            "Shared_Pct_Store_1": round(shared_pct_a, 2),
            "Shared_Pct_Store_2": round(shared_pct_b, 2),
            "Smaller_Store_Shared_Pct": round(
                smaller_store_pct, 2
            ),
            "Jaccard_Similarity_Pct": round(jaccard, 2)
        })

    # Create results DataFrame
    report = pd.DataFrame(results)

    # Rank pairs by device similarity
    report = report.sort_values(
        "Jaccard_Similarity_Pct",
        ascending=False
    ).reset_index(drop=True)

    report["Competition_Indicator_Rank"] = (
        report.index + 1
    )

    # Save report
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = (
        OUTPUT_DIR / "store_cannibalization_analysis.csv"
    )

    report.to_csv(output_file, index=False)

    # Save a concise top-pairs report
    top_pairs = report.head(5)

    top_pairs.to_csv(
        REPORT_DIR / "top_store_competition_pairs.csv",
        index=False
    )

    # Display results
    print(f"\nStore pairs analyzed: {len(report)}")

    print("\nCannibalization Screening Results:")
    print(report.to_string(index=False))

    print("\nTop Potential Competition Pair:")

    print(
        report.iloc[0][
            [
                "StoreName_1",
                "StoreName_2",
                "Geographical_Overlap_Pct",
                "Shared_Devices",
                "Jaccard_Similarity_Pct"
            ]
        ].to_string()
    )

    print("\nGenerated Files:")
    print(output_file)
    print(REPORT_DIR / "top_store_competition_pairs.csv")

    print("\n========== ANALYSIS COMPLETED ==========")


if __name__ == "__main__":
    main()
    