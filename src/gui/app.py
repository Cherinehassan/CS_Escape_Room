#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main application GUI for Cybersecurity Escape Room
"""

import os
import sys
import logging
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QVBoxLayout, 
    QHBoxLayout, QWidget, QPushButton, QLabel, QFrame,
    QMessageBox
)
from PyQt6.QtGui import QIcon, QPixmap, QFont, QColor, QPalette
from PyQt6.QtCore import Qt, QSize

from src.core.auth import AuthManager
from src.core.game_state import GameStateManager
from src.gui.auth_screens import LoginScreen, RegisterScreen
from src.gui.menu_screen import MenuScreen
from src.gui.profile_screen import ProfileScreen
from src.gui.tutorial_screen import TutorialScreen
from src.gui.challenge_screen import ChallengeScreen
from src.gui.puzzle_screen import PuzzleScreen
from src.gui.analytics_screen import AnalyticsScreen
from src.gui.achievement_screen import AchievementScreen

logger = logging.getLogger(__name__)


class CybersecurityEscapeRoom(QMainWindow):
    """Main application window"""
    
    def __init__(self, db_manager, puzzle_manager):
        """Initialize main window"""
        super().__init__()
        
        # Set up managers
        self.db_manager = db_manager
        self.puzzle_manager = puzzle_manager
        self.auth_manager = AuthManager(db_manager)
        self.game_state = GameStateManager(db_manager)
        
        # Set up window
        self.setWindowTitle("Cybersecurity Escape Room")
        self.setMinimumSize(1024, 768)
        
        # Initialize UI
        self._init_ui()
        self._setup_styles()
        
        # Set window icon if available
        icon_path = os.path.join('assets', 'images', 'app_icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Show login screen by default
        self.goto_login()
    
    def _init_ui(self):
        """Initialize UI components"""
        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create header
        self.header = QFrame()
        self.header.setObjectName("header")
        self.header.setFixedHeight(60)
        self.header_layout = QHBoxLayout(self.header)
        
        # Add logo to header
        self.logo_label = QLabel("CYBERSECURITY ESCAPE ROOM")
        self.logo_label.setObjectName("logo")
        self.header_layout.addWidget(self.logo_label)
        
        # Add spacer to push user info to right
        self.header_layout.addStretch()
        
        # Add user info section (hidden by default)
        self.user_info = QLabel()
        self.user_info.setObjectName("userInfo")
        self.user_info.setVisible(False)
        self.header_layout.addWidget(self.user_info)
        
        # Add logout button (hidden by default)
        self.logout_button = QPushButton("Logout")
        self.logout_button.setObjectName("logoutButton")
        self.logout_button.clicked.connect(self.logout)
        self.logout_button.setVisible(False)
        self.header_layout.addWidget(self.logout_button)
        
        # Add header to main layout
        self.main_layout.addWidget(self.header)
        
        # Create stacked widget for screens
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        
        # Create screens
        self.login_screen = LoginScreen(self)
        self.register_screen = RegisterScreen(self)
        self.menu_screen = MenuScreen(self)
        self.profile_screen = ProfileScreen(self)
        self.tutorial_screen = TutorialScreen(self)
        self.challenge_screen = ChallengeScreen(self)
        self.puzzle_screen = PuzzleScreen(self)
        self.analytics_screen = AnalyticsScreen(self)
        self.achievement_screen = AchievementScreen(self)
        
        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.register_screen)
        self.stacked_widget.addWidget(self.menu_screen)
        self.stacked_widget.addWidget(self.profile_screen)
        self.stacked_widget.addWidget(self.tutorial_screen)
        self.stacked_widget.addWidget(self.challenge_screen)
        self.stacked_widget.addWidget(self.puzzle_screen)
        self.stacked_widget.addWidget(self.analytics_screen)
        self.stacked_widget.addWidget(self.achievement_screen)
    
    def _setup_styles(self):
        """Set up application styles"""
        # Set application-wide palette
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(18, 18, 18))  # Dark background
        palette.setColor(QPalette.ColorRole.WindowText, QColor(240, 240, 240))  # Light text
        palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))  # Dark widgets
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 45, 45))  # Alternate dark widgets
        palette.setColor(QPalette.ColorRole.Text, QColor(240, 240, 240))  # Light text in widgets
        palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))  # Dark buttons
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(240, 240, 240))  # Light button text
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))  # Blue highlight
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))  # White highlighted text
        QApplication.instance().setPalette(palette)
        
        # Set application stylesheet
        stylesheet = """
            QMainWindow {
                background-color: #121212;
            }
            
            #header {
                background-color: #1e1e1e;
                border-bottom: 1px solid #333;
            }
            
            #logo {
                color: #00ff99;
                font-size: 18px;
                font-weight: bold;
            }
            
            #userInfo {
                color: #f0f0f0;
                margin-right: 10px;
            }
            
            #logoutButton {
                background-color: #333;
                color: #f0f0f0;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 5px 10px;
            }
            
            #logoutButton:hover {
                background-color: #444;
                border: 1px solid #666;
            }
            
            QPushButton {
                background-color: #333;
                color: #f0f0f0;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 100px;
            }
            
            QPushButton:hover {
                background-color: #444;
                border: 1px solid #666;
            }
            
            QPushButton:pressed {
                background-color: #222;
            }
            
            QPushButton.primary {
                background-color: #0059b3;
                border: 1px solid #0066cc;
            }
            
            QPushButton.primary:hover {
                background-color: #0066cc;
                border: 1px solid #0073e6;
            }
            
            QPushButton.success {
                background-color: #00802b;
                border: 1px solid #009933;
            }
            
            QPushButton.success:hover {
                background-color: #009933;
                border: 1px solid #00b33c;
            }
            
            QPushButton.danger {
                background-color: #b30000;
                border: 1px solid #cc0000;
            }
            
            QPushButton.danger:hover {
                background-color: #cc0000;
                border: 1px solid #ff0000;
            }
            
            QLineEdit, QTextEdit, QComboBox {
                background-color: #2a2a2a;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 6px;
                color: #f0f0f0;
            }
            
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 1px solid #0073e6;
            }
            
            QLabel {
                color: #f0f0f0;
            }
            
            QLabel.heading {
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            
            QLabel.subheading {
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            
            QProgressBar {
                border: 1px solid #555;
                border-radius: 4px;
                background-color: #2a2a2a;
                text-align: center;
                height: 20px;
            }
            
            QProgressBar::chunk {
                background-color: #0073e6;
                width: 10px;
            }
            
            QTabWidget::pane {
                border: 1px solid #555;
                background-color: #1e1e1e;
            }
            
            QTabBar::tab {
                background-color: #2a2a2a;
                color: #f0f0f0;
                border: 1px solid #555;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 6px 12px;
                margin-right: 2px;
            }
            
            QTabBar::tab:selected {
                background-color: #1e1e1e;
                border-bottom: 1px solid #1e1e1e;
            }
            
            QTabBar::tab:hover {
                background-color: #333;
            }
            
            QScrollBar:vertical {
                border: none;
                background: #2a2a2a;
                width: 10px;
                margin: 0;
            }
            
            QScrollBar::handle:vertical {
                background: #555;
                min-height: 20px;
                border-radius: 5px;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0;
            }
        """
        self.setStyleSheet(stylesheet)
    
    def goto_login(self):
        """Show login screen"""
        self.stacked_widget.setCurrentWidget(self.login_screen)
        self.user_info.setVisible(False)
        self.logout_button.setVisible(False)
    
    def goto_register(self):
        """Show register screen"""
        self.stacked_widget.setCurrentWidget(self.register_screen)
        self.user_info.setVisible(False)
        self.logout_button.setVisible(False)
    
    def goto_menu(self):
        """Show menu screen"""
        self.menu_screen.refresh()
        self.stacked_widget.setCurrentWidget(self.menu_screen)
        self._update_user_info()
    
    def goto_profile(self):
        """Show profile screen"""
        self.profile_screen.refresh()
        self.stacked_widget.setCurrentWidget(self.profile_screen)
        self._update_user_info()
    
    def goto_tutorial(self):
        """Show tutorial screen"""
        self.tutorial_screen.refresh()
        self.stacked_widget.setCurrentWidget(self.tutorial_screen)
        self._update_user_info()
    
    def goto_challenges(self):
        """Show challenge selection screen"""
        self.challenge_screen.refresh()
        self.stacked_widget.setCurrentWidget(self.challenge_screen)
        self._update_user_info()
    
    def start_puzzle(self, puzzle_id):
        """Start a specific puzzle"""
        # Get the puzzle data from puzzle manager instead of database
        puzzle_data = self.puzzle_manager.get_puzzle_by_id(puzzle_id)
        
        if puzzle_data:
            self.puzzle_screen.set_puzzle(puzzle_id, puzzle_data)
            self.stacked_widget.setCurrentWidget(self.puzzle_screen)
            self._update_user_info()
        else:
            QMessageBox.warning(self, "Puzzle Not Found", f"Could not find puzzle with ID {puzzle_id}")
    
    def goto_analytics(self):
        """Show analytics screen"""
        self.analytics_screen.refresh()
        self.stacked_widget.setCurrentWidget(self.analytics_screen)
        self._update_user_info()
    
    def goto_achievements(self):
        """Show achievements screen"""
        self.achievement_screen.refresh()
        self.stacked_widget.setCurrentWidget(self.achievement_screen)
        self._update_user_info()
    
    def login(self, username_or_email, password):
        """Login user"""
        success, result = self.auth_manager.login_user(username_or_email, password)
        if success:
            user_id = result
            self.game_state.set_user(user_id)
            logger.info(f"User logged in successfully: {username_or_email}")
            self.goto_menu()
        else:
            message = result
            QMessageBox.warning(self, "Login Failed", message)
    
    def register(self, username, email, password, display_name=None):
        """Register new user"""
        success, message = self.auth_manager.register_user(username, email, password, display_name)
        if success:
            QMessageBox.information(self, "Registration Successful", 
                                   "Account created successfully! You can now log in.")
            self.goto_login()
        else:
            QMessageBox.warning(self, "Registration Failed", message)
    
    def logout(self):
        """Logout current user"""
        self.game_state.set_user(None)
        self.goto_login()
    
    def _update_user_info(self):
        """Update user info in header"""
        profile = self.game_state.get_user_profile()
        if profile:
            display_name = profile.get('display_name', profile.get('username', ''))
            points = profile.get('total_points', 0)
            self.user_info.setText(f"{display_name} | Points: {points}")
            self.user_info.setVisible(True)
            self.logout_button.setVisible(True)
        else:
            self.user_info.setVisible(False)
            self.logout_button.setVisible(False) 