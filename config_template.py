# ============================================================
#  VENICE ALMANAC — CONFIGURATION TEMPLATE
#  Copy this file to config.py and fill in your local paths.
#
#  SETUP INSTRUCTIONS:
#  1. Copy this file: cp config_template.py config.py
#  2. Create the local almanac root folder
#  3. Fill in your absolute paths below
#  4. The local folder structure must mirror Drive exactly:
#
#  Venezia_Almanac_1947/          ← LOCAL_ALMANAC_ROOT
#      pages/                     ← PAGES_DIR (notebook 01 temp working dir)
#      llm_ocr_results/           ← OCR_RESULTS_DIR
#          page_10/
#          page_11/
#          ...
#          provincia/
#      logs/                      ← LOGS_DIR
#      evaluation/                ← EVAL_OUTPUT_DIR
#      clean_pages/               ← CLEAN_PAGES_DIR
#      clean_pages_llm/           ← LLM_LOG_DIR (legacy LLM-arbitration selector output)
#      geospatial/                ← GEOSPATIAL_DIR
#          outputs/               ← GEOCODER_OUTPUT_DIR
#          final/combined_geocoded_inside_venice.csv/.geojson  ← final combined dataset
#          final/detail/csv/      ← FINAL_DETAIL_CSV_DIR
#          final/detail/geojson/  ← FINAL_DETAIL_GEOJSON_DIR
#          final/cleaning/        ← role/profession/category cleaning-stage CSVs
#          final/audit/           ← FINAL_AUDIT_DIR
#      ocr_choices/               ← OCR_CHOICES_DIR (notebook 00 test data)
#          choice1_ocr_engine/
#          choice2_architecture/
#          choice3_diversity_validation/
#      stats/                     ← STATS_DIR (notebook 04 outputs)
#      stats_geo_analysis/        ← STATS_GEO_DIR (notebook 08 outputs)
#          reference/{category,occupation,profession}/  (pinned/cached clustering state, shared across runs)
#          RUN_TAG/
#              general/{csv,figures}
#              category/{csv,figures}
#              profession/{csv,figures}
#              occupation/{csv,figures}     (only present for runs that did occupation resolution)
#
#  Also under the root:
#      almanac_1947.pdf           ← PDF_PATH (committed to git)
#      token.pickle               ← TOKEN_PICKLE (not committed — create it yourself)
#      credentials.json           ← CREDENTIALS_JSON (not committed — create it yourself)
#      openapikey.txt             ← OPENAI_KEY_FILE (not committed — create it yourself)
# ============================================================

# ── Project root ─────────────────────────────────────────────
# This folder mirrors Venezia_Almanac_1947/ on Google Drive.
LOCAL_ALMANAC_ROOT = "/path/to/your/Venezia_Almanac_1947"

# ── Subfolders — names must match Drive folder names exactly ──
PAGES_DIR           = LOCAL_ALMANAC_ROOT + "/pages"
OCR_RESULTS_DIR     = LOCAL_ALMANAC_ROOT + "/llm_ocr_results"
LOGS_DIR            = LOCAL_ALMANAC_ROOT + "/logs"
EVAL_OUTPUT_DIR     = LOCAL_ALMANAC_ROOT + "/evaluation"
CLEAN_PAGES_DIR     = LOCAL_ALMANAC_ROOT + "/clean_pages"
PROGRESS_FILE       = LOCAL_ALMANAC_ROOT + "/progress.txt"
GROUND_TRUTH_DIR = LOCAL_ALMANAC_ROOT + "/ground_truth"
OCR_CHOICES_DIR  = LOCAL_ALMANAC_ROOT + "/ocr_choices"
STATS_DIR        = LOCAL_ALMANAC_ROOT + "/stats"        # notebook 04 outputs
STATS_GEO_DIR    = LOCAL_ALMANAC_ROOT + "/stats_geo_analysis"  # notebook 08 outputs
LLM_LOG_DIR      = LOCAL_ALMANAC_ROOT + "/clean_pages_llm"  # legacy LLM-arbitration selector output

# ── Geospatial files ─────────────────────────────────────────
GEOSPATIAL_DIR      = LOCAL_ALMANAC_ROOT + "/geospatial"
SESTIERE_PATH       = GEOSPATIAL_DIR + "/sestiere.geojson"
PARISHES_PATH       = GEOSPATIAL_DIR + "/parishes.geojson"
NCIV_PATH           = GEOSPATIAL_DIR + "/n_civ.geojson"
REF_TABLE_PATH      = GEOSPATIAL_DIR + "/venice_location_reference_table.csv"
GEOCODER_OUTPUT_DIR = GEOSPATIAL_DIR + "/outputs"
NOMINATIM_OUTPUT_DIR = GEOSPATIAL_DIR + "/nominatim_outputs"
FINAL_OUTPUT_DIR     = GEOSPATIAL_DIR + "/final"
FINAL_DETAIL_CSV_DIR       = FINAL_OUTPUT_DIR + "/detail/csv"
FINAL_DETAIL_GEOJSON_DIR   = FINAL_OUTPUT_DIR + "/detail/geojson"
FINAL_CLEANING_DIR         = FINAL_OUTPUT_DIR + "/cleaning"
FINAL_AUDIT_DIR            = FINAL_OUTPUT_DIR + "/audit"


# ── PDF + local secrets ───────────────────────────────────────
# PDF_PATH is committed to git, under the project root.
# The other three are not committed — create them yourself.
PDF_PATH         = "almanac_1947.pdf"
TOKEN_PICKLE     = "token.pickle"
CREDENTIALS_JSON = "credentials.json"
OPENAI_KEY_FILE  = "openapikey.txt"

# ── Drive folder names ───────────────────────────────────────
# Do not change these unless you rename the folders on Drive.
DRIVE_ROOT_FOLDER        = "Venezia_Almanac_1947"
DRIVE_IMAGES_FOLDER      = "images"
DRIVE_OCR_FOLDER         = "llm_ocr_results"
DRIVE_CLEAN_PAGES_FOLDER = "clean_pages"
DRIVE_EVALUATION_FOLDER  = "evaluation"
DRIVE_GEOSPATIAL_FOLDER = "geospatial"
DRIVE_OUTPUTS_FOLDER    = "outputs"
DRIVE_NOMINATIM_FOLDER = "nominatim_outputs"
DRIVE_FINAL_FOLDER   = "final"
DRIVE_LOGS_FOLDER        = "logs"
DRIVE_PROVINCIA_FOLDER   = "provincia"
DRIVE_LLM_LOG_FOLDER     = "clean_pages_llm"
DRIVE_STATS_FOLDER       = "stats_geo_analysis"
DRIVE_OCR_CHOICES_FOLDER = "ocr_choices"
DRIVE_STATS4_FOLDER      = "stats"  # notebook 04 outputs — distinct from DRIVE_STATS_FOLDER (notebook 08)

# ── Save mode ─────────────────────────────────────────────────
# Single switch for every notebook's local/Drive I/O (see drive_utils.py).
# "local" = save/load only locally | "drive" = only Drive | "both" = both.
SAVE_MODE = "drive"

# ── Eval fallback paths ──────────────────────────────────────
# Only used by the version selector if no eval_all_ folder is found.
# Normally auto-detected — you should not need to change these.
EVAL_RESULTS_CSV = EVAL_OUTPUT_DIR + "/fallback_results.csv"
EVAL_SUMMARY_CSV = EVAL_OUTPUT_DIR + "/fallback_summary.csv"