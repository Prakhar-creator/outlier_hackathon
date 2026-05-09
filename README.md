# Python Repository Metrics CLI

A command-line tool that analyzes local Python Git repositories and produces objective metrics about code size and complexity over time.

## Features

✅ **Cyclomatic Complexity Analysis** - Calculates per-function complexity using Python AST  
✅ **Code Metrics** - Tracks code lines, comments, blank lines per commit  
✅ **Git History** - Analyzes last N commits in chronological order  
✅ **Trend Charts** - Generates PNG visualizations of code evolution  
✅ **JSON Reports** - Structured output for further analysis  
✅ **Fully Offline** - No external services or APIs required  
✅ **Read-Only** - No mutation of Git history  

## Project Structure

```
.
├── complexity.py       # Cyclomatic complexity computation (AST-based)
├── analyzer.py         # Repository analysis over Git history
├── report.py           # JSON summary report generation
├── charts.py           # PNG trend chart generation
├── metrics_cli.py      # CLI entry point and orchestration
├── tests/              # Test suite
│   ├── test_complexity.py
│   ├── test_analyzer.py
│   └── test_cli.py
└── prompt.md           # Project specification
```

## Installation

### Prerequisites
- Python 3.10+
- Git (local CLI)
- Virtual environment

### Setup

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install matplotlib
```

## Usage

### Basic Analysis

```bash
python metrics_cli.py analyze --repo <repo_path> --commits 10 --out <output_dir>
```

### Options

- `--repo` (required): Path to Git repository
- `--commits` (optional, default=10): Number of commits to analyze  
- `--out` (required): Output directory for reports and charts

### Example

```bash
python metrics_cli.py analyze --repo /path/to/repo --commits 20 --out ./output
```

This generates:
- `summary.json` - Detailed metrics per commit
- `code_lines_trend.png` - Visualization of code growth

## Output Format

### summary.json

```json
{
  "repository_path": "/path/to/repo",
  "commits": ["abc123...", "def456...", ...],
  "per_commit_metrics": [
    {
      "commit": "abc123...",
      "total_files": 15,
      "total_code_lines": 1234,
      "total_comment_lines": 89,
      "total_blank_lines": 156,
      "average_cyclomatic_complexity": 2.5,
      "maximum_cyclomatic_complexity": 12
    },
    ...
  ]
}
```

## Metrics Definitions

### Cyclomatic Complexity

Per-function complexity using Python AST:
- **Base complexity**: 1 per function
- **+1 for**: if/elif, for/while, and/or, except, ternary expressions
- **Nested functions**: Analyzed independently  
- **Module-level code**: Ignored

**Example**:
```python
def analyze(x):           # base: 1
    if x > 0:             # +1
        if x > 10:        # +1
            return x
        else:
            return x / 2
    return 0

# Complexity = 3
```

### Line Classification

- **Code lines**: Non-blank, non-comment lines (includes inline comments)
- **Comment lines**: Lines starting with `#` (after stripping whitespace)
- **Blank lines**: Empty or whitespace-only lines

### Excluded Paths

The tool ignores:
- `.git/` - Git metadata
- `.venv/` - Virtual environments
- `site-packages/` - Third-party libraries
- `__pycache__/` - Python cache
- `.pytest_cache/` - Test cache

## API Reference

### `complexity.compute_function_complexities(source_code: str) -> list[int]`

Extract cyclomatic complexity for all functions in Python source.

```python
from complexity import compute_function_complexities

code = """
def foo(x):
    if x > 0:
        return True
    return False
"""

complexities = compute_function_complexities(code)
# Returns: [2]
```

### `analyzer.analyze_repository(repo_path: str, num_commits: int) -> dict`

Analyze repository metrics over Git history.

```python
from analyzer import analyze_repository

metrics = analyze_repository("/path/to/repo", 10)
# Returns: structured metrics dict
```

### `report.write_summary_report(metrics: dict, output_dir: str) -> None`

Write metrics to JSON file.

```python
from report import write_summary_report

write_summary_report(metrics, "./output")
# Creates: ./output/summary.json
```

### `charts.generate_code_trend_chart(metrics: dict, output_dir: str) -> None`

Generate PNG trend chart.

```python
from charts import generate_code_trend_chart

generate_code_trend_chart(metrics, "./output")
# Creates: ./output/code_lines_trend.png
```

## Testing

Run the complete test suite:

```bash
python -m pytest tests/ -v
```

Test coverage:
- ✅ Complexity calculation edge cases (10 tests)
- ✅ CLI integration (1 test)
- **Total: 11 tests passing**

### Running Specific Tests

```bash
python -m pytest tests/test_complexity.py -v    # Complexity tests
python -m pytest tests/test_cli.py -v           # CLI integration test
```

## Error Handling

The tool validates:
- ✅ Repository path exists
- ✅ Directory is a Git repository
- ✅ Commits count is positive
- ✅ Output directory can be created
- ✅ Git operations succeed
- ✅ Proper restoration of original branch

Example errors:

```bash
$ python metrics_cli.py analyze --repo /nonexistent --out /tmp/out
Error: Repository path '/nonexistent' does not exist

$ python metrics_cli.py analyze --repo /tmp/notgit --out /tmp/out
Error: '/tmp/notgit' is not a Git repository
```

## Implementation Details

### Git Workflow

1. **Read current branch** - For restoration after analysis
2. **Get commit hashes** - Via `git log`
3. **For each commit**:
   - Checkout commit (read-only)
   - Scan for `.py` files
   - Analyze metrics
4. **Restore branch** - No history mutation

### Complexity Calculation

Uses Python's `ast` module for deterministic analysis:
- Parses each file into AST
- Visits function definitions
- Counts control flow statements
- Prevents nested function double-counting

### Performance

- Typical 10-commit analysis: < 2 seconds
- Scales linearly with commits and file count
- Memory-efficient streaming of file I/O

## Constraints & Compliance

✅ ONLY `.py` files analyzed  
✅ Third-party code excluded (.venv, site-packages)  
✅ Fully offline operation  
✅ Read-only Git access  
✅ Chronological commit processing (oldest → newest)  
✅ Per-commit snapshot semantics  
✅ Nested functions independent analysis  
✅ Clear error messages  

## Examples

### Analyze Current Project (Last 5 Commits)

```bash
python metrics_cli.py analyze --repo . --commits 5 --out ./metrics
```

### Analyze Remote Repository

```bash
git clone <repo_url> /tmp/myrepo
python metrics_cli.py analyze --repo /tmp/myrepo --commits 30 --out ./analysis
```

### Programmatic Usage

```python
from analyzer import analyze_repository
from report import write_summary_report
from charts import generate_code_trend_chart

# Analyze
metrics = analyze_repository("/path/to/repo", 20)

# Generate outputs
write_summary_report(metrics, "./output")
generate_code_trend_chart(metrics, "./output")

print("Analysis complete!")
```

## Requirements

- Python 3.10+
- matplotlib >= 3.10.9
- Git CLI
- Standard library (ast, json, subprocess, pathlib)

## License

This project is part of the Outlier Hackathon.
