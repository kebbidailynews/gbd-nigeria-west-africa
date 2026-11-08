#!/usr/bin/env python3
import argparse
from src.data_validation import load_and_validate
p=argparse.ArgumentParser(description="Validate harmonised GBD estimates")
p.add_argument("--input",required=True); args=p.parse_args()
df=load_and_validate(args.input)
print(f"Validated {len(df):,} rows across {df['location'].nunique()} locations and {df['year'].nunique()} years.")
