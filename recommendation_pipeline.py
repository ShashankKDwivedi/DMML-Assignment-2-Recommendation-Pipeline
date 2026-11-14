"""Orchestration entry point for schedulers such as cron/Task Scheduler."""
from pathlib import Path
from src.orchestration.pipeline import run_pipeline

if __name__ == '__main__':
    run_pipeline(Path(__file__).resolve().parents[1])
