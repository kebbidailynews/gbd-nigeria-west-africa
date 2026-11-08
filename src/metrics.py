import pandas as pd

def endpoint_change(df: pd.DataFrame) -> pd.DataFrame:
    keys = ["measure", "location", "sex", "age", "cause", "metric"]
    rows = []
    for key, group in df.sort_values("year").groupby(keys, dropna=False):
        first, last = group.iloc[0], group.iloc[-1]
        rows.append(dict(zip(keys, key), start_year=int(first.year), end_year=int(last.year),
                         start_value=float(first.value), end_value=float(last.value),
                         absolute_change=float(last.value-first.value),
                         relative_change_pct=float((last.value/first.value-1)*100) if first.value else float("nan")))
    return pd.DataFrame(rows)

def add_daly_identity_check(df: pd.DataFrame) -> pd.DataFrame:
    keys=["location","year","sex","age","cause","metric"]
    wide=df.pivot_table(index=keys,columns="measure",values="value",aggfunc="first").reset_index()
    if not {"DALYs","YLLs","YLDs"}.issubset(wide.columns):
        raise ValueError("DALY identity requires DALYs, YLLs and YLDs")
    wide["difference"]=wide["DALYs"]-wide["YLLs"]-wide["YLDs"]
    return wide
