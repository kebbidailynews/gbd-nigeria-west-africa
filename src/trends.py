import numpy as np
import pandas as pd
from scipy.stats import linregress

def log_linear_trends(df: pd.DataFrame, group_cols=None) -> pd.DataFrame:
    """Exploratory OLS trend in log(value); not joinpoint or causal inference."""
    group_cols=group_cols or ["measure","location","sex","age","cause","metric"]
    output=[]
    for key,g in df.sort_values("year").groupby(group_cols,dropna=False):
        g=g[(g["value"]>0)].drop_duplicates("year")
        if g["year"].nunique()<5: continue
        fit=linregress(g["year"].to_numpy(),np.log(g["value"].to_numpy()))
        rec=dict(zip(group_cols,key if isinstance(key,tuple) else (key,)))
        rec.update(n_years=int(g["year"].nunique()),slope=float(fit.slope),annual_change_pct=float((np.exp(fit.slope)-1)*100),r_squared=float(fit.rvalue**2),p_value=float(fit.pvalue))
        output.append(rec)
    return pd.DataFrame(output)
