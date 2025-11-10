from PyQt6.QtCore import QObject, QTimer
from PyQt6.QtWebEngineCore import QWebEnginePage

class AdBlockerController(QObject):
    """Coordinates between model and web views for ad blocking functionality"""
    
    def __init__(self, ad_blocker_model, parent=None):
        super().__init__(parent)
        self.model = ad_blocker_model
        self.current_web_view = None
        
        # JavaScript code for YouTube ad blocking
        self.ad_blocker_script = """
// YouTube Ad Blocker Script - Less Aggressive Version
(function() {
    'use strict';
    
    console.log('YouTube Ad Blocker injected');
    
    // Function to skip pre-roll ads
    function skipPreRollAds() {
        try {
            const skipButton = document.querySelector('.ytp-ad-skip-button, .ytp-ad-skip-button-modern');
            if (skipButton && skipButton.offsetParent !== null) {
                console.log('Skipping pre-roll ad');
                skipButton.click();
                return true;
            }
        } catch (e) {
            console.log('Error skipping pre-roll ad:', e);
        }
        return false;
    }
    
    // Function to detect and skip mid-roll ads
    function skipMidRollAds() {
        try {
            const adDisplay = document.querySelector('.ad-showing, .ad-interrupting');
            if (adDisplay) {
                console.log('Skipping mid-roll ad');
                const video = document.querySelector('video');
                if (video && !isNaN(video.duration)) {
                    video.currentTime = video.duration;
                }
                return true;
            }
        } catch (e) {
            console.log('Error skipping mid-roll ad:', e);
        }
        return false;
    }
    
    // Function to remove ad overlays
    function removeAdOverlays() {
        try {
            const overlays = document.querySelectorAll('.ytp-ad-overlay-container, .ytp-ad-message-container');
            let removed = 0;
            overlays.forEach(overlay => {
                if (overlay && overlay.parentNode) {
                    console.log('Removing ad overlay');
                    overlay.remove();
                    removed++;
                }
            });
            return removed > 0;
        } catch (e) {
            console.log('Error removing overlays:', e);
            return false;
        }
    }
    
    // Function to block ad requests (more targeted)
    function blockAdRequests() {
        try {
            // Only target specific ad elements that are clearly ads, avoiding video player
            const adElements = document.querySelectorAll(
                '.ytd-ad-slot-renderer, .video-ads, .ad-container, .ad-div, .ad-overlay, .ad-slot, .ad-slot-wrapper'
            );
            adElements.forEach(element => {
                if (element && element.style && element.style.display !== 'none') {
                    // Check if element is not part of the main video player
                    const videoPlayer = document.querySelector('#movie_player, .html5-video-player');
                    if (!videoPlayer || !videoPlayer.contains(element)) {
                        element.style.display = 'none';
                    }
                }
            });
        } catch (e) {
            console.log('Error blocking ad requests:', e);
        }
    }
    
    // Main ad blocking function with safety checks
    function blockYouTubeAds() {
        try {
            let blocked = false;
            
            // Only run if page is fully loaded
            if (document.readyState === 'complete') {
                blocked = skipPreRollAds() || blocked;
                blocked = skipMidRollAds() || blocked;
                blocked = removeAdOverlays() || blocked;
                blockAdRequests();
            }
            
            return blocked;
        } catch (e) {
            console.log('Error in ad blocking:', e);
            return false;
        }
    }
    
    // Wait for page to be fully ready before starting
    function initializeAdBlocker() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(startAdBlocker, 1000);
            });
        } else {
            setTimeout(startAdBlocker, 1000);
        }
    }
    
    function startAdBlocker() {
        console.log('Starting YouTube ad blocker');
        
        // Run ad blocking periodically with longer interval
        const adBlockInterval = setInterval(blockYouTubeAds, 2000);
        
        // Also run when video state changes
        const video = document.querySelector('video');
        if (video) {
            video.addEventListener('timeupdate', blockYouTubeAds);
            video.addEventListener('play', blockYouTubeAds);
            video.addEventListener('loadeddata', blockYouTubeAds);
        }
        
        // Clean up when page unloads
        window.addEventListener('beforeunload', function() {
            clearInterval(adBlockInterval);
        });
    }
    
    // Initialize the ad blocker
    initializeAdBlocker();
    
})();
"""

    def on_url_changed(self, url):
        """Handle URL changes to detect YouTube pages"""
        if self.model.is_youtube_url(url):
            print(f"Detected YouTube page: {url.toString()}")
            # Schedule JavaScript injection after page loads with longer delay
            QTimer.singleShot(2000, self.inject_ad_blocker_script)
        else:
            print(f"Non-YouTube page: {url.toString()}")

    def on_page_loaded(self, success):
        """Handle page load completion"""
        if success and self.current_web_view:
            current_url = self.current_web_view.url()
            if self.model.is_youtube_url(current_url) and self.model.enabled:
                print("Injecting ad blocker script on YouTube page")
                # Use longer delay to ensure YouTube is fully loaded
                QTimer.singleShot(1500, self.inject_ad_blocker_script)

    def set_current_web_view(self, web_view):
        """Set the current web view for ad blocking"""
        self.current_web_view = web_view
        
        if web_view:
            # Connect to web view events
            web_view.urlChanged.connect(self.on_url_changed)
            web_view.loadFinished.connect(self.on_page_loaded)

    def inject_ad_blocker_script(self):
        """Inject ad blocking JavaScript into the current web view"""
        if not self.current_web_view or not self.model.enabled:
            return
            
        current_url = self.current_web_view.url()
        if self.model.is_youtube_url(current_url):
            try:
                self.current_web_view.page().runJavaScript(self.ad_blocker_script)
                print("Ad blocker script injected successfully")
            except Exception as e:
                print(f"Failed to inject ad blocker script: {e}")

    def toggle_ad_blocking(self):
        """Toggle ad blocking and update current page if needed"""
        new_state = self.model.toggle_ad_blocking()
        
        # If ad blocking was just enabled and we're on YouTube, inject script
        if new_state and self.current_web_view:
            current_url = self.current_web_view.url()
            if self.model.is_youtube_url(current_url):
                self.inject_ad_blocker_script()
        
        return new_state
