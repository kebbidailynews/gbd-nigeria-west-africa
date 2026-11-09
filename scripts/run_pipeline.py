#!/usr/bin/env python3
"""Run reproducible summaries and figures on a validated harmonised extract."""
import argparse
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import platform
import pandas as pd

from src.data_validation import load_and_validate
from src.metrics import endpoint_change, add_daly_identity_check
from src.trends import log_linear_trends
from src.uncertainty import summarise_draws
from src.plots import plot_country_trends

p = argparse.ArgumentParser(description="Run GBD analysis pipeline")
p.add_argument("--input", required=True)
p.add_argument("--draws")
p.add_argument("--output", default="results")
p.add_argument("--start-year", type=int, default=1990)
p.add_argument("--end-year", type=int, default=2023)
a = p.parse_args()

if a.end_year <= a.start_year:
    p.error("--end-year must be later than --start-year")

out = Path(a.output)
for folder in ["tables", "figures", "statistical_outputs"]:
    (out / folder).mkdir(parents=True, exist_ok=True)

df = load_and_validate(a.input, min_year=a.start_year, max_year=a.end_year)
endpoint_change(df, start_year=a.start_year, end_year=a.end_year).to_csv(
    out / "tables" / "endpoint_changes.csv", index=False
)
log_linear_trends(df).to_csv(out / "tables" / "exploratory_trends.csv", index=False)

identity_status = "not_run"
try:
    identity = add_daly_identity_check(df)
    identity.to_csv(out / "tables" / "daly_identity_check.csv", index=False)
    identity_status = "pass" if bool(identity["identity_pass"].all()) else "check_failed_rows"
except ValueError as exc:
    # Missing one or more of the three measures can make the check inapplicable.
    # Duplicate or malformed inputs are still surfaced in the metadata.
    identity_status = f"not_completed: {exc}"

plot_country_trends(df, out / "figures")

draw_summary_rows = 0
if a.draws:
    draws = pd.read_csv(a.draws)
    keys = [c for c in ["measure", "location", "year", "sex", "age", "cause", "metric"]
            if c in draws.columns]
    if len(keys) != 7:
        raise ValueError("Draw file must contain all seven estimate-identifying columns")
    summary = summarise_draws(draws, keys)
    summary.to_csv(out / "tables" / "draw_summaries.csv", index=False)
    draw_summary_rows = int(len(summary))

metadata = {
    "run_timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "python_version": platform.python_version(),
    "package_versions": {name: importlib.metadata.version(name) for name in ["pandas", "numpy", "scipy", "matplotlib"]},
    "input": str(a.input),
    "input_sha256": hashlib.sha256(Path(a.input).read_bytes()).hexdigest(),
    "source_manifest_path": "data/metadata/source_manifest.csv",
    "source_manifest_present": Path("data/metadata/source_manifest.csv").exists(),
    "rows": int(len(df)),
    "locations": sorted(df.location.unique().tolist()),
    "year_range_observed": [int(df.year.min()), int(df.year.max())],
    "requested_endpoint_years": [a.start_year, a.end_year],
    "endpoint_series_count": int(len(pd.read_csv(out / "tables" / "endpoint_changes.csv"))),
    "draw_summary_rows": draw_summary_rows,
    "daly_identity_status": identity_status,
    "empirical_data_verified_by_pipeline": False,
    "verification_note": "Structural validation is not source provenance verification; independently review the source manifest, hierarchy IDs, units and access terms."
}
(out / "statistical_outputs" / "run_metadata.json").write_text(json.dumps(metadata, indent=2))
print(f"Pipeline complete: {len(df):,} validated rows. Review source provenance before interpretation.")
