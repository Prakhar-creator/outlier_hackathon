Title
Python Repository Metrics CLI with Git History Trends

Description / Context
Build a command‑line tool that analyzes a local Python Git repository and produces objective, offline metrics about code size and complexity over time.
The tool MUST:

Analyze only Python source files
Run fully offline
Require no external services or APIs
Work against the local Git history of the repository

The tool is intended for engineering managers and architects to understand:

Codebase size growth
Comment coverage
Cyclomatic complexity trends
Evolution of these metrics across commits


Tech Stack

Language: Python 3.10+
Git access: local git CLI
Parsing: Python ast module
Charts: matplotlib
Output formats: JSON + PNG
Execution: CLI tool


Scope Constraints (Mandatory)

ONLY .py files are analyzed
Files inside .git/ are ignored
Third‑party vendored code (e.g. .venv/, site-packages/) MUST be ignored
Analysis is performed on the current branch only
All metrics are computed per commit snapshot, not incrementally


Metric Definitions (Deterministic Rules)
Line Classification (Python)
Each line is classified using the following rules after stripping whitespace:

Blank line: empty or whitespace‑only
Comment line: starts with #
Code line: any other non‑blank line

Inline comments MUST count as code lines, not comment lines.

File Count

A file is counted if it has extension .py
File count is reported per commit


Cyclomatic Complexity (Python Only)
Cyclomatic complexity MUST be calculated per function using the Python AST.
Each function:

Starts with base complexity = 1
+1 for each occurrence of:

if, elif
for, while
and, or
except
conditional expressions (x if y else z)


Nested functions are analyzed independently

Module‑level code is ignored for complexity purposes.

Git History Analysis

The tool MUST analyze the last N commits on the current branch
Commits MUST be processed in chronological order (oldest → newest)
Default: N = 10
Git checkout MUST be read‑only (no mutation of history)

If Git is unavailable or the directory is not a repository, the tool MUST exit with a clear error message.

Output Artifacts
Summary Report (JSON)
The tool MUST generate a JSON summary containing:

Repository path
Commit hash list (oldest → newest)
Per‑commit metrics:

total files
total code lines
total comment lines
total blank lines
average cyclomatic complexity
maximum cyclomatic complexity




Trend Charts (PNG)
The tool MUST generate at least one PNG chart:

X‑axis: commit order
Y‑axis: total code lines
Filename: code_lines_trend.png

Charts MUST be written to an output directory.

CLI Behavior
The tool MUST be executed via:
Shellpython metrics_cli.py analyze --repo <path> --commits <N> --out <output_dir>Show more lines

--repo: path to Git repository
--commits: optional, default = 10
--out: output directory (created if missing)


Expected Interface (TEST‑CRITICAL)
Repository Analyzer

Path: analyzer.py
Name: analyze_repository
Type: Function
Input:

repo_path: str
num_commits: int


Output:
PythondictShow more lines

Description:
Analyzes the last num_commits commits and returns structured metrics per commit. Tests verify metric correctness on a controlled repo.


Complexity Analyzer

Path: complexity.py
Name: compute_function_complexities
Type: Function
Input:

source_code: str


Output:
Pythonlist[int]Show more lines

Description:
Returns cyclomatic complexity values for each function in the given Python source. Tests verify AST correctness.


Report Writer

Path: report.py
Name: write_summary_report
Type: Function
Input:

metrics: dict
output_dir: str


Output:

summary.json written to disk


Description:
Serializes metrics into deterministic JSON.


Chart Generator

Path: charts.py
Name: generate_code_trend_chart
Type: Function
Input:

metrics: dict
output_dir: str


Output:

code_lines_trend.png


Description:
Generates a PNG chart of code lines over commit history.


CLI Entry Point

Path: metrics_cli.py
Name: CLI main
Type: CLI entry point
Description:
Parses arguments, invokes analysis, writes reports and charts.