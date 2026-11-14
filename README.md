# End-to-End Data Management Pipeline for a Recommendation System

## Assignment alignment
This repository implements the required pipeline:
**Data Ingestion → Data Validation → Data Preparation → Data Transformation → Feature Management → Model Training → Model Evaluation → Orchestration**.

The implementation uses a clearly documented **synthetic dataset** so the project is self-contained and reproducible. The assignment permits synthetic data when clearly documented.

## Models
1. **PopularityBaseline**: ranks items using interaction popularity weighted by average rating.
2. **ItemBasedCollaborativeFiltering**: item-item cosine similarity from the user-item rating matrix.

## Evaluation
K=5. The pipeline reports:
- Precision@5
- Recall@5
- NDCG@5
- Coverage
- Diversity

An 80/20 **time-based split** is used to avoid training on future interactions.

## Validation
Automated checks cover:
- missing required columns
- duplicate rows
- invalid ratings outside 1–5
- invalid timestamps
- referential integrity for user and item IDs

Invalid interaction records are written to `data/errors/invalid_interactions.csv`; validation findings are written to `data/errors/validation_report.csv`.

## Feature management
Reusable user, item and interaction feature tables are created in `data/features/`. The feature catalog is documented in `feature_catalog.csv`.

## Experiment tracking
A lightweight local experiment tracker records run name, timestamp, parameters, metrics and model artifacts in `artifacts/experiment_runs.json`. This avoids requiring an external tracking server while preserving reproducible experiment metadata.

## Orchestration
`run_pipeline.py` executes the complete workflow in dependency order. This is the clearly structured scheduled Python workflow option from the assignment.

## Setup
```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python generate_data.py
python run_pipeline.py
```

## Outputs
- `data/raw/`: raw users, items and interactions
- `data/errors/`: invalid records and validation report
- `data/processed/`: time-split datasets and derived tables
- `data/features/`: reusable features
- `models/`: trained model artifacts
- `reports/model_evaluation.csv`: comparison table
- `artifacts/experiment_runs.json`: experiment tracking log
- `logs/pipeline_run.log`: successful run log
- `reports/final_report.pdf`: short final report
- `reports/architecture.png`: pipeline architecture diagram

## Reproducibility
The data generator uses seed 2026. The pipeline configuration is stored in `configs/config.json`. Running the two commands above recreates the data and all derived artifacts.

## Notes
The synthetic data is intentionally injected with a small number of invalid interaction records and one duplicate so the validation/error-handling stage has demonstrable output. These records are removed before training.
