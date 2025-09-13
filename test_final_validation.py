"""
Final summary test that validates all the expected moves from test-moves.prompt.md

This test validates that PSTimer's cube simulation correctly implements WCA-standard
Rubik's cube moves and produces the exact results specified in the test prompt.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.cube_visualization import CubeSimulator


def main():
    """Run the complete test suite as specified in test-moves.prompt.md"""
    print("PSTimer Cube Move Validation - Final Report")
    print("=" * 60)
    print("Validating cube moves against test-moves.prompt.md specifications")
    print("=" * 60)

    # Test specifications from the prompt
    test_specifications = [
        {
            "description": "White face observations (viewing white face as front)",
            "tests": [
                (
                    "F",
                    [["W", "W", "W"], ["W", "W", "W"], ["O", "O", "O"]],
                    "F move affects bottom row with orange",
                ),
                (
                    "F'",
                    [["W", "W", "W"], ["W", "W", "W"], ["R", "R", "R"]],
                    "F' move affects bottom row with red",
                ),
                (
                    "B",
                    [["R", "R", "R"], ["W", "W", "W"], ["W", "W", "W"]],
                    "B move affects top row with red",
                ),
                (
                    "B'",
                    [["O", "O", "O"], ["W", "W", "W"], ["W", "W", "W"]],
                    "B' move affects top row with orange",
                ),
                (
                    "R",
                    [["W", "W", "G"], ["W", "W", "G"], ["W", "W", "G"]],
                    "R move affects right column with green",
                ),
                (
                    "R'",
                    [["W", "W", "B"], ["W", "W", "B"], ["W", "W", "B"]],
                    "R' move affects right column with blue",
                ),
                (
                    "L",
                    [["B", "W", "W"], ["B", "W", "W"], ["B", "W", "W"]],
                    "L move affects left column with blue",
                ),
                (
                    "L'",
                    [["G", "W", "W"], ["G", "W", "W"], ["G", "W", "W"]],
                    "L' move affects left column with green",
                ),
            ],
            "observe_face": "U",  # White face
        },
        {
            "description": "Green face observations (viewing green face as front)",
            "tests": [
                (
                    "U",
                    [["R", "R", "R"], ["G", "G", "G"], ["G", "G", "G"]],
                    "U move affects top row with red",
                ),
                (
                    "U'",
                    [["O", "O", "O"], ["G", "G", "G"], ["G", "G", "G"]],
                    "U' move affects top row with orange",
                ),
                (
                    "D",
                    [["G", "G", "G"], ["G", "G", "G"], ["O", "O", "O"]],
                    "D move affects bottom row with orange",
                ),
                (
                    "D'",
                    [["G", "G", "G"], ["G", "G", "G"], ["R", "R", "R"]],
                    "D' move affects bottom row with red",
                ),
            ],
            "observe_face": "F",  # Green face
        },
    ]

    total_tests = 0
    passed_tests = 0

    for spec in test_specifications:
        print(f"\n{spec['description']}:")
        print("-" * len(spec["description"]))

        for move, expected, description in spec["tests"]:
            total_tests += 1
            cube = CubeSimulator()
            cube.execute_move(move)

            actual = cube.state[spec["observe_face"]]

            if actual == expected:
                print(f"✓ {move:3s}: {description}")
                passed_tests += 1
            else:
                print(f"✗ {move:3s}: {description}")
                print(f"    Expected: {expected}")
                print(f"    Got:      {actual}")

    # Additional validation tests
    print(f"\nAdditional Validation Tests:")
    print("-" * 30)

    # Test move cancellations
    moves = ["F", "B", "R", "L", "U", "D"]
    for move in moves:
        total_tests += 1
        cube = CubeSimulator()
        initial_state = {
            face: [row[:] for row in cube.state[face]] for face in cube.state
        }

        cube.execute_move(move)
        cube.execute_move(f"{move}'")

        states_equal = all(
            cube.state[face] == initial_state[face] for face in cube.state
        )

        if states_equal:
            print(f"✓ {move} {move}' cancellation works")
            passed_tests += 1
        else:
            print(f"✗ {move} {move}' cancellation failed")

    # Test double moves
    for move in moves:
        total_tests += 1
        cube1 = CubeSimulator()
        cube1.execute_move(f"{move}2")

        cube2 = CubeSimulator()
        cube2.execute_move(move)
        cube2.execute_move(move)

        states_equal = all(
            cube1.state[face] == cube2.state[face] for face in cube1.state
        )

        if states_equal:
            print(f"✓ {move}2 == {move} {move}")
            passed_tests += 1
        else:
            print(f"✗ {move}2 != {move} {move}")

    # Final report
    print("\n" + "=" * 60)
    print("FINAL TEST RESULTS")
    print("=" * 60)
    print(f"Tests passed: {passed_tests}/{total_tests}")

    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("\nPSTimer's cube simulation correctly implements:")
        print("✓ All basic moves (F, B, R, L, U, D) and their primes")
        print("✓ Double moves (F2, B2, R2, L2, U2, D2)")
        print("✓ Move cancellations (X X' = identity)")
        print("✓ WCA-standard cube orientation and color scheme")
        print("✓ Correct move effects as specified in test-moves.prompt.md")

        print("\nThe cube simulation is ready for use in PSTimer!")
        return True
    else:
        failed = total_tests - passed_tests
        print(f"❌ {failed} tests failed")
        print("The cube simulation needs additional fixes.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
