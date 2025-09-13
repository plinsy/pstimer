#!/usr/bin/env python3

from src.cube_visualization import CubeSimulator


def debug_move_5():
    """Debug what happens at move 5 (L)"""
    cube = CubeSimulator()

    # Apply moves 1-4
    moves = ["U2", "R'", "L", "U2"]
    for i, move in enumerate(moves):
        cube.execute_move(move)
        print(f"Move {i+1}: {move}")
        print(f"U face: {cube.state['U']}")
        print()

    print("=== State right before move 5 (L) ===")
    print(
        f"U left column: {[cube.state['U'][0][0], cube.state['U'][1][0], cube.state['U'][2][0]]}"
    )
    print(
        f"F left column: {[cube.state['F'][0][0], cube.state['F'][1][0], cube.state['F'][2][0]]}"
    )
    print(
        f"D left column: {[cube.state['D'][0][0], cube.state['D'][1][0], cube.state['D'][2][0]]}"
    )
    print(
        f"B right column: {[cube.state['B'][0][2], cube.state['B'][1][2], cube.state['B'][2][2]]}"
    )
    print()
    print("Full faces:")
    for face_name in ["U", "F", "D", "B", "L", "R"]:
        print(f"{face_name}: {cube.state[face_name]}")
    print()

    # Apply L and see what happens
    cube.execute_move("L")
    print("=== After move 5 (L) ===")
    print(f"U face: {cube.state['U']}")
    print(
        f"U left column: {[cube.state['U'][0][0], cube.state['U'][1][0], cube.state['U'][2][0]]}"
    )

    print("\nExpected: U left column should be ['W', 'W', 'W']")
    print(
        f"Actual: U left column is {[cube.state['U'][0][0], cube.state['U'][1][0], cube.state['U'][2][0]]}"
    )


if __name__ == "__main__":
    debug_move_5()
