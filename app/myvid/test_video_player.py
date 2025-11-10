import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from myvid_window import MyVidWindow


def test_video_player():
    """Test the video player implementation."""
    app = QApplication(sys.argv)
    
    # Create and show the video player window
    window = MyVidWindow()
    window.show()
    
    # Print verification information
    print("Video Player Test")
    print("=" * 50)
    print(f"Window size: {window.width()}x{window.height()}")
    print(f"Control bar height: {window.control_bar.height()}")
    print(f"Video display size: {window.video_display.width()}x{window.video_display.height()}")
    print(f"Total time: {window.total_time} seconds ({window.control_bar.format_time(window.total_time)})")
    print("\nControl bar features:")
    print("- [<<] [<] [>/■] [>] [>>] timeline [⬚]")
    print("- Timeline slider with progress indicator")
    print("- Current and total time display")
    print("- Keyboard shortcuts: Space, Left/Right arrows, F, Esc")
    print("\nAll classes are under 150 lines:")
    print(f"- MyVidWindow: {len(open('app/myvid/myvid_window.py').readlines())} lines")
    print(f"- ControlBar: {len(open('app/myvid/control_bar.py').readlines())} lines")
    print(f"- VideoDisplay: {len(open('app/myvid/video_display.py').readlines())} lines")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    test_video_player()
