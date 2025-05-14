#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Login screen for Cybersecurity Escape Room
Handles user authentication
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QFrame, QGridLayout,
                            QSpacerItem, QSizePolicy, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont

from ..utils.animation_effects import FlickerEffect, CyberDoorTransition


class LoginScreen(QWidget):
    """Login screen for user authentication"""
    
    # Signals
    login_successful = pyqtSignal(str)  # Emitted when login is successful with username
    signup_requested = pyqtSignal()    # Emitted when signup button is clicked
    
    def __init__(self, parent=None):
        """
        Initialize login screen
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        self._create_ui()
        self._connect_signals()
        self._apply_styles()
        self._apply_animations()
    
    def _create_ui(self):
        """Create the login UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(50, 50, 50, 50)
        
        # Title
        title_frame = QFrame()
        title_frame.setObjectName("titleFrame")
        title_layout = QVBoxLayout(title_frame)
        
        self.title_label = QLabel("CYBERSECURITY ESCAPE ROOM")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setObjectName("titleLabel")
        title_layout.addWidget(self.title_label)
        
        self.subtitle_label = QLabel("LOGIN TO CONTINUE")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setObjectName("subtitleLabel")
        title_layout.addWidget(self.subtitle_label)
        
        main_layout.addWidget(title_frame)
        
        # Spacer
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Login form
        form_frame = QFrame()
        form_frame.setObjectName("formFrame")
        form_layout = QGridLayout(form_frame)
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(10)
        
        # Username
        username_label = QLabel("USERNAME:")
        username_label.setObjectName("formLabel")
        form_layout.addWidget(username_label, 0, 0)
        
        self.username_input = QLineEdit()
        self.username_input.setObjectName("inputField")
        self.username_input.setPlaceholderText("Enter your username")
        form_layout.addWidget(self.username_input, 0, 1)
        
        # Password
        password_label = QLabel("PASSWORD:")
        password_label.setObjectName("formLabel")
        form_layout.addWidget(password_label, 1, 0)
        
        self.password_input = QLineEdit()
        self.password_input.setObjectName("inputField")
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(self.password_input, 1, 1)
        
        main_layout.addWidget(form_frame)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.signup_button = QPushButton("SIGN UP")
        self.signup_button.setObjectName("secondaryButton")
        button_layout.addWidget(self.signup_button)
        
        self.login_button = QPushButton("LOGIN")
        self.login_button.setObjectName("primaryButton")
        button_layout.addWidget(self.login_button)
        
        main_layout.addLayout(button_layout)
        
        # Spacer
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Copyright
        self.copyright_label = QLabel("© 2023 Cybersecurity Escape Room")
        self.copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.copyright_label.setObjectName("copyrightLabel")
        main_layout.addWidget(self.copyright_label)
    
    def _connect_signals(self):
        """Connect signals to slots"""
        self.login_button.clicked.connect(self._on_login_clicked)
        self.signup_button.clicked.connect(self.signup_requested.emit)
        self.password_input.returnPressed.connect(self._on_login_clicked)
        self.username_input.returnPressed.connect(lambda: self.password_input.setFocus())
    
    def _apply_styles(self):
        """Apply styles to the login screen"""
        self.setStyleSheet("""
            #titleLabel {
                font-size: 32px;
                font-weight: bold;
                color: #00ccff;
                margin-bottom: 10px;
            }
            
            #subtitleLabel {
                font-size: 18px;
                color: #cccccc;
                margin-bottom: 20px;
            }
            
            #formFrame {
                background-color: rgba(0, 0, 0, 0.3);
                border-radius: 10px;
                padding: 20px;
                border: 1px solid #333333;
            }
            
            #formLabel {
                font-size: 14px;
                color: #00ccff;
                font-weight: bold;
            }
            
            #inputField {
                background-color: rgba(0, 0, 0, 0.5);
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                min-width: 250px;
            }
            
            #inputField:focus {
                border: 1px solid #00ccff;
            }
            
            #primaryButton {
                background-color: #00ccff;
                color: #000000;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            
            #primaryButton:hover {
                background-color: #33d6ff;
            }
            
            #primaryButton:pressed {
                background-color: #0099cc;
            }
            
            #secondaryButton {
                background-color: transparent;
                color: #00ccff;
                border: 1px solid #00ccff;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            
            #secondaryButton:hover {
                background-color: rgba(0, 204, 255, 0.1);
            }
            
            #secondaryButton:pressed {
                background-color: rgba(0, 204, 255, 0.2);
            }
            
            #copyrightLabel {
                color: #777777;
                font-size: 12px;
            }
        """)
    
    def _apply_animations(self):
        """Apply animations to login screen elements"""
        # Flicker effect on title
        self.title_flicker = FlickerEffect(
            self.title_label, 
            color="#00ccff", 
            intensity=0.2,
            interval_range=(2000, 5000)
        )
        self.title_flicker.start()
    
    def _on_login_clicked(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username:
            QMessageBox.warning(self, "Login Error", "Please enter a username")
            self.username_input.setFocus()
            return
        
        if not password:
            QMessageBox.warning(self, "Login Error", "Please enter a password")
            self.password_input.setFocus()
            return
        
        # In a real application, verify credentials against database
        # For this example, we'll just emit the login successful signal
        # You would replace this with actual authentication logic
        
        # Clear any current input
        self.clear_inputs()
        
        # Emit signal with username
        self.login_successful.emit(username)
    
    def set_error_message(self, message):
        """
        Display an error message
        
        Args:
            message: Error message to display
        """
        QMessageBox.warning(self, "Login Error", message)
    
    def clear_inputs(self):
        """Clear all input fields"""
        self.username_input.clear()
        self.password_input.clear()
        self.username_input.setFocus() 