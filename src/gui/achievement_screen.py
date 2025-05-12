#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Achievements screen for Cybersecurity Escape Room
Displays earned badges and achievements
"""

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

logger = logging.getLogger(__name__)


class AchievementScreen(QWidget):
    """Achievements screen showing badges and accomplishments"""
    
    def __init__(self, main_window):
        """Initialize achievements screen"""
        super().__init__()
        self.main_window = main_window
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Header with back button
        header_layout = QHBoxLayout()
        
        back_button = QPushButton("← Back to Menu")
        back_button.setObjectName("backButton")
        back_button.clicked.connect(self.goto_menu)
        header_layout.addWidget(back_button)
        
        header_layout.addStretch()
        main_layout.addLayout(header_layout)
        
        # Title
        title_label = QLabel("Your Achievements")
        title_label.setObjectName("screenTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Achievements area with scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Placeholder content
        placeholder_frame = QFrame()
        placeholder_frame.setObjectName("contentFrame")
        placeholder_layout = QVBoxLayout(placeholder_frame)
        
        placeholder = QLabel("Achievements screen is under construction. This will display badges, trophies, and certificates earned through completing challenges and meeting specific objectives.")
        placeholder.setWordWrap(True)
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder_layout.addWidget(placeholder)
        
        scroll_layout.addWidget(placeholder_frame)
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        # Set stylesheet
        self.setStyleSheet("""
            #screenTitle {
                font-size: 24px;
                font-weight: bold;
                color: #00ff99;
                margin-bottom: 20px;
            }
            
            #contentFrame {
                background-color: #1e1e1e;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 15px;
            }
            
            #backButton {
                background-color: transparent;
                border: none;
                color: #00ff99;
                text-decoration: underline;
                font-weight: bold;
            }
            
            #backButton:hover {
                color: #00cc99;
            }
        """)
    
    def refresh(self):
        """Update achievements data"""
        # Placeholder for actual implementation
        pass
    
    def goto_menu(self):
        """Return to menu screen"""
        self.main_window.goto_menu() 