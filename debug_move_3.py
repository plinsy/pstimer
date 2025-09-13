#!/usr/bin/env python3

from src.cube_visualization import CubeSimulator


def debug_move_3():
    """Debug what happens at move 3 (L)"""
    cube = CubeSimulator()

    # Apply moves 1-2
    cube.execute_move("U2")
    cube.execute_move("R'")

    print("=== State right before move 3 (L) ===")
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

    print("Full faces before move 3:")
    for face_name in ["U", "F", "D", "B"]:
        print(f"{face_name}: {cube.state[face_name]}")
    print()

    # Apply L move manually step by step to understand the cycle
    print("L move should do:")
    print(
        f"U left ← F left: {[cube.state['F'][0][0], cube.state['F'][1][0], cube.state['F'][2][0]]}"
    )
    print(
        f"F left ← D left: {[cube.state['D'][0][0], cube.state['D'][1][0], cube.state['D'][2][0]]}"
    )
    print(
        f"D left ← B right (rev): {[cube.state['B'][2][2], cube.state['B'][1][2], cube.state['B'][0][2]]}"
    )
    print(
        f"B right ← U left (rev): {[cube.state['U'][2][0], cube.state['U'][1][0], cube.state['U'][0][0]]}"
    )
    print()

    # Apply L
    cube.execute_move("L")
    print("=== After move 3 (L) ===")
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


if __name__ == "__main__":
    debug_move_3()
