from pathlib import Path
import pandas as pd


def load_csv_data(raw_dir: str | Path) -> dict[str, pd.DataFrame]:
    raw_dir = Path(raw_dir)
    return {
        'users': pd.read_csv(raw_dir / 'users.csv'),
        'items': pd.read_csv(raw_dir / 'items.csv'),
        'interactions': pd.read_csv(raw_dir / 'interactions.csv', parse_dates=['timestamp']),
    }
