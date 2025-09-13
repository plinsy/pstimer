"""
Debug script to understand the current cube state and expected vs actual orientations.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.cube_visualization import CubeSimulator


def print_full_cube_state(cube, title="Cube State"):
    """Print the complete state of all faces."""
    print(f"\n{title}:")
    print("=" * 30)
    faces = ["U", "D", "F", "B", "L", "R"]
    for face in faces:
        print(f"{face}: {cube.state[face]}")


def analyze_expected_vs_actual():
    """Analyze what the test expects vs what we get."""
    print("CUBE ORIENTATION ANALYSIS")
    print("=" * 50)

    # Create a fresh cube
    cube = CubeSimulator()
    print_full_cube_state(cube, "Current WCA Standard Initial State")

    print("\nExpected test behavior analysis:")
    print("- Tests expect white front face initially")
    print("- Tests expect F move to change bottom row to orange")
    print("- Current cube has green front face")

    # Test what colors are adjacent in current cube
    print("\nCurrent cube color mapping:")
    print(f"Front (F): Green")
    print(f"Up (U): White")
    print(f"Down (D): Yellow")
    print(f"Left (L): Orange")
    print(f"Right (R): Red")
    print(f"Back (B): Blue")

    # Let me test some moves to understand the current behavior
    print("\n" + "=" * 50)
    print("TESTING CURRENT MOVES")

    # Test F move on current green front face
    cube_f = CubeSimulator()
    print(f"\nBefore F move - Front face: {cube_f.state['F']}")
    cube_f.execute_move("F")
    print(f"After F move - Front face: {cube_f.state['F']}")
    print("Changes observed:")
    print(f"  - F face itself rotated: {cube_f.state['F']}")

    # Test what happens to adjacent faces
    cube_check = CubeSimulator()
    print(f"\nBefore F - Bottom row of U face: {cube_check.state['U'][2]}")
    print(f"Before F - Top row of D face: {cube_check.state['D'][0]}")
    print(
        f"Before F - Right column of L face: [row[2] for row in {cube_check.state['L']}]"
    )
    print(
        f"Before F - Left column of R face: [row[0] for row in {cube_check.state['R']}]"
    )

    cube_check.execute_move("F")
    print(f"\nAfter F - Bottom row of U face: {cube_check.state['U'][2]}")
    print(f"After F - Top row of D face: {cube_check.state['D'][0]}")
    print(
        f"After F - Right column of L face: [row[2] for row in {cube_check.state['L']}]"
    )
    print(
        f"After F - Left column of R face: [row[0] for row in {cube_check.state['R']}]"
    )


def test_correct_wca_orientation():
    """Test what the correct WCA orientation should be."""
    print("\n" + "=" * 50)
    print("WCA STANDARD CUBE ORIENTATION")
    print("=" * 50)

    print("According to WCA standards:")
    print("- White face should be UP (U)")
    print("- Yellow face should be DOWN (D)")
    print("- Green face should be FRONT (F)")
    print("- Blue face should be BACK (B)")
    print("- Orange face should be LEFT (L)")
    print("- Red face should be RIGHT (R)")

    print("\nBut the test prompt expects:")
    print("- White face as FRONT initially")
    print(
        "- This suggests the test is looking at the front face in a specific orientation"
    )

    print(
        "\nLet me create a cube with WHITE as front face to match test expectations..."
    )

    # Create a cube with white front face to match test expectations
    cube = CubeSimulator()

    # Manually set white as front face for testing
    cube.state["F"] = [["W", "W", "W"], ["W", "W", "W"], ["W", "W", "W"]]

    print(f"\nModified cube with White front: {cube.state['F']}")

    # Now test F move
    cube.execute_move("F")
    print(f"After F move: {cube.state['F']}")

    # The issue is that when we rotate F face, we're rotating the white stickers
    # But the test expects to see the EFFECT on the front face from adjacent faces


if __name__ == "__main__":
    analyze_expected_vs_actual()
    test_correct_wca_orientation()
