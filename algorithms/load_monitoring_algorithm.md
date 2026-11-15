# Load Monitoring Algorithm (Overload Detection)

Source: Thesis Section 3.2, Figure 3.2.1
(`../docs/images/fig_3_2_1_load_sensor_algorithm.png`). Unlike the pH sensor, the
load sensor samples in real time — overload can happen suddenly and can't be
predicted by a duty cycle. Every reading is stored to build the per-patient
database used by the AI model (see [`../docs/ai_workflow.md`](../docs/ai_workflow.md)),
but an alert only fires when a reading crosses a threshold.

## Decision Flow

```
1. Load Sensing — convert the strain gauge reading to a load value.
2. Is osseointegration complete?
     ├─ NO  → Rehabilitation branch (below)
     └─ YES → Case 1: Post-osseointegration branch
```

### Case 1 — Post-Osseointegration (Personalized Load Limit)

```
3. Get patient data (age, sex, medical condition, disease history).
4. Compute the patient's max load limit from 4 factors (see table below).
5. Does the current load pass the limit?
     ├─ YES → step 9: raise "High Risk" alarm + notification.
     └─ NO  → continue
6. Does the current load pass 70% of the limit?
     ├─ YES → step 9: raise "High Risk" alarm + notification.
     └─ NO  → continue
7. Log this as a low/normal-load reading, increment a daily counter.
8. Has the daily count of low-load repetitions passed the doctor-set limit
   (example given in the thesis: 25/day)?
     ├─ YES → step 9: raise "High Risk" alarm + notification
              (repeated low load, many times a day, is still a risk).
     └─ NO  → END (no alert this cycle).
```

**Personalized max-load-limit factors** (thesis Table 3.2.1):

| Condition | Adjustment | Reason |
|---|---|---|
| Old age (60+) | −30% | Bone becomes lighter / less strong without changing shape |
| Osteoporosis | −60% | Reduced bone strength, higher break risk |
| Women | −20% | Smaller bone structure; hormonal effects can accelerate density loss |
| Low bone density | −30% to −60% | Less mineral concentration in bone, lower stress tolerance |

### Case 2 — Pre-Osseointegration (Rehabilitation Exercises)

Before osseointegration is complete, the patient must not bear normal load — only
a lightweight prosthetic part is worn while completing a prescribed exercise
program, split into three sub-phases:

```
10. Which phase is the patient in? (Phase 1 → 1 kg prosthetic weight,
    Phase 2 → 2 kg, Phase 3 → 3.5 kg — steps 11–14)
15. Which week of that phase? (weeks vary the exercise "sub-algorithm" used)
      ├─ Week 1–2 → Sub-Algorithm 1
      ├─ Week 3   → Sub-Algorithm 2
      └─ Week 4   → Sub-Algorithm 3 → on completion, notify the doctor (step 20)
```

Sub-algorithm parameters (thesis Table 3.2.2):

| Sub-Algorithm | Exercise Duration (min) | Exercises/Day | Days Required |
|---|---|---|---|
| Sub-1 | 30 | 4 | 14 |
| Sub-2 | 60 | 6 | 7 |
| Sub-3 | 120 | 4 | 7 |

Each day: show the patient the required duration/count → count exercises done as
`(x, y)` → at a fixed check time, confirm `x = X` and `y = Y` for that sub-phase →
if met, increment the day counter `z` toward the required days `Z` for that phase →
once `z = Z`, advance to the next sub-algorithm (or notify the doctor, if this was
the final sub-algorithm of the final phase).

## Reference Implementation

See [`../src/risk_detection.py`](../src/risk_detection.py)
(`compute_max_load_limit`, `classify_load_risk`) and
[`../algorithms/rehabilitation_algorithm.md`](rehabilitation_algorithm.md) for the
exercise-tracking logic.
