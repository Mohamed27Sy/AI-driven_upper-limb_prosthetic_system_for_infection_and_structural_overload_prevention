"""
feature_extraction.py
======================
Builds the per-window features the predictive AI model (prediction.py) is trained
on, matching the feature list described in ../docs/ai_workflow.md /
../ai/03_feature_engineering.ipynb:
  peak load, average load, duration, threshold crossings, time-of-day,
  location, repetition frequency, previous risk events.
"""
import pandas as pd
import numpy as np


def extract_window_features(interval_df: pd.DataFrame, window: str = "1D",
                             normal_limit_kg: float = 8.0,
                             high_risk_limit_kg: float = 12.0) -> pd.DataFrame:
    """`interval_df` must have columns: timestamp, max_load_kg, unit_location.
    Returns one row of features per time window (default: per day).
    """
    df = interval_df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")

    grouped = df.groupby(pd.Grouper(freq=window))
    features = grouped.agg(
        peak_load_kg=("max_load_kg", "max"),
        avg_load_kg=("max_load_kg", "mean"),
        n_intervals=("max_load_kg", "count"),
    )
    features["normal_crossings"] = grouped["max_load_kg"].apply(
        lambda s: (s >= normal_limit_kg).sum()
    )
    features["high_risk_crossings"] = grouped["max_load_kg"].apply(
        lambda s: (s >= high_risk_limit_kg).sum()
    )
    features["crossing_ratio"] = (
        features["normal_crossings"] / features["n_intervals"].replace(0, np.nan)
    ).fillna(0)
    features["dominant_location"] = grouped.apply(
        lambda g: g["unit_location"].mode().iloc[0] if not g.empty else np.nan
    )
    return features.dropna(subset=["peak_load_kg"]).reset_index()


def add_repetition_frequency(features: pd.DataFrame, location_col: str = "dominant_location",
                              lookback_windows: int = 7) -> pd.DataFrame:
    """Counts, for each row, how many of the previous `lookback_windows` rows
    shared the same dominant location and crossed the normal-load line —
    a proxy for "this same routine keeps repeating" (thesis section 3.3).
    """
    features = features.copy()
    crossed = features["normal_crossings"] > 0
    repetition = []
    for i in range(len(features)):
        start = max(0, i - lookback_windows)
        window_slice = features.iloc[start:i]
        same_location_crossed = (
            (window_slice[location_col] == features.iloc[i][location_col]) & crossed.iloc[start:i]
        ).sum()
        repetition.append(same_location_crossed)
    features["repetition_frequency"] = repetition
    return features
