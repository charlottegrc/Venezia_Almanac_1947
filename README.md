# Venezia Almanac 1947

A research pipeline that extracts, cleans, and geocodes structured data from a 1947
Venetian commercial almanac (575 scanned pages). It turns page scans into a
geocoded, occupation-classified dataset of businesses and residents for spatial
analysis.

The pipeline is a sequence of notebooks, run in numeric order, sharing two
Python modules (`config.py`, `drive_utils.py`). Every notebook can read/write
locally, to Google Drive, or both — see [Local vs. Drive I/O](#local-vs-drive-io)
below.

---

## Table of contents

- [Setup](#setup)
- [Pipeline: what to run, in what order](#pipeline-what-to-run-in-what-order)
- [Repository structure](#repository-structure)
- [Shared modules](#shared-modules)
- [Notebook reference](#notebook-reference)
- [Local vs. Drive I/O](#local-vs-drive-io)
- [Conventions](#conventions)

---

## Setup

Steps to go from a fresh clone to a runnable pipeline, in order:

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Requires Python 3.10+ (developed against 3.13).

### 2. Create `config.py` from the template

```bash
cp config_template.py config.py
```

Open `config.py` and set:

- **`LOCAL_ALMANAC_ROOT`** — absolute path to this project folder.
- **`SAVE_MODE`** — `"local"`, `"drive"`, or `"both"`.
  `"drive"` or `"both"` require a Google account — see [Local vs. Drive I/O](#local-vs-drive-io).
- The four **`PDF_PATH` / `TOKEN_PICKLE` / `CREDENTIALS_JSON` / `OPENAI_KEY_FILE`**
  paths — see step 3.

Every other constant is a subfolder name under `LOCAL_ALMANAC_ROOT`.

### 3. Provide the files `config.py` points at

| File | Constant | How to get it |
|---|---|---|
| `almanac_1947.pdf` | `PDF_PATH` | the source PDF scan — feeds notebook 01, in the [project root](./almanac_1947.pdf) |
| `openapikey.txt` | `OPENAI_KEY_FILE` | a plain-text file containing one line: `api_key=sk-...` (your OpenAI API key) |
| `credentials.json` | `CREDENTIALS_JSON` | only needed if `SAVE_MODE` includes `"drive"` — an OAuth **Desktop app** client secret downloaded from the [Google Cloud Console](https://console.cloud.google.com/) (enable the Drive API on the project first) |
| `token.pickle` | `TOKEN_PICKLE` | **don't create this yourself** — the first notebook cell that calls `get_drive_service()` opens a browser OAuth consent screen and writes this file automatically. If the token later expires, delete it and re-run. |

`config_template.py`'s default paths for these four are bare filenames (e.g.
`"token.pickle"`), meaning they're expected directly in the project root next to
the notebooks.

### 4. Run the pipeline

Notebooks `01` → `08`, in numeric order, each one reading what the
previous one wrote. Notebook `00` is optional/exploratory and can be run
independently at any time.

Note: Notebook 07 reads a hardcoded `NOMINATIM_RUN_NAME` — after running notebook
06, update that variable to point at the run you just produced before executing
notebook 07.

---

## Pipeline: what to run, in what order

```
PDF → [01 OCR] → llm_ocr_results/
                → [02 eval] → evaluation/eval_all_*/
                → [03 version select] → clean_pages/page_N/*.csv
                → [04 stats] (read-only reporting)
                → [05 geocoder: sestiere/parish/civic-number matching]
                     → geospatial/outputs/RUNTAG_TIMESTAMP/
                → [06 nominatim geocoder] → geospatial/nominatim_outputs/
                → [07 check & clean: n_civ recheck, interpolation]
                     → geospatial/final/
                → [08 geo stats: clustering, heatmaps] → stats_geo_analysis/
```

| # | Notebook | Reads | Writes |
|---|---|---|---|
| 0 | `00_model_selection.ipynb` | test data under `ocr_choices/` | comparison CSVs back into `ocr_choices/choiceN_*/` |
| 1 | `01_ocr_pipeline.ipynb` | `almanac_1947.pdf`, `progress.txt` checkpoint | `llm_ocr_results/page_N/` |
| 2 | `02_evaluation.ipynb` | `llm_ocr_results/`, `ground_truth/` | `evaluation/eval_all_<timestamp>/` |
| 3 | `03_version_selector.ipynb` | `llm_ocr_results/`, `evaluation/` | `clean_pages/page_N/page_N_semantic.csv` + `page_N_ocr.txt` |
| 4 | `04_statistics.ipynb` | `evaluation/`, `clean_pages/` (read-only) | `stats/` (CSVs + `stats/figures/`) |
| 5 | `05_geocoder.ipynb` | `clean_pages/`, `geospatial/*.geojson` + reference CSV | `geospatial/outputs/RUNTAG_TIMESTAMP/` |
| 6 | `06_nominatim_geocoder.ipynb` | latest `geospatial/outputs/` run | `geospatial/nominatim_outputs/nominatim_TIMESTAMP/` |
| 7 | `07_check_and_clean.ipynb` | a specific `NOMINATIM_RUN_NAME` (hardcoded per run — update before running) | `geospatial/final/detail/{csv,geojson}/`, `geospatial/final/cleaning/`, `geospatial/final/audit/`, plus `combined_geocoded_outside_venice` and `centroid` (csv+geojson) directly in `geospatial/final/` |
| 8 | `08_geo_stats.ipynb` | `geospatial/final/detail/` | `stats_geo_analysis/RUN_TAG/`, plus `combined_geocoded_inside_venice` and `occupation_inside_venice_geocoded_RUN_TAG` (csv+geojson) directly in `geospatial/final/` |

---

## Repository structure

```
Venezia_Almanac_1947/
├── 00_model_selection.ipynb .. 08_geo_stats.ipynb   ← the pipeline, run in order
├── config_template.py         ← template for config.py (committed)
├── drive_utils.py             ← shared Drive I/O helpers
├── requirements.txt
├── progress.txt               ← notebook 01's resume checkpoint (created at runtime)
├── pages/                     ← notebook 01's temp working dir (page images, transient)
├── llm_ocr_results/           ← raw OCR + extraction output, stage 01
├── evaluation/                ← per-page quality scores, stage 02
├── clean_pages/                ← winning OCR run per page, stage 03 (the pipeline's canonical per-page text)
├── clean_pages_llm/            ← legacy LLM-arbitration version selector output (superseded design, kept for reference)
├── ground_truth/               ← manually-verified pages used to score OCR quality
│   ├── txt/
│   └── csv/
├── ocr_choices/                ← notebook 00's test data + results (OCR engine / architecture / prompt-diversity comparisons)
│   ├── choice1_ocr_engine/
│   ├── choice2_architecture/
│   └── choice3_diversity_validation/
├── stats/                      ← notebook 04 output (evaluation/version-selection reporting)
│   └── figures/
├── geospatial/                 ← reference geodata + all geocoder output
│   ├── sestiere.geojson, parishes.geojson, n_civ.geojson, venice_location_reference_table.csv  (committed, read locally)
│   ├── outputs/                ← notebook 05 output
│   ├── nominatim_outputs/      ← notebook 06 output
│   └── final/                  ← consolidated geocoded datasets — the thesis reads directly from here
│       ├── combined_geocoded_inside_venice.csv/.geojson, combined_geocoded_outside_venice.csv/.geojson, centroid.csv/.geojson, occupation_inside_venice_geocoded_RUN_TAG.csv/.geojson
│       ├── detail/{csv,geojson}/    ← notebook 07's per-stage matched/unmatched files
│       ├── cleaning/                ← role/profession/category cleaning-stage CSVs
│       └── audit/                   ← diagnostic/reconciliation reports
├── stats_geo_analysis/         ← notebook 08 output (clustering, occupation classification, heatmaps)
│   ├── reference/{category,occupation,profession}/
│   └── <RUN_TAG>/{general,category,profession,occupation}/{csv,figures}
├── overleaf/                   ← thesis LaTeX source
└── logs/                       ← raw notebook-01 run logs
```

`geospatial/final/` holds the pipeline's consolidated deliverables directly at its root: `combined_geocoded_inside_venice` and `combined_geocoded_outside_venice` (every matched row for each zone), `centroid` (every centroid-fallback match across both zones), and `occupation_inside_venice_geocoded_<RUN_TAG>` (the inside-Venice dataset with occupation classification). `detail/` holds the per-stage matched/unmatched files these are assembled from, `cleaning/` holds role/profession/category cleaning-stage CSVs, and `audit/` holds diagnostic/reconciliation reports.

---

## Shared modules

### `config.py` / `config_template.py`

Every local path, every Drive folder name, and the global `SAVE_MODE` switch
(`"local"` / `"drive"` / `"both"`) that every notebook's I/O respects.

### `drive_utils.py`

Implementation of Drive auth (OAuth via `credentials.json` → cached
`token.pickle`), folder lookup/creation, file download/upload, and the
`save_or_upload_{csv,geojson,text}` helpers every notebook calls. These default to
`config.SAVE_MODE` when the caller doesn't pass `save_mode` explicitly. Also home
to `find_run_folder()` (picks the newest `RUN_TAG`-named run folder by parsing the
timestamp embedded in the folder name) and `find_csv_by_name()`
(recursive filename search).

---

## Notebook reference

### 00 — Model & Method Selection (`00_model_selection.ipynb`)
Exploratory only, run before/independent of the main sequence. Three comparisons,
each self-contained in its own `ocr_choices/choiceN_*/` folder:
- **choice 1** (`choice1_ocr_engine/`) — OCR engine comparison (e.g. Gemini vs GPT reading) against 2 ground-truth pages.
- **choice 2** (`choice2_architecture/`) — extraction architecture/strategy comparison on page 70.
- **choice 3** (`choice3_diversity_validation/`) — broader validation across a diverse page sample (`exploration_outputs/`).

### 01 — OCR & Semantic Extraction (`01_ocr_pipeline.ipynb`)
Main production pipeline: PDF pages in (via `pdf2image`), semantic CSV + raw OCR
text out. Has a `RUN_MODE` switch (`full` / `pages` / `range`) and a `progress.txt`
checkpoint so it can resume or skip already-processed pages. Writes to
`llm_ocr_results/page_N/`.

### 02 — Evaluation (`02_evaluation.ipynb`)
Scores OCR output quality per page. Writes an `evaluation/eval_all_<timestamp>/` folder.

### 03 — Version Selection (`03_version_selector.ipynb`)
Picks the best run per page using notebook 02's scores, writes the winner to
`clean_pages/page_N/page_N_semantic.csv` + matching `page_N_ocr.txt`.

### 04 — Statistics (`04_statistics.ipynb`)
Read-only reporting over the outputs of stages 02–03. Produces the OCR/extraction-quality figures and
summary tables under `stats/`.

### 05 — Geocoder (`05_geocoder.ipynb`)
Matches each row's `Address`/`Location` text to real Venice coordinates using the
local reference GeoJSONs (`geospatial/sestiere.geojson`, `parishes.geojson`,
`n_civ.geojson`, `venice_location_reference_table.csv`). Writes `geospatial/outputs/RUNTAG_TIMESTAMP/`
(geocoded / unmatched / ambiguous CSVs + GeoJSON + a markdown report).

### 06 — Nominatim Geocoder (`06_nominatim_geocoder.ipynb`)
Second-pass geocoding via the public Nominatim API for rows notebook 05 couldn't
resolve. Writes `geospatial/nominatim_outputs/nominatim_TIMESTAMP/`.

### 07 — Check and Clean (`07_check_and_clean.ipynb`)
Post-Nominatim enrichment: final cross-source stats. Reads a specific
`NOMINATIM_RUN_NAME` — hardcoded per run, update it to point at the Nominatim run
being enriched before executing. Syncs the latest useful files from notebook
05/06's run folders into `geospatial/final/detail/{csv,geojson}/` (overwriting the
previous state), writes diagnostic exports to `geospatial/final/audit/` and
cleaning-stage CSVs to `geospatial/final/cleaning/`, and builds the consolidated
`combined_geocoded_outside_venice` and `centroid` datasets directly in
`geospatial/final/`.

### 08 — Geo Stats (`08_geo_stats.ipynb`)
Combines the designated inside-Venice files from `geospatial/final/detail/` and
produces:
- hex-density heatmaps (overall, and split by Category / Profession / Role),
- k-means clustering of raw Category/Profession/Occupation text into classes
  (two parallel methods — "direct" and "tokenised"/LLM-canonicalized —
  compared against each other),
- an LLM-based **occupation resolution** stage that merges each row's
  Category/Role/Profession fields into one `occupation` value, flags contradictions
  between fields, and applies deterministic overrides for known filler/institution
  values.

Every run writes to its own `stats_geo_analysis/<RUN_TAG>/` folder, plus the
consolidated `combined_geocoded_inside_venice` and
`occupation_inside_venice_geocoded_<RUN_TAG>` datasets directly to
`geospatial/final/`.

---

## Local vs. Drive I/O

Nearly every notebook follows the same pattern:

- **Read**: try the local path first, fall back to Drive.
- **Write**: write local and/or Drive per `config.SAVE_MODE`, mirroring the exact
  same folder structure on both sides.

---

## Conventions

- **`RUN_TAG`** — a `datetime.now()` timestamp generated once per notebook
  execution (05, 06, 08), used to namespace that run's whole output folder so
  reruns never silently overwrite a previous run's results.
- **Accumulating outputs** — several stages write a fresh timestamped folder every
  run with nothing automatically deleting old ones.
