
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from .navigation_bar import NavigationBar
from .tab_widget import TabWidget
from .history_model import HistoryModel
from .history_widget import HistoryWidget

class MyBrowserWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Browser")
        self.setGeometry(100, 100, 1024, 768)

        # Initialize components
        self.history_model = HistoryModel(self)
        self.tab_widget = TabWidget(self)
        self.navigation_bar = NavigationBar(self)
        self.history_widget = HistoryWidget(self.history_model, self)

        # Setup UI
        self.addToolBar(self.navigation_bar)
        self.setCentralWidget(self.tab_widget)
        
        # Position history widget
        self.history_widget.setWindowTitle("Browser History")
        self.history_widget.resize(600, 400)
        self.history_widget.hide()

        # Create initial tab
        initial_tab = self.tab_widget.create_tab()
        
        # Connect initial tab to history tracking
        initial_tab.title_changed.connect(self.add_to_history)

        # Connect signals
        self.connect_signals()

    def connect_signals(self):
        # Navigation signals
        self.navigation_bar.go_button.clicked.connect(self.navigate_to_url)
        self.navigation_bar.url_line_edit.returnPressed.connect(self.navigate_to_url)
        self.navigation_bar.history_button.clicked.connect(self.toggle_history)
        
        # Tab signals
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        self.tab_widget.tab_count_changed.connect(self.update_window_title)
        
        # Connect to tab creation to ensure new tabs track history
        self.tab_widget.tab_count_changed.connect(self.connect_new_tab_to_history)
        
        # History signals
        self.history_widget.history_item_clicked.connect(self.open_history_url_in_new_tab)

    def navigate_to_url(self):
        url = self.navigation_bar.url_line_edit.text()
        if not url.startswith("http"):
            url = "http://" + url
        current_web_view = self.tab_widget.currentWidget()
        if current_web_view:
            current_web_view.set_url(url)

    def on_tab_changed(self, index):
        """Update navigation bar when tab changes"""
        current_web_view = self.tab_widget.currentWidget()
        if current_web_view:
            # Update URL in navigation bar
            current_url = current_web_view.url().toString()
            self.navigation_bar.url_line_edit.setText(current_url)
            
            # Connect navigation buttons to current tab (safe disconnect)
            try:
                self.navigation_bar.back_button.clicked.disconnect()
            except TypeError:
                pass  # No connections to disconnect
            try:
                self.navigation_bar.next_button.clicked.disconnect()
            except TypeError:
                pass  # No connections to disconnect
            try:
                self.navigation_bar.reload_button.clicked.disconnect()
            except TypeError:
                pass  # No connections to disconnect
            
            self.navigation_bar.back_button.clicked.connect(current_web_view.back)
            self.navigation_bar.next_button.clicked.connect(current_web_view.forward)
            self.navigation_bar.reload_button.clicked.connect(current_web_view.reload)
            
            # Connect title changed signal for history tracking
            current_web_view.title_changed.connect(self.add_to_history)

    def add_to_history(self, title, url):
        """Add page to history when title changes"""
        if url and url != "about:blank" and not url.startswith("data:"):
            self.history_model.add_entry(url, title)

    def toggle_history(self):
        """Show or hide history widget"""
        if self.history_widget.isVisible():
            self.history_widget.hide()
        else:
            # Position history widget near the navigation bar
            nav_bar_rect = self.navigation_bar.geometry()
            history_pos = self.mapToGlobal(nav_bar_rect.bottomLeft())
            self.history_widget.move(history_pos.x(), history_pos.y())
            self.history_widget.show()
            self.history_widget.raise_()
            self.history_widget.activateWindow()

    def open_history_url_in_new_tab(self, url):
        """Open a history URL in a new tab"""
        self.tab_widget.create_tab_with_url(url)

    def connect_new_tab_to_history(self, tab_count):
        """Connect the most recent tab to history tracking"""
        if tab_count > 0:
            # Get the most recent tab (last one added)
            recent_tab = self.tab_widget.widget(tab_count - 1)
            if recent_tab:
                # Connect title changed signal for history tracking
                recent_tab.title_changed.connect(self.add_to_history)

    def update_window_title(self, tab_count):
        """Update window title with tab count"""
        self.setWindowTitle(f"My Browser - {tab_count} tabs")

    def closeEvent(self, event):
        self.close()
