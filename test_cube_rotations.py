"""
Test cube rotations (x, x', y, y', z, z', z2) to verify they work according to specifications.

Initial position: White on top, Green in front, Red on right
Expected results:
- x move: Blue face (back) should be what I see when I do the x move (blue becomes front)
- x' move: Green (front) should be the top when I do x' move
- z move: Orange (left) should be the top when I do z move
- z' move: Red (right) should be the top when I do z' move
- z2 move: Yellow (down) should be the top when I do z2 move
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.cube_visualization import CubeSimulator


def print_cube_orientation(cube, title):
    """Print the current cube orientation."""
    print(f"\n{title}:")
    print(f"  Top (U):   {cube.state['U'][1][1]} face")
    print(f"  Front (F): {cube.state['F'][1][1]} face")
    print(f"  Right (R): {cube.state['R'][1][1]} face")
    print(f"  Left (L):  {cube.state['L'][1][1]} face")
    print(f"  Back (B):  {cube.state['B'][1][1]} face")
    print(f"  Down (D):  {cube.state['D'][1][1]} face")


def test_initial_orientation():
    """Test that the initial cube state matches expected WCA orientation."""
    print("TESTING INITIAL CUBE ORIENTATION")
    print("=" * 50)

    cube = CubeSimulator()
    print_cube_orientation(cube, "Initial WCA Standard Position")

    # Verify initial state
    expected_initial = {
        "U": "W",  # White on top
        "F": "G",  # Green in front
        "R": "R",  # Red on right
        "L": "O",  # Orange on left
        "B": "B",  # Blue in back
        "D": "Y",  # Yellow on bottom
    }

    actual = {face: cube.state[face][1][1] for face in ["U", "F", "R", "L", "B", "D"]}

    if actual == expected_initial:
        print("✓ Initial orientation is correct")
        return True
    else:
        print("✗ Initial orientation is incorrect")
        print(f"Expected: {expected_initial}")
        print(f"Actual: {actual}")
        return False


def test_x_rotation():
    """Test x rotation: Blue face should become front."""
    print("\n" + "=" * 50)
    print("TESTING X ROTATION")
    print("=" * 50)

    cube = CubeSimulator()
    print_cube_orientation(cube, "Before x rotation")

    cube.execute_move("x")
    print_cube_orientation(cube, "After x rotation")

    # After x rotation, blue should be front
    if cube.state["F"][1][1] == "B":
        print("✓ x rotation: Blue face is now front")
        return True
    else:
        print(
            f"✗ x rotation failed: Expected Blue front, got {cube.state['F'][1][1]} front"
        )
        return False


def test_x_prime_rotation():
    """Test x' rotation: Green should become top."""
    print("\n" + "=" * 50)
    print("TESTING X' ROTATION")
    print("=" * 50)

    cube = CubeSimulator()
    print_cube_orientation(cube, "Before x' rotation")

    cube.execute_move("x'")
    print_cube_orientation(cube, "After x' rotation")

    # After x' rotation, green should be top
    if cube.state["U"][1][1] == "G":
        print("✓ x' rotation: Green face is now top")
        return True
    else:
        print(
            f"✗ x' rotation failed: Expected Green top, got {cube.state['U'][1][1]} top"
        )
        return False


def test_z_rotation():
    """Test z rotation: Orange should become top."""
    print("\n" + "=" * 50)
    print("TESTING Z ROTATION")
    print("=" * 50)

    cube = CubeSimulator()
    print_cube_orientation(cube, "Before z rotation")

    cube.execute_move("z")
    print_cube_orientation(cube, "After z rotation")

    # After z rotation, orange should be top
    if cube.state["U"][1][1] == "O":
        print("✓ z rotation: Orange face is now top")
        return True
    else:
        print(
            f"✗ z rotation failed: Expected Orange top, got {cube.state['U'][1][1]} top"
        )
        return False


def test_z_prime_rotation():
    """Test z' rotation: Red should become top."""
    print("\n" + "=" * 50)
    print("TESTING Z' ROTATION")
    print("=" * 50)

    cube = CubeSimulator()
    print_cube_orientation(cube, "Before z' rotation")

    cube.execute_move("z'")
    print_cube_orientation(cube, "After z' rotation")

    # After z' rotation, red should be top
    if cube.state["U"][1][1] == "R":
        print("✓ z' rotation: Red face is now top")
        return True
    else:
        print(
            f"✗ z' rotation failed: Expected Red top, got {cube.state['U'][1][1]} top"
        )
        return False


def test_z2_rotation():
    """Test z2 rotation: Yellow should become top."""
    print("\n" + "=" * 50)
    print("TESTING Z2 ROTATION")
    print("=" * 50)

    cube = CubeSimulator()
    print_cube_orientation(cube, "Before z2 rotation")

    cube.execute_move("z2")
    print_cube_orientation(cube, "After z2 rotation")

    # After z2 rotation, yellow should be top
    if cube.state["U"][1][1] == "Y":
        print("✓ z2 rotation: Yellow face is now top")
        return True
    else:
        print(
            f"✗ z2 rotation failed: Expected Yellow top, got {cube.state['U'][1][1]} top"
        )
        return False


def test_rotation_cancellations():
    """Test that rotations cancel with their opposites."""
    print("\n" + "=" * 50)
    print("TESTING ROTATION CANCELLATIONS")
    print("=" * 50)

    rotation_pairs = [("x", "x'"), ("y", "y'"), ("z", "z'")]
    tests_passed = 0

    for rot1, rot2 in rotation_pairs:
        cube = CubeSimulator()
        initial_state = cube.state.copy()

        cube.execute_move(rot1)
        cube.execute_move(rot2)

        if cube.state == initial_state:
            print(f"✓ {rot1} {rot2} cancellation works")
            tests_passed += 1
        else:
            print(f"✗ {rot1} {rot2} cancellation failed")

    # Test z2 z2 cancellation (should return to original)
    cube = CubeSimulator()
    initial_state = cube.state.copy()
    cube.execute_move("z2")
    cube.execute_move("z2")

    if cube.state == initial_state:
        print("✓ z2 z2 cancellation works")
        tests_passed += 1
    else:
        print("✗ z2 z2 cancellation failed")

    return tests_passed == 4


def run_all_rotation_tests():
    """Run all rotation tests."""
    print("CUBE ROTATION TESTS")
    print("=" * 60)

    tests = [
        test_initial_orientation(),
        test_x_rotation(),
        test_x_prime_rotation(),
        test_z_rotation(),
        test_z_prime_rotation(),
        test_z2_rotation(),
        test_rotation_cancellations(),
    ]

    passed = sum(tests)
    total = len(tests)

    print("\n" + "=" * 60)
    print(f"ROTATION TEST SUMMARY: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL ROTATION TESTS PASSED!")
        print("Cube rotations are working correctly!")
    else:
        print(f"⚠️  {total - passed} rotation tests failed.")
        print("Cube rotation implementation needs fixes.")

    return passed == total


if __name__ == "__main__":
    success = run_all_rotation_tests()
    sys.exit(0 if success else 1)
