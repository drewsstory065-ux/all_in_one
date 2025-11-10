
from PyQt6.QtCore import QUrl, QStandardPaths
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtWebEngineWidgets import QWebEngineView

class WebView(QWebEngineView):
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
        self.load(QUrl("https://www.google.com"))

    def set_url(self, url):
        self.load(QUrl(url))

