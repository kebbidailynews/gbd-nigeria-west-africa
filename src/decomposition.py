"""Three-factor Shapley decomposition of population burden change."""
import itertools
import pandas as pd


def shapley_burden_decomposition(start: pd.DataFrame, end: pd.DataFrame) -> dict:
    """Decompose burden change into population size, age mix and age-specific rate.

    Inputs must contain one row per identical age group, with compatible
    population counts and rates. This is accounting attribution, not causality.
    """
    required = {"age", "population", "rate"}
    if not required.issubset(start.columns) or not required.issubset(end.columns):
        raise ValueError("Inputs require age, population and rate")
    if start["age"].duplicated().any() or end["age"].duplicated().any():
        raise ValueError("Age groups must be unique")
    if set(start.age) != set(end.age):
        raise ValueError("Mismatched age groups")
    a = start.set_index("age").sort_index()
    b = end.set_index("age").sort_index()
    for frame in (a, b):
        if frame[["population", "rate"]].isna().any().any():
            raise ValueError("Population and rates must be complete")
        if (frame[["population", "rate"]].to_numpy() < 0).any():
            raise ValueError("Population and rates must be non-negative")
        if frame["population"].sum() <= 0:
            raise ValueError("Total population must be positive")

    # Factor 0: total population; factor 1: age composition; factor 2: age-specific rates.
    def burden(state):
        total = float(a.population.sum() if state[0] == 0 else b.population.sum())
        shares = a.population / a.population.sum() if state[1] == 0 else b.population / b.population.sum()
        rates = a.rate if state[2] == 0 else b.rate
        return float((total * shares * rates).sum())

    names = ["population", "age_structure", "age_specific_rate"]
    contributions = dict.fromkeys(names, 0.0)
    permutations = list(itertools.permutations(range(3)))
    for order in permutations:
        state = [0, 0, 0]
        previous = burden(state)
        for factor in order:
            state[factor] = 1
            current = burden(state)
            contributions[names[factor]] += (current - previous) / len(permutations)
            previous = current

    first, last = burden([0, 0, 0]), burden([1, 1, 1])
    return {"burden_start": first, "burden_end": last,
            "burden_change": last - first, **contributions}
