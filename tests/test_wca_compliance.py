"""
Test WCA compliance of scramble algorithms.
"""

import pytest
import re
from src.scramble import ScrambleManager, ThreeByThreeScramble, TwoByTwoScramble


class TestWCACompliance:
    """Test WCA compliance for all puzzle types."""

    def test_3x3_basic_compliance(self, scramble_manager):
        """Test basic 3x3x3 WCA compliance rules."""
        scramble_manager.set_type("3x3x3")

        for _ in range(10):  # Test multiple scrambles
            scramble = scramble_manager.generate_new()
            moves = scramble.split()

            # Check scramble length
            assert len(moves) == 20, f"Expected 20 moves, got {len(moves)}"

            # Check no consecutive same face moves
            for i in range(len(moves) - 1):
                current_face = moves[i][0]
                next_face = moves[i + 1][0]
                assert current_face != next_face, \
                    f"Consecutive same face moves: {moves[i]} {moves[i+1]}"

    def test_3x3_opposite_face_restriction(self):
        """Test 3x3x3 opposite face move restrictions."""
        generator = ThreeByThreeScramble()

        for _ in range(5):
            scramble = generator.generate()
            moves = scramble.split()

            # Check no more than 2 consecutive moves on opposite faces
            for i in range(len(moves) - 2):
                faces = [moves[i][0], moves[i+1][0], moves[i+2][0]]

                # Check if first and second are opposite
                if faces[0] in generator.OPPOSITE_FACES and \
                   faces[1] == generator.OPPOSITE_FACES[faces[0]]:
                    # Third move should not be on the same face as first
                    assert faces[2] != faces[0], \
                        f"Three consecutive opposite face moves: {moves[i:i+3]}"

    def test_3x3_valid_moves(self):
        """Test that all 3x3x3 moves are valid."""
        generator = ThreeByThreeScramble()
        valid_faces = set(generator.FACES)
        valid_modifiers = set(generator.MODIFIERS)

        for _ in range(3):
            scramble = generator.generate()
            moves = scramble.split()

            for move in moves:
                face = move[0]
                modifier = move[1:] if len(move) > 1 else ""

                assert face in valid_faces, f"Invalid face: {face}"
                assert modifier in valid_modifiers, f"Invalid modifier: {modifier}"

    def test_2x2_compliance(self):
        """Test 2x2x2 WCA compliance."""
        sm = ScrambleManager("2x2x2")

        for _ in range(5):
            scramble = sm.generate_new()
            moves = scramble.split()

            # Check scramble length
            assert len(moves) == 11, f"Expected 11 moves, got {len(moves)}"

            # Check only U, R, F faces are used
            for move in moves:
                face = move[0]
                assert face in ["U", "R", "F"], f"Invalid face for 2x2: {face}"

            # Check no consecutive same face moves
            for i in range(len(moves) - 1):
                current_face = moves[i][0]
                next_face = moves[i + 1][0]
                assert current_face != next_face, \
                    f"Consecutive same face moves: {moves[i]} {moves[i+1]}"

    @pytest.mark.parametrize("puzzle_type,expected_faces", [
        ("3x3x3", ["U", "D", "L", "R", "F", "B"]),
        ("2x2x2", ["U", "R", "F"]),
        ("4x4x4", ["U", "D", "L", "R", "F", "B", "Uw", "Dw", "Lw", "Rw", "Fw", "Bw"]),
        ("Pyraminx", ["U", "L", "R", "B", "u", "l", "r", "b"]),
    ])
    def test_puzzle_face_restrictions(self, puzzle_type, expected_faces):
        """Test that each puzzle type uses only valid faces."""
        sm = ScrambleManager(puzzle_type)
        scramble = sm.generate_new()
        moves = scramble.split()

        for move in moves:
            # Extract face (handle wide moves like 'Uw')
            if move.startswith(('Uw', 'Dw', 'Lw', 'Rw', 'Fw', 'Bw')):
                face = move[:2]
            else:
                face = move[0]

            assert face in expected_faces, \
                f"Invalid face '{face}' for {puzzle_type}: {move}"

    def test_scramble_randomness(self):
        """Test that scrambles are reasonably random."""
        sm = ScrambleManager("3x3x3")

        # Generate multiple scrambles and check they're different
        scrambles = [sm.generate_new() for _ in range(10)]
        unique_scrambles = set(scrambles)

        # Should have at least 8 unique scrambles out of 10
        assert len(unique_scrambles) >= 8, \
            f"Scrambles not random enough: {len(unique_scrambles)}/10 unique"

    def test_move_notation_format(self):
        """Test that move notation follows correct format."""
        sm = ScrambleManager("3x3x3")

        # Regex pattern for valid move notation
        move_pattern = re.compile(r"^[UDLRFB]w?[2']?$")

        for _ in range(3):
            scramble = sm.generate_new()
            moves = scramble.split()

            for move in moves:
                assert move_pattern.match(move), f"Invalid move notation: {move}"
