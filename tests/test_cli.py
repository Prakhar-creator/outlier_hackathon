import os
import subprocess
import sys
import tempfile
import textwrap


def git(cmd, cwd):
    subprocess.run(
        ["git"] + cmd,
        cwd=cwd,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def write_file(path, content):
    with open(path, "w") as f:
        f.write(textwrap.dedent(content))


def test_cli_creates_reports_and_charts():
    # This assertion FAILS cleanly before code injection
    assert os.path.exists("metrics_cli.py"), "metrics_cli.py must exist at repo root"

    with tempfile.TemporaryDirectory() as repo, tempfile.TemporaryDirectory() as out:
        git(["init"], cwd=repo)

        write_file(
            os.path.join(repo, "a.py"),
            """
            def foo():
                return 1
            """
        )

        git(["add", "."], cwd=repo)
        git(["commit", "-m", "initial commit"], cwd=repo)

        result = subprocess.run(
            [
                sys.executable,
                "metrics_cli.py",
                "analyze",
                "--repo",
                repo,
                "--commits",
                "1",
                "--out",
                out,
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

        summary_path = os.path.join(out, "summary.json")
        chart_path = os.path.join(out, "code_lines_trend.png")

        assert os.path.exists(summary_path), "summary.json must be generated"
        assert os.path.exists(chart_path), "code_lines_trend.png must be generated"