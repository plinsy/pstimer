"""
Test timer functionality and precision.
"""

import pytest
import time
from unittest.mock import patch
from src.timer import Stopwatch


class TestStopwatch:
    """Test Stopwatch timer functionality."""

    def test_timer_creation(self, timer):
        """Test timer initial state."""
        assert not timer.running
        assert timer.get_time() == 0.0

    def test_timer_start_stop(self, timer):
        """Test starting and stopping the timer."""
        # Start timer
        timer.start()
        assert timer.running

        # Let it run briefly
        time.sleep(0.01)

        # Stop timer
        elapsed = timer.stop()
        assert not timer.running
        assert elapsed > 0
        assert elapsed == timer.get_time()

    def test_timer_precision(self, timer):
        """Test timer precision and accuracy."""
        timer.start()

        # Sleep for a known duration
        sleep_duration = 0.1  # 100ms
        time.sleep(sleep_duration)

        elapsed = timer.stop()

        # Should be close to sleep duration (within 10ms tolerance)
        assert abs(elapsed - sleep_duration) < 0.01, \
            f"Timer inaccurate: expected ~{sleep_duration}, got {elapsed}"

    def test_timer_reset(self, timer):
        """Test timer reset functionality."""
        # Run timer briefly
        timer.start()
        time.sleep(0.01)
        timer.stop()

        assert timer.get_time() > 0

        # Reset timer
        timer.reset()
        assert timer.get_time() == 0.0
        assert not timer.running

    def test_multiple_start_calls(self, timer):
        """Test that multiple start calls don't break the timer."""
        timer.start()
        original_start_time = timer.start_ts

        # Call start again
        timer.start()

        # Should not change the start time when already running
        assert timer.start_ts == original_start_time
        assert timer.running

    def test_stop_without_start(self, timer):
        """Test stopping timer that wasn't started."""
        elapsed = timer.stop()
        assert elapsed == 0.0
        assert not timer.running

    def test_get_time_while_running(self, timer):
        """Test getting time while timer is running."""
        timer.start()
        time.sleep(0.05)

        elapsed1 = timer.get_time()
        assert elapsed1 > 0
        assert timer.running  # Should still be running

        time.sleep(0.05)
        elapsed2 = timer.get_time()
        assert elapsed2 > elapsed1  # Should have increased

    @patch('time.perf_counter')
    def test_timer_uses_perf_counter(self, mock_perf_counter, timer):
        """Test that timer uses time.perf_counter for precision."""
        mock_perf_counter.side_effect = [1.0, 2.5]  # Start at 1.0, stop at 2.5

        timer.start()
        elapsed = timer.stop()

        assert elapsed == 1.5  # 2.5 - 1.0
        assert mock_perf_counter.call_count >= 2

    def test_timer_state_consistency(self, timer):
        """Test timer state remains consistent."""
        # Initial state
        assert not timer.running
        assert timer.get_time() == 0.0

        # After start
        timer.start()
        assert timer.running
        assert timer.get_time() >= 0.0

        # After stop
        elapsed = timer.stop()
        assert not timer.running
        assert timer.get_time() == elapsed

        # After reset
        timer.reset()
        assert not timer.running
        assert timer.get_time() == 0.0

    def test_timer_format_time(self, timer):
        """Test time formatting if available."""
        # Test the static format_time method
        formatted = timer.format_time(65.432)
        assert isinstance(formatted, str)
        assert "1:05" in formatted  # Should contain the minutes and seconds

    def test_timer_multiple_cycles(self, timer):
        """Test timer through multiple start/stop cycles."""
        for i in range(3):
            timer.reset()
            timer.start()
            time.sleep(0.01 * (i + 1))  # Variable sleep times
            elapsed = timer.stop()

            assert elapsed > 0
            assert not timer.running
            assert timer.get_time() == elapsed
