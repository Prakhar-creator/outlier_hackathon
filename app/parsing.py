#!/usr/bin/env python
"""
Parsing and validation script for the Python Repository Metrics CLI.

This script validates the implementation and runs all tests to ensure
the application is functioning correctly.
"""

import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime


def run_tests() -> dict:
    """
    Run the test suite and collect results.
    
    Returns:
        Dictionary with test results
    """
    print("=" * 60)
    print("RUNNING TEST SUITE")
    print("=" * 60)
    print()
    
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        capture_output=False,
        text=True,
    )
    
    return {
        "returncode": result.returncode,
        "status": "PASSED" if result.returncode == 0 else "FAILED",
    }


def validate_modules() -> dict:
    """
    Validate that all required modules can be imported.
    
    Returns:
        Dictionary with validation results
    """
    print()
    print("=" * 60)
    print("MODULE VALIDATION")
    print("=" * 60)
    print()
    
    required_modules = {
        "complexity": "compute_function_complexities",
        "analyzer": "analyze_repository",
        "report": "write_summary_report",
        "charts": "generate_code_trend_chart",
    }
    
    all_valid = True
    results = {}
    
    for module_name, function_name in required_modules.items():
        try:
            module = __import__(module_name)
            func = getattr(module, function_name)
            print(f"✅ {module_name:20} → {function_name}")
            results[module_name] = "PASS"
        except Exception as e:
            print(f"❌ {module_name:20} → {function_name} (ERROR: {e})")
            results[module_name] = "FAIL"
            all_valid = False
    
    return {
        "all_valid": all_valid,
        "modules": results,
    }


def check_cli() -> dict:
    """
    Check that the CLI is functional.
    
    Returns:
        Dictionary with CLI check results
    """
    print()
    print("=" * 60)
    print("CLI VALIDATION")
    print("=" * 60)
    print()
    
    result = subprocess.run(
        [sys.executable, "metrics_cli.py", "--help"],
        capture_output=True,
        text=True,
    )
    
    cli_valid = result.returncode == 0
    status = "PASS" if cli_valid else "FAIL"
    print(f"✅ CLI Help: {status}")
    
    return {
        "cli_valid": cli_valid,
        "status": status,
    }


def generate_report(test_result: dict, module_validation: dict, cli_check: dict) -> dict:
    """
    Generate final validation report.
    
    Returns:
        Dictionary with final report
    """
    all_passed = (
        test_result["returncode"] == 0 and
        module_validation["all_valid"] and
        cli_check["cli_valid"]
    )
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "status": "SUCCESS" if all_passed else "FAILURE",
        "tests": test_result,
        "modules": module_validation,
        "cli": cli_check,
        "overall": "ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED",
    }
    
    return report


def main():
    """Main validation script."""
    print()
    print("╔" + "=" * 58 + "╗")
    print("║" + " PYTHON REPOSITORY METRICS CLI - VALIDATION ".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Run validations
    test_result = run_tests()
    module_validation = validate_modules()
    cli_check = check_cli()
    
    # Generate report
    report = generate_report(test_result, module_validation, cli_check)
    
    # Print summary
    print()
    print("=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Status: {report['status']}")
    print(f"Overall: {report['overall']}")
    print(f"Timestamp: {report['timestamp']}")
    print()
    
    # Return appropriate exit code
    if report['status'] == 'SUCCESS':
        print("✅ ALL VALIDATIONS PASSED")
        return 0
    else:
        print("❌ SOME VALIDATIONS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
