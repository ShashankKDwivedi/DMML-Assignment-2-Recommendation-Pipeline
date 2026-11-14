from pathlib import Path
import json
from datetime import datetime, timezone

class LocalExperimentTracker:
    """Lightweight local experiment tracker: records parameters, metrics and artifact paths."""
    def __init__(self, path: str | Path):
        self.path = Path(path); self.path.parent.mkdir(parents=True, exist_ok=True)
        self.runs = []
    def log_run(self, name: str, params: dict, metrics: dict, artifacts: list[str]):
        self.runs.append({'run_name': name, 'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'params': params, 'metrics': metrics, 'artifacts': artifacts})
        self.path.write_text(json.dumps(self.runs, indent=2, default=str), encoding='utf-8')
