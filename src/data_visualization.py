import os
import matplotlib.pyplot as plt
import seaborn as sns

from .data_loader import load_data
from .config import OUTPUT_DIR

def generate_plots(csv_path: str = None, output_dir: str = None, pairplot_vars: list = None) -> dict:
    """
    Generate correlation heatmap and pairplot.
    - csv_path: optional CSV path (overrides config)
    - output_dir: where to save images (defaults to config.OUTPUT_DIR)
    - pairplot_vars: list of numeric columns to include in pairplot (limits size)
    Returns dict with saved file paths.
    """
    output_dir = output_dir or OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    df = load_data(csv_path)
    numeric_df = df.select_dtypes(include=["float64", "int64"])

    # Heatmap
    print("Generating Heatmap...")
    plt.figure(figsize=(12, 10))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Feature Correlation Matrix")
    heatmap_path = os.path.join(output_dir, "correlation_heatmap.png")
    plt.tight_layout()
    plt.savefig(heatmap_path)
    plt.close()

    # Pairplot: limit variables to avoid extremely large plots
    print("Generating Pairplot...")
    if pairplot_vars is None:
        # Choose clinically relevant columns if available
        preferred = ["total_bilirubin", "direct_bilirubin", "alkaline_phosphotase",
                     "alamine_aminotransferase", "aspartate_aminotransferase", "albumin"]
        pairplot_vars = [c for c in preferred if c in numeric_df.columns]
        if not pairplot_vars:
            pairplot_vars = numeric_df.columns.tolist()[:6]  # fallback

    cols = list(pairplot_vars)
    if "dataset" in df.columns:
        cols = cols + ["dataset"]
    pairplot = sns.pairplot(df[cols], hue="dataset" if "dataset" in df.columns else None, palette="husl", diag_kind="kde")
    pairplot_path = os.path.join(output_dir, "pairplot_distribution.png")
    pairplot.savefig(pairplot_path)
    plt.close()

    print("Plots saved to:", output_dir)
    return {"heatmap": heatmap_path, "pairplot": pairplot_path}

if __name__ == "__main__":
    generate_plots()