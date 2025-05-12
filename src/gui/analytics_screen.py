#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analytics screen for Cybersecurity Escape Room
Displays user performance statistics and learning analytics
"""

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QProgressBar
)
from PyQt6.QtCore import Qt

logger = logging.getLogger(__name__)


class AnalyticsScreen(QWidget):
    """Analytics screen showing user performance statistics"""
    
    def __init__(self, main_window):
        """Initialize analytics screen"""
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
        title_label = QLabel("Performance Analytics")
        title_label.setObjectName("screenTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Content frame
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_layout = QVBoxLayout(content_frame)
        
        # Placeholder content
        placeholder = QLabel("Analytics screen is under construction. This will display detailed statistics, progress tracking, and learning analytics based on user performance.")
        placeholder.setWordWrap(True)
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(placeholder)
        
        main_layout.addWidget(content_frame)
        
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
        """Update analytics data"""
        # Placeholder for actual implementation
        pass
    
    def goto_menu(self):
        """Return to menu screen"""
        self.main_window.goto_menu() 