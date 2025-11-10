from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QSlider
from PyQt6.QtCore import Qt, pyqtSignal

from .styles import VideoPlayerStyles


class ControlBar(QWidget):
    """Control bar component with playback controls and timeline."""
    
    # Signals for control actions
    toggle_playlist = pyqtSignal()
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
    previous_video = pyqtSignal()
    next_video = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.is_playing = False
        self.setup_ui()
    
    def update_navigation_buttons(self, current_index, item_count, loop_mode=False):
        """Update the enabled state of previous/next buttons based on playlist position."""
        # Previous button: disabled if at first item and not in loop mode
        self.previous_btn.setEnabled(loop_mode or current_index > 0)
        
        # Next button: disabled if at last item and not in loop mode
        self.next_btn.setEnabled(loop_mode or current_index < item_count - 1)
    
    def setup_ui(self):
        """Initialize the control bar UI."""
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)
        
        # Control buttons
        self.toggle_playlist_btn = self.create_button("☰", "Show Playlist")
        self.select_video_btn = self.create_button("📁", "Select Video")
        self.rewind_fast_btn = self.create_button("<<", "Rewind Fast")
        self.rewind_btn = self.create_button("<", "Rewind")
        self.previous_btn = self.create_button("◀◀", "Previous Video (B)")
        self.play_pause_btn = self.create_button(">", "Play")
        self.next_btn = self.create_button("▶▶", "Next Video (N)")
        self.forward_btn = self.create_button(">", "Forward")
        self.forward_fast_btn = self.create_button(">>", "Forward Fast")
        
        # Time labels
        self.current_time_label = QLabel("00:00")
        self.current_time_label.setStyleSheet(VideoPlayerStyles.TIME_LABEL_STYLE)
        self.current_time_label.setFixedWidth(40)
        
        # Timeline slider
        self.timeline_slider = QSlider(Qt.Orientation.Horizontal)
        self.timeline_slider.setStyleSheet(VideoPlayerStyles.TIMELINE_SLIDER_STYLE)
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
        layout.addWidget(self.toggle_playlist_btn)
        layout.addWidget(self.select_video_btn)
        layout.addWidget(self.rewind_fast_btn)
        layout.addWidget(self.rewind_btn)
        layout.addWidget(self.previous_btn)
        layout.addWidget(self.play_pause_btn)
        layout.addWidget(self.next_btn)
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
        self.toggle_playlist_btn.clicked.connect(self.toggle_playlist.emit)
        self.select_video_btn.clicked.connect(self.select_video.emit)
        self.rewind_fast_btn.clicked.connect(self.rewind_fast.emit)
        self.rewind_btn.clicked.connect(self.rewind.emit)
        self.previous_btn.clicked.connect(self.previous_video.emit)
        self.play_pause_btn.clicked.connect(self.toggle_play_pause)
        self.next_btn.clicked.connect(self.next_video.emit)
        self.forward_btn.clicked.connect(self.forward.emit)
        self.forward_fast_btn.clicked.connect(self.forward_fast.emit)
        self.volume_btn.clicked.connect(self.toggle_volume_display)
        self.volume_slider.valueChanged.connect(self.volume_changed.emit)
        self.fullscreen_btn.clicked.connect(self.toggle_fullscreen.emit)
        self.timeline_slider.sliderMoved.connect(self.seek.emit)
        self.timeline_slider.sliderReleased.connect(self.on_slider_released)
    
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
    
    def update_playlist_button(self, is_visible):
        """Update the playlist toggle button based on playlist visibility."""
        if is_visible:
            self.toggle_playlist_btn.setToolTip("Hide Playlist")
        else:
            self.toggle_playlist_btn.setToolTip("Show Playlist")
    
    def on_slider_released(self):
        """Handle slider release for timeline seeking."""
        position = self.timeline_slider.value()
        self.seek.emit(position)
    
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
