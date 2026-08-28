# Nominatim Geocoder — Stats Report
Run: `nominatim_20260619_1134`
Source geocoder run: `all_pages_20260619_1044`
Generated: 2026-06-20 00:07

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
| 5f  | Nominatim outside Venice, flagged      | 2010 |
| 6   | Nominatim inside Venice, named place   | 380 |
| 6f  | Nominatim inside Venice, flagged       | 199 |
| 7a  | Centroid, no real address              | 380 |
| 7b  | Centroid, Nominatim failed             | 2064 |
| —   | Failed entirely                        | 4414 |

**Total geocoded (Nominatim):** 3252
**Total geocoded (centroid):** 2444
**Total failed:** 4414

## Provincia Section

| Class | Rows |
|-------|------|
| Outside-Venice Provincia rows | 0 |
| Inside-Venice Provincia rows  | 0 |

---

_End of report_