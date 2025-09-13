#!/usr/bin/env python3

from src.cube_visualization import CubeSimulator


def test_l_move():
    cube = CubeSimulator()

    print("=== Testing L move sequence ===")
    print("Starting from solved state")

    # Apply the sequence up to move 16 (just before U2)
    moves_before_u2 = [
        "U2",
        "R'",
        "L",
        "U2",
        "L",
        "R2",
        "D'",
        "B2",
        "L",
        "R",
        "U'",
        "F2",
        "L'",
        "U'",
        "B2",
        "F",
    ]

    for i, move in enumerate(moves_before_u2):
        cube.execute_move(move)
        print(f"Move {i+1}: {move}")
        print(f"U face: {cube.state['U']}")
        print()

    print("=== Now testing U2 and L2 ===")

    # State before U2
    print("Before U2:")
    print(f"U face: {cube.state['U']}")
    print(
        f"F left column: {[cube.state['F'][0][0], cube.state['F'][1][0], cube.state['F'][2][0]]}"
    )
    print(
        f"B right column: {[cube.state['B'][0][2], cube.state['B'][1][2], cube.state['B'][2][2]]}"
    )
    print(
        f"D left column: {[cube.state['D'][0][0], cube.state['D'][1][0], cube.state['D'][2][0]]}"
    )
    print()

    # Apply U2
    cube.execute_move("U2")
    print("After U2:")
    print(f"U face: {cube.state['U']}")
    print(
        f"F left column: {[cube.state['F'][0][0], cube.state['F'][1][0], cube.state['F'][2][0]]}"
    )
    print(
        f"B right column: {[cube.state['B'][0][2], cube.state['B'][1][2], cube.state['B'][2][2]]}"
    )
    print(
        f"D left column: {[cube.state['D'][0][0], cube.state['D'][1][0], cube.state['D'][2][0]]}"
    )
    print()

    # Apply L2
    cube.execute_move("L2")
    print("After L2:")
    print(f"U face: {cube.state['U']}")
    print(
        f"F left column: {[cube.state['F'][0][0], cube.state['F'][1][0], cube.state['F'][2][0]]}"
    )
    print(
        f"B right column: {[cube.state['B'][0][2], cube.state['B'][1][2], cube.state['B'][2][2]]}"
    )
    print(
        f"D left column: {[cube.state['D'][0][0], cube.state['D'][1][0], cube.state['D'][2][0]]}"
    )


if __name__ == "__main__":
    test_l_move()
