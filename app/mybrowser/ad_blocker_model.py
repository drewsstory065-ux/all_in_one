from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import QSettings

class AdBlockerModel(QObject):
    """Manages ad blocking rules, YouTube detection, and user preferences"""
    
    # Signals
    ad_blocking_state_changed = pyqtSignal(bool)  # Emits when ad blocking is enabled/disabled
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("MyBrowser", "AdBlocker")
        
        # Load ad blocking state from persistent storage
        self._enabled = self.settings.value("ad_blocking_enabled", True, type=bool)
        
        # YouTube domain patterns
        self.youtube_domains = [
            "youtube.com",
            "www.youtube.com",
            "m.youtube.com",
            "youtu.be"
        ]

    @property
    def enabled(self):
        """Get current ad blocking state"""
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        """Set ad blocking state and persist to storage"""
        if self._enabled != value:
            self._enabled = value
            self.settings.setValue("ad_blocking_enabled", value)
            self.ad_blocking_state_changed.emit(value)

    def is_youtube_url(self, url):
        """Check if URL is a YouTube domain"""
        if not url:
            return False
        
        url_str = url.toString() if hasattr(url, 'toString') else str(url)
        
        for domain in self.youtube_domains:
            if domain in url_str:
                return True
        return False

    def toggle_ad_blocking(self):
        """Toggle ad blocking state"""
        self.enabled = not self.enabled
        return self.enabled

    def get_ad_blocking_status(self):
        """Get current ad blocking status for display"""
        return "🔇" if self.enabled else "🔊"

    def get_ad_blocking_tooltip(self):
        """Get tooltip text for ad blocking status"""
        status = "enabled" if self.enabled else "disabled"
        return f"Ad blocking is {status}. Click to toggle."
