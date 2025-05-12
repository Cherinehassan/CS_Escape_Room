#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Challenges screen for Cybersecurity Escape Room
Displays available puzzles and allows selection
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QGridLayout, QSpacerItem,
                            QSizePolicy, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont, QIcon, QColor

from ..utils.animation_effects import FlickerEffect, PulseAnimation


class ChallengeCard(QFrame):
    """Card widget displaying a challenge/puzzle"""
    
    # Signal emitted when card is selected
    selected = pyqtSignal(int)  # Emits puzzle ID
    
    def __init__(self, puzzle_id, title, difficulty, category, description, parent=None):
        """
        Initialize challenge card
        
        Args:
            puzzle_id: ID of puzzle
            title: Title of puzzle
            difficulty: Difficulty level (easy, medium, hard)
            category: Category (e.g., network, crypto)
            description: Brief description
            parent: Parent widget
        """
        super().__init__(parent)
        self.puzzle_id = puzzle_id
        self.title = title
        self.difficulty = difficulty
        self.category = category
        self.description = description
        
        self._create_ui()
        self._apply_styles()
        self._connect_signals()
    
    def _create_ui(self):
        """Create the card UI"""
        self.setObjectName(f"challengeCard_{self.puzzle_id}")
        self.setMinimumSize(280, 200)
        self.setMaximumSize(320, 250)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        self.title_label = QLabel(self.title)
        self.title_label.setObjectName("cardTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.title_label)
        
        # Card content
        content_layout = QVBoxLayout()
        content_layout.setSpacing(8)
        
        # Difficulty and category
        info_layout = QHBoxLayout()
        
        self.difficulty_label = QLabel(f"Difficulty: {self.difficulty}")
        self.difficulty_label.setObjectName(f"difficulty_{self.difficulty.lower()}")
        info_layout.addWidget(self.difficulty_label)
        
        info_layout.addStretch()
        
        self.category_label = QLabel(f"Category: {self.category}")
        self.category_label.setObjectName(f"category_{self.category.lower()}")
        info_layout.addWidget(self.category_label)
        
        content_layout.addLayout(info_layout)
        
        # Description
        self.description_label = QLabel(self.description)
        self.description_label.setObjectName("cardDescription")
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        content_layout.addWidget(self.description_label)
        
        main_layout.addLayout(content_layout)
        
        # Start button
        self.start_button = QPushButton("START CHALLENGE")
        self.start_button.setObjectName("challengeButton")
        main_layout.addWidget(self.start_button)
    
    def _connect_signals(self):
        """Connect signals to slots"""
        self.start_button.clicked.connect(lambda: self.selected.emit(self.puzzle_id))
    
    def _apply_styles(self):
        """Apply styles to the card"""
        # Set base styles based on difficulty
        difficulty_colors = {
            "easy": "#4caf50",     # Green
            "medium": "#ff9800",   # Orange
            "hard": "#f44336"      # Red
        }
        
        difficulty_color = difficulty_colors.get(self.difficulty.lower(), "#00ccff")
        
        self.setStyleSheet(f"""
            #challengeCard_{self.puzzle_id} {{
                background-color: rgba(10, 15, 20, 0.7);
                border: 1px solid {difficulty_color};
                border-radius: 8px;
            }}
            
            #cardTitle {{
                font-size: 18px;
                font-weight: bold;
                color: {difficulty_color};
            }}
            
            #difficulty_{self.difficulty.lower()} {{
                color: {difficulty_color};
                font-weight: bold;
                font-size: 12px;
            }}
            
            #category_{self.category.lower()} {{
                color: #00ccff;
                font-weight: bold;
                font-size: 12px;
            }}
            
            #cardDescription {{
                color: #cccccc;
                font-size: 12px;
                margin-top: 5px;
                margin-bottom: 10px;
            }}
            
            #challengeButton {{
                background-color: rgba(0, 0, 0, 0.5);
                color: {difficulty_color};
                border: 1px solid {difficulty_color};
                border-radius: 4px;
                padding: 8px;
                font-size: 12px;
                font-weight: bold;
            }}
            
            #challengeButton:hover {{
                background-color: rgba(0, 0, 0, 0.7);
                border: 1px solid #ffffff;
                color: #ffffff;
            }}
        """)
    
    def highlight(self):
        """Highlight the card when selected"""
        # Set a more prominent border
        original_style = self.styleSheet()
        highlight_style = original_style.replace("border: 1px solid", "border: 2px solid")
        self.setStyleSheet(highlight_style)


class ChallengesScreen(QWidget):
    """Screen displaying available cybersecurity challenges"""
    
    # Signals
    challenge_selected = pyqtSignal(int)  # Emitted when a challenge is selected
    return_to_menu = pyqtSignal()         # Emitted when back button is clicked
    
    def __init__(self, puzzle_manager, parent=None):
        """
        Initialize challenges screen
        
        Args:
            puzzle_manager: Puzzle manager instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.puzzle_manager = puzzle_manager
        
        self._create_ui()
        self._connect_signals()
        self._apply_styles()
        self._apply_animations()
        
        # Populate puzzles
        self.load_puzzles()
    
    def _create_ui(self):
        """Create the main UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Header section
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QVBoxLayout(header_frame)
        
        self.title_label = QLabel("CYBERSECURITY CHALLENGES")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setObjectName("titleLabel")
        header_layout.addWidget(self.title_label)
        
        self.subtitle_label = QLabel("Select a challenge to test your cybersecurity skills")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setObjectName("subtitleLabel")
        header_layout.addWidget(self.subtitle_label)
        
        main_layout.addWidget(header_frame)
        
        # Filter controls (can be expanded in the future)
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        
        self.back_button = QPushButton("← BACK TO MENU")
        self.back_button.setObjectName("backButton")
        filter_layout.addWidget(self.back_button)
        
        filter_layout.addStretch()
        
        main_layout.addLayout(filter_layout)
        
        # Challenge cards in scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("challengesScrollArea")
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Scroll content widget
        scroll_content = QWidget()
        self.challenges_layout = QGridLayout(scroll_content)
        self.challenges_layout.setSpacing(20)
        
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
    
    def _connect_signals(self):
        """Connect signals to slots"""
        self.back_button.clicked.connect(self.return_to_menu.emit)
    
    def _apply_styles(self):
        """Apply styles to the challenges screen"""
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
            
            #backButton {
                background-color: rgba(0, 0, 0, 0.5);
                color: #cccccc;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
            }
            
            #backButton:hover {
                background-color: rgba(0, 0, 0, 0.7);
                color: #ffffff;
                border-color: #00ccff;
            }
            
            #challengesScrollArea {
                background-color: transparent;
                border: none;
            }
            
            QScrollBar:vertical {
                background: rgba(0, 0, 0, 0.3);
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background: rgba(0, 204, 255, 0.5);
                min-height: 20px;
                border-radius: 6px;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
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
    
    def load_puzzles(self):
        """Load and display available puzzles"""
        # Clear existing layout
        while self.challenges_layout.count():
            item = self.challenges_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Get puzzles from manager
        puzzles = self.puzzle_manager.get_all_puzzles()
        
        # Create a card for each puzzle
        row, col = 0, 0
        max_cols = 3  # Number of columns in grid
        
        for puzzle in puzzles:
            # For backward compatibility, try to handle both dictionary format
            # and Puzzle objects - prefer dictionary fields if puzzle is a dict
            # otherwise use Puzzle object attributes
            if isinstance(puzzle, dict):
                card = ChallengeCard(
                    puzzle.get('id', 0),
                    puzzle.get('title', 'Unknown Challenge'),
                    puzzle.get('difficulty', 'Medium'),
                    puzzle.get('category', 'General'),
                    puzzle.get('short_description', 'No description available'),
                    self
                )
            else:
                # Find short description if available, or use first part of full description
                short_desc = getattr(puzzle, 'short_description', 
                              puzzle.description[:100] + '...' if len(puzzle.description) > 100 
                              else puzzle.description)
                
                # Use Puzzle object's attributes
                card = ChallengeCard(
                    puzzle.id,
                    getattr(puzzle, 'title', puzzle.name),  # Use title or fall back to name
                    puzzle.difficulty,
                    puzzle.category,
                    short_desc,
                    self
                )
            
            # Connect card signal
            card.selected.connect(self.challenge_selected.emit)
            
            # Add to layout
            self.challenges_layout.addWidget(card, row, col)
            
            # Update grid position
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def update_challenges(self):
        """Refresh the challenges display"""
        self.load_puzzles() 