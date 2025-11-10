from PyQt6.QtCore import QObject, pyqtSignal
from datetime import datetime
import json
import os
from PyQt6.QtCore import QStandardPaths


class HistoryItem:
    def __init__(self, url, title, timestamp=None):
        self.url = url
        self.title = title
        self.timestamp = timestamp or datetime.now()

    def to_dict(self):
        return {
            'url': self.url,
            'title': self.title,
            'timestamp': self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            url=data['url'],
            title=data['title'],
            timestamp=datetime.fromisoformat(data['timestamp'])
        )


class HistoryModel(QObject):
    history_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._history = []
        self._max_items = 100
        self._storage_file = self._get_storage_path()
        self._load_history()

    def _get_storage_path(self):
        data_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, 'browser_history.json')

    def _load_history(self):
        try:
            if os.path.exists(self._storage_file):
                with open(self._storage_file, 'r') as f:
                    data = json.load(f)
                    self._history = [HistoryItem.from_dict(item) for item in data]
        except Exception as e:
            print(f"Error loading history: {e}")
            self._history = []

    def _save_history(self):
        try:
            with open(self._storage_file, 'w') as f:
                data = [item.to_dict() for item in self._history]
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")

    def add_entry(self, url, title):
        # Remove any existing entry with the same URL
        self._history = [item for item in self._history if item.url != url]
        
        # Add new entry at the beginning
        self._history.insert(0, HistoryItem(url, title))
        
        # Limit history size
        if len(self._history) > self._max_items:
            self._history = self._history[:self._max_items]
        
        self._save_history()
        self.history_changed.emit()

    def get_history(self):
        return self._history.copy()

    def clear_history(self):
        self._history = []
        self._save_history()
        self.history_changed.emit()

    def remove_entry(self, url):
        self._history = [item for item in self._history if item.url != url]
        self._save_history()
        self.history_changed.emit()
