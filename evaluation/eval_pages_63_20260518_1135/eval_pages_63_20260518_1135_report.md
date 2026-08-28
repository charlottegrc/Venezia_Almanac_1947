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

- Pages evaluated: 1
- Propagation failures: 1


## Failure Reason Summary

- COMPLEX_LAYOUT_OK: 1 pages

## Page Summary Table

Sorted by priority (worst first).

| Page        |   Runs Found |   Rows Min |   Rows Max |   Row Variation | Schema OK   | Prop Flag   | Schema Drift                     | Has GT   |   Best F1 |   Best Char Acc | Failure Reasons   | Missing   | Action   |
|:------------|-------------:|-----------:|-----------:|----------------:|:------------|:------------|:---------------------------------|:---------|----------:|----------------:|:------------------|:----------|:---------|
| page_63.jpg |            3 |         63 |         64 |               1 | ✓           |             | Additional Info; Additional Info |          |     98.28 |           91.81 | COMPLEX_LAYOUT_OK |           | OK       |