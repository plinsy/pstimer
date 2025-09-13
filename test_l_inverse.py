#!/usr/bin/env python3

from src.cube_visualization import CubeSimulator


def test_l_inverse():
    cube = CubeSimulator()

    print("=== Testing L and L' are inverses ===")
    print("Starting from solved state")
    print(f"U face: {cube.state['U']}")
    print(
        f"F left: {[cube.state['F'][0][0], cube.state['F'][1][0], cube.state['F'][2][0]]}"
    )
    print(
        f"D left: {[cube.state['D'][0][0], cube.state['D'][1][0], cube.state['D'][2][0]]}"
    )
    print(
        f"B right: {[cube.state['B'][0][2], cube.state['B'][1][2], cube.state['B'][2][2]]}"
    )
    print()

    # Apply L
    cube.execute_move("L")
    print("After L:")
    print(f"U face: {cube.state['U']}")
    print(
        f"F left: {[cube.state['F'][0][0], cube.state['F'][1][0], cube.state['F'][2][0]]}"
    )
    print(
        f"D left: {[cube.state['D'][0][0], cube.state['D'][1][0], cube.state['D'][2][0]]}"
    )
    print(
        f"B right: {[cube.state['B'][0][2], cube.state['B'][1][2], cube.state['B'][2][2]]}"
    )
    print()

    # Apply L'
    cube.execute_move("L'")
    print("After L':")
    print(f"U face: {cube.state['U']}")
    print(
        f"F left: {[cube.state['F'][0][0], cube.state['F'][1][0], cube.state['F'][2][0]]}"
    )
    print(
        f"D left: {[cube.state['D'][0][0], cube.state['D'][1][0], cube.state['D'][2][0]]}"
    )
    print(
        f"B right: {[cube.state['B'][0][2], cube.state['B'][1][2], cube.state['B'][2][2]]}"
    )

    # Check if back to solved
    is_solved = all(
        all(
            all(cell == expected for cell in row)
            for row, expected in zip(
                face,
                (
                    [["W"] * 3, ["W"] * 3, ["W"] * 3]
                    if face_name == "U"
                    else (
                        [["Y"] * 3, ["Y"] * 3, ["Y"] * 3]
                        if face_name == "D"
                        else (
                            [["G"] * 3, ["G"] * 3, ["G"] * 3]
                            if face_name == "F"
                            else (
                                [["B"] * 3, ["B"] * 3, ["B"] * 3]
                                if face_name == "B"
                                else (
                                    [["O"] * 3, ["O"] * 3, ["O"] * 3]
                                    if face_name == "L"
                                    else [["R"] * 3, ["R"] * 3, ["R"] * 3]
                                )
                            )
                        )
                    )
                ),
            )
        )
        for face_name, face in cube.state.items()
    )
    print(f"\n✓ L followed by L' returns to solved state: {is_solved}")


if __name__ == "__main__":
    test_l_inverse()
