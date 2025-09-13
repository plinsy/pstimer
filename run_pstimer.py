#!/usr/bin/env python
"""
PSTimer launcher that handles Tcl/Tk compatibility issues.
This script ensures PSTimer runs with a compatible Python/Tcl configuration.
"""
import sys
import os
import subprocess


def main():
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )

    if in_venv:
        print(f"Virtual environment detected: {sys.prefix}")
        print(f"Python version: {sys.version}")

    # Try to import tkinter to test compatibility
    try:
        import tkinter as tk

        # Try to create a window to test Tcl/Tk
        root = tk.Tk()
        root.withdraw()  # Hide the window immediately
        root.destroy()
        print("Tkinter test successful - launching PSTimer...")

        # Import and run PSTimer using the main module
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.join(script_dir, "main.py")

        # Execute main.py in this process
        with open(main_path, "r") as f:
            code = f.read()
        exec(code, {"__name__": "__main__", "__file__": main_path})

    except Exception as e:
        print(f"Tkinter test failed: {e}")
        print("\nTrying to launch with system Python...")

        # Get the current script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_py = os.path.join(script_dir, "main.py")

        # Try to run with system python
        try:
            # On Windows, try common system Python locations
            system_pythons = [
                "python",  # Usually works if Python is in PATH
                "py",  # Python launcher
                "py -3.12",  # Specific version
            ]

            for python_cmd in system_pythons:
                try:
                    print(f"Trying: {python_cmd}")
                    result = subprocess.run(
                        f"{python_cmd} {main_py}",
                        shell=True,
                        check=True,
                        cwd=script_dir,
                    )
                    return  # Success!
                except subprocess.CalledProcessError:
                    continue

        except Exception as fallback_error:
            print(f"All fallback attempts failed: {fallback_error}")
            print("\nPlease try one of these solutions:")
            print("1. Reinstall Python 3.13 with Tcl/Tk support")
            print("2. Use system Python: python main.py")
            print("3. Create a new virtual environment with Python 3.12")
            sys.exit(1)


if __name__ == "__main__":
    main()
