#!/usr/bin/env python3
"""
Test script for compact mode functionality.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.ui import PSTimerUI
import time


def test_compact_mode():
    """Test compact mode functionality."""
    print("Testing PSTimer compact mode features...")

    # Create the UI
    app = PSTimerUI()

    # Test initial state
    print(f"Initial compact mode state: {app.is_compact_mode}")
    assert app.is_compact_mode == False, "Should start in normal mode"

    print(f"Initial compact position: {app.compact_position}")
    assert app.compact_position == "top-right", "Default position should be top-right"

    # Test position setting
    app._set_compact_position("bottom-left")
    print(f"Position after setting to bottom-left: {app.compact_position}")
    assert app.compact_position == "bottom-left", "Position should be updated"

    # Test entering compact mode
    print("Testing compact mode entry...")
    original_children_count = len(app.winfo_children())
    app._enter_compact_mode()

    print(f"Compact mode state after entering: {app.is_compact_mode}")
    assert app.is_compact_mode == True, "Should be in compact mode"

    print(f"Window geometry in compact mode: {app.geometry()}")
    # Verify compact widgets exist
    assert len(app.compact_widgets) > 0, "Should have compact widgets"
    assert "timer" in app.compact_widgets, "Should have timer widget"
    assert "scramble" in app.compact_widgets, "Should have scramble widget"

    # Test exiting compact mode
    print("Testing compact mode exit...")
    app._exit_compact_mode()

    print(f"Compact mode state after exiting: {app.is_compact_mode}")
    assert app.is_compact_mode == False, "Should be back in normal mode"

    print(f"Compact widgets after exit: {len(app.compact_widgets)}")
    assert len(app.compact_widgets) == 0, "Compact widgets should be cleared"

    # Test toggle function
    print("Testing compact mode toggle...")
    app._toggle_compact_mode()  # Should enter
    assert app.is_compact_mode == True, "Toggle should enter compact mode"

    app._toggle_compact_mode()  # Should exit
    assert app.is_compact_mode == False, "Toggle should exit compact mode"

    # Clean up
    app.destroy()

    print("✅ All compact mode tests passed!")


if __name__ == "__main__":
    test_compact_mode()
