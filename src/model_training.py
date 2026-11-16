"""
model_training.py – SafeHer
Complete ML pipeline: feature engineering, training, evaluation, persistence.

Target: binary risk_label (0 = lower risk, 1 = higher risk).
Models: Logistic Regression, Decision Tree, Random Forest.
All output is clearly labelled as relative / indicative risk.
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from typing import Optional, Tuple, Dict

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report,
)
from sklearn.pipeline import Pipeline

MODELS_DIR = Path(__file__).parent.parent / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH   = MODELS_DIR / "safeher_risk_model.joblib"
ENCODER_PATH = MODELS_DIR / "label_encoders.joblib"

FEATURE_COLS = [
    "hour", "severity", "lighting_enc", "transport_enc",
    "category_enc", "day_of_week_enc",
]

CATEGORICAL_FEATURE_MAP = {
    "lighting_enc":      "lighting",
    "transport_enc":     "transport_mode",
    "category_enc":      "category",
    "day_of_week_enc":   "day_of_week",
}


def engineer_features(df: pd.DataFrame, encoders: Optional[Dict] = None, fit: bool = True):
    """
    Encode categoricals and return (feature_df, updated_encoders).
    If fit=True, a new encoder is fitted; otherwise the supplied encoder is reused.
    """
    df = df.copy()
    encoders = encoders or {}

    for enc_col, src_col in CATEGORICAL_FEATURE_MAP.items():
        if src_col not in df.columns:
            df[enc_col] = 0
            continue
        if fit or enc_col not in encoders:
            le = LabelEncoder()
            df[enc_col] = le.fit_transform(df[src_col].astype(str))
            encoders[enc_col] = le
        else:
            le = encoders[enc_col]
            # Handle unseen labels gracefully
            known = set(le.classes_)
            df[enc_col] = df[src_col].astype(str).apply(
                lambda x: le.transform([x])[0] if x in known else -1
            )

    for c in FEATURE_COLS:
        if c not in df.columns:
            df[c] = 0

    return df[FEATURE_COLS], encoders


def get_available_models() -> Dict[str, object]:
    return {
        "Logistic Regression": Pipeline([
            ("scaler", StandardScaler()),
            ("clf",    LogisticRegression(max_iter=500, random_state=42)),
        ]),
        "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=42),
        "Random Forest":  RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42, n_jobs=1),
    }


def train_all_models(df: pd.DataFrame) -> dict:
    """
    Train all baseline models and return a structured results dict.
    Returns {} if data is insufficient.
    """
    if df.empty or "risk_label" not in df.columns:
        return {}

    # A stratified hold-out split and 5-fold CV need enough samples per class.
    work = df.copy()
    work["risk_label"] = pd.to_numeric(work["risk_label"], errors="coerce")
    work = work.dropna(subset=["risk_label"])
    if len(work) < 100 or not set(work["risk_label"].unique()).issubset({0, 1}):
        return {}
    class_counts = work["risk_label"].value_counts()
    if len(class_counts) != 2 or int(class_counts.min()) < 5:
        return {}

    X, encoders = engineer_features(work, fit=True)
    y = work["risk_label"].astype(int).values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    results  = {}
    best_f1  = -1
    best_name = None
    best_model = None

    for name, model in get_available_models().items():
        model.fit(X_train, y_train)
        y_pred   = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision= precision_score(y_test, y_pred, zero_division=0)
        recall   = recall_score(y_test, y_pred, zero_division=0)
        f1       = f1_score(y_test, y_pred, zero_division=0)
        cm       = confusion_matrix(y_test, y_pred)
        report   = classification_report(y_test, y_pred, output_dict=True)
        cv_f1    = cross_val_score(model, X, y, cv=5, scoring="f1", n_jobs=1).mean()

        # Feature importance
        fi = _get_feature_importance(model, X.columns.tolist())

        results[name] = {
            "model":       model,
            "accuracy":    accuracy,
            "precision":   precision,
            "recall":      recall,
            "f1":          f1,
            "cv_f1":       cv_f1,
            "cm":          cm,
            "report":      report,
            "feature_importance": fi,
            "feature_names": X.columns.tolist(),
        }
        if f1 > best_f1:
            best_f1   = f1
            best_name = name
            best_model = model

    # Persist best model
    if best_model:
        joblib.dump(best_model, MODEL_PATH)
        joblib.dump(encoders,   ENCODER_PATH)

    results["_meta"] = {
        "best_model":    best_name,
        "encoders":      encoders,
        "feature_names": X.columns.tolist(),
        "train_size":    len(X_train),
        "test_size":     len(X_test),
    }
    return results


def _get_feature_importance(model, feature_names: list) -> np.ndarray:
    """Extract feature importances regardless of model type."""
    # For Pipeline objects, inspect the last step
    clf = model.steps[-1][1] if hasattr(model, "steps") else model
    if hasattr(clf, "feature_importances_"):
        return clf.feature_importances_
    if hasattr(clf, "coef_"):
        return np.abs(clf.coef_[0])
    return np.ones(len(feature_names)) / len(feature_names)


def load_saved_model():
    """Load the persisted best model and encoders, or return None."""
    if MODEL_PATH.exists() and ENCODER_PATH.exists():
        return joblib.load(MODEL_PATH), joblib.load(ENCODER_PATH)
    return None, None


def predict_risk(input_dict: dict) -> Optional[int]:
    """
    Predict risk for a single input dict.  Returns 0/1 or None on failure.
    """
    model, encoders = load_saved_model()
    if model is None:
        return None

    row_df = pd.DataFrame([input_dict])

    # Derive needed columns from raw inputs
    if "hour" in row_df.columns:
        h = row_df["hour"].iloc[0]
        row_df["time_of_day"] = (
            "Night" if h < 6 else "Morning" if h < 12 else "Afternoon" if h < 17 else "Evening" if h < 20 else "Night"
        )
        row_df["day_of_week"] = pd.Timestamp.now().day_name()  # demo: use current day

    X, _ = engineer_features(row_df, encoders=encoders, fit=False)
    try:
        return int(model.predict(X)[0])
    except Exception:
        return None


def get_model_metrics_summary(results: dict) -> pd.DataFrame:
    """Return a tidy DataFrame of metrics for all models (for display)."""
    rows = []
    for name, res in results.items():
        if name == "_meta":
            continue
        rows.append({
            "Model":     name,
            "Accuracy":  round(res["accuracy"],  4),
            "Precision": round(res["precision"], 4),
            "Recall":    round(res["recall"],    4),
            "F1 Score":  round(res["f1"],        4),
            "CV F1":     round(res["cv_f1"],     4),
        })
    return pd.DataFrame(rows)
