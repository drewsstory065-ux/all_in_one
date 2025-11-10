from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QListWidgetItem, QMenu, QInputDialog
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QGuiApplication, QAction
from datetime import datetime


class BookmarkWidget(QWidget):
    bookmark_item_clicked = pyqtSignal(str)  # Emits URL when bookmark item is clicked

    def __init__(self, bookmark_model, parent=None):
        super().__init__(parent)
        self.bookmark_model = bookmark_model
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        self.setup_ui()
        self.populate_bookmarks()
        
        # Connect signals
        self.bookmark_model.bookmarks_changed.connect(self.populate_bookmarks)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Bookmark list
        self.bookmark_list = QListWidget()
        self.bookmark_list.itemClicked.connect(self.on_bookmark_item_clicked)
        self.bookmark_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.bookmark_list.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.bookmark_list)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Add Current")
        self.add_button.clicked.connect(self.add_current_bookmark)
        buttons_layout.addWidget(self.add_button)
        
        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.bookmark_model.clear_bookmarks)
        buttons_layout.addWidget(self.clear_button)
        
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.hide)
        buttons_layout.addWidget(self.close_button)
        
        layout.addLayout(buttons_layout)

    def populate_bookmarks(self):
        self.bookmark_list.clear()
        bookmark_items = self.bookmark_model.get_bookmarks()
        
        for item in bookmark_items:
            # Format the display text
            timestamp = item.timestamp.strftime("%Y-%m-%d %H:%M")
            folder_info = f" [{item.folder}]" if item.folder else ""
            display_text = f"{item.title}{folder_info}\n{item.url}\n{timestamp}"
            
            list_item = QListWidgetItem(display_text)
            list_item.setData(Qt.ItemDataRole.UserRole, item.url)
            self.bookmark_list.addItem(list_item)

    def on_bookmark_item_clicked(self, item):
        url = item.data(Qt.ItemDataRole.UserRole)
        self.bookmark_item_clicked.emit(url)
        self.hide()

    def show_context_menu(self, position):
        item = self.bookmark_list.itemAt(position)
        if not item:
            return
            
        url = item.data(Qt.ItemDataRole.UserRole)
        menu = QMenu(self)
        
        # Open in current tab
        open_current_action = QAction("Open in Current Tab", self)
        open_current_action.triggered.connect(lambda: self.open_bookmark_in_current_tab(url))
        menu.addAction(open_current_action)
        
        # Open in new tab
        open_new_action = QAction("Open in New Tab", self)
        open_new_action.triggered.connect(lambda: self.open_bookmark_in_new_tab(url))
        menu.addAction(open_new_action)
        
        menu.addSeparator()
        
        # Edit folder
        edit_folder_action = QAction("Edit Folder", self)
        edit_folder_action.triggered.connect(lambda: self.edit_bookmark_folder(url))
        menu.addAction(edit_folder_action)
        
        menu.addSeparator()
        
        # Remove bookmark
        remove_action = QAction("Remove Bookmark", self)
        remove_action.triggered.connect(lambda: self.bookmark_model.remove_bookmark(url))
        menu.addAction(remove_action)
        
        menu.exec(self.bookmark_list.mapToGlobal(position))

    def open_bookmark_in_current_tab(self, url):
        self.bookmark_item_clicked.emit(url)
        self.hide()

    def open_bookmark_in_new_tab(self, url):
        # Emit the URL and let the main window handle opening in new tab
        self.bookmark_item_clicked.emit(url)
        self.hide()

    def add_current_bookmark(self):
        # This will be connected from the main window to add current page
        parent = self.parent()
        if parent and hasattr(parent, 'add_current_page_to_bookmarks'):
            parent.add_current_page_to_bookmarks()

    def edit_bookmark_folder(self, url):
        bookmark = self.bookmark_model.get_bookmark_by_url(url)
        if bookmark:
            current_folder = bookmark.folder or ""
            folder, ok = QInputDialog.getText(
                self, 
                "Edit Bookmark Folder", 
                "Folder name:", 
                text=current_folder
            )
            if ok:
                # Update the bookmark with new folder
                self.bookmark_model.add_bookmark(url, bookmark.title, folder)
