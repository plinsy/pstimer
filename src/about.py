"""
About dialog for PSTimer.
"""

import tkinter as tk
from tkinter import ttk


class AboutDialog:
    """About dialog showing application information."""

    def __init__(self, parent, theme_manager):
        self.parent = parent
        self.theme_manager = theme_manager

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("About PSTimer")
        self.dialog.geometry("400x350")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center the dialog
        self.dialog.update_idletasks()
        x = (
            parent.winfo_rootx()
            + parent.winfo_width() // 2
            - self.dialog.winfo_width() // 2
        )
        y = (
            parent.winfo_rooty()
            + parent.winfo_height() // 2
            - self.dialog.winfo_height() // 2
        )
        self.dialog.geometry(f"+{x}+{y}")

        theme = self.theme_manager.get_theme()
        self.dialog.configure(bg=theme["bg"])

        self._create_widgets()

    def _create_widgets(self):
        """Create the about dialog widgets."""
        theme = self.theme_manager.get_theme()

        # Main frame
        main_frame = tk.Frame(self.dialog, bg=theme["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # App name and version
        app_label = tk.Label(
            main_frame,
            text="PSTimer",
            font=(theme["font_family"], 24, "bold"),
            bg=theme["bg"],
            fg=theme["text_primary"],
        )
        app_label.pack(pady=(0, 5))

        version_label = tk.Label(
            main_frame,
            text="Version 1.0.0",
            font=(theme["font_family"], 12),
            bg=theme["bg"],
            fg=theme["text_secondary"],
        )
        version_label.pack(pady=(0, 20))

        # Description
        desc_text = (
            "A modern speedcubing timer inspired by csTimer.\n"
            "Built with Python and Tkinter for cross-platform compatibility."
        )

        desc_label = tk.Label(
            main_frame,
            text=desc_text,
            font=(theme["font_family"], 11),
            bg=theme["bg"],
            fg=theme["text_primary"],
            justify=tk.CENTER,
            wraplength=350,
        )
        desc_label.pack(pady=(0, 20))

        # Features
        features_frame = tk.Frame(main_frame, bg=theme["bg"])
        features_frame.pack(pady=(0, 20))

        tk.Label(
            features_frame,
            text="Features:",
            font=(theme["font_family"], 12, "bold"),
            bg=theme["bg"],
            fg=theme["text_primary"],
        ).pack(anchor=tk.W)

        features = [
            "• High-precision timing",
            "• Multiple puzzle support",
            "• Advanced statistics (ao5, ao12, ao100)",
            "• 3D cube visualization",
            "• Session management",
            "• Multiple themes",
            "• Window transparency for multitasking",
        ]

        for feature in features:
            tk.Label(
                features_frame,
                text=feature,
                font=(theme["font_family"], 10),
                bg=theme["bg"],
                fg=theme["text_primary"],
            ).pack(anchor=tk.W, padx=10)

        # Controls
        controls_frame = tk.Frame(main_frame, bg=theme["bg"])
        controls_frame.pack(pady=(10, 20))

        tk.Label(
            controls_frame,
            text="Controls:",
            font=(theme["font_family"], 12, "bold"),
            bg=theme["bg"],
            fg=theme["text_primary"],
        ).pack(anchor=tk.W)

        controls = [
            "• Space: Hold to ready, release to start",
            "• Any key: Stop timer",
            "• S: New scramble",
            "• R: Reset timer",
            "• Ctrl + =: Increase transparency",
            "• Ctrl + -: Decrease transparency",
            "• Ctrl + 0: Reset transparency",
        ]

        for control in controls:
            tk.Label(
                controls_frame,
                text=control,
                font=(theme["font_family"], 10),
                bg=theme["bg"],
                fg=theme["text_primary"],
            ).pack(anchor=tk.W, padx=10)

        # Credits
        credits_label = tk.Label(
            main_frame,
            text="Inspired by csTimer • Built with ❤️ for the speedcubing community",
            font=(theme["font_family"], 9),
            bg=theme["bg"],
            fg=theme["text_secondary"],
        )
        credits_label.pack(pady=(10, 0))

        # Close button
        close_btn = tk.Button(
            main_frame,
            text="Close",
            command=self.dialog.destroy,
            width=12,
            font=(theme["font_family"], 10),
            bg=theme["accent"],
            fg="white",
        )
        close_btn.pack(pady=(20, 0))

    def show(self):
        """Show the dialog."""
        self.dialog.wait_window()


def show_about_dialog(parent, theme_manager):
    """Show the about dialog."""
    dialog = AboutDialog(parent, theme_manager)
    dialog.show()
