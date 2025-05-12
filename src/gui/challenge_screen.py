#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Challenge selection screen for Cybersecurity Escape Room
"""

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QComboBox, QGridLayout, QSpacerItem,
    QSizePolicy
)
from PyQt6.QtCore import Qt

logger = logging.getLogger(__name__)


class ChallengeScreen(QWidget):
    """Challenge selection screen"""
    
    def __init__(self, main_window):
        """Initialize challenge screen"""
        super().__init__()
        self.main_window = main_window
        self.current_category = "All"
        self.current_difficulty = "All"
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
        title_label = QLabel("Cybersecurity Challenges")
        title_label.setObjectName("screenTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Filters
        filter_frame = QFrame()
        filter_frame.setObjectName("filterFrame")
        filter_layout = QHBoxLayout(filter_frame)
        
        # Category filter
        filter_layout.addWidget(QLabel("Category:"))
        self.category_combo = QComboBox()
        self.category_combo.addItem("All")
        self.category_combo.currentTextChanged.connect(self.filter_changed)
        filter_layout.addWidget(self.category_combo)
        
        filter_layout.addSpacing(20)
        
        # Difficulty filter
        filter_layout.addWidget(QLabel("Difficulty:"))
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["All", "Easy", "Medium", "Hard"])
        self.difficulty_combo.currentTextChanged.connect(self.filter_changed)
        filter_layout.addWidget(self.difficulty_combo)
        
        filter_layout.addStretch()
        
        main_layout.addWidget(filter_frame)
        
        # Challenge list container with scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        self.challenges_container = QWidget()
        self.challenges_container.setObjectName("challengesContainer")
        self.challenges_grid = QGridLayout(self.challenges_container)
        self.challenges_grid.setColumnStretch(2, 1)  # Make the third column stretch
        self.challenges_grid.setSpacing(10)
        
        scroll_area.setWidget(self.challenges_container)
        main_layout.addWidget(scroll_area, 1)  # 1 = stretch factor
        
        # Set stylesheet
        self.setStyleSheet("""
            #screenTitle {
                font-size: 24px;
                font-weight: bold;
                color: #00ff99;
                margin-bottom: 10px;
            }
            
            #filterFrame {
                background-color: #1e1e1e;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 15px;
            }
            
            #challengesContainer {
                background-color: transparent;
                padding: 5px;
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
            
            QComboBox {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 5px 10px;
                color: #eee;
                min-width: 120px;
            }
            
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #444;
            }
            
            QComboBox QAbstractItemView {
                background-color: #2a2a2a;
                border: 1px solid #444;
                color: #eee;
                selection-background-color: #0066cc;
            }
        """)
    
    def refresh(self):
        """Update challenge list"""
        # Load categories
        self._load_categories()
        
        # Load challenges
        self._load_challenges()
    
    def _load_categories(self):
        """Load challenge categories from database"""
        try:
            # Remember current selection
            current_text = self.category_combo.currentText()
            
            # Clear combo box except "All"
            while self.category_combo.count() > 1:
                self.category_combo.removeItem(1)
            
            # Get categories from puzzle manager instead of database
            categories = self.main_window.puzzle_manager.get_categories()
            
            # Add to combo box
            for category in categories:
                self.category_combo.addItem(category)
            
            # Try to restore selection
            index = self.category_combo.findText(current_text)
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
            else:
                self.category_combo.setCurrentIndex(0)  # "All"
                
        except Exception as e:
            logger.error(f"Error loading categories: {e}")
    
    def _load_challenges(self):
        """Load challenges based on current filters"""
        # Clear existing challenges
        self._clear_challenges()
        
        try:
            # Get available puzzles from puzzle manager
            all_puzzles = self.main_window.puzzle_manager.get_all_puzzles()
            
            # Apply filters
            filtered_puzzles = []
            for puzzle in all_puzzles:
                # Category filter
                if self.current_category != "All" and puzzle.get('category') != self.current_category:
                    continue
                
                # Difficulty filter
                if self.current_difficulty != "All" and puzzle.get('difficulty') != self.current_difficulty:
                    continue
                
                filtered_puzzles.append(puzzle)
            
            # Display challenges
            if not filtered_puzzles:
                # No challenges found
                label = QLabel("No challenges found matching the current filters.")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setWordWrap(True)
                self.challenges_grid.addWidget(label, 0, 0, 1, 3)
            else:
                # Add each challenge
                for i, puzzle in enumerate(filtered_puzzles):
                    self._add_challenge_item(puzzle, i)
            
        except Exception as e:
            logger.error(f"Error loading challenges: {e}")
            # Show error message
            label = QLabel(f"Error loading challenges: {str(e)}")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setWordWrap(True)
            self.challenges_grid.addWidget(label, 0, 0, 1, 3)
    
    def _clear_challenges(self):
        """Clear all challenges from the grid"""
        # Remove all widgets
        while self.challenges_grid.count():
            item = self.challenges_grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    
    def _add_challenge_item(self, puzzle, index):
        """Add a challenge item to the grid"""
        row = index
        
        # Difficulty indicator
        difficulty = puzzle.get('difficulty', 'Unknown').lower()
        difficulty_icon = QLabel()
        difficulty_icon.setFixedSize(16, 16)
        difficulty_icon.setObjectName(f"difficulty{difficulty.capitalize()}")
        difficulty_icon.setToolTip(f"Difficulty: {difficulty.capitalize()}")
        self.challenges_grid.addWidget(difficulty_icon, row, 0)
        
        # Challenge title and description
        info_frame = QFrame()
        info_frame.setObjectName("challengeInfo")
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(0, 5, 0, 5)
        info_layout.setSpacing(5)
        
        title = puzzle.get('name', 'Unknown Challenge')
        title_label = QLabel(title)
        title_label.setObjectName("challengeTitle")
        info_layout.addWidget(title_label)
        
        description = puzzle.get('description', '')
        if len(description) > 100:
            description = description[:97] + '...'
        desc_label = QLabel(description)
        desc_label.setObjectName("challengeDesc")
        desc_label.setWordWrap(True)
        info_layout.addWidget(desc_label)
        
        # Add category label if available
        category = puzzle.get('category', '')
        if category:
            category_label = QLabel(f"Category: {category}")
            category_label.setObjectName("challengeCategory")
            category_label.setStyleSheet("color: #0099cc; font-size: 12px;")
            info_layout.addWidget(category_label)
        
        self.challenges_grid.addWidget(info_frame, row, 1)
        
        # Button column
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Points display (set a default value of 100 points if not specified)
        points = 100  # Default points based on difficulty
        if difficulty.lower() == 'easy':
            points = 100
        elif difficulty.lower() == 'medium':
            points = 200
        elif difficulty.lower() == 'hard':
            points = 300
            
        points_label = QLabel(f"{points} pts")
        points_label.setObjectName("challengePoints")
        btn_layout.addWidget(points_label)
        
        # Start button
        start_button = QPushButton("Start")
        start_button.setProperty("class", "primary")
        start_button.setObjectName("startButton")
        start_button.clicked.connect(lambda: self.start_challenge(puzzle.get('id')))
        btn_layout.addWidget(start_button)
        
        self.challenges_grid.addLayout(btn_layout, row, 2)
        
        # Styling for the grid items
        difficulty_icon.setStyleSheet(f"""
            #difficultyEasy {{
                background-color: #00cc66;
                border-radius: 8px;
            }}
            
            #difficultyMedium {{
                background-color: #ffcc00;
                border-radius: 8px;
            }}
            
            #difficultyHard {{
                background-color: #ff3333;
                border-radius: 8px;
            }}
        """)
        
        info_frame.setStyleSheet("""
            #challengeInfo {
                padding: 5px;
            }
            
            #challengeTitle {
                font-size: 15px;
                font-weight: bold;
                color: #ffffff;
            }
            
            #challengeDesc {
                font-size: 13px;
                color: #bbbbbb;
            }
            
            #challengePoints {
                font-size: 14px;
                font-weight: bold;
                color: #ffcc00;
            }
            
            #startButton {
                min-width: 80px;
            }
        """)
        
        # Add a separator line after each challenge except the last one
        if index < len(self.main_window.puzzle_manager.get_all_puzzles()) - 1:
            separator = QFrame()
            separator.setFrameShape(QFrame.Shape.HLine)
            separator.setFrameShadow(QFrame.Shadow.Sunken)
            separator.setObjectName("challengeSeparator")
            separator.setStyleSheet("background-color: #333;")
            self.challenges_grid.addWidget(separator, row + 1, 0, 1, 3)
    
    def filter_changed(self):
        """Handle filter changes"""
        self.current_category = self.category_combo.currentText()
        self.current_difficulty = self.difficulty_combo.currentText()
        self._load_challenges()
    
    def start_challenge(self, puzzle_id):
        """Start a selected challenge"""
        if puzzle_id:
            self.main_window.start_puzzle(puzzle_id)
    
    def goto_menu(self):
        """Return to menu screen"""
        self.main_window.goto_menu() 