# Data acquisition protocol

1. Use the IHME GBD Results tool and explicitly select GBD 2023.
2. Select years 1990–2023, Nigeria, and the comparator geography defined in the protocol.
3. Export DALYs, YLLs and YLDs; retain metric (number/rate), sex, age, cause and uncertainty fields.
4. Obtain age-specific population estimates for decomposition from a documented compatible source/release.
5. For neurological causes, export the relevant cause hierarchy levels and retain cause IDs.
6. For vision, separately define impairment outcomes and ophthalmic causes. Do not merge these constructs without a justified estimand.
7. Record filters, query permalink, release, timestamp, units, standard population, hierarchy IDs, file checksum and access terms in the source manifest.
8. Keep source downloads private unless the provider explicitly permits redistribution. Never upload restricted extracts to this public repository.
9. Validate labels, units, duplicates, interval ordering, missing years and hierarchy nesting before analysis.
10. Freeze the analysis dataset and record a SHA-256 checksum before producing tables or figures.

## Geographic estimand gate

Western Sub-Saharan Africa is an IHME-defined region and is not automatically identical to a custom West Africa list. Name the intended comparator explicitly. Never sum a region with its component countries.

## Release gate

Do not report empirical findings until source extracts have passed validation and all mappings and filters have been independently reviewed.
