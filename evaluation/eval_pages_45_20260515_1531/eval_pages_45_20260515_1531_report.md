# OCR Evaluation Report


## Log Anomalies

- LOG WARNING: run_1_all.log is NOT May 4th run → ignored for baseline signals


### page_45.jpg

**page_45.jpg_semantic_1.csv**
- Rows: 42 | Empty: 0 | Truncated: 0
- Layout: COMPLEX_LAYOUT | Ad type: NO_AD
- Schema: Name,Address,Location,Role,Profession
- Flags: propagation_address
- ⚠ -> WARNING: 25 rows (47%) missing both Address and Location on page_45.jpg
- Issues: extra_cols:{'Additional Info', 'page'}

**page_45.jpg_semantic_2.csv**
- Rows: 42 | Empty: 0 | Truncated: 0
- Layout: COMPLEX_LAYOUT | Ad type: NO_AD (pure structured directory content)
- Schema: Name,Address,Location,Role,Profession
- Flags: propagation_address
- ⚠ -> WARNING: 41 rows (75%) missing both Address and Location on page_45.jpg
- Issues: extra_cols:{'page'}

**page_45.jpg_semantic_1.csv**
- Rows: 42 | Empty: 0 | Truncated: 0
- Layout: COMPLEX_LAYOUT | Ad type: NO_AD
- Schema: Name,Address,Location,Role,Profession
- Flags: propagation_address
- ⚠ -> WARNING: 25 rows (47%) missing both Address and Location on page_45.jpg
- Issues: extra_cols:{'Additional Info', 'page'}

- Pages evaluated: 1
- Propagation failures: 1


## Failure Reason Summary

- COMPLEX_LAYOUT_OK: 1 pages

## Provincia Aggregate Files

- No provincia aggregate files found.