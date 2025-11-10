from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QAction
from PyQt6.QtCore import pyqtSignal
from src.tools.config import Config


class SystemTrayHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.tray_icon = None
        self.config = Config()
        self.setup_system_tray()
    
    def setup_system_tray(self):
        # Create system tray icon
        self.tray_icon = QSystemTrayIcon()
        
        # Use icon from config file
        icon_path = self.config.get('app', 'icon_path')
        icon = QIcon(icon_path)
        self.tray_icon.setIcon(icon)
        
        # Create context menu
        tray_menu = QMenu()
        show_action = QAction("Show", None)
        quit_action = QAction("Quit", None)
        
        show_action.triggered.connect(self.show_main_window)
        quit_action.triggered.connect(self.quit_application)
        
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()
    
    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_main_window()
    
    def show_main_window(self):
        if self.main_window.isHidden():
            self.main_window.show()
        else:
            self.main_window.raise_()
            self.main_window.activateWindow()
    
    def quit_application(self):
        self.main_window.close()