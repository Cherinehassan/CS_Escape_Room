#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Signup screen for Cybersecurity Escape Room
Handles user registration
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QFrame, QGridLayout,
                            QSpacerItem, QSizePolicy, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont

from ..utils.animation_effects import FlickerEffect, CyberDoorTransition


class SignupScreen(QWidget):
    """Signup screen for user registration"""
    
    # Signals
    signup_successful = pyqtSignal(str)  # Emitted when signup is successful with username
    login_requested = pyqtSignal()      # Emitted when login button is clicked
    
    def __init__(self, parent=None):
        """
        Initialize signup screen
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        self._create_ui()
        self._connect_signals()
        self._apply_styles()
        self._apply_animations()
    
    def _create_ui(self):
        """Create the signup UI"""
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
        
        self.subtitle_label = QLabel("CREATE NEW ACCOUNT")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setObjectName("subtitleLabel")
        title_layout.addWidget(self.subtitle_label)
        
        main_layout.addWidget(title_frame)
        
        # Spacer
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Signup form
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
        self.username_input.setPlaceholderText("Choose a username")
        form_layout.addWidget(self.username_input, 0, 1)
        
        # Email
        email_label = QLabel("EMAIL:")
        email_label.setObjectName("formLabel")
        form_layout.addWidget(email_label, 1, 0)
        
        self.email_input = QLineEdit()
        self.email_input.setObjectName("inputField")
        self.email_input.setPlaceholderText("Enter your email")
        form_layout.addWidget(self.email_input, 1, 1)
        
        # Password
        password_label = QLabel("PASSWORD:")
        password_label.setObjectName("formLabel")
        form_layout.addWidget(password_label, 2, 0)
        
        self.password_input = QLineEdit()
        self.password_input.setObjectName("inputField")
        self.password_input.setPlaceholderText("Create a password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(self.password_input, 2, 1)
        
        # Confirm Password
        confirm_label = QLabel("CONFIRM PASSWORD:")
        confirm_label.setObjectName("formLabel")
        form_layout.addWidget(confirm_label, 3, 0)
        
        self.confirm_input = QLineEdit()
        self.confirm_input.setObjectName("inputField")
        self.confirm_input.setPlaceholderText("Confirm your password")
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(self.confirm_input, 3, 1)
        
        main_layout.addWidget(form_frame)
        
        # Password hint
        self.password_hint = QLabel("Password must be at least 8 characters long and include uppercase, lowercase, numbers and special characters")
        self.password_hint.setObjectName("hintLabel")
        self.password_hint.setWordWrap(True)
        self.password_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.password_hint)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.login_button = QPushButton("BACK TO LOGIN")
        self.login_button.setObjectName("secondaryButton")
        button_layout.addWidget(self.login_button)
        
        self.signup_button = QPushButton("CREATE ACCOUNT")
        self.signup_button.setObjectName("primaryButton")
        button_layout.addWidget(self.signup_button)
        
        main_layout.addLayout(button_layout)
        
        # Spacer
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Copyright
        self.copyright_label = QLabel("© 2023 Cybersecurity Escape Room")
        self.copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.copyright_label.setObjectName("copyrightLabel")
        main_layout.addWidget(self.copyright_label)
    
    def _connect_signals(self):
        """Connect signals to slots"""
        self.signup_button.clicked.connect(self._on_signup_clicked)
        self.login_button.clicked.connect(self.login_requested.emit)
        
        # Enter key handling
        self.username_input.returnPressed.connect(lambda: self.email_input.setFocus())
        self.email_input.returnPressed.connect(lambda: self.password_input.setFocus())
        self.password_input.returnPressed.connect(lambda: self.confirm_input.setFocus())
        self.confirm_input.returnPressed.connect(self._on_signup_clicked)
    
    def _apply_styles(self):
        """Apply styles to the signup screen"""
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
            
            #hintLabel {
                font-size: 12px;
                color: #999999;
                margin-top: 5px;
                margin-bottom: 15px;
            }
            
            #primaryButton {
                background-color: #00ccff;
                color: #000000;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 160px;
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
                min-width: 160px;
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
        """Apply animations to signup screen elements"""
        # Flicker effect on title
        self.title_flicker = FlickerEffect(
            self.title_label, 
            color="#00ccff", 
            intensity=0.2,
            interval_range=(2000, 5000)
        )
        self.title_flicker.start()
    
    def _on_signup_clicked(self):
        """Handle signup button click"""
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        # Validate inputs
        if not username:
            QMessageBox.warning(self, "Signup Error", "Please enter a username")
            self.username_input.setFocus()
            return
        
        if not email:
            QMessageBox.warning(self, "Signup Error", "Please enter an email address")
            self.email_input.setFocus()
            return
        
        if '@' not in email or '.' not in email:
            QMessageBox.warning(self, "Signup Error", "Please enter a valid email address")
            self.email_input.setFocus()
            return
        
        if not password:
            QMessageBox.warning(self, "Signup Error", "Please create a password")
            self.password_input.setFocus()
            return
        
        if len(password) < 8:
            QMessageBox.warning(self, "Signup Error", "Password must be at least 8 characters long")
            self.password_input.setFocus()
            return
        
        # Check password complexity (this is a simple check, you might want more sophisticated validation)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        if not (has_upper and has_lower and has_digit and has_special):
            QMessageBox.warning(self, "Signup Error", 
                             "Password must include uppercase, lowercase, numbers, and special characters")
            self.password_input.setFocus()
            return
        
        if password != confirm:
            QMessageBox.warning(self, "Signup Error", "Passwords do not match")
            self.confirm_input.setFocus()
            return
        
        # In a real application, create a new user in the database
        # For this example, we'll just emit the signup successful signal
        # You would replace this with actual user creation logic
        self.signup_successful.emit(username)
    
    def set_error_message(self, message):
        """
        Display an error message
        
        Args:
            message: Error message to display
        """
        QMessageBox.warning(self, "Signup Error", message)
    
    def clear_inputs(self):
        """Clear all input fields"""
        self.username_input.clear()
        self.email_input.clear()
        self.password_input.clear()
        self.confirm_input.clear()
        self.username_input.setFocus() 