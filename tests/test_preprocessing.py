import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from preprocessing import (
    RehabDay, track_rehabilitation_progress, clean_load_log, segment_into_intervals
)


def test_rehab_progress_advances_sub_algorithm():
    # 14 consecutive days that all meet Sub-1's goal (30 min, 4 sessions)
    days = [RehabDay(day_index=i, sessions_done=4, minutes_done=30) for i in range(14)]
    progress = track_rehabilitation_progress(days, phase=1)
    assert progress.sub_algorithm == 2
    assert progress.day_in_sub == 0


def test_rehab_progress_does_not_advance_if_goal_missed():
    days = [RehabDay(day_index=i, sessions_done=2, minutes_done=10) for i in range(14)]
    progress = track_rehabilitation_progress(days, phase=1)
    assert progress.sub_algorithm == 1
    assert progress.day_in_sub == 0


def test_clean_load_log_drops_negative_and_missing():
    df = pd.DataFrame({
        "timestamp": ["2026-01-01 10:00:00", "2026-01-01 10:00:10", None],
        "day_of_week": ["Thu", "Thu", "Thu"],
        "unit_location": [1, 1, 1],
        "applied_load_kg": [5.0, -1.0, 3.0],
    })
    cleaned = clean_load_log(df)
    assert len(cleaned) == 1
    assert cleaned.iloc[0]["applied_load_kg"] == 5.0


def test_segment_into_intervals():
    df = pd.DataFrame({
        "timestamp": pd.date_range("2026-01-01", periods=20, freq="1s"),
        "applied_load_kg": list(range(20)),
    })
    out = segment_into_intervals(df, interval_seconds=10)
    assert len(out) == 2
    assert out.iloc[0]["max_load_kg"] == 9
