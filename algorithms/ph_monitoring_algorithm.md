# pH Monitoring Algorithm (Infection Detection)

Source: Thesis Section 3.1, Figure 3.1.1 (`../docs/images/fig_3_1_1_ph_sensor_algorithm.png`).

The pH sensor is sampled on a duty cycle of roughly 30–120 minutes rather than
continuously — pH changes slowly relative to the reaction that causes it, and
continuous real-time sampling would cost far more power than the change in signal
justifies.

## Decision Flow

```
1.  Read pH.
2.  pH < 7?
      ├─ NO  → check pH > 7.5? (go to "Alkaline branch" below)
      └─ YES → acidic branch:
3.        Re-check pH up to 3 times (transient dips are common and not
          necessarily infection).
4.        Still decreasing after 3 checks?
              ├─ NO  → normal pH fluctuation / healing → END
              └─ YES → continue
5.        Now pH < 6.5?
              ├─ NO  → still within normal tissue range → END
              └─ YES → continue
7.        Raise "Medium Risk" alarm + notification to patient's mobile gate unit.
8.        Start a 24-hour timer: did the patient contact the doctor in time?
              ├─ YES (step 9) → doctor prescribes medication (antibiotic)
              │        10. Did pH return to normal?
              │              ├─ YES → END
              │              └─ NO  → escalate to High Risk (step 11)
              └─ NO  → escalate to High Risk (step 11)
11. "High Risk" notification to both patient and doctor — patient must see the
    doctor immediately.
12. Doctor makes a case-specific decision (specific medication or surgery) → END.
```

```
Alkaline branch (pH > 7):
13. pH > 7.5?
      ├─ NO  → normal → END
      └─ YES → continue
14. Flag as risk of alkaline bacterial activity.
15. Raise "Medium Risk" alarm + notification.
16. Start a 48-hour timer: did the patient contact the doctor in time?
      ├─ YES (step 17) → doctor prescribes a basic treatment (acidic gel)
      │        18. Did pH return to normal?
      │              ├─ YES → END
      │              └─ NO  → escalate to High Risk (step 11/12, as above)
      └─ NO  → escalate to High Risk (step 11/12, as above)
```

## Why Two Branches

| Condition | pH range | Bacterial mechanism | Tissue effect |
|---|---|---|---|
| Acidic environment | pH < 6.5 | Breaks down surrounding proteins, prevents cell renewal | Environment becomes weaker/unstable for the implant |
| Alkaline environment | pH > 7.5 | Bacteria increase salt/calcium accumulation | Hard biofilm forms, isolating sensor and implant from tissue |
| Critical risk | pH < 6 or pH > 9 | Tissue breakdown spreads outside the implant site | Toxic to surrounding live tissue |
| Normal | 7.0 ± 0.3 | No bacterial activity | Stable, with minor dips during normal healing |

## Reference Implementation

See [`../src/risk_detection.py`](../src/risk_detection.py) (`classify_ph_risk`) for
a Python implementation of this decision logic, and
[`../tests/test_risk_detection.py`](../tests/test_risk_detection.py) for its tests.
