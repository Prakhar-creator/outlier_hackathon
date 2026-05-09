#!/usr/bin/env python
import sys
import argparse
import os
from pathlib import Path
from analyzer import analyze_repository
from report import write_summary_report
from charts import generate_code_trend_chart


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Python repository metrics over Git history"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze repository")
    analyze_parser.add_argument("--repo", required=True, help="Path to Git repository")
    analyze_parser.add_argument(
        "--commits", type=int, default=10, help="Number of commits to analyze (default: 10)"
    )
    analyze_parser.add_argument("--out", required=True, help="Output directory")
    
    args = parser.parse_args()
    
    if args.command != "analyze":
        parser.print_help()
        sys.exit(1)
    
    # Validate repository path
    repo_path = args.repo
    if not os.path.isdir(repo_path):
        print(f"Error: Repository path '{repo_path}' does not exist", file=sys.stderr)
        return 1
    
    if not os.path.isdir(os.path.join(repo_path, ".git")):
        print(f"Error: '{repo_path}' is not a Git repository", file=sys.stderr)
        return 1
    
    # Validate commits count
    if args.commits <= 0:
        print(f"Error: Number of commits must be positive", file=sys.stderr)
        return 1
    
    # Create output directory if it doesn't exist
    output_dir = Path(args.out)
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating output directory: {e}", file=sys.stderr)
        return 1
    
    try:
        # Analyze repository
        metrics = analyze_repository(repo_path, args.commits)
        
        # Write JSON summary report
        write_summary_report(metrics, str(output_dir))
        
        # Generate trend chart
        generate_code_trend_chart(metrics, str(output_dir))
        
        print(f"Analysis complete. Output written to {output_dir}")
        return 0
    
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
