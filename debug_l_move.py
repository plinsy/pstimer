#!/usr/bin/env python3

from src.cube_visualization import CubeSimulator


def debug_l_move():
    cube = CubeSimulator()

    print("=== Debugging L move step by step ===")
    print("Initial state:")
    print(
        f"U left: {[cube.state['U'][0][0], cube.state['U'][1][0], cube.state['U'][2][0]]}"
    )
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

    # Apply L move manually to trace what should happen
    print("Expected L move should do:")
    print("U left ← F left: ['G', 'G', 'G']")
    print("F left ← D left: ['Y', 'Y', 'Y']")
    print("D left ← B right (reversed): ['B', 'B', 'B'] → ['B', 'B', 'B']")
    print("B right ← U left (reversed): ['W', 'W', 'W'] → ['W', 'W', 'W']")
    print()

    # Now apply actual L move
    cube.execute_move("L")
    print("After L move:")
    print(
        f"U left: {[cube.state['U'][0][0], cube.state['U'][1][0], cube.state['U'][2][0]]}"
    )
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

    # Test what two L moves should do
    cube2 = CubeSimulator()
    cube2.execute_move("L")
    cube2.execute_move("L")
    print("After L L (L2):")
    print(
        f"U left: {[cube2.state['U'][0][0], cube2.state['U'][1][0], cube2.state['U'][2][0]]}"
    )
    print(
        f"F left: {[cube2.state['F'][0][0], cube2.state['F'][1][0], cube2.state['F'][2][0]]}"
    )
    print(
        f"D left: {[cube2.state['D'][0][0], cube2.state['D'][1][0], cube2.state['D'][2][0]]}"
    )
    print(
        f"B right: {[cube2.state['B'][0][2], cube2.state['B'][1][2], cube2.state['B'][2][2]]}"
    )


if __name__ == "__main__":
    debug_l_move()
