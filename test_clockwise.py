#!/usr/bin/env python3

from src.cube_visualization import CubeSimulator


def test_clockwise_rotation():
    """Test that non-prime moves rotate faces clockwise"""
    cube = CubeSimulator()

    print("=== Testing clockwise face rotations ===")

    # Test U move - should rotate U face clockwise
    print("U face before U move:")
    print("Initial (should be all W): ", cube.state["U"])

    # Make U face distinguishable
    cube.state["U"] = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]

    print("Modified U face:", cube.state["U"])

    # Apply U move
    cube._move_u()
    print("After U move (should be 90° clockwise):")
    print(cube.state["U"])
    print("Expected: [['7', '4', '1'], ['8', '5', '2'], ['9', '6', '3']]")
    print()

    # Test that U' reverses it
    cube._move_u_prime()
    print("After U' (should return to original):")
    print(cube.state["U"])
    print("Expected: [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]")


if __name__ == "__main__":
    test_clockwise_rotation()
