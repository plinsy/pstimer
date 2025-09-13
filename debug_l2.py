#!/usr/bin/env python3

from src.cube_visualization import CubeSimulator


def debug_l2_move():
    """Debug exactly what happens during L2"""
    cube = CubeSimulator()

    # Apply all moves up to move 17 (U2)
    moves_before_l2 = [
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
        "U2",
    ]

    for move in moves_before_l2:
        cube.execute_move(move)

    print("=== State right before L2 ===")
    print(f"U(0,0) = {cube.state['U'][0][0]}")
    print(f"F(0,0) = {cube.state['F'][0][0]}")
    print(f"D(0,0) = {cube.state['D'][0][0]}")
    print(f"B(2,2) = {cube.state['B'][2][2]}")  # This feeds into D(0,0) after first L
    print()
    print("Full faces:")
    print(f"U: {cube.state['U']}")
    print(f"F: {cube.state['F']}")
    print(f"D: {cube.state['D']}")
    print(f"B: {cube.state['B']}")
    print()

    # Apply first L
    cube.execute_move("L")
    print("=== After first L ===")
    print(f"U(0,0) = {cube.state['U'][0][0]} (should be F(0,0) from before)")
    print(f"F(0,0) = {cube.state['F'][0][0]} (should be D(0,0) from before)")
    print(f"D(0,0) = {cube.state['D'][0][0]} (should be B(2,2) from before)")
    print(f"B(2,2) = {cube.state['B'][2][2]} (should be U(2,0) from before)")
    print()

    # Apply second L
    cube.execute_move("L")
    print("=== After second L (L2 complete) ===")
    print(f"U(0,0) = {cube.state['U'][0][0]}")
    print(f"Full U face: {cube.state['U']}")


if __name__ == "__main__":
    debug_l2_move()
