import os
import json
from datetime import datetime


def ensure_output_dir(path: str):
    os.makedirs(path, exist_ok=True)


def save_summary(metrics_dict: dict, output_dir: str):
    summary = {
        "timestamp": datetime.now().isoformat(),
        "results": metrics_dict
    }
    path = os.path.join(output_dir, "summary.json")
    with open(path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nResumen guardado en {path}")
