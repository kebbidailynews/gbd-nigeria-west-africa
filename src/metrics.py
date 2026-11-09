"""Descriptive change metrics and internal DALY identity checks."""
import numpy as np
import pandas as pd

KEYS = ["measure", "location", "sex", "age", "cause", "metric"]


def endpoint_change(df: pd.DataFrame, start_year: int | None = None,
                    end_year: int | None = None) -> pd.DataFrame:
    """Calculate endpoint differences and compound annualised change.

    If years are omitted, each series' observed first and last years are used.
    Supply explicit years for a consistent cross-series comparison.
    """
    required = set(KEYS + ["year", "value"])
    if not required.issubset(df.columns):
        raise ValueError(f"Missing columns: {sorted(required - set(df.columns))}")
    if df.duplicated(KEYS + ["year"]).any():
        raise ValueError("Duplicate series-year estimates detected")

    rows = []
    for key, group in df.sort_values("year").groupby(KEYS, dropna=False):
        if start_year is None:
            first = group.iloc[0]
        else:
            selected = group[group.year == start_year]
            if selected.empty:
                continue
            first = selected.iloc[0]
        if end_year is None:
            last = group.iloc[-1]
        else:
            selected = group[group.year == end_year]
            if selected.empty:
                continue
            last = selected.iloc[0]
        if int(last.year) <= int(first.year):
            raise ValueError("End year must be later than start year")
        absolute = float(last.value - first.value)
        relative = float((last.value / first.value - 1) * 100) if first.value else np.nan
        annualised = (float(((last.value / first.value) ** (1 / (last.year-first.year)) - 1) * 100)
                      if first.value > 0 and last.value >= 0 else np.nan)
        rows.append(dict(zip(KEYS, key), start_year=int(first.year), end_year=int(last.year),
                         start_value=float(first.value), end_value=float(last.value),
                         absolute_change=absolute, relative_change_pct=relative,
                         annualised_change_pct=annualised))
    return pd.DataFrame(rows)


def add_daly_identity_check(df: pd.DataFrame, *, atol: float = 1e-6) -> pd.DataFrame:
    """Check DALYs = YLLs + YLDs on matching estimate dimensions.

    This is an arithmetic consistency check, not an independent validation
    of the source model. It requires exactly one row per measure and key.
    """
    keys = ["location", "year", "sex", "age", "cause", "metric"]
    needed = set(keys + ["measure", "value"])
    if not needed.issubset(df.columns):
        raise ValueError(f"Missing columns: {sorted(needed - set(df.columns))}")
    if df.duplicated(keys + ["measure"]).any():
        raise ValueError("Duplicate rows prevent DALY identity check")
    wide = df.pivot(index=keys, columns="measure", values="value").reset_index()
    if not {"DALYs", "YLLs", "YLDs"}.issubset(wide.columns):
        raise ValueError("DALY identity requires DALYs, YLLs and YLDs")
    wide["difference"] = wide["DALYs"] - wide["YLLs"] - wide["YLDs"]
    wide["identity_pass"] = np.isclose(wide["difference"], 0, atol=atol, rtol=0)
    return wide
