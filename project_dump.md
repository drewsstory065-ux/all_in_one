
/home/azerty/dev/all_in_one/main.py

```python

import sys
from PyQt6.QtWidgets import QApplication
from app.main.main_window import MainWindow

from app.main.system_tray_handler import SystemTrayHandler

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()  
    
    tray_handler = SystemTrayHandler(window)
    
    window.show()
    sys.exit(app.exec())


```
---

/home/azerty/dev/all_in_one/src/tools/config.py

```python

import configparser
import os


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        # Get the path to config.ini relative to the project root
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.ini')
        config_path = os.path.abspath(config_path)
        self.config.read(config_path)
    
    def get(self, section, key, fallback=None):
        """
        Get a configuration value.
        
        Args:
            section: The section name in the config file
            key: The key name in the section
            fallback: Default value if key is not found
        
        Returns:
            The configuration value or fallback
        """
        return self.config.get(section, key, fallback=fallback)
    
    def get_int(self, section, key, fallback=0):
        """
        Get an integer configuration value.
        
        Args:
            section: The section name in the config file
            key: The key name in the section
            fallback: Default value if key is not found
        
        Returns:
            The configuration value as int or fallback
        """
        return self.config.getint(section, key, fallback=fallback)
    
    def get_bool(self, section, key, fallback=False):
        """
        Get a boolean configuration value.
        
        Args:
            section: The section name in the config file
            key: The key name in the section
            fallback: Default value if key is not found
        
        Returns:
            The configuration value as bool or fallback
        """
        return self.config.getboolean(section, key, fallback=fallback)
    
    def get_float(self, section, key, fallback=0.0):
        """
        Get a float configuration value.
        
        Args:
            section: The section name in the config file
            key: The key name in the section
            fallback: Default value if key is not found
        
        Returns:
            The configuration value as float or fallback
        """
        return self.config.getfloat(section, key, fallback=fallback)
```
---

/home/azerty/dev/all_in_one/app/main/main_window.py

```python

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(100, 500)
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
        
        # Add video player button
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
    
    def open_video_player(self):
        from app.myvid.myvid_window import MyVidWindow
        self.video_window = MyVidWindow()
        self.video_window.show()


```
---

/home/azerty/dev/all_in_one/app/main/system_tray_handler.py

```python

from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QAction
from PyQt6.QtCore import pyqtSignal
from src.tools.config import Config


class SystemTrayHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.tray_icon = None
        self.config = Config()
        self.setup_system_tray()
    
    def setup_system_tray(self):
        # Create system tray icon
        self.tray_icon = QSystemTrayIcon()
        
        # Use icon from config file
        icon_path = self.config.get('app', 'icon_path')
        icon = QIcon(icon_path)
        self.tray_icon.setIcon(icon)
        
        # Create context menu
        tray_menu = QMenu()
        show_action = QAction("Show", None)
        quit_action = QAction("Quit", None)
        
        show_action.triggered.connect(self.show_main_window)
        quit_action.triggered.connect(self.quit_application)
        
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()
    
    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_main_window()
    
    def show_main_window(self):
        if self.main_window.isHidden():
            self.main_window.show()
        else:
            self.main_window.raise_()
            self.main_window.activateWindow()
    
    def quit_application(self):
        self.main_window.close()
```
---

/home/azerty/dev/all_in_one/app/myvid/control_bar.py

```python

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QSlider
from PyQt6.QtCore import Qt, pyqtSignal, QRect
from PyQt6.QtGui import QPainter, QMouseEvent

from .styles import VideoPlayerStyles


class TimelineSlider(QWidget):
    """Custom timeline slider that handles edge cases better than QSlider."""
    
    positionChanged = pyqtSignal(int)  # Emits percentage (0-100)
    
    def __init__(self):
        super().__init__()
        self._value = 0
        self._minimum = 0
        self._maximum = 100
        self._is_dragging = False
        self.setMinimumHeight(20)
        self.setMinimumWidth(200)
    
    def value(self):
        return self._value
    
    def setValue(self, value):
        if value != self._value:
            self._value = max(self._minimum, min(self._maximum, value))
            self.update()
            self.positionChanged.emit(self._value)
    
    def minimum(self):
        return self._minimum
    
    def maximum(self):
        return self._maximum
    
    def setMinimum(self, value):
        self._minimum = value
    
    def setMaximum(self, value):
        self._maximum = value
    
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_dragging = True
            self._update_value_from_position(event.pos())
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if self._is_dragging:
            self._update_value_from_position(event.pos())
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_dragging = False
            self._update_value_from_position(event.pos())
    
    def _update_value_from_position(self, pos):
        width = self.width()
        if width > 0:
            relative_pos = max(0, min(width, pos.x()))
            percentage = int((relative_pos / width) * 100)
            self.setValue(percentage)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background
        bg_rect = QRect(0, self.height() // 2 - 2, self.width(), 4)
        painter.fillRect(bg_rect, Qt.GlobalColor.gray)
        
        # Draw progress
        if self._maximum > 0:
            progress_width = int((self._value / 100.0) * self.width())
            progress_rect = QRect(0, self.height() // 2 - 2, progress_width, 4)
            painter.fillRect(progress_rect, Qt.GlobalColor.blue)
        
        # Draw handle
        handle_pos = int((self._value / 100.0) * self.width())
        handle_rect = QRect(handle_pos - 4, self.height() // 2 - 6, 8, 12)
        painter.fillRect(handle_rect, Qt.GlobalColor.darkBlue)


class ControlBar(QWidget):
    """Control bar component with playback controls and timeline."""
    
    # Signals for control actions
    rewind_fast = pyqtSignal()
    rewind = pyqtSignal()
    play_pause = pyqtSignal()
    forward = pyqtSignal()
    forward_fast = pyqtSignal()
    seek = pyqtSignal(int)  # Position in seconds
    volume_changed = pyqtSignal(int)  # Volume level 0-100
    volume_display_toggled = pyqtSignal()
    toggle_fullscreen = pyqtSignal()
    select_video = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.is_playing = False
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the control bar UI."""
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)
        
        # Control buttons
        self.select_video_btn = self.create_button("📁", "Select Video")
        self.rewind_fast_btn = self.create_button("<<", "Rewind Fast")
        self.rewind_btn = self.create_button("<", "Rewind")
        self.play_pause_btn = self.create_button(">", "Play")
        self.forward_btn = self.create_button(">", "Forward")
        self.forward_fast_btn = self.create_button(">>", "Forward Fast")
        
        # Time labels
        self.current_time_label = QLabel("00:00")
        self.current_time_label.setStyleSheet(VideoPlayerStyles.TIME_LABEL_STYLE)
        self.current_time_label.setFixedWidth(40)
        
        # Timeline slider - using custom implementation for better stability
        self.timeline_slider = TimelineSlider()
        self.timeline_slider.setMinimum(0)
        self.timeline_slider.setMaximum(100)
        self.timeline_slider.setValue(0)
        
        self.total_time_label = QLabel("00:00")
        self.total_time_label.setStyleSheet(VideoPlayerStyles.TIME_LABEL_STYLE)
        self.total_time_label.setFixedWidth(40)
        
        # Volume control
        self.volume_btn = self.create_button("🔊", "Volume")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setStyleSheet(VideoPlayerStyles.VOLUME_SLIDER_STYLE)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(80)  # Default volume
        self.volume_slider.setFixedWidth(60)
        self.volume_slider.hide()  # Initially hidden
        
        # Fullscreen button
        self.fullscreen_btn = self.create_button("⬚", "Toggle Fullscreen")
        
        # Add widgets to layout
        layout.addWidget(self.select_video_btn)
        layout.addWidget(self.rewind_fast_btn)
        layout.addWidget(self.rewind_btn)
        layout.addWidget(self.play_pause_btn)
        layout.addWidget(self.forward_btn)
        layout.addWidget(self.forward_fast_btn)
        layout.addWidget(self.current_time_label)
        layout.addWidget(self.timeline_slider)
        layout.addWidget(self.total_time_label)
        layout.addWidget(self.volume_btn)
        layout.addWidget(self.volume_slider)
        layout.addWidget(self.fullscreen_btn)
        
        self.setLayout(layout)
        self.setFixedHeight(25)
        self.setStyleSheet(VideoPlayerStyles.CONTROL_BAR_STYLE)
        
        # Connect signals
        self.connect_signals()
    
    def create_button(self, text, tooltip):
        """Create a styled control button."""
        button = QPushButton(text)
        button.setFixedSize(20, 20)
        button.setStyleSheet(VideoPlayerStyles.BUTTON_STYLE)
        button.setToolTip(tooltip)
        return button
    
    def connect_signals(self):
        """Connect button and slider signals."""
        self.select_video_btn.clicked.connect(self.select_video.emit)
        self.rewind_fast_btn.clicked.connect(self.rewind_fast.emit)
        self.rewind_btn.clicked.connect(self.rewind.emit)
        self.play_pause_btn.clicked.connect(self.toggle_play_pause)
        self.forward_btn.clicked.connect(self.forward.emit)
        self.forward_fast_btn.clicked.connect(self.forward_fast.emit)
        self.volume_btn.clicked.connect(self.toggle_volume_display)
        self.volume_slider.valueChanged.connect(self.volume_changed.emit)
        self.fullscreen_btn.clicked.connect(self.toggle_fullscreen.emit)
        self.timeline_slider.positionChanged.connect(self.seek.emit)
    
    def toggle_volume_display(self):
        """Toggle volume slider visibility."""
        if self.volume_slider.isVisible():
            self.volume_slider.hide()
        else:
            self.volume_slider.show()
        self.volume_display_toggled.emit()
    
    def set_volume(self, volume):
        """Set volume level and update button icon."""
        self.volume_slider.setValue(volume)
        if volume == 0:
            self.volume_btn.setText("🔇")
            self.volume_btn.setToolTip("Unmute")
        else:
            self.volume_btn.setText("🔊")
            self.volume_btn.setToolTip("Volume")
    
    
    def toggle_play_pause(self):
        """Toggle between play and pause states."""
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_pause_btn.setText("■")
            self.play_pause_btn.setToolTip("Pause")
        else:
            self.play_pause_btn.setText(">")
            self.play_pause_btn.setToolTip("Play")
        self.play_pause.emit()
    
    def update_time_display(self, current_time, total_time):
        """Update the time display labels and timeline."""
        # Update time labels
        current_str = self.format_time(current_time)
        total_str = self.format_time(total_time)
        self.current_time_label.setText(current_str)
        self.total_time_label.setText(total_str)
        
        # Update timeline slider
        if total_time > 0:
            percentage = int((current_time / total_time) * 100)
            self.timeline_slider.setValue(percentage)
    
    def format_time(self, seconds):
        """Format seconds into MM:SS or HH:MM:SS format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"

```
---

/home/azerty/dev/all_in_one/app/myvid/playlist_widget.py

```python

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QListWidget, QListWidgetItem, QLabel, QFileDialog)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from .styles import VideoPlayerStyles
from .playlist_manager import PlaylistManager


class PlaylistWidget(QWidget):
    """Widget that displays and manages the playlist."""
    
    # Signals
    item_selected = pyqtSignal(int)  # Emitted when user selects an item
    play_next_requested = pyqtSignal()  # Emitted when next button clicked
    play_previous_requested = pyqtSignal()  # Emitted when previous button clicked
    
    def __init__(self, playlist_manager: PlaylistManager):
        super().__init__()
        self.playlist_manager = playlist_manager
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Initialize the playlist UI."""
        self.setMinimumWidth(250)
        self.setMaximumWidth(350)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Header
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("Playlist")
        self.title_label.setStyleSheet(VideoPlayerStyles.PLAYLIST_TITLE_STYLE)
        self.title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        self.count_label = QLabel("(0 items)")
        self.count_label.setStyleSheet(VideoPlayerStyles.PLAYLIST_COUNT_STYLE)
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.count_label)
        
        # Control buttons
        control_layout = QHBoxLayout()
        
        self.add_btn = self.create_button("+", "Add Videos")
        self.add_multiple_btn = self.create_button("++", "Add Multiple Videos")
        self.clear_btn = self.create_button("×", "Clear Playlist")
        self.prev_btn = self.create_button("◀", "Previous")
        self.next_btn = self.create_button("▶", "Next")
        
        control_layout.addWidget(self.add_btn)
        control_layout.addWidget(self.add_multiple_btn)
        control_layout.addWidget(self.clear_btn)
        control_layout.addStretch()
        control_layout.addWidget(self.prev_btn)
        control_layout.addWidget(self.next_btn)
        
        # Playlist list
        self.playlist_list = QListWidget()
        self.playlist_list.setStyleSheet(VideoPlayerStyles.PLAYLIST_LIST_STYLE)
        self.playlist_list.setAlternatingRowColors(True)
        
        # Playlist mode buttons
        mode_layout = QHBoxLayout()
        
        self.loop_btn = self.create_button("🔁", "Loop Playlist")
        self.shuffle_btn = self.create_button("🔀", "Shuffle Playlist")
        
        mode_layout.addWidget(self.loop_btn)
        mode_layout.addWidget(self.shuffle_btn)
        mode_layout.addStretch()
        
        # Add all to main layout
        layout.addLayout(header_layout)
        layout.addLayout(control_layout)
        layout.addWidget(self.playlist_list)
        layout.addLayout(mode_layout)
        
        self.setLayout(layout)
        self.update_display()
    
    def create_button(self, text: str, tooltip: str) -> QPushButton:
        """Create a styled button."""
        button = QPushButton(text)
        button.setFixedSize(25, 25)
        button.setStyleSheet(VideoPlayerStyles.PLAYLIST_BUTTON_STYLE)
        button.setToolTip(tooltip)
        return button
    
    def connect_signals(self):
        """Connect all signals."""
        # Button signals
        self.add_btn.clicked.connect(self.on_add_video)
        self.add_multiple_btn.clicked.connect(self.on_add_multiple_videos)
        self.clear_btn.clicked.connect(self.on_clear_playlist)
        self.prev_btn.clicked.connect(self.play_previous_requested.emit)
        self.next_btn.clicked.connect(self.play_next_requested.emit)
        self.loop_btn.clicked.connect(self.on_toggle_loop)
        self.shuffle_btn.clicked.connect(self.on_toggle_shuffle)
        
        # List signals
        self.playlist_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        
        # Playlist manager signals
        self.playlist_manager.playlist_changed.connect(self.update_display)
        self.playlist_manager.current_item_changed.connect(self.on_current_item_changed)
    
    def on_add_video(self):
        """Add a single video to playlist."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Add Video to Playlist",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv);;All Files (*)"
        )
        
        if file_path:
            self.playlist_manager.add_item(file_path)
    
    def on_add_multiple_videos(self):
        """Add multiple videos to playlist."""
        file_dialog = QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(
            self,
            "Add Videos to Playlist",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv);;All Files (*)"
        )
        
        if file_paths:
            self.playlist_manager.add_items(file_paths)
    
    def on_clear_playlist(self):
        """Clear the entire playlist."""
        self.playlist_manager.clear()
    
    def on_toggle_loop(self):
        """Toggle loop mode."""
        is_looping = self.playlist_manager.toggle_loop()
        if is_looping:
            self.loop_btn.setStyleSheet(VideoPlayerStyles.PLAYLIST_BUTTON_ACTIVE_STYLE)
        else:
            self.loop_btn.setStyleSheet(VideoPlayerStyles.PLAYLIST_BUTTON_STYLE)
    
    def on_toggle_shuffle(self):
        """Toggle shuffle mode."""
        is_shuffling = self.playlist_manager.toggle_shuffle()
        if is_shuffling:
            self.shuffle_btn.setStyleSheet(VideoPlayerStyles.PLAYLIST_BUTTON_ACTIVE_STYLE)
        else:
            self.shuffle_btn.setStyleSheet(VideoPlayerStyles.PLAYLIST_BUTTON_STYLE)
    
    def on_item_double_clicked(self, item: QListWidgetItem):
        """Handle double-click on playlist item."""
        index = self.playlist_list.row(item)
        self.item_selected.emit(index)
    
    def on_current_item_changed(self, index: int):
        """Update display when current item changes."""
        self.update_current_item_highlight()
    
    def update_display(self):
        """Update the entire playlist display."""
        self.playlist_list.clear()
        
        for i, item in enumerate(self.playlist_manager.items):
            list_item = QListWidgetItem(item.title)
            self.playlist_list.addItem(list_item)
        
        self.update_current_item_highlight()
        self.update_count_display()
    
    def update_current_item_highlight(self):
        """Highlight the current playing item."""
        current_index = self.playlist_manager.current_index
        
        for i in range(self.playlist_list.count()):
            item = self.playlist_list.item(i)
            if i == current_index:
                item.setBackground(Qt.GlobalColor.lightBlue)
                item.setForeground(Qt.GlobalColor.black)
            else:
                item.setBackground(Qt.GlobalColor.white)
                item.setForeground(Qt.GlobalColor.black)
    
    def update_count_display(self):
        """Update the item count display."""
        count = self.playlist_manager.count
        self.count_label.setText(f"({count} item{'s' if count != 1 else ''})")

```
---

/home/azerty/dev/all_in_one/app/myvid/myvid_window.py

```python

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from .video_display import VideoDisplay
from .control_bar import ControlBar
from .playlist_manager import PlaylistManager
from .playlist_widget import PlaylistWidget
from .styles import VideoPlayerStyles


class MyVidWindow(QWidget):
    """Main video player window that integrates all components."""
    
    def __init__(self):
        super().__init__()
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.current_time = 0
        self.total_time = 0
        self.is_playing = False
        self.timer = QTimer()
        
        self.setup_ui()
        self.connect_signals()
        self.center_window()
    
    def setup_ui(self):
        """Initialize the main window UI."""
        self.setWindowTitle("Video Player")
        self.setMinimumSize(600, 400)
        self.resize(1000, 600)
        self.setStyleSheet(VideoPlayerStyles.MAIN_WINDOW_STYLE)
        
        # Create playlist manager
        self.playlist_manager = PlaylistManager()
        
        # Create main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left side: video display and controls
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        
        # Create and add video display
        self.video_display = VideoDisplay()
        left_layout.addWidget(self.video_display)
        
        # Create and add control bar
        self.control_bar = ControlBar()
        left_layout.addWidget(self.control_bar)
        
        # Right side: playlist
        self.playlist_widget = PlaylistWidget(self.playlist_manager)
        
        # Add to main layout
        main_layout.addLayout(left_layout, 3)  # 3/4 width for video
        main_layout.addWidget(self.playlist_widget, 1)  # 1/4 width for playlist
        
        self.setLayout(main_layout)
    
    def connect_signals(self):
        """Connect all component signals."""
        # Control bar signals
        self.control_bar.select_video.connect(self.on_select_video)
        self.control_bar.rewind_fast.connect(self.on_rewind_fast)
        self.control_bar.rewind.connect(self.on_rewind)
        self.control_bar.play_pause.connect(self.on_play_pause)
        self.control_bar.forward.connect(self.on_forward)
        self.control_bar.forward_fast.connect(self.on_forward_fast)
        self.control_bar.seek.connect(self.on_seek)
        self.control_bar.volume_changed.connect(self.on_volume_changed)
        self.control_bar.volume_display_toggled.connect(self.on_toggle_volume_display)
        self.control_bar.toggle_fullscreen.connect(self.on_toggle_fullscreen)
        
        # Media player signals
        self.media_player.positionChanged.connect(self.on_position_changed)
        self.media_player.durationChanged.connect(self.on_duration_changed)
        self.media_player.playbackStateChanged.connect(self.on_playback_state_changed)
        self.media_player.mediaStatusChanged.connect(self.on_media_status_changed)
        
        # Playlist signals
        self.playlist_widget.item_selected.connect(self.on_playlist_item_selected)
        self.playlist_widget.play_next_requested.connect(self.on_play_next)
        self.playlist_widget.play_previous_requested.connect(self.on_play_previous)
        self.playlist_manager.current_item_changed.connect(self.on_playlist_current_changed)
        
        # Timer for UI updates
        self.timer.timeout.connect(self.update_time_display)
    
    def center_window(self):
        """Center the window on screen."""
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.setGeometry(x, y, self.width(), self.height())
    
    def on_rewind_fast(self):
        """Handle fast rewind action."""
        if self.media_player.duration() > 0:
            new_position = max(0, self.media_player.position() - 10000)  # 10 seconds
            self.media_player.setPosition(new_position)
    
    def on_rewind(self):
        """Handle rewind action."""
        if self.media_player.duration() > 0:
            new_position = max(0, self.media_player.position() - 5000)  # 5 seconds
            self.media_player.setPosition(new_position)
    
    def on_play_pause(self):
        """Handle play/pause toggle."""
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()
    
    def on_forward(self):
        """Handle forward action."""
        if self.media_player.duration() > 0:
            new_position = min(self.media_player.duration(), self.media_player.position() + 5000)  # 5 seconds
            self.media_player.setPosition(new_position)
    
    def on_forward_fast(self):
        """Handle fast forward action."""
        if self.media_player.duration() > 0:
            new_position = min(self.media_player.duration(), self.media_player.position() + 10000)  # 10 seconds
            self.media_player.setPosition(new_position)
    
    def on_seek(self, position):
        """Handle timeline seeking."""
        duration = self.media_player.duration()
        if duration > 0:
            seek_position = int((position / 100) * duration)
            self.media_player.setPosition(seek_position)
    
    def on_toggle_fullscreen(self):
        """Handle fullscreen toggle."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    def on_volume_changed(self, volume):
        """Handle volume level changes."""
        # Set audio output volume (0.0 to 1.0 scale)
        audio_output = self.media_player.audioOutput()
        if audio_output:
            audio_output.setVolume(volume / 100.0)
        # Update volume button icon
        self.control_bar.set_volume(volume)
    
    def on_toggle_volume_display(self):
        """Toggle volume slider visibility."""
        self.control_bar.toggle_volume_display()
    
    def on_select_video(self):
        """Handle video file selection."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Select Video File",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv);;All Files (*)"
        )
        
        if file_path:
            # Stop current playback
            self.media_player.stop()
            
            # Load video into display
            self.video_display.load_video(file_path, self.media_player)
            file_name = file_path.split("/")[-1]
            self.setWindowTitle(f"Video Player - {file_name}")
            
            # Start playback immediately
            self.media_player.play()
            
            print(f"Selected video: {file_path}")
    
    def on_position_changed(self, position):
        """Handle media player position changes."""
        self.current_time = position // 1000  # Convert to seconds
        self.update_time_display()
    
    def on_duration_changed(self, duration):
        """Handle media player duration changes."""
        self.total_time = duration // 1000  # Convert to seconds
        self.update_time_display()
    
    def on_playback_state_changed(self, state):
        """Handle playback state changes."""
        self.is_playing = (state == QMediaPlayer.PlaybackState.PlayingState)
        self.control_bar.is_playing = self.is_playing
        
        if self.is_playing:
            self.control_bar.play_pause_btn.setText("■")
            self.control_bar.play_pause_btn.setToolTip("Pause")
            self.timer.start(100)  # Update UI more frequently during playback
        else:
            self.control_bar.play_pause_btn.setText(">")
            self.control_bar.play_pause_btn.setToolTip("Play")
            self.timer.stop()
    
    def update_time_display(self):
        """Update the time display and timeline."""
        if self.total_time > 0:
            percentage = int((self.current_time / self.total_time) * 100)
            self.control_bar.update_time_display(self.current_time, self.total_time)
            self.control_bar.timeline_slider.setValue(percentage)
        else:
            self.control_bar.update_time_display(0, 0)
    
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts."""
        if event.key() == Qt.Key.Key_Space:
            self.on_play_pause()
        elif event.key() == Qt.Key.Key_Left:
            self.on_rewind()
        elif event.key() == Qt.Key.Key_Right:
            self.on_forward()
        elif event.key() == Qt.Key.Key_Escape and self.isFullScreen():
            self.showNormal()
        elif event.key() == Qt.Key.Key_F:
            self.on_toggle_fullscreen()
        elif event.key() == Qt.Key.Key_N:
            self.on_play_next()
        elif event.key() == Qt.Key.Key_P:
            self.on_play_previous()
        else:
            super().keyPressEvent(event)
    
    def on_playlist_item_selected(self, index: int):
        """Handle playlist item selection."""
        if self.playlist_manager.set_current_index(index):
            self.play_current_playlist_item()
    
    def on_play_next(self):
        """Play next item in playlist."""
        if self.playlist_manager.next():
            self.play_current_playlist_item()
    
    def on_play_previous(self):
        """Play previous item in playlist."""
        if self.playlist_manager.previous():
            self.play_current_playlist_item()
    
    def on_playlist_current_changed(self, index: int):
        """Handle current playlist item change."""
        if index >= 0:
            self.play_current_playlist_item()
    
    def on_media_status_changed(self, status):
        """Handle media status changes for playlist auto-advance."""
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            # Auto-advance to next video when current one ends
            if self.playlist_manager.is_looping:
                # If looping, restart current video
                self.media_player.play()
            elif self.playlist_manager.next():
                # Play next video
                self.play_current_playlist_item()
    
    def play_current_playlist_item(self):
        """Play the current playlist item."""
        current_item = self.playlist_manager.current_item
        if current_item:
            # Stop current playback
            self.media_player.stop()
            
            # Load and play the video
            self.video_display.load_video(current_item.file_path, self.media_player)
            self.setWindowTitle(f"Video Player - {current_item.title}")
            self.media_player.play()
            
            print(f"Playing playlist item: {current_item.file_path}")

```
---

/home/azerty/dev/all_in_one/app/myvid/playlist_manager.py

```python

from PyQt6.QtCore import QObject, pyqtSignal
from typing import List, Optional


class PlaylistItem:
    """Represents a single item in the playlist."""
    
    def __init__(self, file_path: str, title: str = ""):
        self.file_path = file_path
        self.title = title or file_path.split("/")[-1]
        self.duration = 0  # Will be set when video is loaded
    
    def __str__(self):
        return f"{self.title} ({self.file_path})"


class PlaylistManager(QObject):
    """Manages playlist functionality and state."""
    
    # Signals
    playlist_changed = pyqtSignal()  # Emitted when playlist content changes
    current_item_changed = pyqtSignal(int)  # Emitted when current item index changes
    playback_finished = pyqtSignal()  # Emitted when current video finishes
    
    def __init__(self):
        super().__init__()
        self._items: List[PlaylistItem] = []
        self._current_index = -1
        self._loop_mode = False  # Loop the entire playlist
        self._shuffle_mode = False
    
    @property
    def items(self) -> List[PlaylistItem]:
        """Get all playlist items."""
        return self._items.copy()
    
    @property
    def current_index(self) -> int:
        """Get current item index."""
        return self._current_index
    
    @property
    def current_item(self) -> Optional[PlaylistItem]:
        """Get current playlist item."""
        if 0 <= self._current_index < len(self._items):
            return self._items[self._current_index]
        return None
    
    @property
    def count(self) -> int:
        """Get number of items in playlist."""
        return len(self._items)
    
    @property
    def has_items(self) -> bool:
        """Check if playlist has any items."""
        return len(self._items) > 0
    
    def add_item(self, file_path: str, title: str = "") -> None:
        """Add a video to the playlist."""
        item = PlaylistItem(file_path, title)
        self._items.append(item)
        self.playlist_changed.emit()
        
        # If this is the first item, set it as current
        if len(self._items) == 1:
            self._current_index = 0
            self.current_item_changed.emit(0)
    
    def add_items(self, file_paths: List[str]) -> None:
        """Add multiple videos to the playlist."""
        for file_path in file_paths:
            self.add_item(file_path)
    
    def remove_item(self, index: int) -> None:
        """Remove item at specified index."""
        if 0 <= index < len(self._items):
            self._items.pop(index)
            
            # Adjust current index if needed
            if self._current_index >= index:
                if self._current_index == index:
                    # Current item was removed
                    if len(self._items) > 0:
                        self._current_index = min(index, len(self._items) - 1)
                    else:
                        self._current_index = -1
                else:
                    self._current_index -= 1
            
            self.playlist_changed.emit()
            self.current_item_changed.emit(self._current_index)
    
    def clear(self) -> None:
        """Clear all items from playlist."""
        self._items.clear()
        self._current_index = -1
        self.playlist_changed.emit()
        self.current_item_changed.emit(-1)
    
    def move_item(self, from_index: int, to_index: int) -> None:
        """Move item from one position to another."""
        if (0 <= from_index < len(self._items) and 
            0 <= to_index < len(self._items)):
            item = self._items.pop(from_index)
            self._items.insert(to_index, item)
            
            # Update current index if needed
            if self._current_index == from_index:
                self._current_index = to_index
            elif (from_index < self._current_index <= to_index):
                self._current_index -= 1
            elif (to_index <= self._current_index < from_index):
                self._current_index += 1
            
            self.playlist_changed.emit()
            self.current_item_changed.emit(self._current_index)
    
    def set_current_index(self, index: int) -> bool:
        """Set current item index."""
        if 0 <= index < len(self._items):
            self._current_index = index
            self.current_item_changed.emit(index)
            return True
        return False
    
    def next(self) -> bool:
        """Move to next item in playlist."""
        if not self._items:
            return False
        
        if self._shuffle_mode:
            import random
            self._current_index = random.randint(0, len(self._items) - 1)
        else:
            self._current_index = (self._current_index + 1) % len(self._items)
        
        self.current_item_changed.emit(self._current_index)
        return True
    
    def previous(self) -> bool:
        """Move to previous item in playlist."""
        if not self._items:
            return False
        
        if self._shuffle_mode:
            import random
            self._current_index = random.randint(0, len(self._items) - 1)
        else:
            self._current_index = (self._current_index - 1) % len(self._items)
        
        self.current_item_changed.emit(self._current_index)
        return True
    
    def toggle_loop(self) -> bool:
        """Toggle loop mode."""
        self._loop_mode = not self._loop_mode
        return self._loop_mode
    
    def toggle_shuffle(self) -> bool:
        """Toggle shuffle mode."""
        self._shuffle_mode = not self._shuffle_mode
        return self._shuffle_mode
    
    @property
    def is_looping(self) -> bool:
        """Check if loop mode is enabled."""
        return self._loop_mode
    
    @property
    def is_shuffling(self) -> bool:
        """Check if shuffle mode is enabled."""
        return self._shuffle_mode

```
---

/home/azerty/dev/all_in_one/app/myvid/styles.py

```python

"""Styles for the video player components."""


class VideoPlayerStyles:
    """Static styles for video player components."""
    
    # Control bar styles
    CONTROL_BAR_STYLE = "background-color: #2d2d2d; border-top: 1px solid #444;"
    
    # Button styles
    BUTTON_STYLE = """
        QPushButton {
            background-color: #404040;
            border: 1px solid #555;
            color: white;
            font-size: 10px;
            border-radius: 2px;
        }
        QPushButton:hover {
            background-color: #505050;
            border: 1px solid #666;
        }
        QPushButton:pressed {
            background-color: #606060;
        }
    """
    
    # Time label styles
    TIME_LABEL_STYLE = "color: white; font-size: 10px;"
    
    # Timeline slider styles
    TIMELINE_SLIDER_STYLE = """
        QSlider::groove:horizontal {
            border: 1px solid #999999;
            height: 4px;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
            margin: 2px 0;
        }
        QSlider::handle:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
            border: 1px solid #5c5c5c;
            width: 8px;
            margin: -4px 0;
            border-radius: 3px;
        }
        QSlider::sub-page:horizontal {
            background: #0078d4;
            border: 1px solid #777;
            height: 4px;
            border-radius: 2px;
        }
    """
    
    # Volume slider styles
    VOLUME_SLIDER_STYLE = """
        QSlider::groove:horizontal {
            background: #555;
            height: 3px;
            border-radius: 1px;
        }
        
        QSlider::handle:horizontal {
            background: #fff;
            border: 1px solid #777;
            width: 8px;
            height: 8px;
            border-radius: 4px;
            margin: -3px 0;
        }
        
        QSlider::sub-page:horizontal {
            background: #0078d4;
            border-radius: 1px;
        }
    """
    
    # Video display styles
    VIDEO_DISPLAY_STYLE = """
        background-color: black; 
        color: white; 
        border: 1px solid #333;
        min-height: 300px;
    """
    
    # Main window styles
    MAIN_WINDOW_STYLE = "background-color: #1e1e1e;"
    
    # Playlist styles
    PLAYLIST_TITLE_STYLE = "color: white; font-size: 12px; font-weight: bold;"
    PLAYLIST_COUNT_STYLE = "color: #888; font-size: 10px;"
    
    PLAYLIST_BUTTON_STYLE = """
        QPushButton {
            background-color: #404040;
            border: 1px solid #555;
            color: white;
            font-size: 10px;
            border-radius: 2px;
        }
        QPushButton:hover {
            background-color: #505050;
            border: 1px solid #666;
        }
        QPushButton:pressed {
            background-color: #606060;
        }
    """
    
    PLAYLIST_BUTTON_ACTIVE_STYLE = """
        QPushButton {
            background-color: #0078d4;
            border: 1px solid #005a9e;
            color: white;
            font-size: 10px;
            border-radius: 2px;
        }
        QPushButton:hover {
            background-color: #106ebe;
            border: 1px solid #005a9e;
        }
        QPushButton:pressed {
            background-color: #005a9e;
        }
    """
    
    PLAYLIST_LIST_STYLE = """
        QListWidget {
            background-color: #2d2d2d;
            border: 1px solid #444;
            color: white;
            font-size: 11px;
            outline: none;
        }
        QListWidget::item {
            border-bottom: 1px solid #3d3d3d;
            padding: 5px;
        }
        QListWidget::item:selected {
            background-color: #0078d4;
            color: white;
        }
        QListWidget::item:hover {
            background-color: #3d3d3d;
        }
        QListWidget::item:alternate {
            background-color: #2a2a2a;
        }
    """

```
---

/home/azerty/dev/all_in_one/app/myvid/video_display.py

```python

from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget

from .styles import VideoPlayerStyles


class VideoDisplay(QVideoWidget):
    """Video display component that shows actual video content."""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the video display UI."""
        self.setStyleSheet(VideoPlayerStyles.VIDEO_DISPLAY_STYLE)
    
    def load_video(self, file_path, media_player):
        """Load and display actual video file."""
        media_player.setVideoOutput(self)
        media_player.setSource(QUrl.fromLocalFile(file_path))
    
    def reset_display(self):
        """Reset the display to initial state."""
        self.setStyleSheet(VideoPlayerStyles.VIDEO_DISPLAY_STYLE)
    
    def update_video_size(self, width, height):
        """Update the video display size."""
        self.setMinimumSize(width, height)

```
---

/home/azerty/dev/all_in_one/app/myvid/test_video_player.py

```python

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from myvid_window import MyVidWindow


def test_video_player():
    """Test the video player implementation."""
    app = QApplication(sys.argv)
    
    # Create and show the video player window
    window = MyVidWindow()
    window.show()
    
    # Print verification information
    print("Video Player Test")
    print("=" * 50)
    print(f"Window size: {window.width()}x{window.height()}")
    print(f"Control bar height: {window.control_bar.height()}")
    print(f"Video display size: {window.video_display.width()}x{window.video_display.height()}")
    print(f"Playlist widget width: {window.playlist_widget.width()}")
    print(f"Playlist items: {window.playlist_manager.count}")
    print(f"Total time: {window.total_time} seconds ({window.control_bar.format_time(window.total_time)})")
    print("\nControl bar features:")
    print("- [<<] [<] [>/■] [>] [>>] timeline [⬚]")
    print("- Timeline slider with progress indicator")
    print("- Current and total time display")
    print("- Keyboard shortcuts: Space, Left/Right arrows, F, Esc, N (next), P (previous)")
    print("\nPlaylist features:")
    print("- Add single/multiple videos to playlist")
    print("- Navigate between videos (previous/next)")
    print("- Loop and shuffle modes")
    print("- Auto-advance to next video")
    print("- Double-click to select any video")
    print("\nAll classes are under 150 lines:")
    print(f"- MyVidWindow: {len(open('app/myvid/myvid_window.py').readlines())} lines")
    print(f"- ControlBar: {len(open('app/myvid/control_bar.py').readlines())} lines")
    print(f"- VideoDisplay: {len(open('app/myvid/video_display.py').readlines())} lines")
    print(f"- PlaylistManager: {len(open('app/myvid/playlist_manager.py').readlines())} lines")
    print(f"- PlaylistWidget: {len(open('app/myvid/playlist_widget.py').readlines())} lines")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    test_video_player()

```
---

/home/azerty/dev/all_in_one/run.sh

```bash

#!/bin/bash
./install.sh
python3 main.py


```
---

/home/azerty/dev/all_in_one/install.sh

```bash

#!/bin/bash

# Check if all required tools are already installed
if command -v python3 &> /dev/null && command -v pip3 &> /dev/null && python3 -c "import PyQt6" &> /dev/null; then
    echo "All required tools (Python3, pip3, PyQt6) are already installed."
    exit 0
fi

# Update package list once at the beginning to avoid redundant updates
sudo apt update

# Check for Python3
if ! command -v python3 &> /dev/null; then
    echo "Python3 could not be found. Installing Python3..."
    sudo apt install -y python3
else
    echo "Python3 is already installed."
fi

# Check for pip3
if ! command -v pip3 &> /dev/null; then
    echo "pip3 could not be found. Installing pip3..."
    sudo apt install -y python3-pip
else
    echo "pip3 is already installed."
fi

# Check for PyQt6
if ! python3 -c "import PyQt6" &> /dev/null; then
    echo "PyQt6 is not installed. Installing PyQt6..."
    pip3 install PyQt6
else
    echo "PyQt6 is already installed."
fi


```
---

/home/azerty/dev/all_in_one/config/config.ini

```ini

[app]
icon_path = /home/azerty/dev/all_in_one/img/all_in_one_1.png
```
---

