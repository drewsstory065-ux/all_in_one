# YouTube Player Implementation

# Create YouTube player folder structure
mkdir -p app/youtube/{control_bar,styles,video_display}

# Main YouTube window
echo 'from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from .video_display import YouTubeVideoDisplay
from .control_bar import YouTubeControlBar
from .styles import YouTubeStyles


class YouTubeWindow(QWidget):
    """Main YouTube player window."""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.center_window()
    
    def setup_ui(self):
        """Initialize UI components."""
        self.setWindowTitle("YouTube Player")
        self.setMinimumSize(600, 400)
        self.resize(800, 600)
        self.setStyleSheet(YouTubeStyles.WINDOW_STYLE)
        
        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create video display
        self.video_display = YouTubeVideoDisplay()
        main_layout.addWidget(self.video_display)
        
        # Create control bar
        self.control_bar = YouTubeControlBar()
        main_layout.addWidget(self.control_bar)
        
        self.setLayout(main_layout)
    
    def center_window(self):
        """Center the window on screen."""
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.setGeometry(x, y, self.width(), self.height())
' > app/youtube/youtube_window.py

# YouTube video display
echo 'from PyQt6.QtWidgets import QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

from .styles import YouTubeStyles


class YouTubeVideoDisplay(QWebEngineView):
    """Display for YouTube videos using web engine."""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the display."""
        self.setStyleSheet(YouTubeStyles.VIDEO_DISPLAY_STYLE)
    
    def load_video(self, video_id):
        """Load YouTube video by ID."""
        url = f"https://www.youtube.com/embed/{video_id}?autoplay=1"
        self.load(QUrl(url))
' > app/youtube/video_display.py

# YouTube control bar
echo 'from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit
from PyQt6.QtCore import pyqtSignal

from .styles import YouTubeStyles


class YouTubeControlBar(QWidget):
    """Control bar for YouTube player."""
    
    video_requested = pyqtSignal(str)  # Emits video ID
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Initialize UI components."""
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube URL or Video ID")
        self.url_input.setStyleSheet(YouTubeStyles.INPUT_STYLE)
        
        self.load_btn = QPushButton("Load")
        self.load_btn.setStyleSheet(YouTubeStyles.BUTTON_STYLE)
        
        layout.addWidget(self.url_input)
        layout.addWidget(self.load_btn)
        
        self.setLayout(layout)
        self.setStyleSheet(YouTubeStyles.CONTROL_BAR_STYLE)
    
    def connect_signals(self):
        """Connect button signals."""
        self.load_btn.clicked.connect(self.on_load_clicked)
        self.url_input.returnPressed.connect(self.on_load_clicked)
    
    def on_load_clicked(self):
        """Handle load button click."""
        text = self.url_input.text()
        video_id = self.extract_video_id(text)
        if video_id:
            self.video_requested.emit(video_id)
    
    def extract_video_id(self, url_or_id):
        """Extract video ID from URL or return if already ID."""
        if "youtube.com" in url_or_id:
            start = url_or_id.find("v=")
            if start != -1:
                start += 2
                video_id = url_or_id[start:start+11]
                return video_id
        elif "youtu.be" in url_or_id:
            start = url_or_id.find(".be/")
            if start != -1:
                start += 4
                video_id = url_or_id[start:start+11]
                return video_id
        elif len(url_or_id) == 11:
            return url_or_id
        return None
' > app/youtube/control_bar.py

# YouTube styles
echo 'class YouTubeStyles:
    """CSS styles for YouTube player."""
    
    WINDOW_STYLE = """
        QWidget {
            background-color: #000;
        }
    """
    
    VIDEO_DISPLAY_STYLE = """
        QWebEngineView {
            background-color: #000;
            border: none;
        }
    """
    
    CONTROL_BAR_STYLE = """
        QWidget {
            background-color: #2d2d2d;
            border-top: 1px solid #444;
        }
    """
    
    INPUT_STYLE = """
        QLineEdit {
            padding: 5px;
            border: 1px solid #555;
            border-radius: 3px;
            background-color: #fff;
            color: #000;
        }
    """
    
    BUTTON_STYLE = """
        QPushButton {
            background-color: #cc181e;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #ff0000;
        }
    """
' > app/youtube/styles.py

# Update main.py to include YouTube player
sed -i '/from app.main.main_window import MainWindow/a from app.youtube.youtube_window import YouTubeWindow' main.py
sed -i '/window = MainWindow()/a         self.youtube_window = YouTubeWindow()' main.py
sed -i '/video_btn = QPushButton("Video Player")/a         youtube_btn = QPushButton("YouTube Player")\n        youtube_btn.clicked.connect(self.open_youtube_player)\n        layout.addWidget(youtube_btn)' app/main/main_window.py
sed -i '/def open_video_player(self):/a     def open_youtube_player(self):\n        from app.youtube.youtube_window import YouTubeWindow\n        self.youtube_window = YouTubeWindow()\n        self.youtube_window.show()' app/main/main_window.py