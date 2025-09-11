"""
Timer core functionality for PSTimer.
"""

import time


class Stopwatch:
    """High-precision stopwatch for speedcubing timing."""

    def __init__(self):
        self.running = False
        self.start_ts = None
        self.elapsed = 0.0  # seconds

    def start(self):
        """Start the timer."""
        if not self.running:
            self.start_ts = time.perf_counter()
            self.running = True

    def stop(self):
        """Stop the timer and return final time."""
        if self.running:
            self.elapsed += time.perf_counter() - self.start_ts
            self.start_ts = None
            self.running = False
            return self.elapsed
        return self.elapsed

    def reset(self):
        """Reset the timer to zero."""
        self.running = False
        self.start_ts = None
        self.elapsed = 0.0

    def get_time(self):
        """Get current elapsed time."""
        if self.running and self.start_ts is not None:
            return self.elapsed + (time.perf_counter() - self.start_ts)
        return self.elapsed

    @staticmethod
    def format_time(seconds):
        """Format time in speedcubing format (M:SS.cc or SS.cc)."""
        if seconds is None:
            return "---"

        total_cs = int(round(seconds * 100))
        cs = total_cs % 100
        total_s = total_cs // 100
        s = total_s % 60
        m = total_s // 60

        if total_s >= 60:
            return f"{m}:{s:02d}.{cs:02d}"
        else:
            return f"{s:02d}.{cs:02d}"

    @staticmethod
    def time_to_seconds(time_str):
        """Convert formatted time string back to seconds."""
        try:
            if ":" in time_str:
                parts = time_str.split(":")
                minutes = int(parts[0])
                sec_parts = parts[1].split(".")
                seconds = int(sec_parts[0])
                centiseconds = int(sec_parts[1])
                return minutes * 60 + seconds + centiseconds / 100
            else:
                sec_parts = time_str.split(".")
                seconds = int(sec_parts[0])
                centiseconds = int(sec_parts[1])
                return seconds + centiseconds / 100
        except (ValueError, IndexError):
            return 0.0
