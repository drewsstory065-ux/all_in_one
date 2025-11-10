
from PyQt6.QtCore import QUrl, QStandardPaths
from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtWebEngineCore import QWebEngineProfile
from .web_view import WebView

class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.setMovable(True)

        self.profile = QWebEngineProfile("my-profile", self)
        self.profile.setPersistentStoragePath(
            QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        )

    def create_tab(self, url="https://www.google.com"):
        web_view = WebView(profile=self.profile)
        web_view.load(QUrl(url))
        index = self.addTab(web_view, "New Tab")
        self.setCurrentIndex(index)
        web_view.urlChanged.connect(
            lambda qurl, view=web_view: self.update_tab_title(view, qurl)
        )
        return web_view

    def close_tab(self, index):
        if self.count() > 1:
            self.removeTab(index)
        else:
            self.parent().close()

    def update_tab_title(self, view, qurl):
        index = self.indexOf(view)
        if index != -1:
            self.setTabText(index, view.page().title())

