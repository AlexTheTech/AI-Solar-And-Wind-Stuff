import argparse
import pandas as pd


def engineer_features(df: pd.DataFrame, lags=1, rolling=3):
    df["hour"] = df["time"].dt.hour
    df["day_of_year"] = df["time"].dt.dayofyear
    if "shortwave_radiation" in df.columns:
        df["radiation_roll_mean"] = df["shortwave_radiation"].rolling(rolling, min_periods=1).mean()
    if "simulated_solar_output_w" in df.columns:
        df["solar_output_lag1"] = df["simulated_solar_output_w"].shift(lags)
    if "simulated_wind_output_w" in df.columns:
        df["wind_output_lag1"] = df["simulated_wind_output_w"].shift(lags)
    df.dropna(inplace=True)
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv")
    parser.add_argument("output_csv")
    args = parser.parse_args()
    df = pd.read_csv(args.input_csv, parse_dates=["time"])
    df = engineer_features(df)
    df.to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main()
