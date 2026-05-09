import matplotlib.pyplot as plt
from pathlib import Path


def generate_code_trend_chart(metrics: dict, output_dir: str) -> None:
    """
    Generate a PNG chart showing code lines trend over commits.
    
    Args:
        metrics: Dictionary containing analyzed metrics with structure:
                 - commits: list[str]
                 - per_commit_metrics: list[dict] with 'total_code_lines' key
        output_dir: Directory where the code_lines_trend.png file will be written
    """
    commits = metrics["commits"]
    per_commit = metrics["per_commit_metrics"]
    
    code_lines = [m["total_code_lines"] for m in per_commit]
    
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(commits)), code_lines, marker="o", linestyle="-", linewidth=2)
    plt.xlabel("Commit Order")
    plt.ylabel("Total Code Lines")
    plt.title("Code Lines Trend")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_path = Path(output_dir) / "code_lines_trend.png"
    plt.savefig(output_path, dpi=100)
    plt.close()
