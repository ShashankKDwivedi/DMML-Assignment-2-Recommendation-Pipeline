from pathlib import Path
import pandas as pd


def validate_data(data: dict[str, pd.DataFrame], error_dir: str | Path) -> tuple[dict[str, pd.DataFrame], dict]:
    error_dir = Path(error_dir); error_dir.mkdir(parents=True, exist_ok=True)
    users, items, interactions = data['users'], data['items'], data['interactions']
    errors = []
    required = {
        'users': ['user_id', 'age', 'country'],
        'items': ['item_id', 'category', 'item_title'],
        'interactions': ['user_id', 'item_id', 'rating', 'timestamp'],
    }
    for name, cols in required.items():
        missing = [c for c in cols if c not in data[name].columns]
        if missing:
            errors.append({'table': name, 'issue': 'missing_columns', 'count': len(missing), 'details': ','.join(missing)})
    duplicate_counts = {name: int(df.duplicated().sum()) for name, df in data.items()}
    for name, count in duplicate_counts.items():
        if count:
            errors.append({'table': name, 'issue': 'duplicates', 'count': count, 'details': 'duplicate rows'})
    bad_rating = ~interactions['rating'].between(1, 5)
    bad_timestamp = interactions['timestamp'].isna()
    bad_user = ~interactions['user_id'].isin(users['user_id'])
    bad_item = ~interactions['item_id'].isin(items['item_id'])
    masks = {'invalid_rating': bad_rating, 'invalid_timestamp': bad_timestamp, 'invalid_user_fk': bad_user, 'invalid_item_fk': bad_item}
    invalid_any = pd.Series(False, index=interactions.index)
    for issue, mask in masks.items():
        count = int(mask.sum())
        invalid_any |= mask
        if count:
            errors.append({'table': 'interactions', 'issue': issue, 'count': count, 'details': 'record separated to errors'})
    invalid = interactions.loc[invalid_any].copy()
    if not invalid.empty:
        invalid.to_csv(error_dir / 'invalid_interactions.csv', index=False)
    clean = interactions.loc[~invalid_any].copy()
    report = pd.DataFrame(errors)
    report.to_csv(error_dir / 'validation_report.csv', index=False)
    summary = {
        'users_rows': len(users), 'items_rows': len(items), 'interactions_rows': len(interactions),
        'valid_interactions': len(clean), 'invalid_interactions': len(invalid),
        'duplicate_counts': duplicate_counts, 'errors': errors,
    }
    return {'users': users.drop_duplicates().copy(), 'items': items.drop_duplicates().copy(), 'interactions': clean}, summary
