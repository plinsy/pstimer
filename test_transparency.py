#!/usr/bin/env python3
"""
Test script for transparency functionality.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.ui import PSTimerUI
import time


def test_transparency():
    """Test transparency functionality."""
    print("Testing PSTimer transparency features...")

    # Create the UI
    app = PSTimerUI()

    # Test initial transparency
    print(f"Initial transparency: {app.transparency}")
    assert app.transparency == 1.0, "Initial transparency should be 1.0"

    # Test transparency adjustment
    app._adjust_transparency(-0.2)
    print(f"Transparency after -0.2 adjustment: {app.transparency}")
    assert app.transparency == 0.8, "Transparency should be 0.8"

    # Test minimum transparency boundary
    app._adjust_transparency(-1.0)
    print(f"Transparency after large negative adjustment: {app.transparency}")
    assert app.transparency == 0.3, "Transparency should not go below 0.3"

    # Test maximum transparency boundary
    app._adjust_transparency(1.0)
    print(f"Transparency after large positive adjustment: {app.transparency}")
    assert app.transparency == 1.0, "Transparency should not go above 1.0"

    # Test reset transparency
    app._adjust_transparency(-0.5)  # Set to 0.5
    app._reset_transparency()
    print(f"Transparency after reset: {app.transparency}")
    assert app.transparency == 1.0, "Reset should set transparency to 1.0"

    # Clean up
    app.destroy()

    print("✅ All transparency tests passed!")


if __name__ == "__main__":
    test_transparency()
