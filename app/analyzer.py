import os
import subprocess
from pathlib import Path
from complexity import compute_function_complexities


def get_git_commits(repo_path: str, num_commits: int) -> list[str]:
    """
    Get the last num_commits commit hashes in chronological order (oldest first).
    
    Args:
        repo_path: Path to the Git repository
        num_commits: Number of commits to retrieve
        
    Returns:
        List of commit hashes in chronological order (oldest first)
        
    Raises:
        RuntimeError: If git command fails
    """
    result = subprocess.run(
        ["git", "log", "--oneline", f"-{num_commits}", "--pretty=format:%H"],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to get git commits: {result.stderr}")
    
    commits = result.stdout.strip().split("\n")
    commits = [c.strip() for c in commits if c.strip()]
    commits.reverse()  # Reverse to get oldest first
    return commits


def analyze_code_metrics(python_files: list[str]) -> dict:
    """
    Analyze code metrics for a set of Python files.
    
    Args:
        python_files: List of Python file paths to analyze
        
    Returns:
        Dictionary with metrics: total_code_lines, total_comment_lines, total_blank_lines,
                                 average_cyclomatic_complexity, maximum_cyclomatic_complexity
    """
    total_code_lines = 0
    total_comment_lines = 0
    total_blank_lines = 0
    all_complexities = []
    
    for filepath in python_files:
        if not filepath.endswith(".py"):
            continue
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except (IOError, UnicodeDecodeError):
            continue
        
        # Get complexity for this file
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                source = f.read()
            complexities = compute_function_complexities(source)
            all_complexities.extend(complexities)
        except Exception:
            pass
        
        # Classify lines
        for line in lines:
            stripped = line.strip()
            if not stripped:
                total_blank_lines += 1
            elif stripped.startswith("#"):
                total_comment_lines += 1
            else:
                total_code_lines += 1
    
    avg_complexity = (
        sum(all_complexities) / len(all_complexities)
        if all_complexities
        else 0
    )
    max_complexity = max(all_complexities) if all_complexities else 0
    
    return {
        "total_code_lines": total_code_lines,
        "total_comment_lines": total_comment_lines,
        "total_blank_lines": total_blank_lines,
        "average_cyclomatic_complexity": avg_complexity,
        "maximum_cyclomatic_complexity": max_complexity,
    }


def get_python_files(repo_path: str) -> list[str]:
    """
    Get all Python files in the repository, excluding common vendor directories.
    
    IGNORED directories: .git, .venv, site-packages, __pycache__, .pytest_cache
    
    Args:
        repo_path: Path to the repository
        
    Returns:
        List of absolute paths to .py files
    """
    python_files = []
    exclude_dirs = {".git", ".venv", "__pycache__", ".pytest_cache", "site-packages"}
    
    for root, dirs, files in os.walk(repo_path):
        # Remove excluded directories from dirs to prevent traversal
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    
    return python_files


def analyze_repository(repo_path: str, num_commits: int) -> dict:
    """
    Analyze a Git repository and compute metrics for the last num_commits commits.
    
    The analysis:
    - Processes commits in chronological order (oldest → newest)
    - Checks out each commit and analyzes Python files
    - Computes per-commit metrics for code lines, comments, complexity
    - Restores the original branch after analysis
    
    Args:
        repo_path: Path to the Git repository
        num_commits: Number of recent commits to analyze
        
    Returns:
        Dictionary with structure:
        {
            'repository_path': str,
            'commits': list[str],  # commit hashes in chronological order
            'per_commit_metrics': [
                {
                    'commit': str,
                    'total_files': int,
                    'total_code_lines': int,
                    'total_comment_lines': int,
                    'total_blank_lines': int,
                    'average_cyclomatic_complexity': float,
                    'maximum_cyclomatic_complexity': int
                },
                ...
            ]
        }
        
    Raises:
        RuntimeError: If repository is invalid or git operations fail
    """
    # Verify it's a git repository
    if not os.path.isdir(os.path.join(repo_path, ".git")):
        raise RuntimeError(f"{repo_path} is not a Git repository")
    
    commits = get_git_commits(repo_path, num_commits)
    if not commits:
        raise RuntimeError(f"No commits found in repository (attempted to get {num_commits})")
    
    metrics = {
        "repository_path": repo_path,
        "commits": commits,
        "per_commit_metrics": [],
    }
    
    # Get current branch to restore later
    original_branch = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
    ).stdout.strip()
    
    try:
        for commit_hash in commits:
            # Checkout the commit
            result = subprocess.run(
                ["git", "checkout", commit_hash],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                raise RuntimeError(f"Failed to checkout commit {commit_hash}: {result.stderr}")
            
            # Get all Python files at this commit
            python_files = get_python_files(repo_path)
            
            # Analyze metrics
            commit_metrics = analyze_code_metrics(python_files)
            commit_metrics["commit"] = commit_hash
            commit_metrics["total_files"] = len(python_files)
            
            metrics["per_commit_metrics"].append(commit_metrics)
    finally:
        # Restore original branch (read-only, no history mutation)
        subprocess.run(
            ["git", "checkout", original_branch],
            cwd=repo_path,
            capture_output=True,
        )
    
    return metrics
