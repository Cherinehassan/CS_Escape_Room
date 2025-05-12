#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Theme manager for Cybersecurity Escape Room
Provides styling and theme utilities
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor, QFont


class ThemeManager:
    """Manages application themes and styling"""
    
    # Theme constants
    DARK_CYBER = "dark_cyber"
    TERMINAL = "terminal"
    NEON_HACKER = "neon_hacker"
    
    def __init__(self):
        """Initialize the theme manager"""
        self.current_theme = None
        self.category_colors = {
            "Cryptography": "#42f5a7",      # Neon green
            "Social Engineering": "#f542e0", # Pink
            "Hashing": "#42c5f5",           # Light blue
            "Authentication": "#f5a742",    # Orange
            "Encryption": "#42f5f5"         # Cyan
        }
        
        # Font settings
        self.fonts = {
            "title": QFont("Consolas", 18, QFont.Weight.Bold),
            "heading": QFont("Consolas", 14, QFont.Weight.Bold),
            "normal": QFont("Consolas", 11),
            "code": QFont("Courier New", 10),
            "terminal": QFont("Courier New", 12)
        }
    
    def apply_theme(self, theme=DARK_CYBER):
        """
        Apply a theme to the application
        
        Args:
            theme: Theme identifier
        """
        self.current_theme = theme
        
        if theme == self.DARK_CYBER:
            self._apply_dark_cyber_theme()
        elif theme == self.TERMINAL:
            self._apply_terminal_theme()
        elif theme == self.NEON_HACKER:
            self._apply_neon_hacker_theme()
        else:
            # Default to dark cyber theme
            self._apply_dark_cyber_theme()
    
    def _apply_dark_cyber_theme(self):
        """Apply dark cyber theme"""
        app = QApplication.instance()
        
        # Create a dark palette
        dark_palette = QPalette()
        
        # Set colors
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(18, 18, 18))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(60, 60, 60))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(0, 255, 0))
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(0, 160, 255))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 150, 255))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        # Apply the palette
        app.setPalette(dark_palette)
        
        # Set stylesheet
        stylesheet = """
        QMainWindow, QDialog {
            background-color: #191919;
            color: #dcdcdc;
        }
        
        QWidget {
            background-color: #191919;
            color: #dcdcdc;
        }
        
        QPushButton {
            background-color: #3c3c3c;
            color: #dcdcdc;
            border: 1px solid #0f3460;
            border-radius: 4px;
            padding: 5px 15px;
        }
        
        QPushButton:hover {
            background-color: #4c4c4c;
            border: 1px solid #0f5485;
        }
        
        QPushButton:pressed {
            background-color: #2c2c2c;
        }
        
        QLineEdit, QTextEdit, QPlainTextEdit {
            background-color: #121212;
            color: #dcdcdc;
            border: 1px solid #3c3c3c;
            border-radius: 3px;
            padding: 2px 4px;
        }
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
            border: 1px solid #0f5485;
        }
        
        QLabel {
            color: #dcdcdc;
            font-family: Consolas, Monaco, monospace;
        }
        
        QMenuBar {
            background-color: #191919;
            color: #dcdcdc;
        }
        
        QMenuBar::item:selected {
            background-color: #3c3c3c;
        }
        
        QMenu {
            background-color: #191919;
            color: #dcdcdc;
        }
        
        QMenu::item:selected {
            background-color: #3c3c3c;
        }
        
        QTabWidget::pane {
            border: 1px solid #3c3c3c;
        }
        
        QTabBar::tab {
            background-color: #191919;
            color: #dcdcdc;
            border: 1px solid #3c3c3c;
            padding: 5px 10px;
        }
        
        QTabBar::tab:selected {
            background-color: #3c3c3c;
        }
        
        QScrollBar:vertical {
            background-color: #191919;
            width: 12px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #3c3c3c;
            min-height: 20px;
            border-radius: 3px;
        }
        
        QScrollBar:horizontal {
            background-color: #191919;
            height: 12px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #3c3c3c;
            min-width: 20px;
            border-radius: 3px;
        }
        """
        
        app.setStyleSheet(stylesheet)
    
    def _apply_terminal_theme(self):
        """Apply terminal-like theme"""
        app = QApplication.instance()
        
        # Create a terminal palette
        terminal_palette = QPalette()
        
        # Set colors
        terminal_palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0))
        terminal_palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 255, 0))
        terminal_palette.setColor(QPalette.ColorRole.Base, QColor(0, 0, 0))
        terminal_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(15, 15, 15))
        terminal_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(0, 0, 0))
        terminal_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 255, 0))
        terminal_palette.setColor(QPalette.ColorRole.Text, QColor(0, 255, 0))
        terminal_palette.setColor(QPalette.ColorRole.Button, QColor(25, 25, 25))
        terminal_palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 255, 0))
        terminal_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
        terminal_palette.setColor(QPalette.ColorRole.Link, QColor(0, 160, 255))
        terminal_palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 100, 0))
        terminal_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 255, 0))
        
        # Apply the palette
        app.setPalette(terminal_palette)
        
        # Set stylesheet
        stylesheet = """
        QMainWindow, QDialog {
            background-color: #000000;
            color: #00ff00;
        }
        
        QWidget {
            background-color: #000000;
            color: #00ff00;
            font-family: "Courier New", Courier, monospace;
        }
        
        QPushButton {
            background-color: #191919;
            color: #00ff00;
            border: 1px solid #00ff00;
            border-radius: 0px;
            padding: 5px 15px;
            font-family: "Courier New", Courier, monospace;
        }
        
        QPushButton:hover {
            background-color: #303030;
        }
        
        QPushButton:pressed {
            background-color: #000000;
        }
        
        QLineEdit, QTextEdit, QPlainTextEdit {
            background-color: #000000;
            color: #00ff00;
            border: 1px solid #00ff00;
            border-radius: 0px;
            padding: 2px 4px;
            font-family: "Courier New", Courier, monospace;
        }
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
            border: 1px solid #00ff99;
        }
        
        QLabel {
            color: #00ff00;
            font-family: "Courier New", Courier, monospace;
        }
        
        QTabWidget::pane {
            border: 1px solid #00ff00;
        }
        
        QTabBar::tab {
            background-color: #000000;
            color: #00ff00;
            border: 1px solid #00ff00;
            padding: 5px 10px;
        }
        
        QTabBar::tab:selected {
            background-color: #003300;
        }
        
        QScrollBar:vertical {
            background-color: #000000;
            width: 10px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #00ff00;
            min-height: 20px;
        }
        
        QScrollBar:horizontal {
            background-color: #000000;
            height: 10px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #00ff00;
            min-width: 20px;
        }
        """
        
        app.setStyleSheet(stylesheet)
    
    def _apply_neon_hacker_theme(self):
        """Apply neon hacker theme"""
        app = QApplication.instance()
        
        # Create a neon palette
        neon_palette = QPalette()
        
        # Set colors
        neon_palette.setColor(QPalette.ColorRole.Window, QColor(10, 10, 20))
        neon_palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 255, 255))
        neon_palette.setColor(QPalette.ColorRole.Base, QColor(5, 5, 15))
        neon_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(20, 20, 40))
        neon_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(5, 5, 15))
        neon_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 255, 255))
        neon_palette.setColor(QPalette.ColorRole.Text, QColor(0, 255, 255))
        neon_palette.setColor(QPalette.ColorRole.Button, QColor(30, 30, 60))
        neon_palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 255, 255))
        neon_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 255))
        neon_palette.setColor(QPalette.ColorRole.Link, QColor(0, 160, 255))
        neon_palette.setColor(QPalette.ColorRole.Highlight, QColor(80, 0, 80))
        neon_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 0, 255))
        
        # Apply the palette
        app.setPalette(neon_palette)
        
        # Set stylesheet
        stylesheet = """
        QMainWindow, QDialog {
            background-color: #0a0a14;
            color: #00ffff;
        }
        
        QWidget {
            background-color: #0a0a14;
            color: #00ffff;
        }
        
        QPushButton {
            background-color: #1e1e3c;
            color: #00ffff;
            border: 1px solid #ff00ff;
            border-radius: 4px;
            padding: 5px 15px;
        }
        
        QPushButton:hover {
            background-color: #2a2a50;
            border: 1px solid #ff60ff;
        }
        
        QPushButton:pressed {
            background-color: #14142a;
        }
        
        QLineEdit, QTextEdit, QPlainTextEdit {
            background-color: #05050f;
            color: #00ffff;
            border: 1px solid #6600cc;
            border-radius: 3px;
            padding: 2px 4px;
        }
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
            border: 1px solid #cc00cc;
        }
        
        QLabel {
            color: #00ffff;
        }
        
        QMenuBar {
            background-color: #0a0a14;
            color: #00ffff;
        }
        
        QMenuBar::item:selected {
            background-color: #1e1e3c;
        }
        
        QMenu {
            background-color: #0a0a14;
            color: #00ffff;
        }
        
        QMenu::item:selected {
            background-color: #1e1e3c;
        }
        
        QTabWidget::pane {
            border: 1px solid #6600cc;
        }
        
        QTabBar::tab {
            background-color: #0a0a14;
            color: #00ffff;
            border: 1px solid #6600cc;
            padding: 5px 10px;
        }
        
        QTabBar::tab:selected {
            background-color: #1e1e3c;
        }
        
        QScrollBar:vertical {
            background-color: #0a0a14;
            width: 12px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #6600cc;
            min-height: 20px;
            border-radius: 3px;
        }
        
        QScrollBar:horizontal {
            background-color: #0a0a14;
            height: 12px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #6600cc;
            min-width: 20px;
            border-radius: 3px;
        }
        
        /* Neon text effect - will only work on QLabels */
        QLabel.neon {
            color: #00ffff;
            text-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff, 0 0 15px #00ffff;
        }
        """
        
        app.setStyleSheet(stylesheet)
    
    def get_category_color(self, category):
        """
        Get color for a specific puzzle category
        
        Args:
            category: Puzzle category name
            
        Returns:
            str: Color hex code
        """
        return self.category_colors.get(category, "#ffffff")
    
    def get_font(self, font_type):
        """
        Get a specific font
        
        Args:
            font_type: Font type (title, heading, normal, code, terminal)
            
        Returns:
            QFont: Font object
        """
        return self.fonts.get(font_type, self.fonts["normal"])
    
    def style_by_difficulty(self, difficulty):
        """
        Get style for a specific difficulty level
        
        Args:
            difficulty: Difficulty level (Easy, Medium, Hard)
            
        Returns:
            str: CSS style string
        """
        if difficulty == "Easy":
            return "color: #42f55a; font-weight: bold;"
        elif difficulty == "Medium":
            return "color: #f5a742; font-weight: bold;"
        elif difficulty == "Hard":
            return "color: #f54242; font-weight: bold;"
        else:
            return "color: #ffffff; font-weight: bold;" 