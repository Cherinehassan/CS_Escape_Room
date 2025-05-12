#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Profile screen for Cybersecurity Escape Room
"""

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QLineEdit, QFormLayout, QStackedWidget
)
from PyQt6.QtCore import Qt

logger = logging.getLogger(__name__)


class ProfileScreen(QWidget):
    """User profile screen"""
    
    def __init__(self, main_window):
        """Initialize profile screen"""
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
        title_label = QLabel("Your Profile")
        title_label.setObjectName("screenTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Profile content container
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_layout = QVBoxLayout(content_frame)
        
        # Stacked widget for view/edit modes
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget)
        
        # Create view mode widget
        view_widget = QWidget()
        view_layout = QVBoxLayout(view_widget)
        
        # User info section
        info_frame = QFrame()
        info_frame.setObjectName("profileInfoFrame")
        info_layout = QFormLayout(info_frame)
        
        self.username_label = QLabel()
        info_layout.addRow(QLabel("Username:"), self.username_label)
        
        self.display_name_label = QLabel()
        info_layout.addRow(QLabel("Display Name:"), self.display_name_label)
        
        self.email_label = QLabel()
        info_layout.addRow(QLabel("Email:"), self.email_label)
        
        self.joined_label = QLabel()
        info_layout.addRow(QLabel("Joined:"), self.joined_label)
        
        self.last_login_label = QLabel()
        info_layout.addRow(QLabel("Last Login:"), self.last_login_label)
        
        view_layout.addWidget(info_frame)
        
        # Stats section
        stats_frame = QFrame()
        stats_frame.setObjectName("profileStatsFrame")
        stats_layout = QFormLayout(stats_frame)
        
        self.points_label = QLabel()
        stats_layout.addRow(QLabel("Total Points:"), self.points_label)
        
        self.current_streak_label = QLabel()
        stats_layout.addRow(QLabel("Current Streak:"), self.current_streak_label)
        
        self.highest_streak_label = QLabel()
        stats_layout.addRow(QLabel("Highest Streak:"), self.highest_streak_label)
        
        self.puzzles_solved_label = QLabel()
        stats_layout.addRow(QLabel("Puzzles Solved:"), self.puzzles_solved_label)
        
        view_layout.addWidget(stats_frame)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        edit_profile_button = QPushButton("Edit Profile")
        edit_profile_button.setObjectName("editProfileButton")
        edit_profile_button.clicked.connect(self.toggle_edit_mode)
        buttons_layout.addWidget(edit_profile_button)
        
        change_password_button = QPushButton("Change Password")
        change_password_button.setObjectName("changePasswordButton")
        change_password_button.clicked.connect(self.show_change_password)
        buttons_layout.addWidget(change_password_button)
        
        buttons_layout.addStretch()
        view_layout.addLayout(buttons_layout)
        
        # Add view mode to stacked widget
        self.stacked_widget.addWidget(view_widget)
        
        # Create edit mode widget (placeholder for now)
        edit_widget = QWidget()
        edit_layout = QVBoxLayout(edit_widget)
        edit_layout.addWidget(QLabel("Edit profile form will go here"))
        
        # Cancel and save buttons for edit mode
        edit_buttons = QHBoxLayout()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel_edit)
        edit_buttons.addWidget(cancel_button)
        
        save_button = QPushButton("Save Changes")
        save_button.setProperty("class", "primary")
        save_button.clicked.connect(self.save_profile)
        edit_buttons.addWidget(save_button)
        
        edit_layout.addLayout(edit_buttons)
        
        # Add edit mode to stacked widget
        self.stacked_widget.addWidget(edit_widget)
        
        # Add content frame to main layout
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
            
            #profileInfoFrame, #profileStatsFrame {
                background-color: #262626;
                border-radius: 6px;
                padding: 15px;
                margin-bottom: 20px;
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
        """Update profile data"""
        profile = self.main_window.game_state.get_user_profile()
        if not profile:
            return
        
        # Update profile information labels
        self.username_label.setText(profile.get('username', 'N/A'))
        self.display_name_label.setText(profile.get('display_name', 'N/A'))
        self.email_label.setText(profile.get('email', 'N/A'))
        
        # Format dates
        joined_date = profile.get('created_at')
        if joined_date:
            self.joined_label.setText(joined_date.strftime('%Y-%m-%d'))
        else:
            self.joined_label.setText('N/A')
        
        last_login = profile.get('last_login')
        if last_login:
            self.last_login_label.setText(last_login.strftime('%Y-%m-%d %H:%M'))
        else:
            self.last_login_label.setText('N/A')
        
        # Update stats
        self.points_label.setText(str(profile.get('total_points', 0)))
        self.current_streak_label.setText(str(profile.get('current_streak', 0)))
        self.highest_streak_label.setText(str(profile.get('highest_streak', 0)))
        
        # Get puzzle completion count
        stats = self.main_window.game_state.get_user_stats()
        self.puzzles_solved_label.setText(str(stats.get('successful_attempts', 0)))
        
        # Reset to view mode
        self.stacked_widget.setCurrentIndex(0)
    
    def toggle_edit_mode(self):
        """Switch to edit profile mode"""
        # In a complete implementation, we would populate form fields here
        self.stacked_widget.setCurrentIndex(1)
    
    def cancel_edit(self):
        """Cancel edit mode and return to view mode"""
        self.stacked_widget.setCurrentIndex(0)
    
    def save_profile(self):
        """Save profile changes"""
        # In a complete implementation, we would save changes to the database here
        self.stacked_widget.setCurrentIndex(0)
        self.refresh()
    
    def show_change_password(self):
        """Show change password dialog"""
        # In a complete implementation, we would show a dialog for changing password
        pass
    
    def goto_menu(self):
        """Return to menu screen"""
        self.main_window.goto_menu() 