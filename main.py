"""Batch entry point for the revised LOS study.

There is only one copy of the analysis: the notebook notebooks/LOS_study.ipynb.
This script runs every code cell of that notebook, in order, as plain Python,
so the script and the notebook can never drift apart. It needs no Jupyter.

    python main.py            # full run, writes results/ (about 10-15 minutes)
    python main.py --quick    # small test run on 25% of patients, writes results_quick/

The quick run uses the same code with smaller settings and never touches results/.
To refresh the outputs stored inside the notebook itself, open it in Jupyter and
choose "Restart kernel and run all", or run:
    jupyter nbconvert --to notebook --execute --inplace notebooks/LOS_study.ipynb
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOTEBOOK = ROOT / "notebooks" / "LOS_study.ipynb"


def display(*objects):
    """Stand-in for Jupyter's display(): print tables and values to the console."""
    for obj in objects:
        if hasattr(obj, "to_string"):
            print(obj.to_string(max_rows=40))
        else:
            print(obj)


def main():
    parser = argparse.ArgumentParser(description="Run the LOS study notebook as a script.")
    parser.add_argument("--quick", action="store_true", help="small test run, results go to results_quick/")
    args = parser.parse_args()

    # The notebook reads this variable to choose its settings and output folder.
    os.environ["LOS_QUICK"] = "1" if args.quick else "0"

    import matplotlib
    matplotlib.use("Agg")                    # draw figures to files only
    import matplotlib.pyplot as plt
    plt.show = lambda *a, **k: None          # figures are saved by the notebook code itself

    with open(NOTEBOOK, encoding="utf-8") as f:
        notebook = json.load(f)
    code_cells = ["".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code"]

    os.chdir(NOTEBOOK.parent)                # same working directory as in Jupyter
    namespace = {"__name__": "__main__", "display": display}
    start = time.time()
    for i, source in enumerate(code_cells, start=1):
        first_line = source.strip().split("\n")[0][:70]
        print("\n--- cell %d/%d: %s" % (i, len(code_cells), first_line), flush=True)
        exec(compile(source, "%s [code cell %d]" % (NOTEBOOK.name, i), "exec"), namespace)
    print("\nFinished %d cells in %.0f s." % (len(code_cells), time.time() - start))


if __name__ == "__main__":
    sys.exit(main())
