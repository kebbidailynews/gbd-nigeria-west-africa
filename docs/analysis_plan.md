# Prespecified analysis plan

## Primary objectives

1. Describe 1990–2023 trends in DALYs, YLLs and YLDs in Nigeria using GBD 2023.
2. Report both absolute counts and age-standardised rates per 100,000, keeping these metrics separate.
3. Compare Nigeria with the GBD Western Sub-Saharan Africa benchmark, explicitly noting that Nigeria is included in the regional aggregate.
4. Quantify the basic GBD Level 2 neurological cause group and its non-overlapping child-cause composition.
5. Quantify blindness and vision loss as an impairment outcome, and report ophthalmic causes separately.
6. Describe age and sex differences.
7. Decompose count changes into total population growth, age-structure change and age-specific rate change where compatible inputs exist.

## Primary contrasts

- 1990 versus 2023, using the same release, estimate context, measure, metric, location, sex and age definition.
- Both sexes combined as the headline series; male and female series as stratified analyses.
- Counts and age-standardised rates are co-primary descriptive presentations, not interchangeable outcomes.

## Secondary analyses

- Rank the ten largest causes by DALY count and age-standardised DALY rate in 1990 and 2023.
- Report YLL and YLD contributions separately.
- Expanded nervous-system conditions are a distinct secondary estimand, with a documented cross-hierarchy crosswalk.
- Ophthalmic causes are reported as causes and not summed with blindness/vision-loss impairment outcomes.
- A leave-Nigeria-out regional comparator may be added only after official country membership and denominator/draw compatibility are established.

## Statistical summaries

- Absolute change = 2023 estimate minus 1990 estimate.
- Relative percentage change = (2023 / 1990 - 1) × 100.
- Annualised percentage change = ((2023 / 1990)^(1/33) - 1) × 100, when both endpoint estimates are positive.
- Use GBD 95% uncertainty intervals. If paired draws are available, calculate each contrast draw-by-draw and summarise the resulting distribution. Do not derive change intervals from marginal bounds.
- Log-linear regression is exploratory and descriptive. It is not joinpoint regression and does not establish causality.
- Apply no causal language to decomposition contributions.

## Data and hierarchy checks

Before analysis, verify the GBD round, year coverage, estimate context, location IDs, cause/impairment IDs, parent-child relationships, sex and age coverage, metric, unit, age standard, duplicates, missingness and interval ordering. Preserve the unmodified source files and checksums.

## Sensitivity analyses

1. Compare the basic GBD neurological group with the separately defined expanded nervous-system grouping.
2. Present counts and age-standardised rates side by side to distinguish population growth from rate changes.
3. Compare the regional benchmark with a leave-Nigeria-out aggregate only if it can be reconstructed from compatible country estimates.
4. Re-run key summaries after excluding any cause mapping that cannot be verified at the GBD 2023 hierarchy/sequela level.

## Interpretation guardrails

This is a descriptive secondary analysis of modeled GBD estimates. It cannot independently validate IHME's underlying estimation models. Avoid interpreting non-overlapping uncertainty intervals as a formal hypothesis test. Avoid causal explanations for observed temporal patterns. State the implications of uncertainty, modeled inputs, data availability and changes in GBD methodology.
