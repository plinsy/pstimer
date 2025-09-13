"""
Debug x rotation by tracing exactly what should happen.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.cube_visualization import CubeSimulator


def trace_x_rotation():
    """Trace what should happen in x rotation step by step."""
    print("TRACING X ROTATION")
    print("=" * 30)

    cube = CubeSimulator()
    print("Initial state:")
    print(f"  U (top): {cube.state['U'][1][1]} (White)")
    print(f"  F (front): {cube.state['F'][1][1]} (Green)")
    print(f"  R (right): {cube.state['R'][1][1]} (Red)")
    print(f"  L (left): {cube.state['L'][1][1]} (Orange)")
    print(f"  B (back): {cube.state['B'][1][1]} (Blue)")
    print(f"  D (down): {cube.state['D'][1][1]} (Yellow)")

    print("\nAfter x rotation, we want Blue to be front.")
    print("So: Blue (currently in B position) should move to F position")
    print("This means: B -> F")

    print("\nIf we rotate around the R-L axis (x rotation):")
    print("The R and L faces stay in place (they just rotate)")
    print("The other 4 faces (U, F, D, B) cycle around")

    print("\nFor Blue to end up in front position:")
    print("We need: B -> F")
    print("If B -> F, then where do the others go?")

    print("\nLet's think of it as a 4-cycle in the order they appear around the axis:")
    print("Looking from the right side: U (top), F (front), D (bottom), B (back)")
    print("For B to go to F position, we need 2 steps in the cycle:")
    print("  U -> B (2 steps counter-clockwise)")
    print("  F -> U (2 steps counter-clockwise)")
    print("  D -> F (2 steps counter-clockwise)")
    print("  B -> D (2 steps counter-clockwise)")

    print("\nWait, that's not right. Let me think of actual cube rotation...")

    print("\nIf I physically hold the cube and rotate it around the R-L axis")
    print("such that the back face comes to the front:")
    print("- The back face (Blue) goes to front")
    print("- The front face (Green) goes to bottom")
    print("- The bottom face (Yellow) goes to back")
    print("- The top face (White) goes to top... no wait")

    print("\nLet me try a different approach...")
    print("If B -> F (Blue back to front)")
    print("And this is a rotation, then it's a 90° rotation")
    print("So the cycle should be: B -> F -> ? -> ? -> B")

    print("\nActually, let me test what our current implementation does:")
    cube.execute_move("x")
    print(f"\nAfter our x implementation:")
    print(f"  U (top): {cube.state['U'][1][1]}")
    print(f"  F (front): {cube.state['F'][1][1]}")
    print(f"  R (right): {cube.state['R'][1][1]}")
    print(f"  L (left): {cube.state['L'][1][1]}")
    print(f"  B (back): {cube.state['B'][1][1]}")
    print(f"  D (down): {cube.state['D'][1][1]}")

    print("\nWe get Yellow (Y) in front, but we want Blue (B) in front")
    print("Our current cycle is: F->U, U->B, B->D, D->F")
    print("This puts: Green->top, White->back, Blue->bottom, Yellow->front")

    print("\nBut we want Blue in front!")
    print("So we need Blue to move from back to front")
    print("That means: B -> F")
    print("If B->F, and it's one step in a 4-cycle:")
    print("Then: U->D, F->U, D->B, B->F")
    print("Or: U->F, F->D, D->B, B->U")

    print("\nLet me try: B->F, F->D, D->B, U->? - this is only 3 in the cycle")
    print("The 4-cycle must be: B->F, F->D, D->B, B->U... no that's wrong")
    print("Try: B->F, U->B, F->D, D->U")


if __name__ == "__main__":
    trace_x_rotation()
