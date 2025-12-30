import os

# Data and output paths can be overridden with environment variables
REPO_ROOT = os.path.dirname(os.path.dirname(__file__)) if "__file__" in globals() else os.getcwd()
DATA_DIR = os.getenv("DATA_DIR", os.path.join(REPO_ROOT, "data"))
DATA_FILE = os.getenv("DATA_FILE", os.path.join(DATA_DIR, "indian_liver_patient.csv"))
OUTPUT_DIR = os.getenv("OUTPUT_DIR", os.path.join(REPO_ROOT, "outputs"))

# Database config
DB_PATH = os.getenv("DB_PATH", os.path.join(REPO_ROOT, "db", "app.db"))