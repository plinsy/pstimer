# Writing the Rubik's Cube timer Tkinter app to a file and show a short preview.
#!/usr/bin/env python3
"""
Cross-platform Rubik's Cube timer using Tkinter.

Features:
- Start / Stop / Reset timer
- Spacebar toggles start/stop (press and hold? No — single toggle)
- 'r' resets current timer and clears selection
- 's' generates a new scramble
- Generates 3x3 scrambles (extensible via ScrambleGenerator classes)
- Simple animations: scramble slides in, time label scales/pulses while running
- Stores a session list of times shown in a sidebar

To run:
    python rubiks_timer.py
"""
import tkinter as tk
from tkinter import ttk
import time
import random
from datetime import datetime

# ------------------- Statistics Calculator -------------------


class StatisticsCalculator:
    """Calculates speedcubing statistics like ao5, ao12, ao100, mo3."""

    @staticmethod
    def calculate_ao5(times):
        """Calculate Average of 5 (remove best and worst, average the rest)."""
        if len(times) < 5:
            return None
        recent_5 = [t[0] for t in times[:5]]  # Get just the time values
        recent_5.sort()
        # Remove best (first) and worst (last), average the middle 3
        return sum(recent_5[1:4]) / 3

    @staticmethod
    def calculate_ao12(times):
        """Calculate Average of 12 (remove best and worst, average the rest)."""
        if len(times) < 12:
            return None
        recent_12 = [t[0] for t in times[:12]]
        recent_12.sort()
        # Remove best and worst, average the middle 10
        return sum(recent_12[1:11]) / 10

    @staticmethod
    def calculate_ao100(times):
        """Calculate Average of 100 (remove best 5 and worst 5, average the rest)."""
        if len(times) < 100:
            return None
        recent_100 = [t[0] for t in times[:100]]
        recent_100.sort()
        # Remove best 5 and worst 5, average the middle 90
        return sum(recent_100[5:95]) / 90

    @staticmethod
    def calculate_mo3(times):
        """Calculate Mean of 3 (simple average of last 3 times)."""
        if len(times) < 3:
            return None
        recent_3 = [t[0] for t in times[:3]]
        return sum(recent_3) / 3


# ------------------- Theme System -------------------


class ThemeManager:
    """Manages color themes for the application."""

    THEMES = {
        "Dark": {
            "bg": "#222222",
            "sidebar_bg": "#1e1e1e",
            "listbox_bg": "#111111",
            "text_fg": "white",
            "hint_fg": "#bbbbbb",
            "running_base": 34,
            "running_range": 6,
        },
        "Light": {
            "bg": "#f0f0f0",
            "sidebar_bg": "#e8e8e8",
            "listbox_bg": "#ffffff",
            "text_fg": "black",
            "hint_fg": "#666666",
            "running_base": 220,
            "running_range": -15,
        },
        "Blue": {
            "bg": "#1a1a2e",
            "sidebar_bg": "#16213e",
            "listbox_bg": "#0f3460",
            "text_fg": "#eee6e6",
            "hint_fg": "#a8a8a8",
            "running_base": 26,
            "running_range": 8,
        },
        "Green": {
            "bg": "#1e2a1e",
            "sidebar_bg": "#1a241a",
            "listbox_bg": "#152015",
            "text_fg": "#e6ffe6",
            "hint_fg": "#a8c8a8",
            "running_base": 30,
            "running_range": 10,
        },
        "Purple": {
            "bg": "#2a1e2a",
            "sidebar_bg": "#241a24",
            "listbox_bg": "#201520",
            "text_fg": "#ffe6ff",
            "hint_fg": "#c8a8c8",
            "running_base": 42,
            "running_range": 8,
        },
    }

    def __init__(self, theme_name="Dark"):
        self.current_theme = theme_name

    def get_theme(self):
        return self.THEMES.get(self.current_theme, self.THEMES["Dark"])

    def set_theme(self, theme_name):
        if theme_name in self.THEMES:
            self.current_theme = theme_name
            return True
        return False

    def get_theme_names(self):
        return list(self.THEMES.keys())


# ------------------- Scramble Generator Architecture -------------------

class ScrambleGenerator:
    """Base class for scramble generators. Subclass this to support more puzzles."""
    def generate(self):
        raise NotImplementedError("generate must be implemented by subclasses")

class ThreeByThreeScramble(ScrambleGenerator):
    """Generates a standard 3x3 scramble string (20 moves by default)."""

    FACES = ['U', 'D', 'L', 'R', 'F', 'B']
    MODIFIERS = ['', "'", '2']

    def __init__(self, length=20):
        self.length = length

    def generate(self):
        seq = []
        prev_face = None
        for _ in range(self.length):
            # avoid same face twice in a row and avoid opposite face directly after (optional)
            face = random.choice(self.FACES)
            while face == prev_face:
                face = random.choice(self.FACES)
            modifier = random.choice(self.MODIFIERS)
            seq.append(face + modifier)
            prev_face = face
        return ' '.join(seq)

# ------------------- Timer Logic -------------------

class Stopwatch:
    def __init__(self, update_interval=10):
        self.running = False
        self.start_ts = None
        self.elapsed = 0.0  # seconds
        self.update_interval = update_interval  # milliseconds
        self._after_id = None

    def start(self):
        if not self.running:
            self.start_ts = time.perf_counter()
            self.running = True

    def stop(self):
        if self.running:
            self.elapsed += time.perf_counter() - self.start_ts
            self.start_ts = None
            self.running = False

    def reset(self):
        self.running = False
        self.start_ts = None
        self.elapsed = 0.0

    def get_time(self):
        if self.running and self.start_ts is not None:
            return self.elapsed + (time.perf_counter() - self.start_ts)
        return self.elapsed

    def format_time(self, seconds):
        # Format as M:SS.cc (centiseconds)
        total_cs = int(round(seconds * 100))
        cs = total_cs % 100
        total_s = total_cs // 100
        s = total_s % 60
        m = total_s // 60
        return f"{m}:{s:02d}.{cs:02d}"

# ------------------- GUI App -------------------

class TimerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rubik's Cube Timer (Tkinter)")
        self.geometry("740x360")
        self.minsize(640, 300)

        # Initialize theme manager
        self.theme_manager = ThemeManager()
        theme = self.theme_manager.get_theme()
        self.configure(bg=theme["bg"])

        # Core components
        self.stopwatch = Stopwatch()
        self.scramble_gen = ThreeByThreeScramble()
        self.times = []  # list of (time_in_seconds, timestamp)
        self.stats_calc = StatisticsCalculator()

        # UI elements
        self._build_ui()

        # Animation parameters
        self.pulse_dir = 1
        self.pulse_scale = 1.0
        self.bg_phase = 0.0

        # Ready state for hold-space mechanism
        self.ready_state = False
        self.ready_start_time = None

        # Bind keys - use KeyPress and KeyRelease for space
        self.bind("<KeyPress-space>", self.space_pressed)
        self.bind("<KeyRelease-space>", self.space_released)
        self.bind("s", lambda e: self.new_scramble())
        self.bind("r", lambda e: self.reset_current())

        # Bind any key press to stop timer if running
        self.bind("<KeyPress>", self.any_key_pressed)

        # Make sure the window can receive focus
        self.focus_set()

        # Start UI loop
        self._update_ui_loop()

    def _build_ui(self):
        theme = self.theme_manager.get_theme()

        # Top frame for theme selector
        top_frame = tk.Frame(self, bg=theme["bg"])
        top_frame.pack(fill=tk.X, padx=12, pady=(8, 0))

        theme_label = tk.Label(
            top_frame,
            text="Theme:",
            bg=theme["bg"],
            fg=theme["text_fg"],
            font=("Arial", 10),
        )
        theme_label.pack(side=tk.LEFT)

        self.theme_var = tk.StringVar(value=self.theme_manager.current_theme)
        self.theme_combo = ttk.Combobox(
            top_frame,
            textvariable=self.theme_var,
            values=self.theme_manager.get_theme_names(),
            state="readonly",
            width=10,
        )
        self.theme_combo.pack(side=tk.LEFT, padx=(6, 0))
        self.theme_combo.bind("<<ComboboxSelected>>", self._on_theme_change)

        # Left frame: main display
        left = tk.Frame(self, bg=theme["bg"])
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=12, pady=12)

        # Time label
        self.time_var = tk.StringVar(value="0:00.00")
        self.time_label = tk.Label(
            left,
            textvariable=self.time_var,
            font=("Consolas", 48, "bold"),
            fg=theme["text_fg"],
            bg=theme["bg"],
        )
        self.time_label.pack(anchor='center', pady=(10, 8))

        # Scramble area (with slide-in animation using place)
        scramble_frame = tk.Frame(left, bg=theme["bg"])
        scramble_frame.pack(fill=tk.X, pady=(6, 6))
        self.scramble_canvas = tk.Canvas(
            scramble_frame, height=40, bg=theme["bg"], highlightthickness=0
        )
        self.scramble_canvas.pack(fill=tk.X, expand=True)
        self.scramble_text_id = None
        self.current_scramble = ""
        self.new_scramble(initial=True)

        # Controls row
        ctrls = tk.Frame(left, bg=theme["bg"])
        ctrls.pack(pady=(8, 6))

        self.start_btn = tk.Button(ctrls, text="Start", command=self.start_timer, width=10)
        self.start_btn.grid(row=0, column=0, padx=4)
        self.stop_btn = tk.Button(ctrls, text="Stop", command=self.stop_timer, width=10)
        self.stop_btn.grid(row=0, column=1, padx=4)
        self.reset_btn = tk.Button(ctrls, text="Reset", command=self.reset_current, width=10)
        self.reset_btn.grid(row=0, column=2, padx=4)
        self.scramble_btn = tk.Button(ctrls, text="New Scramble", command=self.new_scramble, width=12)
        self.scramble_btn.grid(row=0, column=3, padx=4)

        hint = tk.Label(
            left,
            text="Hold Space: Ready • Release Space: Start • Any Key: Stop • S: Scramble • R: Reset",
            bg=theme["bg"],
            fg=theme["hint_fg"],
            font=("Arial", 10),
        )
        hint.pack(pady=(6, 0))

        # Right frame: session list
        right = tk.Frame(self, width=220, bg=theme["sidebar_bg"])
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=12, pady=12)
        right.pack_propagate(False)

        # Statistics section
        stats_frame = tk.Frame(right, bg=theme["sidebar_bg"])
        stats_frame.pack(fill=tk.X, pady=(6, 8))

        tk.Label(
            stats_frame,
            text="Statistics",
            bg=theme["sidebar_bg"],
            fg=theme["text_fg"],
            font=("Arial", 12, "bold"),
        ).pack()

        # Create statistics labels
        stats_container = tk.Frame(stats_frame, bg=theme["sidebar_bg"])
        stats_container.pack(fill=tk.X, pady=(4, 0))

        self.mo3_label = tk.Label(
            stats_container,
            text="mo3: ---",
            bg=theme["sidebar_bg"],
            fg=theme["text_fg"],
            font=("Consolas", 10),
            anchor="w",
        )
        self.mo3_label.pack(fill=tk.X, padx=8)

        self.ao5_label = tk.Label(
            stats_container,
            text="ao5: ---",
            bg=theme["sidebar_bg"],
            fg=theme["text_fg"],
            font=("Consolas", 10),
            anchor="w",
        )
        self.ao5_label.pack(fill=tk.X, padx=8)

        self.ao12_label = tk.Label(
            stats_container,
            text="ao12: ---",
            bg=theme["sidebar_bg"],
            fg=theme["text_fg"],
            font=("Consolas", 10),
            anchor="w",
        )
        self.ao12_label.pack(fill=tk.X, padx=8)

        self.ao100_label = tk.Label(
            stats_container,
            text="ao100: ---",
            bg=theme["sidebar_bg"],
            fg=theme["text_fg"],
            font=("Consolas", 10),
            anchor="w",
        )
        self.ao100_label.pack(fill=tk.X, padx=8)

        tk.Label(
            right,
            text="Session Times",
            bg=theme["sidebar_bg"],
            fg=theme["text_fg"],
            font=("Arial", 12, "bold"),
        ).pack(pady=(6, 4))
        self.times_listbox = tk.Listbox(
            right,
            height=12,
            bg=theme["listbox_bg"],
            fg=theme["text_fg"],
            bd=0,
            font=("Consolas", 11),
            activestyle="none",
        )
        self.times_listbox.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        btns_frame = tk.Frame(right, bg=theme["sidebar_bg"])
        btns_frame.pack(pady=(0, 8))
        tk.Button(btns_frame, text="Copy Last", command=self.copy_last).grid(
            row=0, column=0, padx=4
        )
        tk.Button(btns_frame, text="Clear", command=self.clear_times).grid(
            row=0, column=1, padx=4
        )

    # ---------------- UI Actions ----------------

    def start_timer(self):
        if not self.stopwatch.running:
            self.stopwatch.start()
            self._animate_scale_pulse(start=True)

    def stop_timer(self):
        if self.stopwatch.running:
            self.stopwatch.stop()
            elapsed = self.stopwatch.get_time()
            self._record_time(elapsed)
            self._animate_scale_pulse(start=False)

            # Auto-generate new scramble after solve (but don't reset timer)
            self.after(100, self._auto_generate_scramble)

    def reset_current(self):
        self.stopwatch.reset()
        self.time_var.set(self.stopwatch.format_time(0.0))
        # small bounce animation to indicate reset
        self._bounce_time_label()

    def _auto_reset_after_solve(self):
        """Automatically reset the timer to 0 and generate new scramble after completing a solve."""
        self.stopwatch.reset()
        self.time_var.set(self.stopwatch.format_time(0.0))

        # Auto-generate new scramble for next solve
        self.new_scramble()

    def _auto_generate_scramble(self):
        """Automatically generate new scramble after completing a solve."""
        self.new_scramble()

    def space_pressed(self, event=None):
        """Handle space key press - enter ready state if timer is not running."""
        if not self.stopwatch.running and not self.ready_state:
            # Reset timer when entering ready state (only on space hold)
            self.stopwatch.reset()
            self.time_var.set(self.stopwatch.format_time(0.0))

            self.ready_state = True
            self.ready_start_time = time.time()
            # Visual feedback for ready state
            self._show_ready_state()

    def space_released(self, event=None):
        """Handle space key release - start timer if ready, stop if running."""
        if self.stopwatch.running:
            # If timer is running, stop it
            self.stop_timer()
        elif self.ready_state:
            # Check if space was held long enough (minimum 500ms for safety)
            hold_time = time.time() - (self.ready_start_time or 0)
            if hold_time >= 0.5:
                # Start the timer
                self.ready_state = False
                self._hide_ready_state()
                self.start_timer()
            else:
                # Released too quickly, cancel ready state
                self.ready_state = False
                self._hide_ready_state()

    def toggle_timer(self, event=None):
        """Legacy method - now handled by space press/release."""
        if self.stopwatch.running:
            self.stop_timer()
        else:
            self.start_timer()

    def any_key_pressed(self, event=None):
        """Handle any key press - stop timer if running, but allow special keys for other functions."""
        # Only stop timer if it's running and it's not a special key we want to preserve
        if self.stopwatch.running:
            # Check if it's a key we want to handle specially
            if event and hasattr(event, "keysym"):
                key = event.keysym.lower()
                # Don't stop timer for these special keys - let them handle their own functions
                if key in ["s", "r"]:
                    return
                # Space is handled by space_released, so ignore it here to avoid double-stopping
                if key == "space":
                    return

            # For any other key, stop the timer
            self.stop_timer()

    def new_scramble(self, initial=False):
        self.current_scramble = self.scramble_gen.generate()
        self._slide_in_scramble(initial=initial)

    def _record_time(self, seconds):
        ts = datetime.now()
        self.times.insert(0, (seconds, ts))
        display = f"{self.stopwatch.format_time(seconds)}  —  {ts.strftime('%H:%M:%S')}"
        self.times_listbox.insert(0, display)
        # keep the list reasonable size
        if self.times_listbox.size() > 200:
            self.times_listbox.delete(200, tk.END)

        # Update statistics
        self._update_statistics()

    def _update_statistics(self):
        """Update all statistics displays."""
        # Calculate statistics
        mo3 = self.stats_calc.calculate_mo3(self.times)
        ao5 = self.stats_calc.calculate_ao5(self.times)
        ao12 = self.stats_calc.calculate_ao12(self.times)
        ao100 = self.stats_calc.calculate_ao100(self.times)

        # Update labels
        self.mo3_label.config(
            text=f"mo3: {self.stopwatch.format_time(mo3) if mo3 else '---'}"
        )
        self.ao5_label.config(
            text=f"ao5: {self.stopwatch.format_time(ao5) if ao5 else '---'}"
        )
        self.ao12_label.config(
            text=f"ao12: {self.stopwatch.format_time(ao12) if ao12 else '---'}"
        )
        self.ao100_label.config(
            text=f"ao100: {self.stopwatch.format_time(ao100) if ao100 else '---'}"
        )

    def copy_last(self):
        if self.times:
            last = self.stopwatch.format_time(self.times[0][0])
            self.clipboard_clear()
            self.clipboard_append(last)

    def clear_times(self):
        self.times = []
        self.times_listbox.delete(0, tk.END)
        # Reset statistics display
        self._update_statistics()

    def _show_ready_state(self):
        """Show visual feedback that the timer is ready to start."""
        theme = self.theme_manager.get_theme()
        # Change time label to green to indicate ready
        self.time_label.configure(fg="#00ff00")  # Bright green
        # Slightly scale up the time label
        self.time_label.configure(font=("Consolas", int(48 * 1.05), "bold"))

    def _hide_ready_state(self):
        """Hide ready state visual feedback."""
        theme = self.theme_manager.get_theme()
        # Restore normal text color
        self.time_label.configure(fg=theme["text_fg"])
        # Restore normal size
        self.time_label.configure(font=("Consolas", int(48 * self.pulse_scale), "bold"))

    def _on_theme_change(self, event=None):
        """Handle theme selection change."""
        new_theme = self.theme_var.get()
        if self.theme_manager.set_theme(new_theme):
            self._apply_theme()

    def _apply_theme(self):
        """Apply the current theme to all UI elements."""
        theme = self.theme_manager.get_theme()

        # Update main window and all frames
        def update_widget_theme(widget, is_listbox=False, is_canvas=False):
            try:
                if is_listbox:
                    widget.configure(bg=theme["listbox_bg"], fg=theme["text_fg"])
                elif is_canvas:
                    widget.configure(bg=theme["bg"])
                    # Update scramble text color if it exists
                    if hasattr(self, "scramble_text_id") and self.scramble_text_id:
                        widget.itemconfig(self.scramble_text_id, fill=theme["text_fg"])
                else:
                    widget.configure(bg=theme["bg"])
            except tk.TclError:
                pass

        # Update main window
        self.configure(bg=theme["bg"])

        # Update all child widgets recursively
        def update_children(parent, sidebar=False):
            for child in parent.winfo_children():
                widget_class = child.winfo_class()

                if widget_class == "Frame":
                    if sidebar:
                        try:
                            child.configure(bg=theme["sidebar_bg"])
                        except:
                            pass
                    else:
                        try:
                            child.configure(bg=theme["bg"])
                        except:
                            pass
                    update_children(child, sidebar)
                elif widget_class == "Label":
                    try:
                        if sidebar:
                            child.configure(bg=theme["sidebar_bg"], fg=theme["text_fg"])
                        else:
                            # Check if it's the hint label by text content
                            if "Space:" in child.cget("text"):
                                child.configure(bg=theme["bg"], fg=theme["hint_fg"])
                            else:
                                child.configure(bg=theme["bg"], fg=theme["text_fg"])
                    except:
                        pass
                elif widget_class == "Listbox":
                    try:
                        child.configure(bg=theme["listbox_bg"], fg=theme["text_fg"])
                    except:
                        pass
                elif widget_class == "Canvas":
                    try:
                        child.configure(bg=theme["bg"])
                        # Update scramble text color
                        if hasattr(self, "scramble_text_id") and self.scramble_text_id:
                            child.itemconfig(
                                self.scramble_text_id, fill=theme["text_fg"]
                            )
                    except:
                        pass
                else:
                    update_children(child, sidebar)

        # Find and update the right panel (session times)
        for child in self.winfo_children():
            if isinstance(child, tk.Frame):
                # Check if this is the right frame by looking for the times listbox
                has_listbox = any(
                    isinstance(grandchild, tk.Listbox)
                    for grandchild in child.winfo_children()
                )
                if has_listbox:
                    try:
                        child.configure(bg=theme["sidebar_bg"])
                    except:
                        pass
                    update_children(child, sidebar=True)
                else:
                    update_children(child, sidebar=False)

    # ---------------- Animations ----------------

    def _slide_in_scramble(self, initial=False):
        # remove existing text
        self.scramble_canvas.delete("all")
        width = self.scramble_canvas.winfo_width() or self.scramble_canvas.winfo_reqwidth()
        # start from left off-canvas, slide to center
        text = self.current_scramble
        theme = self.theme_manager.get_theme()
        self.scramble_text_id = self.scramble_canvas.create_text(
            -10,
            20,
            text=text,
            anchor="w",
            font=("Arial", 12, "bold"),
            fill=theme["text_fg"],
        )
        target_x = 10
        duration = 300  # ms
        steps = 20
        delay = max(1, duration // steps)
        dx = (target_x + 10) / steps

        def step(i, x):
            if i >= steps:
                self.scramble_canvas.coords(self.scramble_text_id, target_x, 20)
                return
            self.scramble_canvas.move(self.scramble_text_id, dx, 0)
            self.after(delay, lambda: step(i+1, x+dx))

        if initial:
            # show immediately without animating on startup
            self.scramble_canvas.coords(self.scramble_text_id, target_x, 20)
        else:
            step(0, -10)

    def _animate_scale_pulse(self, start=True):
        # Scale the time label slightly to make it feel 'poppy' when starting/stopping
        target = 1.12 if start else 1.0
        steps = 6
        current = self.pulse_scale
        delta = (target - current) / steps

        def step(i):
            nonlocal current
            if i >= steps:
                self.pulse_scale = target
                self.time_label.config(font=("Consolas", int(48 * self.pulse_scale), "bold"))
                return
            current += delta
            self.time_label.config(font=("Consolas", int(48 * current), "bold"))
            self.after(25, lambda: step(i+1))

        step(0)

    def _bounce_time_label(self):
        # small quick bounce effect
        orig = 48
        steps = 8
        def step(i):
            if i > steps:
                self.time_label.config(font=("Consolas", orig, "bold"))
                return
            # ease out bounce using a sin-ish pattern
            size = orig + int(6 * (1 - abs((i / steps) * 2 - 1)))
            self.time_label.config(font=("Consolas", size, "bold"))
            self.after(25, lambda: step(i+1))
        step(0)

    # ---------------- UI Loop ----------------

    def _update_ui_loop(self):
        # Update running time display
        t = self.stopwatch.get_time()
        self.time_var.set(self.stopwatch.format_time(t))

        theme = self.theme_manager.get_theme()

        # Background pulse when running
        if self.stopwatch.running:
            self.bg_phase += 0.12
            offset = (1 + 0.06 * (1 + (0.8 * (1 + (0.5 * random.random())))))  # small random jitter
            # compute subtle brightness change using theme colors
            base_brightness = theme["running_base"]
            brightness_range = theme["running_range"]
            darkness = int(
                base_brightness + brightness_range * (1 + (0.5 * (1 + random.random())))
            )
            darkness = max(0, min(255, darkness))  # clamp to valid range
            color = f"#{darkness:02x}{darkness:02x}{darkness:02x}"
            self.configure(bg=color)
            for w in self.winfo_children():
                try:
                    # Don't change sidebar background during pulse
                    if isinstance(w, tk.Frame) and any(
                        isinstance(child, tk.Listbox) for child in w.winfo_children()
                    ):
                        continue
                    w.configure(bg=color)
                except Exception:
                    pass
        else:
            # reset to base theme colors
            self.configure(bg=theme["bg"])
            for w in self.winfo_children():
                try:
                    # Apply proper theme colors for different widget types
                    if isinstance(w, tk.Frame):
                        # Check if this is the sidebar frame
                        has_listbox = any(
                            isinstance(child, tk.Listbox)
                            for child in w.winfo_children()
                        )
                        if has_listbox:
                            w.configure(bg=theme["sidebar_bg"])
                        else:
                            w.configure(bg=theme["bg"])
                    else:
                        w.configure(bg=theme["bg"])
                except Exception:
                    pass

        # Keep time label size consistent with pulse_scale (unless in ready state)
        if not self.ready_state:
            self.time_label.config(
                font=("Consolas", int(48 * self.pulse_scale), "bold")
            )

        # schedule next update
        self.after(30, self._update_ui_loop)


if __name__ == "__main__":
    app = TimerApp()
    app.mainloop()
'''

# Save file
path = "/mnt/data/rubiks_timer.py"
with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print(f"Saved Rubik's Cube timer app to: {path}")
print("Run it with: python /mnt/data/rubiks_timer.py")
print("\nControls: Space = start/stop, S = new scramble, R = reset\n")


# Also show the first ~300 characters of the file to preview
with open(path, "r", encoding="utf-8") as f:
    preview = f.read(800)
print("----- File preview -----\n")
print(preview)
'''
