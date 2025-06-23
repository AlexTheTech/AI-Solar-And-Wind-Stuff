import argparse
import math
import pandas as pd

SOLAR_EFFICIENCY = 0.2  # typical panel efficiency
WIND_EFFICIENCY = 0.4   # typical turbine efficiency
AIR_DENSITY = 1.225     # kg/m^3


def simulate(df: pd.DataFrame, panel_areas=None, turbine_radii=None):
    panel_areas = panel_areas or [1.0]
    turbine_radii = turbine_radii or [1.0]
    if "shortwave_radiation" in df.columns:
        for area in panel_areas:
            col = f"simulated_solar_output_w_{area}" if len(panel_areas) > 1 else "simulated_solar_output_w"
            df[col] = df["shortwave_radiation"] * area * SOLAR_EFFICIENCY
    if "wind_speed_10m" in df.columns:
        for radius in turbine_radii:
            swept_area = math.pi * radius ** 2
            col = f"simulated_wind_output_w_{radius}" if len(turbine_radii) > 1 else "simulated_wind_output_w"
            df[col] = 0.5 * AIR_DENSITY * swept_area * (df["wind_speed_10m"] ** 3) * WIND_EFFICIENCY
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv")
    parser.add_argument("output_csv")
    parser.add_argument("--panel_area", default="1.0",
                        help="Comma separated panel areas in square meters")
    parser.add_argument("--turbine_radius", default="1.0",
                        help="Comma separated turbine radii in meters")
    args = parser.parse_args()
    df = pd.read_csv(args.input_csv, parse_dates=["time"])
    panel_areas = [float(x) for x in args.panel_area.split(',')]
    turbine_radii = [float(x) for x in args.turbine_radius.split(',')]
    df = simulate(df, panel_areas, turbine_radii)
    df.to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main()
