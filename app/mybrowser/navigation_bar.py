
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QToolBar, QLineEdit, QPushButton

class NavigationBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIconSize(QSize(24, 24))

        self.back_button = QPushButton("<", self)
        self.next_button = QPushButton(">", self)
        self.reload_button = QPushButton("Reload", self)
        self.url_line_edit = QLineEdit(self)
        self.go_button = QPushButton("Go", self)

        self.back_button.setFixedSize(30, 30)
        self.next_button.setFixedSize(30, 30)

        self.addWidget(self.back_button)
        self.addWidget(self.next_button)
        self.addWidget(self.reload_button)
        self.addWidget(self.url_line_edit)
        self.addWidget(self.go_button)
