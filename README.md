# Global Burden of Disease in Nigeria and West Africa

**Principal author:** Ekemini Thompson  
**Primary setting:** Nigeria  
**Comparative setting:** West Africa  
**Primary data release:** GBD 2023 (estimates through 2023)  
**Period:** 1990–2023  
**Status:** Research protocol and reproducible analysis framework; empirical results are pending verified source data.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Research question

How has disease burden changed in Nigeria and West Africa, and how do neurological disorders and vision-related conditions contribute to DALYs, YLLs and YLDs, accounting for demographic change and uncertainty?

## Scientific integrity notice

This repository does **not** contain fabricated GBD observations or claim to reproduce IHME estimates independently. It provides a validated workflow for analysing lawfully obtained, versioned source data. Results remain pending until the required source extracts are added and validated. GBD uncertainty intervals are not treated as conventional confidence intervals. Point estimates and marginal interval bounds are not sufficient to reconstruct posterior draws or dependence structures.

## Core measures

- DALYs = YLLs + YLDs.
- YLLs = deaths × standard remaining life expectancy at age of death.
- YLDs follow the selected GBD release methodology; prevalence × disability weight is a conceptual summary and may require adjustments for comorbidity and sequelae.

Prefer published GBD estimates for DALYs, YLLs and YLDs. Do not recompute them from incomplete inputs.

## Data sources and acquisition

1. [IHME GBD Results](https://vizhub.healthdata.org/gbd-results/) — select GBD 2023 and record extraction details.
   - GBD 2023 flagship paper: https://doi.org/10.1016/S0140-6736(25)01637-X
   - Official GBD overview: https://healthdata.org/research-analysis/gbd
2. [IHME data resources](https://www.healthdata.org/data-tools-practices/data)
3. [WHO Global Health Observatory](https://www.who.int/data/gho)
4. [WHO World Report on Vision](https://www.who.int/publications/i/item/9789241516570)
5. [World Bank World Development Indicators](https://databank.worldbank.org/source/world-development-indicators)
6. [UN World Population Prospects](https://population.un.org/wpp/)

Access conditions, citation requirements and redistribution rights vary by source and release. Download the required extracts directly from their official providers. Do not commit restricted source files. Record release, extraction date, filters, units and source URL in `data/metadata/source_manifest.csv`.

### Expected analytical input

A harmonised CSV should contain at least:

`measure, location, year, sex, age, cause, metric, value, lower, upper`

Recommended values:
- `measure`: DALYs, YLLs, YLDs, deaths, prevalence, incidence
- `metric`: Number or Rate
- `value`, `lower`, `upper`: same units and scale
- `location`: standardised country or regional label
- `year`: integer
- `sex`, `age`, `cause`: source-defined categories

For robust uncertainty propagation, add posterior draw columns or a separate long-form draw file. The current pipeline validates summary estimates and plots marginal 95% uncertainty intervals; it does not infer joint uncertainty from summary bounds.

See `docs/data_dictionary.md` and `docs/methodology.md`.

## Quick start

```bash
git clone https://github.com/kebbidailynews/gbd-nigeria-west-africa.git
cd gbd-nigeria-west-africa
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp data/metadata/source_manifest_template.csv data/metadata/source_manifest.csv
# Add a permitted, harmonised extract at data/processed/gbd_harmonised.csv
python scripts/validate_data.py --input data/processed/gbd_harmonised.csv
python scripts/run_pipeline.py --input data/processed/gbd_harmonised.csv
pytest
```

Optional R workflow: install R >= 4.2 and packages `readr`, `dplyr`, `ggplot2`, `tidyr`; run `R/run_analysis.R data/processed/gbd_harmonised.csv`.

## Outputs

The pipeline writes:
- CSV summaries to `results/tables/`
- PNG figures (300 dpi) to `results/figures/`
- validation and run metadata to `results/statistical_outputs/`

Figures are generated only from the supplied validated data. Empty result directories are intentional until source data are provided.

## Repository map

- `src/`: validation, metrics, trend summaries and plotting
- `scripts/`: command-line entry points
- `R/`: complementary R analysis
- `tests/`: unit tests using explicitly synthetic test data
- `manuscript/`: protocol-stage manuscript
- `config/`: analysis settings and disease group mappings
- `data/`: no source data included by default

## Disease classification

The cause hierarchy must be mapped to the selected GBD release before analysis. Neurological and vision categories must be selected using the official release hierarchy. Avoid double-counting aggregate categories and their child causes. Vision impairment and ophthalmic causes are not interchangeable; document any supplementary WHO estimates separately.

## Manuscript and reporting

The manuscript is currently a protocol/framework, not a completed results paper. Use GATHER principles for health estimates and applicable STROBE guidance. Update title, year range, methods and results only after the release and data are verified.

## Reproducibility

Record:
- GBD release/version and download date
- source filters and location/cause hierarchy
- population standard used for age standardisation
- software versions and random seeds
- all transformations and exclusions
- uncertainty data structure and assumptions

## Citation

See `CITATION.cff`. Cite the exact GBD release and original data provider in any resulting publication.

## License

Original code is MIT-licensed. Third-party datasets remain subject to their own licences and access terms.

## Advanced analysis modules

- **Posterior-draw uncertainty:** pass `--draws path/to/draws.csv` to the pipeline. The long-form file must contain `measure, location, year, sex, age, cause, metric, draw_id, value`. The pipeline calculates empirical central 95% intervals from the draws. Draw-wise derived metrics must preserve draw pairing; see `docs/uncertainty_and_decomposition.md`.
- **Demographic decomposition:** `src/decomposition.py` provides an exact three-factor Shapley decomposition of burden change into total population growth, age-structure change and age-specific rate change. It requires comparable age-specific population and rate inputs at both endpoints.

These methods are available for analysis but are not evidence that the corresponding source data have already been acquired. Do not run a draw analysis on fabricated or independently re-numbered draws.

## Data acquisition gate

Follow [`docs/data_acquisition_protocol.md`](docs/data_acquisition_protocol.md)
before analysis. The primary study uses the GBD region Western Sub-Saharan Africa
only if that is the intended estimand; country-level West Africa must be explicitly
defined. Regional totals must never be added to constituent country estimates.
The official WHO GATHER checklist is tracked in
[`docs/GATHER_checklist.md`](docs/GATHER_checklist.md).
