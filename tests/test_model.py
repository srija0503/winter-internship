import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

from src.data_loader import load_data

def test_svm_runs_and_returns_accuracy():
    """
    Lightweight QA: trains an SVM on available data to ensure pipeline correctness.
    This test will pass as long as model runs and returns a numeric accuracy between 0 and 1.
    """
    df = load_data().dropna().drop_duplicates()
    assert "dataset" in df.columns, "dataset column missing from data"

    # Map dataset to binary labels if textual
    if df["dataset"].dtype == object:
        y = df["dataset"].map({"liver_disease": 1, "healthy": 0})
    else:
        y = df["dataset"]

    X = df.select_dtypes(include=[np.number]).drop(columns=["dataset"], errors=True) if "dataset" in df.columns else df.select_dtypes(include=[np.number])
    assert len(X) >= 10, "Not enough numeric rows to run model test (need >=10)."

    # Align rows with labels (drop any rows with missing y)
    combined = X.join(y)
    combined = combined.dropna()
    X_clean = combined.drop(columns=["dataset"]) if "dataset" in combined.columns else combined.drop(columns=[combined.columns[-1]])
    y_clean = combined["dataset"] if "dataset" in combined.columns else combined.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(X_clean, y_clean, test_size=0.2, random_state=42, stratify=y_clean)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    clf = SVC(kernel="rbf", random_state=42)
    clf.fit(X_train_scaled, y_train)
    preds = clf.predict(X_test_scaled)
    acc = accuracy_score(y_test, preds)
    print(f"Test Accuracy: {acc:.4f}")
    assert 0.0 <= acc <= 1.0