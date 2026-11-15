# Smart Prosthesis Monitoring System with Predictive AI

**Biomedical Engineering · Medical Devices · Sensors · Embedded Systems · AI · Digital Health**

> Graduation project (Azerbaijan State Oil and Industry University, Instrumentation
> Engineering Dept., 2026) — *"Smartification of Prosthetics for Improved
> Human-Interaction Efficiency"* — reorganized here as an engineering portfolio
> repository. Original thesis: [`docs/original_thesis.pdf`](docs/original_thesis.pdf).

---

## Overview

Osseointegrated upper-limb prostheses (an implant fused directly into bone) give
patients better load-feeling and more stable mechanical control than socket-based
prosthetics. But the technique carries two under-monitored risks:

1. **Infection** — the implant breaks the skin barrier, creating an open path for
   bacteria around the bone-implant interface.
2. **Mechanical overload** — patients cannot always feel exactly how much load they
   are putting through the implant, so bone/implant damage can build up silently.

This project designs a **dual-sensor patient safety system** to catch both risks
early:

- An **IrO₂ pH sensor** at the bone-implant interface, to detect the chemical
  signature of infection before visible symptoms appear.
- A **strain-gauge load sensor** at the abutment, to track mechanical loading in
  real time.
- A **predictive AI component** that studies a patient's long-term load history to
  recognize repeated high- and medium-load routines (not just single overload
  events) and warn the patient before the risk repeats.

```
                 SMART PROSTHESIS
                        │
          ┌─────────────┴─────────────┐
          │                           │
     pH Monitoring              Load Monitoring
          │                           │
    Infection Risk             Mechanical Risk
          │                           │
          └─────────────┬─────────────┘
                         │
                   Processing
                         │
                  AI Prediction
                         │
                Risk Notification
```

## Problem

Patients typically only get their osseointegrated implant checked on a fixed
schedule (e.g. monthly). Infection and overload both tend to build up silently
between visits — by the time a problem is caught at the next appointment it may
already have progressed. See [`docs/project_overview.md`](docs/project_overview.md)
for the full problem framing and comparison against existing infection-detection
methods.

## System Architecture

The system is organized into four connected units, matching the thesis's block
diagram (Figure 2.1.1):

| Unit | Location | Elements |
|---|---|---|
| **Internal Body** | inside the implant | pH sensor, load sensor, processing unit |
| **Body-Connected** | prosthetic arm | battery, inductive power transfer |
| **Near Body** | mobile gate unit | display, memory, controls, patient notifications |
| **Remote** | doctor dashboard / cloud | data storage, AI training data, doctor instructions |

```
┌───────────────────────────────┐
│         IMPLANT / BODY        │
│                                │
│   pH Sensor      Load Sensor  │
│        │              │       │
│        └──────┬───────┘       │
│               ↓                │
│        Processing Unit         │
└───────────────┬────────────────┘
                 │  (wireless)
                 ↓
┌───────────────────────────────┐
│        MOBILE GATE UNIT        │
│  Processing / Display / Memory │
│  / Patient Communication       │
└───────────────┬────────────────┘
                 │
               Cloud
                 │
                 ↓
┌───────────────────────────────┐
│        DOCTOR DASHBOARD        │
│   Data / Alerts / Instructions │
└───────────────────────────────┘
```

Full per-unit breakdown (battery/inductive power system, near-body and remote
processing) is in [`docs/technical_documentation.md`](docs/technical_documentation.md)
and the original figures in [`docs/images/`](docs/images/).

## Sensor Systems

### pH Monitoring (infection detection)

An IrO₂-based sensor placed at the bone-implant interface detects both acidic
(pH < 6.5, bacterial breakdown of tissue) and alkaline (pH > 7.5, biofilm/salt
buildup) deviations, chosen for its biocompatibility, chemical stability, and fast
response. Signal path: IrO₂ sensor → buffer (isolation) → offset (removes negative
readings) → gain amplifier → processing unit.

### Load Monitoring (overload detection)

A strain-gauge sensor at the abutment measures real-time mechanical load. Signal
path: strain gauge → Wheatstone bridge → instrumentation amplifier → low-pass
filter → processing unit. The allowed load limit is personalized per patient using
four factors (age, osteoporosis, sex, bone density — see
[`algorithms/load_monitoring_algorithm.md`](algorithms/load_monitoring_algorithm.md)).
Before osseointegration is complete, the same sensor also tracks a 3-phase
rehabilitation exercise program instead of a load limit.

Full decision logic for both sensors — written out from the thesis's flowcharts —
is in [`algorithms/`](algorithms/).

## Predictive AI

The load-monitoring database (timestamp, location, applied load) is used to train
a model that looks for **repeated patterns** in a patient's routine — not just
single threshold violations. Two example patterns from the thesis:

1. **Short, high-load spikes** repeated at the same place/time (e.g. carrying
   groceries from the same supermarket every week).
2. **Medium, sustained loads** repeated over long windows (e.g. a recurring chore
   that keeps load elevated for 10–17 minutes at a time).

The model flags a patient's routine as `Safe` (0) or `Risk` (1) so the system can
notify them *before* the pattern repeats, rather than only reacting after a
threshold is crossed. See [`ai/`](ai/) for the reconstructed notebooks and
[`docs/ai_workflow.md`](docs/ai_workflow.md) for the full pipeline description.

## Results

The thesis's own evaluation (screenshots preserved in
[`results/`](results/)) reported a confusion matrix over roughly 600k labeled
intervals with the model correctly identifying the large majority of `Risk` cases,
alongside a worked example of a repeated medium-load routine (peak ≈ 4 kg, average
≈ 0.80 kg, 29 of 85 intervals crossing the normal-load line without any single
interval crossing the high-risk limit). Full write-up:
[`results/results_summary.md`](results/results_summary.md).

**This was a laboratory/simulation evaluation, not a clinical one — see
Limitations below.**

## Repository Structure

```
smart-prosthesis-monitoring-ai/
├── README.md
├── LICENSE
├── requirements.txt
├── docs/                    # architecture, original thesis, figures
├── algorithms/              # pH / load / rehabilitation decision logic
├── ai/                      # notebooks: exploration → preprocessing → training → testing → results
├── src/                     # reusable Python modules behind the notebooks
├── tests/                   # unit tests for src/
├── results/                 # thesis figures + regenerated results
├── data/                    # data schema (no real patient data included)
└── images/                  # supporting figures
```

## Limitations

- No in-human testing was performed; the implant-side sensors are a design/simulation,
  not a built and validated medical device.
- Evaluation was done in laboratory/artificial-environment simulations, not on real
  patients or real implant hardware.
- The pH sensor's long-term stability inside tissue fluid, and the AI model's ability
  to generalize across different patients' routines, are stated assumptions of the
  original thesis rather than things that were empirically validated.
- Clinical validation and regulatory approval are outside the scope of this project.
- The AI notebooks in this repository are a **methodology reconstruction**: they
  implement the same monitoring logic and produce the same style of analysis
  (interval-based load fluctuation, repeated-pattern detection, Safe/Risk
  classification) described in the thesis, using synthetic data generated to match
  the thesis's own reported statistics, since the original patient-routine dataset
  was not exported from the thesis work. This is stated explicitly wherever it
  applies — see [`ai/README.md`](ai/README.md).

## Future Development

```
Real Sensor Prototype → Embedded Implementation (e.g. STM32)
      → Wireless Communication → Real-Time Database
      → Doctor Dashboard → AI Model Deployment → Edge/Embedded AI
```

- Real-time sensor acquisition on physical hardware
- Wireless communication between the four units (currently only block-diagrammed)
- Cloud database and doctor dashboard implementation
- Larger, real (not synthetic) patient-routine datasets
- Patient-specific model personalization and external validation
- Model and power optimization for a low-power embedded deployment

## Technologies

Python, Jupyter, pandas, NumPy, scikit-learn, Matplotlib/Seaborn — see
[`requirements.txt`](requirements.txt).

## Project Status

**Research prototype / system design** — graduation project, reorganized as a
portfolio repository. Not a certified or clinically validated medical device.

## Author

Mohamad Khaled Alkadi — Instrumentation Engineering, Azerbaijan State Oil and
Industry University (2026). Advisor: Assoc. Prof. T.CH. Aliyev.
