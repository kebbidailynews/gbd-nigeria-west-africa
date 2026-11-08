from pathlib import Path
import pandas as pd

REQUIRED = ["measure", "location", "year", "sex", "age", "cause", "metric", "value", "lower", "upper"]

def load_and_validate(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = sorted(set(REQUIRED) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    for col in ["year", "value", "lower", "upper"]:
        df[col] = pd.to_numeric(df[col], errors="raise")
    if df[REQUIRED].isna().any().any():
        raise ValueError("Required fields contain missing values")
    if (df[["value", "lower", "upper"]] < 0).any().any():
        raise ValueError("Negative estimates detected")
    if ((df["lower"] > df["value"]) | (df["value"] > df["upper"])).any():
        raise ValueError("Invalid uncertainty interval ordering")
    if (df["year"] % 1 != 0).any():
        raise ValueError("Year must be integer-valued")
    return df
