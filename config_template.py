#  VENICE ALMANAC — CONFIGURATION TEMPLATE
#  Copy this file to config.py and fill in your local paths.
#
#  SETUP INSTRUCTIONS:
#  1. Copy this file: cp config_template.py config.py
#  2. Create the local almanac root folder
#  3. Fill in your absolute paths below
#  4. The local folder structure must mirror Drive exactly


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
STATS_DIR        = LOCAL_ALMANAC_ROOT + "/stats"        
STATS_GEO_DIR    = LOCAL_ALMANAC_ROOT + "/stats_geo_analysis"  
LLM_LOG_DIR      = LOCAL_ALMANAC_ROOT + "/clean_pages_llm"  

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
# PDF_PATH is under the project root.
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
DRIVE_STATS4_FOLDER      = "stats"  

# ── Save mode ─────────────────────────────────────────────────
# for every notebook's local/Drive I/O (see drive_utils.py).
# "local" = save/load only locally | "drive" = only Drive | "both" = both.
SAVE_MODE = "drive"

# ── Eval fallback paths ──────────────────────────────────────
# Only used by the version selector if no eval_all_ folder is found.
# Normally auto-detected — should not need to change these.
EVAL_RESULTS_CSV = EVAL_OUTPUT_DIR + "/fallback_results.csv"
EVAL_SUMMARY_CSV = EVAL_OUTPUT_DIR + "/fallback_summary.csv"