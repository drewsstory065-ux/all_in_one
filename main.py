import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtCore import Qt
from app.main.main_window import MainWindow

from app.main.system_tray_handler import SystemTrayHandler

if __name__ == "__main__":
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    window = MainWindow()
    
    tray_handler = SystemTrayHandler(window)
    
    window.show()
    sys.exit(app.exec())
