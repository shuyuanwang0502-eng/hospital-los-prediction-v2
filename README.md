# Hospital Length-of-Stay Prediction

**From a university group project to a revised, leakage-aware study with planning simulations.**

Can we tell at admission whether a new patient will stay Short (0-20 days), Medium (21-50) or Long (more than 50), and is that useful for hospital bed planning? This repository holds both the original TUM course project and a revised study that answers the question with a stricter, more honest design.

| Start here | |
|---|---|
| **Revised study: main notebook** (code + explanations + outputs) | [`notebooks/LOS_study.ipynb`](notebooks/LOS_study.ipynb) |
| Final report of the revised study | [`FINAL_REPORT.md`](FINAL_REPORT.md) |
| What changed from the original, and why | [`PROJECT_EVOLUTION.md`](PROJECT_EVOLUTION.md) |
| Original group project (unchanged) | [`original_course_project/`](original_course_project/) |
| 中文阅读指南 (Chinese reading guide) | [`READING_GUIDE_zh.md`](READING_GUIDE_zh.md) |
| Installation and running | [below](#install-and-run) |

## Authorship

* **Original course project** (TUM *Programming*, summer semester 2025): Group 2, Shuyuan Wang, Luoze Guo, Beibei Le, Ping-Jui Chen, Chia-Chen Li. Preserved unchanged in `original_course_project/`.
* **Revised study** (everything else in this repository): individual follow-up work by **Shuyuan Wang**, built on the group project. The other group members are credited for the original project, not for the revised analysis.

## The revised study in one minute

**Design.** 318,438 labeled admissions of 92,017 patients at 32 hospitals, split **by patient** into training (60%), validation (20%) and test (20%) sets. Only fields plausibly available at admission are used. `Visitors with Patient`, whose recording time is unknown, and patient aggregates over other (possibly future) admissions are tested separately, not used in the main model. Models are chosen on the validation set; the test set is used once.

**Results on unseen test patients**

| Model | Accuracy | Macro-F1 | ROC-AUC for "Long stay" |
|---|---|---|---|
| Always predict "Medium" | 48.7% | 21.8% | – |
| Lookup table (hospital × ward × severity) | 50.6% | 38.4% | 0.683 |
| Logistic regression | 51.6% | 42.1% | 0.708 |
| Random forest | 53.5% | 47.0% | 0.742 |
| **Gradient boosting (selected)** | **54.1%** | **48.5%** | **0.752** |
| *Supplement: gradient boosting + Visitors* | *62.7%* | *62.3%* | *0.893* |

![Test results](results/figures/05_test_model_comparison.png)

**What it means**
* Admission data predict individual LOS only modestly better than a simple lookup table. The model's clearest value is **ranking risk**: flagging the 20% riskiest admissions captures 45.3% of all Long stays, against 37.7% for the lookup table and 20% for a random choice.
* For simulated batches of 100 admissions, total proxy bed-days are forecast with 5.0% error (best lookup table 5.2%), and the model's 90% range contained the actual total in 91.1% of test batches. These are simulations: the data have no dates, so daily occupancy was not modelled.
* `Visitors with Patient` would add 8.6 accuracy points **if** it is known at admission. That has to be confirmed with the data owner.

**Relation to the original 61%.** The course project reported 61% accuracy, with Visitors as a feature, a random split of admissions and XGBoost tuned on the test set. Re-creating its random forest gives 60.5%, so the original result is reproduced. With the same information (Visitors included) and a patient split, the revised pipeline reaches 62.7%, against 60.2% for the original approach. The main result of 54.1% answers a stricter question, so it is not a like-for-like comparison. See [`PROJECT_EVOLUTION.md`](PROJECT_EVOLUTION.md#3-controlled-comparison-where-does-the-difference-to-61-come-from).

## Repository structure

```
├── README.md                    you are here
├── READING_GUIDE_zh.md          Chinese reading guide
├── PROJECT_EVOLUTION.md         original vs revised: every change, why, and its effect
├── FINAL_REPORT.md              report of the revised study
├── notebooks/
│   └── LOS_study.ipynb          MAIN ENTRY: the full revised analysis, with saved outputs
├── main.py                      runs the same notebook cells as a script (no Jupyter needed)
├── src/
│   └── plotting.py              chart helpers only (no analysis logic)
├── results/                     output of the official full run
│   ├── metrics.json             every reported number
│   ├── tables/                  result tables (CSV)
│   └── figures/                 all figures (PNG)
├── data/
│   ├── healthcare_analytics.csv the course dataset
│   └── README.md                field dictionary and availability assumptions
├── original_course_project/     the group submission, unchanged
│   ├── Final Project_25 Rick Edition.ipynb
│   ├── Presentation_python.pdf
│   └── README.md                what it did, its reported results and known issues
└── requirements.txt
```

## Install and run

Python 3.8 or newer.

```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Read and re-run the notebook:** `jupyter lab notebooks/LOS_study.ipynb`, then *Run → Restart Kernel and Run All Cells*. A full run took 8.8 minutes on a 2-core machine.

**Run as a script:**

```bash
python main.py            # full run, rewrites results/
python main.py --quick    # 25% of patients and smaller settings, writes results_quick/ (ignored by git)
```

`main.py` executes the code cells of the notebook in order, so the script and the notebook always use the same method and settings. The quick mode is for checking that everything runs; its numbers are not the official results.

**PyCharm:** open the project folder, set the interpreter to the `.venv` above (*Settings → Project → Python Interpreter*), then run `main.py`, or open the notebook in PyCharm's Jupyter view.

## Reproducibility notes

* One random seed (42) for every random step. Re-running with the same library versions gives identical numbers; a full `main.py` run reproduced the notebook's `metrics.json` exactly (apart from run time).
* The saved outputs were produced with Python 3.13.17, pandas 3.0.5, scikit-learn 1.9.1, numpy 2.5.3, matplotlib 3.11.2. The code avoids newer-only features so that it also runs with Python 3.8, pandas 2.0 and scikit-learn 1.3, but it was not executed with those versions. Small numerical differences between scikit-learn versions are possible.
* The notebook outputs were generated by executing all code cells in order in a fresh Python process.

## Data

The course dataset `Topic3_healthcare_analytics_dataset`, the same data as the public *AV Healthcare Analytics II* dataset. See [`data/README.md`](data/README.md) for the field dictionary and the assumptions about which fields are known at admission.
