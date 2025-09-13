"""
Test runner script for PSTimer using pytest.

This script provides an easy way to run tests with different configurations.
"""

import subprocess
import sys
import os


def run_tests(test_type="all", verbose=True, coverage=False):
    """
    Run PSTimer tests using pytest.
    
    Args:
        test_type: Type of tests to run ("all", "wca", "unit", "integration")
        verbose: Whether to run in verbose mode
        coverage: Whether to include coverage reporting
    """
    
    cmd = [sys.executable, "-m", "pytest"]
    
    # Add verbosity
    if verbose:
        cmd.append("-v")
    
    # Add coverage if requested
    if coverage:
        cmd.extend(["--cov=src", "--cov-report=html", "--cov-report=term"])
    
    # Select test type
    if test_type == "wca":
        cmd.extend(["-m", "wca"])
    elif test_type == "unit":
        cmd.extend(["-m", "not integration"])
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
    elif test_type == "fast":
        cmd.extend(["-m", "not slow"])
    
    # Add test directory
    cmd.append("tests/")
    
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=os.path.dirname(__file__))
    return result.returncode


def main():
    """Main test runner entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="PSTimer Test Runner")
    parser.add_argument(
        "--type", 
        choices=["all", "wca", "unit", "integration", "fast"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--coverage", 
        action="store_true",
        help="Include coverage reporting"
    )
    parser.add_argument(
        "--quiet", 
        action="store_true",
        help="Run in quiet mode"
    )
    
    args = parser.parse_args()
    
    return run_tests(
        test_type=args.type,
        verbose=not args.quiet,
        coverage=args.coverage
    )


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
