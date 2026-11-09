# Global Burden of Disease in Nigeria and West Africa

**Principal author:** Ekemini Thompson  
**Primary setting:** Nigeria  
**Regional benchmark:** Western Sub-Saharan Africa (GBD region; includes Nigeria)  
**Primary data release:** GBD 2023 (estimates through 2023)  
**Period:** 1990–2023  
**Status:** Research protocol and reproducible analysis framework; empirical results are pending verified source data.

[![Tests](https://github.com/kebbidailynews/gbd-nigeria-west-africa/actions/workflows/tests.yml/badge.svg)](https://github.com/kebbidailynews/gbd-nigeria-west-africa/actions/workflows/tests.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Research question

How has disease burden changed in Nigeria and the GBD Western Sub-Saharan Africa region, and how do neurological disorders and vision-related conditions contribute to DALYs, YLLs and YLDs, accounting for demographic change and uncertainty?

## Scientific integrity notice

This repository does not contain fabricated GBD observations or claim to reproduce IHME estimates independently. It provides a reproducible workflow for analysing lawfully obtained, versioned source data. Results remain pending until the required source extracts are added and validated. GBD uncertainty intervals are not treated as conventional confidence intervals. Point estimates and marginal interval bounds are not sufficient to reconstruct posterior draws or dependence structures.

## Critical geographic qualification

Nigeria is included in the GBD Western Sub-Saharan Africa regional estimate. The regional estimate is therefore a nested benchmark, not an independent comparator. If a leave-Nigeria-out comparator is required, verify the exact GBD 2023 country membership and aggregate compatible country counts and denominators (or paired draws). Never use an unweighted mean of country rates. See the data acquisition protocol.

## Core measures

- DALYs = YLLs + YLDs.
- YLLs = deaths multiplied by standard remaining life expectancy at age of death.
- YLDs follow the selected GBD release methodology; prevalence multiplied by disability weight is a conceptual summary and may require adjustments for comorbidity and sequelae.

Prefer published GBD estimates for DALYs, YLLs and YLDs. Do not recompute them from incomplete inputs.

## Neurological and vision estimands

The primary neurological analysis uses the basic GBD Level 2 neurological cause group. A separately labelled expanded nervous-system analysis may include selected conditions from other GBD branches, but must be prespecified and must avoid overlap. These are not interchangeable estimands.

Vision impairment (blindness and vision loss) is selected in the impairment context. Ophthalmic causes (such as cataract, refractive disorders, glaucoma, diabetic retinopathy and age-related macular degeneration) are selected separately in the cause context. Do not add impairment totals to cause totals.

See [the estimand specification](docs/neurological_and_vision_estimands.md) and [the provisional mapping](config/disease_mapping.yaml). Final classifications require GBD 2023 IDs and hierarchy levels.

## Data sources and acquisition

1. [IHME GBD Results Tool](https://vizhub.healthdata.org/gbd-results/) — select GBD 2023 and record extraction details.
2. [GBD 2023 flagship study](https://doi.org/10.1016/S0140-6736(25)01637-X).
3. [IHME GBD overview](https://healthdata.org/gbd).
4. [WHO Global Health Observatory](https://www.who.int/data/gho).
5. [WHO World Report on Vision](https://www.who.int/publications/i/item/9789241516570).

An account is required to download estimates from the GBD Results Tool. Use narrow query batches: the tool documentation warns that very large queries can omit requested dimensions. Download cause and impairment contexts separately, retain IDs and names, and reconcile expected dimensions before analysis.

Access conditions, citation requirements and redistribution rights vary by source and release. Do not commit restricted source files. Record release, extraction date, filters, units, source URL, query permalink and SHA-256 checksum in the source manifest.

### Expected analytical input

The harmonised CSV must contain:

    measure, location, year, sex, age, cause, metric, value, lower, upper

Recommended optional fields include location_id, cause_id, parent_cause_id, hierarchy_level, estimate_context, age_standard, and source_file. Preserve original source IDs and labels. Do not replace IDs with fuzzy text matching.

For robust uncertainty propagation, add posterior draw columns or a separate long-form draw file. GBD 2023 uses 250 draws for its reported estimates; use the original draw IDs when available and permitted. Do not synthesize or independently re-number draws.

See [the data dictionary](docs/data_dictionary.md), [methods framework](docs/methodology.md), and [acquisition protocol](docs/data_acquisition_protocol.md).

## Quick start

    git clone https://github.com/kebbidailynews/gbd-nigeria-west-africa.git
    cd gbd-nigeria-west-africa
    python -m venv .venv

Activate the environment (macOS/Linux: source .venv/bin/activate; Windows PowerShell: .venv\Scripts\Activate.ps1), then:

    pip install -r requirements.txt
    cp data/metadata/source_manifest_template.csv data/metadata/source_manifest.csv
    python scripts/validate_data.py --input data/processed/gbd_harmonised.csv
    python scripts/run_pipeline.py --input data/processed/gbd_harmonised.csv
    pytest -q

Optional R workflow: install R >= 4.2 and packages readr, dplyr, ggplot2 and tidyr; run Rscript R/run_analysis.R data/processed/gbd_harmonised.csv.

## Outputs

The pipeline writes CSV summaries to results/tables, PNG figures (300 dpi) to results/figures, and run metadata to results/statistical_outputs. Figures are generated only from supplied validated data. Empty result directories are intentional until source data are provided.

## Repository map

- src/: validation, metrics, uncertainty, decomposition, trends and plotting
- scripts/: command-line entry points
- R/: complementary R analysis
- tests/: unit tests using explicitly synthetic test data
- manuscript/: protocol-stage manuscript
- config/: analysis settings and provisional disease group mappings
- data/: no source data included by default
- docs/: methods, data acquisition, estimands, limitations and reporting guidance

## Reporting and reproducibility

Follow the 18-item [GATHER reporting checklist](https://www.who.int/data/gather) and applicable STROBE guidance. Record the GBD release, download date, query filters, source IDs, population standard, units, software versions, transformations, exclusions and checksums. See the GATHER tracker in docs/GATHER_checklist.md.

## Advanced analysis modules

- Posterior-draw uncertainty: pass --draws path/to/draws.csv to the pipeline. The long-form file must contain estimate-identifying columns plus draw_id and value. Preserve original pairing.
- Demographic decomposition: src/decomposition.py decomposes change into total population growth, age-structure change and age-specific rate change. It requires compatible age-specific populations and rates at both endpoints.

These methods are available for analysis but do not indicate that source data have already been acquired.

## Manuscript status

The manuscript is a protocol/framework, not a completed empirical paper. No empirical findings should be written until the official extracts, hierarchy mappings, units, uncertainty data and geographic definitions pass review.

## Citation and licensing

See CITATION.cff. Cite the exact GBD release and original data provider in any resulting publication. Original code is MIT-licensed; third-party datasets remain subject to their own licences and access terms.
