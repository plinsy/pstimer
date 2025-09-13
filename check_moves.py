#!/usr/bin/env python3

from src.cube_visualization import CubeSimulator


def check_move_by_move():
    """Check each move in the sequence to see where divergence occurs"""
    cube = CubeSimulator()

    # The scramble sequence
    scramble = "U2 R' L U2 L R2 D' B2 L R U' F2 L' U' B2 F U2 L2 U B'"
    moves = scramble.split()

    print("=== Checking move by move ===")
    print("Initial state U(0,0):", cube.state["U"][0][0])

    for i, move in enumerate(moves):
        cube.execute_move(move)
        print(f"Move {i+1}: {move} -> U(0,0) = {cube.state['U'][0][0]}")

        # Pay special attention to moves 16, 17, 18
        if i + 1 in [16, 17, 18]:
            print(f"  Full U face: {cube.state['U']}")


if __name__ == "__main__":
    check_move_by_move()
