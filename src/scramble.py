"""
Scramble generation for various puzzle types.
"""

import random


class ScrambleGenerator:
    """Base class for scramble generators."""

    def generate(self):
        """Generate a scramble sequence."""
        raise NotImplementedError("Subclasses must implement generate()")


class ThreeByThreeScramble(ScrambleGenerator):
    """WCA-compliant 3x3x3 Rubik's cube scramble generator."""

    FACES = ["U", "D", "L", "R", "F", "B"]
    MODIFIERS = ["", "'", "2"]

    # Define opposite faces for WCA compliance
    OPPOSITE_FACES = {"U": "D", "D": "U", "L": "R", "R": "L", "F": "B", "B": "F"}

    def __init__(self, length=20):
        self.length = length

    def generate(self):
        """Generate a WCA-compliant 3x3 scramble sequence."""
        sequence = []
        last_face = None
        second_last_face = None

        for _ in range(self.length):
            valid_faces = self.FACES.copy()

            # Remove last face (no consecutive same face moves)
            if last_face in valid_faces:
                valid_faces.remove(last_face)

            # Remove opposite of last face if last two moves were on opposite faces
            if (
                last_face
                and second_last_face
                and last_face == self.OPPOSITE_FACES.get(second_last_face)
            ):
                if self.OPPOSITE_FACES[last_face] in valid_faces:
                    valid_faces.remove(self.OPPOSITE_FACES[last_face])

            face = random.choice(valid_faces)
            modifier = random.choice(self.MODIFIERS)
            sequence.append(face + modifier)

            # Update face history
            second_last_face = last_face
            last_face = face

        return " ".join(sequence)


class TwoByTwoScramble(ScrambleGenerator):
    """WCA-compliant 2x2x2 pocket cube scramble generator."""

    FACES = ["U", "R", "F"]
    MODIFIERS = ["", "'", "2"]

    def __init__(self, length=11):
        self.length = length

    def generate(self):
        """Generate a WCA-compliant 2x2 scramble sequence."""
        sequence = []
        last_face = None

        for _ in range(self.length):
            # For 2x2, we only avoid consecutive moves on the same face
            valid_faces = self.FACES.copy()
            if last_face in valid_faces:
                valid_faces.remove(last_face)

            face = random.choice(valid_faces)
            modifier = random.choice(self.MODIFIERS)
            sequence.append(face + modifier)
            last_face = face

        return " ".join(sequence)


class FourByFourScramble(ScrambleGenerator):
    """WCA-compliant 4x4x4 cube scramble generator."""

    OUTER_FACES = ["U", "D", "L", "R", "F", "B"]
    WIDE_FACES = ["Uw", "Dw", "Lw", "Rw", "Fw", "Bw"]
    MODIFIERS = ["", "'", "2"]

    # Define opposite faces
    OPPOSITE_FACES = {
        "U": "D",
        "D": "U",
        "Uw": "Dw",
        "Dw": "Uw",
        "L": "R",
        "R": "L",
        "Lw": "Rw",
        "Rw": "Lw",
        "F": "B",
        "B": "F",
        "Fw": "Bw",
        "Bw": "Fw",
    }

    # Define face families (outer and wide moves of same axis)
    FACE_FAMILIES = {
        "U": ["U", "Uw"],
        "D": ["D", "Dw"],
        "Uw": ["U", "Uw"],
        "Dw": ["D", "Dw"],
        "L": ["L", "Lw"],
        "R": ["R", "Rw"],
        "Lw": ["L", "Lw"],
        "Rw": ["R", "Rw"],
        "F": ["F", "Fw"],
        "B": ["B", "Bw"],
        "Fw": ["F", "Fw"],
        "Bw": ["B", "Bw"],
    }

    def __init__(self, length=40):
        self.length = length

    def generate(self):
        """Generate a WCA-compliant 4x4 scramble sequence."""
        sequence = []
        all_faces = self.OUTER_FACES + self.WIDE_FACES
        last_face = None
        second_last_face = None

        for _ in range(self.length):
            valid_faces = all_faces.copy()

            # Remove moves from the same face family as the last move
            if last_face:
                family = self.FACE_FAMILIES.get(last_face, [last_face])
                for face in family:
                    if face in valid_faces:
                        valid_faces.remove(face)

            # Remove opposite face moves if last two were on opposite faces
            if (
                last_face
                and second_last_face
                and last_face in self.OPPOSITE_FACES
                and self.OPPOSITE_FACES[last_face] == second_last_face
            ):
                opposite_family = self.FACE_FAMILIES.get(
                    self.OPPOSITE_FACES[last_face], []
                )
                for face in opposite_family:
                    if face in valid_faces:
                        valid_faces.remove(face)

            face = random.choice(valid_faces)
            modifier = random.choice(self.MODIFIERS)
            sequence.append(face + modifier)

            # Update face history
            second_last_face = last_face
            last_face = face

        return " ".join(sequence)


class FiveByFiveScramble(ScrambleGenerator):
    """WCA-compliant 5x5x5 cube scramble generator."""

    OUTER_FACES = ["U", "D", "L", "R", "F", "B"]
    WIDE_FACES = ["Uw", "Dw", "Lw", "Rw", "Fw", "Bw"]
    MODIFIERS = ["", "'", "2"]

    # Define opposite faces
    OPPOSITE_FACES = {
        "U": "D",
        "D": "U",
        "Uw": "Dw",
        "Dw": "Uw",
        "L": "R",
        "R": "L",
        "Lw": "Rw",
        "Rw": "Lw",
        "F": "B",
        "B": "F",
        "Fw": "Bw",
        "Bw": "Fw",
    }

    # Define face families
    FACE_FAMILIES = {
        "U": ["U", "Uw"],
        "D": ["D", "Dw"],
        "Uw": ["U", "Uw"],
        "Dw": ["D", "Dw"],
        "L": ["L", "Lw"],
        "R": ["R", "Rw"],
        "Lw": ["L", "Lw"],
        "Rw": ["R", "Rw"],
        "F": ["F", "Fw"],
        "B": ["B", "Bw"],
        "Fw": ["F", "Fw"],
        "Bw": ["B", "Bw"],
    }

    def __init__(self, length=60):
        self.length = length

    def generate(self):
        """Generate a WCA-compliant 5x5 scramble sequence."""
        sequence = []
        all_faces = self.OUTER_FACES + self.WIDE_FACES
        last_face = None
        second_last_face = None

        for _ in range(self.length):
            valid_faces = all_faces.copy()

            # Remove moves from the same face family as the last move
            if last_face:
                family = self.FACE_FAMILIES.get(last_face, [last_face])
                for face in family:
                    if face in valid_faces:
                        valid_faces.remove(face)

            # Remove opposite face moves if last two were on opposite faces
            if (
                last_face
                and second_last_face
                and last_face in self.OPPOSITE_FACES
                and self.OPPOSITE_FACES[last_face] == second_last_face
            ):
                opposite_family = self.FACE_FAMILIES.get(
                    self.OPPOSITE_FACES[last_face], []
                )
                for face in opposite_family:
                    if face in valid_faces:
                        valid_faces.remove(face)

            face = random.choice(valid_faces)
            modifier = random.choice(self.MODIFIERS)
            sequence.append(face + modifier)

            # Update face history
            second_last_face = last_face
            last_face = face

        return " ".join(sequence)


class PyraminxScramble(ScrambleGenerator):
    """WCA-compliant Pyraminx scramble generator."""

    FACES = ["U", "L", "R", "B"]
    TIP_MOVES = ["u", "l", "r", "b"]
    MODIFIERS = ["", "'"]

    def __init__(self, length=11):
        self.length = length

    def generate(self):
        """Generate a WCA-compliant Pyraminx scramble sequence."""
        sequence = []
        last_face = None

        # Generate main scramble moves
        for _ in range(self.length):
            valid_faces = self.FACES.copy()
            if last_face in valid_faces:
                valid_faces.remove(last_face)

            face = random.choice(valid_faces)
            modifier = random.choice(self.MODIFIERS)
            sequence.append(face + modifier)
            last_face = face

        # Add tip moves
        tip_sequence = []
        for tip in self.TIP_MOVES:
            if random.choice([True, False]):  # 50% chance for each tip
                modifier = random.choice(self.MODIFIERS)
                tip_sequence.append(tip + modifier)

        if tip_sequence:
            sequence.extend(tip_sequence)

        return " ".join(sequence)


class SkewbScramble(ScrambleGenerator):
    """WCA-compliant Skewb scramble generator."""

    FACES = ["U", "L", "R", "B"]
    MODIFIERS = ["", "'"]

    def __init__(self, length=11):
        self.length = length

    def generate(self):
        """Generate a WCA-compliant Skewb scramble sequence."""
        sequence = []
        last_face = None

        for _ in range(self.length):
            valid_faces = self.FACES.copy()
            if last_face in valid_faces:
                valid_faces.remove(last_face)

            face = random.choice(valid_faces)
            modifier = random.choice(self.MODIFIERS)
            sequence.append(face + modifier)
            last_face = face

        return " ".join(sequence)


class MegaminxScramble(ScrambleGenerator):
    """WCA-compliant Megaminx scramble generator."""

    MOVES = ["U", "D"]
    MODIFIERS = ["", "'"]

    def __init__(self, length=77):  # 7 rounds of 11 moves each
        self.length = length

    def generate(self):
        """Generate a WCA-compliant Megaminx scramble sequence."""
        sequence = []

        # Megaminx scrambles follow a specific pattern
        rounds = self.length // 11
        remaining = self.length % 11

        for round_num in range(rounds):
            # Each round: 7 moves + R++ U' or R-- U'
            for _ in range(7):
                move = random.choice(self.MOVES)
                modifier = random.choice(self.MODIFIERS)
                sequence.append(move + modifier)

            # Add rotation
            if random.choice([True, False]):
                sequence.append("R++")
            else:
                sequence.append("R--")
            sequence.append("U'")

        # Add remaining moves
        for _ in range(remaining):
            move = random.choice(self.MOVES)
            modifier = random.choice(self.MODIFIERS)
            sequence.append(move + modifier)

        return " ".join(sequence)


class SquareOneScramble(ScrambleGenerator):
    """WCA-compliant Square-1 scramble generator."""

    def __init__(self, length=20):
        self.length = length

    def generate(self):
        """Generate a WCA-compliant Square-1 scramble sequence."""
        sequence = []

        for _ in range(self.length):
            # Generate random twist values (-5 to +6, avoiding 0)
            top = random.randint(-5, 6)
            if top == 0:
                top = random.choice([-1, 1])

            bottom = random.randint(-5, 6)
            if bottom == 0:
                bottom = random.choice([-1, 1])

            # Format the move
            if top > 0:
                top_str = f"{top}"
            else:
                top_str = str(top)

            if bottom > 0:
                bottom_str = f"{bottom}"
            else:
                bottom_str = str(bottom)

            sequence.append(f"({top_str},{bottom_str})")

            # Add slice move (except for last move)
            if _ < self.length - 1:
                sequence.append("/")

        return " ".join(sequence)


class ScrambleManager:
    """Manages different scramble types and generation."""

    SCRAMBLE_TYPES = {
        "3x3x3": ThreeByThreeScramble,
        "2x2x2": TwoByTwoScramble,
        "4x4x4": FourByFourScramble,
        "5x5x5": FiveByFiveScramble,
        "Pyraminx": PyraminxScramble,
        "Skewb": SkewbScramble,
        "Megaminx": MegaminxScramble,
        "Square-1": SquareOneScramble,
    }

    def __init__(self, scramble_type="3x3x3"):
        self.current_type = scramble_type
        self.generator = self.SCRAMBLE_TYPES[scramble_type]()
        self.history = []
        self.current_index = -1

    def set_type(self, scramble_type):
        """Change the scramble type."""
        if scramble_type in self.SCRAMBLE_TYPES:
            self.current_type = scramble_type
            self.generator = self.SCRAMBLE_TYPES[scramble_type]()
            return True
        return False

    def generate_new(self):
        """Generate a new scramble and add to history."""
        scramble = self.generator.generate()
        self.history.append(scramble)
        self.current_index = len(self.history) - 1
        return scramble

    def get_current(self):
        """Get the current scramble."""
        if self.history and 0 <= self.current_index < len(self.history):
            return self.history[self.current_index]
        return self.generate_new()

    def get_previous(self):
        """Go to previous scramble in history."""
        if self.current_index > 0:
            self.current_index -= 1
            return self.history[self.current_index]
        return None

    def get_next(self):
        """Go to next scramble in history."""
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            return self.history[self.current_index]
        return self.generate_new()

    def get_available_types(self):
        """Get list of available scramble types."""
        return list(self.SCRAMBLE_TYPES.keys())
