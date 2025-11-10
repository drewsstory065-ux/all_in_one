from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(150, 100)
        self.setWindowFlags(
            Qt.WindowType.Window 
            | Qt.WindowType.WindowCloseButtonHint 
            | Qt.WindowType.WindowMinimizeButtonHint
        )
        self.setStyleSheet("background-color: lightgray;")
        self.move_to_bottom_right()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        browser_btn = QPushButton("Open Browser")
        browser_btn.clicked.connect(self.open_browser)
        layout.addWidget(browser_btn)

        video_btn = QPushButton("Video Player")
        video_btn.clicked.connect(self.open_video_player)
        layout.addWidget(video_btn)
        
        self.setLayout(layout)

    def move_to_bottom_right(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        x = screen_geometry.width() - self.width()
        y = screen_geometry.height() - self.height()
        self.setGeometry(x, y, self.width(), self.height())

    def showEvent(self, event):
        super().showEvent(event)
        self.move_to_bottom_right()
    
    def open_browser(self):
        from app.mybrowser.mybrowser_window import MyBrowserWindow
        self.browser_window = MyBrowserWindow()
        self.browser_window.show()
    
    def open_video_player(self):
        from app.myvid.myvid_window import MyVidWindow
        self.video_window = MyVidWindow()
        self.video_window.show()
