"""
Statistics calculation for speedcubing times.
"""

from datetime import datetime


class StatisticsCalculator:
    """Calculates speedcubing statistics like ao5, ao12, mo3, etc."""

    @staticmethod
    def calculate_mo3(times):
        """Calculate Mean of 3 (simple average of last 3 times)."""
        if len(times) < 3:
            return None
        recent_3 = [t.time for t in times[:3]]
        return sum(recent_3) / 3

    @staticmethod
    def calculate_ao5(times):
        """Calculate Average of 5 (remove best and worst, average the rest)."""
        if len(times) < 5:
            return None
        recent_5 = [t.time for t in times[:5]]
        recent_5.sort()
        # Remove best (first) and worst (last), average the middle 3
        return sum(recent_5[1:4]) / 3

    @staticmethod
    def calculate_ao12(times):
        """Calculate Average of 12 (remove best and worst, average the rest)."""
        if len(times) < 12:
            return None
        recent_12 = [t.time for t in times[:12]]
        recent_12.sort()
        # Remove best and worst, average the middle 10
        return sum(recent_12[1:11]) / 10

    @staticmethod
    def calculate_ao100(times):
        """Calculate Average of 100 (remove best 5 and worst 5, average the rest)."""
        if len(times) < 100:
            return None
        recent_100 = [t.time for t in times[:100]]
        recent_100.sort()
        # Remove best 5 and worst 5, average the middle 90
        return sum(recent_100[5:95]) / 90

    @staticmethod
    def get_best_time(times):
        """Get the best (fastest) time."""
        if not times:
            return None
        return min(times, key=lambda t: t.time)

    @staticmethod
    def get_worst_time(times):
        """Get the worst (slowest) time."""
        if not times:
            return None
        return max(times, key=lambda t: t.time)

    @staticmethod
    def get_session_mean(times):
        """Calculate mean of all times in session."""
        if not times:
            return None
        return sum(t.time for t in times) / len(times)


class SolveTime:
    """Represents a single solve time with metadata."""

    def __init__(self, time, scramble="", timestamp=None, penalty=None):
        self.time = time
        self.scramble = scramble
        self.timestamp = timestamp or datetime.now()
        self.penalty = penalty  # None, "+2", "DNF"

    @property
    def display_time(self):
        """Get display time with penalty applied."""
        if self.penalty == "DNF":
            return float("inf")
        elif self.penalty == "+2":
            return self.time + 2.0
        return self.time

    @property
    def formatted_time(self):
        """Get formatted time string."""
        from .timer import Stopwatch

        return str(self)

    def __str__(self):
        from .timer import Stopwatch

        time_str = Stopwatch.format_time(self.time)
        if self.penalty == "DNF":
            return "DNF"
        elif self.penalty == "+2":
            return f"{Stopwatch.format_time(self.time + 2.0)}+"
        return time_str


class Session:
    """Manages a session of solves."""

    def __init__(self, name="Session 1"):
        self.name = name
        self.times = []
        self.stats_calc = StatisticsCalculator()

    def add_time(self, solve_time):
        """Add a solve time to the session."""
        self.times.insert(0, solve_time)  # Insert at beginning for newest first

    def remove_time(self, index):
        """Remove a time from the session."""
        if 0 <= index < len(self.times):
            return self.times.pop(index)
        return None

    def clear_times(self):
        """Clear all times from the session."""
        self.times.clear()

    def clear(self):
        """Alias for clear_times for consistency."""
        self.clear_times()

    def get_statistics(self):
        """Get all statistics for the session."""
        return {
            "count": len(self.times),
            "mo3": self.stats_calc.calculate_mo3(self.times),
            "ao5": self.stats_calc.calculate_ao5(self.times),
            "ao12": self.stats_calc.calculate_ao12(self.times),
            "ao100": self.stats_calc.calculate_ao100(self.times),
            "best": self.stats_calc.get_best_time(self.times),
            "worst": self.stats_calc.get_worst_time(self.times),
            "mean": self.stats_calc.get_session_mean(self.times),
        }

    def __len__(self):
        return len(self.times)


class SessionManager:
    """Manages multiple sessions."""

    def __init__(self):
        self.sessions = [Session("Session 1")]
        self.current_session_index = 0

    @property
    def current_session(self):
        """Get the current active session."""
        return self.sessions[self.current_session_index]

    def add_session(self, name=None):
        """Add a new session."""
        if name is None:
            name = f"Session {len(self.sessions) + 1}"
        session = Session(name)
        self.sessions.append(session)
        return session

    def new_session(self, name=None):
        """Create a new session and switch to it."""
        session = self.add_session(name)
        self.current_session_index = len(self.sessions) - 1
        return session

    def switch_session(self, index):
        """Switch to a different session."""
        if 0 <= index < len(self.sessions):
            self.current_session_index = index
            return True
        return False

    def delete_session(self, index):
        """Delete a session."""
        if len(self.sessions) > 1 and 0 <= index < len(self.sessions):
            del self.sessions[index]
            if self.current_session_index >= len(self.sessions):
                self.current_session_index = len(self.sessions) - 1
            return True
        return False
