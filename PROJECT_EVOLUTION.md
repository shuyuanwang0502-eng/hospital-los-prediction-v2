# Project Evolution: from the course project to the revised study

This document records what changed between the original group project ([`original_course_project/`](original_course_project/)) and the revised individual study ([`notebooks/LOS_study.ipynb`](notebooks/LOS_study.ipynb)), why, and what each change did to the results. All numbers for the revised study come from [`results/metrics.json`](results/metrics.json).

**Authorship.** The original project is the joint work of Group 2 (Shuyuan Wang, Luoze Guo, Beibei Le, Ping-Jui Chen, Chia-Chen Li). The revised study is a later follow-up by Shuyuan Wang alone. The original files, outputs and conclusions are preserved unchanged.

## 1. In short

| | Original course project | Revised study |
|---|---|---|
| Question | Which factors influence LOS, and can we predict the 3-class LOS? | The same, made specific: predict at admission for **patients not seen before**, and test the use for bed planning |
| Information used | All columns except IDs and hospital codes, **including Visitors** | Only fields plausibly available at admission; Visitors and cross-admission aggregates as clearly labeled supplements |
| Evaluation | Random split of admissions; XGBoost tuned on the test set | Split by patient into training, validation and test; selection on validation only; test used once |
| Headline result | 61% accuracy (XGBoost) | 54.1% accuracy, 48.5% macro-F1 (gradient boosting, no Visitors); 62.7% with Visitors |
| Use of results | Feature importance and conclusions about classes | Plus baselines, confidence intervals, error analysis, a probability check and simulated planning scenarios |

**The two headline numbers are not directly comparable.** The original answers an easier question (Visitors included, same patients possibly on both sides of the split, test-set tuning). The controlled comparison in Section 3 separates these effects.

## 2. Changes by type

Columns: what the original did or what was wrong; what changed; why; how it is implemented (notebook section); the actual effect and its limits.

### 2.1 Fixes of errors

| Original approach or issue | Change in the revised study | Why | How | Actual effect and limits |
|---|---|---|---|---|
| XGBoost hyper-parameters were chosen by **test-set accuracy** (Optuna objective = test accuracy) | Model and hyper-parameters are chosen on a separate validation set; the test set is scored once at the end | Choosing on the test set makes the test score optimistic, because the choice is tuned to that particular sample | §6 split, §8 selection, §9 single test evaluation | The test score is now an honest estimate. How optimistic the original 61% was cannot be measured exactly, because the original XGBoost was not re-run (`xgboost` was not available in the environment used here) |
| Visitors were described as negatively correlated with LOS (r ≈ -0.42), meaning "more visitors, shorter stay" | Corrected: r = +0.42, more visitors go with longer stays | Sign error in the interpretation of the heatmap | §4.4 | Changes the interpretation, not the models |
| The y-axis of the regression plots read "0=Long, 2=Short" | Encoding stated consistently as 0 = Short, 1 = Medium, 2 = Long | Mislabelled axis | §2 target definition | Presentation only |
| The notebook reads `Topic3_healthcare_analytics_dataset.csv`, but the file is named `... (1).csv`; dependencies are installed with `!pip` inside the notebook | Fixed paths relative to the project; dependencies in `requirements.txt` | The original notebook does not run as-is | `data/`, setup cell, `requirements.txt` | The revised notebook runs top to bottom. The original notebook is kept unchanged; its issues are listed in `original_course_project/README.md` |
| The reported XGBoost classification report shows 95,532 test rows (a 30% split), but the XGBoost code splits 25% | Every reported number is written to `results/` by the code that produced it | The reported table did not match the code next to it | `RESULTS` dictionary → `metrics.json`; docs are filled from it | Numbers in the README, report and notebook are consistent with one run |

### 2.2 Method improvements

| Original approach or issue | Change in the revised study | Why | How | Actual effect and limits |
|---|---|---|---|---|
| **Problem definition:** "predict LOS" without saying for whom or when | Predict at admission, for new patients; two planning uses defined | The evaluation design follows from the use case | §1 | Makes the task harder but closer to a real use |
| **Train/test split by admission**: the same patient could be in both sets | Split by `patientid` into training (60%), validation (20%) and test (20%); no patient crosses sets | Same-patient admissions are correlated (r = 0.32 vs 0.00), so overlap can inflate scores | §4.5 evidence, §6 `GroupShuffleSplit` and an assertion | With the original features the split barely changed the score (60.5% → 60.2%), probably because they hold little patient-identifying information. It should matter more for patient-level features; that was not tested separately |
| **`Visitors with Patient` used as a feature** (the strongest one) | Excluded from the main model; tested as a supplement | Its recording time is unknown; if it is counted during the stay, it partly reflects the outcome | §5, §9.4 | Main accuracy 54.1% without it vs 62.7% with it. Which number applies in practice depends on facts not in the data |
| **Hospital codes dropped** as "irrelevant IDs" | `Hospital_code` and the patient's city are used as categorical features | Hospitals differ strongly in LOS (Long share 8-35% across hospitals); a hospital code is a known property of the admission, not a patient ID | §4.2, §5 | `Hospital_code` is the most important feature of the final model |
| Mode imputation fitted on the full data before splitting | Missing `Bed Grade` filled with the **training** median inside the pipeline; missing patient city kept as its own category | Anything learned from data must be learned from training data only | §6 `make_tree_preprocessor` / `make_linear_preprocessor` | Negligible numerical effect (113 rows), but the procedure is now correct |
| The same encoding for every model (one-hot for nominal columns, integer codes for ordinal ones) | Trees get integer codes with native categorical splits (gradient boosting); logistic regression gets one-hot + standardisation | Each model gets the encoding it can use | §6 | Part of the "new pipeline" gain in Section 3 |
| OLS regression on class labels 0/1/2 as a baseline | Replaced by proper classification baselines: majority class, a lookup table and logistic regression | OLS on labels assumes equal, continuous distances between classes and its R² is not comparable with accuracy | §7 | The lookup table (50.6% / 38.4% macro-F1) is the benchmark a model has to beat |
| Model comparison: RF and XGBoost tuned differently (CV vs test set), on different splits | All models on the same split, target and features; selection by validation macro-F1; gradient boosting iterations by validation log-loss | A fair comparison needs equal conditions | §8 | Gradient boosting 48.5% vs random forest 47.0% vs logistic regression 42.1% macro-F1 on test |
| A fixed number of trees | Early stopping on validation log-loss | Too many iterations memorise the training data (validation loss rises again, §8 chart) | `fit_hgb_with_validation` | 67 iterations chosen for the final model |

### 2.3 New analyses

| Original approach or issue | Change in the revised study | Why | How | Actual effect and limits |
|---|---|---|---|---|
| Accuracy and a classification report only | Accuracy, balanced accuracy, macro-F1, log-loss, per-class precision/recall/F1, confusion matrix, ROC-AUC and average precision for P(Long) | Classes are imbalanced; planning needs probabilities and rankings | §9 | Shows that Short and Long recall are low (38%, 31%) even though the ranking of Long risk is informative (AUC 0.752) |
| No uncertainty around scores | 95% bootstrap intervals that resample **patients**; paired differences between models | To tell real differences from sampling noise | §9.1 | Final model vs random forest: +1.5 macro-F1 points (CI +1.1 to +1.8) |
| No check of the probabilities | Reliability diagram, Brier score and expected calibration error of P(Long) on the test set | Early stopping does not by itself prove that probabilities are calibrated | §10.4 | ECE 0.004: the probabilities match observed rates on this test set. No claim is made beyond it |
| Feature importance from the model's internal measure | Permutation importance on test data, plus coefficients of the interpretable logistic regression | Internal importances are biased towards features with many values; permutation importance measures the effect on the chosen metric | §10.1-10.2 | Top features: Hospital code (5.8 pp), Ward Type (4.1 pp), Admission Deposit (4.0 pp), City Code Patient (2.8 pp), Type of Admission (2.2 pp) |
| No error analysis | Accuracy and Long recall by severity, ward, admission type, age and department; where Long stays are misclassified | To see where the model fails | §10.3 | 56% of Long stays are predicted Medium; missed Long stays look like ordinary admissions |
| No supplementary experiments | Visitors and retrospective patient aggregates, each labeled with whether it is deployable | To quantify what the excluded information would add | §9.4 | Visitors +8.6 accuracy points; retrospective aggregates +1.0 |
| No link to decisions | Simulated bed-day demand of admission batches (with intervals checked on validation), a case-mix shift scenario, a proxy-day sensitivity analysis and long-stay screening at fixed review capacity | To test usefulness for planning, within what the data support | §11 | Batch MAPE 5.0% vs 5.2% for the best lookup table; flagging 20% captures 45.3% of Long stays vs 37.7%. These are simulations; no real schedule or outcome was tested |

### 2.4 Code organisation and readability

| Original approach or issue | Change in the revised study | Why | How | Actual effect and limits |
|---|---|---|---|---|
| One notebook with repeated imports, re-defined splits (`x_train` defined three times) and hard-coded best parameters copied from earlier output | One notebook in 12 sections, each explaining *why* and *how to read the output*; all key logic written in the cells | The analysis should be readable from top to bottom | `notebooks/LOS_study.ipynb` | Main reading entry of the project |
| No script entry point | `main.py` runs the same notebook cells as a script; `--quick` writes to a separate folder | One analysis logic, two ways to run it | `main.py` | A full run of `main.py` reproduced the notebook's `metrics.json` exactly (apart from run time) |
| Results only in the notebook | Every table and figure saved to `results/`; documents filled from `metrics.json` | Consistent numbers across README, report and notebook | `save_table`, `plotting.save_show`, `RESULTS` | – |
| Random seeds partly fixed | One seed (42) for every random step | Reproducibility | setup cell | Re-runs give identical numbers with the same library versions |

## 3. Controlled comparison: where does the difference to 61% come from?

The original random forest (its encoding and its tuned hyper-parameters, copied from the original notebook) was re-created and run under different conditions (§9.5):

| Setting | Split | Visitors | Accuracy | Macro-F1 |
|---|---|---|---|---|
| Original as reported (XGBoost, tuned on test) | random admissions | yes | 61% | 61% |
| C1: original RF, original conditions | random admissions 75/25 | yes | 60.5% | 59.1% |
| C2: original RF, this study's patient split | by patient | yes | 60.2% | 58.5% |
| C3: original RF, patient split, no Visitors | by patient | no | 52.4% | 42.5% |
| N1: new pipeline with Visitors | by patient | yes | 62.7% | 62.3% |
| N2: new pipeline, main model | by patient | no | 54.1% | 48.5% |

C2-C3 and N1-N2 use the same test patients. C1 has its own random test set.

* **Reproduction.** C1 lands at 60.5%, close to the reported 61%. The original result is reproduced in substance.
* **Split.** C1 → C2 changes accuracy by -0.3 points: small for these features.
* **Visitors.** C2 → C3 changes accuracy by -7.8 points. Most of the gap between 61% and the revised main result comes from removing Visitors, not from the split or the model.
* **New pipeline, same information.** With Visitors: N1 vs C2 = +2.5 accuracy points (+3.8 macro-F1). Without Visitors: N2 vs C3 = +1.7 accuracy points (+6.0 macro-F1). This is the measurable effect of the revised method itself (hospital codes, encoding, gradient boosting with early stopping).

## 4. Note on an earlier draft revision

An earlier draft of this revision (October 2026, not part of this repository) reported about 65% three-class accuracy. That draft:
* used aggregates over **all** admissions of a patient (number of admissions, mean visitors, mean severity, ...), which include future records because the data have no dates;
* built "history" features from the labels of the patient's other admissions under a **random admission split**, which is not possible for a truly new patient and mixes in future stays;
* kept `Visitors with Patient`;
* called its probabilities "calibrated" because of early stopping, without testing it, and called about 65% a ceiling of the dataset without evidence.

The revised study reverses all four: aggregates appear only as a labeled retrospective supplement, history features are dropped, Visitors is a supplement, and probability quality is tested directly. The lower headline number is the expected consequence of the stricter question.
