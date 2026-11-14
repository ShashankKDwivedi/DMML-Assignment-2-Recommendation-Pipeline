# Submission checklist

| Assignment requirement | Delivered artifact |
|---|---|
| Data ingestion | `src/ingestion/load_data.py` |
| Data validation + error records | `src/validation/validate.py`, `data/errors/` |
| Data preparation + time split | `src/preparation/prepare.py`, `data/processed/` |
| Data transformation | `src/transformation/transform.py` |
| Feature management + catalog | `data/features/`, `feature_catalog.csv` |
| Popularity baseline | `src/training/models.py` |
| Personalized recommender | `src/training/models.py` (Item-based CF) |
| Experiment tracking | `src/tracking/local_tracker.py`, `artifacts/experiment_runs.json` |
| Precision@K, Recall@K, NDCG@K, Coverage, Diversity | `src/evaluation/metrics.py` |
| Results comparison | `reports/model_evaluation.csv` |
| Orchestration workflow | `src/orchestration/pipeline.py`, `dags/recommendation_pipeline.py` |
| Architecture diagram | `reports/architecture.png` |
| Successful execution evidence | `reports/pipeline_success_capture.png` |
| Short final report PDF | `reports/final_report.pdf` |
| Setup instructions | `README.md` |
| Dependencies | `requirements.txt` |

## Before submission
1. Read the README and run the project once in the target environment.
2. If your faculty specifically requires a screenshot from the BITS virtual lab, take that screenshot after executing `python run_pipeline.py` there and replace `reports/pipeline_success_capture.png` with the actual screenshot.
3. Push the repository to GitHub and submit the GitHub URL plus `reports/final_report.pdf` as required by the assignment.
