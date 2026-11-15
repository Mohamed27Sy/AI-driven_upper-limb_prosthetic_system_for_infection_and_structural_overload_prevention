# AI Notebooks

Six notebooks, in pipeline order, implementing the predictive AI component
described in [`../docs/ai_workflow.md`](../docs/ai_workflow.md):

| Notebook | Purpose |
|---|---|
| `01_data_exploration.ipynb` | Generate/inspect the per-patient load database |
| `02_data_preprocessing.ipynb` | Clean the log, segment into 10-second intervals |
| `03_feature_engineering.ipynb` | Build per-day features + Safe/Risk labels |
| `04_model_training.ipynb` | Train a classifier on those features |
| `05_model_testing.ipynb` | Confusion matrix, precision/recall/F1 on held-out data |
| `06_results_analysis.ipynb` | Interpret results, with the same caveats as the thesis |

All six were run end-to-end while building this repository (see `../data/` and
`../results/` for the generated CSVs, trained model, and plots).

## What's a direct thesis result vs. a reconstruction

Be precise about this distinction — it matters if this repo is used in a job
application or academic context:

- **Direct from the thesis (not reproduced here as data, only as description):**
  the two example patterns in Section 3.3 (a short high-load spike at a
  supermarket; a repeated 10–17 minute medium-load routine at home, peak ≈ 4 kg,
  average ≈ 0.80 kg, 29/85 intervals crossing the normal limit) and the reported
  confusion matrix (Figure 3.3.4). Those numbers and the original screenshots are
  preserved as images in [`../results/`](../results/) — they are **not**
  regenerated or altered.
- **Reconstruction (this repo's own code, not the original implementation):**
  the synthetic dataset in `01_data_exploration.ipynb` was generated to have the
  same statistical shape as the thesis's reported numbers, because the original
  per-patient database was not exported from the thesis work. Everything from
  `02` onward runs on that synthetic data. The classifier in
  `04_model_training.ipynb` is a standard `RandomForestClassifier` chosen because
  the thesis documents the model's *inputs, outputs, and target patterns* but not
  a specific architecture — using a named, verifiable algorithm here is more
  honest than presenting an unspecified "AI model" as if it were the original one.

If you reuse this repository, keep that distinction visible rather than
presenting the reconstruction's output numbers as the thesis's own results.
