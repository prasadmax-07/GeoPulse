
import pendulum
import subprocess
import sys

from pathlib import Path
from airflow.sdk import dag, task

PROJECT_ROOT = Path("/mnt/c/Users/prasa/GeoPulse")
PYTHON = sys.executable


def run_script(script_path):
    subprocess.run(
        [PYTHON, str(PROJECT_ROOT / script_path)],
        cwd=str(PROJECT_ROOT),
        check=True,
    )


@dag(
    dag_id="geopulse_daily_pipeline",
    schedule="0 2 * * *",
    start_date=pendulum.datetime(2026, 11, 19, tz="Asia/Kolkata"),
    catchup=False,
    tags=["geopulse", "mobility", "automation"],
)
def geopulse_daily_pipeline():

    @task
    def store_catchment_analysis():
        run_script("src/spatial_processing/analyze_store_catchments.py")

    @task
    def hourly_footfall_analysis():
        run_script("src/spatial_processing/analyze_hourly_footfall.py")

    @task
    def catchment_overlap_analysis():
        run_script("src/spatial_processing/analyze_catchment_overlap.py")

    @task
    def h3_mobility_aggregation():
        run_script("src/geospatial/h3_aggregation.py")

    @task
    def h3_hotspot_visualization():
        run_script("src/geospatial/h3_hotspot_map.py")

    catchment = store_catchment_analysis()

    hourly = hourly_footfall_analysis()
    overlap = catchment_overlap_analysis()

    h3 = h3_mobility_aggregation()
    hotspot = h3_hotspot_visualization()

    catchment >> [hourly, overlap]
    h3 >> hotspot


geopulse_daily_pipeline()

