"""
Comprehensive test suite for cube moves with additional validation.
This extends the basic move tests with more thorough validation.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.cube_visualization import CubeSimulator


def test_all_basic_moves():
    """Test all basic moves (F, B, R, L, U, D) and their primes."""
    print("COMPREHENSIVE CUBE MOVE VALIDATION")
    print("=" * 50)

    moves_and_expected = [
        # Format: (move, expected_white_face, description)
        (
            "F",
            [["W", "W", "W"], ["W", "W", "W"], ["O", "O", "O"]],
            "F affects white bottom",
        ),
        (
            "F'",
            [["W", "W", "W"], ["W", "W", "W"], ["R", "R", "R"]],
            "F' affects white bottom",
        ),
        (
            "B",
            [["R", "R", "R"], ["W", "W", "W"], ["W", "W", "W"]],
            "B affects white top",
        ),
        (
            "B'",
            [["O", "O", "O"], ["W", "W", "W"], ["W", "W", "W"]],
            "B' affects white top",
        ),
        (
            "R",
            [["W", "W", "G"], ["W", "W", "G"], ["W", "W", "G"]],
            "R affects white right",
        ),
        (
            "R'",
            [["W", "W", "B"], ["W", "W", "B"], ["W", "W", "B"]],
            "R' affects white right",
        ),
        (
            "L",
            [["B", "W", "W"], ["B", "W", "W"], ["B", "W", "W"]],
            "L affects white left",
        ),
        (
            "L'",
            [["G", "W", "W"], ["G", "W", "W"], ["G", "W", "W"]],
            "L' affects white left",
        ),
    ]

    tests_passed = 0
    for move, expected_white, description in moves_and_expected:
        cube = CubeSimulator()
        cube.execute_move(move)
        if cube.state["U"] == expected_white:
            print(f"✓ {move}: {description}")
            tests_passed += 1
        else:
            print(f"✗ {move}: {description} - FAILED")
            print(f"  Expected: {expected_white}")
            print(f"  Got:      {cube.state['U']}")

    # Test U and D moves with green front observation
    ud_moves = [
        (
            "U",
            [["R", "R", "R"], ["G", "G", "G"], ["G", "G", "G"]],
            "U affects green top",
        ),
        (
            "U'",
            [["O", "O", "O"], ["G", "G", "G"], ["G", "G", "G"]],
            "U' affects green top",
        ),
        (
            "D",
            [["G", "G", "G"], ["G", "G", "G"], ["O", "O", "O"]],
            "D affects green bottom",
        ),
        (
            "D'",
            [["G", "G", "G"], ["G", "G", "G"], ["R", "R", "R"]],
            "D' affects green bottom",
        ),
    ]

    for move, expected_green, description in ud_moves:
        cube = CubeSimulator()
        cube.execute_move(move)
        if cube.state["F"] == expected_green:
            print(f"✓ {move}: {description}")
            tests_passed += 1
        else:
            print(f"✗ {move}: {description} - FAILED")
            print(f"  Expected: {expected_green}")
            print(f"  Got:      {cube.state['F']}")

    print(f"\nBasic moves test: {tests_passed}/12 passed")
    return tests_passed == 12


def test_move_cancellations():
    """Test that moves cancel with their opposites."""
    print("\n" + "=" * 50)
    print("MOVE CANCELLATION TESTS")
    print("=" * 50)

    move_pairs = [
        ("F", "F'"),
        ("B", "B'"),
        ("R", "R'"),
        ("L", "L'"),
        ("U", "U'"),
        ("D", "D'"),
    ]
    cancellation_tests_passed = 0

    for move1, move2 in move_pairs:
        cube = CubeSimulator()
        initial_state = cube.state.copy()

        # Apply move then its inverse
        cube.execute_move(move1)
        cube.execute_move(move2)

        if cube.state == initial_state:
            print(f"✓ {move1} {move2} cancellation works")
            cancellation_tests_passed += 1
        else:
            print(f"✗ {move1} {move2} cancellation FAILED")

    print(f"\nCancellation tests: {cancellation_tests_passed}/6 passed")
    return cancellation_tests_passed == 6


def test_double_moves():
    """Test that double moves work correctly."""
    print("\n" + "=" * 50)
    print("DOUBLE MOVE TESTS")
    print("=" * 50)

    moves = ["F", "B", "R", "L", "U", "D"]
    double_tests_passed = 0

    for move in moves:
        # Test that X2 == X X
        cube1 = CubeSimulator()
        cube1.execute_move(f"{move}2")

        cube2 = CubeSimulator()
        cube2.execute_move(move)
        cube2.execute_move(move)

        if cube1.state == cube2.state:
            print(f"✓ {move}2 == {move} {move}")
            double_tests_passed += 1
        else:
            print(f"✗ {move}2 != {move} {move}")

    print(f"\nDouble move tests: {double_tests_passed}/6 passed")
    return double_tests_passed == 6


def test_four_move_cycles():
    """Test that four identical moves return to solved state."""
    print("\n" + "=" * 50)
    print("FOUR-MOVE CYCLE TESTS")
    print("=" * 50)

    moves = ["F", "B", "R", "L", "U", "D"]
    cycle_tests_passed = 0

    for move in moves:
        cube = CubeSimulator()
        initial_state = cube.state.copy()

        # Apply move four times
        for _ in range(4):
            cube.execute_move(move)

        if cube.state == initial_state:
            print(f"✓ {move}^4 returns to solved state")
            cycle_tests_passed += 1
        else:
            print(f"✗ {move}^4 does not return to solved state")

    print(f"\nFour-move cycle tests: {cycle_tests_passed}/6 passed")
    return cycle_tests_passed == 6


def test_commutator_properties():
    """Test some basic commutator properties."""
    print("\n" + "=" * 50)
    print("COMMUTATOR TESTS")
    print("=" * 50)

    # Test that R U R' U' is not the identity (but applying it 6 times should be)
    cube = CubeSimulator()
    initial_state = {}
    for face in cube.state:
        initial_state[face] = [row[:] for row in cube.state[face]]  # Deep copy

    # Apply R U R' U' sequence
    sequence = ["R", "U", "R'", "U'"]
    for move in sequence:
        cube.execute_move(move)

    # Check if states are equal (need to compare properly)
    states_equal = True
    for face in cube.state:
        if cube.state[face] != initial_state[face]:
            states_equal = False
            break

    # Should not be solved after one application
    if not states_equal:
        print("✓ R U R' U' is not identity (expected)")

        # Apply it 5 more times (6 total) - should return to solved
        for _ in range(5):
            for move in sequence:
                cube.execute_move(move)

        # Check if back to solved
        final_states_equal = True
        for face in cube.state:
            if cube.state[face] != initial_state[face]:
                final_states_equal = False
                break

        if final_states_equal:
            print("✓ (R U R' U')^6 returns to solved state")
            return True
        else:
            print("✗ (R U R' U')^6 does not return to solved state")
            return False
    else:
        print("✗ R U R' U' incorrectly returns to identity")
        return False


def run_comprehensive_tests():
    """Run all comprehensive tests."""
    print("RUNNING COMPREHENSIVE CUBE MOVE TESTS")
    print("=" * 60)

    test_results = [
        test_all_basic_moves(),
        test_move_cancellations(),
        test_double_moves(),
        test_four_move_cycles(),
        test_commutator_properties(),
    ]

    passed_tests = sum(test_results)
    total_tests = len(test_results)

    print("\n" + "=" * 60)
    print(
        f"COMPREHENSIVE TEST SUMMARY: {passed_tests}/{total_tests} test categories passed"
    )

    if passed_tests == total_tests:
        print("🎉 ALL COMPREHENSIVE TESTS PASSED!")
        print("The cube simulation is working correctly according to WCA standards.")
    else:
        print(f"⚠️  {total_tests - passed_tests} test categories failed.")
        print("The cube simulation needs further fixes.")

    return passed_tests == total_tests


if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
