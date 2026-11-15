# Predictive AI — Workflow

Source: Section 3.3 of the original thesis.

## Purpose

The load sensor alone can only react *after* a reading crosses a threshold. The AI
component instead studies a patient's **load history** for repeated routine
patterns, so the system can warn the patient *before* the same risky routine
happens again — covering both:

- **Repeated high-load spikes** for a short period (e.g. carrying groceries by
  hand instead of using a cart).
- **Repeated medium loads sustained over a longer period** (e.g. a recurring chore
  that keeps load elevated for 10–17 minutes) — flagged even though no single
  reading crosses the high-risk limit, because sustained medium load can damage
  bone over time just as high spikes can.

## Pipeline

```
Load Sensor Data
      ↓
Patient Database (timestamp, day of week, location unit, applied load)
      ↓
Data Preprocessing (cleaning, interval segmentation)
      ↓
Feature Extraction (peak load, average load, duration, threshold crossings,
                     time-of-day, location, repetition frequency)
      ↓
Pattern Detection (repeated high-load vs. repeated medium-load routines)
      ↓
AI Model (Safe / Risk classification)
      ↓
Risk Prediction
      ↓
Patient Notification (via mobile gate unit)
```

## Notebooks

The [`../ai/`](../ai/) folder reconstructs this pipeline as six notebooks, numbered
in pipeline order: exploration → preprocessing → feature engineering → training →
testing → results analysis. See [`../ai/README.md`](../ai/README.md) for exactly
which parts are a direct reconstruction of the thesis's own reported numbers
(the confusion matrix and the two example load patterns) versus supporting
scaffolding built to demonstrate the same methodology on synthetic data.

## Interpretation Note

The thesis is explicit that this was a laboratory/simulation evaluation, not a
clinical one. Model performance numbers here should be read the same way: they
demonstrate that the described methodology works on data with the same statistical
shape the thesis reports, not that the system has been clinically validated.
