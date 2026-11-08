"""Three-factor Shapley decomposition of population burden change."""
import itertools
import pandas as pd

def shapley_burden_decomposition(start: pd.DataFrame,end: pd.DataFrame) -> dict:
    required={"age","population","rate"}
    if not required.issubset(start.columns) or not required.issubset(end.columns): raise ValueError("Inputs require age, population and rate")
    if set(start.age)!=set(end.age): raise ValueError("Mismatched age groups")
    a=start.set_index("age").sort_index(); b=end.set_index("age").sort_index()
    if (a[["population","rate"]].to_numpy()<0).any() or (b[["population","rate"]].to_numpy()<0).any(): raise ValueError("Population and rates must be non-negative")
    factors=["population","age_structure","age_specific_rate"]
    def burden(state):
        total=float(a.population.sum() if state[0]==0 else b.population.sum())
        shares=a.population/a.population.sum() if state[1]==0 else b.population/b.population.sum()
        rates=a.rate if state[2]==0 else b.rate
        return float((total*shares*rates).sum())
    contributions=dict.fromkeys(factors,0.0)
    for i,name in enumerate(factors):
        for perm in itertools.permutations([j for j in range(3) if j!=i]):
            state=[0,0,0]; previous=burden(state)
            for idx in list(perm)+[i]:
                state[idx]=1; current=burden(state)
                if idx==i: contributions[name]+=(current-previous)/2
                previous=current
    first=burden([0,0,0]); last=burden([1,1,1])
    return {"burden_start":first,"burden_end":last,"burden_change":last-first,**contributions}
