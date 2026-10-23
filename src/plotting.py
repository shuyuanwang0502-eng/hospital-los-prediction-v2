"""Plotting helpers for the LOS study notebook.

This module only draws charts from numbers that the notebook has already
computed. It contains no data cleaning, splitting, training or evaluation
logic, so every analysis step stays visible in the notebook itself.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Folder where figures are saved; the notebook sets this at start-up.
FIG_DIR = Path("figures")

BLUE, ORANGE, AQUA, VIOLET = "#2a78d6", "#eb6834", "#1baf7a", "#6250d6"
GREY, INK, MUTED = "#b8b7b2", "#0b0b0b", "#52514e"
CLASS_COLORS = [BLUE, AQUA, ORANGE]          # Short, Medium, Long
CLASS_NAMES = ["Short (0-20 d)", "Medium (21-50 d)", "Long (>50 d)"]

plt.rcParams.update({
    "figure.dpi": 100, "savefig.dpi": 150, "savefig.bbox": "tight",
    "font.size": 10, "axes.titlesize": 11, "axes.titleweight": "bold",
    "axes.edgecolor": GREY, "axes.labelcolor": MUTED, "xtick.color": MUTED,
    "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#ecebe7", "grid.linewidth": 0.8,
    "axes.axisbelow": True, "legend.frameon": False,
})


def save_show(fig, name):
    """Save a figure to FIG_DIR/<name>.png, show it, then close it."""
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / (name + ".png"))
    plt.show()
    plt.close(fig)


def stay_distribution(bin_share, bin_labels, bin_class):
    """Bar chart of the 11 Stay bins, coloured by the 3-class grouping."""
    fig, ax = plt.subplots(figsize=(8.5, 3.6))
    colors = [CLASS_COLORS[c] for c in bin_class]
    ax.bar(range(len(bin_share)), np.asarray(bin_share) * 100, color=colors, width=0.75)
    ax.set_xticks(range(len(bin_share)))
    ax.set_xticklabels(bin_labels)
    ax.set_xlabel("Length of stay (days)")
    ax.set_ylabel("% of labeled admissions")
    ax.set_title("Distribution of the target")
    for k, name in enumerate(CLASS_NAMES):
        ax.bar(0, 0, color=CLASS_COLORS[k], label=name)
    ax.legend(loc="upper right")
    return fig


def long_share_panels(panels, overall_long_share):
    """One small bar chart per feature: share of Long stays in each category.

    panels: list of (title, labels, long_shares) tuples.
    """
    n = len(panels)
    cols = 3
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(12, 3.3 * rows))
    axes = np.atleast_1d(axes).ravel()
    for ax, (title, labels, shares) in zip(axes, panels):
        ax.bar(range(len(labels)), np.asarray(shares) * 100, color=BLUE, width=0.7)
        ax.axhline(overall_long_share * 100, color=MUTED, ls="--", lw=1)
        ax.set_xticks(range(len(labels)))
        rotate = len(labels) > 5 or max([len(str(l)) for l in labels] + [0]) > 8
        ax.set_xticklabels(labels, rotation=30 if rotate else 0,
                           ha="right" if rotate else "center", fontsize=8)
        ax.set_title(title)
        ax.set_ylabel("% Long (>50 d)")
    for ax in axes[n:]:
        ax.axis("off")
    fig.tight_layout()
    return fig


def line_by_value(x, y, title, xlabel, ylabel, note=None):
    """Simple line chart, e.g. mean stay by number of visitors."""
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.plot(x, y, color=BLUE, lw=2, marker="o", ms=5)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if note:
        ax.text(0.02, 0.95, note, transform=ax.transAxes, va="top", fontsize=8, color=MUTED)
    return fig


def model_scores(names, accuracy, macro_f1, title, err_acc=None, err_f1=None):
    """Grouped horizontal bars of accuracy and macro-F1 per model."""
    fig, ax = plt.subplots(figsize=(8, 0.65 * len(names) + 1.4))
    y = np.arange(len(names))[::-1]
    h = 0.38
    ax.barh(y + h / 2, np.asarray(accuracy) * 100, height=h, color=BLUE, label="Accuracy",
            xerr=None if err_acc is None else np.asarray(err_acc) * 100, ecolor=MUTED)
    ax.barh(y - h / 2, np.asarray(macro_f1) * 100, height=h, color=AQUA, label="Macro-F1",
            xerr=None if err_f1 is None else np.asarray(err_f1) * 100, ecolor=MUTED)
    for yi, a, f in zip(y, accuracy, macro_f1):
        ax.text(a * 100 + 0.6, yi + h / 2, "%.1f" % (a * 100), va="center", fontsize=8, color=INK)
        ax.text(f * 100 + 0.6, yi - h / 2, "%.1f" % (f * 100), va="center", fontsize=8, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels(names)
    ax.set_xlim(0, max(max(accuracy), max(macro_f1)) * 100 + 8)
    ax.set_xlabel("Score (%)")
    ax.set_title(title)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2)
    return fig


def validation_curves(curves, title):
    """Validation log-loss against number of boosting iterations.

    curves: dict label -> array of log-loss per iteration.
    """
    fig, ax = plt.subplots(figsize=(7, 3.8))
    colors = [BLUE, ORANGE, AQUA, VIOLET]
    for (label, losses), c in zip(curves.items(), colors):
        it = np.arange(1, len(losses) + 1)
        ax.plot(it, losses, color=c, lw=1.8, label=label)
        best = int(np.argmin(losses))
        ax.scatter([best + 1], [losses[best]], color=c, s=25, zorder=3)
    ax.set_xlabel("Boosting iterations")
    ax.set_ylabel("Validation log-loss")
    ax.set_title(title)
    ax.legend(fontsize=8)
    return fig


def confusion(cm_counts, title):
    """Row-normalised confusion matrix with counts in brackets."""
    cm = np.asarray(cm_counts, dtype=float)
    row = cm / cm.sum(axis=1, keepdims=True)
    fig, ax = plt.subplots(figsize=(5, 4.3))
    ax.imshow(row, cmap="Blues", vmin=0, vmax=1)
    ax.grid(False)
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, "%.0f%%\n(%d)" % (row[i, j] * 100, cm[i, j]), ha="center",
                    va="center", fontsize=9, color="white" if row[i, j] > 0.5 else INK)
    short = ["Short", "Medium", "Long"]
    ax.set_xticks(range(3)); ax.set_xticklabels(short)
    ax.set_yticks(range(3)); ax.set_yticklabels(short)
    ax.set_xlabel("Predicted class"); ax.set_ylabel("Actual class")
    ax.set_title(title)
    return fig


def horizontal_bars(labels, values, title, xlabel, errors=None, color=BLUE):
    """Sorted horizontal bar chart (e.g. permutation importance)."""
    order = np.argsort(values)
    fig, ax = plt.subplots(figsize=(7, 0.36 * len(labels) + 1.2))
    ax.barh(np.asarray(labels)[order], np.asarray(values)[order], color=color, height=0.65,
            xerr=None if errors is None else np.asarray(errors)[order], ecolor=MUTED)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    return fig


def reliability(mean_pred, observed, counts, title, label="Model"):
    """Reliability diagram: observed frequency against mean predicted probability."""
    fig, ax = plt.subplots(figsize=(4.8, 4.4))
    ax.plot([0, 1], [0, 1], color=GREY, ls="--", lw=1, label="Perfect calibration")
    ax.plot(mean_pred, observed, color=BLUE, lw=2, marker="o", ms=5, label=label)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xlabel("Mean predicted P(Long)")
    ax.set_ylabel("Observed share of Long stays")
    ax.set_title(title)
    ax.legend(loc="upper left", fontsize=8)
    return fig


def screening_curves(fractions, curves, title):
    """Share of long stays caught when flagging the top-x% riskiest admissions.

    curves: dict label -> recall values aligned with `fractions`.
    """
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    colors = [BLUE, ORANGE, AQUA]
    for (label, rec), c in zip(curves.items(), colors):
        ax.plot(np.asarray(fractions) * 100, np.asarray(rec) * 100, color=c, lw=2, label=label)
    ax.plot([0, 100], [0, 100], color=GREY, ls="--", lw=1, label="Random order")
    ax.set_xlabel("% of admissions flagged")
    ax.set_ylabel("% of all Long stays flagged (recall)")
    ax.set_title(title)
    ax.legend(loc="lower right", fontsize=8)
    return fig


def batch_errors(method_labels, scenario_values, scenario_labels, title):
    """Grouped bars: mean absolute % error of batch bed-day totals per method."""
    fig, ax = plt.subplots(figsize=(8, 0.75 * len(method_labels) + 1.4))
    y = np.arange(len(method_labels))[::-1]
    n = len(scenario_values)
    h = 0.8 / n
    colors = [GREY, BLUE, ORANGE]
    for k, (vals, lab) in enumerate(zip(scenario_values, scenario_labels)):
        off = (n - 1) / 2 * h - k * h
        ax.barh(y + off, np.asarray(vals) * 100, height=h, color=colors[k], label=lab)
        for yi, v in zip(y + off, vals):
            ax.text(v * 100 + 0.15, yi, "%.1f%%" % (v * 100), va="center", fontsize=8, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels(method_labels)
    ax.set_xlabel("Mean absolute % error of a batch's total proxy bed-days")
    ax.set_title(title)
    ax.legend(loc="lower right", fontsize=8)
    return fig


def batch_intervals(forecast, low, high, actual, title):
    """Forecast, 90% simulation interval and actual total for sample batches."""
    order = np.argsort(forecast)
    x = np.arange(len(order))
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.fill_between(x, np.asarray(low)[order], np.asarray(high)[order], color=BLUE, alpha=0.18,
                    lw=0, label="90% simulation interval")
    ax.plot(x, np.asarray(forecast)[order], color=BLUE, lw=2, label="Model forecast")
    ax.scatter(x, np.asarray(actual)[order], color=ORANGE, s=14, zorder=3, label="Actual (proxy)")
    ax.set_xticks([])
    ax.set_xlabel("Simulated admission batches (sorted by forecast)")
    ax.set_ylabel("Total proxy bed-days of the batch")
    ax.set_title(title)
    ax.legend(loc="upper left", fontsize=8)
    return fig
