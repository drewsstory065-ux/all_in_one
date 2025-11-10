from PyQt6.QtCore import QObject, pyqtSignal
from datetime import datetime
import json
import os
from PyQt6.QtCore import QStandardPaths


class BookmarkItem:
    def __init__(self, url, title, timestamp=None, folder=None):
        self.url = url
        self.title = title
        self.timestamp = timestamp or datetime.now()
        self.folder = folder or ""

    def to_dict(self):
        return {
            'url': self.url,
            'title': self.title,
            'timestamp': self.timestamp.isoformat(),
            'folder': self.folder
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            url=data['url'],
            title=data['title'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            folder=data.get('folder', '')
        )


class BookmarkModel(QObject):
    bookmark_added = pyqtSignal()
    bookmark_removed = pyqtSignal()
    bookmarks_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._bookmarks = []
        self._max_items = 200
        self._storage_file = self._get_storage_path()
        self._load_bookmarks()

    def _get_storage_path(self):
        data_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, 'browser_bookmarks.json')

    def _load_bookmarks(self):
        try:
            if os.path.exists(self._storage_file):
                with open(self._storage_file, 'r') as f:
                    data = json.load(f)
                    self._bookmarks = [BookmarkItem.from_dict(item) for item in data]
        except Exception as e:
            print(f"Error loading bookmarks: {e}")
            self._bookmarks = []

    def _save_bookmarks(self):
        try:
            with open(self._storage_file, 'w') as f:
                data = [item.to_dict() for item in self._bookmarks]
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving bookmarks: {e}")

    def add_bookmark(self, url, title, folder=None):
        # Check if bookmark already exists
        existing_bookmark = self.get_bookmark_by_url(url)
        if existing_bookmark:
            # Update existing bookmark
            existing_bookmark.title = title
            existing_bookmark.timestamp = datetime.now()
            existing_bookmark.folder = folder or existing_bookmark.folder
        else:
            # Add new bookmark
            self._bookmarks.append(BookmarkItem(url, title, folder=folder))
            
            # Limit bookmarks size
            if len(self._bookmarks) > self._max_items:
                self._bookmarks = self._bookmarks[:self._max_items]
        
        self._save_bookmarks()
        self.bookmarks_changed.emit()
        self.bookmark_added.emit()

    def remove_bookmark(self, url):
        self._bookmarks = [item for item in self._bookmarks if item.url != url]
        self._save_bookmarks()
        self.bookmarks_changed.emit()
        self.bookmark_removed.emit()

    def get_bookmarks(self):
        return self._bookmarks.copy()

    def get_bookmark_by_url(self, url):
        for bookmark in self._bookmarks:
            if bookmark.url == url:
                return bookmark
        return None

    def is_bookmarked(self, url):
        return self.get_bookmark_by_url(url) is not None

    def clear_bookmarks(self):
        self._bookmarks = []
        self._save_bookmarks()
        self.bookmarks_changed.emit()

    def get_folders(self):
        folders = set()
        for bookmark in self._bookmarks:
            if bookmark.folder:
                folders.add(bookmark.folder)
        return sorted(list(folders))

    def get_bookmarks_by_folder(self, folder):
        return [bookmark for bookmark in self._bookmarks if bookmark.folder == folder]
