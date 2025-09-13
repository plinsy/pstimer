"""
Work backwards from the desired results to implement correct rotations.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.cube_visualization import CubeSimulator


def analyze_desired_results():
    """Analyze what each rotation should achieve."""
    print("DESIRED ROTATION RESULTS")
    print("=" * 40)

    print("Initial: W=top, G=front, R=right, O=left, B=back, Y=down")
    print()

    print("After x:  Blue (B) should be front")
    print("  - B (back) -> F (front)")
    print("  - Need to figure out where other faces go")
    print()

    print("After x': Green (G) should be top")
    print("  - G (front) -> U (top)")
    print("  - This is the inverse of x")
    print()

    print("After z:  Orange (O) should be top")
    print("  - O (left) -> U (top)")
    print()

    print("After z': Red (R) should be top")
    print("  - R (right) -> U (top)")
    print("  - This is the inverse of z")
    print()

    print("After z2: Yellow (Y) should be top")
    print("  - Y (down) -> U (top)")
    print("  - This should be two z rotations")


def design_correct_rotations():
    """Design the correct rotation mappings."""
    print("\n" + "=" * 40)
    print("DESIGNING CORRECT ROTATIONS")
    print("=" * 40)

    print("For x rotation (Blue -> Front):")
    print("  If B -> F, and it's a rotation around R-L axis...")
    print("  Then the other faces in that plane must also rotate:")
    print("  B -> F (back to front)")
    print("  F -> D (front to down)")
    print("  D -> B (down to back)")
    print("  U -> F? No wait... we need to think about this as a true rotation")
    print()

    print("Let me think of this as physically rotating the cube:")
    print("  x rotation = rotate around the right-left axis")
    print("  If I want the back to come to the front...")
    print("  I need to rotate the cube 'backwards' towards me")
    print()

    print("Standard x rotation in speedcubing:")
    print("  x = R M' L'")
    print("  This rotates: F->D, U->F, B->U, D->B")
    print("  But that puts B->U (Blue to top)")
    print()

    print("We want Blue to front, so we need:")
    print("  B->F, which means we want: F->U, U->B, B->D, D->F")
    print("  This is x' (x-prime), not x!")
    print()

    print("So our mapping should be:")
    print("  User's 'x' should actually execute speedcubing 'x''")
    print("  User's 'x'' should actually execute speedcubing 'x'")


if __name__ == "__main__":
    analyze_desired_results()
    design_correct_rotations()
