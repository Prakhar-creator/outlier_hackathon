#!/bin/bash
set -e

echo "===================================="
echo "Python Repository Metrics CLI"
echo "===================================="
echo ""

# Check if we're in Docker or local environment
if [ -f "/.dockerenv" ]; then
    echo "Running in Docker container"
    PYTHON_CMD="python"
else
    echo "Running in local environment"
    if [ -d ".venv" ]; then
        source .venv/bin/activate
    fi
    PYTHON_CMD="python"
fi

# Run tests if requested
if [ "$1" = "test" ]; then
    echo "Running tests..."
    if [ -d "tests" ]; then
        $PYTHON_CMD -m pytest tests/ -v
    else
        echo "No tests directory found"
        exit 1
    fi
    exit $?
fi

# Run CLI analysis if arguments provided
if [ $# -gt 0 ]; then
    $PYTHON_CMD metrics_cli.py "$@"
    exit $?
fi

# Show help by default
$PYTHON_CMD metrics_cli.py --help
