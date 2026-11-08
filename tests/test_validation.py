import pandas as pd
import pytest
from src.data_validation import load_and_validate

def frame():
    return pd.DataFrame([{"measure":"DALYs","location":"Nigeria","year":2020,"sex":"Both","age":"Age-standardised","cause":"Stroke","metric":"Rate","value":100.0,"lower":90.0,"upper":110.0}])

def test_valid_data(tmp_path):
    p=tmp_path/"valid.csv"; frame().to_csv(p,index=False); assert len(load_and_validate(p))==1

def test_rejects_bad_interval(tmp_path):
    d=frame(); d.loc[0,"lower"]=105; p=tmp_path/"bad.csv"; d.to_csv(p,index=False)
    with pytest.raises(ValueError): load_and_validate(p)

def test_rejects_missing_columns(tmp_path):
    p=tmp_path/"missing.csv"; pd.DataFrame({"measure":["DALYs"]}).to_csv(p,index=False)
    with pytest.raises(ValueError): load_and_validate(p)
