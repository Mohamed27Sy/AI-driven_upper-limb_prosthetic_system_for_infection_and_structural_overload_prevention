"""
risk_detection.py
==================
Direct implementations of the two sensor decision algorithms described in
../algorithms/ph_monitoring_algorithm.md and ../algorithms/load_monitoring_algorithm.md.

These are rule-based (not learned) — they encode the thesis's own flowcharts
(Figures 3.1.1 and 3.2.1), not the predictive AI model (see prediction.py).
"""
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class RiskLevel(Enum):
    NORMAL = "normal"
    MEDIUM = "medium_risk"
    HIGH = "high_risk"


@dataclass
class PHReading:
    value: float


def classify_ph_risk(readings: List[PHReading], contacted_doctor_in_time: Optional[bool] = None,
                      ph_returned_to_normal: Optional[bool] = None) -> RiskLevel:
    """Implements algorithms/ph_monitoring_algorithm.md.

    `readings` should be the pH value plus up to 3 re-checks (thesis step 3/16).
    `contacted_doctor_in_time` / `ph_returned_to_normal` are only consulted once
    a Medium Risk alert has already been raised, matching thesis steps 8-12 / 16-18.
    """
    if not readings:
        raise ValueError("At least one pH reading is required")

    latest = readings[-1].value

    if latest < 7:
        # Acidic branch
        still_decreasing = len(readings) >= 3 and all(
            readings[i].value >= readings[i + 1].value for i in range(len(readings) - 1)
        )
        if not (still_decreasing and latest < 6.5):
            return RiskLevel.NORMAL
        risk = RiskLevel.MEDIUM
        timer_hours = 24
    elif latest > 7.5:
        # Alkaline branch
        risk = RiskLevel.MEDIUM
        timer_hours = 48
    else:
        return RiskLevel.NORMAL

    # Medium risk raised — escalate to High Risk unless the patient contacted
    # the doctor in time AND pH returned to normal afterward.
    if contacted_doctor_in_time and ph_returned_to_normal:
        return RiskLevel.NORMAL  # resolved after treatment
    if contacted_doctor_in_time is None:
        return risk  # still within the contact window, no escalation decision yet
    return RiskLevel.HIGH


# --- Load limit factors, thesis Table 3.2.1 ---
LOAD_LIMIT_FACTORS = {
    "old_age": 0.70,       # -30%
    "osteoporosis": 0.40,  # -60%
    "woman": 0.80,         # -20%
    "low_density_min": 0.40,  # -60% (worst case)
    "low_density_max": 0.70,  # -30% (best case)
}


def compute_max_load_limit(base_limit_kg: float, *, old_age: bool = False,
                            osteoporosis: bool = False, woman: bool = False,
                            low_bone_density: bool = False) -> float:
    """Applies thesis Table 3.2.1's four factors multiplicatively to a base
    (healthy, middle-aged) load limit. `low_bone_density` uses the conservative
    (-60%) end of the reported -30% to -60% range.
    """
    limit = base_limit_kg
    if old_age:
        limit *= LOAD_LIMIT_FACTORS["old_age"]
    if osteoporosis:
        limit *= LOAD_LIMIT_FACTORS["osteoporosis"]
    if woman:
        limit *= LOAD_LIMIT_FACTORS["woman"]
    if low_bone_density:
        limit *= LOAD_LIMIT_FACTORS["low_density_min"]
    return round(limit, 2)


def classify_load_risk(current_load_kg: float, max_limit_kg: float,
                        daily_low_load_count: int, daily_low_load_allowance: int = 25) -> RiskLevel:
    """Implements algorithms/load_monitoring_algorithm.md, Case 1 (steps 5-9)."""
    if current_load_kg >= max_limit_kg:
        return RiskLevel.HIGH
    if current_load_kg >= 0.70 * max_limit_kg:
        return RiskLevel.HIGH
    if daily_low_load_count >= daily_low_load_allowance:
        return RiskLevel.HIGH
    return RiskLevel.NORMAL
