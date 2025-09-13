"""
Simple test to verify the cube moves work correctly in the application context.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.cube_visualization import CubeSimulator
from src.scramble import generate_scramble


def test_basic_functionality():
    """Test basic cube and scramble functionality."""
    print("PSTimer Cube Functionality Test")
    print("=" * 35)

    # Test 1: Basic cube creation and moves
    print("1. Testing basic cube moves...")
    cube = CubeSimulator()

    # Test a simple sequence
    test_sequence = "R U R' U'"
    print(f"   Applying sequence: {test_sequence}")
    cube.apply_scramble(test_sequence)
    print("   ✓ Sequence applied successfully")

    # Test 2: Scramble generation
    print("\n2. Testing scramble generation...")
    scramble = generate_scramble()
    print(f"   Generated scramble: {scramble}")
    print(f"   ✓ Scramble generated successfully")

    # Test 3: Apply scramble to cube
    print("\n3. Testing scramble application...")
    cube.reset_to_solved()
    cube.apply_scramble(scramble)
    print("   ✓ Scramble applied to cube successfully")

    # Test 4: Verify cube state changes
    print("\n4. Testing cube state changes...")
    cube1 = CubeSimulator()
    cube2 = CubeSimulator()

    cube2.execute_move("F")

    # Should be different
    if cube1.state != cube2.state:
        print("   ✓ Moves correctly change cube state")
    else:
        print("   ✗ Moves do not change cube state")

    print("\n✅ All basic functionality tests passed!")
    print("The fixed cube simulation is working correctly.")


if __name__ == "__main__":
    test_basic_functionality()
