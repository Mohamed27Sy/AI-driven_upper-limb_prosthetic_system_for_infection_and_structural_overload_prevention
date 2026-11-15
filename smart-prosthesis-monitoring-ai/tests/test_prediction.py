import sys, os
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from prediction import build_model, split_features, predict_risk, FEATURE_COLUMNS


def _synthetic_features(n=200, seed=0):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "peak_load_kg": rng.uniform(0, 15, n),
        "avg_load_kg": rng.uniform(0, 8, n),
        "normal_crossings": rng.integers(0, 40, n),
        "high_risk_crossings": rng.integers(0, 5, n),
        "crossing_ratio": rng.uniform(0, 1, n),
        "repetition_frequency": rng.integers(0, 7, n),
    })
    df["risk_label"] = (
        (df["high_risk_crossings"] > 1) | (df["repetition_frequency"] > 4)
    ).astype(int)
    return df


def test_model_trains_and_predicts():
    features = _synthetic_features()
    X_train, X_test, y_train, y_test = split_features(features)
    model = build_model()
    model.fit(X_train, y_train)
    preds = predict_risk(model, X_test)
    assert len(preds) == len(y_test)
    assert set(np.unique(preds)).issubset({0, 1})
