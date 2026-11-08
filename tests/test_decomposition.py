import pandas as pd
import pytest
from src.decomposition import shapley_burden_decomposition

def test_shapley_components_sum_to_change():
    a=pd.DataFrame({"age":["0-4","5+"],"population":[100,100],"rate":[10,20]})
    b=pd.DataFrame({"age":["0-4","5+"],"population":[120,180],"rate":[8,18]})
    out=shapley_burden_decomposition(a,b)
    assert out["burden_change"]==pytest.approx(sum(out[k] for k in ["population","age_structure","age_specific_rate"]))
    assert out["burden_end"]>out["burden_start"]
