# PyTimer - Rubik's Cube Timer AI Instructions

## Project Overview
A cross-platform Tkinter-based Rubik's Cube timer with animations and session tracking. Single-file application with modular architecture for extensibility.

## Architecture Components

### Core Classes
- **ScrambleGenerator**: Base class for puzzle scramble algorithms
  - `ThreeByThreeScramble`: 3x3 cube implementation with face/modifier logic
  - Pattern: Avoids same face repetition, uses FACES/MODIFIERS constants
- **Stopwatch**: High-precision timer using `time.perf_counter()`
  - Tracks running state, elapsed time, provides centisecond formatting (M:SS.cc)
- **TimerApp**: Main Tkinter application with component composition

### UI Architecture
- **Left Panel**: Timer display, scramble canvas, controls, keyboard hints
- **Right Panel**: Session history listbox with copy/clear functionality
- **Canvas-based scramble display**: Enables slide-in animations using `place()` geometry

### Animation System
All animations use Tkinter's `after()` method with lambda closures:
- **Scramble slide-in**: Text moves from off-canvas left to center position
- **Timer pulse**: Font scaling during start/stop (1.0 → 1.12 scale)
- **Reset bounce**: Quick size animation using easing patterns
- **Background pulse**: Color cycling during timer runs with random jitter

## Development Patterns

### Event Handling
- Keyboard bindings: Space (toggle), 's' (scramble), 'r' (reset)
- Button commands map directly to methods without lambda wrappers
- Single `toggle_timer()` method handles start/stop logic

### State Management
- Timer state in `Stopwatch` class, UI state in `TimerApp`
- Session data: `[(seconds, timestamp), ...]` list structure
- UI updates via `_update_ui_loop()` with 30ms intervals

### Extension Points
- New puzzle types: Subclass `ScrambleGenerator` 
- Animation effects: Follow pattern in `_animate_scale_pulse()`
- Timer formats: Modify `format_time()` method

## Development Workflow

### Environment Setup
```bash
# Virtual environment exists at .venv/
# Activate with platform-specific command
python main.py  # Run directly, no dependencies beyond tkinter
```

### Code Organization
- Single file by design for portability
- Class-based components with clear separation
- Constants defined at class level (FACES, MODIFIERS)

### Debugging Notes
- UI updates happen in main thread only
- Animation state tracked via instance variables (pulse_scale, bg_phase)
- Error handling minimal - focus on UI responsiveness

## Key Files
- `main.py`: Complete application (347 lines)
- `.venv/`: Python virtual environment
- `.gitignore`: Standard Python exclusions

When extending this codebase, maintain the single-file architecture and animation-driven UX patterns.
