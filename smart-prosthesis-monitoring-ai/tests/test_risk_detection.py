import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from risk_detection import (
    PHReading, classify_ph_risk, RiskLevel, compute_max_load_limit, classify_load_risk
)


def test_ph_normal_range():
    assert classify_ph_risk([PHReading(7.0)]) == RiskLevel.NORMAL


def test_ph_acidic_medium_risk():
    readings = [PHReading(6.9), PHReading(6.7), PHReading(6.4)]
    assert classify_ph_risk(readings) == RiskLevel.MEDIUM


def test_ph_acidic_escalates_to_high_risk_if_not_contacted():
    readings = [PHReading(6.9), PHReading(6.7), PHReading(6.4)]
    result = classify_ph_risk(readings, contacted_doctor_in_time=False)
    assert result == RiskLevel.HIGH


def test_ph_acidic_resolves_after_treatment():
    readings = [PHReading(6.9), PHReading(6.7), PHReading(6.4)]
    result = classify_ph_risk(
        readings, contacted_doctor_in_time=True, ph_returned_to_normal=True
    )
    assert result == RiskLevel.NORMAL


def test_ph_alkaline_medium_risk():
    assert classify_ph_risk([PHReading(7.8)]) == RiskLevel.MEDIUM


def test_load_limit_factors_compound():
    # old age (-30%) and osteoporosis (-60%) compound multiplicatively
    limit = compute_max_load_limit(20.0, old_age=True, osteoporosis=True)
    assert limit == round(20.0 * 0.70 * 0.40, 2)


def test_load_risk_high_when_over_limit():
    assert classify_load_risk(15.0, max_limit_kg=12.0, daily_low_load_count=0) == RiskLevel.HIGH


def test_load_risk_high_when_repeated_low_load_exceeds_allowance():
    assert classify_load_risk(2.0, max_limit_kg=12.0, daily_low_load_count=30) == RiskLevel.HIGH


def test_load_risk_normal():
    assert classify_load_risk(2.0, max_limit_kg=12.0, daily_low_load_count=3) == RiskLevel.NORMAL
