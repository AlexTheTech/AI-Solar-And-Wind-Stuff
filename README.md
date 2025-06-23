# Renewable Energy Forecasting Pipeline

This project demonstrates a basic pipeline to download weather data, simulate solar and wind output, engineer features, and train an XGBoost model for forecasting.
The repository now includes a sample list of **200** diverse global locations in `locations.json`. You can regenerate this file using `scripts/generate_locations.py` which samples cities from an open dataset.

## Scripts

- `scripts/collect_data.py` – Download hourly weather data from the [Open-Meteo](https://open-meteo.com/) archive API for the locations listed in `locations.json`. The timeframe and locations file can be overridden via command line arguments.
- `scripts/simulate_output.py` – Add physics-informed estimates of solar and wind output. Multiple panel areas or turbine sizes can be provided as comma separated values to generate several configurations at once.
- `scripts/generate_locations.py` – Build a list of 200 random global cities from an online city database. This file is pre-generated but can be refreshed.
- `scripts/feature_engineer.py` – Create additional time-based and rolling statistics features for model training.
- `scripts/train_model.py` – Train an XGBoost regression model to predict output seven days ahead.

## Quick Example

```bash
# 1. Download weather data (requires internet access)
python scripts/collect_data.py --locations_file locations.json --days 90

# 2. Simulate renewable system output
python scripts/simulate_output.py data/raw/weather_raw_Berlin_DE_52.52_13.405.csv \
    data/processed/berlin_simulated.csv --panel_area 1.0,2.0 --turbine_radius 1.2

# 3. Feature engineering
python scripts/feature_engineer.py data/processed/berlin_simulated.csv data/processed/berlin_features.csv

# 4. Train the forecasting model
python scripts/train_model.py data/processed/berlin_features.csv simulated_solar_output_w --model_out berlin_solar.xgb
```

The example commands above fetch data for Berlin and create a model predicting solar output. Additional locations are defined in `locations.json` and will be processed automatically when running `collect_data.py`.
`simulate_output.py` supports comma separated values so you can generate columns for many solar panel sizes or wind turbine radii in a single run.

Note that access to the Open-Meteo API may be blocked in some environments. If so, the data download step will fail and the remaining pipeline stages cannot run until suitable data is available.
