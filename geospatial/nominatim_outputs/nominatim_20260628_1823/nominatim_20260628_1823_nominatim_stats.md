# Nominatim Geocoder — Stats Report
Run: `nominatim_20260628_1823`
Source geocoder run: `all_pages_20260619_1044`
Generated: 2026-07-03 17:21

---

## Classification

| Class | Rows |
|-------|------|
| outside_venice (regex) | 5125 |
| inside_venice (regex)  | 4985 |
| Total input            | 10110 |

## Geocoding Results

| Tier | Description | Rows |
|------|-------------|------|
| 5   | Nominatim outside Venice, real address | 663 |
| 5f  | Nominatim outside Venice, flagged      | 1645 |
| 6   | Nominatim inside Venice, named place   | 909 |
| 6f  | Nominatim inside Venice, flagged       | 608 |
| 7a  | Centroid, no real address              | 380 |
| 7b  | Centroid, Nominatim failed             | 2429 |
| —   | Failed entirely                        | 3476 |

**Total geocoded (Nominatim):** 3825
**Total geocoded (centroid):** 2809
**Total failed:** 3476

## Outside Venice detail

| Metric | Value |
|--------|-------|
| Nominatim matched (5+5f) | 2308 |
| Centroid placed (7a+7b)  | 2809 |
| Failed outside           | 8 |

## Inside Venice detail

| Metric | Value |
|--------|-------|
| Nominatim matched (6+6f) | 1517 |
| Failed inside            | 3468 |

## Provincia Section

| Class | Rows |
|-------|------|
| Outside-Venice Provincia rows | 0 |
| Inside-Venice Provincia rows  | 0 |

---

_End of report_