"""
3D Cube visualization for PSTimer.
"""

import tkinter as tk
from tkinter import Canvas
import math


class CubeVisualization:
    """3D cube visualization widget."""

    # Color mapping for cube faces
    FACE_COLORS = {
        "U": "#ffffff",  # White (Up)
        "D": "#ffff00",  # Yellow (Down)
        "F": "#ff0000",  # Red (Front)
        "B": "#ff8c00",  # Orange (Back)
        "L": "#00ff00",  # Green (Left)
        "R": "#0000ff",  # Blue (Right)
    }

    def __init__(self, parent, width=200, height=200):
        self.canvas = Canvas(parent, width=width, height=height, bg="#f0f0f0")
        self.width = width
        self.height = height

        # 3D rotation angles
        self.angle_x = 20
        self.angle_y = 35
        self.angle_z = 0

        # Cube state (3x3x3 = 54 stickers)
        self.cube_state = self._init_solved_state()

        # Animation variables
        self.is_animating = False
        self.animation_queue = []

        self._draw_cube()

        # Bind mouse events for rotation
        self.canvas.bind("<Button-1>", self._on_mouse_press)
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.last_mouse_x = 0
        self.last_mouse_y = 0

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

    def _project_3d_to_2d(self, x, y, z):
        """Project 3D coordinates to 2D screen coordinates."""
        # Apply rotations
        rad_x = math.radians(self.angle_x)
        rad_y = math.radians(self.angle_y)
        rad_z = math.radians(self.angle_z)

        # Rotate around Y axis
        x1 = x * math.cos(rad_y) - z * math.sin(rad_y)
        z1 = x * math.sin(rad_y) + z * math.cos(rad_y)

        # Rotate around X axis
        y1 = y * math.cos(rad_x) - z1 * math.sin(rad_x)
        z2 = y * math.sin(rad_x) + z1 * math.cos(rad_x)

        # Simple perspective projection
        distance = 300
        scale = distance / (distance + z2)

        # Convert to screen coordinates
        screen_x = self.width / 2 + x1 * scale * 50
        screen_y = self.height / 2 - y1 * scale * 50

        return screen_x, screen_y

    def _draw_cube(self):
        """Draw the 3D cube on the canvas."""
        self.canvas.delete("all")

        # Define cube vertices (-1 to 1)
        cube_size = 1.0

        # Draw each face
        self._draw_face(
            "F",
            [
                (-cube_size, -cube_size, cube_size),
                (cube_size, -cube_size, cube_size),
                (cube_size, cube_size, cube_size),
                (-cube_size, cube_size, cube_size),
            ],
        )

        self._draw_face(
            "R",
            [
                (cube_size, -cube_size, cube_size),
                (cube_size, -cube_size, -cube_size),
                (cube_size, cube_size, -cube_size),
                (cube_size, cube_size, cube_size),
            ],
        )

        self._draw_face(
            "U",
            [
                (-cube_size, cube_size, cube_size),
                (cube_size, cube_size, cube_size),
                (cube_size, cube_size, -cube_size),
                (-cube_size, cube_size, -cube_size),
            ],
        )

    def _draw_face(self, face_name, corners):
        """Draw a single face of the cube."""
        # Project corners to 2D
        projected = [self._project_3d_to_2d(x, y, z) for x, y, z in corners]

        # Calculate face normal for visibility
        if not self._is_face_visible(corners):
            return

        # Draw the face outline
        points = []
        for x, y in projected:
            points.extend([x, y])

        self.canvas.create_polygon(points, outline="black", fill="lightgray", width=2)

        # Draw the 3x3 grid on the face
        self._draw_face_grid(face_name, projected)

    def _is_face_visible(self, corners):
        """Check if a face is visible (front-facing)."""
        # Simple visibility check using cross product
        v1 = [corners[1][i] - corners[0][i] for i in range(3)]
        v2 = [corners[2][i] - corners[0][i] for i in range(3)]

        # Cross product for normal
        normal_z = v1[0] * v2[1] - v1[1] * v2[0]

        return normal_z > 0

    def _draw_face_grid(self, face_name, corners):
        """Draw the 3x3 grid of stickers on a face."""
        if face_name not in self.cube_state:
            return

        # Calculate grid positions
        for row in range(3):
            for col in range(3):
                # Get corner positions for this grid cell
                x_ratio = col / 3.0
                y_ratio = row / 3.0

                # Interpolate corners
                top_left = self._interpolate_point(corners[0], corners[1], x_ratio)
                top_right = self._interpolate_point(
                    corners[0], corners[1], x_ratio + 1 / 3
                )
                bottom_left = self._interpolate_point(corners[3], corners[2], x_ratio)
                bottom_right = self._interpolate_point(
                    corners[3], corners[2], x_ratio + 1 / 3
                )

                top_left = self._interpolate_point(top_left, bottom_left, y_ratio)
                top_right = self._interpolate_point(top_right, bottom_right, y_ratio)
                bottom_left = self._interpolate_point(
                    top_left, bottom_left, y_ratio + 1 / 3
                )
                bottom_right = self._interpolate_point(
                    top_right, bottom_right, y_ratio + 1 / 3
                )

                # Get color for this sticker
                sticker_color = self._get_sticker_color(face_name, row, col)

                # Draw the sticker
                points = [*top_left, *top_right, *bottom_right, *bottom_left]
                self.canvas.create_polygon(
                    points, fill=sticker_color, outline="black", width=1
                )

    def _interpolate_point(self, p1, p2, ratio):
        """Interpolate between two 2D points."""
        return [p1[0] + (p2[0] - p1[0]) * ratio, p1[1] + (p2[1] - p1[1]) * ratio]

    def _get_sticker_color(self, face, row, col):
        """Get the color of a specific sticker."""
        sticker = self.cube_state[face][row][col]
        color_map = {
            "W": "#ffffff",  # White
            "Y": "#ffff00",  # Yellow
            "R": "#ff0000",  # Red
            "O": "#ff8c00",  # Orange
            "G": "#00ff00",  # Green
            "B": "#0000ff",  # Blue
        }
        return color_map.get(sticker, "#cccccc")

    def _on_mouse_press(self, event):
        """Handle mouse press for rotation."""
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

    def _on_mouse_drag(self, event):
        """Handle mouse drag for rotation."""
        dx = event.x - self.last_mouse_x
        dy = event.y - self.last_mouse_y

        self.angle_y += dx * 0.5
        self.angle_x += dy * 0.5

        # Keep angles in reasonable range
        self.angle_x = max(-90, min(90, self.angle_x))

        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

        self._draw_cube()

    def apply_scramble(self, scramble):
        """Apply a scramble to the cube state (simplified)."""
        # This would need a full cube simulation implementation
        # For now, just randomize colors for demonstration
        import random

        colors = ["W", "Y", "R", "O", "G", "B"]

        for face in self.cube_state:
            for row in range(3):
                for col in range(3):
                    # Keep center pieces fixed
                    if row == 1 and col == 1:
                        continue
                    self.cube_state[face][row][col] = random.choice(colors)

        self._draw_cube()

    def reset_to_solved(self):
        """Reset cube to solved state."""
        self.cube_state = self._init_solved_state()
        self._draw_cube()

    def get_canvas(self):
        """Get the canvas widget."""
        return self.canvas
