#!/usr/bin/env python3
"""
Test the cube simulation functionality.
"""

from src.cube_visualization import CubeSimulator


def test_cube_moves():
    """Test basic cube moves."""
    cube = CubeSimulator()

    print("Initial solved state:")
    print_cube_state(cube)

    # Test U move
    cube.execute_move("U")
    print("\nAfter U move:")
    print_cube_state(cube)

    # Test U' (undo)
    cube.execute_move("U'")
    print("\nAfter U' move (should be back to solved):")
    print_cube_state(cube)

    # Test a simple scramble
    cube.reset_to_solved()
    cube.apply_scramble("R U R' U'")
    print("\nAfter scramble 'R U R' U'':")
    print_cube_state(cube)


def print_cube_state(cube):
    """Print the cube state in a readable format."""
    for face_name, face_state in cube.state.items():
        print(f"{face_name}: {face_state}")


if __name__ == "__main__":
    test_cube_moves()
