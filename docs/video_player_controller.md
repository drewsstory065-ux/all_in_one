# Video Player Controller Documentation

## Overview

The video player controller is a PyQt6-based application that provides a complete video playback interface with intuitive controls. This document details the implementation of the control bar and its components.

## Architecture

### Main Components

1. **MyVidWindow** (`myvid_window.py`) - Main window that integrates all components
2. **ControlBar** (`control_bar.py`) - Control interface with playback controls
3. **VideoDisplay** (`video_display.py`) - Video rendering component
4. **VideoPlayerStyles** (`styles.py`) - Styling definitions

## Control Bar Implementation

### ControlBar Class

The `ControlBar` class provides all playback controls and timeline functionality.

#### Key Features

- **Playback Controls**: Play/pause, rewind, forward buttons
- **Timeline Slider**: Visual progress indicator and seeking
- **Volume Control**: Volume slider with mute functionality
- **Time Display**: Current and total time labels
- **Fullscreen Toggle**: Fullscreen mode control
- **Video Selection**: File browser integration

#### Signal Definitions

```python
# Control actions
rewind_fast = pyqtSignal()
rewind = pyqtSignal()
play_pause = pyqtSignal()
forward = pyqtSignal()
forward_fast = pyqtSignal()
seek = pyqtSignal(int)  # Position percentage (0-100)
volume_changed = pyqtSignal(int)  # Volume level 0-100
volume_display_toggled = pyqtSignal()
toggle_fullscreen = pyqtSignal()
select_video = pyqtSignal()
```

#### Button Functions

- **📁 Select Video**: Opens file dialog to choose video file
- **<< Fast Rewind**: Rewinds 10 seconds
- **< Rewind**: Rewinds 5 seconds
- **>/■ Play/Pause**: Toggles playback state
- **> Forward**: Forwards 5 seconds
- **>> Fast Forward**: Forwards 10 seconds
- **🔊 Volume**: Toggles volume slider visibility
- **⬚ Fullscreen**: Toggles fullscreen mode

#### Timeline Implementation

The timeline uses a custom slider implementation that:
- Shows current progress as percentage (0-100)
- Allows seeking by clicking or dragging
- Updates in real-time during playback
- Handles edge cases (no video loaded, zero duration)

#### Volume Control

- **Volume Slider**: Hidden by default, toggled by volume button
- **Visual Feedback**: Button icon changes based on volume level
- **Mute State**: Shows mute icon when volume is 0

## MyVidWindow Integration

### Signal Connections

The main window connects control bar signals to corresponding methods:

```python
# Control bar signals
self.control_bar.select_video.connect(self.on_select_video)
self.control_bar.rewind_fast.connect(self.on_rewind_fast)
self.control_bar.rewind.connect(self.on_rewind)
self.control_bar.play_pause.connect(self.on_play_pause)
self.control_bar.forward.connect(self.on_forward)
self.control_bar.forward_fast.connect(self.on_forward_fast)
self.control_bar.seek.connect(self.on_seek)
self.control_bar.volume_changed.connect(self.on_volume_changed)
self.control_bar.volume_display_toggled.connect(self.on_toggle_volume_display)
self.control_bar.toggle_fullscreen.connect(self.on_toggle_fullscreen)
```

### Key Methods

#### on_seek(position)
Handles timeline seeking by converting percentage to media position:
```python
def on_seek(self, position):
    """Handle timeline seeking."""
    duration = self.media_player.duration()
    if duration > 0:
        seek_position = int((position / 100) * duration)
        self.media_player.setPosition(seek_position)
```

#### on_volume_changed(volume)
Updates audio output volume and control bar display:
```python
def on_volume_changed(self, volume):
    """Handle volume level changes."""
    audio_output = self.media_player.audioOutput()
    if audio_output:
        audio_output.setVolume(volume / 100.0)
    self.control_bar.set_volume(volume)
```

## Styling

All styling is defined in `VideoPlayerStyles` class with consistent theming:
- **Button Styles**: Rounded buttons with hover effects
- **Slider Styles**: Custom progress bars with visual feedback
- **Time Labels**: Monospaced fonts for alignment
- **Control Bar**: Compact layout with proper spacing

## Keyboard Shortcuts

- **Space**: Play/Pause
- **Left Arrow**: Rewind 5 seconds
- **Right Arrow**: Forward 5 seconds
- **F**: Toggle fullscreen
- **Esc**: Exit fullscreen

## Error Handling

The implementation includes robust error handling:
- **No Video Loaded**: Timeline and controls disabled
- **Zero Duration**: Prevents division by zero errors
- **Invalid Files**: Graceful file selection failure
- **Signal Conflicts**: Unique signal names to avoid conflicts

## Dependencies

- **PyQt6**: Main GUI framework
- **PyQt6-Multimedia**: Video and audio playback
- **FFmpeg**: Media codec support (system dependency)

## File Structure

```
app/myvid/
├── myvid_window.py    # Main window implementation
├── control_bar.py     # Control interface
├── video_display.py   # Video rendering
├── styles.py          # Styling definitions
└── test_video_player.py # Testing utility
```

This architecture provides a modular, maintainable video player with professional-grade controls and robust error handling.
