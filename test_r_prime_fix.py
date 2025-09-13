#!/usr/bin/env python3
"""
Test the corrected R' move specifically.
"""

from src.cube_visualization import CubeSimulator


def test_r_prime_specific():
    """Test R' move specifically after U2."""
    cube = CubeSimulator()

    print("Testing R' move after U2:")
    print("Initial solved state:")
    print(f"U: {cube.state['U']}")

    # Apply U2
    cube.execute_move("U2")
    print(f"After U2: {cube.state['U']}")

    # Apply R'
    cube.execute_move("R'")
    print(f"After R': {cube.state['U']}")

    expected = [["W", "W", "B"], ["W", "W", "B"], ["W", "W", "G"]]
    print(f"Expected: {expected}")

    if cube.state["U"] == expected:
        print("✓ R' move is correct!")
    else:
        print("✗ R' move is still incorrect")


def test_r_and_r_prime():
    """Test that R and R' are inverses."""
    cube = CubeSimulator()

    print("\nTesting R and R' are inverses:")
    original_state = {face: [row[:] for row in cube.state[face]] for face in cube.state}

    # Apply R then R'
    cube.execute_move("R")
    cube.execute_move("R'")

    # Check if back to original
    is_same = True
    for face in cube.state:
        if cube.state[face] != original_state[face]:
            is_same = False
            break

    if is_same:
        print("✓ R followed by R' returns to solved state")
    else:
        print("✗ R followed by R' does not return to solved state")
        print("Current U face:", cube.state["U"])
        print("Original U face:", original_state["U"])


if __name__ == "__main__":
    test_r_prime_specific()
    test_r_and_r_prime()
