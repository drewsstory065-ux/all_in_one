from PyQt6.QtCore import QObject, pyqtSignal
from pathlib import Path
from typing import Dict, List, Optional


class PlaylistItem:
    """Represents a single item in the playlist."""
    
    def __init__(self, file_path, title=None):
        self.file_path = file_path
        self.title = title or Path(file_path).name
        self.duration = 0  # Will be populated when video is loaded
    
    def __str__(self):
        return f"{self.title} ({self.format_duration()})"
    
    def format_duration(self):
        """Format duration into MM:SS or HH:MM:SS format."""
        if self.duration <= 0:
            return "--:--"
        
        hours = int(self.duration // 3600)
        minutes = int((self.duration % 3600) // 60)
        secs = int(self.duration % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"


class PlaylistModel(QObject):
    """Model class for managing the playlist data."""
    
    # Signals
    playlist_changed = pyqtSignal()  # Emitted when playlist items change
    current_item_changed = pyqtSignal(int)  # Emitted when current item index changes
    
    def __init__(self):
        super().__init__()
        self.items = []
        self.current_index = -1
        self.loop_mode = False  # Loop the entire playlist
        self.repeat_mode = False  # Repeat current item
    
    def add_video(self, file_path):
        """Add a video file to the playlist."""
        item = PlaylistItem(file_path)
        self.items.append(item)
        self.playlist_changed.emit()
        
        # If this is the first item, set it as current
        if len(self.items) == 1:
            self.set_current_index(0)
    
    def add_videos(self, file_paths):
        """Add multiple video files to the playlist."""
        for file_path in file_paths:
            self.add_video(file_path)
    
    def remove_video(self, index):
        """Remove a video from the playlist."""
        if 0 <= index < len(self.items):
            self.items.pop(index)
            
            # Adjust current index if needed
            if self.current_index >= len(self.items):
                self.current_index = len(self.items) - 1
            elif self.current_index == index:
                self.current_index = -1
            
            self.playlist_changed.emit()
            self.current_item_changed.emit(self.current_index)
    
    def clear_playlist(self):
        """Clear all items from the playlist."""
        self.items.clear()
        self.current_index = -1
        self.playlist_changed.emit()
        self.current_item_changed.emit(self.current_index)
    
    def set_current_index(self, index):
        """Set the current playing item index."""
        if 0 <= index < len(self.items):
            self.current_index = index
            self.current_item_changed.emit(index)
    
    def get_current_item(self):
        """Get the current playlist item."""
        if 0 <= self.current_index < len(self.items):
            return self.items[self.current_index]
        return None
    
    def get_next_index(self):
        """Get the next item index based on current mode."""
        if not self.items:
            return -1
        
        if self.repeat_mode:
            return self.current_index  # Repeat current item
        
        if self.loop_mode:
            # Loop through entire playlist
            return (self.current_index + 1) % len(self.items)
        else:
            # Normal sequential playback
            if self.current_index + 1 < len(self.items):
                return self.current_index + 1
            else:
                return -1  # End of playlist
    
    def get_previous_index(self):
        """Get the previous item index."""
        if not self.items:
            return -1
        
        if self.loop_mode:
            # Loop through entire playlist
            return (self.current_index - 1) % len(self.items)
        else:
            # Normal sequential playback
            if self.current_index - 1 >= 0:
                return self.current_index - 1
            else:
                return -1  # Beginning of playlist
    
    def move_item_up(self, index):
        """Move an item up in the playlist."""
        if index > 0 and index < len(self.items):
            self.items[index], self.items[index - 1] = self.items[index - 1], self.items[index]
            
            # Adjust current index if needed
            if self.current_index == index:
                self.current_index = index - 1
            elif self.current_index == index - 1:
                self.current_index = index
            
            self.playlist_changed.emit()
            self.current_item_changed.emit(self.current_index)
    
    def move_item_down(self, index):
        """Move an item down in the playlist."""
        if index >= 0 and index < len(self.items) - 1:
            self.items[index], self.items[index + 1] = self.items[index + 1], self.items[index]
            
            # Adjust current index if needed
            if self.current_index == index:
                self.current_index = index + 1
            elif self.current_index == index + 1:
                self.current_index = index
            
            self.playlist_changed.emit()
            self.current_item_changed.emit(self.current_index)
    
    def set_loop_mode(self, enabled):
        """Enable or disable loop mode."""
        self.loop_mode = enabled
    
    def set_repeat_mode(self, enabled):
        """Enable or disable repeat mode."""
        self.repeat_mode = enabled
    
    def get_item_count(self):
        """Get the number of items in the playlist."""
        return len(self.items)
    
    def get_item_at(self, index):
        """Get the playlist item at the specified index."""
        if 0 <= index < len(self.items):
            return self.items[index]
        return None
    
    def update_item_duration(self, index, duration):
        """Update the duration of a playlist item."""
        if 0 <= index < len(self.items):
            self.items[index].duration = duration
            self.playlist_changed.emit()

    def serialize(self) -> Dict:
        """Serialize current playlist state to dictionary format."""
        return {
            'playlist_items': [
                {
                    'file_path': item.file_path,
                    'display_name': str(item)
                }
                for item in self.items
            ],
            'current_index': self.current_index,
            'loop_mode': self.loop_mode,
            'repeat_mode': self.repeat_mode
        }

    def load_from_data(self, data: Dict) -> bool:
        """
        Load playlist from serialized data.
        
        Args:
            data: Dictionary containing playlist state
            
        Returns:
            bool: True if loading was successful, False otherwise
        """
        try:
            # Clear current playlist
            self.items.clear()
            
            # Load playlist items
            for item_data in data.get('playlist_items', []):
                file_path = item_data.get('file_path')
                if file_path:
                    item = PlaylistItem(file_path)
                    self.items.append(item)
            
            # Load other state
            self.current_index = data.get('current_index', -1)
            self.loop_mode = data.get('loop_mode', False)
            self.repeat_mode = data.get('repeat_mode', False)
            
            # Emit signals to update UI
            self.playlist_changed.emit()
            self.current_item_changed.emit(self.current_index)
            
            return True
            
        except Exception as e:
            print(f"Error loading playlist data: {e}")
            return False
