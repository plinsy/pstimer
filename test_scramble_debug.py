#!/usr/bin/env python3
"""
Test cube simulation with the specific scramble provided by the user.
"""

from src.cube_visualization import CubeSimulator


def test_specific_scramble():
    """Test the specific scramble: U2 R' L U2 L R2 D' B2 L R U' F2 L' U' B2 F U2 L2 U B'"""
    cube = CubeSimulator()

    print("Initial solved state:")
    print_cube_faces(cube)

    # Apply the scramble step by step to debug
    scramble = "U2 R' L U2 L R2 D' B2 L R U' F2 L' U' B2 F U2 L2 U B'"
    moves = scramble.split()

    print(f"\nApplying scramble: {scramble}")
    print(f"Number of moves: {len(moves)}")

    for i, move in enumerate(moves):
        print(f"\nMove {i+1}: {move}")
        cube.execute_move(move)
        print(f"U face after {move}: {cube.state['U']}")

    print("\nFinal state after full scramble:")
    print_cube_faces(cube)

    # Check the white face specifically
    print("\nWhite face (U) final state:")
    for row in range(3):
        row_colors = []
        for col in range(3):
            sticker = cube.state["U"][row][col]
            color_name = get_color_name(sticker)
            row_colors.append(color_name)
        print(f"Row {row}: {' '.join(row_colors)}")


def get_color_name(letter):
    """Convert letter to color name."""
    color_map = {
        "W": "White",
        "Y": "Yellow",
        "R": "Red",
        "O": "Orange",
        "G": "Green",
        "B": "Blue",
    }
    return color_map.get(letter, letter)


def print_cube_faces(cube):
    """Print all cube faces."""
    for face_name, face_state in cube.state.items():
        print(f"{face_name}: {face_state}")


def test_individual_moves():
    """Test individual moves to verify they work correctly."""
    cube = CubeSimulator()

    print("Testing U move:")
    print("Before U:", cube.state["U"])
    cube.execute_move("U")
    print("After U:", cube.state["U"])

    # Reset and test U2
    cube.reset_to_solved()
    print("\nTesting U2 move:")
    print("Before U2:", cube.state["U"])
    cube.execute_move("U2")
    print("After U2:", cube.state["U"])

    # Reset and test U'
    cube.reset_to_solved()
    print("\nTesting U' move:")
    print("Before U':", cube.state["U"])
    cube.execute_move("U'")
    print("After U':", cube.state["U"])


if __name__ == "__main__":
    print("=== Testing Individual Moves ===")
    test_individual_moves()

    print("\n=== Testing Specific Scramble ===")
    test_specific_scramble()
