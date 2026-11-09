import pandas as pd
import pytest
from src.data_validation import load_and_validate


def frame():
    return pd.DataFrame([{"measure":"DALYs","location":"Nigeria","year":2020,
        "sex":"Both","age":"Age-standardised","cause":"Stroke","metric":"Rate",
        "value":100.0,"lower":90.0,"upper":110.0}])


def test_valid_data(tmp_path):
    p=tmp_path/"valid.csv"; frame().to_csv(p,index=False)
    assert len(load_and_validate(p))==1


def test_rejects_bad_interval(tmp_path):
    d=frame(); d.loc[0,"lower"]=105; p=tmp_path/"bad.csv"; d.to_csv(p,index=False)
    with pytest.raises(ValueError): load_and_validate(p)


def test_rejects_missing_columns(tmp_path):
    p=tmp_path/"missing.csv"; pd.DataFrame({"measure":["DALYs"]}).to_csv(p,index=False)
    with pytest.raises(ValueError): load_and_validate(p)


def test_rejects_duplicate_estimate_key(tmp_path):
    d=pd.concat([frame(),frame()],ignore_index=True); p=tmp_path/"duplicate.csv"; d.to_csv(p,index=False)
    with pytest.raises(ValueError,match="Duplicate estimate keys"): load_and_validate(p)


def test_rejects_year_outside_study_window(tmp_path):
    d=frame(); d.loc[0,"year"]=1980; p=tmp_path/"year.csv"; d.to_csv(p,index=False)
    with pytest.raises(ValueError,match="minimum"): load_and_validate(p,min_year=1990,max_year=2023)
