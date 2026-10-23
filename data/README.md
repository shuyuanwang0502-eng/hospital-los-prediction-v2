# Data

`healthcare_analytics.csv` is the course dataset (originally named `Topic3_healthcare_analytics_dataset (1).csv`), copied byte for byte. It is the same data as the public *AV Healthcare Analytics II* dataset.

* 455,495 rows, one per hospital admission, 18 columns.
* 318,438 rows have a `Stay` label (11 bins of 10 days, the last one "More than 100 Days"). They belong to 92,017 patients.
* 137,057 rows have no `Stay` label. None of their patients appear among the labeled rows. They are not used in the analysis.

| Column | Meaning | Available at admission? (assumption) |
|---|---|---|
| `case_id` | Admission identifier | identifier, not used |
| `Hospital_code` | Hospital (32) | yes |
| `Hospital_type_code`, `City_Code_Hospital`, `Hospital_region_code`, `Ward_Facility_Code` | Hospital properties (constant within each hospital) | yes |
| `Available Extra Rooms in Hospital` | Free rooms | yes, assumed to be a snapshot at admission |
| `Department` | Treating department (5) | yes, assumed assigned at admission |
| `Ward_Type` | Ward type P-U | yes, assumed admission ward |
| `Bed Grade` | Condition of the bed, 1-4 (113 labeled rows missing) | yes, assumed |
| `patientid` | Patient identifier | identifier, used only to group the data split |
| `City_Code_Patient` | Patient's city (4,532 labeled rows missing) | yes |
| `Type of Admission` | Trauma / Emergency / Urgent | yes |
| `Severity of Illness` | Minor / Moderate / Extreme | yes, assumed assessed at admission |
| `Visitors with Patient` | Number of visitors | **unclear**; may be counted during the stay. Excluded from the main model |
| `Age` | Age band (10-year bands) | yes |
| `Admission_Deposit` | Deposit paid at admission | yes |
| `Stay` | Length of stay (target) | outcome |

The dataset has no admission or discharge dates, and `case_id` is not in chronological order within a patient.
