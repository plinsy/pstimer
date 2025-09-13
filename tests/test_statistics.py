"""
Test statistics calculations and session management.
"""

import pytest
from datetime import datetime, timedelta
from src.statistics import StatisticsCalculator, SessionManager, SolveTime


class TestStatisticsCalculator:
    """Test statistics calculation methods."""

    def test_mo3_calculation(self, statistics_calculator, solve_times):
        """Test Mean of 3 calculation."""
        # Test with enough times
        result = statistics_calculator.calculate_mo3(solve_times)
        expected = (12.45 + 15.67 + 11.23) / 3  # First 3 times
        assert abs(result - expected) < 0.01, f"Expected {expected}, got {result}"
        
        # Test with insufficient times
        assert statistics_calculator.calculate_mo3([]) is None
        assert statistics_calculator.calculate_mo3(solve_times[:2]) is None

    def test_ao5_calculation(self, statistics_calculator, solve_times):
        """Test Average of 5 calculation."""
        result = statistics_calculator.calculate_ao5(solve_times)
        
        # ao5 removes best and worst, averages middle 3
        times_only = [t.time for t in solve_times]
        times_only.sort()
        expected = sum(times_only[1:4]) / 3  # Remove first and last
        
        assert abs(result - expected) < 0.01, f"Expected {expected}, got {result}"
        
        # Test with insufficient times
        assert statistics_calculator.calculate_ao5(solve_times[:4]) is None

    def test_ao12_calculation(self, statistics_calculator):
        """Test Average of 12 calculation."""
        # Create 12 solve times
        times = [SolveTime(i * 1.5 + 10, f"scramble_{i}") for i in range(12)]
        
        result = statistics_calculator.calculate_ao12(times)
        
        # ao12 removes best and worst, averages middle 10
        times_only = [t.time for t in times]
        times_only.sort()
        expected = sum(times_only[1:11]) / 10
        
        assert abs(result - expected) < 0.01, f"Expected {expected}, got {result}"

    def test_ao100_calculation(self, statistics_calculator):
        """Test Average of 100 calculation."""
        # Create 100 solve times
        times = [SolveTime(i * 0.1 + 10, f"scramble_{i}") for i in range(100)]
        
        result = statistics_calculator.calculate_ao100(times)
        
        # ao100 removes best 5 and worst 5, averages middle 90
        times_only = [t.time for t in times]
        times_only.sort()
        expected = sum(times_only[5:95]) / 90
        
        assert abs(result - expected) < 0.01, f"Expected {expected}, got {result}"

    def test_best_worst_time(self, statistics_calculator, solve_times):
        """Test best and worst time calculations."""
        best = statistics_calculator.get_best_time(solve_times)
        worst = statistics_calculator.get_worst_time(solve_times)
        
        assert best.time == 11.23, f"Expected best time 11.23, got {best.time}"
        assert worst.time == 15.67, f"Expected worst time 15.67, got {worst.time}"
        
        # Test with empty list
        assert statistics_calculator.get_best_time([]) is None
        assert statistics_calculator.get_worst_time([]) is None

    def test_session_mean(self, statistics_calculator, solve_times):
        """Test session mean calculation."""
        result = statistics_calculator.get_session_mean(solve_times)
        expected = sum(t.time for t in solve_times) / len(solve_times)
        
        assert abs(result - expected) < 0.01, f"Expected {expected}, got {result}"
        assert statistics_calculator.get_session_mean([]) is None


class TestSolveTime:
    """Test SolveTime data structure."""

    def test_solve_time_creation(self):
        """Test SolveTime object creation."""
        now = datetime.now()
        solve = SolveTime(12.34, "R U R' U'", now, "+2")
        
        assert solve.time == 12.34
        assert solve.scramble == "R U R' U'"
        assert solve.timestamp == now
        assert solve.penalty == "+2"

    def test_solve_time_defaults(self):
        """Test SolveTime default values."""
        solve = SolveTime(15.67)
        
        assert solve.time == 15.67
        assert solve.scramble == ""
        assert solve.penalty is None
        assert isinstance(solve.timestamp, datetime)

    def test_effective_time_property(self):
        """Test effective_time property with penalties."""
        # Normal solve
        solve1 = SolveTime(12.34)
        assert solve1.effective_time == 12.34
        
        # +2 penalty
        solve2 = SolveTime(12.34, penalty="+2")
        assert solve2.effective_time == 14.34
        
        # DNF penalty
        solve3 = SolveTime(12.34, penalty="DNF")
        assert solve3.effective_time == float('inf')


class TestSessionManager:
    """Test session management functionality."""

    def test_session_creation(self):
        """Test creating a new session."""
        sm = SessionManager()
        assert len(sm.current_session) == 0
        assert sm.session_name == "Session 1"

    def test_add_solve_time(self):
        """Test adding solve times to session."""
        sm = SessionManager()
        solve = SolveTime(12.34, "R U R' U'")
        
        sm.add_solve_time(solve)
        assert len(sm.current_session) == 1
        assert sm.current_session[0] == solve

    def test_get_recent_times(self):
        """Test getting recent solve times."""
        sm = SessionManager()
        
        # Add some solve times
        for i in range(10):
            solve = SolveTime(10 + i, f"scramble_{i}")
            sm.add_solve_time(solve)
        
        # Test getting recent times
        recent_5 = sm.get_recent_times(5)
        assert len(recent_5) == 5
        assert recent_5[0].time == 19  # Most recent (last added)
        assert recent_5[4].time == 15  # 5th most recent

    def test_clear_session(self):
        """Test clearing current session."""
        sm = SessionManager()
        
        # Add some solve times
        for i in range(5):
            sm.add_solve_time(SolveTime(10 + i))
        
        assert len(sm.current_session) == 5
        
        sm.clear_session()
        assert len(sm.current_session) == 0

    def test_remove_last_solve(self):
        """Test removing the last solve time."""
        sm = SessionManager()
        
        # Add some solve times
        solve1 = SolveTime(12.34)
        solve2 = SolveTime(15.67)
        sm.add_solve_time(solve1)
        sm.add_solve_time(solve2)
        
        assert len(sm.current_session) == 2
        
        removed = sm.remove_last_solve()
        assert removed == solve2
        assert len(sm.current_session) == 1
        assert sm.current_session[0] == solve1
        
        # Test removing from empty session
        sm.clear_session()
        assert sm.remove_last_solve() is None
