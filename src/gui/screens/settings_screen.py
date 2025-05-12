#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Settings screen for Cybersecurity Escape Room
Allows users to customize their experience
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QGridLayout, QSpacerItem,
                            QSizePolicy, QSlider, QCheckBox, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont

from ..utils.animation_effects import FlickerEffect


class SettingsScreen(QWidget):
    """Settings screen for game customization"""
    
    # Signals
    settings_saved = pyqtSignal(dict)  # Emitted when settings are saved
    return_to_menu = pyqtSignal()      # Emitted when back button is clicked
    
    def __init__(self, parent=None):
        """
        Initialize settings screen
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Default settings
        self.settings = {
            "difficulty": "medium",
            "dark_mode": True,
            "animations_enabled": True,
            "fullscreen": False,
            "hint_system": True
        }
        
        self._create_ui()
        self._connect_signals()
        self._apply_styles()
        self._apply_animations()
        
        # Load settings (will be implemented with actual settings persistence)
        self._load_settings()
    
    def _create_ui(self):
        """Create the settings UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(50, 50, 50, 50)
        
        # Title
        title_frame = QFrame()
        title_frame.setObjectName("titleFrame")
        title_layout = QVBoxLayout(title_frame)
        
        self.title_label = QLabel("SETTINGS")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setObjectName("titleLabel")
        title_layout.addWidget(self.title_label)
        
        self.subtitle_label = QLabel("Customize your escape room experience")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setObjectName("subtitleLabel")
        title_layout.addWidget(self.subtitle_label)
        
        main_layout.addWidget(title_frame)
        
        # Settings container
        settings_frame = QFrame()
        settings_frame.setObjectName("settingsFrame")
        settings_layout = QGridLayout(settings_frame)
        settings_layout.setVerticalSpacing(20)
        settings_layout.setHorizontalSpacing(15)
        settings_layout.setContentsMargins(25, 25, 25, 25)
        
        # Game settings section
        game_label = QLabel("GAME SETTINGS")
        game_label.setObjectName("sectionLabel")
        settings_layout.addWidget(game_label, 0, 0, 1, 2)
        
        # Difficulty
        difficulty_label = QLabel("Difficulty Level:")
        difficulty_label.setObjectName("settingLabel")
        settings_layout.addWidget(difficulty_label, 1, 0)
        
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Easy", "Medium", "Hard"])
        self.difficulty_combo.setCurrentText("Medium")
        self.difficulty_combo.setObjectName("difficultyCombo")
        settings_layout.addWidget(self.difficulty_combo, 1, 1)
        
        # Hint system
        hint_label = QLabel("Hint System:")
        hint_label.setObjectName("settingLabel")
        settings_layout.addWidget(hint_label, 2, 0)
        
        self.hint_check = QCheckBox("Enable hints")
        self.hint_check.setChecked(True)
        self.hint_check.setObjectName("settingCheck")
        settings_layout.addWidget(self.hint_check, 2, 1)
        
        # Display settings section
        display_label = QLabel("DISPLAY SETTINGS")
        display_label.setObjectName("sectionLabel")
        settings_layout.addWidget(display_label, 3, 0, 1, 2)
        
        # Dark mode
        theme_label = QLabel("Dark Mode:")
        theme_label.setObjectName("settingLabel")
        settings_layout.addWidget(theme_label, 4, 0)
        
        self.dark_mode_check = QCheckBox("Enable dark mode")
        self.dark_mode_check.setChecked(True)
        self.dark_mode_check.setObjectName("settingCheck")
        settings_layout.addWidget(self.dark_mode_check, 4, 1)
        
        # Animations
        anim_label = QLabel("Animations:")
        anim_label.setObjectName("settingLabel")
        settings_layout.addWidget(anim_label, 5, 0)
        
        self.animations_check = QCheckBox("Enable animations")
        self.animations_check.setChecked(True)
        self.animations_check.setObjectName("settingCheck")
        settings_layout.addWidget(self.animations_check, 5, 1)
        
        # Fullscreen
        fullscreen_label = QLabel("Fullscreen:")
        fullscreen_label.setObjectName("settingLabel")
        settings_layout.addWidget(fullscreen_label, 6, 0)
        
        self.fullscreen_check = QCheckBox("Enable fullscreen mode")
        self.fullscreen_check.setChecked(False)
        self.fullscreen_check.setObjectName("settingCheck")
        settings_layout.addWidget(self.fullscreen_check, 6, 1)
        
        main_layout.addWidget(settings_frame)
        
        # Button area
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.back_button = QPushButton("CANCEL")
        self.back_button.setObjectName("cancelButton")
        button_layout.addWidget(self.back_button)
        
        button_layout.addStretch()
        
        self.save_button = QPushButton("SAVE SETTINGS")
        self.save_button.setObjectName("saveButton")
        button_layout.addWidget(self.save_button)
        
        main_layout.addLayout(button_layout)
        
        # Add spacer at bottom
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
    
    def _connect_signals(self):
        """Connect signals to slots"""
        self.back_button.clicked.connect(self.return_to_menu.emit)
        self.save_button.clicked.connect(self._save_settings)
    
    def _apply_styles(self):
        """Apply styles to the settings screen"""
        self.setStyleSheet("""
            #titleLabel {
                font-size: 36px;
                font-weight: bold;
                color: #00ccff;
                margin-bottom: 10px;
            }
            
            #subtitleLabel {
                font-size: 18px;
                color: #cccccc;
                margin-bottom: 20px;
            }
            
            #settingsFrame {
                background-color: rgba(0, 0, 0, 0.3);
                border-radius: 10px;
                border: 1px solid #333333;
            }
            
            #sectionLabel {
                font-size: 16px;
                font-weight: bold;
                color: #00ccff;
                margin-top: 10px;
                border-bottom: 1px solid #555555;
                padding-bottom: 5px;
            }
            
            #settingLabel {
                font-size: 14px;
                color: #cccccc;
            }
            
            QComboBox {
                background-color: rgba(0, 0, 0, 0.5);
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px;
                min-width: 150px;
            }
            
            QComboBox::drop-down {
                border-left: 1px solid #555555;
                width: 20px;
            }
            
            QComboBox:hover {
                border: 1px solid #00ccff;
            }
            
            QComboBox QAbstractItemView {
                background-color: rgba(10, 10, 10, 0.9);
                color: #ffffff;
                selection-background-color: #00ccff;
                selection-color: #000000;
                border: 1px solid #555555;
            }
            
            QCheckBox {
                color: #ffffff;
                spacing: 5px;
            }
            
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
            }
            
            QCheckBox::indicator:unchecked {
                background-color: rgba(0, 0, 0, 0.5);
                border: 1px solid #555555;
                border-radius: 3px;
            }
            
            QCheckBox::indicator:checked {
                background-color: #00ccff;
                border: 1px solid #00ccff;
                border-radius: 3px;
            }
            
            #saveButton {
                background-color: #00ccff;
                color: #000000;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            
            #saveButton:hover {
                background-color: #33d6ff;
            }
            
            #saveButton:pressed {
                background-color: #0099cc;
            }
            
            #cancelButton {
                background-color: transparent;
                color: #cccccc;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            
            #cancelButton:hover {
                color: #ffffff;
                border-color: #777777;
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
    
    def _apply_animations(self):
        """Apply animations to elements"""
        # Flicker effect on title
        self.title_flicker = FlickerEffect(
            self.title_label, 
            color="#00ccff", 
            intensity=0.2,
            interval_range=(2000, 5000)
        )
        self.title_flicker.start()
    
    def _load_settings(self):
        """Load settings from storage (placeholder for now)"""
        # Update UI with current settings
        self.difficulty_combo.setCurrentText(self.settings["difficulty"].capitalize())
        self.dark_mode_check.setChecked(self.settings["dark_mode"])
        self.animations_check.setChecked(self.settings["animations_enabled"])
        self.fullscreen_check.setChecked(self.settings["fullscreen"])
        self.hint_check.setChecked(self.settings["hint_system"])
    
    def _save_settings(self):
        """Save settings and emit signal"""
        # Update settings from UI
        self.settings["difficulty"] = self.difficulty_combo.currentText().lower()
        self.settings["dark_mode"] = self.dark_mode_check.isChecked()
        self.settings["animations_enabled"] = self.animations_check.isChecked()
        self.settings["fullscreen"] = self.fullscreen_check.isChecked()
        self.settings["hint_system"] = self.hint_check.isChecked()
        
        # Emit signal with settings
        self.settings_saved.emit(self.settings)
        
        # Return to menu
        self.return_to_menu.emit()
    
    def update_settings(self, settings):
        """
        Update settings from external source
        
        Args:
            settings: Dictionary of settings
        """
        self.settings.update(settings)
        self._load_settings() 