# Uncertainty and demographic decomposition

## Draw-based uncertainty

Use the source's posterior draws where available and permitted. Each draw identifier must retain its original pairing across measures and components. Summarise empirical central intervals from the draw distribution. Do not independently re-number or randomly pair draws from separate files. `src/uncertainty.py` rejects duplicate keys and mismatched draw IDs when summing two components.

## Shapley decomposition

`src/decomposition.py` decomposes the change in total burden into three contributions: total population growth, age-structure change and age-specific rate change. The contributions average marginal effects over all factor orderings and sum to the total change. Inputs must use identical age groups and compatible rate units at both endpoints.

This decomposition is a descriptive accounting identity, not causal attribution. Check the scale convention for rates and whether an additional multiplier is required when converting rates to counts.
