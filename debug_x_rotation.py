"""
Debug the x rotation logic step by step.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.cube_visualization import CubeSimulator


def debug_x_rotation_step_by_step():
    """Debug what the x rotation should actually do."""
    print("DEBUGGING X ROTATION LOGIC")
    print("=" * 40)

    print("Initial state:")
    print("- White (W) on top (U)")
    print("- Green (G) in front (F)")
    print("- Red (R) on right (R)")
    print("- Orange (O) on left (L)")
    print("- Blue (B) in back (B)")
    print("- Yellow (Y) on bottom (D)")

    print("\nAfter x rotation, we want:")
    print("- Blue (B) to be what we see in front")
    print("- This means Blue should move from back (B) to front (F)")

    print("\nThinking about the x rotation around the R-L axis:")
    print("- If we're looking at the cube from the front...")
    print("- x rotation turns the cube 'forward' around the left-right axis")
    print("- The front face (Green) should go DOWN")
    print("- The top face (White) should come to the FRONT")
    print("- The back face (Blue) should come to the TOP")
    print("- The bottom face (Yellow) should go to the BACK")

    print("\nSo the cycle should be:")
    print("F -> D, U -> F, B -> U, D -> B")
    print("Green -> Down, White -> Front, Blue -> Top, Yellow -> Back")

    print("\nBut we want Blue in front, not Blue on top...")
    print("Let me reconsider...")

    print("\nActually, if Blue should be 'what I see' after x rotation:")
    print("Then x rotation should bring Back to Front position")
    print("This means: B -> F")

    print("\nIf B goes to F, then following the cycle:")
    print("B -> F (Blue to Front)")
    print("F -> D (Green to Down)")
    print("D -> B (Yellow to Back)")
    print("U -> ... where does Up go?")

    print("\nLet me think of this as rotating around the R-L axis...")
    print("Imagine looking from the Right side of the cube:")
    print("- Front face rotates down")
    print("- Bottom face rotates to back")
    print("- Back face rotates up")
    print("- Top face rotates to front")

    print("\nSo: F->D, D->B, B->U, U->F")
    print("But we want Blue (back) to end up in front...")
    print("That means we need: B->F")
    print("Which requires the reverse cycle: F->U, U->B, B->D, D->F")


if __name__ == "__main__":
    debug_x_rotation_step_by_step()
