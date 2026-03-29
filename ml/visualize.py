"""
visualize.py — Data exploration and model visualization for Tirana Real Estate.

Reads the preprocessed listing data and produces a set of charts saved to
ml/figures/. Run this AFTER training (price_estimator.pkl must exist).

Usage (from the repo root, in WSL):
    python ml/visualize.py

Output directory:
    ml/figures/
        01_price_distribution.png
        02_sqm_vs_price.png
        03_bedrooms_distribution.png
        04_bathrooms_distribution.png
        05_furnishing_status.png
        06_correlation_heatmap.png
        07_feature_importance.png
        08_predicted_vs_actual.png
"""

import os
import sys
import logging
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")   # Non-interactive backend (safe for WSL / headless)
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH  = os.path.join(REPO_ROOT, "data", "tirana_house_prices.json")
MODEL_PATH = os.path.join(REPO_ROOT, "models", "price_estimator.pkl")
FIG_DIR    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")

sys.path.insert(0, os.path.join(REPO_ROOT, "backend"))
from preprocessing import load_and_preprocess  # noqa: E402

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
BLUE   = "#2563EB"
GREEN  = "#10B981"
ORANGE = "#F97316"
GRAY   = "#6B7280"
BG     = "#F9FAFB"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor":   BG,
    "axes.edgecolor":   "#E5E7EB",
    "axes.grid":        True,
    "grid.color":       "#E5E7EB",
    "grid.linestyle":   "--",
    "grid.alpha":       0.7,
    "font.family":      "DejaVu Sans",
    "font.size":        11,
    "axes.titlesize":   13,
    "axes.titleweight": "bold",
    "axes.labelsize":   11,
})


def save(fig, filename: str):
    path = os.path.join(FIG_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved → %s", path)


# ---------------------------------------------------------------------------
# Individual chart functions
# ---------------------------------------------------------------------------

def plot_price_distribution(df: pd.DataFrame):
    """Histogram of listing prices (ML-clean dataset)."""
    fig, ax = plt.subplots(figsize=(9, 5))
    prices = df["price_in_euro"].dropna()
    ax.hist(prices, bins=60, color=BLUE, edgecolor="white", linewidth=0.4)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{x:,.0f}"))
    ax.set_xlabel("Price (€)")
    ax.set_ylabel("Number of listings")
    ax.set_title("01 · Price Distribution (after outlier removal)")
    median_val = prices.median()
    ax.axvline(median_val, color=ORANGE, linestyle="--", linewidth=1.5,
               label=f"Median €{median_val:,.0f}")
    ax.legend()
    save(fig, "01_price_distribution.png")


def plot_sqm_vs_price(df: pd.DataFrame):
    """Scatter plot: square meters vs price."""
    fig, ax = plt.subplots(figsize=(9, 5))
    sub = df[["square_meters", "price_in_euro"]].dropna()
    ax.scatter(sub["square_meters"], sub["price_in_euro"],
               alpha=0.35, s=18, color=BLUE, edgecolors="none")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f} m²"))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{x:,.0f}"))
    ax.set_xlabel("Square Meters")
    ax.set_ylabel("Price (€)")
    ax.set_title("02 · Square Meters vs. Price")
    save(fig, "02_sqm_vs_price.png")


def plot_bedrooms_distribution(df: pd.DataFrame):
    """Bar chart of bedrooms count."""
    fig, ax = plt.subplots(figsize=(8, 5))
    counts = df["bedrooms"].dropna().astype(int).value_counts().sort_index()
    bars = ax.bar(counts.index.astype(str), counts.values, color=BLUE, edgecolor="white")
    ax.bar_label(bars, fmt="%d", padding=3, color=GRAY)
    ax.set_xlabel("Number of Bedrooms")
    ax.set_ylabel("Number of Listings")
    ax.set_title("03 · Bedroom Count Distribution")
    save(fig, "03_bedrooms_distribution.png")


def plot_bathrooms_distribution(df: pd.DataFrame):
    """Bar chart of bathrooms count."""
    fig, ax = plt.subplots(figsize=(8, 5))
    counts = df["bathrooms"].dropna().astype(int).value_counts().sort_index()
    bars = ax.bar(counts.index.astype(str), counts.values, color=GREEN, edgecolor="white")
    ax.bar_label(bars, fmt="%d", padding=3, color=GRAY)
    ax.set_xlabel("Number of Bathrooms")
    ax.set_ylabel("Number of Listings")
    ax.set_title("04 · Bathroom Count Distribution")
    save(fig, "04_bathrooms_distribution.png")


def plot_furnishing_status(df: pd.DataFrame):
    """Horizontal bar chart of furnishing status."""
    fig, ax = plt.subplots(figsize=(8, 5))
    counts = df["furnishing_status"].fillna("unknown").value_counts()
    bars = ax.barh(counts.index.tolist(), counts.values, color=ORANGE, edgecolor="white")
    ax.bar_label(bars, fmt="%d", padding=3, color=GRAY)
    ax.set_xlabel("Number of Listings")
    ax.set_title("05 · Furnishing Status Distribution")
    ax.invert_yaxis()
    save(fig, "05_furnishing_status.png")


def plot_correlation_heatmap(df: pd.DataFrame):
    """Correlation heatmap for key numeric features."""
    cols = ["price_in_euro", "square_meters", "bedrooms", "bathrooms", "floor"]
    sub = df[cols].dropna()
    corr = sub.corr()

    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(
        corr,
        annot=True, fmt=".2f", linewidths=0.5,
        cmap="Blues", vmin=-1, vmax=1,
        ax=ax, square=True,
        cbar_kws={"shrink": 0.8},
    )
    ax.set_title("06 · Feature Correlation Heatmap")
    save(fig, "06_correlation_heatmap.png")


def plot_feature_importance(bundle: dict):
    """Horizontal bar chart of Random Forest feature importances."""
    model    = bundle["model"]
    features = bundle["features"]
    importances = model.feature_importances_
    order = np.argsort(importances)

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(
        [features[i] for i in order],
        importances[order],
        color=BLUE, edgecolor="white",
    )
    ax.bar_label(bars, fmt="%.3f", padding=3, color=GRAY)
    ax.set_xlabel("Importance")
    ax.set_title("07 · Feature Importances (Random Forest)")
    save(fig, "07_feature_importance.png")


def plot_predicted_vs_actual(bundle: dict, df: pd.DataFrame):
    """Scatter: predicted vs actual price on the full ML dataset."""
    import joblib
    from sklearn.preprocessing import LabelEncoder

    model   = bundle["model"]
    encoder = bundle["encoder"]

    NUMERIC_FEATURES    = ["square_meters", "bedrooms", "bathrooms", "floor"]
    BOOLEAN_FEATURES    = ["has_elevator", "has_terrace"]
    CATEGORICAL_FEATURE = "furnishing_status"

    rows, prices = [], []
    for _, row in df.iterrows():
        if row.get("price_in_euro") is None or any(pd.isna(row.get(f)) for f in NUMERIC_FEATURES):
            continue
        r = [float(row.get(f) or 0) for f in NUMERIC_FEATURES]
        r += [float(bool(row.get(f))) for f in BOOLEAN_FEATURES]
        furn = row.get(CATEGORICAL_FEATURE) or "unknown"
        furn_enc = encoder.transform([furn])[0] if furn in encoder.classes_ else -1
        r.append(float(furn_enc))
        rows.append(r)
        prices.append(float(row["price_in_euro"]))

    if not rows:
        logger.warning("No rows to plot for predicted vs actual.")
        return

    X = np.array(rows, dtype=float)
    y = np.array(prices, dtype=float)
    y_pred = model.predict(X)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(y, y_pred, alpha=0.30, s=15, color=BLUE, edgecolors="none")
    lim_min = min(y.min(), y_pred.min()) * 0.95
    lim_max = max(y.max(), y_pred.max()) * 1.05
    ax.plot([lim_min, lim_max], [lim_min, lim_max], color=ORANGE,
            linewidth=1.5, linestyle="--", label="Perfect prediction")
    ax.set_xlabel("Actual Price (€)")
    ax.set_ylabel("Predicted Price (€)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{x:,.0f}"))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{x:,.0f}"))
    ax.set_title("08 · Predicted vs. Actual Price")
    ax.legend()
    save(fig, "08_predicted_vs_actual.png")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    logger.info("=== Phase 3: Data Visualization ===")
    os.makedirs(FIG_DIR, exist_ok=True)
    logger.info("Output directory: %s", FIG_DIR)

    # Load data
    display_data, ml_data = load_and_preprocess(DATA_PATH)
    df_display = pd.DataFrame(display_data)
    df_ml      = pd.DataFrame(ml_data)
    logger.info("Display dataset: %d records | ML dataset: %d records",
                len(df_display), len(df_ml))

    # Charts that use the ML (outlier-filtered) dataset
    plot_price_distribution(df_ml)
    plot_sqm_vs_price(df_ml)
    plot_bedrooms_distribution(df_ml)
    plot_bathrooms_distribution(df_ml)
    plot_furnishing_status(df_ml)
    plot_correlation_heatmap(df_ml)

    # Charts that require the trained model
    if os.path.exists(MODEL_PATH):
        import joblib
        bundle = joblib.load(MODEL_PATH)
        plot_feature_importance(bundle)
        plot_predicted_vs_actual(bundle, df_ml)
    else:
        logger.warning(
            "Model not found at %s — skipping feature importance and "
            "predicted-vs-actual charts. Run `python ml/train_model.py` first.",
            MODEL_PATH,
        )

    logger.info("All figures saved to %s", FIG_DIR)


if __name__ == "__main__":
    main()
