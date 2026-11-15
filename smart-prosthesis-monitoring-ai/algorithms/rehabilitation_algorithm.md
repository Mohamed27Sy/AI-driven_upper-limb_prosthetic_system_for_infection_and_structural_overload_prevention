# Rehabilitation / Exercise Algorithm (Pre-Osseointegration)

Source: Thesis Section 3.2, Figure 3.2.2
(`../docs/images/fig_3_2_2_load_sub_algorithms.png`). This is the detail behind
"Case 2" in [`load_monitoring_algorithm.md`](load_monitoring_algorithm.md) — what
actually happens inside each sub-algorithm while a patient is still completing
osseointegration and is not yet allowed normal prosthetic load.

## Why It Exists

Osseointegration takes time to complete. During that window the patient must avoid
taking real load through the implant, but still needs to do doctor-prescribed
exercises so the process succeeds. The load sensor is reused here — not to catch
overload, but to confirm the prescribed exercises are actually being done.

## Per-Day Loop (within a sub-algorithm)

```
1. Show the patient a notification of the day's required exercises:
   duration target (X minutes), count target (Y exercises). Start a timer.
2. Count each exercise completed → x. Count cumulative duration achieved → y.
3. At a fixed daily check time (thesis example: 3 p.m.), check x = X and y = Y.
     ├─ Both met     → step 4
     └─ Not met      → back to step 1 (re-notify the patient for the rest of the day)
4. Increment the phase-day counter z by 1 (one more day of the goal met).
5. Has the required number of days for this sub-algorithm been reached (z = Z)?
     ├─ NO  → END for today (continue same sub-algorithm tomorrow)
     └─ YES → step 6
6. Advance:
     Sub-1 → Sub-2 → Sub-3 → (Sub-3 complete) → notify doctor, phase's exercise
     program is finished.
```

## Parameters by Sub-Algorithm

| Sub-Algorithm | Applies to week(s) | Duration/session (min), X | Sessions/day, Y | Days required, Z |
|---|---|---|---|---|
| Sub-1 | Weeks 1–2 of the phase | 30 | 4 | 14 |
| Sub-2 | Week 3 of the phase | 60 | 6 | 7 |
| Sub-3 | Week 4 of the phase | 120 | 4 | 7 |

Each of the three main load-bearing phases (1 kg / 2 kg / 3.5 kg prosthetic weight
— see [`load_monitoring_algorithm.md`](load_monitoring_algorithm.md)) runs through
all three sub-algorithms in sequence before the patient can move to the next
phase's weight.

## Reference Implementation

See [`../src/preprocessing.py`](../src/preprocessing.py)
(`track_rehabilitation_progress`) for a Python implementation of this per-day
tracking loop.
