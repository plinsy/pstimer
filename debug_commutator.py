"""
Debug the commutator issue to understand why R U R' U' returns to identity.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.cube_visualization import CubeSimulator


def debug_commutator():
    """Debug the R U R' U' sequence."""
    print("DEBUGGING R U R' U' COMMUTATOR")
    print("=" * 40)

    cube = CubeSimulator()

    def print_cube_state(label):
        print(f"\n{label}:")
        for face_name in ["U", "F", "R", "B", "L", "D"]:
            print(f"  {face_name}: {cube.state[face_name]}")

    print_cube_state("Initial state")
    initial_state = {}
    for face in cube.state:
        initial_state[face] = [row[:] for row in cube.state[face]]  # Deep copy

    # Apply R
    cube.execute_move("R")
    print_cube_state("After R")

    # Apply U
    cube.execute_move("U")
    print_cube_state("After R U")

    # Apply R'
    cube.execute_move("R'")
    print_cube_state("After R U R'")

    # Apply U'
    cube.execute_move("U'")
    print_cube_state("After R U R' U'")

    # Check if it's back to initial
    if cube.state == initial_state:
        print("\n❌ PROBLEM: R U R' U' returned to solved state!")
        print("This should NOT happen - it indicates an issue with the moves.")
    else:
        print("\n✅ GOOD: R U R' U' did not return to solved state.")
        print("This is the expected behavior.")

        # Let's see what changed
        changed_faces = []
        for face in ["U", "F", "R", "B", "L", "D"]:
            if cube.state[face] != initial_state[face]:
                changed_faces.append(face)

        print(f"Changed faces: {changed_faces}")


def test_individual_moves():
    """Test each move individually to see if they're working."""
    print("\n" + "=" * 40)
    print("TESTING INDIVIDUAL MOVES")
    print("=" * 40)

    moves = ["R", "U", "R'", "U'"]

    for move in moves:
        cube = CubeSimulator()
        initial = {}
        for face in cube.state:
            initial[face] = [row[:] for row in cube.state[face]]  # Deep copy

        cube.execute_move(move)

        if cube.state == initial:
            print(f"❌ {move} does nothing!")
        else:
            print(f"✅ {move} changes the cube")
            # Show what changed
            for face in ["U", "F", "R", "B", "L", "D"]:
                if cube.state[face] != initial[face]:
                    print(f"  {face} changed: {initial[face]} -> {cube.state[face]}")


if __name__ == "__main__":
    debug_commutator()
    test_individual_moves()
