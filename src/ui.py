"""
Main UI for PSTimer - csTimer-inspired Rubik's cube timer.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

from .timer import Stopwatch
from .scramble import ScrambleManager
from .statistics import SessionManager, SolveTime
from .themes import ThemeManager
from .cube_visualization import CubeVisualization
from .settings import show_settings_dialog
from .about import show_about_dialog


class PSTimerUI(tk.Tk):
    """Main application window for PSTimer."""

    def __init__(self):
        super().__init__()

        # Initialize core components
        self.stopwatch = Stopwatch()
        self.scramble_manager = ScrambleManager()
        self.session_manager = SessionManager()
        self.theme_manager = ThemeManager()

        # UI state
        self.is_ready = False
        self.ready_start_time = None
        self.inspection_time = None
        self.inspection_enabled = False
        self.hold_time = 300  # Default hold time in milliseconds
        self.transparency = 1.0  # Default transparency (fully opaque)
        self.user_settings = {}  # Store user settings

        # Compact mode state
        self.is_compact_mode = False
        self.compact_position = (
            "top-right"  # top-left, top-right, bottom-left, bottom-right
        )
        self.normal_geometry = None  # Store normal window size/position
        self.compact_widgets = {}  # Store compact mode widgets

        # Animation variables
        self.pulse_scale = 1.0
        self.bg_animation_id = None

        self._setup_window()
        self._create_ui()
        self._setup_bindings()
        self._update_session_display()  # Initialize session display
        self._start_ui_loop()

    def _setup_window(self):
        """Setup main window properties."""
        self.title("PSTimer - Speedcubing Timer")
        self.geometry("1200x800")
        self.minsize(900, 600)

        # Apply theme
        theme = self.theme_manager.get_theme()
        self.configure(bg=theme["bg"])

        # Configure grid weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def _create_ui(self):
        """Create the main UI layout."""
        theme = self.theme_manager.get_theme()

        # Top navigation bar
        self._create_top_bar()

        # Main content area
        main_frame = tk.Frame(self, bg=theme["bg"])
        main_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # Left panel (statistics)
        self._create_left_panel(main_frame)

        # Center panel (timer and scramble)
        self._create_center_panel(main_frame)

        # Right panel (cube visualization)
        self._create_right_panel(main_frame)

    def _create_top_bar(self):
        """Create the top navigation bar."""
        theme = self.theme_manager.get_theme()

        top_bar = tk.Frame(self, bg=theme["secondary_bg"], height=50)
        top_bar.grid(row=0, column=0, columnspan=3, sticky="ew", padx=0, pady=0)
        top_bar.grid_propagate(False)

        # Left side - Settings and menu buttons
        left_frame = tk.Frame(top_bar, bg=theme["secondary_bg"])
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Settings button (gear icon placeholder)
        settings_btn = tk.Button(
            left_frame,
            text="⚙",
            font=(theme["font_family"], 16),
            bg=theme["button_bg"],
            fg=theme["text_primary"],
            relief="flat",
            padx=10,
            pady=5,
            command=self._show_settings,
        )
        settings_btn.pack(side=tk.LEFT, padx=2)

        # Menu button
        menu_btn = tk.Button(
            left_frame,
            text="☰",
            font=(theme["font_family"], 16),
            bg=theme["button_bg"],
            fg=theme["text_primary"],
            relief="flat",
            padx=10,
            pady=5,
            command=self._show_menu,
        )
        menu_btn.pack(side=tk.LEFT, padx=2)

        # Center - Logo/Title
        title_label = tk.Label(
            top_bar,
            text="PSTimer",
            font=(theme["font_family"], 20, "bold"),
            bg=theme["secondary_bg"],
            fg=theme["text_primary"],
        )
        title_label.pack(side=tk.LEFT, expand=True)

        # Right side - Scramble type and navigation
        right_frame = tk.Frame(top_bar, bg=theme["secondary_bg"])
        right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Scramble type dropdown
        self.scramble_type_var = tk.StringVar(value="3x3x3")
        scramble_combo = ttk.Combobox(
            right_frame,
            textvariable=self.scramble_type_var,
            values=self.scramble_manager.get_available_types(),
            state="readonly",
            width=8,
        )
        scramble_combo.pack(side=tk.RIGHT, padx=5)
        scramble_combo.bind("<<ComboboxSelected>>", self._on_scramble_type_change)

        tk.Label(
            right_frame,
            text="last/next",
            font=(theme["font_family"], 10),
            bg=theme["secondary_bg"],
            fg=theme["text_secondary"],
        ).pack(side=tk.RIGHT, padx=5)

        # Scramble navigation
        prev_btn = tk.Button(
            right_frame,
            text="◀",
            font=(theme["font_family"], 12),
            bg=theme["button_bg"],
            fg=theme["text_primary"],
            relief="flat",
            padx=8,
            pady=2,
            command=self._previous_scramble,
        )
        prev_btn.pack(side=tk.RIGHT, padx=2)

        next_btn = tk.Button(
            right_frame,
            text="▶",
            font=(theme["font_family"], 12),
            bg=theme["button_bg"],
            fg=theme["text_primary"],
            relief="flat",
            padx=8,
            pady=2,
            command=self._next_scramble,
        )
        next_btn.pack(side=tk.RIGHT, padx=2)

    def _create_left_panel(self, parent):
        """Create the left statistics panel."""
        theme = self.theme_manager.get_theme()

        left_panel = tk.Frame(parent, bg=theme["sidebar_bg"], width=250)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        left_panel.grid_propagate(False)

        # Session info
        session_frame = tk.Frame(left_panel, bg=theme["sidebar_bg"])
        session_frame.pack(fill=tk.X, padx=10, pady=10)

        self.session_label = tk.Label(
            session_frame,
            text="Session - 3x3x3",
            font=(theme["font_family"], 12, "bold"),
            bg=theme["sidebar_bg"],
            fg=theme["text_primary"],
        )
        self.session_label.pack(anchor=tk.W)

        # Current/Best times
        times_frame = tk.Frame(left_panel, bg=theme["sidebar_bg"])
        times_frame.pack(fill=tk.X, padx=10, pady=5)

        # Headers
        headers_frame = tk.Frame(times_frame, bg=theme["sidebar_bg"])
        headers_frame.pack(fill=tk.X)

        tk.Label(headers_frame, text="", width=8, bg=theme["sidebar_bg"]).pack(
            side=tk.LEFT
        )
        tk.Label(
            headers_frame,
            text="current",
            font=(theme["font_family"], 10, "bold"),
            bg=theme["sidebar_bg"],
            fg=theme["text_primary"],
            width=10,
        ).pack(side=tk.LEFT)
        tk.Label(
            headers_frame,
            text="best",
            font=(theme["font_family"], 10, "bold"),
            bg=theme["sidebar_bg"],
            fg=theme["text_primary"],
            width=10,
        ).pack(side=tk.LEFT)

        # Statistics rows
        self.stats_labels = {}
        stats_data = [
            ("time", "14.17", "4.24"),
            ("mo3", "11.56", "10.36"),
            ("ao5", "16.93", "12.82"),
            ("ao12", "18.06", "16.76"),
            ("ao100", "18.99", "18.96"),
        ]

        for stat_name, current, best in stats_data:
            row_frame = tk.Frame(times_frame, bg=theme["sidebar_bg"])
            row_frame.pack(fill=tk.X, pady=1)

            # Stat name
            name_label = tk.Label(
                row_frame,
                text=stat_name,
                font=(theme["mono_font"], 10),
                bg=theme["sidebar_bg"],
                fg=theme["text_primary"],
                width=8,
                anchor=tk.W,
            )
            name_label.pack(side=tk.LEFT)

            # Current value
            current_label = tk.Label(
                row_frame,
                text=current,
                font=(theme["mono_font"], 10),
                bg=theme["sidebar_bg"],
                fg=theme["text_primary"],
                width=10,
            )
            current_label.pack(side=tk.LEFT)

            # Best value
            best_label = tk.Label(
                row_frame,
                text=best,
                font=(theme["mono_font"], 10),
                bg=theme["sidebar_bg"],
                fg=theme["text_primary"],
                width=10,
            )
            best_label.pack(side=tk.LEFT)

            self.stats_labels[stat_name] = (current_label, best_label)

        # Solve count and mean
        solve_info_frame = tk.Frame(left_panel, bg=theme["sidebar_bg"])
        solve_info_frame.pack(fill=tk.X, padx=10, pady=10)

        self.solve_count_label = tk.Label(
            solve_info_frame,
            text="solve: 113/113",
            font=(theme["font_family"], 11, "bold"),
            bg=theme["sidebar_bg"],
            fg=theme["text_primary"],
        )
        self.solve_count_label.pack(anchor=tk.W)

        self.mean_label = tk.Label(
            solve_info_frame,
            text="mean: 18.57",
            font=(theme["font_family"], 11, "bold"),
            bg=theme["sidebar_bg"],
            fg=theme["text_primary"],
        )
        self.mean_label.pack(anchor=tk.W)

        # Session times table
        times_table_frame = tk.Frame(left_panel, bg=theme["sidebar_bg"])
        times_table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Table header
        table_header = tk.Frame(times_table_frame, bg=theme["sidebar_bg"])
        table_header.pack(fill=tk.X)

        headers = [("#", 4), ("time", 8), ("ao5", 8), ("ao12", 8)]
        for header, width in headers:
            tk.Label(
                table_header,
                text=header,
                font=(theme["mono_font"], 9, "bold"),
                bg=theme["sidebar_bg"],
                fg=theme["text_primary"],
                width=width,
            ).pack(side=tk.LEFT, padx=1)

        # Scrollable times list
        times_container = tk.Frame(times_table_frame, bg=theme["sidebar_bg"])
        times_container.pack(fill=tk.BOTH, expand=True)

        # Create scrollbar
        scrollbar = ttk.Scrollbar(times_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create times listbox
        self.times_listbox = tk.Listbox(
            times_container,
            bg=theme["bg"],
            fg=theme["text_primary"],
            font=(theme["mono_font"], 9),
            selectbackground=theme["accent"],
            relief="flat",
            yscrollcommand=scrollbar.set,
        )
        self.times_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.times_listbox.yview)

        # Add sample data
        sample_times = [
            "113  14.17  16.93  18.06",
            "112  16.28  16.31  18.42",
            "111   4.24  18.02  18.39",
            "110  20.35  20.20  18.95",
            "109  21.40  20.16  19.14",
        ]
        for time_str in sample_times:
            self.times_listbox.insert(tk.END, time_str)

    def _create_center_panel(self, parent):
        """Create the center timer and scramble panel."""
        theme = self.theme_manager.get_theme()

        center_panel = tk.Frame(parent, bg=theme["bg"])
        center_panel.grid(row=0, column=1, sticky="nsew", padx=10)
        center_panel.grid_rowconfigure(1, weight=1)

        # Scramble display
        scramble_frame = tk.Frame(center_panel, bg=theme["bg"], height=80)
        scramble_frame.pack(fill=tk.X, pady=(20, 10))
        scramble_frame.pack_propagate(False)

        self.scramble_label = tk.Label(
            scramble_frame,
            text="B2 D' L F' U R' B2 U' R2 F2 U2 F2 L' D2 R2 B2 R2 F2 D2 U",
            font=(theme["font_family"], 14),
            bg=theme["bg"],
            fg=theme["text_primary"],
            wraplength=500,
            justify=tk.CENTER,
        )
        self.scramble_label.pack(expand=True)

        # Timer display
        timer_frame = tk.Frame(center_panel, bg=theme["bg"])
        timer_frame.pack(expand=True, fill=tk.BOTH)

        self.timer_label = tk.Label(
            timer_frame,
            text="14.17",
            font=(theme["mono_font"], 120, "bold"),
            bg=theme["bg"],
            fg=theme["timer_color"],
        )
        self.timer_label.pack(expand=True)

        # Statistics below timer
        stats_below_frame = tk.Frame(center_panel, bg=theme["bg"])
        stats_below_frame.pack(pady=20)

        self.ao5_below_label = tk.Label(
            stats_below_frame,
            text="ao5: 16.93",
            font=(theme["font_family"], 24, "bold"),
            bg=theme["bg"],
            fg="#4CAF50",
        )
        self.ao5_below_label.pack()

        self.ao12_below_label = tk.Label(
            stats_below_frame,
            text="ao12: 18.06",
            font=(theme["font_family"], 24, "bold"),
            bg=theme["bg"],
            fg="#2196F3",
        )
        self.ao12_below_label.pack()

        # Additional stats with delta
        delta_label = tk.Label(
            stats_below_frame,
            text="(-2.11)",
            font=(theme["font_family"], 18),
            bg=theme["bg"],
            fg="#4CAF50",
        )
        delta_label.pack()

    def _create_right_panel(self, parent):
        """Create the right cube visualization panel."""
        theme = self.theme_manager.get_theme()

        right_panel = tk.Frame(parent, bg=theme["sidebar_bg"], width=250)
        right_panel.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        right_panel.grid_propagate(False)

        # Cube visualization
        cube_frame = tk.Frame(right_panel, bg=theme["sidebar_bg"])
        cube_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add the 3D cube
        self.cube_viz = CubeVisualization(cube_frame, width=220, height=220)
        self.cube_viz.get_canvas().pack(expand=True, fill=tk.BOTH)

        # Scramble function note
        function_label = tk.Label(
            right_panel,
            text="Function draw scramble",
            font=(theme["font_family"], 10),
            bg=theme["sidebar_bg"],
            fg=theme["text_secondary"],
        )
        function_label.pack(pady=(0, 10))

    def _setup_bindings(self):
        """Setup keyboard and mouse bindings."""
        self.bind("<KeyPress-space>", self._on_space_press)
        self.bind("<KeyRelease-space>", self._on_space_release)
        self.bind("<KeyPress-s>", lambda e: self._generate_new_scramble())
        self.bind("<KeyPress-r>", lambda e: self._reset_timer())

        # Transparency controls
        self.bind(
            "<Control-equal>", lambda e: self._adjust_transparency(0.05)
        )  # Ctrl + = (increase transparency)
        self.bind(
            "<Control-minus>", lambda e: self._adjust_transparency(-0.05)
        )  # Ctrl + - (decrease transparency)
        self.bind(
            "<Control-0>", lambda e: self._reset_transparency()
        )  # Ctrl + 0 (reset to opaque)

        # Compact mode controls
        self.bind(
            "<Control-m>", lambda e: self._toggle_compact_mode()
        )  # Ctrl + M (toggle compact mode)
        self.bind(
            "<Control-1>", lambda e: self._set_compact_position("top-left")
        )  # Ctrl + 1
        self.bind(
            "<Control-2>", lambda e: self._set_compact_position("top-right")
        )  # Ctrl + 2
        self.bind(
            "<Control-3>", lambda e: self._set_compact_position("bottom-left")
        )  # Ctrl + 3
        self.bind(
            "<Control-4>", lambda e: self._set_compact_position("bottom-right")
        )  # Ctrl + 4

        self.bind("<KeyPress>", self._on_any_key)

        self.focus_set()  # Ensure window can receive key events

    def _start_ui_loop(self):
        """Start the main UI update loop."""
        self._update_timer_display()
        self._generate_new_scramble()

    def _update_timer_display(self):
        """Update the timer display."""
        current_time = self.stopwatch.get_time()
        formatted_time = self.stopwatch.format_time(current_time)

        # Update main timer (if in normal mode and widget exists)
        if not self.is_compact_mode and hasattr(self, "timer_label"):
            try:
                self.timer_label.config(text=formatted_time)

                # Change color based on state
                theme = self.theme_manager.get_theme()
                if self.is_ready:
                    self.timer_label.config(fg=theme["timer_ready"])
                elif self.stopwatch.running:
                    self.timer_label.config(fg=theme["timer_running"])
                else:
                    self.timer_label.config(fg=theme["timer_color"])
            except tk.TclError:
                # Widget has been destroyed, ignore
                pass

        # Update compact display (if in compact mode)
        if self.is_compact_mode:
            self._update_compact_display()

        # Schedule next update
        self.after(50, self._update_timer_display)

    def _on_space_press(self, event):
        """Handle space key press."""
        if self.stopwatch.running:
            return  # Space press ignored while running

        if not self.is_ready:
            self.is_ready = True
            self.ready_start_time = time.time()
            self.stopwatch.reset()

            # Start inspection time if enabled
            if self.inspection_enabled:
                self.inspection_time = time.time()

    def _on_space_release(self, event):
        """Handle space key release."""
        if self.stopwatch.running:
            # Stop the timer
            final_time = self.stopwatch.stop()
            self._record_solve(final_time)
            self.is_ready = False
        elif self.is_ready:
            # Check if held long enough
            hold_time = time.time() - (self.ready_start_time or 0)
            hold_threshold = self.hold_time / 1000.0  # Convert ms to seconds

            if hold_time >= hold_threshold:
                # Check inspection time if enabled
                if self.inspection_enabled and self.inspection_time:
                    inspection_elapsed = time.time() - self.inspection_time
                    if inspection_elapsed > 17.0:  # Over 17 seconds = DNF
                        messagebox.showwarning(
                            "Inspection Time",
                            "Inspection time exceeded 17 seconds - DNF!",
                        )
                        self.is_ready = False
                        self.inspection_time = None
                        return
                    elif inspection_elapsed > 15.0:  # Over 15 seconds = +2 penalty
                        messagebox.showinfo(
                            "Inspection Time",
                            "Inspection time over 15 seconds - +2 penalty will be applied",
                        )

                self.stopwatch.start()
                self.is_ready = False
                self.inspection_time = None
            else:
                self.is_ready = False
                self.inspection_time = None

    def _on_any_key(self, event):
        """Handle any key press to stop timer."""
        if self.stopwatch.running and event.keysym not in ["space", "s", "r"]:
            final_time = self.stopwatch.stop()
            self._record_solve(final_time)

    def _record_solve(self, solve_time):
        """Record a completed solve."""
        scramble = self.scramble_manager.get_current()
        solve = SolveTime(solve_time, scramble)
        self.session_manager.current_session.add_time(solve)

        # Update displays
        self._update_statistics()
        self._update_times_list()
        self._update_session_display()

        # Generate new scramble for next solve
        self.after(100, self._generate_new_scramble)

    def _update_statistics(self):
        """Update all statistics displays."""
        stats = self.session_manager.current_session.get_statistics()

        # Only update UI elements if not in compact mode
        if not self.is_compact_mode:
            # Update current stats in left panel
            if "mo3" in self.stats_labels:
                current_label, _ = self.stats_labels["mo3"]
                mo3_text = (
                    self.stopwatch.format_time(stats["mo3"]) if stats["mo3"] else "---"
                )
                try:
                    current_label.config(text=mo3_text)
                except tk.TclError:
                    # Widget has been destroyed, ignore
                    pass

            if "ao5" in self.stats_labels:
                current_label, _ = self.stats_labels["ao5"]
                ao5_text = (
                    self.stopwatch.format_time(stats["ao5"]) if stats["ao5"] else "---"
                )
                try:
                    current_label.config(text=ao5_text)
                except tk.TclError:
                    # Widget has been destroyed, ignore
                    pass

            if "ao12" in self.stats_labels:
                current_label, _ = self.stats_labels["ao12"]
                ao12_text = (
                    self.stopwatch.format_time(stats["ao12"])
                    if stats["ao12"]
                    else "---"
                )
                try:
                    current_label.config(text=ao12_text)
                except tk.TclError:
                    # Widget has been destroyed, ignore
                    pass

            # Update center panel stats
            try:
                if stats["ao5"]:
                    self.ao5_below_label.config(
                        text=f"ao5: {self.stopwatch.format_time(stats['ao5'])}"
                    )
                if stats["ao12"]:
                    self.ao12_below_label.config(
                        text=f"ao12: {self.stopwatch.format_time(stats['ao12'])}"
                    )

                # Update solve count
                session = self.session_manager.current_session
                self.solve_count_label.config(
                    text=f"solve: {len(session)}/{len(session)}"
                )

                if stats["mean"]:
                    self.mean_label.config(
                        text=f"mean: {self.stopwatch.format_time(stats['mean'])}"
                    )
            except tk.TclError:
                # Widgets have been destroyed, ignore
                pass

    def _update_times_list(self):
        """Update the times list display."""
        # Only update if not in compact mode
        if self.is_compact_mode:
            return

        session = self.session_manager.current_session

        try:
            # Clear current list
            self.times_listbox.delete(0, tk.END)

            # Add times with stats
            for i, solve in enumerate(session.times[:20]):  # Show last 20
                time_str = self.stopwatch.format_time(solve.time)

                # Calculate ao5 and ao12 for this position
                ao5_str = "---"
                ao12_str = "---"

                if i >= 4:  # Need at least 5 times for ao5
                    recent_5 = session.times[i - 4 : i + 1]
                    if len(recent_5) == 5:
                        ao5_val = session.stats_calc.calculate_ao5(recent_5)
                        if ao5_val:
                            ao5_str = self.stopwatch.format_time(ao5_val)

                if i >= 11:  # Need at least 12 times for ao12
                    recent_12 = session.times[i - 11 : i + 1]
                    if len(recent_12) == 12:
                        ao12_val = session.stats_calc.calculate_ao12(recent_12)
                        if ao12_val:
                            ao12_str = self.stopwatch.format_time(ao12_val)

                solve_num = len(session.times) - i
                line = f"{solve_num:3d}  {time_str:>6}  {ao5_str:>6}  {ao12_str:>6}"
                self.times_listbox.insert(tk.END, line)
        except tk.TclError:
            # Widget has been destroyed, ignore
            pass

    def _update_session_display(self):
        """Update the session information display."""
        # Only update if not in compact mode
        if self.is_compact_mode:
            return

        puzzle_type = self.scramble_type_var.get()
        solve_count = len(self.session_manager.current_session)

        # Update session label
        try:
            self.session_label.config(
                text=f"Session - {puzzle_type} ({solve_count} solves)"
            )
        except tk.TclError:
            # Widget has been destroyed, ignore
            pass

    def _generate_new_scramble(self):
        """Generate and display a new scramble."""
        scramble = self.scramble_manager.generate_new()

        # Update scramble display based on current mode
        if self.is_compact_mode:
            try:
                self.compact_widgets["scramble"].config(text=scramble)
            except (tk.TclError, KeyError):
                pass
        else:
            try:
                self.scramble_label.config(text=scramble)
            except tk.TclError:
                pass

        # Apply to cube visualization (only in normal mode)
        if not self.is_compact_mode:
            try:
                self.cube_viz.apply_scramble(scramble)
            except tk.TclError:
                pass

    def _previous_scramble(self):
        """Go to previous scramble."""
        scramble = self.scramble_manager.get_previous()
        if scramble:
            # Update scramble display based on current mode
            if self.is_compact_mode:
                try:
                    self.compact_widgets["scramble"].config(text=scramble)
                except (tk.TclError, KeyError):
                    pass
            else:
                try:
                    self.scramble_label.config(text=scramble)
                except tk.TclError:
                    pass
            # Apply to cube visualization (only in normal mode)
            if not self.is_compact_mode:
                try:
                    self.cube_viz.apply_scramble(scramble)
                except tk.TclError:
                    pass

    def _next_scramble(self):
        """Go to next scramble."""
        scramble = self.scramble_manager.get_next()

        # Update scramble display based on current mode
        if self.is_compact_mode:
            try:
                self.compact_widgets["scramble"].config(text=scramble)
            except (tk.TclError, KeyError):
                pass
        else:
            try:
                self.scramble_label.config(text=scramble)
            except tk.TclError:
                pass
        # Apply to cube visualization (only in normal mode)
        if not self.is_compact_mode:
            try:
                self.cube_viz.apply_scramble(scramble)
            except tk.TclError:
                pass

    def _on_scramble_type_change(self, event):
        """Handle scramble type change."""
        new_type = self.scramble_type_var.get()
        if self.scramble_manager.set_type(new_type):
            self._generate_new_scramble()

    def _reset_timer(self):
        """Reset the timer to zero."""
        self.stopwatch.reset()
        self.is_ready = False

    def _adjust_transparency(self, delta):
        """Adjust window transparency by delta amount."""
        new_transparency = max(0.3, min(1.0, self.transparency + delta))
        if new_transparency != self.transparency:
            self.transparency = new_transparency
            self.attributes("-alpha", self.transparency)

    def _reset_transparency(self):
        """Reset transparency to fully opaque."""
        self.transparency = 1.0
        self.attributes("-alpha", self.transparency)

    def _toggle_compact_mode(self):
        """Toggle between normal and compact mode."""
        if self.is_compact_mode:
            self._exit_compact_mode()
        else:
            self._enter_compact_mode()

    def _enter_compact_mode(self):
        """Enter compact mode showing only timer and scramble."""
        if self.is_compact_mode:
            return

        # Store current window geometry
        self.normal_geometry = self.geometry()
        self.is_compact_mode = True

        # Hide all existing widgets by destroying main UI
        for widget in self.winfo_children():
            widget.destroy()

        # Create compact UI first
        self._create_compact_ui()

        # Position window based on compact_position (this will also set size)
        self._position_compact_window()

    def _exit_compact_mode(self):
        """Exit compact mode and restore normal UI."""
        if not self.is_compact_mode:
            return

        self.is_compact_mode = False

        # Remove topmost attribute
        self.attributes("-topmost", False)

        # Reset window size constraints
        self.resizable(True, True)
        self.minsize(900, 600)  # Reset to normal minimum size
        self.maxsize(0, 0)  # Remove maximum size limit

        # Clear compact widgets
        for widget in self.winfo_children():
            widget.destroy()
        self.compact_widgets.clear()

        # Restore normal UI
        self._create_ui()

        # Restore window geometry
        if self.normal_geometry:
            self.geometry(self.normal_geometry)

        # Refresh displays
        self._update_session_display()

    def _create_compact_ui(self):
        """Create the compact mode UI with minimal elements."""
        theme = self.theme_manager.get_theme()

        # Configure window for compact mode
        self.configure(bg=theme["bg"])

        # Main compact frame
        compact_frame = tk.Frame(self, bg=theme["bg"], padx=10, pady=10)
        compact_frame.pack(fill=tk.BOTH, expand=True)

        # Timer display (large and prominent)
        self.compact_widgets["timer"] = tk.Label(
            compact_frame,
            text="00:00.00",
            font=(theme["mono_font"], 20, "bold"),
            bg=theme["bg"],
            fg=theme["timer_color"],
        )
        self.compact_widgets["timer"].pack(pady=(0, 10))

        # Scramble display (smaller but readable)
        self.compact_widgets["scramble"] = tk.Label(
            compact_frame,
            text="Loading scramble...",
            font=(theme["font_family"], 10),
            bg=theme["bg"],
            fg=theme["text_primary"],
            wraplength=250,
            justify=tk.CENTER,
        )
        self.compact_widgets["scramble"].pack(pady=(0, 10))

        # Quick controls row
        controls_frame = tk.Frame(compact_frame, bg=theme["bg"])
        controls_frame.pack()

        # Exit compact mode button
        exit_btn = tk.Button(
            controls_frame,
            text="↗",  # Expand icon
            command=self._exit_compact_mode,
            font=(theme["font_family"], 12, "bold"),
            width=3,
            bg=theme["accent"],
            fg="white",
        )
        exit_btn.pack(side=tk.LEFT, padx=(0, 5))

        # New scramble button
        scramble_btn = tk.Button(
            controls_frame,
            text="S",
            command=self._generate_new_scramble,
            font=(theme["font_family"], 10, "bold"),
            width=3,
            bg=theme["button_bg"],
            fg=theme["text_primary"],
        )
        scramble_btn.pack(side=tk.LEFT, padx=(0, 5))

        # Reset button
        reset_btn = tk.Button(
            controls_frame,
            text="R",
            command=self._reset_timer,
            font=(theme["font_family"], 10, "bold"),
            width=3,
            bg=theme["button_bg"],
            fg=theme["text_primary"],
        )
        reset_btn.pack(side=tk.LEFT)

        # Update compact display with current data
        self._update_compact_display()

    def _update_compact_display(self):
        """Update the compact mode display elements."""
        if not self.is_compact_mode:
            return

        # Update timer display
        if "timer" in self.compact_widgets:
            current_time = self.stopwatch.get_time()
            time_text = self.stopwatch.format_time(current_time)

            # Color based on timer state
            theme = self.theme_manager.get_theme()
            if self.stopwatch.running:
                color = theme["timer_running"]
            elif self.is_ready:
                color = theme["timer_ready"]
            else:
                color = theme["timer_color"]

            self.compact_widgets["timer"].config(text=time_text, fg=color)

        # Update scramble display
        if "scramble" in self.compact_widgets:
            current_scramble = self.scramble_manager.get_current()
            if current_scramble:
                self.compact_widgets["scramble"].config(text=current_scramble)

    def _position_compact_window(self):
        """Position the compact window based on compact_position setting."""
        # Define compact window dimensions (fixed size for consistency)
        window_width = 280
        window_height = 150

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position based on compact_position
        margin = 20  # Margin from screen edges

        if self.compact_position == "top-left":
            x, y = margin, margin
        elif self.compact_position == "top-right":
            x, y = screen_width - window_width - margin, margin
        elif self.compact_position == "bottom-left":
            x, y = margin, screen_height - window_height - margin
        elif self.compact_position == "bottom-right":
            x, y = (
                screen_width - window_width - margin,
                screen_height - window_height - margin,
            )
        else:
            x, y = margin, margin  # Default to top-left

        # Set window size and position with explicit dimensions
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Configure window properties for compact mode
        self.minsize(window_width, window_height)
        self.maxsize(window_width, window_height)
        self.resizable(False, False)

        # Make window stay on top in compact mode
        self.attributes("-topmost", True)

        # Ensure window is properly positioned (additional updates)
        self.update_idletasks()
        self.update()

    def _set_compact_position(self, position):
        """Set the compact mode position and reposition if currently compact."""
        self.compact_position = position
        if self.is_compact_mode:
            self._position_compact_window()

    def _show_settings(self):
        """Show settings dialog and apply changes."""
        result = show_settings_dialog(
            self,
            self.theme_manager,
            self.session_manager,
            current_transparency=self.transparency,
            current_compact_position=self.compact_position,
        )
        if result:
            # Apply settings
            self._apply_settings(result)

    def _apply_settings(self, settings):
        """Apply settings from the settings dialog."""
        # Apply puzzle type change
        if "puzzle_type" in settings:
            new_type = settings["puzzle_type"]
            if self.scramble_manager.set_type(new_type):
                self.scramble_type_var.set(new_type)
                # Generate new scramble for the new puzzle type
                self._generate_new_scramble()
                # Update session display
                self._update_session_display()

        # Apply inspection time setting
        if "inspection" in settings:
            self.inspection_enabled = settings["inspection"]

        # Apply hold time setting
        if "hold_time" in settings:
            self.hold_time = settings["hold_time"]

        # Apply transparency setting
        if "transparency" in settings:
            transparency = settings["transparency"]
            self.transparency = transparency
            self.attributes("-alpha", transparency)

        # Apply compact position setting
        if "compact_position" in settings:
            self.compact_position = settings["compact_position"]
            if self.is_compact_mode:
                self._position_compact_window()

        # Store settings for future use
        self.user_settings = settings

        # Show confirmation
        messagebox.showinfo(
            "Settings Applied",
            f"Settings have been applied successfully!\n\n"
            f"Puzzle type: {settings.get('puzzle_type', 'unchanged')}\n"
            f"Inspection time: {'Enabled' if settings.get('inspection', False) else 'Disabled'}\n"
            f"Transparency: {int(settings.get('transparency', 1.0) * 100)}%\n"
            f"Compact position: {settings.get('compact_position', 'unchanged')}\n"
            f"Theme: {settings.get('theme', 'unchanged')}",
        )

    def _show_menu(self):
        """Show main menu."""
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(
            label="New Session",
            command=self._new_session,
        )
        menu.add_command(
            label="Clear Session",
            command=self._clear_session,
        )
        menu.add_separator()
        menu.add_command(
            label="Export Times",
            command=self._export_times,
        )
        menu.add_command(
            label="Import Times",
            command=lambda: messagebox.showinfo("Menu", "Import not yet implemented"),
        )
        menu.add_separator()
        menu.add_command(
            label="About PSTimer",
            command=lambda: show_about_dialog(self, self.theme_manager),
        )
        menu.add_separator()
        menu.add_command(label="Exit", command=self.quit)

        # Show menu at mouse position
        try:
            menu.tk_popup(self.winfo_pointerx(), self.winfo_pointery())
        finally:
            menu.grab_release()

    def _new_session(self):
        """Start a new session."""
        if len(self.session_manager.current_session) > 0:
            response = messagebox.askyesno(
                "New Session",
                f"Current session has {len(self.session_manager.current_session)} solves.\n"
                "Are you sure you want to start a new session?",
            )
            if not response:
                return

        self.session_manager.new_session()
        self._update_statistics()
        self._update_times_list()
        self._update_session_display()
        self._generate_new_scramble()
        messagebox.showinfo("New Session", "New session started!")

    def _clear_session(self):
        """Clear the current session."""
        if len(self.session_manager.current_session) == 0:
            messagebox.showinfo("Clear Session", "Session is already empty.")
            return

        response = messagebox.askyesno(
            "Clear Session",
            f"Are you sure you want to clear all {len(self.session_manager.current_session)} solves from the current session?",
        )
        if response:
            self.session_manager.current_session.clear()
            self._update_statistics()
            self._update_times_list()
            self._update_session_display()
            messagebox.showinfo("Clear Session", "Session cleared!")

    def _export_times(self):
        """Export session times to a text file."""
        from tkinter import filedialog

        session = self.session_manager.current_session
        if len(session) == 0:
            messagebox.showinfo("Export Times", "No times to export.")
            return

        filename = filedialog.asksaveasfilename(
            title="Export Times",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("All files", "*.*"),
            ],
        )

        if filename:
            try:
                with open(filename, "w") as f:
                    f.write(f"PSTimer Session Export\n")
                    f.write(f"Puzzle Type: {self.scramble_type_var.get()}\n")
                    f.write(f"Total Solves: {len(session)}\n")
                    f.write("=" * 50 + "\n\n")

                    for i, solve in enumerate(session.times, 1):
                        f.write(
                            f"{i:3d}. {solve.formatted_time:>8s} - {solve.scramble}\n"
                        )

                    # Add statistics
                    stats = session.get_statistics()
                    f.write("\n" + "=" * 50 + "\n")
                    f.write("Statistics:\n")
                    f.write(f"Best: {stats.get('best', 'N/A')}\n")
                    if stats.get("ao5"):
                        f.write(f"ao5: {stats['ao5']}\n")
                    if stats.get("ao12"):
                        f.write(f"ao12: {stats['ao12']}\n")
                    if stats.get("ao100"):
                        f.write(f"ao100: {stats['ao100']}\n")

                messagebox.showinfo("Export Complete", f"Times exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export times:\n{e}")

    def _apply_theme(self):
        """Apply the current theme to all UI elements."""
        theme = self.theme_manager.get_theme()

        # Update main window
        self.configure(bg=theme["bg"])

        # This would need a more comprehensive implementation
        # to update all widgets recursively
        messagebox.showinfo(
            "Theme",
            f"Theme changed to {self.theme_manager.current_theme_name}.\nRestart the application to see full changes.",
        )
