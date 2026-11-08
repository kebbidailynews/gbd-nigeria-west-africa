import pandas as pd
import pytest
from src.uncertainty import summarise_draws,paired_component_sum

def test_draw_summary_uses_empirical_quantiles():
    d=pd.DataFrame({"cause":["stroke"]*4,"draw_id":[0,1,2,3],"value":[1,2,3,4]})
    out=summarise_draws(d,["cause"]); assert out.loc[0,"value"]==2.5 and out.loc[0,"n_draws"]==4

def test_paired_sum_preserves_draw_alignment():
    a=pd.DataFrame({"cause":["stroke"]*2,"draw_id":[0,1],"value":[2,3]}); b=pd.DataFrame({"cause":["stroke"]*2,"draw_id":[0,1],"value":[4,5]})
    assert paired_component_sum(a,b,["cause"])["combined"].tolist()==[6,8]

def test_paired_sum_rejects_unmatched_draws():
    a=pd.DataFrame({"cause":["stroke"],"draw_id":[0],"value":[2]}); b=pd.DataFrame({"cause":["stroke"],"draw_id":[1],"value":[4]})
    with pytest.raises(ValueError,match="do not align"): paired_component_sum(a,b,["cause"])
