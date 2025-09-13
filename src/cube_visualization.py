"""
3D Cube visualization for PSTimer with proper cube simulation.
"""

import tkinter as tk
from tkinter import Canvas
import math
import copy


class CubeSimulator:
    """Simulates a 3x3x3 Rubik's cube state and moves."""

    def __init__(self):
        self.reset_to_solved()

    def reset_to_solved(self):
        """Reset cube to solved state with correct WCA orientation."""
        # Standard WCA cube orientation: White top, Green front
        self.state = {
            "U": [["W", "W", "W"], ["W", "W", "W"], ["W", "W", "W"]],  # White (Up)
            "D": [["Y", "Y", "Y"], ["Y", "Y", "Y"], ["Y", "Y", "Y"]],  # Yellow (Down)
            "F": [["G", "G", "G"], ["G", "G", "G"], ["G", "G", "G"]],  # Green (Front)
            "B": [["B", "B", "B"], ["B", "B", "B"], ["B", "B", "B"]],  # Blue (Back)
            "L": [["O", "O", "O"], ["O", "O", "O"], ["O", "O", "O"]],  # Orange (Left)
            "R": [["R", "R", "R"], ["R", "R", "R"], ["R", "R", "R"]],  # Red (Right)
        }

    def _rotate_face_clockwise(self, face):
        """Rotate a face 90 degrees clockwise."""
        old_face = [row[:] for row in self.state[face]]
        for i in range(3):
            for j in range(3):
                self.state[face][i][j] = old_face[2 - j][i]

    def _rotate_face_counterclockwise(self, face):
        """Rotate a face 90 degrees counterclockwise."""
        old_face = [row[:] for row in self.state[face]]
        for i in range(3):
            for j in range(3):
                self.state[face][i][j] = old_face[j][2 - i]

    def _move_u(self):
        """Perform U move (Up face clockwise)."""
        self._rotate_face_clockwise("U")
        # Correctly cycle the top rows of F, R, B, L in reverse direction
        temp = self.state["F"][0][:]
        self.state["F"][0] = self.state["R"][0][:]
        self.state["R"][0] = self.state["B"][0][:]
        self.state["B"][0] = self.state["L"][0][:]
        self.state["L"][0] = temp

    def _move_d(self):
        """Perform D move (Down face clockwise)."""
        self._rotate_face_clockwise("D")
        # Correctly cycle the bottom rows of F, L, B, R (opposite of U)
        temp = self.state["F"][2][:]
        self.state["F"][2] = self.state["L"][2][:]
        self.state["L"][2] = self.state["B"][2][:]
        self.state["B"][2] = self.state["R"][2][:]
        self.state["R"][2] = temp

    def _move_f(self):
        """Perform F move (Front face clockwise)."""
        self._rotate_face_clockwise("F")
        # Correctly cycle U, R, D, L edges
        temp = self.state["U"][2][:]
        self.state["U"][2][0] = self.state["L"][2][2]
        self.state["U"][2][1] = self.state["L"][1][2]
        self.state["U"][2][2] = self.state["L"][0][2]

        self.state["L"][0][2] = self.state["D"][0][0]
        self.state["L"][1][2] = self.state["D"][0][1]
        self.state["L"][2][2] = self.state["D"][0][2]

        self.state["D"][0][0] = self.state["R"][2][0]
        self.state["D"][0][1] = self.state["R"][1][0]
        self.state["D"][0][2] = self.state["R"][0][0]

        self.state["R"][0][0] = temp[2]
        self.state["R"][1][0] = temp[1]
        self.state["R"][2][0] = temp[0]

    def _move_b(self):
        """Perform B move (Back face clockwise)."""
        self._rotate_face_clockwise("B")
        # Correctly cycle U, L, D, R edges (note: B is opposite F)
        temp = self.state["U"][0][:]
        self.state["U"][0][0] = self.state["R"][0][2]
        self.state["U"][0][1] = self.state["R"][1][2]
        self.state["U"][0][2] = self.state["R"][2][2]

        self.state["R"][0][2] = self.state["D"][2][2]
        self.state["R"][1][2] = self.state["D"][2][1]
        self.state["R"][2][2] = self.state["D"][2][0]

        self.state["D"][2][0] = self.state["L"][0][0]
        self.state["D"][2][1] = self.state["L"][1][0]
        self.state["D"][2][2] = self.state["L"][2][0]

        self.state["L"][0][0] = temp[2]
        self.state["L"][1][0] = temp[1]
        self.state["L"][2][0] = temp[0]

    def _move_l(self):
        """Perform L move (Left face clockwise)."""
        self._rotate_face_clockwise("L")
        # L' cycle is reverse of current L: U ← B ← D ← F ← U
        temp = [self.state["U"][0][0], self.state["U"][1][0], self.state["U"][2][0]]

        # U left column ← B right column (reversed)
        self.state["U"][0][0] = self.state["B"][2][2]
        self.state["U"][1][0] = self.state["B"][1][2]
        self.state["U"][2][0] = self.state["B"][0][2]

        # B right column ← D left column (reversed)
        self.state["B"][0][2] = self.state["D"][2][0]
        self.state["B"][1][2] = self.state["D"][1][0]
        self.state["B"][2][2] = self.state["D"][0][0]

        # D left column ← F left column
        self.state["D"][0][0] = self.state["F"][0][0]
        self.state["D"][1][0] = self.state["F"][1][0]
        self.state["D"][2][0] = self.state["F"][2][0]

        # F left column ← U left column
        self.state["F"][0][0] = temp[0]
        self.state["F"][1][0] = temp[1]
        self.state["F"][2][0] = temp[2]

    def _move_r(self):
        """Perform R move (Right face clockwise) - WCA standard."""
        self._rotate_face_clockwise("R")
        # Correct WCA R move cycle: U←F←D←B←U
        temp = [self.state["U"][0][2], self.state["U"][1][2], self.state["U"][2][2]]

        # U right column ← F right column
        self.state["U"][0][2] = self.state["F"][0][2]
        self.state["U"][1][2] = self.state["F"][1][2]
        self.state["U"][2][2] = self.state["F"][2][2]

        # F right column ← D right column
        self.state["F"][0][2] = self.state["D"][0][2]
        self.state["F"][1][2] = self.state["D"][1][2]
        self.state["F"][2][2] = self.state["D"][2][2]

        # D right column ← B left column (reversed order)
        self.state["D"][0][2] = self.state["B"][2][0]
        self.state["D"][1][2] = self.state["B"][1][0]
        self.state["D"][2][2] = self.state["B"][0][0]

        # B left column ← U right column (reversed order)
        self.state["B"][0][0] = temp[2]
        self.state["B"][1][0] = temp[1]
        self.state["B"][2][0] = temp[0]

    def _move_u_prime(self):
        """U' move: Up face counterclockwise"""
        self._rotate_face_counterclockwise("U")
        # Reverse the cycle: F←L←B←R←F (original direction)
        temp = self.state["F"][0][:]
        self.state["F"][0] = self.state["L"][0][:]
        self.state["L"][0] = self.state["B"][0][:]
        self.state["B"][0] = self.state["R"][0][:]
        self.state["R"][0] = temp

    def _move_d_prime(self):
        """D' move: Down face counterclockwise"""
        self._rotate_face_counterclockwise("D")
        # Reverse the cycle: F←R←B←L←F (opposite of D move)
        temp = self.state["F"][2][:]
        self.state["F"][2] = self.state["R"][2][:]
        self.state["R"][2] = self.state["B"][2][:]
        self.state["B"][2] = self.state["L"][2][:]
        self.state["L"][2] = temp

    def _move_f_prime(self):
        """F' move: Front face counterclockwise"""
        self._rotate_face_counterclockwise("F")
        # Reverse the F move cycle
        temp = self.state["U"][2][:]
        self.state["U"][2][0] = self.state["R"][0][0]
        self.state["U"][2][1] = self.state["R"][1][0]
        self.state["U"][2][2] = self.state["R"][2][0]

        self.state["R"][0][0] = self.state["D"][0][2]
        self.state["R"][1][0] = self.state["D"][0][1]
        self.state["R"][2][0] = self.state["D"][0][0]

        self.state["D"][0][0] = self.state["L"][2][2]
        self.state["D"][0][1] = self.state["L"][1][2]
        self.state["D"][0][2] = self.state["L"][0][2]

        self.state["L"][0][2] = temp[2]
        self.state["L"][1][2] = temp[1]
        self.state["L"][2][2] = temp[0]

    def _move_b_prime(self):
        """B' move: Back face counterclockwise"""
        self._rotate_face_counterclockwise("B")
        # Reverse the B move cycle
        temp = self.state["U"][0][:]
        self.state["U"][0][0] = self.state["L"][0][0]
        self.state["U"][0][1] = self.state["L"][1][0]
        self.state["U"][0][2] = self.state["L"][2][0]

        self.state["L"][0][0] = self.state["D"][2][2]
        self.state["L"][1][0] = self.state["D"][2][1]
        self.state["L"][2][0] = self.state["D"][2][0]

        self.state["D"][2][0] = self.state["R"][2][2]
        self.state["D"][2][1] = self.state["R"][1][2]
        self.state["D"][2][2] = self.state["R"][0][2]

        self.state["R"][0][2] = temp[2]
        self.state["R"][1][2] = temp[1]
        self.state["R"][2][2] = temp[0]

    def _move_l_prime(self):
        """L' move: Left face counterclockwise"""
        self._rotate_face_counterclockwise("L")
        # L move cycle: U ← F ← D ← B ← U (B is reversed)
        temp = [self.state["U"][0][0], self.state["U"][1][0], self.state["U"][2][0]]

        # U left column ← F left column
        self.state["U"][0][0] = self.state["F"][0][0]
        self.state["U"][1][0] = self.state["F"][1][0]
        self.state["U"][2][0] = self.state["F"][2][0]

        # F left column ← D left column
        self.state["F"][0][0] = self.state["D"][0][0]
        self.state["F"][1][0] = self.state["D"][1][0]
        self.state["F"][2][0] = self.state["D"][2][0]

        # D left column ← B right column (reversed)
        self.state["D"][0][0] = self.state["B"][2][2]
        self.state["D"][1][0] = self.state["B"][1][2]
        self.state["D"][2][0] = self.state["B"][0][2]

        # B right column ← U left column (reversed)
        self.state["B"][0][2] = temp[2]
        self.state["B"][1][2] = temp[1]
        self.state["B"][2][2] = temp[0]

    def _move_r_prime(self):
        """R' move: Right face counterclockwise"""
        self._rotate_face_counterclockwise("R")
        # R' cycle is opposite of R: U←B←D←F←U
        temp = [self.state["U"][0][2], self.state["U"][1][2], self.state["U"][2][2]]

        # U right column ← B left column (reversed)
        self.state["U"][0][2] = self.state["B"][2][0]
        self.state["U"][1][2] = self.state["B"][1][0]
        self.state["U"][2][2] = self.state["B"][0][0]

        # B left column ← D right column (reversed)
        self.state["B"][0][0] = self.state["D"][2][2]
        self.state["B"][1][0] = self.state["D"][1][2]
        self.state["B"][2][0] = self.state["D"][0][2]

        # D right column ← F right column
        self.state["D"][0][2] = self.state["F"][0][2]
        self.state["D"][1][2] = self.state["F"][1][2]
        self.state["D"][2][2] = self.state["F"][2][2]

        # F right column ← U right column
        self.state["F"][0][2] = temp[0]
        self.state["F"][1][2] = temp[1]
        self.state["F"][2][2] = temp[2]

    def _rotation_x(self):
        """x rotation: Makes Blue (back) become front
        Cycle: B->F, U->B, D->U, F->D"""
        # Save the faces that will move
        temp_f = [row[:] for row in self.state["F"]]
        temp_u = [row[:] for row in self.state["U"]]
        temp_b = [row[:] for row in self.state["B"]]
        temp_d = [row[:] for row in self.state["D"]]

        # Apply cycle: B->F, U->B, D->U, F->D
        self.state["F"] = [
            [temp_b[2 - i][2 - j] for j in range(3)] for i in range(3)
        ]  # Back to Front (flipped)
        self.state["B"] = [
            [temp_u[2 - i][2 - j] for j in range(3)] for i in range(3)
        ]  # Up to Back (flipped)
        self.state["U"] = temp_d  # Down to Up
        self.state["D"] = temp_f  # Front to Down

        # Rotate side faces
        self._rotate_face_counterclockwise("R")
        self._rotate_face_clockwise("L")

    def _rotation_x_prime(self):
        """x' rotation: Makes Green (front) become top
        Reverse cycle: F->U, B->D, U->F, D->B"""
        # Save the faces that will move
        temp_f = [row[:] for row in self.state["F"]]
        temp_u = [row[:] for row in self.state["U"]]
        temp_b = [row[:] for row in self.state["B"]]
        temp_d = [row[:] for row in self.state["D"]]

        # Apply reverse cycle: F->U, B->D, U->F, D->B
        self.state["U"] = temp_f  # Front to Up
        self.state["D"] = [
            [temp_b[2 - i][2 - j] for j in range(3)] for i in range(3)
        ]  # Back to Down (flipped)
        self.state["F"] = temp_u  # Up to Front
        self.state["B"] = [
            [temp_d[2 - i][2 - j] for j in range(3)] for i in range(3)
        ]  # Down to Back (flipped)

        # Rotate side faces in reverse
        self._rotate_face_clockwise("R")
        self._rotate_face_counterclockwise("L")

    def _rotation_y(self):
        """y rotation: Rotate entire cube around U-D axis (like U move but whole cube)
        F -> L, L -> B, B -> R, R -> F"""
        # Save the faces that will move
        temp_f = [row[:] for row in self.state["F"]]
        temp_l = [row[:] for row in self.state["L"]]
        temp_b = [row[:] for row in self.state["B"]]
        temp_r = [row[:] for row in self.state["R"]]

        # Rotate faces: F -> L -> B -> R -> F
        self.state["L"] = temp_f
        self.state["B"] = temp_l
        self.state["R"] = temp_b
        self.state["F"] = temp_r

        # Rotate U and D faces
        self._rotate_face_clockwise("U")
        self._rotate_face_counterclockwise("D")

    def _rotation_y_prime(self):
        """y' rotation: Reverse y rotation"""
        # Save the faces that will move
        temp_f = [row[:] for row in self.state["F"]]
        temp_l = [row[:] for row in self.state["L"]]
        temp_b = [row[:] for row in self.state["B"]]
        temp_r = [row[:] for row in self.state["R"]]

        # Rotate faces in reverse: F -> R -> B -> L -> F
        self.state["R"] = temp_f
        self.state["B"] = temp_r
        self.state["L"] = temp_b
        self.state["F"] = temp_l

        # Rotate U and D faces in reverse
        self._rotate_face_counterclockwise("U")
        self._rotate_face_clockwise("D")

    def _rotation_z(self):
        """z rotation: Rotate entire cube around F-B axis (like F move but whole cube)
        After z: Orange (left) becomes what you see (new top)"""
        # Save the faces that will move
        temp_u = [row[:] for row in self.state["U"]]
        temp_l = [row[:] for row in self.state["L"]]
        temp_d = [row[:] for row in self.state["D"]]
        temp_r = [row[:] for row in self.state["R"]]

        # For z rotation: U->R, L->U, D->L, R->D
        # This makes Orange (L) go to top (U)
        self.state["R"] = temp_u
        self.state["U"] = temp_l
        self.state["L"] = temp_d
        self.state["D"] = temp_r

        # Rotate F and B faces
        self._rotate_face_clockwise("F")
        self._rotate_face_counterclockwise("B")

    def _rotation_z_prime(self):
        """z' rotation: Reverse z rotation
        After z': Red (right) becomes what you see (new top)"""
        # Save the faces that will move
        temp_u = [row[:] for row in self.state["U"]]
        temp_l = [row[:] for row in self.state["L"]]
        temp_d = [row[:] for row in self.state["D"]]
        temp_r = [row[:] for row in self.state["R"]]

        # For z' rotation (reverse of z): U->L, R->U, D->R, L->D
        # This makes Red (R) go to top (U)
        self.state["L"] = temp_u
        self.state["U"] = temp_r
        self.state["R"] = temp_d
        self.state["D"] = temp_l

        # Rotate F and B faces in reverse
        self._rotate_face_counterclockwise("F")
        self._rotate_face_clockwise("B")

    def execute_move(self, move):
        """Execute a single move (e.g., 'U', 'R'', 'F2')."""
        move = move.strip()
        if not move:
            return

        base_move = move[0]
        modifier = move[1:] if len(move) > 1 else ""

        # Map base moves to methods
        move_methods = {
            "U": self._move_u,
            "D": self._move_d,
            "F": self._move_f,
            "B": self._move_b,
            "L": self._move_l,
            "R": self._move_r,
            "x": self._rotation_x,
            "y": self._rotation_y,
            "z": self._rotation_z,
        }

        # Map prime moves to counterclockwise methods
        prime_methods = {
            "U": self._move_u_prime,
            "D": self._move_d_prime,
            "F": self._move_f_prime,
            "B": self._move_b_prime,
            "L": self._move_l_prime,
            "R": self._move_r_prime,
            "x": self._rotation_x_prime,
            "y": self._rotation_y_prime,
            "z": self._rotation_z_prime,
        }

        if base_move not in move_methods:
            return  # Invalid move

        # Execute based on modifier
        if modifier == "":
            move_methods[base_move]()
        elif modifier == "'":
            # Prime = counterclockwise
            if base_move in prime_methods:
                prime_methods[base_move]()
        elif modifier == "2":
            # Double turn = 2 clockwise turns
            move_methods[base_move]()
            move_methods[base_move]()
            # Special case for rotations with 2
            if base_move in ["x", "y", "z"]:
                pass  # Two rotations already applied above

    def apply_scramble(self, scramble):
        """Apply a scramble sequence to the cube."""
        if not scramble:
            return

        moves = scramble.split()
        for move in moves:
            self.execute_move(move)


class CubeVisualization:
    """Displays a 2D unfolded view of the cube showing all 6 faces."""

    # Color mapping for cube faces
    COLOR_MAP = {
        "W": "#ffffff",  # White
        "Y": "#ffff00",  # Yellow
        "R": "#ff0000",  # Red
        "O": "#ff8c00",  # Orange
        "G": "#00ff00",  # Green
        "B": "#0000ff",  # Blue
    }

    def __init__(self, parent, width=400, height=300):
        self.canvas = Canvas(parent, width=width, height=height, bg="#f0f0f0")
        self.width = width
        self.height = height

        # Initialize cube simulator
        self.cube = CubeSimulator()

        # Face size for drawing
        self.face_size = 66  # Increased for better visibility
        self.sticker_size = 20  # Increased for better visibility

        self._draw_cube_unfolded()

    def _init_solved_state(self):
        """Initialize a solved cube state."""
        return {
            "U": [["W"] * 3 for _ in range(3)],  # White
            "D": [["Y"] * 3 for _ in range(3)],  # Yellow
            "F": [["R"] * 3 for _ in range(3)],  # Red
            "B": [["O"] * 3 for _ in range(3)],  # Orange
            "L": [["G"] * 3 for _ in range(3)],  # Green
            "R": [["B"] * 3 for _ in range(3)],  # Blue
        }

    def _draw_cube_unfolded(self):
        """Draw the cube in an unfolded 2D layout showing all 6 faces."""
        self.canvas.delete("all")

        # Calculate positions for the cross layout:
        #     [U]
        # [L] [F] [R] [B]
        #     [D]

        center_x = self.width // 2
        center_y = self.height // 2

        # Face positions in the unfolded layout
        face_positions = {
            "U": (center_x, center_y - self.face_size),  # Top
            "F": (center_x, center_y),  # Center
            "L": (center_x - self.face_size, center_y),  # Left
            "R": (center_x + self.face_size, center_y),  # Right
            "B": (center_x + 2 * self.face_size, center_y),  # Far right
            "D": (center_x, center_y + self.face_size),  # Bottom
        }

        # Draw each face
        for face_name, (x, y) in face_positions.items():
            self._draw_face_2d(face_name, x, y)

        # Add labels
        self._draw_face_labels(face_positions)

    def _draw_face_2d(self, face_name, center_x, center_y):
        """Draw a single face as a 3x3 grid."""
        if face_name not in self.cube.state:
            return

        # Calculate starting position (top-left corner)
        start_x = center_x - self.face_size // 2
        start_y = center_y - self.face_size // 2

        # Draw 3x3 grid of stickers
        for row in range(3):
            for col in range(3):
                x = start_x + col * self.sticker_size
                y = start_y + row * self.sticker_size

                # Get sticker color
                sticker = self.cube.state[face_name][row][col]
                color = self.COLOR_MAP.get(sticker, "#cccccc")

                # Draw sticker with better border
                self.canvas.create_rectangle(
                    x + 1,
                    y + 1,
                    x + self.sticker_size - 1,
                    y + self.sticker_size - 1,
                    fill=color,
                    outline="black",
                    width=1,
                )

    def _draw_face_labels(self, face_positions):
        """Draw labels for each face."""
        for face_name, (x, y) in face_positions.items():
            # Position label above each face
            label_y = y - self.face_size // 2 - 15
            self.canvas.create_text(
                x, label_y, text=face_name, font=("Arial", 10, "bold"), fill="black"
            )

    def apply_scramble(self, scramble):
        """Apply a scramble to the cube state."""
        # Reset to solved state first
        self.cube.reset_to_solved()

        # Apply the scramble
        self.cube.apply_scramble(scramble)

        # Redraw the cube
        self._draw_cube_unfolded()

    def reset_to_solved(self):
        """Reset cube to solved state."""
        self.cube.reset_to_solved()
        self._draw_cube_unfolded()

    def get_canvas(self):
        """Get the canvas widget."""
        return self.canvas
