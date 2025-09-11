# PSTimer Transparency Feature

## Overview
PSTimer now includes **window transparency settings** to enable multitasking while practicing speedcubing. This feature allows you to make the timer window semi-transparent so you can see and interact with other applications (like code editors, documents, or tutorials) while keeping the timer visible.

## Features Added

### 1. **Settings Dialog Integration**
- **Transparency Slider**: Adjustable from 30% to 100% opacity
- **Real-time Preview**: Percentage display updates as you adjust
- **Current Value Preservation**: Settings dialog loads your current transparency level
- **Help Text**: Clear explanation of the feature's purpose

### 2. **Keyboard Shortcuts**
Perfect for quick adjustments while coding or working:
- **Ctrl + =**: Increase transparency (more opaque)
- **Ctrl + -**: Decrease transparency (more see-through)  
- **Ctrl + 0**: Reset to fully opaque (100%)

### 3. **Automatic Boundaries**
- **Minimum**: 30% opacity (prevents window from becoming invisible)
- **Maximum**: 100% opacity (fully opaque)
- **Smooth Increments**: 5% steps for precise control

## Usage Scenarios

### **Perfect for Developers**
```
┌─────────────────┐    ┌─────────────────┐
│   Code Editor   │    │  PSTimer (50%)  │
│                 │    │                 │
│ def solve():    │    │    00:45.23     │
│   # algorithm   │    │                 │
│   R U R' U'     │    │   F R U R' U'   │
│                 │    │                 │
└─────────────────┘    └─────────────────┘
```

### **Great for Document Work**
- Timer overlay on documents while practicing
- Keep track of solve times during virtual competitions
- Monitor progress while taking notes

### **Video Tutorials**
- Watch solving tutorials with timer overlay
- Practice along with YouTube videos
- Keep timer visible during online lessons

## Technical Implementation

### **Window Alpha Channel**
- Uses Tkinter's `wm_attributes("-alpha", value)` 
- Cross-platform compatibility (Windows, macOS, Linux)
- Hardware-accelerated rendering

### **Settings Persistence**
- Transparency level saved with other user preferences
- Restored when application restarts
- Integrated with existing settings system

### **Real-time Updates**
- Immediate visual feedback when adjusting
- No application restart required
- Smooth transitions between opacity levels

## Controls Reference

### **Via Settings Dialog**
1. Click **⚙ (Settings)** button
2. Navigate to **"Appearance"** section
3. Adjust **"Window transparency"** slider
4. Click **"Apply"** to save changes

### **Via Keyboard Shortcuts**
| Shortcut | Action | Result |
|----------|--------|---------|
| `Ctrl + =` | Increase opacity | +5% more visible |
| `Ctrl + -` | Decrease opacity | +5% more transparent |  
| `Ctrl + 0` | Reset transparency | 100% opaque |

## Best Practices

### **Recommended Transparency Levels**
- **80-90%**: Light transparency for coding
- **60-70%**: Medium transparency for documents
- **40-50%**: High transparency for video tutorials
- **30%**: Maximum transparency (minimum allowed)

### **Productivity Tips**
1. **Start at 80%** and adjust based on background content
2. **Use keyboard shortcuts** for quick adjustments
3. **Reset to 100%** during focused solving sessions
4. **Lower to 50%** when learning new algorithms

## Integration with Existing Features

### **Works with All Themes**
- csTimer (default)
- Dark theme
- Blue theme

### **Maintains All Functionality**
- Full timer operations
- Statistics tracking
- Session management
- 3D cube visualization
- Scramble generation

### **Keyboard Compatibility** 
- Transparency shortcuts don't interfere with existing controls
- Space bar still controls timer
- 'S' and 'R' shortcuts remain functional

## Benefits for Speedcubers

### **Enhanced Practice Sessions**
- **Multi-task efficiently**: Code while practicing F2L
- **Learn continuously**: Keep tutorials visible during practice
- **Track progress**: Monitor times while taking notes
- **Stay organized**: Access other apps without losing timer

### **Competition Preparation**
- **Simulate distractions**: Practice with background applications
- **Time management**: Track solving while managing competition notes
- **Virtual competitions**: Overlay timer on video calls

### **Learning & Development**
- **Algorithm practice**: Keep notation visible while timing
- **Tutorial integration**: Follow along with video guides
- **Documentation**: Take notes while tracking improvement

---

## Quick Start Guide

1. **Open PSTimer**
2. **Press Ctrl + -** a few times to make window transparent
3. **Open your code editor/document** behind the timer
4. **Practice solving** while working on other tasks
5. **Press Ctrl + 0** to return to full opacity when needed

**Perfect for the modern speedcuber who codes, studies, or multitasks! 🚀**
