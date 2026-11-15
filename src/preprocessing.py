"""
preprocessing.py
================
Data cleaning and rehabilitation-tracking logic behind the pre-osseointegration
exercise program described in ../algorithms/rehabilitation_algorithm.md.

This module is a direct implementation of the thesis's own algorithm steps
(Figure 3.2.2). It does not depend on real patient data — `track_rehabilitation_progress`
operates on whatever daily exercise logs you feed it.
"""
from dataclasses import dataclass, field
from typing import List, Optional
import pandas as pd

# Sub-algorithm parameters from thesis Table 3.2.2
SUB_ALGORITHM_PARAMS = {
    1: {"duration_min": 30, "sessions_per_day": 4, "days_required": 14},
    2: {"duration_min": 60, "sessions_per_day": 6, "days_required": 7},
    3: {"duration_min": 120, "sessions_per_day": 4, "days_required": 7},
}

PHASE_WEIGHTS_KG = {1: 1.0, 2: 2.0, 3: 3.5}


@dataclass
class RehabDay:
    day_index: int
    sessions_done: int
    minutes_done: int


@dataclass
class RehabProgress:
    phase: int = 1
    sub_algorithm: int = 1
    day_in_sub: int = 0
    completed: bool = False
    log: List[str] = field(default_factory=list)


def track_rehabilitation_progress(days: List[RehabDay], phase: int = 1) -> RehabProgress:
    """Run the per-day loop from algorithms/rehabilitation_algorithm.md over a
    sequence of daily exercise logs, advancing sub-algorithms/phases as goals
    are met. Mirrors thesis Figure 3.2.2, steps 1-6.
    """
    progress = RehabProgress(phase=phase)
    for day in days:
        params = SUB_ALGORITHM_PARAMS[progress.sub_algorithm]
        goal_met = (
            day.sessions_done >= params["sessions_per_day"]
            and day.minutes_done >= params["duration_min"]
        )
        if not goal_met:
            progress.log.append(
                f"Day {day.day_index}: goal NOT met "
                f"(sub-{progress.sub_algorithm}, phase {progress.phase})"
            )
            continue

        progress.day_in_sub += 1
        progress.log.append(
            f"Day {day.day_index}: goal met "
            f"({progress.day_in_sub}/{params['days_required']} days, "
            f"sub-{progress.sub_algorithm}, phase {progress.phase})"
        )

        if progress.day_in_sub >= params["days_required"]:
            progress.day_in_sub = 0
            if progress.sub_algorithm < 3:
                progress.sub_algorithm += 1
                progress.log.append(
                    f"  -> advancing to sub-algorithm {progress.sub_algorithm}"
                )
            elif progress.phase < 3:
                progress.phase += 1
                progress.sub_algorithm = 1
                progress.log.append(
                    f"  -> phase complete, advancing to phase {progress.phase} "
                    f"({PHASE_WEIGHTS_KG[progress.phase]} kg)"
                )
            else:
                progress.completed = True
                progress.log.append("  -> rehabilitation program complete, notify doctor")
    return progress


def clean_load_log(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning for a raw load-sensor log.

    Expected columns: timestamp, day_of_week, unit_location, applied_load_kg.
    Drops rows with missing/negative load values and sorts by timestamp.
    """
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.dropna(subset=["timestamp", "applied_load_kg"])
    df = df[df["applied_load_kg"] >= 0]
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df


def segment_into_intervals(df: pd.DataFrame, interval_seconds: int = 10) -> pd.DataFrame:
    """Resample a load log into fixed-width intervals, taking the max load
    per interval (matches the thesis's 10-second interval analysis, Figure 3.3.3).
    """
    df = df.set_index("timestamp")
    resampled = df["applied_load_kg"].resample(f"{interval_seconds}s").max()
    return resampled.reset_index().rename(columns={"applied_load_kg": "max_load_kg"})
