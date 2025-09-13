"""
Test configuration and fixtures for PSTimer.
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))


@pytest.fixture
def mock_tkinter():
    """Mock tkinter to avoid GUI creation during tests."""
    with patch('tkinter.Tk'), \
         patch('tkinter.ttk'), \
         patch('tkinter.messagebox'):
        yield


@pytest.fixture
def scramble_manager():
    """Create a ScrambleManager instance for testing."""
    from src.scramble import ScrambleManager
    return ScrambleManager("3x3x3")


@pytest.fixture
def statistics_calculator():
    """Create a StatisticsCalculator instance for testing."""
    from src.statistics import StatisticsCalculator
    return StatisticsCalculator()


@pytest.fixture
def solve_times():
    """Create sample solve times for testing statistics."""
    from src.statistics import SolveTime
    from datetime import datetime
    
    times = [
        SolveTime(12.45, "R U R' U'", datetime.now()),
        SolveTime(15.67, "F R U' R' F'", datetime.now()),
        SolveTime(11.23, "R U2 R' U'", datetime.now()),
        SolveTime(14.89, "U R U' R'", datetime.now()),
        SolveTime(13.56, "F U F' U'", datetime.now()),
    ]
    return times


@pytest.fixture
def timer():
    """Create a Stopwatch instance for testing."""
    from src.timer import Stopwatch
    return Stopwatch()


@pytest.fixture
def theme_manager():
    """Create a ThemeManager instance for testing."""
    from src.themes import ThemeManager
    return ThemeManager()
