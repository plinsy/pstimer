# PSTimer - Professional Speedcubing Timer AI Instructions

## Project Overview
A modular, csTimer-inspired Rubik's cube timer with WCA-compliant scrambles, advanced statistics, 3D visualization, multiple themes, and unique features like compact mode and transparency. Built with Python/Tkinter in a clean, extensible architecture.

## Architecture Components

### Core Module Structure
- **`main.py`**: Entry point that imports `src.ui.PSTimerUI` and runs the application
- **`src/ui.py`**: Main UI class (1200+ lines) with csTimer-inspired 3-panel layout
- **`src/timer.py`**: High-precision `Stopwatch` class using `time.perf_counter()`
- **`src/scramble.py`**: Extensible scramble system with WCA-compliant generators
- **`src/statistics.py`**: Session management and speedcubing statistics (mo3, ao5, ao12, ao100)
- **`src/themes.py`**: Theme system with csTimer, Dark, and Blue themes
- **`src/cube_visualization.py`**: 3D interactive cube using OpenGL-style rendering
- **`src/settings.py`**: Settings dialog for configuration management

### UI Architecture Pattern
The main `PSTimerUI` class creates a 3-panel csTimer-inspired layout:
```python
# In _create_ui():
self._create_left_panel(main_frame)    # Statistics & solve history
self._create_center_panel(main_frame)  # Timer & scramble display  
self._create_right_panel(main_frame)   # 3D cube visualization
```

### Key Classes & Responsibilities

#### `PSTimerUI` (src/ui.py)
- Main application window inheriting from `tk.Tk`
- Manages dual-mode UI: normal (3-panel) and compact (overlay) modes
- Handles keyboard events: Space (timer), S (scramble), Ctrl+M (compact mode)
- Animation system using `tk.after()` for timer pulse effects

#### `ScrambleManager` (src/scramble.py)
- Supports 8 WCA puzzle types with compliant algorithms
- Pattern: Each puzzle class extends `ScrambleGenerator` base class
- Example: `ThreeByThreeScramble` avoids consecutive same-face/opposite-face moves
- Uses `FACES`, `MODIFIERS`, `OPPOSITE_FACES` constants for move restrictions

#### `SessionManager` & `StatisticsCalculator` (src/statistics.py) 
- Session data structure: `SolveTime` objects with metadata
- Statistics follow WCA trimming rules (remove best/worst for averages)
- Real-time calculation: ao5 (trim 1 best/worst), ao12 (trim 1), ao100 (trim 5)

### Unique Features Implementation

#### Compact Mode (`is_compact_mode` state)
- Minimal 280x150px overlay with 4 corner positioning options
- Dual UI system: `_create_ui()` vs `_create_compact_ui()` methods
- Always-on-top window with essential timer/scramble display

#### Transparency System
- `self.transparency` attribute (0.0-1.0) with Ctrl+/- keyboard controls
- Uses `self.attributes('-alpha', self.transparency)` for window transparency

#### Theme Integration
- All UI creation methods reference `theme = self.theme_manager.get_theme()`
- Consistent color application across panels using theme dictionary keys
- Theme switching triggers full UI recreation via `_apply_theme()`

## Development Patterns

### Testing Structure
- Feature-specific test files: `test_wca_compliance.py`, `test_compact_mode.py`, `test_transparency.py`
- Tests import from `src/` modules and verify component functionality
- WCA compliance tests validate scramble algorithm correctness

### Event Handling Pattern
```python
# Keyboard bindings in __init__():
self.bind('<KeyPress>', self._on_key_press)
self.bind('<KeyRelease>', self._on_key_release)

# Timer state management:
self.is_ready = False  # Space bar hold state
self.ready_start_time = None  # For hold time validation
```

### Animation System
- Timer pulse: `self.pulse_scale` animated between 1.0-1.12 during start/stop
- Background animation: `self.bg_animation_id` for color cycling during timer runs
- All animations use `self.after()` with cleanup on state changes

## Development Workflow

### Running the Application
```bash
python main.py  # Direct execution, no build process needed
```

### Adding New Puzzle Types
1. Create new generator class in `src/scramble.py` extending `ScrambleGenerator`
2. Add to `PUZZLE_TYPES` dict in `ScrambleManager.__init__()`
3. Update dropdown options in `_create_top_bar()` method

### Adding New Themes
1. Add theme dict to `THEMES` in `src/themes.py`
2. Include all required color keys (bg, text_primary, timer_color, etc.)
3. Theme automatically available via theme switching system

### Key Integration Points
- **Settings persistence**: User preferences stored in `self.user_settings` dict
- **Session data**: Solve times stored as `[(SolveTime, timestamp), ...]` lists
- **Statistics updates**: Triggered after each solve via `_update_statistics_display()`
- **3D cube state**: Scramble sequences drive cube visualization updates

When extending PSTimer, follow the modular src/ structure, maintain WCA compliance for scrambles, and preserve the csTimer-inspired UX patterns.
