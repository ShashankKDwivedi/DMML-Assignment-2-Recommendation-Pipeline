from pathlib import Path
import json
from src.ingestion.load_data import load_csv_data
from src.validation.validate import validate_data
from src.preparation.prepare import prepare_data
from src.transformation.transform import transform_features
from src.training.models import PopularityRecommender, ItemCFRecommender, save_model
from src.evaluation.metrics import evaluate_model
from src.tracking.local_tracker import LocalExperimentTracker


def run_pipeline(root='.'):
    root=Path(root)
    print('[1/7] Data ingestion')
    raw=load_csv_data(root/'data/raw')
    print(f"      users={len(raw['users'])}, items={len(raw['items'])}, interactions={len(raw['interactions'])}")
    print('[2/7] Data validation')
    clean, validation=validate_data(raw, root/'data/errors')
    print(f"      valid={validation['valid_interactions']}, invalid={validation['invalid_interactions']}")
    print('[3/7] Preparation / time split')
    prep=prepare_data(clean, root/'data/processed')
    print(f"      train={len(prep['train'])}, test={len(prep['test'])}")
    print('[4/7] Feature management')
    transform_features(prep, root/'data/features')
    print('[5/7] Model training')
    models={
        'PopularityBaseline': PopularityRecommender(prep['items']).fit(prep['train']),
        'ItemBasedCollaborativeFiltering': ItemCFRecommender().fit(prep['train'])
    }
    print('[6/7] Evaluation')
    results=[]
    tracker=LocalExperimentTracker(root/'artifacts/experiment_runs.json')
    for name, model in models.items():
        metrics=evaluate_model(model, prep['train'], prep['test'], prep['items']['item_id'].tolist(), k=5, item_metadata=prep['items'])
        save_model(model, root/'models'/f'{name}.pkl')
        tracker.log_run(name, {'K':5, 'split':'80/20 time-based'}, metrics, [f'models/{name}.pkl'])
        row={'Model':name, **metrics}; results.append(row)
        print('      ', name, json.dumps(metrics))
    print('[7/7] Orchestration complete')
    out=root/'reports/model_evaluation.csv'; out.parent.mkdir(parents=True,exist_ok=True)
    import pandas as pd
    pd.DataFrame(results).to_csv(out,index=False)
    (root/'logs/pipeline_run.log').write_text('PIPELINE STATUS: SUCCESS\n'+json.dumps(results,indent=2),encoding='utf-8')
    return results

if __name__=='__main__':
    run_pipeline('.')
