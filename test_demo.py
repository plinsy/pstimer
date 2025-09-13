"""
Demo script showing pytest working with PSTimer.
"""

import subprocess
import sys


def run_single_test():
    """Run a single test to demonstrate pytest is working."""
    print("🧪 Running PSTimer Tests with pytest")
    print("=" * 50)

    # Run just the WCA compliance tests
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/test_wca_compliance.py::TestWCACompliance::test_3x3_valid_moves",
        "-v",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        print("STDOUT:")
        print(result.stdout)

        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        print(f"\nExit code: {result.returncode}")

        if result.returncode == 0:
            print("✅ Test passed! pytest is working correctly.")
        else:
            print("❌ Test failed, but pytest is running.")

    except subprocess.TimeoutExpired:
        print("⏰ Test timed out")
    except Exception as e:
        print(f"❌ Error running test: {e}")


if __name__ == "__main__":
    run_single_test()
