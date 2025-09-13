# PSTimer - Professional Speedcubing Timer AI Instructions

## Project Overview
A modular, csTimer-inspired Rubik's cube timer with WCA-compliant scrambles, advanced statistics, 3D visualization, multiple themes, and unique features like compact mode and transparency. Built with Python/Tkinter in a clean, extensible architecture.

## Architecture Components

### Entry Point & Module Structure
- **`main.py`**: Simple entry point that adds `src/` to path and runs `PSTimerUI().mainloop()`
- **`src/ui.py`**: Main UI class (1379 lines) orchestrating all components
- **`src/timer.py`**: High-precision `Stopwatch` class using `time.perf_counter()`
- **`src/scramble.py`**: WCA-compliant scramble generators (461 lines) with strict move validation
- **`src/statistics.py`**: Session management and speedcubing statistics with WCA trimming rules
- **`src/themes.py`**: Theme system with predefined color schemes (csTimer, Dark, Blue)
- **`src/cube_visualization.py`**: 3D interactive cube simulation with OpenGL-style rendering
- **`src/settings.py`**: Settings dialog for configuration management

### UI Architecture Pattern
The `PSTimerUI` class implements a dual-mode system with csTimer-inspired 3-panel layout:
```python
# Normal mode: _create_ui() creates 3 panels
self._create_left_panel(main_frame)    # Statistics & solve history
self._create_center_panel(main_frame)  # Timer & scramble display  
self._create_right_panel(main_frame)   # 3D cube visualization

# Compact mode: _create_compact_ui() creates minimal overlay
self.is_compact_mode = True/False      # State toggle
self.compact_position = "top-right"    # Corner positioning
```

### Core Classes & Data Flow

#### `PSTimerUI` State Management
- **Timer states**: `self.is_ready`, `self.ready_start_time` for space bar hold validation
- **UI modes**: `self.is_compact_mode` with geometry caching in `self.normal_geometry`
- **Animations**: `self.pulse_scale` (1.0-1.12) and `self.bg_animation_id` for visual feedback
- **Settings**: `self.user_settings` dict persisted across sessions

#### WCA-Compliant Scramble System
- **Base pattern**: All generators extend `ScrambleGenerator` with `generate()` method
- **3x3 rules**: 20 moves, no consecutive same face, max 2 consecutive opposite faces
- **Move validation**: Uses `OPPOSITE_FACES` dict and face history tracking
- **Example**: `ThreeByThreeScramble` checks `last_face` and `second_last_face`

#### Statistics with WCA Trimming
- **Data structure**: `SolveTime(time, scramble, timestamp, penalty)` objects
- **Calculations**: ao5 (remove 1 best/worst), ao12 (remove 1), ao100 (remove 5 each)
- **Real-time updates**: `_update_statistics_display()` called after each solve
### Unique Features Implementation

#### Compact Mode System
- **State toggle**: `self.is_compact_mode` with `Ctrl+M` keyboard shortcut
- **Positioning**: `self.compact_position` supports 4 corners (`Ctrl+1-4`)
- **Geometry caching**: `self.normal_geometry` preserves main window state
- **Dual UI creation**: Completely separate `_create_compact_ui()` method

#### Transparency System  
- **Control**: `self.transparency` (0.0-1.0) with `Ctrl+/-` and `Ctrl+0` shortcuts
- **Implementation**: `self.attributes('-alpha', self.transparency)` for window alpha
- **Theme integration**: All UI creation references `theme = self.theme_manager.get_theme()`

#### Animation Framework
- **Timer pulse**: `self.pulse_scale` animated between 1.0-1.12 using `tk.after()`
- **Background effects**: `self.bg_animation_id` for color cycling during timer runs
- **State-based cleanup**: Animations cancelled on timer state changes

## Development Patterns

### Modern Testing Structure with pytest
- **Framework**: Complete migration from simple assertions to pytest-based testing
- **Organization**: `tests/` directory with 48 comprehensive tests across 4 test files
- **Coverage**: WCA compliance (`test_wca_compliance.py`), statistics (`test_statistics.py`), timer precision (`test_timer.py`), and themes (`test_themes.py`)
- **Fixtures**: Centralized test setup in `tests/conftest.py` with reusable components
- **Configuration**: `pytest.ini` for test discovery and execution settings
- **Test runner**: `run_tests.py` script with coverage, filtering, and different execution modes

### Testing Patterns Used Throughout
```python
# Parameterized tests for multiple puzzle types
@pytest.mark.parametrize("puzzle_type,expected_faces", [
    ("3x3x3", ["U", "D", "L", "R", "F", "B"]),
    ("2x2x2", ["U", "R", "F"]),
])

# Fixture-based setup for consistent test environments
@pytest.fixture
def scramble_manager():
    return ScrambleManager("3x3x3")

# Comprehensive validation with detailed error messages
assert len(moves) == 20, f"Expected 20 moves, got {len(moves)}"
```

### Event Handling Pattern
```python
# Keyboard bindings in PSTimerUI.__init__():
self.bind('<KeyPress>', self._on_key_press)
self.bind('<KeyRelease>', self._on_key_release)

# Timer state management pattern:
self.is_ready = False          # Space bar hold state
self.ready_start_time = None   # For 300ms hold validation
self.hold_time = 300          # Configurable hold threshold
```

### Theme System Architecture
- **Theme definitions**: Complete color dictionaries in `THEMES` dict in `themes.py`
- **Required keys**: `bg`, `text_primary`, `timer_color`, `timer_ready`, `timer_running`, etc.
- **Application pattern**: `theme = self.theme_manager.get_theme()` in all UI methods
- **Dynamic switching**: `_apply_theme()` triggers full UI recreation

## Development Workflow

### Running & Testing
```bash
# Development - direct execution
python main.py

# Modern testing with pytest
pytest tests/ -v                    # Run all tests
pytest tests/test_wca_compliance.py # Run specific test file
pytest --cov=src --cov-report=html  # Run with coverage

# Test runner with options
python run_tests.py --type=wca      # Run WCA compliance tests only
python run_tests.py --coverage      # Include coverage reporting

# Distribution build (uses PyInstaller)
python build_dist.py               # Cross-platform build script
```

### Build System Details
- **PyInstaller spec**: `PSTimer.spec` with `console=False` for GUI app
- **Icon handling**: Uses `icons/favicon.ico` for Windows builds
- **Distribution**: Creates `PSTimer-Distribution/` with executable and assets
- **Requirements check**: `build_dist.py` validates PyInstaller availability

### Testing Strategy
- **Functionality tests**: `test_basic_functionality.py` verifies core cube/scramble operations
- **Compliance validation**: WCA tests ensure tournament-legal scrambles
- **Feature testing**: Specific tests for compact mode, transparency, themes
- **No test framework**: Uses simple assertions and print statements

### Adding New Features

#### New Puzzle Types
1. Create generator class in `src/scramble.py` extending `ScrambleGenerator`
2. Add WCA-compliant move validation (see `ThreeByThreeScramble` pattern)
3. Add to `PUZZLE_TYPES` dict in `ScrambleManager.__init__()`
4. Update dropdown in `PSTimerUI._create_top_bar()`

#### New Themes
1. Add complete color dict to `THEMES` in `src/themes.py`
2. Include all required keys: `bg`, `text_primary`, `timer_color`, etc.
3. Theme automatically available via existing switching system

### Key Integration Points
- **Settings persistence**: `self.user_settings` dict (no external config files)
- **Session data**: Solve times as `[(SolveTime, timestamp), ...]` lists in memory
- **Statistics updates**: Automatic recalculation via `_update_statistics_display()`
- **Cube visualization**: Scramble sequences drive 3D state updates
- **Logo/icon loading**: `_load_logo_image()` with size caching in `self.logo_images`

### Critical Patterns to Preserve
- **csTimer-inspired UX**: 3-panel layout with consistent keyboard controls
- **WCA compliance**: Strict move validation in all scramble generators  
- **Modular architecture**: Clear separation between UI, timer, scramble, statistics
- **Animation framework**: `tk.after()` based system with proper cleanup
- **Dual-mode UI**: Seamless switching between normal and compact modes

When extending PSTimer, maintain the established patterns for WCA compliance, follow the modular src/ structure, and preserve the csTimer-inspired user experience.
