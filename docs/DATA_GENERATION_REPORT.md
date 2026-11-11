
# GeoPulse – Data Generation & EDA Report

## 1. Project Overview

GeoPulse is a hyper-local retail mobility analytics
platform designed to analyze simulated mobile GPS
data and identify urban footfall patterns.

## 2. Dataset Information

- Dataset: GPS Mobility Dataset
- City: Mumbai (Simulated)
- Total Records: 100,000
- Unique Devices: 10,000
- GPS Pings per Device: 10
- Time Coverage: 24 Hours
- File Format: CSV

## 3. Dataset Attributes

| Column | Description |
|---|---|
| DeviceID | Anonymized device identifier |
| Latitude | GPS latitude |
| Longitude | GPS longitude |
| Timestamp | GPS ping timestamp |
| LocationZone | Simulated city zone |

## 4. Data Generation

Python was used to generate synthetic GPS mobility
records using NumPy and Pandas.

Five simulated Mumbai zones were created:
BKC, Fort, Andheri, Powai and Dadar.

GPS coordinates were generated around these zones.
Hourly activity probabilities were used to simulate
different traffic patterns throughout the day.

## 5. Exploratory Data Analysis

The generated dataset was analyzed using Pandas
and Matplotlib.

The following analyses were performed:

- Hourly GPS activity distribution
- Zone-wise GPS activity
- Hourly traffic comparison across zones
- Unique devices by location zone

## 6. Visualizations

The following visualizations were generated:

1. Hourly Traffic Distribution
2. Zone-wise GPS Activity
3. Hourly Traffic by Zone

## 7. Data Quality Validation

The dataset was checked for:

- Missing values
- Duplicate records
- Invalid latitude and longitude
- Timestamp validity
- Unique device identifiers

## 8. Technology Stack

- Python
- Pandas
- NumPy
- Matplotlib
- VS Code
- Git and GitHub

## 9. Conclusion

The initial synthetic GPS dataset was generated
and explored successfully.

This dataset establishes the foundation for the
next stage of GeoPulse, which involves geospatial
processing, spatial joins and cloud data storage.

Note: All generated mobility data is synthetic and
does not represent actual individual movement.

## Data Quality Validation Results

The synthetic GPS mobility dataset was validated using `validate_gps_data.py`.

**Dataset summary**
- Total records: 100,000
- Unique devices: 10,000
- Total columns: 5
- Time coverage: 11 November 2026, 00:00:09 to 23:59:49
- Location zones: BKC, Andheri, Dadar, Fort and Powai

**Validation results**
- Missing values: 0
- Duplicate records: 0
- Invalid latitude records: 0
- Invalid longitude records: 0

**Key observations**
- The dataset contains an average of 10 GPS records per device.
- Peak activity occurred at 8 AM with 10,203 GPS records.
- A second peak occurred at 6 PM with 10,110 GPS records.
- The hourly distribution reflects the intended simulated morning and evening commute patterns.

**Conclusion**

The dataset passed the implemented structural and data quality checks. It is suitable for the next stage of exploratory spatial analysis. Realistic device movement and store-visit identification will require additional processing.
