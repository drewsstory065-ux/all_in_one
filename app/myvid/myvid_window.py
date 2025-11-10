from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from .video_display import VideoDisplay
from .control_bar import ControlBar
from .playlist_model import PlaylistModel
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
        self.setMinimumSize(400, 300)
        self.resize(800, 500)
        self.setStyleSheet(VideoPlayerStyles.MAIN_WINDOW_STYLE)
        
        # Create main horizontal layout for video and playlist
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create vertical layout for video display and controls
        video_layout = QVBoxLayout()
        video_layout.setContentsMargins(0, 0, 0, 0)
        video_layout.setSpacing(0)
        
        # Create and add video display
        self.video_display = VideoDisplay()
        video_layout.addWidget(self.video_display)
        
        # Create and add control bar
        self.control_bar = ControlBar()
        video_layout.addWidget(self.control_bar)
        
        # Create playlist model and widget
        self.playlist_model = PlaylistModel()
        self.playlist_widget = PlaylistWidget(self.playlist_model)
        
        # Add video layout and playlist to main layout
        main_layout.addLayout(video_layout)
        main_layout.addWidget(self.playlist_widget)
        
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
        self.playlist_widget.playlist_visibility_changed.connect(self.on_playlist_visibility_changed)
        self.playlist_model.current_item_changed.connect(self.on_current_playlist_item_changed)
        
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
        elif event.key() == Qt.Key.Key_P:
            self.playlist_widget.on_toggle_playlist()
        elif event.key() == Qt.Key.Key_N:
            self.play_next_video()
        elif event.key() == Qt.Key.Key_B:
            self.play_previous_video()
        else:
            super().keyPressEvent(event)
    
    # Playlist-related methods
    def on_playlist_item_selected(self, file_path):
        """Handle selection of a playlist item."""
        self.load_video_from_path(file_path)
    
    def on_playlist_visibility_changed(self, is_visible):
        """Handle playlist visibility changes."""
        # Adjust window size when playlist is shown/hidden
        if is_visible:
            self.resize(self.width() + 300, self.height())
        else:
            self.resize(self.width() - 300, self.height())
        self.center_window()
    
    def on_current_playlist_item_changed(self, index):
        """Handle changes to the current playlist item."""
        if index >= 0:
            current_item = self.playlist_model.get_current_item()
            if current_item:
                self.load_video_from_path(current_item.file_path)
    
    def on_media_status_changed(self, status):
        """Handle media status changes for playlist auto-advance."""
        from PyQt6.QtMultimedia import QMediaPlayer
        
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            # Auto-advance to next video when current one ends
            self.play_next_video()
    
    def load_video_from_path(self, file_path):
        """Load and play a video from the given file path."""
        if file_path:
            # Stop current playback
            self.media_player.stop()
            
            # Load video into display
            self.video_display.load_video(file_path, self.media_player)
            file_name = file_path.split("/")[-1]
            self.setWindowTitle(f"Video Player - {file_name}")
            
            # Start playback immediately after loading
            self.media_player.play()
            
            print(f"Playing video: {file_path}")
    
    def play_next_video(self):
        """Play the next video in the playlist."""
        next_index = self.playlist_model.get_next_index()
        if next_index >= 0:
            self.playlist_model.set_current_index(next_index)
        else:
            # End of playlist reached
            self.media_player.stop()
            print("End of playlist reached")
    
    def play_previous_video(self):
        """Play the previous video in the playlist."""
        prev_index = self.playlist_model.get_previous_index()
        if prev_index >= 0:
            self.playlist_model.set_current_index(prev_index)
    
    def on_select_video(self):
        """Handle video file selection - now adds to playlist."""
        file_dialog = QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(
            self,
            "Select Video Files",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv);;All Files (*)"
        )
        
        if file_paths:
            # Add files to playlist
            self.playlist_model.add_videos(file_paths)
            
            # If no video is currently playing, play the first one
            if self.playlist_model.current_index == -1 and self.playlist_model.get_item_count() > 0:
                self.playlist_model.set_current_index(0)
