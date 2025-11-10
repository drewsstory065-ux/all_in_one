from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QListWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QGuiApplication
from datetime import datetime


class HistoryWidget(QWidget):
    history_item_clicked = pyqtSignal(str)  # Emits URL when history item is clicked

    def __init__(self, history_model, parent=None):
        super().__init__(parent)
        self.history_model = history_model
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        self.setup_ui()
        self.populate_history()
        
        # Connect signals
        self.history_model.history_changed.connect(self.populate_history)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # History list
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.on_history_item_clicked)
        layout.addWidget(self.history_list)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        self.clear_button = QPushButton("Clear History")
        self.clear_button.clicked.connect(self.history_model.clear_history)
        buttons_layout.addWidget(self.clear_button)
        
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.hide)
        buttons_layout.addWidget(self.close_button)
        
        layout.addLayout(buttons_layout)

    def populate_history(self):
        self.history_list.clear()
        history_items = self.history_model.get_history()
        
        for item in history_items:
            # Format the display text
            timestamp = item.timestamp.strftime("%Y-%m-%d %H:%M")
            display_text = f"{item.title}\n{item.url}\n{timestamp}"
            
            list_item = QListWidgetItem(display_text)
            list_item.setData(Qt.ItemDataRole.UserRole, item.url)
            self.history_list.addItem(list_item)

    def on_history_item_clicked(self, item):
        url = item.data(Qt.ItemDataRole.UserRole)
        self.history_item_clicked.emit(url)
        self.hide()
