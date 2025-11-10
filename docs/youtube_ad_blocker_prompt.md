# AI Implementation Prompt: YouTube Ad Blocker Feature

## Feature Requirements
Implement an ad blocking system specifically for YouTube that:
- **Detects YouTube pages** automatically when user navigates to youtube.com
- **Blocks/skips video ads** that appear before videos start playing
- **Skips mid-roll ads** that interrupt videos during playback
- **Provides visual feedback** when ads are blocked (optional status indicator)
- **Respects user preferences** with enable/disable toggle

## Technical Approach Options

### Option 1: JavaScript Injection (Recommended)
Inject custom JavaScript into YouTube pages to:
- Intercept and block ad requests
- Skip ad segments in video players
- Remove ad overlays and banners

### Option 2: Content Blocking
Use QtWebEngine's content blocking capabilities:
- Block ad domains and scripts
- Remove ad elements from DOM
- Intercept network requests

### Option 3: Hybrid Approach
Combine JavaScript injection with content blocking for maximum effectiveness.

## Implementation Architecture

### 1. Ad Blocker Model (`app/mybrowser/ad_blocker_model.py`)
```python
class AdBlockerModel(QObject):
    # Manages ad blocking rules, YouTube detection, user preferences
    # Persistent storage for enabled/disabled state
    # YouTube domain detection logic
    pass
```

### 2. Ad Blocker Controller (`app/mybrowser/ad_blocker_controller.py`)
```python
class AdBlockerController(QObject):
    # Coordinates between model and web views
    # Injects JavaScript into YouTube pages
    # Monitors page navigation for YouTube detection
    # Handles ad blocking logic
    pass
```

### 3. Navigation Bar Integration
- Add small toggle button (🔇/🔊) to enable/disable ad blocking
- Visual indicator when ad blocking is active on YouTube
- Tooltip showing ad blocking status

### 4. Web View Integration
- Extend WebView to support JavaScript injection
- Connect to ad blocker controller for YouTube pages
- Handle page load events for domain detection

## Critical Implementation Details

### YouTube Detection
```python
def is_youtube_url(url):
    return "youtube.com" in url or "youtu.be" in url
```

### JavaScript Injection Pattern
```python
def inject_ad_blocker_script(web_view):
    javascript_code = """
    // YouTube ad blocking logic
    // - Skip pre-roll ads
    // - Block mid-roll ads  
    // - Remove ad overlays
    // - Bypass ad segments
    """
    web_view.page().runJavaScript(javascript_code)
```

### Safe Script Injection
- Inject only on YouTube domains
- Handle injection failures gracefully
- Avoid breaking YouTube functionality
- Test with various YouTube page types (home, watch, search)

## Ad Blocking Strategies

### Pre-roll Ad Skipping
```javascript
// Detect and skip video ads before content
const skipAd = () => {
    const skipButton = document.querySelector('.ytp-ad-skip-button, .ytp-ad-skip-button-modern');
    if (skipButton) {
        skipButton.click();
        return true;
    }
    return false;
};
```

### Mid-roll Ad Detection
```javascript
// Monitor for mid-roll ads during playback
const checkForAds = () => {
    const adDisplay = document.querySelector('.ad-showing, .ad-interrupting');
    if (adDisplay) {
        // Try to skip ad or seek past it
        const video = document.querySelector('video');
        if (video) {
            video.currentTime = video.duration;
        }
    }
};
```

### Ad Overlay Removal
```javascript
// Remove banner ads and overlays
const removeOverlays = () => {
    const overlays = document.querySelectorAll('.ytp-ad-overlay-container, .ytp-ad-message-container');
    overlays.forEach(overlay => overlay.remove());
};
```

## Integration Points

### Main Window Integration
```python
# In mybrowser_window.py
self.ad_blocker_model = AdBlockerModel(self)
self.ad_blocker_controller = AdBlockerController(self.ad_blocker_model, self)

# Connect to web view events
web_view.urlChanged.connect(self.ad_blocker_controller.on_url_changed)
web_view.loadFinished.connect(self.ad_blocker_controller.on_page_loaded)
```

### Navigation Bar Button
- Add small mute/unmute icon button
- Toggle ad blocking on/off
- Show visual feedback when active on YouTube
- Store user preference persistently

## Common Challenges & Solutions

### Challenge: YouTube Anti-Adblock Detection
**Solution**: Use subtle blocking techniques, rotate user agents, implement detection evasion

### Challenge: Breaking YouTube Functionality  
**Solution**: Test extensively, use minimal interference approach, provide disable option

### Challenge: Performance Impact
**Solution**: Optimize JavaScript, inject only when needed, use efficient selectors

### Challenge: Legal Considerations
**Solution**: Make it optional, educate users about ad-supported content, respect platform terms

## Testing Requirements

### Functional Testing
- [ ] YouTube homepage loads normally
- [ ] Video playback works without ads
- [ ] Pre-roll ads are skipped automatically
- [ ] Mid-roll ads are bypassed
- [ ] Ad overlays are removed
- [ ] Non-YouTube sites unaffected
- [ ] Toggle functionality works
- [ ] Preferences persist across sessions

### Performance Testing
- [ ] No significant page load delay
- [ ] Smooth video playback
- [ ] Minimal memory usage
- [ ] Efficient JavaScript execution

### Edge Cases
- [ ] YouTube live streams
- [ ] YouTube embedded players
- [ ] Multiple tabs with YouTube
- [ ] Network connectivity issues
- [ ] YouTube UI updates

## Implementation Priority

### Phase 1: Basic Ad Skipping
1. YouTube domain detection
2. Pre-roll ad skip button automation
3. Simple toggle functionality

### Phase 2: Enhanced Blocking
1. Mid-roll ad detection and skipping
2. Ad overlay removal
3. Performance optimization

### Phase 3: Advanced Features
1. Anti-adblock evasion
2. Custom blocking rules
3. Statistics and reporting

## Success Criteria
- YouTube videos play without interruption from ads
- No broken YouTube functionality
- Minimal performance impact
- User-controlled enable/disable
- No console errors or warnings
- Works across different YouTube page types

## Important Considerations
- **User Control**: Always provide enable/disable option
- **Transparency**: Clearly indicate when ad blocking is active
- **Responsibility**: Educate users about content creator support
- **Maintenance**: YouTube frequently updates, so ad blocking may need updates
- **Legality**: Ensure compliance with local laws and platform terms

This implementation should focus on providing a smooth, uninterrupted YouTube viewing experience while maintaining browser stability and user control.
