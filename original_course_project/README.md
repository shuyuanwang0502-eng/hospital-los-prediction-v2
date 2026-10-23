# Original course project (group submission, unchanged)

**Course:** Programming, Technical University of Munich, summer semester 2025
**Team (Group 2):** Shuyuan Wang, Luoze Guo, Beibei Le, Ping-Jui Chen (Rick), Chia-Chen Li

This folder preserves the group's original work exactly as submitted. Nothing in it has been edited, re-run or re-scored. The revised study in the rest of this repository is a later, individual follow-up by Shuyuan Wang; it does not change or replace the group's results reported here.

| File | What it is |
|---|---|
| `Final Project_25 Rick Edition.ipynb` | The group's final notebook (byte-identical copy; SHA-256 `5577264…8360`) |
| `Presentation_python.pdf` | The slides presented in class (byte-identical copy) |

## What the project did

**Research questions** (from the course brief): *What are the key factors that influence hospital length of stay?* and *Can we predict a patient's length of stay from those factors?*

**Data preparation**
* Dropped rows without a `Stay` label; ran a "proxy MCAR test" (comparing group means) for the missing values of `Stay`, `Bed Grade` and `City_Code_Patient`.
* Filled missing `Bed Grade` and `City_Code_Patient` with the most frequent value.
* Dropped `case_id`, `patientid`, `Hospital_code`, `Hospital_region_code`, `City_Code_Hospital` and `City_Code_Patient` as identifiers without predictive value.
* Grouped the 11 `Stay` bins into `Stay_Category`: Short (0-20 days), Medium (21-50), Long (more than 50).
* Label-encoded admission type, severity and age band; one-hot encoded hospital type, department, ward type and ward facility; scaled the admission deposit to [0, 1].

**Exploratory analysis:** class distribution, severity vs stay category, deposit vs stay category, correlation heatmap and regression plots for features with |r| > 0.15.

**Models**
1. Ordinary least squares on the 0/1/2 stay category, using features with |correlation| > 0.10.
2. Random forest, hyper-parameters tuned with Optuna (5 trials, 3-fold cross-validation on the training split).
3. XGBoost, hyper-parameters tuned with Optuna (10 trials).

## Results as reported by the group

The notebook file contains **no saved cell outputs**; the numbers below are the ones written in its markdown cells and on the slides.

| Model | Reported result |
|---|---|
| OLS | Train R² 0.233, test R² 0.228, RMSE 0.62 (category units) |
| Random forest | Best Optuna cross-validation accuracy 0.604; slides: test accuracy about 61%, recall of the Short class about 40% |
| XGBoost | Test accuracy 61%; F1 0.50 (Short), 0.65 (Medium), 0.67 (Long); macro-F1 0.61 |

Conclusions of the group: tree models clearly beat the linear model, medium and long stays are predicted best, and `Visitors with Patient` is the most important feature.

## Known issues (documented, not fixed in this folder)

**Running the notebook as-is**
* It reads `Topic3_healthcare_analytics_dataset.csv`, while the course file is named `Topic3_healthcare_analytics_dataset (1).csv` (in this repository: `data/healthcare_analytics.csv`). To run it, place a copy of the data next to the notebook under the expected name.
* It needs `statsmodels`, `seaborn`, `xgboost` and `optuna`, which are installed from inside the notebook with `!pip install` cells. They are not part of the revised project's requirements.
* The random-forest Optuna search takes about 20 minutes (judging by the timestamps in the notebook).
* The XGBoost classification report in the markdown cell lists a support of 95,532 test rows (30% of the data), but the XGBoost code cell splits 25%, so the reported table seems to come from an earlier version of the code.

**Method issues** (explained in detail in [`../PROJECT_EVOLUTION.md`](../PROJECT_EVOLUTION.md))
* XGBoost hyper-parameters were chosen by **test-set accuracy**, so the reported 61% is optimistically biased.
* Train and test were split by admission, so the same patient could appear in both.
* `Visitors with Patient`, whose recording time is unknown and which may be counted during the stay, was the strongest feature.
* Hospital codes were removed although LOS differs strongly between hospitals.
* The correlation of visitors with the stay category was described as negative (r ≈ -0.42); it is positive (+0.42).
* The y-axis of the regression plots is labelled "0=Long, 2=Short"; the encoding is the reverse (0 = Short).
* OLS was fitted to class labels 0/1/2, which treats the distance between classes as equal and continuous.

The revised study re-creates the original random forest (its encoding and its tuned hyper-parameters) to test how these choices affect the score; see Section 9.5 of [`../notebooks/LOS_study.ipynb`](../notebooks/LOS_study.ipynb).
