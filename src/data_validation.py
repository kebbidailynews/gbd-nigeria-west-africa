"""Strict validation for harmonised, aggregate GBD estimates."""
from pathlib import Path
import numpy as np
import pandas as pd

REQUIRED = ["measure", "location", "year", "sex", "age", "cause", "metric",
            "value", "lower", "upper"]
ESTIMATE_KEYS = ["measure", "location", "year", "sex", "age", "cause", "metric"]


def load_and_validate(path: str | Path, *, min_year: int | None = None,
                      max_year: int | None = None) -> pd.DataFrame:
    """Load a harmonised CSV and reject ambiguous or invalid estimate rows.

    Extra columns (e.g. location_id, cause_id, draw metadata) are retained.
    Posterior draws should normally be stored separately in long form.
    """
    df = pd.read_csv(path)
    missing = sorted(set(REQUIRED) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    for col in ["measure", "location", "sex", "age", "cause", "metric"]:
        df[col] = df[col].astype("string").str.strip()
        if df[col].isna().any() or df[col].eq("").any():
            raise ValueError(f"Blank categorical values in {col}")

    for col in ["year", "value", "lower", "upper"]:
        df[col] = pd.to_numeric(df[col], errors="raise")
        if not np.isfinite(df[col].to_numpy(dtype=float)).all():
            raise ValueError(f"Non-finite numeric values in {col}")

    if (df["year"] % 1 != 0).any():
        raise ValueError("Year must be integer-valued")
    df["year"] = df["year"].astype("int64")
    if min_year is not None and (df["year"] < min_year).any():
        raise ValueError(f"Year earlier than configured minimum {min_year}")
    if max_year is not None and (df["year"] > max_year).any():
        raise ValueError(f"Year later than configured maximum {max_year}")

    if (df[["value", "lower", "upper"]] < 0).any().any():
        raise ValueError("Negative estimates detected")
    if ((df["lower"] > df["value"]) | (df["value"] > df["upper"])).any():
        raise ValueError("Invalid uncertainty interval ordering")

    duplicates = df.duplicated(ESTIMATE_KEYS, keep=False)
    if duplicates.any():
        examples = df.loc[duplicates, ESTIMATE_KEYS].head(3).to_dict("records")
        raise ValueError(f"Duplicate estimate keys detected; examples: {examples}")

    return df
