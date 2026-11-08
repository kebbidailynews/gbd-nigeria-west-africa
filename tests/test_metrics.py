import pandas as pd
from src.metrics import endpoint_change,add_daly_identity_check

def test_endpoint_change():
    rows=[["DALYs","Nigeria",2000,"Both","All ages","Stroke","Number",100,90,110],["DALYs","Nigeria",2020,"Both","All ages","Stroke","Number",150,140,160]]
    d=pd.DataFrame(rows,columns=["measure","location","year","sex","age","cause","metric","value","lower","upper"])
    out=endpoint_change(d); assert out.iloc[0].absolute_change==50 and out.iloc[0].relative_change_pct==50

def test_daly_identity():
    rows=[[m,"Nigeria",2020,"Both","All ages","Stroke","Number",v,v-1,v+1] for m,v in [("DALYs",100),("YLLs",70),("YLDs",30)]]
    d=pd.DataFrame(rows,columns=["measure","location","year","sex","age","cause","metric","value","lower","upper"])
    assert add_daly_identity_check(d).iloc[0].difference==0
