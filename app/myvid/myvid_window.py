from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QSplitter
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from .video_display import VideoDisplay
from .control_bar import ControlBar
from .playlist_model import PlaylistModel
from .playlist_widget import PlaylistWidget
from .playlist_persistence import PlaylistPersistence
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
        
        # Create main splitter for resizable playlist and video layout
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.setChildrenCollapsible(False)
        
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
        
        # Create video container widget
        video_container = QWidget()
        video_container.setLayout(video_layout)
        
        # Create playlist model and widget
        self.playlist_model = PlaylistModel()
        self.playlist_widget = PlaylistWidget(self.playlist_model)
        
        # Add playlist and video container to splitter (playlist on left)
        self.main_splitter.addWidget(self.playlist_widget)
        self.main_splitter.addWidget(video_container)
        
        # Set initial sizes (playlist: 300px, video: rest of space)
        self.main_splitter.setSizes([300, 500])
        
        # Set splitter handle style for better visibility
        self.main_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #555555;
                width: 2px;
            }
            QSplitter::handle:hover {
                background-color: #777777;
            }
        """)
        
        # Create main layout and add splitter
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.main_splitter)
        
        self.setLayout(main_layout)
        
        # Load saved playlist state after UI is set up
        self.load_saved_playlist()
    
    def connect_signals(self):
        """Connect all component signals."""
        # Control bar signals
        self.control_bar.toggle_playlist.connect(self.on_toggle_playlist)
        self.control_bar.select_video.connect(self.on_select_video)
        self.control_bar.rewind_fast.connect(self.on_rewind_fast)
        self.control_bar.rewind.connect(self.on_rewind)
        self.control_bar.previous_video.connect(self.play_previous_video)
        self.control_bar.play_pause.connect(self.on_play_pause)
        self.control_bar.next_video.connect(self.play_next_video)
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
        self.playlist_model.playlist_changed.connect(self.update_navigation_buttons)
        self.playlist_model.current_item_changed.connect(self.update_navigation_buttons)
        
        # Timer for UI updates
        self.timer.timeout.connect(self.update_time_display)
    
    def center_window(self):
        """Center the window on screen."""
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.setGeometry(x, y, self.width(), self.height())
    
    def closeEvent(self, event):
        """Save playlist state before closing."""
        try:
            # Get current playlist width from splitter
            playlist_width = self.main_splitter.sizes()[0]
            
            # Save playlist state
            PlaylistPersistence.save_playlist(self.playlist_model, playlist_width)
            
            print("Playlist state saved successfully")
            
        except Exception as e:
            print(f"Error saving playlist state: {e}")
        
        super().closeEvent(event)
    
    def load_saved_playlist(self):
        """Load saved playlist state from persistent storage."""
        try:
            playlist_data, playlist_width = PlaylistPersistence.load_playlist()
            
            if playlist_data:
                # Load playlist data into model
                success = self.playlist_model.load_from_data(playlist_data)
                
                if success:
                    print("Playlist state loaded successfully")
                    
                    # Restore playlist width if available
                    if playlist_width is not None:
                        total_width = self.main_splitter.width()
                        video_width = total_width - playlist_width
                        self.main_splitter.setSizes([playlist_width, video_width])
                        print(f"Restored playlist width: {playlist_width}px")
                    
                    # If there's a current item, play it
                    if self.playlist_model.current_index >= 0:
                        current_item = self.playlist_model.get_current_item()
                        if current_item:
                            self.load_video_from_path(current_item.file_path)
                else:
                    print("Failed to load playlist data")
            else:
                print("No saved playlist state found")
                
        except Exception as e:
            print(f"Error loading saved playlist: {e}")
    
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
    
    def on_toggle_playlist(self):
        """Handle playlist toggle from control bar."""
        self.playlist_widget.on_toggle_playlist()
    
    
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
        # Show/hide playlist widget in splitter
        self.playlist_widget.setVisible(is_visible)
        
        # Update control bar button state
        self.control_bar.update_playlist_button(is_visible)
    
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
    
    def update_navigation_buttons(self):
        """Update the state of previous/next navigation buttons."""
        current_index = self.playlist_model.current_index
        item_count = self.playlist_model.get_item_count()
        loop_mode = self.playlist_model.loop_mode
        
        self.control_bar.update_navigation_buttons(current_index, item_count, loop_mode)
    
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
