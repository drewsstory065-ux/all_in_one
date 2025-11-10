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
