#!/usr/bin/env python3
"""
Simple test to demonstrate transparency features.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

def demo_transparency():
    """Create a demo window to test transparency alongside PSTimer."""
    
    # Create a demo background window
    demo = tk.Tk()
    demo.title("Background Application (Simulate Code Editor)")
    demo.geometry("800x600")
    demo.configure(bg="white")
    
    # Add some content to simulate a real application
    title = tk.Label(demo, text="PSTimer Transparency Demo", 
                     font=("Arial", 20, "bold"), bg="white")
    title.pack(pady=20)
    
    instructions = tk.Label(demo, text="""
This window simulates a code editor or document.

1. Launch PSTimer (python main.py)
2. Use Ctrl + - to make PSTimer transparent
3. You should be able to see this text through PSTimer
4. Use Ctrl + = to make PSTimer more opaque
5. Use Ctrl + 0 to reset transparency

Try different transparency levels to find what works best
for your multitasking needs!
""", font=("Arial", 12), bg="white", justify=tk.LEFT)
    instructions.pack(padx=20, pady=20)
    
    # Add a text area to simulate code
    code_text = tk.Text(demo, height=15, width=60, font=("Courier", 10))
    code_text.pack(padx=20, pady=20)
    
    # Add some sample code
    sample_code = """def rubiks_cube_solve():
    # F2L (First Two Layers)
    cross = "F R U R' U' F'"
    f2l_pair1 = "R U R' F R F'"
    f2l_pair2 = "U R U' R' U F R F'"
    
    # OLL (Orientation of Last Layer)  
    oll_algorithm = "R U R' U R U2 R'"
    
    # PLL (Permutation of Last Layer)
    pll_algorithm = "R U R' F' R U R' U' R' F R2 U' R'"
    
    return "Solved!"

# Practice with PSTimer overlay!
solve_time = rubiks_cube_solve()
print(f"Practice time: {solve_time}")"""
    
    code_text.insert("1.0", sample_code)
    
    # Add close button
    close_btn = tk.Button(demo, text="Close Demo", command=demo.destroy,
                         font=("Arial", 12), bg="#007acc", fg="white")
    close_btn.pack(pady=10)
    
    demo.mainloop()

if __name__ == "__main__":
    print("Starting PSTimer Transparency Demo...")
    print("This will create a background window to test transparency against.")
    print("Launch PSTimer in another terminal with: python main.py")
    demo_transparency()
