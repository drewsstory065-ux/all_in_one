#!/bin/bash
mkdir src
mkdir app
mkdir app/main
mkdir config

echo 'from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(100, 500)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: lightgray;")
        self.move_to_bottom_right()
    
    def move_to_bottom_right(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        x = screen_geometry.width() - self.width()
        y = screen_geometry.height() - self.height()
        self.setGeometry(x, y, self.width(), self.height())
' > app/main/main_window.py

echo 'import sys
from PyQt6.QtWidgets import QApplication
from app.main.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()  # Fixed: was Window() but class is MainWindow
    window.show()
    sys.exit(app.exec())
' > main.py

echo '#!/bin/bash

# Check if all required tools are already installed
if command -v python3 &> /dev/null && command -v pip3 &> /dev/null && python3 -c "import PyQt6" &> /dev/null; then
    echo "All required tools (Python3, pip3, PyQt6) are already installed."
    exit 0
fi

# Update package list once at the beginning to avoid redundant updates
sudo apt update

# Check for Python3
if ! command -v python3 &> /dev/null; then
    echo "Python3 could not be found. Installing Python3..."
    sudo apt install -y python3
else
    echo "Python3 is already installed."
fi

# Check for pip3
if ! command -v pip3 &> /dev/null; then
    echo "pip3 could not be found. Installing pip3..."
    sudo apt install -y python3-pip
else
    echo "pip3 is already installed."
fi

# Check for PyQt6
if ! python3 -c "import PyQt6" &> /dev/null; then
    echo "PyQt6 is not installed. Installing PyQt6..."
    pip3 install PyQt6
else
    echo "PyQt6 is already installed."
fi
' > install.sh

echo '#!/bin/bash
./install.sh
python3 main.py
' > run.sh

chmod +x install.sh run.sh
./run.sh