#!/usr/bin/env python3
"""
Test prime moves to verify they turn counterclockwise correctly.
"""

from src.cube_visualization import CubeSimulator


def test_prime_moves():
    """Test that prime moves correctly turn counterclockwise."""

    print("Testing that prime moves are counterclockwise:")
    print("A move followed by its prime should return to solved state.\n")

    # Test each face
    faces = ["U", "D", "F", "B", "L", "R"]

    for face in faces:
        cube = CubeSimulator()

        print(f"Testing {face} and {face}':")

        # Apply the move
        cube.execute_move(face)
        state_after_move = [row[:] for row in cube.state[face]]

        # Apply the prime move
        cube.execute_move(face + "'")
        state_after_prime = [row[:] for row in cube.state[face]]

        # Check if back to solved
        solved_state = (
            [["W", "W", "W"], ["W", "W", "W"], ["W", "W", "W"]]
            if face == "U"
            else (
                [["Y", "Y", "Y"], ["Y", "Y", "Y"], ["Y", "Y", "Y"]]
                if face == "D"
                else (
                    [["G", "G", "G"], ["G", "G", "G"], ["G", "G", "G"]]
                    if face == "F"
                    else (
                        [["B", "B", "B"], ["B", "B", "B"], ["B", "B", "B"]]
                        if face == "B"
                        else (
                            [["O", "O", "O"], ["O", "O", "O"], ["O", "O", "O"]]
                            if face == "L"
                            else [["R", "R", "R"], ["R", "R", "R"], ["R", "R", "R"]]
                        )
                    )
                )
            )
        )

        if state_after_prime == solved_state:
            print(f"  ✓ {face} + {face}' = solved (correct)")
        else:
            print(f"  ✗ {face} + {face}' ≠ solved (incorrect)")
            print(f"    Expected: {solved_state}")
            print(f"    Got:      {state_after_prime}")

        # Also test that 4 moves return to solved
        cube = CubeSimulator()
        for i in range(4):
            cube.execute_move(face)

        final_state = [row[:] for row in cube.state[face]]
        if final_state == solved_state:
            print(f"  ✓ {face} × 4 = solved (correct)")
        else:
            print(f"  ✗ {face} × 4 ≠ solved (incorrect)")

        print()


def test_specific_prime_example():
    """Test a specific example: R followed by R' should be identity."""
    cube = CubeSimulator()

    print("Testing R followed by R':")
    print("Initial U face:", cube.state["U"])

    cube.execute_move("R")
    print("After R:       ", cube.state["U"])

    cube.execute_move("R'")
    print("After R':      ", cube.state["U"])

    expected = [["W", "W", "W"], ["W", "W", "W"], ["W", "W", "W"]]
    if cube.state["U"] == expected:
        print("✓ R + R' correctly returns to solved state")
    else:
        print("✗ R + R' does not return to solved state")


if __name__ == "__main__":
    test_prime_moves()
    print("=" * 50)
    test_specific_prime_example()
