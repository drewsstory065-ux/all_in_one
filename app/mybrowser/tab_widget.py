
from PyQt6.QtCore import QUrl, QStandardPaths, pyqtSignal
from PyQt6.QtWidgets import QTabWidget, QPushButton
from PyQt6.QtWebEngineCore import QWebEngineProfile
from .web_view import WebView

class TabWidget(QTabWidget):
    tab_count_changed = pyqtSignal(int)  # Signal emitted when tab count changes

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.setMovable(True)

        # Add new tab button
        self.new_tab_button = QPushButton("+")
        self.new_tab_button.setFixedSize(30, 30)
        self.new_tab_button.clicked.connect(self.create_tab)
        self.setCornerWidget(self.new_tab_button)

        self.profile = QWebEngineProfile("my-profile", self)
        self.profile.setPersistentStoragePath(
            QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        )

    def create_tab(self, url="https://www.google.com"):
        web_view = WebView(profile=self.profile)
        if url:
            web_view.load(QUrl(url))
        index = self.addTab(web_view, "New Tab")
        self.setCurrentIndex(index)
        web_view.urlChanged.connect(
            lambda qurl, view=web_view: self.update_tab_title(view, qurl)
        )
        
        # Emit tab count changed signal
        self.tab_count_changed.emit(self.count())
        
        return web_view

    def close_tab(self, index):
        if self.count() > 1:
            self.removeTab(index)
            self.tab_count_changed.emit(self.count())
        else:
            self.parent().close()

    def update_tab_title(self, view, qurl):
        index = self.indexOf(view)
        if index != -1:
            title = view.page().title()
            if not title:
                title = "New Tab"
            self.setTabText(index, title[:20] + "..." if len(title) > 20 else title)

    def create_tab_with_url(self, url):
        """Create a new tab with a specific URL"""
        return self.create_tab(url)
