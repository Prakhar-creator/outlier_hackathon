import json
from pathlib import Path


def write_summary_report(metrics: dict, output_dir: str) -> None:
    """
    Write the metrics summary to a JSON file.
    
    Args:
        metrics: Dictionary containing analyzed metrics with structure:
                 - repository_path: str
                 - commits: list[str]
                 - per_commit_metrics: list[dict]
        output_dir: Directory where the summary.json file will be written
    """
    output_path = Path(output_dir) / "summary.json"
    
    with open(output_path, "w") as f:
        json.dump(metrics, f, indent=2)
