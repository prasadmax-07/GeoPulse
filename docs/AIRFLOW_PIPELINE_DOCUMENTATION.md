# GeoPulse – Airflow Pipeline Documentation

## 1. Overview

GeoPulse uses Apache Airflow to automate its hyper-local retail mobility analytics workflow. The pipeline processes synthetic GPS mobility data, performs spatial analysis, generates H3 aggregations and creates hotspot visualizations.

## 2. Airflow Environment

- Orchestration Tool: Apache Airflow 3.4.0
- Environment: WSL2 with Ubuntu
- Python Version: 3.14
- Execution Mode: Standalone
- Metadata Database: SQLite
- Virtual Environment: `airflow-venv`
- DAG Location: `airflow/dags/`

## 3. Pipeline Architecture

The workflow consists of five processing tasks:

1. **Store Catchment Analysis:** Identifies GPS pings within 500-metre store catchments.
2. **Hourly Footfall Analysis:** Calculates hourly store activity and generates reports.
3. **Catchment Overlap Analysis:** Evaluates geographical overlap between store catchments.
4. **H3 Mobility Aggregation:** Aggregates GPS mobility records into H3 hexagonal cells.
5. **H3 Hotspot Visualization:** Generates a hotspot map from H3 aggregation results.

## 4. Task Dependencies

- Store Catchment Analysis runs first.
- Hourly Footfall Analysis and Catchment Overlap Analysis run after catchment analysis.
- H3 Hotspot Visualization runs after H3 Mobility Aggregation.
- The two processing branches can execute independently.

## 5. Scheduling

The DAG is configured to execute daily at 2:00 AM Indian Standard Time (IST).

Cron Expression: `0 2 * * *`

Catchup is disabled to prevent automatic backfilling of missed scheduled runs.

## 6. Monitoring and Execution

The Airflow web interface is available at:

`http://localhost:8080`

Users can monitor DAG runs, task statuses, execution logs and failures through the dashboard.

The initial five-task workflow was tested successfully, with all five tasks completing successfully.

## 7. Starting and Stopping Airflow

Start Airflow in Ubuntu:

```bash
source ~/airflow-venv/bin/activate
export AIRFLOW_HOME=~/airflow
export AIRFLOW__CORE__DAGS_FOLDER="/mnt/c/Users/prasa/GeoPulse/airflow/dags"
airflow standalone
```

Stop Airflow using `Ctrl + C` in the running terminal.

**Note:** The WSL environment and Airflow services must remain running for scheduled executions to occur. This standalone SQLite configuration is intended for development and demonstration, not production deployment.

## 8. Conclusion

Apache Airflow provides centralized orchestration for GeoPulse's mobility analytics workflow. It reduces manual execution and enables scheduled processing, task dependency management and execution monitoring.