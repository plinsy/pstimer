#!/usr/bin/env python3
"""
Debug the R move specifically.
"""

from src.cube_visualization import CubeSimulator


def test_r_move_debug():
    """Test the R move in detail."""
    cube = CubeSimulator()

    # Apply the first 9 moves to get to the state before R move
    moves = ["U2", "R'", "L", "U2", "L", "R2", "D'", "B2", "L"]

    print("Applying first 9 moves:")
    for i, move in enumerate(moves):
        print(f"Move {i+1}: {move}")
        cube.execute_move(move)

    print("\nState before R move:")
    print_all_faces(cube)

    print(
        "\nExpected U face after R: [['W', 'W', 'Y'], ['W', 'W', 'Y'], ['R', 'W', 'O']]"
    )

    # Apply R move
    print("\nApplying R move...")
    cube.execute_move("R")

    print("\nActual state after R move:")
    print_all_faces(cube)

    print(f"\nActual U face: {cube.state['U']}")


def print_all_faces(cube):
    """Print all cube faces."""
    for face_name in ["U", "F", "R", "B", "L", "D"]:
        print(f"{face_name}: {cube.state[face_name]}")


def test_single_r_move():
    """Test R move on solved cube."""
    cube = CubeSimulator()

    print("Solved cube state:")
    print_all_faces(cube)

    print("\nApplying R move to solved cube...")
    cube.execute_move("R")

    print("\nAfter R move:")
    print_all_faces(cube)


if __name__ == "__main__":
    print("=== Testing R move on solved cube ===")
    test_single_r_move()

    print("\n=== Testing R move in scramble sequence ===")
    test_r_move_debug()
