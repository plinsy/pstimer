"""
Test file to verify cube moves produce expected results as specified in test-moves.prompt.md
This tests each individual move to ensure the cube simulation matches WCA standards.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.cube_visualization import CubeSimulator


def print_face_state(face_state, face_name):
    """Helper to print face state in readable format."""
    print(f"{face_name} Face: {face_state}")


def test_single_move(move, expected_white_face, description=""):
    """Test a single move and verify the white face (U) matches expected result."""
    print(f"\n--- Testing {move} move {description} ---")

    # Create fresh cube
    cube = CubeSimulator()

    # Print initial state (observe white face as the test does)
    print(f"Initial (White Face): {cube.state['U']}")

    # Execute the move
    cube.execute_move(move)

    # Print result (observe white face)
    print(f"After {move}: {cube.state['U']}")
    print(f"Expected: {expected_white_face}")

    # Verify result
    if cube.state["U"] == expected_white_face:
        print(f"✓ PASS: {move} move produces correct result")
        return True
    else:
        print(f"✗ FAIL: {move} move does not match expected result")
        print(f"  Expected: {expected_white_face}")
        print(f"  Got:      {cube.state['U']}")
        return False


def test_move_with_custom_front(
    move, initial_green_face, expected_green_face, description=""
):
    """Test a move with green front face and observe the green face results."""
    print(f"\n--- Testing {move} move {description} ---")

    # Create fresh cube and verify green front face
    cube = CubeSimulator()
    # For green front face tests, we observe the F face (which is green)
    # Set the front face to match initial expectation (it should already be green)

    # Print initial state
    print(f"Initial (Front Face {description}): {cube.state['F']}")

    # Execute the move
    cube.execute_move(move)

    # Print result - for U and D moves with green front, we check effect on green face
    print(f"After {move}: {cube.state['F']}")
    print(f"Expected: {expected_green_face}")

    # Verify result
    if cube.state["F"] == expected_green_face:
        print(f"✓ PASS: {move} move produces correct result")
        return True
    else:
        print(f"✗ FAIL: {move} move does not match expected result")
        print(f"  Expected: {expected_green_face}")
        print(f"  Got:      {cube.state['F']}")
        return False


def run_all_move_tests():
    """Run all move tests as specified in the prompt."""
    print("PSTimer Cube Move Verification Tests")
    print("=" * 50)

    tests_passed = 0
    total_tests = 0

    # Test cases from the prompt (observing WHITE face for most moves)
    # These moves affect the white face when viewing it as the "front"
    white_face_test_cases = [
        # F and F' moves - affect bottom row of white face
        ("F", [["W", "W", "W"], ["W", "W", "W"], ["O", "O", "O"]], ""),
        ("F'", [["W", "W", "W"], ["W", "W", "W"], ["R", "R", "R"]], ""),
        # B and B' moves - affect top row of white face
        ("B", [["R", "R", "R"], ["W", "W", "W"], ["W", "W", "W"]], ""),
        ("B'", [["O", "O", "O"], ["W", "W", "W"], ["W", "W", "W"]], ""),
        # R and R' moves - affect right column of white face
        ("R", [["W", "W", "G"], ["W", "W", "G"], ["W", "W", "G"]], ""),
        ("R'", [["W", "W", "B"], ["W", "W", "B"], ["W", "W", "B"]], ""),
        # L and L' moves - affect left column of white face
        ("L", [["B", "W", "W"], ["B", "W", "W"], ["B", "W", "W"]], ""),
        ("L'", [["G", "W", "W"], ["G", "W", "W"], ["G", "W", "W"]], ""),
    ]

    # Run white face observation tests
    for move, expected, description in white_face_test_cases:
        total_tests += 1
        if test_single_move(move, expected, description):
            tests_passed += 1

    # Test cases with Green front face - these observe the GREEN face (F)
    # U and D moves affect the green front face when it's the front
    green_front_test_cases = [
        # U and U' moves with Green front - affect top row of green face
        ("U", [["R", "R", "R"], ["G", "G", "G"], ["G", "G", "G"]], "Green"),
        ("U'", [["O", "O", "O"], ["G", "G", "G"], ["G", "G", "G"]], "Green"),
        # D and D' moves with Green front - affect bottom row of green face
        ("D", [["G", "G", "G"], ["G", "G", "G"], ["O", "O", "O"]], "Green"),
        ("D'", [["G", "G", "G"], ["G", "G", "G"], ["R", "R", "R"]], "Green"),
    ]

    # Run green front face tests
    for move, expected, description in green_front_test_cases:
        total_tests += 1
        if test_move_with_custom_front(move, None, expected, description):
            tests_passed += 1

    # Print summary
    print("\n" + "=" * 50)
    print(f"TEST SUMMARY: {tests_passed}/{total_tests} tests passed")

    if tests_passed == total_tests:
        print("✓ ALL TESTS PASSED! Cube moves are working correctly.")
    else:
        failed = total_tests - tests_passed
        print(f"✗ {failed} test(s) failed. Cube simulation needs fixes.")

    return tests_passed == total_tests


def test_move_double_and_combinations():
    """Test double moves and move combinations."""
    print("\n" + "=" * 50)
    print("Testing Double Moves and Combinations")
    print("=" * 50)

    cube = CubeSimulator()

    # Test F2 (should be equivalent to F F)
    print("\n--- Testing F2 move ---")
    cube1 = CubeSimulator()
    cube1.execute_move("F2")

    cube2 = CubeSimulator()
    cube2.execute_move("F")
    cube2.execute_move("F")

    print(f"F2 result (white face): {cube1.state['U']}")
    print(f"F F result (white face): {cube2.state['U']}")

    if cube1.state == cube2.state:
        print("✓ PASS: F2 is equivalent to F F")
    else:
        print("✗ FAIL: F2 is not equivalent to F F")

    # Test that F F' returns to solved
    print("\n--- Testing F F' cancellation ---")
    cube3 = CubeSimulator()
    initial_state = cube3.state.copy()
    cube3.execute_move("F")
    cube3.execute_move("F'")

    print(f"Initial (white face): {initial_state['U']}")
    print(f"After F F' (white face): {cube3.state['U']}")

    if cube3.state == initial_state:
        print("✓ PASS: F F' returns to solved state")
    else:
        print("✗ FAIL: F F' does not return to solved state")


def debug_cube_state(cube, move_sequence=""):
    """Helper function to debug full cube state."""
    print(f"\n--- Debug: Full cube state after '{move_sequence}' ---")
    faces = ["U", "D", "F", "B", "L", "R"]
    for face in faces:
        print(f"{face}: {cube.state[face]}")


if __name__ == "__main__":
    # Run main tests
    success = run_all_move_tests()

    # Run additional tests
    test_move_double_and_combinations()

    # Exit with appropriate code
    sys.exit(0 if success else 1)
