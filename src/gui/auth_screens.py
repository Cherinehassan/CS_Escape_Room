#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Authentication screens for Cybersecurity Escape Room
Includes login and registration interfaces
"""

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFormLayout, QFrame, QCheckBox, QSpacerItem,
    QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont

logger = logging.getLogger(__name__)


class LoginScreen(QWidget):
    """Login screen for user authentication"""
    
    def __init__(self, main_window):
        """Initialize login screen"""
        super().__init__()
        self.main_window = main_window
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Content container with proper margins
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(50, 50, 50, 50)
        content_layout.setSpacing(20)
        main_layout.addWidget(content_container)
        
        # Create centered content
        center_widget = QWidget()
        center_layout = QHBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add spacer on left
        center_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Create login form container
        login_container = QFrame()
        login_container.setObjectName("loginContainer")
        login_container.setMinimumWidth(400)
        login_container.setMaximumWidth(450)
        login_layout = QVBoxLayout(login_container)
        login_layout.setSpacing(15)
        
        # Add title
        title_label = QLabel("Login to Cybersecurity Escape Room")
        title_label.setObjectName("loginTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        login_layout.addWidget(title_label)
        
        # Add subtitle
        subtitle_label = QLabel("Enter your credentials to continue your cybersecurity journey")
        subtitle_label.setObjectName("loginSubtitle")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setWordWrap(True)
        login_layout.addWidget(subtitle_label)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        login_layout.addWidget(separator)
        
        # Create form layout
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        
        # Username/Email field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username or Email")
        form_layout.addRow("Username/Email:", self.username_input)
        
        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Password:", self.password_input)
        
        # Add form to login layout
        login_layout.addLayout(form_layout)
        
        # Remember me checkbox
        remember_layout = QHBoxLayout()
        self.remember_checkbox = QCheckBox("Remember me")
        remember_layout.addWidget(self.remember_checkbox)
        remember_layout.addStretch()
        login_layout.addLayout(remember_layout)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setObjectName("loginButton")
        self.login_button.setProperty("class", "primary")
        self.login_button.clicked.connect(self.login)
        login_layout.addWidget(self.login_button)
        
        # Register link
        register_layout = QHBoxLayout()
        register_label = QLabel("Don't have an account?")
        self.register_button = QPushButton("Register")
        self.register_button.setObjectName("registerLink")
        self.register_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_button.clicked.connect(self.goto_register)
        register_layout.addWidget(register_label)
        register_layout.addWidget(self.register_button)
        register_layout.addStretch()
        login_layout.addLayout(register_layout)
        
        # Add the login container to the center
        center_layout.addWidget(login_container)
        
        # Add right graphic/banner (if desired)
        graphic_container = QLabel()
        graphic_container.setObjectName("loginGraphic")
        graphic_container.setMinimumWidth(400)
        graphic_container.setMaximumWidth(600)
        
        # Set image if available
        banner_path = "assets/images/login_banner.png"
        try:
            pixmap = QPixmap(banner_path)
            if not pixmap.isNull():
                graphic_container.setPixmap(pixmap.scaled(graphic_container.size(), 
                                                          Qt.AspectRatioMode.KeepAspectRatio, 
                                                          Qt.TransformationMode.SmoothTransformation))
                graphic_container.setScaledContents(True)
            else:
                # If image not available, show text instead
                graphic_container.setText("CYBERSECURITY\nESCAPE ROOM")
                graphic_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
                graphic_container.setStyleSheet("font-size: 24px; color: #00ff99; background-color: #333;")
        except Exception as e:
            logger.warning(f"Could not load login banner image: {e}")
            # Show text instead
            graphic_container.setText("CYBERSECURITY\nESCAPE ROOM")
            graphic_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
            graphic_container.setStyleSheet("font-size: 24px; color: #00ff99; background-color: #333;")
        
        center_layout.addWidget(graphic_container)
        
        # Add spacer on right
        center_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Add centered content to main layout
        content_layout.addWidget(center_widget)
        content_layout.addStretch()
        
        # Set styles
        self.setStyleSheet("""
            #loginContainer {
                background-color: #1e1e1e;
                border-radius: 8px;
                padding: 20px;
            }
            
            #loginTitle {
                font-size: 22px;
                font-weight: bold;
                color: #00ff99;
            }
            
            #loginSubtitle {
                font-size: 14px;
                color: #aaa;
            }
            
            #loginButton {
                height: 40px;
                font-size: 16px;
                font-weight: bold;
            }
            
            #registerLink {
                background: transparent;
                border: none;
                color: #0099ff;
                text-decoration: underline;
                font-weight: bold;
                padding: 0px;
                min-width: 0px;
            }
            
            #registerLink:hover {
                color: #00ccff;
            }
        """)
    
    def login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            return
        
        self.main_window.login(username, password)
    
    def goto_register(self):
        """Switch to registration screen"""
        self.main_window.goto_register()


class RegisterScreen(QWidget):
    """Registration screen for new users"""
    
    def __init__(self, main_window):
        """Initialize registration screen"""
        super().__init__()
        self.main_window = main_window
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Content container with proper margins
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(50, 50, 50, 50)
        content_layout.setSpacing(20)
        main_layout.addWidget(content_container)
        
        # Create centered content
        center_widget = QWidget()
        center_layout = QHBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add spacer on left
        center_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Create registration form container
        register_container = QFrame()
        register_container.setObjectName("registerContainer")
        register_container.setMinimumWidth(500)
        register_container.setMaximumWidth(600)
        register_layout = QVBoxLayout(register_container)
        register_layout.setSpacing(15)
        
        # Add title
        title_label = QLabel("Create Account")
        title_label.setObjectName("registerTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        register_layout.addWidget(title_label)
        
        # Add subtitle
        subtitle_label = QLabel("Join our cybersecurity training platform and start your learning journey")
        subtitle_label.setObjectName("registerSubtitle")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setWordWrap(True)
        register_layout.addWidget(subtitle_label)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        register_layout.addWidget(separator)
        
        # Create form layout
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        
        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a unique username (letters, numbers, underscores)")
        form_layout.addRow("Username:", self.username_input)
        
        # Display name field
        self.display_name_input = QLineEdit()
        self.display_name_input.setPlaceholderText("Your display name (optional)")
        form_layout.addRow("Display Name:", self.display_name_input)
        
        # Email field
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Your email address")
        form_layout.addRow("Email:", self.email_input)
        
        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Choose a secure password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Password:", self.password_input)
        
        # Confirm password field
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm your password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Confirm Password:", self.confirm_password_input)
        
        # Add form to register layout
        register_layout.addLayout(form_layout)
        
        # Password requirements note
        password_note = QLabel("Password must be at least 8 characters with at least one uppercase letter, one lowercase letter, and one number")
        password_note.setObjectName("passwordNote")
        password_note.setWordWrap(True)
        register_layout.addWidget(password_note)
        
        # Terms checkbox
        terms_layout = QHBoxLayout()
        self.terms_checkbox = QCheckBox("I agree to the Terms and Conditions")
        terms_layout.addWidget(self.terms_checkbox)
        terms_layout.addStretch()
        register_layout.addLayout(terms_layout)
        
        # Register button
        self.register_button = QPushButton("Create Account")
        self.register_button.setObjectName("registerButton")
        self.register_button.setProperty("class", "primary")
        self.register_button.clicked.connect(self.register)
        register_layout.addWidget(self.register_button)
        
        # Login link
        login_layout = QHBoxLayout()
        login_label = QLabel("Already have an account?")
        self.login_button = QPushButton("Login")
        self.login_button.setObjectName("loginLink")
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.clicked.connect(self.goto_login)
        login_layout.addWidget(login_label)
        login_layout.addWidget(self.login_button)
        login_layout.addStretch()
        register_layout.addLayout(login_layout)
        
        # Add the register container to the center
        center_layout.addWidget(register_container)
        
        # Add spacer on right
        center_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Add centered content to main layout
        content_layout.addWidget(center_widget)
        content_layout.addStretch()
        
        # Set styles
        self.setStyleSheet("""
            #registerContainer {
                background-color: #1e1e1e;
                border-radius: 8px;
                padding: 20px;
            }
            
            #registerTitle {
                font-size: 22px;
                font-weight: bold;
                color: #00ff99;
            }
            
            #registerSubtitle {
                font-size: 14px;
                color: #aaa;
            }
            
            #passwordNote {
                font-size: 12px;
                color: #888;
                font-style: italic;
            }
            
            #registerButton {
                height: 40px;
                font-size: 16px;
                font-weight: bold;
            }
            
            #loginLink {
                background: transparent;
                border: none;
                color: #0099ff;
                text-decoration: underline;
                font-weight: bold;
                padding: 0px;
                min-width: 0px;
            }
            
            #loginLink:hover {
                color: #00ccff;
            }
        """)
    
    def register(self):
        """Handle registration button click"""
        username = self.username_input.text().strip()
        display_name = self.display_name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        terms_accepted = self.terms_checkbox.isChecked()
        
        # Basic validation
        if not username or not email or not password:
            logger.warning("Registration failed: Missing required fields")
            return
        
        # Check if passwords match
        if password != confirm_password:
            logger.warning("Registration failed: Passwords don't match")
            return
        
        # Check terms acceptance
        if not terms_accepted:
            logger.warning("Registration failed: Terms not accepted")
            return
        
        # Use display name only if provided
        if not display_name:
            display_name = None
        
        # Attempt registration
        self.main_window.register(username, email, password, display_name)
    
    def goto_login(self):
        """Switch to login screen"""
        self.main_window.goto_login() 