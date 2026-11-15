# Technical Documentation — System Architecture

Source: Chapter 2 of the original thesis (`original_thesis.pdf`), Figures 2.1.1–2.3.1
(reproduced in `images/`).

## Four-Unit Architecture

The system architecture (`images/fig_2_1_1_system_architecture_page.png`) is split
into four connected units:

### 1. Internal Body

- **pH sensor** (IrO₂) and **load sensor** (strain gauge), each feeding into a
  **processing unit** that does initial signal conversion and temporary local
  storage (`images/fig_2_1_2_internal_body_elements.png`).
- A **controller** prepares data and manages transmission to the mobile gate unit
  over a transmitter/receiver antenna pair.
- Local **memory** here only keeps the system running and stores the minimum
  necessary data — full history is kept at the mobile gate unit instead.

### 2. Body-Connected

- The **prosthetic arm's battery** also powers the internal system, via a voltage
  converter and an inductive (two-coil) wireless power link
  (`images/fig_2_1_3_battery_system.png`): a primary coil in the prosthetic arm
  transmits power to a secondary coil at the implant abutment, which powers the
  strain gauge. The pH sensor instead uses its own small rechargeable solid-state
  battery (charged the same way) since pH sensing needs far less energy.

### 3. Near Body — Mobile Gate Unit

- Receives data from the internal processing unit's transmitter, and does the
  **main processing**: comparing pH and load readings against normal ranges,
  storing normal readings, and sending abnormal-reading reports to the remote base
  (`images/fig_2_1_4_near_body_elements.png`).
- Provides the patient-facing interface: control buttons (to contact the doctor or
  answer questions), a display (current status, remaining exercises), and memory
  (full data history, used later to build the AI training database).
- Talks to the remote base via a transmitter/receiver antenna and/or cloud link.

### 4. Remote — Doctor Dashboard / Cloud

- Connected to the mobile gate unit and to cloud storage
  (`images/fig_2_1_5_far_away_body_elements.png`), with I/O for the doctor
  (keyboard, display, printer, USB/DVD/Ethernet).
- Lets the doctor review all notifications and data, make medical decisions on
  medium/high risk events, and modify a patient's load limits or exercise
  instructions — which are then transmitted back down to the mobile gate unit.
- Stores the large accumulated per-patient dataset used to train the predictive AI
  model, whose extracted patterns are then applied back at the mobile gate unit.

## Sensor Placement

(`images/fig_2_1_6_sensor_placement.png`) The load sensor sits at the abutment
(external side, at the compression/bending point) for accurate readings without
requiring surgery to access it later. The pH sensor sits at the fixture, closest to
where infection typically starts.

## pH Sensor — IrO₂

(`images/fig_2_2_1_iro2_sensor_components.png`,
`images/fig_2_2_2_iro2_sensor_working_areas.png`) IrO₂ was chosen for its
biocompatibility, chemical stability, and fast pH response, deposited as a thin
film so it can be integrated into the implant. Its response follows the Nernst
equation, measuring the voltage difference between the IrO₂ working electrode and
an Ag/AgCl reference electrode, with reported sensitivity of roughly −0.65 to
−0.77 mV/pH.

Measurement chain (`images/fig_2_2_3_ph_measurement_control_system.png`):

```
IrO2 Sensor → Buffer (isolation) → Offset (removes negative readings) → Gain Amplifier → Processing Unit
```

pH = 7 is the chemical zero. Acidic shifts read as negative, alkaline shifts as
positive — the offset stage shifts these into a positive-only range the ADC and
processing unit can read.

## Load Sensor — Strain Gauge

Measurement chain (`images/fig_2_3_1_load_measurement_control_system.png`):

```
Strain Gauge Load Sensor → Wheatstone Bridge → Instrumentation Amplifier → Low-Pass Filter → Processing Unit
```

The strain gauge's resistance change is converted to a voltage via a Wheatstone
bridge, amplified, low-pass filtered to remove high-frequency noise, then compared
against the patient's threshold in the processing unit.

See [`../algorithms/`](../algorithms/) for the full decision logic each sensor
follows once a reading reaches the processing unit.
