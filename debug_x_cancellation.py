"""
Debug the x x' cancellation issue.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.cube_visualization import CubeSimulator


def debug_x_cancellation():
    """Debug why x x' doesn't cancel perfectly."""
    print("DEBUGGING X X' CANCELLATION")
    print("=" * 40)

    cube = CubeSimulator()
    print("Initial state:")
    for face in ["U", "F", "R", "L", "B", "D"]:
        print(f"  {face}: {cube.state[face]}")

    initial_state = {face: [row[:] for row in cube.state[face]] for face in cube.state}

    print("\nAfter x:")
    cube.execute_move("x")
    for face in ["U", "F", "R", "L", "B", "D"]:
        print(f"  {face}: {cube.state[face]}")

    print("\nAfter x x':")
    cube.execute_move("x'")
    for face in ["U", "F", "R", "L", "B", "D"]:
        print(f"  {face}: {cube.state[face]}")

    print("\nComparison with initial:")
    all_match = True
    for face in ["U", "F", "R", "L", "B", "D"]:
        if cube.state[face] != initial_state[face]:
            print(f"  {face}: MISMATCH")
            print(f"    Initial: {initial_state[face]}")
            print(f"    Final:   {cube.state[face]}")
            all_match = False
        else:
            print(f"  {face}: MATCH")

    if all_match:
        print("\n✓ Perfect cancellation!")
    else:
        print("\n✗ Imperfect cancellation - likely face rotation issue")


if __name__ == "__main__":
    debug_x_cancellation()
