# Project Overview

Source: Chapter 1 of the original thesis (`original_thesis.pdf`).

## Background

Osseointegration connects a titanium implant directly to bone in three stages
(Figure `fig_1_3_1_osteointegration_process.png`): a temporary metal slice/screw
stabilizes the healing bone, it is then replaced with a titanium tube that the bone
grows around, and once stable that tube becomes the anchor point for the external
prosthetic arm. Compared to classical socket/shell prosthetics
(`fig_1_1_1_prosthetic_limb_types.png`), this gives better load feel and stability,
but removes the soft-tissue cushioning that used to protect the bone from overload
and closes off the skin as a barrier against infection.

## Causes of Implant Failure

The thesis groups implant-failure causes into four categories
(`fig_1_4_1_implant_failure_causes.png`): material failure / engineering design /
implant handling; surgical failure / mechanics of bone fixation / type of surgery;
idiosyncratic host response / local tissue response; and "other causes" (fresh
trauma, overweight). This project addresses the two causes that are both common and
addressable with continuous sensing: **infection** and **overload**.

## Why Continuous Monitoring

Patients are typically checked on a fixed schedule (e.g. monthly). Because patients
differ in body and routine, a problem that starts between two check-ups may not be
noticed until it has already progressed. The thesis compares infection-detection
methods on this basis:

| Method | Response Time | Locality | Early Detection | Cost |
|---|---|---|---|---|
| Clinical/visual test | Highly delayed | Surface skin only | Impossible | Low |
| Standard lab blood test | Hours to a day | Very general (CRP) | Very weak | Expensive |
| Microbiological lab test | 24–72h (14+ days to culture) | Localized, some false positives | Delayed | High |
| **Proposed: IrO₂ pH sensor** | **Real-time, continuous** | **High accuracy — placed at implant** | **Early warning** | **Cost-effective** |

## Two Problems, One System

1. **Overload** — a load sensor at the implant/prosthesis connection point measures
   applied load continuously, notifies the patient when it's too high, and logs
   load/time/location to a per-patient database. An AI model then studies that
   database for repeated routine patterns to predict — and warn about — overload
   *before* it happens again.
2. **Infection** — an IrO₂ pH sensor at the bone-implant interface detects the small
   pH shifts (increase or decrease) caused by bacterial activity, well before
   traditional clinical/lab tests would catch it.

See [`technical_documentation.md`](technical_documentation.md) for the system
architecture and [`../algorithms/`](../algorithms/) for the decision logic of each
sensor.
