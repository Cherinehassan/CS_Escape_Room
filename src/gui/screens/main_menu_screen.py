#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main menu screen for Cybersecurity Escape Room
Central hub for navigating the game
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QGridLayout, QSpacerItem,
                            QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont, QIcon, QColor

from ..utils.animation_effects import FlickerEffect, PulseAnimation, CyberDoorTransition


class MainMenuScreen(QWidget):
    """Main menu screen for game navigation"""
    
    # Signals
    start_game_requested = pyqtSignal()  # Start a new game
    continue_game_requested = pyqtSignal()  # Continue existing game
    view_puzzles_requested = pyqtSignal()  # View available puzzles
    view_dashboard_requested = pyqtSignal()  # View progress dashboard
    view_analytics_requested = pyqtSignal()  # View analytics screen
    view_leaderboard_requested = pyqtSignal()  # View leaderboard
    view_settings_requested = pyqtSignal()  # View settings
    view_tutorial_requested = pyqtSignal()  # View tutorial
    logout_requested = pyqtSignal()  # Log out of the game
    
    def __init__(self, username, parent=None):
        """
        Initialize main menu screen
        
        Args:
            username: Current user's username
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.username = username
        
        self._create_ui()
        self._connect_signals()
        self._apply_styles()
        self._apply_animations()
    
    def _create_ui(self):
        """Create the main menu UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 50, 50, 50)
        
        # Header section
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QVBoxLayout(header_frame)
        
        self.title_label = QLabel("CYBERSECURITY ESCAPE ROOM")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setObjectName("titleLabel")
        header_layout.addWidget(self.title_label)
        
        self.welcome_label = QLabel(f"Welcome, Agent {self.username}")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setObjectName("welcomeLabel")
        header_layout.addWidget(self.welcome_label)
        
        main_layout.addWidget(header_frame)
        
        # Description section
        description_frame = QFrame()
        description_frame.setObjectName("descriptionFrame")
        description_layout = QVBoxLayout(description_frame)
        
        self.description_label = QLabel(
            "Your mission is to solve cybersecurity challenges to escape the virtual puzzle room. "
            "Each challenge will test your knowledge and skills in different areas of cybersecurity. "
            "Are you ready to begin?"
        )
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setObjectName("descriptionLabel")
        description_layout.addWidget(self.description_label)
        
        main_layout.addWidget(description_frame)
        
        # Button section
        button_frame = QFrame()
        button_frame.setObjectName("buttonFrame")
        button_layout = QGridLayout(button_frame)
        button_layout.setSpacing(20)
        
        # Start Game button
        self.start_button = QPushButton("START NEW GAME")
        self.start_button.setObjectName("mainMenuButton")
        button_layout.addWidget(self.start_button, 0, 0)
        
        # Continue Game button
        self.continue_button = QPushButton("CONTINUE")
        self.continue_button.setObjectName("mainMenuButton")
        button_layout.addWidget(self.continue_button, 0, 1)
        
        # View Puzzles button
        self.puzzles_button = QPushButton("VIEW CHALLENGES")
        self.puzzles_button.setObjectName("mainMenuButton")
        button_layout.addWidget(self.puzzles_button, 1, 0)
        
        # Dashboard button
        self.dashboard_button = QPushButton("DASHBOARD")
        self.dashboard_button.setObjectName("mainMenuButton")
        button_layout.addWidget(self.dashboard_button, 1, 1)
        
        # Analytics button
        self.analytics_button = QPushButton("ANALYTICS")
        self.analytics_button.setObjectName("mainMenuButton")
        button_layout.addWidget(self.analytics_button, 2, 0)
        
        # Leaderboard button
        self.leaderboard_button = QPushButton("GLOBAL LEADERBOARD")
        self.leaderboard_button.setObjectName("mainMenuButton")
        button_layout.addWidget(self.leaderboard_button, 2, 1)
        
        # Settings button
        self.settings_button = QPushButton("SETTINGS")
        self.settings_button.setObjectName("mainMenuButton")
        button_layout.addWidget(self.settings_button, 3, 0)
        
        # Tutorial button
        self.tutorial_button = QPushButton("TUTORIAL")
        self.tutorial_button.setObjectName("mainMenuButton")
        button_layout.addWidget(self.tutorial_button, 3, 1)
        
        # Logout button
        self.logout_button = QPushButton("LOGOUT")
        self.logout_button.setObjectName("mainMenuButton")
        button_layout.addWidget(self.logout_button, 3, 1)  # Changed from span to single column
        
        main_layout.addWidget(button_frame)
        
        # Status section
        status_frame = QFrame()
        status_frame.setObjectName("statusFrame")
        status_layout = QHBoxLayout(status_frame)
        
        self.status_label = QLabel("MISSION STATUS: READY")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setObjectName("statusLabel")
        status_layout.addWidget(self.status_label)
        
        main_layout.addWidget(status_frame)
        
        # Spacer
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Copyright
        self.copyright_label = QLabel("© 2023 Cybersecurity Escape Room")
        self.copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.copyright_label.setObjectName("copyrightLabel")
        main_layout.addWidget(self.copyright_label)
    
    def _connect_signals(self):
        """Connect signals to slots"""
        self.start_button.clicked.connect(self.start_game_requested.emit)
        self.continue_button.clicked.connect(self.continue_game_requested.emit)
        self.puzzles_button.clicked.connect(self.view_puzzles_requested.emit)
        self.dashboard_button.clicked.connect(self.view_dashboard_requested.emit)
        self.analytics_button.clicked.connect(self.view_analytics_requested.emit)
        self.leaderboard_button.clicked.connect(self.view_leaderboard_requested.emit)
        self.settings_button.clicked.connect(self.view_settings_requested.emit)
        self.tutorial_button.clicked.connect(self.view_tutorial_requested.emit)
        self.logout_button.clicked.connect(self.logout_requested.emit)
    
    def _apply_styles(self):
        """Apply styles to the main menu screen"""
        self.setStyleSheet("""
            #titleLabel {
                font-size: 36px;
                font-weight: bold;
                color: #00ccff;
                margin-bottom: 10px;
            }
            
            #welcomeLabel {
                font-size: 24px;
                color: #00ff66;
                margin-bottom: 20px;
            }
            
            #descriptionFrame {
                background-color: rgba(0, 0, 0, 0.3);
                border-radius: 10px;
                padding: 20px;
                border: 1px solid #333333;
            }
            
            #descriptionLabel {
                font-size: 16px;
                color: #cccccc;
                line-height: 1.5;
            }
            
            #buttonFrame {
                margin-top: 20px;
                margin-bottom: 20px;
            }
            
            #mainMenuButton {
                background-color: rgba(0, 50, 100, 0.7);
                color: #00ccff;
                border: 2px solid #00ccff;
                border-radius: 8px;
                padding: 15px 20px;
                font-size: 16px;
                font-weight: bold;
                min-height: 60px;
            }
            
            #mainMenuButton:hover {
                background-color: rgba(0, 80, 120, 0.8);
                border: 2px solid #33d6ff;
                color: #ffffff;
            }
            
            #mainMenuButton:pressed {
                background-color: rgba(0, 100, 150, 0.9);
                border: 2px solid #00aaff;
            }
            
            #statusFrame {
                background-color: rgba(0, 0, 0, 0.5);
                border-radius: 5px;
                padding: 10px;
                border: 1px solid #333333;
            }
            
            #statusLabel {
                font-size: 14px;
                color: #00ff66;
                font-family: "Courier New", monospace;
                font-weight: bold;
            }
            
            #copyrightLabel {
                color: #777777;
                font-size: 12px;
                margin-top: 10px;
            }
        """)
    
    def _apply_animations(self):
        """Apply animations to main menu elements"""
        # Flicker effect on title
        self.title_flicker = FlickerEffect(
            self.title_label, 
            color="#00ccff", 
            intensity=0.2,
            interval_range=(2000, 5000)
        )
        self.title_flicker.start()
        
        # Pulse animation on status label
        self.status_pulse = PulseAnimation.create(
            self.status_label,
            b"color",
            QColor("#00ff66"),
            QColor("#009933"),
            duration=1500,
            loop_count=-1  # Infinite
        )
        self.status_pulse.start()
    
    def update_status(self, status_text):
        """
        Update status message
        
        Args:
            status_text: New status text
        """
        self.status_label.setText(f"MISSION STATUS: {status_text}")
    
    def update_username(self, username):
        """
        Update displayed username
        
        Args:
            username: New username
        """
        self.username = username
        self.welcome_label.setText(f"Welcome, Agent {self.username}") 