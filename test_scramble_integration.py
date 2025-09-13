#!/usr/bin/env python3
"""
Test the integration between scramble generation and cube visualization.
"""

from src.scramble import ScrambleManager
from src.cube_visualization import CubeVisualization
import tkinter as tk


def test_scramble_integration():
    """Test that scrambles are properly applied to the cube visualization."""

    # Create scramble manager
    scramble_manager = ScrambleManager()

    # Generate a test scramble
    scramble = scramble_manager.generate_new()
    print(f"Generated scramble: {scramble}")

    # Create a simple window for testing
    root = tk.Tk()
    root.title("Cube Visualization Test")
    root.geometry("400x350")

    # Create cube visualization
    cube_viz = CubeVisualization(root, width=350, height=250)
    cube_viz.get_canvas().pack(padx=10, pady=10)

    # Apply the scramble
    cube_viz.apply_scramble(scramble)

    # Add test button to generate new scrambles
    def new_scramble():
        new_scramble_sequence = scramble_manager.generate_new()
        print(f"New scramble: {new_scramble_sequence}")
        cube_viz.apply_scramble(new_scramble_sequence)

    def reset_cube():
        cube_viz.reset_to_solved()

    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    tk.Button(button_frame, text="New Scramble", command=new_scramble).pack(
        side=tk.LEFT, padx=5
    )
    tk.Button(button_frame, text="Reset", command=reset_cube).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Quit", command=root.quit).pack(side=tk.LEFT, padx=5)

    print("Starting test GUI - close the window when done testing")
    root.mainloop()


if __name__ == "__main__":
    test_scramble_integration()
