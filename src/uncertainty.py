"""Draw-wise uncertainty propagation for GBD-derived quantities."""
import numpy as np
import pandas as pd

def summarise_draws(draws: pd.DataFrame, group_cols: list[str], value_col: str="value", draw_col: str="draw_id", level: float=0.95) -> pd.DataFrame:
    if not 0<level<1: raise ValueError("level must be between 0 and 1")
    required=set(group_cols+[value_col,draw_col]); missing=required-set(draws.columns)
    if missing: raise ValueError(f"Missing draw columns: {sorted(missing)}")
    if draws.duplicated(group_cols+[draw_col]).any(): raise ValueError("Duplicate estimate/draw keys detected")
    values=pd.to_numeric(draws[value_col],errors="coerce")
    if not np.isfinite(values).all(): raise ValueError("Draw values must be finite numeric values")
    alpha=(1-level)/2; rows=[]
    for key,g in draws.groupby(group_cols,dropna=False,sort=False):
        vals=g[value_col].astype(float).to_numpy(); row=dict(zip(group_cols,key if isinstance(key,tuple) else (key,)))
        row.update(value=float(np.mean(vals)),lower=float(np.quantile(vals,alpha)),upper=float(np.quantile(vals,1-alpha)),n_draws=int(len(vals))); rows.append(row)
    return pd.DataFrame(rows)

def paired_component_sum(left: pd.DataFrame,right: pd.DataFrame,keys: list[str],draw_col: str="draw_id",value_col: str="value",output_col: str="combined") -> pd.DataFrame:
    join=keys+[draw_col]
    for frame in (left,right):
        if frame.duplicated(join).any(): raise ValueError("Duplicate estimate/draw keys detected")
    merged=left[join+[value_col]].merge(right[join+[value_col]],on=join,how="outer",suffixes=("_left","_right"),validate="one_to_one",indicator=True)
    if not (merged["_merge"]=="both").all(): raise ValueError("Draw IDs do not align; refusing unpaired uncertainty propagation")
    merged[output_col]=merged[f"{value_col}_left"]+merged[f"{value_col}_right"]
    return merged[join+[output_col]]
