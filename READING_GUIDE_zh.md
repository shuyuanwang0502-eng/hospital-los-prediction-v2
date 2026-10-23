# 中文阅读指南

这个仓库里有两个版本的项目：

* **原版**：TUM《Programming》课程的小组作业（Group 2，五人）。原封不动地放在 `original_course_project/` 里。
* **新版**：Shuyuan Wang 在课程项目基础上做的后续个人改进。仓库里除原版之外的其他内容都属于新版。

仓库正文、代码注释和报告都以英文为主，这份指南用中文说明每个文件是干什么的、按什么顺序看，以及怎么运行。

## 推荐阅读顺序

| 顺序 | 文件 | 看什么 | 大约时间 |
|---|---|---|---|
| 1 | `README.md` | 项目概览、最重要的结果，以及所有文件的入口 | 3 分钟 |
| 2 | `original_course_project/README.md` | 原版做了什么、当时报告的结果、已知问题 | 5 分钟 |
| 3 | `PROJECT_EVOLUTION.md` | 新旧版本的每一处变化：原来怎么做、改成什么、为什么改、怎么实现、实际影响 | 10 分钟 |
| 4 | `notebooks/LOS_study.ipynb` | **新版主体**：12 个部分，代码、讲解和运行输出都在里面 | 40-60 分钟 |
| 5 | `FINAL_REPORT.md` | 新版的正式报告：执行摘要、方法、结果、业务启示、局限 | 15 分钟 |

如果只有 10 分钟：看 README，再看 FINAL_REPORT 的 Executive summary，然后看 notebook 第 12 部分。

## 每个文件和文件夹的用途

| 路径 | 用途 |
|---|---|
| `notebooks/LOS_study.ipynb` | 新版的全部分析。数据清洗、划分、预处理、训练、预测、评估和模拟的代码都直接写在 cell 里，每一部分都写了“为什么这样做”和“输出怎么看” |
| `main.py` | 脚本入口：按顺序执行 notebook 里所有的代码 cell，所以脚本和 notebook 永远是同一套逻辑。不需要 Jupyter |
| `src/plotting.py` | 只负责画图（颜色、样式、几个图表函数），不包含任何分析逻辑 |
| `results/metrics.json` | 正式运行得到的全部数字。README、报告和 notebook 里引用的数字都来自这里 |
| `results/tables/` | 各种结果表（CSV），例如验证集结果、测试集结果、混淆矩阵对应的分类指标、运营模拟结果 |
| `results/figures/` | 所有图（PNG） |
| `data/healthcare_analytics.csv` | 课程数据集（原文件名为 `Topic3_healthcare_analytics_dataset (1).csv`，内容完全相同） |
| `data/README.md` | 字段说明，以及“入院时能不能拿到”的假设 |
| `original_course_project/` | 原版 notebook 和 PPT，逐字节原样复制，没有改动 |
| `PROJECT_EVOLUTION.md` | 改进说明，按“修复错误 / 方法改进 / 新增分析 / 代码组织”分类 |
| `FINAL_REPORT.md` | 新版最终报告 |
| `requirements.txt` | 依赖包 |
| `results_quick/` | 快速模式的输出，只用来检查能不能跑通，不是正式结果，也不进 git |

## 怎么运行

### 在 PyCharm 里

1. 用 PyCharm 打开 `hospital-los-prediction-v2` 这个文件夹。
2. 设置解释器。右下角如果显示 `<No interpreter>`，就是还没设置：
   * 点右下角，选 *Add New Interpreter → Add Local Interpreter*。
   * **最省事的做法**：选 *Select existing*，路径填你之前那个文件夹里已经装好依赖的环境：`.../final project/hospital-los-prediction/.venv/bin/python`。这个环境是 Python 3.8，里面已经有 pandas、scikit-learn、matplotlib 和 jupyter，可以直接用。
   * 或者新建一个环境：选 *Virtualenv → New*，建好后在 PyCharm 底部的 Terminal 里运行 `pip install -r requirements.txt`。
3. 运行方式二选一：
   * **看 notebook**：双击 `notebooks/LOS_study.ipynb`，用 PyCharm 的 Jupyter 视图打开，点 *Run All*。也可以在 Terminal 里运行 `jupyter lab`，在浏览器里打开。
   * **跑脚本**：右键 `main.py` → *Run*。完整运行大约 10 分钟。
4. 想先确认能不能跑通：在 Terminal 里运行 `python main.py --quick`，大约 1 分钟。结果会写到 `results_quick/`，不会覆盖正式结果。

### 在命令行里

```bash
cd "hospital-los-prediction-v2"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py --quick      # 快速检查
python main.py              # 正式完整运行
```

## 新版的关键结果（中文摘要）

* **研究问题**：只用入院时能拿到的信息，预测一个**从没见过的病人**会住短期（0-20 天）、中期（21-50 天）还是长期（50 天以上）；并检验这对床位规划有没有用。
* **设计**：按病人 ID 分成训练集（60%）、验证集（20%）和测试集（20%），同一个病人只会出现在一个集合里。模型和参数只用验证集来选，测试集只在最后用一次。“探视人数”的记录时点不明，所以不进主模型；跨住院记录的病人聚合特征会混入未来信息，也不进主模型。两者都单独做了补充实验。
* **结果**：梯度提升模型在测试集上的准确率是 **54.1%**，macro-F1 是 **48.5%**。查表法（医院 × 病房 × 严重程度）分别是 50.6% 和 38.4%，全部猜“中期”的准确率是 48.7%。提升是真实的，但幅度有限。
* **长住院识别**：ROC-AUC 是 0.752。入院时标记风险最高的 20% 病人，可以覆盖 45.3% 的长住院病例（查表法 37.7%，随机标记 20%）。这只说明“能识别出来”，不代表已经证实能缩短住院或节省成本。
* **床位日需求（模拟）**：对“模拟入院批次”（每批 100 次入院，不等于一周）的累计床位日，模型误差 5.0%，查表法 5.2%；模型的 90% 区间覆盖了 91.1% 的测试批次。床位日用住院区间中点作为代理值，敏感性分析显示结论在不同假设下都不变。
* **探视人数**：如果入院时就能拿到，准确率会升到 62.7%。

## 常见问题

**为什么新版的准确率（54.1%）比原版的 61% 低？是不是做差了？**
不是。原版的 61% 是在更宽松的条件下得到的：用了记录时点不明的“探视人数”、随机划分入院记录、并且在测试集上调参。新版里有一组受控对比（notebook 第 9.5 节，PROJECT_EVOLUTION 第 3 节）：
* 按原版条件重建原版的随机森林，得到 60.5%，基本复现了 61%。
* 在相同信息（都包含探视人数）、相同的按病人划分下，新版方法 62.7%，原版方法 60.2%，新方法更好。
* 差距主要来自去掉“探视人数”，不是来自模型变差。

**快速模式和完整模式有什么区别？**
方法完全一样，只是快速模式只用 25% 的病人，迭代次数和树也更少，用来检查能不能跑通。正式结果只看 `results/`。

**原版 notebook 能运行吗？**
按原样不能：它读取的文件名和实际文件不一样，还需要额外安装 statsmodels、seaborn、xgboost、optuna。具体说明见 `original_course_project/README.md`。为了保留原貌，原版文件没有做任何修改。

**这些数字在哪里能核对？**
全部在 `results/metrics.json` 和 `results/tables/` 里，notebook 里每一步的输出也都保存着。
