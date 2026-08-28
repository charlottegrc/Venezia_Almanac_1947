# OCR Evaluation Report


## Log Anomalies

- LOG WARNING: run_1_all.log is NOT May 4th run → ignored for baseline signals


### page_63.jpg

**page_63.jpg_semantic_1.csv**
- Rows: 64 | Empty: 0 | Truncated: 0
- Layout: COMPLEX_LAYOUT | Ad type: PARTIAL_AD
- Schema: Name,Address,Location,Role,Profession
- Flags: propagation_address

**page_63.jpg_semantic_2.csv**
- Rows: 63 | Empty: 0 | Truncated: 0
- Layout: COMPLEX_LAYOUT | Ad type: 
- Schema: Name,Address,Location,Role,Profession
- Flags: propagation_address

**page_63.jpg_semantic_1.csv**
- Rows: 64 | Empty: 0 | Truncated: 0
- Layout: COMPLEX_LAYOUT | Ad type: PARTIAL_AD
- Schema: Name,Address,Location,Role,Profession
- Flags: propagation_address


## Summary

- Pages evaluated: 1
- Pages with propagation flags: 0
- Pages missing files: 0


## Pages Needing Attention

Only real structural errors listed here. Complex layout and full-ad pages are not errors.

- None

## Missing Files

- None

## Address/Location Coverage

Counts from the **final saved CSV** after propagation ran. Pipeline log warnings (pre-propagation) are not used here. A flag means >30% of rows have neither Address nor Location.

### Clean

- **page_63.jpg**: 0 rows | both missing: 0 | addr only missing: 0 | loc only missing: 0

## Ground Truth Results

Pages with ground truth: 1

- **page_63.jpg** (best run): char_acc=91.81 | bow=66.2 | F1=98.28 | precision=99.13 | recall=97.44 | row_similarity=100.0

## Page Summary Table

Full summary saved as `eval_pages_63_20260519_0054_page_summary.csv` — 1 pages, sorted by priority. Open and filter `Action != OK` for pages needing review.

- OK: 1 pages