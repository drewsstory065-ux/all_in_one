from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                             QPushButton, QLabel, QListWidgetItem, QFileDialog,
                             QCheckBox, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from .styles import VideoPlayerStyles
from .playlist_model import PlaylistModel


class PlaylistWidget(QWidget):
    """UI component for displaying and managing the playlist."""
    
    # Signals
    item_selected = pyqtSignal(str)  # Emitted when a playlist item is selected
    playlist_visibility_changed = pyqtSignal(bool)  # Emitted when playlist visibility changes
    
    def __init__(self, playlist_model):
        super().__init__()
        self.playlist_model = playlist_model
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Initialize the playlist UI."""
        self.setMinimumWidth(300)
        self.setMaximumWidth(400)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Header with title and controls
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("Playlist")
        title_font = QFont()
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet(VideoPlayerStyles.TIME_LABEL_STYLE)
        
        self.add_video_btn = self.create_button("+", "Add Video")
        self.add_folder_btn = self.create_button("📁", "Add Folder")
        self.clear_btn = self.create_button("🗑️", "Clear Playlist")
        self.toggle_btn = self.create_button("◀", "Hide Playlist")
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.add_video_btn)
        header_layout.addWidget(self.add_folder_btn)
        header_layout.addWidget(self.clear_btn)
        header_layout.addWidget(self.toggle_btn)
        
        # Playlist list widget
        self.playlist_list = QListWidget()
        self.playlist_list.setStyleSheet(VideoPlayerStyles.PLAYLIST_STYLE)
        self.playlist_list.setAlternatingRowColors(True)
        
        # Playback mode controls
        mode_layout = QHBoxLayout()
        
        self.loop_checkbox = QCheckBox("Loop")
        self.loop_checkbox.setStyleSheet(VideoPlayerStyles.CHECKBOX_STYLE)
        
        self.repeat_checkbox = QCheckBox("Repeat")
        self.repeat_checkbox.setStyleSheet(VideoPlayerStyles.CHECKBOX_STYLE)
        
        mode_layout.addWidget(self.loop_checkbox)
        mode_layout.addWidget(self.repeat_checkbox)
        mode_layout.addStretch()
        
        # Status label
        self.status_label = QLabel("No videos in playlist")
        self.status_label.setStyleSheet(VideoPlayerStyles.TIME_LABEL_STYLE)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add all widgets to main layout
        layout.addLayout(header_layout)
        layout.addWidget(self.playlist_list)
        layout.addLayout(mode_layout)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        self.update_status()
    
    def create_button(self, text, tooltip):
        """Create a styled button."""
        button = QPushButton(text)
        button.setFixedSize(25, 25)
        button.setStyleSheet(VideoPlayerStyles.BUTTON_STYLE)
        button.setToolTip(tooltip)
        return button
    
    def connect_signals(self):
        """Connect all signals."""
        # Button signals
        self.add_video_btn.clicked.connect(self.on_add_video)
        self.add_folder_btn.clicked.connect(self.on_add_folder)
        self.clear_btn.clicked.connect(self.on_clear_playlist)
        self.toggle_btn.clicked.connect(self.on_toggle_playlist)
        
        # Playlist list signals
        self.playlist_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.playlist_list.customContextMenuRequested.connect(self.on_context_menu)
        
        # Playlist model signals
        self.playlist_model.playlist_changed.connect(self.update_playlist_display)
        self.playlist_model.current_item_changed.connect(self.update_current_item)
        
        # Mode checkbox signals
        self.loop_checkbox.stateChanged.connect(self.on_loop_mode_changed)
        self.repeat_checkbox.stateChanged.connect(self.on_repeat_mode_changed)
        
        # Enable context menu
        self.playlist_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    
    def on_add_video(self):
        """Handle adding video files to playlist."""
        file_dialog = QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(
            self,
            "Select Video Files",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv);;All Files (*)"
        )
        
        if file_paths:
            self.playlist_model.add_videos(file_paths)
    
    def on_add_folder(self):
        """Handle adding all video files from a folder."""
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Folder with Videos"
        )
        
        if folder_path:
            import os
            video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'}
            video_files = []
            
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in video_extensions):
                        video_files.append(os.path.join(root, file))
            
            if video_files:
                self.playlist_model.add_videos(video_files)
            else:
                QMessageBox.information(self, "No Videos Found", 
                                      "No video files found in the selected folder.")
    
    def on_clear_playlist(self):
        """Handle clearing the playlist."""
        if self.playlist_model.get_item_count() > 0:
            reply = QMessageBox.question(
                self,
                "Clear Playlist",
                "Are you sure you want to clear the entire playlist?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.playlist_model.clear_playlist()
    
    def on_toggle_playlist(self):
        """Toggle playlist visibility."""
        is_visible = not self.isVisible()
        self.setVisible(is_visible)
        self.playlist_visibility_changed.emit(is_visible)
        
        # Update toggle button text
        if is_visible:
            self.toggle_btn.setText("◀")
            self.toggle_btn.setToolTip("Hide Playlist")
        else:
            self.toggle_btn.setText("▶")
            self.toggle_btn.setToolTip("Show Playlist")
    
    def on_item_double_clicked(self, item):
        """Handle double-click on playlist item."""
        index = self.playlist_list.row(item)
        self.playlist_model.set_current_index(index)
        current_item = self.playlist_model.get_current_item()
        if current_item:
            self.item_selected.emit(current_item.file_path)
    
    def on_context_menu(self, position):
        """Handle right-click context menu."""
        # This will be implemented in the main window for consistency
        pass
    
    def on_loop_mode_changed(self, state):
        """Handle loop mode checkbox changes."""
        self.playlist_model.set_loop_mode(state == Qt.CheckState.Checked)
    
    def on_repeat_mode_changed(self, state):
        """Handle repeat mode checkbox changes."""
        self.playlist_model.set_repeat_mode(state == Qt.CheckState.Checked)
    
    def update_playlist_display(self):
        """Update the playlist list widget with current items."""
        self.playlist_list.clear()
        
        for i, item in enumerate(self.playlist_model.items):
            list_item = QListWidgetItem(str(item))
            self.playlist_list.addItem(list_item)
        
        self.update_current_item(self.playlist_model.current_index)
        self.update_status()
    
    def update_current_item(self, current_index):
        """Update the visual indication of the current playing item."""
        for i in range(self.playlist_list.count()):
            item = self.playlist_list.item(i)
            if i == current_index:
                item.setBackground(Qt.GlobalColor.darkBlue)
                item.setForeground(Qt.GlobalColor.white)
            else:
                item.setBackground(Qt.GlobalColor.transparent)
                item.setForeground(Qt.GlobalColor.black)
    
    def update_status(self):
        """Update the status label."""
        count = self.playlist_model.get_item_count()
        if count == 0:
            self.status_label.setText("No videos in playlist")
        elif count == 1:
            self.status_label.setText("1 video in playlist")
        else:
            self.status_label.setText(f"{count} videos in playlist")
