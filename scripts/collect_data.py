import json
import os
import argparse
from datetime import datetime, timedelta
import requests
import pandas as pd

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
HOURLY_VARS = [
    "temperature_2m",
    "dew_point_2m",
    "relative_humidity_2m",
    "apparent_temperature",
    "precipitation",
    "rain",
    "snowfall",
    "cloud_cover",
    "shortwave_radiation",
    "surface_pressure",
    "wind_speed_10m",
    "wind_direction_10m",
    "wind_gusts_10m",
]


def load_locations(path="locations.json"):
    """Load location definitions from JSON."""
    with open(path, "r") as f:
        return json.load(f)


def fetch_location(location, start_date, end_date):
    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ",".join(HOURLY_VARS),
        "timezone": "UTC",
    }
    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    hourly = data.get("hourly", {})
    if not hourly:
        return pd.DataFrame()
    df = pd.DataFrame(hourly)
    df.insert(0, "time", pd.to_datetime(df["time"]))
    return df


def save_data(df, location):
    name = location["name"].replace(" ", "_")
    fname = f"weather_raw_{name}_{location['country']}_{location['latitude']}_{location['longitude']}.csv"
    path = os.path.join("data", "raw", fname)
    df.to_csv(path, index=False)
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--locations_file", default="locations.json")
    parser.add_argument("--start_date")
    parser.add_argument("--end_date")
    parser.add_argument("--days", type=int, default=60,
                        help="Number of days back from end_date if start_date not provided")
    args = parser.parse_args()

    locations = load_locations(args.locations_file)

    end = datetime.fromisoformat(args.end_date).date() if args.end_date else datetime.utcnow().date()
    if args.start_date:
        start = datetime.fromisoformat(args.start_date).date()
    else:
        start = end - timedelta(days=args.days)

    for loc in locations:
        try:
            df = fetch_location(loc, start.isoformat(), end.isoformat())
            if not df.empty:
                out = save_data(df, loc)
                print(f"Saved {out} with {len(df)} rows")
            else:
                print(f"No data returned for {loc['name']}")
        except Exception as exc:
            print(f"Failed to fetch {loc['name']}: {exc}")


if __name__ == "__main__":
    main()
