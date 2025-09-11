#!/usr/bin/env python3
"""
PSTimer - A modern speedcubing timer inspired by csTimer.

Features:
- csTimer-inspired UI layout
- Multiple puzzle support (3x3, 2x2, 4x4, etc.)
- Advanced statistics (mo3, ao5, ao12, ao100)
- Session management
- 3D cube visualization
- Multiple themes
- Keyboard controls (Space, S, R)

To run:
    python main.py
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.ui import PSTimerUI


def main():
    """Main entry point for PSTimer."""
    try:
        app = PSTimerUI()
        app.mainloop()
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error starting PSTimer: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
