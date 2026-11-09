# Data acquisition protocol: GBD 2023

## Access and extraction

1. Sign in or register for the official IHME GBD Results Tool: https://vizhub.healthdata.org/gbd-results/. An account is required for downloads.
2. Explicitly select GBD 2023 and years 1990–2023. Do not mix estimates from GBD 2021 or other releases.
3. Run relatively narrow queries. IHME tool guidance warns that very large queries may omit selected years, ages or other requested results. Export separate query batches and reconcile row counts.
4. For the cause context, export DALYs, YLLs and YLDs for Nigeria and Western Sub-Saharan Africa. Include both sexes, male and female, and the age groups needed for prespecified analyses. Export counts and rates as separate metrics where needed.
5. For the basic neurological cause group, export the Level 2 parent for a benchmark. Then export selected Level 3/4 child causes for detailed ranking and trends. Never add a parent estimate to its children.
6. For an expanded nervous-system analysis, export the separately prespecified cross-hierarchy causes. Keep this estimand distinct from the basic GBD neurological Level 2 group.
7. For vision, run a separate impairment query for blindness and vision loss. Run separate cause queries for cataract, refractive disorders, glaucoma, diabetic retinopathy and age-related macular degeneration. Do not add the impairment total to cause-specific estimates.
8. Obtain population estimates by age, sex, location and year from a compatible GBD 2023 source for any custom regional aggregation or demographic decomposition.
9. Retain IDs and names for locations, causes/impairments, measures, metrics, ages and sexes. Prefer exports that include both IDs and names.
10. Record the query share link, download timestamp, file names, SHA-256 checksums, source release, filters, age standard, units, uncertainty fields and terms of use in data/metadata/source_manifest.csv.

## Geography

The GBD Western Sub-Saharan Africa regional estimate includes Nigeria. It is a useful regional benchmark but is not independent of the Nigeria estimate. If the research question requires a comparator excluding Nigeria, verify the region's 2023 country membership from the official location hierarchy and build a leave-Nigeria-out aggregate using country-level counts and compatible denominators or paired draws. Do not average country rates or combine overlapping regional and country totals.

## Query batching and reconciliation

- Batch by estimate context (cause versus impairment), measure, and manageable location/cause selections.
- Keep age, sex, year and metric filters identical across comparison batches.
- After download, verify that all expected years, locations, sexes and age groups are present.
- Compare downloaded row counts with the Cartesian product implied by selected dimensions, allowing only documented source-specific exclusions.
- Do not concatenate files until columns, ID types and release metadata have been checked.
- Preserve original downloaded files unchanged; work from versioned copies.

## Data governance and release gate

Do not upload source extracts to this public repository unless IHME terms explicitly permit redistribution. Keep restricted files private and document access conditions. Do not report empirical findings until all extracts, mappings, units, hierarchy nesting, uncertainty fields and geographic definitions have passed independent review.
