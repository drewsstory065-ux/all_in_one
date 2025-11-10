"""Styles for the video player components."""


class VideoPlayerStyles:
    """Static styles for video player components."""
    
    # Control bar styles
    CONTROL_BAR_STYLE = "background-color: #2d2d2d; border-top: 1px solid #444;"
    
    # Button styles
    BUTTON_STYLE = """
        QPushButton {
            background-color: #404040;
            border: 1px solid #555;
            color: white;
            font-size: 10px;
            border-radius: 2px;
        }
        QPushButton:hover {
            background-color: #505050;
            border: 1px solid #666;
        }
        QPushButton:pressed {
            background-color: #606060;
        }
    """
    
    # Time label styles
    TIME_LABEL_STYLE = "color: white; font-size: 10px;"
    
    # Timeline slider styles
    TIMELINE_SLIDER_STYLE = """
        QSlider::groove:horizontal {
            border: 1px solid #999999;
            height: 4px;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
            margin: 2px 0;
        }
        QSlider::handle:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
            border: 1px solid #5c5c5c;
            width: 8px;
            margin: -4px 0;
            border-radius: 3px;
        }
        QSlider::sub-page:horizontal {
            background: #0078d4;
            border: 1px solid #777;
            height: 4px;
            border-radius: 2px;
        }
    """
    
    # Volume slider styles
    VOLUME_SLIDER_STYLE = """
        QSlider::groove:horizontal {
            background: #555;
            height: 3px;
            border-radius: 1px;
        }
        
        QSlider::handle:horizontal {
            background: #fff;
            border: 1px solid #777;
            width: 8px;
            height: 8px;
            border-radius: 4px;
            margin: -3px 0;
        }
        
        QSlider::sub-page:horizontal {
            background: #0078d4;
            border-radius: 1px;
        }
    """
    
    # Video display styles
    VIDEO_DISPLAY_STYLE = """
        background-color: black; 
        color: white; 
        border: 1px solid #333;
        min-height: 300px;
    """
    
    # Main window styles
    MAIN_WINDOW_STYLE = "background-color: #1e1e1e;"
    
    # Playlist styles
    PLAYLIST_STYLE = """
        QListWidget {
            background-color: #2d2d2d;
            color: white;
            border: 1px solid #444;
            border-radius: 3px;
            font-size: 11px;
        }
        QListWidget::item {
            border-bottom: 1px solid #3d3d3d;
            padding: 3px 5px;
        }
        QListWidget::item:selected {
            background-color: #0078d4;
            color: white;
        }
        QListWidget::item:hover {
            background-color: #3d3d3d;
        }
        QListWidget::item:alternate {
            background-color: #2a2a2a;
        }
    """
    
    # Checkbox styles
    CHECKBOX_STYLE = """
        QCheckBox {
            color: white;
            font-size: 10px;
        }
        QCheckBox::indicator {
            width: 12px;
            height: 12px;
        }
        QCheckBox::indicator:unchecked {
            border: 1px solid #666;
            background-color: #404040;
        }
        QCheckBox::indicator:checked {
            border: 1px solid #0078d4;
            background-color: #0078d4;
        }
    """
