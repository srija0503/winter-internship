"""
Simple orchestration script to:
- load data
- generate plots
"""
import sys
from pathlib import Path

# Ensure src is importable when running from scripts/
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from data_loader import load_data, print_schema
from data_visualization import generate_plots
from config import DATA_FILE, OUTPUT_DIR

def main():
    print("Loading data from:", DATA_FILE)
    df = load_data()
    print("Rows:", len(df))
    print_schema(df)

    # Generate plots
    generate_plots(output_dir=OUTPUT_DIR)
    print("Done. Plots are in:", OUTPUT_DIR)

if __name__ == "__main__":
    main()