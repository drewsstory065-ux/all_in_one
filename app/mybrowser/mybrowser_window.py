
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from .navigation_bar import NavigationBar
from .tab_widget import TabWidget

class MyBrowserWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Browser")
        self.setGeometry(100, 100, 1024, 768)

        self.tab_widget = TabWidget(self)
        self.navigation_bar = NavigationBar(self)

        self.addToolBar(self.navigation_bar)
        self.setCentralWidget(self.tab_widget)

        self.tab_widget.create_tab()

        self.navigation_bar.go_button.clicked.connect(self.navigate_to_url)
        self.navigation_bar.url_line_edit.returnPressed.connect(self.navigate_to_url)
        self.navigation_bar.back_button.clicked.connect(self.tab_widget.currentWidget().back)
        self.navigation_bar.next_button.clicked.connect(self.tab_widget.currentWidget().forward)
        self.navigation_bar.reload_button.clicked.connect(self.tab_widget.currentWidget().reload)

    def navigate_to_url(self):
        url = self.navigation_bar.url_line_edit.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.tab_widget.currentWidget().set_url(url)

    def closeEvent(self, event):
        self.close()
