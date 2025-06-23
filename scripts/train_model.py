import argparse
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

HORIZON = 24 * 7  # hours ahead


def prepare_data(df: pd.DataFrame, target_col: str):
    df = df.copy()
    df["target"] = df[target_col].shift(-HORIZON)
    df.dropna(inplace=True)
    X = df.drop(columns=[target_col, "time", "target"])
    y = df["target"]
    return X, y


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv")
    parser.add_argument("target_col", default="simulated_solar_output_w")
    parser.add_argument("--model_out", default="model.xgb")
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv, parse_dates=["time"])
    X, y = prepare_data(df, args.target_col)
 x1x4sk-codex/develop-automated-pipeline-for-renewable-forecasting
    if len(X) < 10:
        raise ValueError(
            f"Not enough samples ({len(X)}) for training. "
            f"Collect more data or use a shorter forecast horizon."
        )
 main
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    params = {
        "objective": "reg:squarederror",
        "tree_method": "hist",
        "max_depth": 6,
        "eta": 0.1,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
    }
    model = xgb.train(params, dtrain, num_boost_round=200)
    preds = model.predict(dtest)
    mae = mean_absolute_error(y_test, preds)
    print(f"MAE: {mae:.3f}")
    model.save_model(args.model_out)
    print(f"Model saved to {args.model_out}")


if __name__ == "__main__":
    main()
