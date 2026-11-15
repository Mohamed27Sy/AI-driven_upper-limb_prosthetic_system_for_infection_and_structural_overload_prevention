# Results Summary

## Thesis's own reported results (preserved as images, not altered)

- **Repeated high-load pattern** (`fig_3_3_1_ai_repeated_high_load_pattern.png`):
  a short-duration high-load spike detected at a supermarket, interpreted as the
  patient carrying purchases by hand rather than using a cart.
- **Repeated medium-load pattern** (`fig_3_3_2_repeated_medium_load_table.png`,
  `fig_3_3_3_medium_load_full_analysis.png`): a recurring home-location routine,
  10–17 minutes long, peak load ≈ 4 kg, average activity ≈ 0.80 kg. Of 85
  separated 10-second intervals, 29 crossed the normal-load line — none crossed
  the high-risk limit, illustrating that the system flags *sustained medium load*
  as a risk even when no single reading is dangerous on its own.
- **Confusion matrix** (`fig_3_3_4_confusion_matrix.png`): reported over roughly
  600k labeled intervals (Safe = 0, Risk = 1), with the model correctly
  identifying the large majority of both classes.

## Reconstruction results (this repo's own code, on synthetic data)

- `exploration_distribution.png` — load distribution and by-location averages for
  the synthetic dataset generated in `ai/01_data_exploration.ipynb`.
- `confusion_matrix_reconstruction.png` — confusion matrix from
  `ai/05_model_testing.ipynb`, evaluating a `RandomForestClassifier` trained on
  60 days of synthetic per-day features.
- `risk_model.joblib` — the trained model artifact from `ai/04_model_training.ipynb`.

**Important:** both sets of results represent a research prototype and
laboratory/simulation-based evaluation. Neither the original thesis results nor
this repository's reconstruction constitute clinical validation. See the
**Limitations** section of the top-level [`README.md`](../README.md).
