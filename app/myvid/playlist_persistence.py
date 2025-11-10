import json
import os
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class PlaylistPersistence:
    """Handles saving and loading playlist state to/from persistent storage."""
    
    CONFIG_DIR_NAME = "all_in_one"
    PLAYLIST_FILE_NAME = "playlist_state.json"
    VERSION = "1.0"
    
    @classmethod
    def get_config_directory(cls) -> Path:
        """Get platform-appropriate config directory."""
        system = platform.system()
        
        if system == "Windows":
            config_dir = Path(os.environ.get('APPDATA', ''))
        elif system == "Darwin":  # macOS
            config_dir = Path.home() / "Library" / "Application Support"
        else:  # Linux and other Unix-like systems
            config_dir = Path.home() / ".config"
        
        # Create the application-specific config directory
        app_config_dir = config_dir / cls.CONFIG_DIR_NAME
        app_config_dir.mkdir(parents=True, exist_ok=True)
        
        return app_config_dir
    
    @classmethod
    def get_playlist_file_path(cls) -> Path:
        """Get the full path to the playlist state file."""
        config_dir = cls.get_config_directory()
        return config_dir / cls.PLAYLIST_FILE_NAME
    
    @classmethod
    def save_playlist(cls, playlist_model, playlist_width: int) -> bool:
        """
        Save playlist state to persistent storage.
        
        Args:
            playlist_model: The PlaylistModel instance to save
            playlist_width: Current width of the playlist widget
            
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            playlist_data = cls._serialize_playlist(playlist_model)
            playlist_data['playlist_width'] = playlist_width
            playlist_data['version'] = cls.VERSION
            
            file_path = cls.get_playlist_file_path()
            
            # Write to temporary file first, then rename (atomic operation)
            temp_file = file_path.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(playlist_data, f, indent=2, ensure_ascii=False)
            
            # Replace the original file with the temporary one
            temp_file.replace(file_path)
            
            logger.info(f"Playlist state saved successfully to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save playlist state: {e}")
            return False
    
    @classmethod
    def load_playlist(cls) -> Tuple[Optional[Dict], Optional[int]]:
        """
        Load playlist state from persistent storage.
        
        Returns:
            Tuple containing:
            - playlist_data: Dictionary with playlist state, or None if loading failed
            - playlist_width: Saved playlist width, or None if not available
        """
        try:
            file_path = cls.get_playlist_file_path()
            
            if not file_path.exists():
                logger.info("No saved playlist state found")
                return None, None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                playlist_data = json.load(f)
            
            # Validate the loaded data
            if not cls._validate_playlist_data(playlist_data):
                logger.warning("Invalid playlist data format, ignoring saved state")
                return None, None
            
            # Filter out files that no longer exist
            valid_items = []
            for item in playlist_data.get('playlist_items', []):
                file_path = item.get('file_path')
                if file_path and Path(file_path).exists():
                    valid_items.append(item)
                else:
                    logger.warning(f"Video file no longer exists: {file_path}")
            
            playlist_data['playlist_items'] = valid_items
            
            # Adjust current index if it's now out of bounds
            current_index = playlist_data.get('current_index', -1)
            if current_index >= len(valid_items):
                playlist_data['current_index'] = len(valid_items) - 1 if valid_items else -1
            
            playlist_width = playlist_data.get('playlist_width')
            
            logger.info(f"Playlist state loaded successfully from {file_path}")
            return playlist_data, playlist_width
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse playlist state file: {e}")
            return None, None
        except Exception as e:
            logger.error(f"Failed to load playlist state: {e}")
            return None, None
    
    @classmethod
    def _serialize_playlist(cls, playlist_model) -> Dict:
        """Serialize playlist model data to dictionary format."""
        return {
            'playlist_items': [
                {
                    'file_path': item.file_path,
                    'display_name': str(item)
                }
                for item in playlist_model.items
            ],
            'current_index': playlist_model.current_index,
            'loop_mode': playlist_model.loop_mode,
            'repeat_mode': playlist_model.repeat_mode
        }
    
    @classmethod
    def _validate_playlist_data(cls, data: Dict) -> bool:
        """Validate the structure of loaded playlist data."""
        if not isinstance(data, dict):
            return False
        
        # Check required fields
        required_fields = ['playlist_items', 'current_index', 'loop_mode', 'repeat_mode']
        for field in required_fields:
            if field not in data:
                return False
        
        # Validate playlist_items structure
        if not isinstance(data['playlist_items'], list):
            return False
        
        for item in data['playlist_items']:
            if not isinstance(item, dict) or 'file_path' not in item:
                return False
        
        # Validate types
        if not isinstance(data['current_index'], int):
            return False
        if not isinstance(data['loop_mode'], bool):
            return False
        if not isinstance(data['repeat_mode'], bool):
            return False
        
        return True
    
    @classmethod
    def clear_saved_playlist(cls) -> bool:
        """Clear the saved playlist state file."""
        try:
            file_path = cls.get_playlist_file_path()
            if file_path.exists():
                file_path.unlink()
                logger.info("Cleared saved playlist state")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to clear saved playlist state: {e}")
            return False
