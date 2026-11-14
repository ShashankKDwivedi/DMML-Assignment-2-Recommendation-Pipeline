from pathlib import Path
import pandas as pd


def transform_features(prepared: dict, features_dir: str | Path) -> dict[str, pd.DataFrame]:
    features_dir = Path(features_dir); features_dir.mkdir(parents=True, exist_ok=True)
    users = prepared['users'].copy(); items = prepared['items'].copy(); train = prepared['train'].copy()
    ua = prepared['user_activity'].copy(); ip = prepared['item_popularity'].copy()
    now = train['timestamp'].max()
    user_features = users.merge(ua, on='user_id', how='left')
    user_features['user_activity_count'] = user_features['user_activity_count'].fillna(0).astype(int)
    user_features['user_avg_rating'] = user_features['user_avg_rating'].fillna(train['rating'].mean())
    user_features['days_since_last_interaction'] = ((now - user_features['last_interaction']).dt.total_seconds()/86400).fillna(999).round(2)
    item_features = items.merge(ip, on='item_id', how='left')
    item_features['item_popularity'] = item_features['item_popularity'].fillna(0).astype(int)
    item_features['item_avg_rating'] = item_features['item_avg_rating'].fillna(train['rating'].mean())
    item_features['popularity_percentile'] = item_features['item_popularity'].rank(pct=True).fillna(0)
    interaction_features = train[['user_id','item_id','rating','timestamp']].copy()
    interaction_features['is_positive'] = (interaction_features['rating'] >= 4).astype(int)
    user_features.to_csv(features_dir/'user_features.csv', index=False)
    item_features.to_csv(features_dir/'item_features.csv', index=False)
    interaction_features.to_csv(features_dir/'interaction_features.csv', index=False)
    return {'user_features': user_features, 'item_features': item_features, 'interaction_features': interaction_features}
