"""
Settings dialog for PSTimer.
"""

import tkinter as tk
from tkinter import ttk


class SettingsDialog:
    """Settings configuration dialog."""

    def __init__(
        self, parent, theme_manager, session_manager, current_transparency=1.0
    ):
        self.parent = parent
        self.theme_manager = theme_manager
        self.session_manager = session_manager
        self.current_transparency = current_transparency
        self.result = None

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("PSTimer Settings")
        self.dialog.geometry("400x550")  # Increased height for transparency controls
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
        """Create the settings widgets."""
        theme = self.theme_manager.get_theme()

        # Main frame
        main_frame = tk.Frame(self.dialog, bg=theme["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(
            main_frame,
            text="PSTimer Settings",
            font=(theme["font_family"], 16, "bold"),
            bg=theme["bg"],
            fg=theme["text_primary"],
        )
        title_label.pack(pady=(0, 20))

        # Theme settings
        theme_frame = tk.LabelFrame(
            main_frame,
            text="Appearance",
            font=(theme["font_family"], 12, "bold"),
            bg=theme["bg"],
            fg=theme["text_primary"],
        )
        theme_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(
            theme_frame,
            text="Theme:",
            font=(theme["font_family"], 10),
            bg=theme["bg"],
            fg=theme["text_primary"],
        ).pack(anchor=tk.W, padx=10, pady=(10, 5))

        self.theme_var = tk.StringVar(value=self.theme_manager.current_theme_name)
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=self.theme_manager.get_available_themes(),
            state="readonly",
            width=30,
        )
        theme_combo.pack(anchor=tk.W, padx=10, pady=(0, 10))

        # Window transparency
        tk.Label(
            theme_frame,
            text="Window transparency:",
            font=(theme["font_family"], 10),
            bg=theme["bg"],
            fg=theme["text_primary"],
        ).pack(anchor=tk.W, padx=10, pady=(10, 5))

        tk.Label(
            theme_frame,
            text="(Lower values make window more see-through for multitasking)",
            font=(theme["font_family"], 8),
            bg=theme["bg"],
            fg=theme["text_secondary"],
        ).pack(anchor=tk.W, padx=10, pady=(0, 5))

        transparency_frame = tk.Frame(theme_frame, bg=theme["bg"])
        transparency_frame.pack(anchor=tk.W, padx=10, pady=(0, 10))

        self.transparency_var = tk.DoubleVar(value=self.current_transparency)
        transparency_scale = tk.Scale(
            transparency_frame,
            from_=0.3,  # 30% minimum transparency
            to=1.0,  # 100% opaque (no transparency)
            resolution=0.05,
            orient=tk.HORIZONTAL,
            variable=self.transparency_var,
            length=200,
            font=(theme["font_family"], 9),
            bg=theme["bg"],
            fg=theme["text_primary"],
            highlightbackground=theme["bg"],
            troughcolor=theme["panel_bg"],
            activebackground=theme["accent"],
        )
        transparency_scale.pack(side=tk.LEFT)

        transparency_label = tk.Label(
            transparency_frame,
            text="100%",
            font=(theme["font_family"], 9),
            bg=theme["bg"],
            fg=theme["text_secondary"],
            width=4,
        )
        transparency_label.pack(side=tk.LEFT, padx=(10, 0))

        def update_transparency_label(*args):
            value = self.transparency_var.get()
            percentage = int(value * 100)
            transparency_label.config(text=f"{percentage}%")

        self.transparency_var.trace("w", update_transparency_label)

        # Timer settings
        timer_frame = tk.LabelFrame(
            main_frame,
            text="Timer",
            font=(theme["font_family"], 12, "bold"),
            bg=theme["bg"],
            fg=theme["text_primary"],
        )
        timer_frame.pack(fill=tk.X, pady=(0, 15))

        # Inspection time
        self.inspection_var = tk.BooleanVar(value=False)
        inspection_check = tk.Checkbutton(
            timer_frame,
            text="Enable 15-second inspection time",
            variable=self.inspection_var,
            font=(theme["font_family"], 10),
            bg=theme["bg"],
            fg=theme["text_primary"],
            selectcolor=theme["bg"],
        )
        inspection_check.pack(anchor=tk.W, padx=10, pady=10)

        # Hold time for ready state
        tk.Label(
            timer_frame,
            text="Hold time for ready state (ms):",
            font=(theme["font_family"], 10),
            bg=theme["bg"],
            fg=theme["text_primary"],
        ).pack(anchor=tk.W, padx=10, pady=(5, 0))

        self.hold_time_var = tk.StringVar(value="300")
        hold_time_entry = tk.Entry(
            timer_frame,
            textvariable=self.hold_time_var,
            width=10,
            font=(theme["mono_font"], 10),
        )
        hold_time_entry.pack(anchor=tk.W, padx=10, pady=(5, 10))

        # Scramble settings
        scramble_frame = tk.LabelFrame(
            main_frame,
            text="Scrambles",
            font=(theme["font_family"], 12, "bold"),
            bg=theme["bg"],
            fg=theme["text_primary"],
        )
        scramble_frame.pack(fill=tk.X, pady=(0, 15))

        # Puzzle type selection
        tk.Label(
            scramble_frame,
            text="Puzzle type:",
            font=(theme["font_family"], 10),
            bg=theme["bg"],
            fg=theme["text_primary"],
        ).pack(anchor=tk.W, padx=10, pady=(10, 5))

        # Import scramble manager to get available types
        from .scramble import ScrambleManager

        available_types = ScrambleManager().get_available_types()

        self.puzzle_type_var = tk.StringVar(value="3x3x3")
        puzzle_combo = ttk.Combobox(
            scramble_frame,
            textvariable=self.puzzle_type_var,
            values=available_types,
            state="readonly",
            width=30,
        )
        puzzle_combo.pack(anchor=tk.W, padx=10, pady=(0, 10))

        # Scramble length (only for applicable puzzles)
        tk.Label(
            scramble_frame,
            text="Scramble length (for cubes):",
            font=(theme["font_family"], 10),
            bg=theme["bg"],
            fg=theme["text_primary"],
        ).pack(anchor=tk.W, padx=10, pady=(5, 0))

        self.scramble_length_var = tk.StringVar(value="20")
        scramble_length_entry = tk.Entry(
            scramble_frame,
            textvariable=self.scramble_length_var,
            width=10,
            font=(theme["mono_font"], 10),
        )
        scramble_length_entry.pack(anchor=tk.W, padx=10, pady=(0, 10))

        # Session settings
        session_frame = tk.LabelFrame(
            main_frame,
            text="Session",
            font=(theme["font_family"], 12, "bold"),
            bg=theme["bg"],
            fg=theme["text_primary"],
        )
        session_frame.pack(fill=tk.X, pady=(0, 15))

        # Auto-save session
        self.autosave_var = tk.BooleanVar(value=True)
        autosave_check = tk.Checkbutton(
            session_frame,
            text="Auto-save session data",
            variable=self.autosave_var,
            font=(theme["font_family"], 10),
            bg=theme["bg"],
            fg=theme["text_primary"],
            selectcolor=theme["bg"],
        )
        autosave_check.pack(anchor=tk.W, padx=10, pady=10)

        # Statistics to show
        tk.Label(
            session_frame,
            text="Statistics to display:",
            font=(theme["font_family"], 10),
            bg=theme["bg"],
            fg=theme["text_primary"],
        ).pack(anchor=tk.W, padx=10, pady=(5, 0))

        stats_frame = tk.Frame(session_frame, bg=theme["bg"])
        stats_frame.pack(anchor=tk.W, padx=20, pady=5)

        self.show_mo3_var = tk.BooleanVar(value=True)
        self.show_ao5_var = tk.BooleanVar(value=True)
        self.show_ao12_var = tk.BooleanVar(value=True)
        self.show_ao100_var = tk.BooleanVar(value=True)

        for var, text in [
            (self.show_mo3_var, "mo3"),
            (self.show_ao5_var, "ao5"),
            (self.show_ao12_var, "ao12"),
            (self.show_ao100_var, "ao100"),
        ]:
            tk.Checkbutton(
                stats_frame,
                text=text,
                variable=var,
                font=(theme["font_family"], 9),
                bg=theme["bg"],
                fg=theme["text_primary"],
                selectcolor=theme["bg"],
            ).pack(anchor=tk.W)

        # Buttons
        button_frame = tk.Frame(main_frame, bg=theme["bg"])
        button_frame.pack(fill=tk.X, pady=(20, 0))

        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self._cancel,
            width=12,
            font=(theme["font_family"], 10),
        )
        cancel_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # Apply button
        apply_btn = tk.Button(
            button_frame,
            text="Apply",
            command=self._apply,
            width=12,
            font=(theme["font_family"], 10),
            bg=theme["accent"],
            fg="white",
        )
        apply_btn.pack(side=tk.RIGHT)

        # Reset to defaults button
        reset_btn = tk.Button(
            button_frame,
            text="Reset to Defaults",
            command=self._reset_defaults,
            width=15,
            font=(theme["font_family"], 10),
        )
        reset_btn.pack(side=tk.LEFT)

    def _apply(self):
        """Apply the settings."""
        # Apply theme change
        new_theme = self.theme_var.get()
        if new_theme != self.theme_manager.current_theme_name:
            self.theme_manager.set_theme(new_theme)

        # Store other settings (would need to be implemented in main app)
        self.result = {
            "theme": self.theme_var.get(),
            "transparency": self.transparency_var.get(),
            "puzzle_type": self.puzzle_type_var.get(),
            "inspection": self.inspection_var.get(),
            "hold_time": int(self.hold_time_var.get()),
            "scramble_length": int(self.scramble_length_var.get()),
            "autosave": self.autosave_var.get(),
            "show_mo3": self.show_mo3_var.get(),
            "show_ao5": self.show_ao5_var.get(),
            "show_ao12": self.show_ao12_var.get(),
            "show_ao100": self.show_ao100_var.get(),
        }

        self.dialog.destroy()

    def _cancel(self):
        """Cancel the dialog."""
        self.dialog.destroy()

    def _reset_defaults(self):
        """Reset all settings to defaults."""
        self.theme_var.set("csTimer")
        self.transparency_var.set(1.0)
        self.puzzle_type_var.set("3x3x3")
        self.inspection_var.set(False)
        self.hold_time_var.set("300")
        self.scramble_length_var.set("20")
        self.autosave_var.set(True)
        self.show_mo3_var.set(True)
        self.show_ao5_var.set(True)
        self.show_ao12_var.set(True)
        self.show_ao100_var.set(True)

    def show(self):
        """Show the dialog and return the result."""
        self.dialog.wait_window()
        return self.result


def show_settings_dialog(
    parent, theme_manager, session_manager, current_transparency=1.0
):
    """Show the settings dialog."""
    dialog = SettingsDialog(
        parent, theme_manager, session_manager, current_transparency
    )
    return dialog.show()
