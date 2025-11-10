
from PyQt6.QtCore import QUrl, QStandardPaths, pyqtSignal
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtWebEngineWidgets import QWebEngineView

class WebView(QWebEngineView):
    title_changed = pyqtSignal(str, str)  # Emits (title, url) when page title changes

    def __init__(self, parent=None, profile=None):
        if profile:
            super().__init__(profile, parent)
        else:
            super().__init__(parent)
        
        self.settings().setAttribute(
            self.settings().WebAttribute.JavascriptEnabled, True
        )
        self.settings().setAttribute(
            self.settings().WebAttribute.LocalStorageEnabled, True
        )
        self.settings().setAttribute(
            self.settings().WebAttribute.PluginsEnabled, True
        )
        
        # Connect signals for tracking page changes
        self.titleChanged.connect(self.on_title_changed)
        self.urlChanged.connect(self.on_url_changed)
        
        self.load(QUrl("https://www.google.com"))

    def set_url(self, url):
        self.load(QUrl(url))

    def on_title_changed(self, title):
        """Handle title changes and emit signal with current URL"""
        current_url = self.url().toString()
        self.title_changed.emit(title, current_url)

    def on_url_changed(self, url):
        """Handle URL changes and update title if needed"""
        # The title will be updated automatically via titleChanged signal
        pass
