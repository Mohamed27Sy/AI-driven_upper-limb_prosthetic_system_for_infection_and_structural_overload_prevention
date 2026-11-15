"""
prediction.py
==============
The predictive AI component described in ../docs/ai_workflow.md. Classifies a
patient-window's features (see feature_extraction.py) as Safe (0) or Risk (1).

Implementation note: the thesis does not name a specific model architecture, so
this uses a standard, well-understood classifier (scikit-learn's
RandomForestClassifier) rather than inventing an architecture the original work
never specified. Swap `build_model()` for a different estimator if you know what
the original implementation used.
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

FEATURE_COLUMNS = [
    "peak_load_kg",
    "avg_load_kg",
    "normal_crossings",
    "high_risk_crossings",
    "crossing_ratio",
    "repetition_frequency",
]


def build_model(random_state: int = 42) -> RandomForestClassifier:
    return RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        class_weight="balanced",
        random_state=random_state,
    )


def split_features(features: pd.DataFrame, label_col: str = "risk_label",
                    test_size: float = 0.2, random_state: int = 42):
    X = features[FEATURE_COLUMNS]
    y = features[label_col]
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)


def predict_risk(model: RandomForestClassifier, features: pd.DataFrame) -> np.ndarray:
    return model.predict(features[FEATURE_COLUMNS])
