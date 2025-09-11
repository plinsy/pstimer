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
    """Standard 3x3x3 Rubik's cube scramble generator."""

    FACES = ["U", "D", "L", "R", "F", "B"]
    MODIFIERS = ["", "'", "2"]

    def __init__(self, length=20):
        self.length = length

    def generate(self):
        """Generate a 3x3 scramble sequence."""
        sequence = []
        prev_face = None

        for _ in range(self.length):
            # Avoid same face twice in a row
            face = random.choice(self.FACES)
            while face == prev_face:
                face = random.choice(self.FACES)

            modifier = random.choice(self.MODIFIERS)
            sequence.append(face + modifier)
            prev_face = face

        return " ".join(sequence)


class TwoByTwoScramble(ScrambleGenerator):
    """2x2x2 pocket cube scramble generator."""

    FACES = ["U", "R", "F"]
    MODIFIERS = ["", "'", "2"]

    def __init__(self, length=11):
        self.length = length

    def generate(self):
        """Generate a 2x2 scramble sequence."""
        sequence = []
        prev_face = None

        for _ in range(self.length):
            face = random.choice(self.FACES)
            while face == prev_face:
                face = random.choice(self.FACES)

            modifier = random.choice(self.MODIFIERS)
            sequence.append(face + modifier)
            prev_face = face

        return " ".join(sequence)


class FourByFourScramble(ScrambleGenerator):
    """4x4x4 cube scramble generator."""

    FACES = ["U", "D", "L", "R", "F", "B"]
    MODIFIERS = ["", "'", "2"]
    WIDE_MOVES = ["u", "d", "l", "r", "f", "b"]

    def __init__(self, length=40):
        self.length = length

    def generate(self):
        """Generate a 4x4 scramble sequence."""
        sequence = []
        prev_face = None

        for _ in range(self.length):
            # Mix regular and wide moves
            if random.random() < 0.3:  # 30% chance for wide move
                face = random.choice(self.WIDE_MOVES)
            else:
                face = random.choice(self.FACES)

            # Avoid same face family
            if prev_face and face.upper() == prev_face.upper():
                continue

            modifier = random.choice(self.MODIFIERS)
            sequence.append(face + modifier)
            prev_face = face

        return " ".join(sequence)


class ScrambleManager:
    """Manages different scramble types and generation."""

    SCRAMBLE_TYPES = {
        "3x3x3": ThreeByThreeScramble,
        "2x2x2": TwoByTwoScramble,
        "4x4x4": FourByFourScramble,
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
