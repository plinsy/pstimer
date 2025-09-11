#!/usr/bin/env python3
"""
PSTimer Multitasking Demo - Showcasing Transparency + Compact Mode
"""

import sys
import os
import tkinter as tk
from tkinter import ttk

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def create_demo_workspace():
    """Create a demo workspace to showcase PSTimer's multitasking features."""

    demo = tk.Tk()
    demo.title("PSTimer Multitasking Demo - Background Workspace")
    demo.geometry("1000x700")
    demo.configure(bg="#1e1e1e")  # Dark background like VS Code

    # Header
    header = tk.Label(
        demo,
        text="🎯 PSTimer Multitasking Demo",
        font=("Arial", 20, "bold"),
        bg="#1e1e1e",
        fg="#ffffff",
    )
    header.pack(pady=20)

    # Instructions
    instructions = tk.Label(
        demo,
        text="""
🚀 Welcome to PSTimer's Advanced Multitasking Features Demo!

This window simulates your coding/work environment. Follow these steps:

1️⃣  LAUNCH PSTIMER: Open another terminal and run 'python main.py'

2️⃣  TRY TRANSPARENCY:
    • Press Ctrl + - (in PSTimer) to make it transparent
    • You should see this text through the PSTimer window
    • Press Ctrl + = to make it more solid
    • Press Ctrl + 0 to reset to fully opaque

3️⃣  TRY COMPACT MODE:
    • Press Ctrl + M to enter compact mode
    • PSTimer becomes a small overlay showing just timer + scramble
    • Press Ctrl + 1-4 to position it in different corners
    • Try Ctrl + 2 (top-right) for coding workflows

4️⃣  COMBINE FEATURES:
    • Use Ctrl + M for compact mode
    • Use Ctrl + - for transparency  
    • Position with Ctrl + 1-4
    • Perfect for extreme multitasking!

5️⃣  PRACTICE WORKFLOW:
    • Set up your ideal transparency + position
    • Practice solving while "working" in this window
    • Timer stays visible and accessible
    
Press Ctrl + M (in PSTimer) to exit compact mode when done.
        """,
        font=("Arial", 12),
        bg="#1e1e1e",
        fg="#cccccc",
        justify=tk.LEFT,
    )
    instructions.pack(padx=20, pady=20)

    # Simulated code editor
    code_frame = tk.Frame(demo, bg="#2d2d2d")
    code_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    code_title = tk.Label(
        code_frame,
        text="📄 simulated_work.py",
        font=("Courier", 12, "bold"),
        bg="#2d2d2d",
        fg="#ffffff",
    )
    code_title.pack(anchor=tk.W, padx=10, pady=5)

    # Code text area
    code_text = tk.Text(
        code_frame,
        height=20,
        width=80,
        font=("Courier", 10),
        bg="#1e1e1e",
        fg="#d4d4d4",
        insertbackground="#ffffff",
        selectbackground="#264f78",
    )
    code_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Sample code
    sample_code = '''def speedcubing_practice_session():
    """
    Multitask like a pro with PSTimer!
    Perfect transparency + compact mode = ultimate productivity
    """
    
    # Setup your optimal configuration
    transparency_level = 0.6  # 60% for good visibility balance
    compact_position = "top-right"  # Corner positioning
    
    # Rubik's cube algorithms for practice
    algorithms = {
        "OLL": {
            "T-Perm": "R U R' F' R U R' U' R' F R2 U' R'",
            "Y-Perm": "F R U' R' U' R U R' F' R U R' U' R' F R F'",
            "J-Perm": "R U R' F' R U R' U' R' F R2 U' R'",
        },
        "F2L": {
            "Case1": "R U' R' F R F'", 
            "Case2": "F' U F R U R'",
            "Case3": "R U R' U' R U R'",
        }
    }
    
    # Practice while coding - this is where PSTimer shines!
    def practice_while_working():
        """
        With PSTimer's compact mode + transparency:
        1. Keep timer visible in corner (Ctrl + 1-4)
        2. Make it transparent (Ctrl + -)  
        3. Practice F2L while coding
        4. Track improvement over time
        """
        
        print("🎯 PSTimer Features Demo:")
        print("• Compact Mode: Minimal footprint, maximum visibility")
        print("• Transparency: See-through for multitasking")
        print("• Corner Positioning: Stay out of the way")
        print("• Always On Top: Never lose track of your timer")
        print("• Full Functionality: All features work in compact mode")
        
        return "Perfect for speedcubers who code! 🚀"
    
    # Try these PSTimer shortcuts while viewing this code:
    shortcuts = {
        "Ctrl + M": "Toggle compact mode",
        "Ctrl + 1": "Top-left corner", 
        "Ctrl + 2": "Top-right corner (great for coding)",
        "Ctrl + 3": "Bottom-left corner",
        "Ctrl + 4": "Bottom-right corner", 
        "Ctrl + -": "More transparent",
        "Ctrl + +": "More opaque",
        "Ctrl + 0": "Reset transparency",
        "Space": "Timer control (works everywhere!)",
        "S": "New scramble",
        "R": "Reset timer"
    }
    
    print("\\n🎮 Try the shortcuts above with PSTimer running!")
    print("Perfect combination: Compact mode + 60% transparency + top-right corner")
    
    return practice_while_working()

# Run the demo
if __name__ == "__main__":
    result = speedcubing_practice_session()
    print(f"\\n✅ Result: {result}")
    
    # Add your own code here and practice with PSTimer!
    # The compact timer will stay visible in your chosen corner.'''

    code_text.insert("1.0", sample_code)
    code_text.config(state=tk.DISABLED)

    # Control buttons
    button_frame = tk.Frame(demo, bg="#1e1e1e")
    button_frame.pack(pady=10)

    position_label = tk.Label(
        button_frame,
        text="🎯 Recommended: Ctrl+M → Ctrl+2 → Ctrl+- (compact + top-right + transparent)",
        font=("Arial", 10, "bold"),
        bg="#1e1e1e",
        fg="#4CAF50",
    )
    position_label.pack(pady=5)

    close_btn = tk.Button(
        button_frame,
        text="Close Demo",
        command=demo.destroy,
        font=("Arial", 12),
        bg="#007acc",
        fg="white",
        padx=20,
    )
    close_btn.pack(pady=10)

    # Show usage tip
    tip_label = tk.Label(
        demo,
        text="💡 Tip: This demo stays open so you can test PSTimer's transparency and compact mode over it!",
        font=("Arial", 9),
        bg="#1e1e1e",
        fg="#ffcc00",
    )
    tip_label.pack(pady=5)

    return demo


if __name__ == "__main__":
    print("🚀 Starting PSTimer Multitasking Demo...")
    print("This creates a background workspace to test transparency and compact mode.")
    print("Launch PSTimer with: python main.py")
    print("Then try the shortcuts mentioned in the demo window!")

    demo_app = create_demo_workspace()
    demo_app.mainloop()
