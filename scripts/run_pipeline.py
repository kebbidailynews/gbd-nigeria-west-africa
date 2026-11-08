#!/usr/bin/env python3
"""Run reproducible summaries and figures on a validated harmonised extract."""
import argparse
from pathlib import Path
import json
import pandas as pd
from src.data_validation import load_and_validate
from src.metrics import endpoint_change, add_daly_identity_check
from src.trends import log_linear_trends
from src.uncertainty import summarise_draws
from src.plots import plot_country_trends

p=argparse.ArgumentParser(description="Run GBD analysis pipeline")
p.add_argument("--input",required=True)
p.add_argument("--draws")
p.add_argument("--output",default="results")
a=p.parse_args()
out=Path(a.output)
for folder in ["tables","figures","statistical_outputs"]: (out/folder).mkdir(parents=True,exist_ok=True)
df=load_and_validate(a.input)
endpoint_change(df).to_csv(out/"tables"/"endpoint_changes.csv",index=False)
log_linear_trends(df).to_csv(out/"tables"/"exploratory_trends.csv",index=False)
try:
    add_daly_identity_check(df).to_csv(out/"tables"/"daly_identity_check.csv",index=False)
except ValueError:
    pass
plot_country_trends(df,out/"figures")
if a.draws:
    draws=pd.read_csv(a.draws)
    keys=[c for c in ["measure","location","year","sex","age","cause","metric"] if c in draws.columns]
    if not keys: raise ValueError("Draw file must contain estimate-identifying columns")
    summarise_draws(draws,keys).to_csv(out/"tables"/"draw_summaries.csv",index=False)
metadata={"input":str(a.input),"rows":int(len(df)),"locations":sorted(df.location.unique().tolist()),"years":[int(df.year.min()),int(df.year.max())],"empirical_data_verified_by_pipeline":False}
(out/"statistical_outputs"/"run_metadata.json").write_text(json.dumps(metadata,indent=2))
print(f"Pipeline complete: {len(df):,} validated rows. Review source provenance before interpretation.")
