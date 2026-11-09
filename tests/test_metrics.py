import pandas as pd
import pytest
from src.metrics import endpoint_change,add_daly_identity_check


def sample():
    rows=[["DALYs","Nigeria",2000,"Both","All ages","Stroke","Number",100,90,110],
          ["DALYs","Nigeria",2020,"Both","All ages","Stroke","Number",150,140,160]]
    return pd.DataFrame(rows,columns=["measure","location","year","sex","age","cause","metric","value","lower","upper"])


def test_endpoint_change():
    out=endpoint_change(sample())
    assert out.iloc[0].absolute_change==50
    assert out.iloc[0].relative_change_pct==50
    assert out.iloc[0].annualised_change_pct==pytest.approx(((1.5**(1/20))-1)*100)


def test_explicit_endpoints_do_not_silently_substitute_years():
    assert endpoint_change(sample(),start_year=1990,end_year=2020).empty


def test_daly_identity():
    rows=[[m,"Nigeria",2020,"Both","All ages","Stroke","Number",v,v-1,v+1]
          for m,v in [("DALYs",100),("YLLs",70),("YLDs",30)]]
    d=pd.DataFrame(rows,columns=["measure","location","year","sex","age","cause","metric","value","lower","upper"])
    out=add_daly_identity_check(d)
    assert out.iloc[0].difference==0 and bool(out.iloc[0].identity_pass)


def test_daly_identity_rejects_duplicate_measure_rows():
    d=pd.DataFrame([["DALYs","Nigeria",2020,"Both","All ages","Stroke","Number",100],
                    ["DALYs","Nigeria",2020,"Both","All ages","Stroke","Number",100]],
                   columns=["measure","location","year","sex","age","cause","metric","value"])
    with pytest.raises(ValueError,match="Duplicate"): add_daly_identity_check(d)
