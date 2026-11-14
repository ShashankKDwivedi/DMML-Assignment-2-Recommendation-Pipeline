from pathlib import Path
import pandas as pd


def prepare_data(data: dict[str, pd.DataFrame], processed_dir: str | Path) -> dict[str, pd.DataFrame]:
    processed_dir = Path(processed_dir); processed_dir.mkdir(parents=True, exist_ok=True)
    interactions = data['interactions'].copy().sort_values('timestamp')
    interactions['timestamp'] = pd.to_datetime(interactions['timestamp'], utc=True)
    cutoff = interactions['timestamp'].quantile(0.80)
    train = interactions[interactions['timestamp'] <= cutoff].copy()
    test = interactions[interactions['timestamp'] > cutoff].copy()
    users = data['users'].copy(); items = data['items'].copy()
    user_activity = train.groupby('user_id').agg(user_activity_count=('item_id','count'), user_avg_rating=('rating','mean'), last_interaction=('timestamp','max')).reset_index()
    item_popularity = train.groupby('item_id').agg(item_popularity=('user_id','count'), item_avg_rating=('rating','mean')).reset_index()
    matrix = train.pivot_table(index='user_id', columns='item_id', values='rating', aggfunc='mean', fill_value=0)
    train.to_csv(processed_dir/'train.csv', index=False); test.to_csv(processed_dir/'test.csv', index=False)
    user_activity.to_csv(processed_dir/'user_activity.csv', index=False); item_popularity.to_csv(processed_dir/'item_popularity.csv', index=False)
    matrix.to_csv(processed_dir/'user_item_matrix.csv')
    return {'users': users, 'items': items, 'train': train, 'test': test, 'user_activity': user_activity, 'item_popularity': item_popularity, 'matrix': matrix}
