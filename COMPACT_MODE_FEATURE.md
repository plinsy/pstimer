# PSTimer Compact Mode Feature

## Overview
PSTimer now includes a powerful **Compact Mode** that minimizes the application to a small, always-on-top overlay showing only essential information: the timer and current scramble. This is perfect for extreme multitasking scenarios where you need maximum screen real estate while keeping the timer visible.

## What is Compact Mode?

Compact Mode transforms PSTimer from a full-featured application into a minimal overlay that can be positioned in any corner of your screen. It shows:

- **Large, clear timer display**
- **Current scramble** (word-wrapped for readability)  
- **Essential controls** (expand, new scramble, reset)
- **Always on top** - stays visible over other applications
- **Small footprint** - only 280x150 pixels

```
┌─────────────────────────┐
│      00:23.45           │  ← Large timer
│                         │
│  R U R' U' F R F'       │  ← Current scramble
│                         │
│  [↗] [S] [R]           │  ← Quick controls
└─────────────────────────┘
```

## Features

### 🎯 **Positioning Options**
Choose from 4 corner positions:
- **Top-Left** (Ctrl+1)
- **Top-Right** (Ctrl+2) - Default
- **Bottom-Left** (Ctrl+3)  
- **Bottom-Right** (Ctrl+4)

### ⚡ **Quick Controls**
- **↗ Button**: Exit compact mode (return to full view)
- **S Button**: Generate new scramble
- **R Button**: Reset timer
- **All keyboard shortcuts still work** (Space, Ctrl+transparency, etc.)

### 🔄 **Seamless Integration**
- **Settings preserved**: Themes, transparency, preferences maintained
- **Timer functionality**: Full timing accuracy and state management
- **Statistics tracking**: All solves still recorded and tracked
- **Theme compatibility**: Works with all existing themes

## Usage

### **Method 1: Keyboard Shortcut (Recommended)**
```
Ctrl + M    →  Toggle compact mode on/off
Ctrl + 1    →  Position: Top-Left  
Ctrl + 2    →  Position: Top-Right
Ctrl + 3    →  Position: Bottom-Left
Ctrl + 4    →  Position: Bottom-Right
```

### **Method 2: Settings Dialog**
1. Click **⚙ (Settings)** button
2. Navigate to **"Appearance"** section
3. Set **"Compact mode position"** 
4. Click **"Apply"** to save
5. Use **Ctrl+M** to enter compact mode

## Perfect Use Cases

### **For Developers**
```
┌─────────────────────────────────────┐
│  VS Code - Full Screen              │
│  def solve_rubiks():                │
│      # Practicing F2L               │
│      cross = "F R U R' U' F'"       │
│      pair1 = "R U R' U' F R F'"     │
│      return solved                  │
│                                     │
│  # More code here...                │
│                            ┌─────── │
│                            │ 00:34.12│  ← Compact timer
│                            │         │
│                            │R U R' U'│
│                            │         │
│                            │[↗][S][R]│
│                            └─────────│
└─────────────────────────────────────┘
```

### **For Students**
- **Document editing**: Keep timer visible while writing
- **Online learning**: Overlay on video tutorials
- **Research**: Time practice sessions while taking notes

### **For Content Creators**
- **Streaming**: Professional timer overlay for viewers
- **Recording**: Minimal visual impact on content
- **Live competitions**: Clean, unobtrusive timer display

### **For Virtual Competitions**
- **Video calls**: Timer visible during online competitions
- **Screen sharing**: Minimal interference with shared content
- **Remote judging**: Clear timer visibility for judges

## Technical Details

### **Window Behavior**
- **Always on top**: Stays visible over all other applications
- **Fixed size**: 280x150 pixels for consistency
- **Smart positioning**: 20px margin from screen edges
- **Theme-aware**: Colors match your selected theme

### **Performance**
- **Minimal resources**: Reduced CPU and memory usage
- **Full accuracy**: No compromise on timing precision
- **Instant switching**: Sub-second transition between modes
- **State preservation**: All timer state maintained during mode changes

### **Cross-Platform**
- **Windows**: Native window management
- **macOS**: Full compatibility with native features  
- **Linux**: X11 and Wayland support

## Advanced Features

### **Transparency Integration**
Compact mode works seamlessly with transparency settings:
```
Ctrl + M        →  Enter compact mode
Ctrl + -        →  Make compact timer transparent
Ctrl + 1        →  Move to top-left corner
```

### **Smart Scramble Display**
- **Word wrapping**: Long scrambles automatically wrap
- **Font optimization**: Readable at small sizes
- **Theme consistency**: Matches your color preferences

### **Keyboard Accessibility**
All standard PSTimer shortcuts work in compact mode:
- **Space**: Ready/Start timer
- **Any key**: Stop timer
- **S**: New scramble  
- **R**: Reset timer
- **Transparency controls**: Ctrl+=/−/0

## Quick Start Guide

### **Basic Workflow**
1. **Start PSTimer** normally
2. **Position windows** - Open your code editor, documents, etc.
3. **Press Ctrl+M** to enter compact mode
4. **Press Ctrl+2** to position in top-right (or other corner)
5. **Adjust transparency** with Ctrl+− if needed
6. **Practice solving** while working on other tasks
7. **Press Ctrl+M** again to return to full mode when done

### **Pro Tips**
- **Use Ctrl+4** (bottom-right) for coding - keeps timer visible but out of the way
- **Use Ctrl+1** (top-left) for document work - easy to glance at
- **Combine with 60-70% transparency** for optimal visibility balance
- **Use Ctrl+0** to reset transparency if timer becomes hard to see

## Settings Persistence

### **Automatic Saving**
- **Position preference**: Your chosen corner is remembered
- **Mode state**: Application remembers if you prefer compact mode
- **Integration**: Compact settings saved with other preferences

### **Export/Import Compatible**
- Settings can be exported with session data
- Compact mode preferences included in configuration backup
- Seamless setup on new devices

## Troubleshooting

### **Timer Not Visible**
- Check transparency level (Ctrl+0 to reset)
- Verify position (try Ctrl+1-4 to cycle corners)
- Ensure no other applications are set to always-on-top

### **Controls Not Working**
- Click on compact timer to ensure focus
- Verify keyboard shortcuts in About dialog (Help menu)
- Try exiting and re-entering compact mode (Ctrl+M twice)

### **Performance Issues**
- Compact mode uses fewer resources than full mode
- If experiencing lag, try reducing transparency effects
- Close unnecessary background applications

---

## Complete Control Reference

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl + M` | Toggle compact mode | Switch between full and compact view |
| `Ctrl + 1` | Top-left position | Move compact timer to top-left corner |
| `Ctrl + 2` | Top-right position | Move compact timer to top-right corner |
| `Ctrl + 3` | Bottom-left position | Move compact timer to bottom-left corner |
| `Ctrl + 4` | Bottom-right position | Move compact timer to bottom-right corner |
| `Space` | Timer control | Hold to ready, release to start |
| `Any key` | Stop timer | Stop timing and record result |
| `S` | New scramble | Generate fresh scramble |
| `R` | Reset timer | Reset to 00:00.00 |
| `Ctrl + =` | More opaque | Increase window opacity |
| `Ctrl + -` | More transparent | Decrease window opacity |
| `Ctrl + 0` | Reset transparency | Return to fully opaque |

**🚀 Perfect for the modern speedcuber who codes, studies, or multitasks intensively!**

Compact mode gives you the freedom to practice speedcubing while maximizing productivity in your primary tasks. Whether you're a developer practicing algorithms during compilation, a student timing solves during study breaks, or a content creator needing an unobtrusive timer overlay, PSTimer's compact mode adapts to your workflow.
