#!/usr/bin/env python3
"""
Test script to verify WCA compliance of scramble algorithms.
"""

from src.scramble import ScrambleManager
import re


def test_3x3_compliance():
    """Test 3x3x3 WCA compliance."""
    print("Testing 3x3x3 WCA compliance...")
    sm = ScrambleManager("3x3x3")

    for i in range(5):
        scramble = sm.generate_new()
        print(f"  {i+1}: {scramble}")

        # Basic checks
        moves = scramble.split()
        assert len(moves) == 20, f"Expected 20 moves, got {len(moves)}"

        # Check for consecutive same face moves
        for j in range(len(moves) - 1):
            current_face = moves[j][0]
            next_face = moves[j + 1][0]
            assert (
                current_face != next_face
            ), f"Consecutive same face moves: {moves[j]} {moves[j+1]}"

    print("  ✓ 3x3x3 compliance verified")


def test_2x2_compliance():
    """Test 2x2x2 WCA compliance."""
    print("\nTesting 2x2x2 WCA compliance...")
    sm = ScrambleManager("2x2x2")

    for i in range(5):
        scramble = sm.generate_new()
        print(f"  {i+1}: {scramble}")

        moves = scramble.split()
        assert len(moves) == 11, f"Expected 11 moves, got {len(moves)}"

        # Check only U, R, F faces are used
        for move in moves:
            face = move[0]
            assert face in ["U", "R", "F"], f"Invalid face for 2x2: {face}"

        # Check for consecutive same face moves
        for j in range(len(moves) - 1):
            current_face = moves[j][0]
            next_face = moves[j + 1][0]
            assert (
                current_face != next_face
            ), f"Consecutive same face moves: {moves[j]} {moves[j+1]}"

    print("  ✓ 2x2x2 compliance verified")


def test_4x4_compliance():
    """Test 4x4x4 WCA compliance."""
    print("\nTesting 4x4x4 WCA compliance...")
    sm = ScrambleManager("4x4x4")

    for i in range(3):
        scramble = sm.generate_new()
        print(f"  {i+1}: {scramble}")

        moves = scramble.split()
        assert len(moves) == 40, f"Expected 40 moves, got {len(moves)}"

        # Check valid faces (U, D, L, R, F, B, Uw, Dw, Lw, Rw, Fw, Bw)
        valid_faces = {"U", "D", "L", "R", "F", "B", "Uw", "Dw", "Lw", "Rw", "Fw", "Bw"}
        for move in moves:
            face = move.rstrip("'2")
            assert face in valid_faces, f"Invalid face for 4x4: {face}"

    print("  ✓ 4x4x4 compliance verified")


def test_pyraminx_compliance():
    """Test Pyraminx WCA compliance."""
    print("\nTesting Pyraminx WCA compliance...")
    sm = ScrambleManager("Pyraminx")

    for i in range(3):
        scramble = sm.generate_new()
        print(f"  {i+1}: {scramble}")

        moves = scramble.split()

        # Check valid faces
        valid_faces = {"U", "L", "R", "B", "u", "l", "r", "b"}
        for move in moves:
            face = move.rstrip("'")
            assert face in valid_faces, f"Invalid face for Pyraminx: {face}"

    print("  ✓ Pyraminx compliance verified")


def test_square1_compliance():
    """Test Square-1 WCA compliance."""
    print("\nTesting Square-1 WCA compliance...")
    sm = ScrambleManager("Square-1")

    for i in range(3):
        scramble = sm.generate_new()
        print(f"  {i+1}: {scramble}")

        # Check format: alternating moves and slices
        parts = scramble.split()

        # Should have pattern: move / move / move / ... / move
        for j, part in enumerate(parts):
            if j % 2 == 0:  # Even indices should be moves
                assert re.match(
                    r"\(-?\d+,-?\d+\)", part
                ), f"Invalid move format: {part}"
            else:  # Odd indices should be slices
                assert part == "/", f"Expected '/', got: {part}"

    print("  ✓ Square-1 compliance verified")


def test_all_puzzle_types():
    """Test that all puzzle types generate valid scrambles."""
    print("\nTesting all puzzle types...")
    sm = ScrambleManager()

    for puzzle_type in sm.get_available_types():
        print(f"  Testing {puzzle_type}...")
        sm.set_type(puzzle_type)
        scramble = sm.generate_new()
        assert (
            scramble and len(scramble.strip()) > 0
        ), f"Empty scramble for {puzzle_type}"
        print(f"    Sample: {scramble[:50]}{'...' if len(scramble) > 50 else ''}")

    print("  ✓ All puzzle types working")


if __name__ == "__main__":
    print("WCA Compliance Test Suite")
    print("=" * 40)

    try:
        test_3x3_compliance()
        test_2x2_compliance()
        test_4x4_compliance()
        test_pyraminx_compliance()
        test_square1_compliance()
        test_all_puzzle_types()

        print("\n" + "=" * 40)
        print("🎉 All WCA compliance tests passed!")
        print("Your PSTimer now generates WCA-compliant scrambles!")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise
