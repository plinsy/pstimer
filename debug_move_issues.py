"""
Debug the specific move issues identified in the test.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.cube_visualization import CubeSimulator


def debug_l_moves():
    """Debug L and L' move issues."""
    print("DEBUGGING L MOVES")
    print("=" * 30)

    # Test L move
    cube = CubeSimulator()
    print(f"Before L - White face: {cube.state['U']}")
    cube.execute_move("L")
    print(f"After L - White face: {cube.state['U']}")
    print(f"Expected: [['B', 'W', 'W'], ['B', 'W', 'W'], ['B', 'W', 'W']]")
    print(f"Got:      [['G', 'W', 'W'], ['G', 'W', 'W'], ['G', 'W', 'W']]")
    print("Issue: L move puts Green in left column, but test expects Blue")

    # Test L' move
    cube2 = CubeSimulator()
    print(f"\nBefore L' - White face: {cube2.state['U']}")
    cube2.execute_move("L'")
    print(f"After L' - White face: {cube2.state['U']}")
    print(f"Expected: [['G', 'W', 'W'], ['G', 'W', 'W'], ['G', 'W', 'W']]")
    print(f"Got:      [['B', 'W', 'W'], ['B', 'W', 'W'], ['B', 'W', 'W']]")
    print("Issue: L' move puts Blue in left column, but test expects Green")
    print("CONCLUSION: L and L' moves are swapped!")


def debug_u_d_moves():
    """Debug U and D move issues."""
    print("\n" + "=" * 50)
    print("DEBUGGING U/D MOVES WITH GREEN FRONT")
    print("=" * 50)

    # Test U move with green front face
    cube = CubeSimulator()
    print(f"Before U - Green face: {cube.state['F']}")
    cube.execute_move("U")
    print(f"After U - Green face: {cube.state['F']}")
    print(f"Expected: [['R', 'R', 'R'], ['G', 'G', 'G'], ['G', 'G', 'G']]")
    print(f"Got:      [['O', 'O', 'O'], ['G', 'G', 'G'], ['G', 'G', 'G']]")
    print("Issue: U move puts Orange in top row, but test expects Red")

    # Test U' move
    cube2 = CubeSimulator()
    print(f"\nBefore U' - Green face: {cube2.state['F']}")
    cube2.execute_move("U'")
    print(f"After U' - Green face: {cube2.state['F']}")
    print(f"Expected: [['O', 'O', 'O'], ['G', 'G', 'G'], ['G', 'G', 'G']]")
    print(f"Got:      [['R', 'R', 'R'], ['G', 'G', 'G'], ['G', 'G', 'G']]")
    print("Issue: U' move puts Red in top row, but test expects Orange")
    print("CONCLUSION: U and U' moves are swapped!")

    # Test D move
    cube3 = CubeSimulator()
    print(f"\nBefore D - Green face: {cube3.state['F']}")
    cube3.execute_move("D")
    print(f"After D - Green face: {cube3.state['F']}")
    print(f"Expected: [['G', 'G', 'G'], ['G', 'G', 'G'], ['O', 'O', 'O']]")
    print(f"Got:      [['G', 'G', 'G'], ['G', 'G', 'G'], ['R', 'R', 'R']]")
    print("Issue: D move puts Red in bottom row, but test expects Orange")

    # Test D' move
    cube4 = CubeSimulator()
    print(f"\nBefore D' - Green face: {cube4.state['F']}")
    cube4.execute_move("D'")
    print(f"After D' - Green face: {cube4.state['F']}")
    print(f"Expected: [['G', 'G', 'G'], ['G', 'G', 'G'], ['R', 'R', 'R']]")
    print(f"Got:      [['G', 'G', 'G'], ['G', 'G', 'G'], ['O', 'O', 'O']]")
    print("Issue: D' move puts Orange in bottom row, but test expects Red")
    print("CONCLUSION: D and D' moves are also swapped!")


if __name__ == "__main__":
    debug_l_moves()
    debug_u_d_moves()
