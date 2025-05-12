#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Puzzle screen for Cybersecurity Escape Room
Displays and manages a single cybersecurity challenge
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QGridLayout, QSpacerItem,
                            QSizePolicy, QTextEdit, QLineEdit, QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap, QFont, QIcon

from ..utils.animation_effects import FlickerEffect, AccessAnimation


class PuzzleScreen(QWidget):
    """Screen for displaying and managing cybersecurity puzzles"""
    
    # Signals
    puzzle_completed = pyqtSignal(int, float)  # Emitted when puzzle is completed (puzzle_id, time)
    return_to_challenges = pyqtSignal()        # Emitted when back button is clicked
    
    def __init__(self, puzzle_manager, parent=None):
        """
        Initialize puzzle screen
        
        Args:
            puzzle_manager: Puzzle manager instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.puzzle_manager = puzzle_manager
        self.current_puzzle = None
        self.start_time = None
        self.timer = QTimer()
        self.timer.setInterval(1000)  # Update every second
        self.timer.timeout.connect(self._update_timer)
        self.elapsed_seconds = 0
        
        self._create_ui()
        self._connect_signals()
        self._apply_styles()
    
    def _create_ui(self):
        """Create the puzzle UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Header section
        header_layout = QHBoxLayout()
        
        # Back button
        self.back_button = QPushButton("← BACK")
        self.back_button.setObjectName("backButton")
        self.back_button.setFixedWidth(120)
        header_layout.addWidget(self.back_button)
        
        # Title
        self.title_label = QLabel("PUZZLE NAME")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setObjectName("puzzleTitle")
        header_layout.addWidget(self.title_label)
        
        # Timer
        self.timer_label = QLabel("00:00")
        self.timer_label.setObjectName("timerLabel")
        self.timer_label.setFixedWidth(120)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        header_layout.addWidget(self.timer_label)
        
        main_layout.addLayout(header_layout)
        
        # Info bar - difficulty, category, points
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_layout = QHBoxLayout(info_frame)
        info_layout.setSpacing(20)
        
        self.difficulty_label = QLabel("Difficulty: Medium")
        self.difficulty_label.setObjectName("infoLabel")
        info_layout.addWidget(self.difficulty_label)
        
        info_layout.addStretch()
        
        self.category_label = QLabel("Category: Cryptography")
        self.category_label.setObjectName("infoLabel")
        info_layout.addWidget(self.category_label)
        
        info_layout.addStretch()
        
        self.points_label = QLabel("Points: 100")
        self.points_label.setObjectName("infoLabel")
        info_layout.addWidget(self.points_label)
        
        main_layout.addWidget(info_frame)
        
        # Puzzle content area
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Description
        self.description_label = QLabel("Puzzle description goes here...")
        self.description_label.setObjectName("descriptionLabel")
        self.description_label.setWordWrap(True)
        content_layout.addWidget(self.description_label)
        
        # Puzzle-specific content (dynamic)
        self.puzzle_content_widget = QWidget()
        self.puzzle_content_layout = QVBoxLayout(self.puzzle_content_widget)
        content_layout.addWidget(self.puzzle_content_widget)
        
        # Placeholder for puzzle content
        self.puzzle_text = QTextEdit()
        self.puzzle_text.setObjectName("puzzleText")
        self.puzzle_text.setReadOnly(True)
        self.puzzle_text.setPlaceholderText("Puzzle content will appear here")
        self.puzzle_content_layout.addWidget(self.puzzle_text)
        
        main_layout.addWidget(content_frame)
        
        # Solution input area
        solution_frame = QFrame()
        solution_frame.setObjectName("solutionFrame")
        solution_layout = QVBoxLayout(solution_frame)
        
        solution_title = QLabel("SOLUTION")
        solution_title.setObjectName("sectionTitle")
        solution_layout.addWidget(solution_title)
        
        input_layout = QHBoxLayout()
        
        self.solution_input = QLineEdit()
        self.solution_input.setObjectName("solutionInput")
        self.solution_input.setPlaceholderText("Enter your answer here...")
        input_layout.addWidget(self.solution_input)
        
        self.submit_button = QPushButton("SUBMIT")
        self.submit_button.setObjectName("submitButton")
        input_layout.addWidget(self.submit_button)
        
        solution_layout.addLayout(input_layout)
        
        # Hint section
        hint_layout = QHBoxLayout()
        
        self.hint_label = QLabel("Need a hint?")
        self.hint_label.setObjectName("hintLabel")
        hint_layout.addWidget(self.hint_label)
        
        hint_layout.addStretch()
        
        self.hint_button = QPushButton("GET HINT")
        self.hint_button.setObjectName("hintButton")
        hint_layout.addWidget(self.hint_button)
        
        solution_layout.addLayout(hint_layout)
        
        main_layout.addWidget(solution_frame)
        
        # Progress area
        progress_frame = QFrame()
        progress_frame.setObjectName("progressFrame")
        progress_layout = QVBoxLayout(progress_frame)
        
        progress_title = QLabel("PROGRESS")
        progress_title.setObjectName("sectionTitle")
        progress_layout.addWidget(progress_title)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("puzzleProgress")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p% Complete")
        progress_layout.addWidget(self.progress_bar)
        
        main_layout.addWidget(progress_frame)
        
        # Result message (hidden initially)
        self.result_frame = QFrame()
        self.result_frame.setObjectName("resultFrame")
        self.result_frame.setVisible(False)
        result_layout = QVBoxLayout(self.result_frame)
        
        self.result_label = QLabel()
        self.result_label.setObjectName("resultLabel")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setWordWrap(True)
        result_layout.addWidget(self.result_label)
        
        main_layout.addWidget(self.result_frame)
    
    def _connect_signals(self):
        """Connect signals to slots"""
        self.back_button.clicked.connect(self.return_to_challenges.emit)
        self.submit_button.clicked.connect(self._check_solution)
        self.hint_button.clicked.connect(self._show_hint)
        self.solution_input.returnPressed.connect(self._check_solution)
    
    def _apply_styles(self):
        """Apply styles to the puzzle screen"""
        self.setStyleSheet("""
            #puzzleTitle {
                font-size: 28px;
                font-weight: bold;
                color: #00ccff;
            }
            
            #timerLabel {
                font-size: 20px;
                color: #ff9900;
                font-family: 'Courier New', monospace;
                font-weight: bold;
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
            
            #infoFrame {
                background-color: rgba(0, 20, 40, 0.5);
                border-radius: 5px;
                padding: 10px;
                border: 1px solid #333333;
            }
            
            #infoLabel {
                color: #cccccc;
                font-size: 14px;
            }
            
            #contentFrame {
                background-color: rgba(0, 0, 0, 0.3);
                border-radius: 10px;
                border: 1px solid #333333;
            }
            
            #descriptionLabel {
                color: #ffffff;
                font-size: 16px;
                line-height: 1.4;
            }
            
            #puzzleText {
                background-color: rgba(0, 10, 20, 0.7);
                color: #00ff99;
                border: 1px solid #333333;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
            }
            
            #solutionFrame, #progressFrame {
                background-color: rgba(0, 20, 30, 0.4);
                border-radius: 5px;
                padding: 15px;
                border: 1px solid #333333;
            }
            
            #sectionTitle {
                font-size: 16px;
                font-weight: bold;
                color: #00ccff;
                margin-bottom: 10px;
            }
            
            #solutionInput {
                background-color: rgba(0, 0, 0, 0.5);
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                font-family: 'Courier New', monospace;
            }
            
            #solutionInput:focus {
                border: 1px solid #00ccff;
            }
            
            #submitButton {
                background-color: #00ccff;
                color: #000000;
                border: none;
                border-radius: 5px;
                padding: 8px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            
            #submitButton:hover {
                background-color: #33d6ff;
            }
            
            #submitButton:pressed {
                background-color: #0099cc;
            }
            
            #hintLabel {
                color: #cccccc;
                font-style: italic;
                font-size: 14px;
            }
            
            #hintButton {
                background-color: transparent;
                color: #ff9900;
                border: 1px solid #ff9900;
                border-radius: 5px;
                padding: 5px 15px;
                font-size: 12px;
            }
            
            #hintButton:hover {
                background-color: rgba(255, 153, 0, 0.2);
            }
            
            #puzzleProgress {
                background-color: rgba(0, 0, 0, 0.3);
                border: 1px solid #333333;
                border-radius: 3px;
                height: 20px;
                text-align: center;
                color: white;
            }
            
            #puzzleProgress::chunk {
                background-color: #00ccff;
                border-radius: 3px;
            }
            
            #resultFrame {
                background-color: rgba(0, 0, 0, 0.5);
                border-radius: 10px;
                padding: 20px;
                margin-top: 10px;
            }
            
            #resultLabel {
                font-size: 18px;
                font-weight: bold;
            }
            
            #resultLabel[correct="true"] {
                color: #00ff99;
            }
            
            #resultLabel[correct="false"] {
                color: #ff3333;
            }
        """)
    
    def load_puzzle(self, puzzle_id):
        """
        Load a puzzle by ID
        
        Args:
            puzzle_id: ID of the puzzle to load
        """
        # Reset UI state
        self._reset_ui()
        
        # Get puzzle from manager
        self.current_puzzle = self.puzzle_manager.get_puzzle_by_id(puzzle_id)
        if not self.current_puzzle:
            self.description_label.setText("Error: Puzzle not found")
            return
        
        # Update UI based on puzzle object or dictionary
        if isinstance(self.current_puzzle, dict):
            # Handle dictionary format
            self.title_label.setText(self.current_puzzle.get('title', 'Unknown Puzzle'))
            self.description_label.setText(self.current_puzzle.get('description', 'No description available'))
            self.difficulty_label.setText(f"Difficulty: {self.current_puzzle.get('difficulty', 'Medium')}")
            self.category_label.setText(f"Category: {self.current_puzzle.get('category', 'General')}")
            self.points_label.setText(f"Points: {self.current_puzzle.get('points', 100)}")
            self.puzzle_text.setText(self.current_puzzle.get('content', 'No puzzle content available'))
        else:
            # Handle Puzzle object format
            self.title_label.setText(getattr(self.current_puzzle, 'title', self.current_puzzle.name))
            self.description_label.setText(self.current_puzzle.description)
            self.difficulty_label.setText(f"Difficulty: {self.current_puzzle.difficulty}")
            self.category_label.setText(f"Category: {self.current_puzzle.category}")
            self.points_label.setText(f"Points: {getattr(self.current_puzzle, 'points', 100)}")
            
            # Use content field if available, otherwise use description
            content = getattr(self.current_puzzle, 'content', self.current_puzzle.description)
            self.puzzle_text.setText(content)
        
        # Start timer
        self._start_timer()
    
    def _reset_ui(self):
        """Reset the UI state"""
        self.timer.stop()
        self.elapsed_seconds = 0
        self.timer_label.setText("00:00")
        self.solution_input.clear()
        self.progress_bar.setValue(0)
        self.result_frame.setVisible(False)
        self.solution_input.setEnabled(True)
        self.submit_button.setEnabled(True)
    
    def _start_timer(self):
        """Start the puzzle timer"""
        self.elapsed_seconds = 0
        self.timer.start()
        self._update_timer()
    
    def _update_timer(self):
        """Update the timer display"""
        self.elapsed_seconds += 1
        minutes = self.elapsed_seconds // 60
        seconds = self.elapsed_seconds % 60
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")
    
    def _check_solution(self):
        """Check if the submitted solution is correct"""
        if not self.current_puzzle:
            return
        
        user_solution = self.solution_input.text().strip()
        
        # Check answer based on object type
        is_correct = False
        
        if isinstance(self.current_puzzle, dict):
            # Dictionary format
            correct_solution = self.current_puzzle.get('solution', '').strip()
            is_correct = user_solution.lower() == correct_solution.lower()
        else:
            # Puzzle object
            is_correct = self.current_puzzle.check_answer(user_solution)
        
        if is_correct:
            self._handle_correct_solution()
        else:
            self._handle_incorrect_solution()
    
    def _handle_correct_solution(self):
        """Handle correct solution submission"""
        # Stop timer
        self.timer.stop()
        
        # Update UI
        self.progress_bar.setValue(100)
        self.result_frame.setVisible(True)
        self.result_label.setText("CORRECT! Puzzle solved successfully.")
        self.result_label.setProperty("correct", "true")
        self.result_label.setStyleSheet("")  # Force style refresh
        
        # Disable input
        self.solution_input.setEnabled(False)
        self.submit_button.setEnabled(False)
        
        # Play success animation
        AccessAnimation.access_granted(self.result_frame)
        
        # Emit puzzle completed signal
        self.puzzle_completed.emit(
            self.current_puzzle.get('id', 0),
            self.elapsed_seconds
        )
    
    def _handle_incorrect_solution(self):
        """Handle incorrect solution submission"""
        # Update UI
        self.result_frame.setVisible(True)
        self.result_label.setText("INCORRECT. Try again!")
        self.result_label.setProperty("correct", "false")
        self.result_label.setStyleSheet("")  # Force style refresh
        
        # Play failure animation
        AccessAnimation.access_denied(self.result_frame)
        
        # Hide result after a delay
        QTimer.singleShot(3000, lambda: self.result_frame.setVisible(False))
    
    def _show_hint(self):
        """Show a hint for the current puzzle"""
        if not self.current_puzzle:
            return
        
        # Get hint based on object type
        if isinstance(self.current_puzzle, dict):
            hint = self.current_puzzle.get('hint', 'No hint available for this puzzle.')
        else:
            # For Puzzle object, use first hint if available
            hints = getattr(self.current_puzzle, 'hints', [])
            hint = hints[0] if hints else 'No hint available for this puzzle.'
        
        # Update progress penalty for using hint
        current_progress = self.progress_bar.value()
        if current_progress < 75:  # Don't penalize too much when close to solution
            self.progress_bar.setValue(max(0, current_progress - 10))
        
        # Update hint label
        self.hint_label.setText(hint)
        self.hint_label.setStyleSheet("color: #ff9900; font-weight: bold;")
        
        # Disable hint button temporarily
        self.hint_button.setEnabled(False)
        QTimer.singleShot(30000, lambda: self.hint_button.setEnabled(True))  # Re-enable after 30 seconds 