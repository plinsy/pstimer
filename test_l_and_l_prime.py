#!/usr/bin/env python3

from src.cube_visualization import CubeSimulator


def test_l_and_l_prime():
    cube = CubeSimulator()

    print("=== Testing L and L' properly ===")

    # Start from solved
    print(
        "Initial solved state (U left column):",
        [cube.state["U"][0][0], cube.state["U"][1][0], cube.state["U"][2][0]],
    )

    # Apply L
    cube.execute_move("L")
    print(
        "After L (U left column):",
        [cube.state["U"][0][0], cube.state["U"][1][0], cube.state["U"][2][0]],
    )

    # Apply L'
    cube.execute_move("L'")
    print(
        "After L' (U left column):",
        [cube.state["U"][0][0], cube.state["U"][1][0], cube.state["U"][2][0]],
    )

    # Check if cube is solved
    solved = True
    expected_colors = {"U": "W", "D": "Y", "F": "G", "B": "B", "L": "O", "R": "R"}
    for face_name, face in cube.state.items():
        expected_color = expected_colors[face_name]
        for row in face:
            for cell in row:
                if cell != expected_color:
                    solved = False
                    break

    print(f"Is cube solved after L then L'? {solved}")

    if not solved:
        print("\nActual final state:")
        for face_name in ["U", "F", "D", "B", "L", "R"]:
            print(f"{face_name}: {cube.state[face_name]}")


if __name__ == "__main__":
    test_l_and_l_prime()
