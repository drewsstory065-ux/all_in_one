# Video Player Issue Explanation for AI Assistant

## User Request
The user is experiencing issues with a PyQt6 video player application where:
1. **Original Issue**: AAC timestamp errors when using the forward button
2. **Current Issue**: Video plays for 7 seconds then restarts in an infinite loop

## Application Overview
- **Framework**: PyQt6 with QMediaPlayer and QVideoWidget
- **Video Player**: Custom video player with playlist functionality
- **File**: `app/myvid/myvid_window.py`

## Technical Details

### Original Implementation (Working)
The video player had simple seeking functionality:
```python
def on_forward(self):
    if self.media_player.duration() > 0:
        new_position = min(self.media_player.duration(), self.media_player.position() + 5000)
        self.media_player.setPosition(new_position)
```

### Issues Encountered

#### 1. AAC Timestamp Errors
**Symptoms**: Console output showing:
```
[aac @ 0x617ea1bdb440] Could not update timestamps for skipped samples.
```

**Root Cause**: FFmpeg AAC decoder warnings during seeking operations. These are non-fatal but annoying debug messages.

#### 2. 7-Second Loop Issue
**Symptoms**: Video plays for exactly 7 seconds, then restarts from beginning in an infinite loop.

**Attempted Fixes**:
1. **Safe Seek Method**: Added `_safe_seek()` that pauses playback before seeking and resumes after
   - **Result**: Caused crashes after 7 seconds
   
2. **Simplified Safe Seek**: Removed pausing logic, kept only error handling
   - **Result**: Still caused 7-second loop issue

3. **Reverted to Original**: Went back to simple direct seeking
   - **Result**: No crashes, but 7-second loop issue returned

### Current Code State
The code has been reverted to the original simple implementation:
```python
def on_forward(self):
    if self.media_player.duration() > 0:
        new_position = min(self.media_player.duration(), self.media_player.position() + 5000)
        self.media_player.setPosition(new_position)
```

## Fix Attempt 1: Enhanced Media Status Debugging
**Changes Made**: Modified `on_media_status_changed` method in `app/myvid/myvid_window.py`:
- Added detailed logging for all media status changes
- Increased the EndOfMedia detection threshold from 1 second to 2 seconds
- Added debug prints for all media status types to help identify timing issues

**Expected Outcome**: Better visibility into when EndOfMedia is triggered and whether it's a false positive at exactly 7 seconds.

**Status**: **Issue persists** - 7-second loop still occurs after this change.

## Fix Attempt 2: Remove Auto-Play After Video Selection
**Changes Made**: Modified `on_select_video` method in `app/myvid/myvid_window.py`:
- Removed the automatic playback after video selection (`self.media_player.play()`)
- Now requires user to manually click the play button to start playback
- This reverts to the original behavior where user selects video then clicks play

**Root Cause Hypothesis**: The auto-play feature may be causing timing issues with media loading and playback initialization, leading to premature EndOfMedia detection at exactly 7 seconds.

**Expected Outcome**: By requiring manual play button click, the media player has more time to properly initialize and load the video, potentially resolving the 7-second loop issue.

**Status**: **Testing needed** - This change should be tested to see if it resolves the 7-second loop issue.

## Key Observations
- The 7-second loop issue appears to be timing-related
- The issue occurs regardless of seeking implementation
- The video plays normally for exactly 7 seconds before restarting
- No crashes in current state, but infinite loop persists

## Files to Examine
- `app/myvid/myvid_window.py` - Main video player window
- `app/myvid/control_bar.py` - Control bar with forward button
- `app/myvid/video_display.py` - Video display component
- `app/myvid/playlist_manager.py` - Playlist management

## Suspected Areas
1. **Media Status Handling**: Check `on_media_status_changed` method for premature EndOfMedia detection
2. **Timer Issues**: The QTimer used for UI updates might be interfering
3. **Playlist Auto-advance**: The playlist might be auto-advancing incorrectly
4. **Signal/Slot Connections**: Possible signal conflicts causing restart behavior

## Request for AI Assistant
Please analyze the video player code and identify why the video restarts after exactly 7 seconds. Focus on:
- Media status detection
- Timer configurations  
- Playlist auto-advance logic
- Signal/slot connections that might trigger restart

The goal is to fix the 7-second loop while maintaining forward button functionality and ideally reducing AAC timestamp warnings.
