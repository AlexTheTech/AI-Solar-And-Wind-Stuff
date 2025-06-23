# Renewable Energy Forecasting Pipeline

This project demonstrates a basic pipeline to download weather data, simulate solar and wind output, engineer features, and train an XGBoost model for forecasting.

## Scripts

- `scripts/collect_data.py` – Download hourly weather data from the [Open-Meteo](https://open-meteo.com/) archive API for the locations listed in `locations.json`.
- `scripts/simulate_output.py` – Add simple physics-informed estimates of solar and wind output for each weather record.
- `scripts/feature_engineer.py` – Create additional time-based and rolling statistics features for model training.
- `scripts/train_model.py` – Train an XGBoost regression model to predict output seven days ahead.

## Quick Example

```bash
# 1. Download weather data (requires internet access)
python scripts/collect_data.py

# 2. Simulate renewable system output
python scripts/simulate_output.py data/raw/weather_raw_Berlin_DE_52.52_13.405.csv data/processed/berlin_simulated.csv --panel_area 2.0 --turbine_radius 1.2

# 3. Feature engineering
python scripts/feature_engineer.py data/processed/berlin_simulated.csv data/processed/berlin_features.csv

# 4. Train the forecasting model
python scripts/train_model.py data/processed/berlin_features.csv simulated_solar_output_w --model_out berlin_solar.xgb
```

The example commands above fetch data for Berlin and create a model predicting solar output. Additional locations are defined in `locations.json` and will be processed automatically when running `collect_data.py`.

Note that access to the Open-Meteo API may be blocked in some environments. If so, the data download step will fail and the remaining pipeline stages cannot run until suitable data is available.
