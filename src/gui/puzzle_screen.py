#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Puzzle screen for Cybersecurity Escape Room
Displays interactive puzzles and handles user interaction
"""

import logging
import time
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QSplitter, QTextEdit, QLineEdit,
    QGridLayout, QMessageBox, QProgressBar, QDialog
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette

from src.database.db_manager import PuzzleHint

logger = logging.getLogger(__name__)


class PuzzleScreen(QWidget):
    """Puzzle interaction screen"""
    
    def __init__(self, main_window):
        """Initialize puzzle screen"""
        super().__init__()
        self.main_window = main_window
        self.puzzle_id = None
        self.attempt_id = None
        self.puzzle_data = None
        self.hints = []
        self.hints_used = 0
        self.timer = None
        self.time_elapsed = 0
        self.time_limit = None
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Header with back button and timer
        header_layout = QHBoxLayout()
        
        self.back_button = QPushButton("← Exit Challenge")
        self.back_button.setObjectName("backButton")
        self.back_button.clicked.connect(self.confirm_exit)
        header_layout.addWidget(self.back_button)
        
        header_layout.addStretch()
        
        # Timer display
        self.timer_label = QLabel("Time: 00:00")
        self.timer_label.setObjectName("timerLabel")
        header_layout.addWidget(self.timer_label)
        
        main_layout.addLayout(header_layout)
        
        # Title and info bar
        info_bar = QFrame()
        info_bar.setObjectName("infoBar")
        info_layout = QHBoxLayout(info_bar)
        
        self.puzzle_title = QLabel("Puzzle Title")
        self.puzzle_title.setObjectName("puzzleTitle")
        info_layout.addWidget(self.puzzle_title)
        
        info_layout.addStretch()
        
        # Difficulty indicator
        difficulty_layout = QHBoxLayout()
        difficulty_layout.addWidget(QLabel("Difficulty:"))
        self.difficulty_label = QLabel("Medium")
        self.difficulty_label.setObjectName("difficultyLabel")
        difficulty_layout.addWidget(self.difficulty_label)
        info_layout.addLayout(difficulty_layout)
        
        # Points indicator
        points_layout = QHBoxLayout()
        points_layout.addWidget(QLabel("Points:"))
        self.points_label = QLabel("100")
        self.points_label.setObjectName("pointsLabel")
        points_layout.addWidget(self.points_label)
        info_layout.addLayout(points_layout)
        
        main_layout.addWidget(info_bar)
        
        # Main content splitter (puzzle and instructions)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side: Instructions and hints
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Instructions scroll area
        instructions_frame = QFrame()
        instructions_frame.setObjectName("instructionsFrame")
        instructions_layout = QVBoxLayout(instructions_frame)
        
        instructions_title = QLabel("Challenge Instructions")
        instructions_title.setObjectName("sectionTitle")
        instructions_layout.addWidget(instructions_title)
        
        instructions_scroll = QScrollArea()
        instructions_scroll.setWidgetResizable(True)
        instructions_scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        instructions_content = QWidget()
        instructions_content_layout = QVBoxLayout(instructions_content)
        
        self.instructions_text = QLabel("Instructions text will go here...")
        self.instructions_text.setObjectName("instructionsText")
        self.instructions_text.setWordWrap(True)
        instructions_content_layout.addWidget(self.instructions_text)
        instructions_content_layout.addStretch()
        
        instructions_scroll.setWidget(instructions_content)
        instructions_layout.addWidget(instructions_scroll)
        
        left_layout.addWidget(instructions_frame)
        
        # Hints section
        hints_frame = QFrame()
        hints_frame.setObjectName("hintsFrame")
        hints_layout = QVBoxLayout(hints_frame)
        
        hints_title = QLabel("Hints")
        hints_title.setObjectName("sectionTitle")
        hints_layout.addWidget(hints_title)
        
        self.hints_container = QWidget()
        self.hints_container_layout = QVBoxLayout(self.hints_container)
        hints_layout.addWidget(self.hints_container)
        
        # Get hint button
        self.hint_button = QPushButton("Get Hint")
        self.hint_button.setObjectName("hintButton")
        self.hint_button.clicked.connect(self.reveal_hint)
        hints_layout.addWidget(self.hint_button)
        
        left_layout.addWidget(hints_frame)
        
        # Right side: Puzzle content
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        self.puzzle_container = QFrame()
        self.puzzle_container.setObjectName("puzzleContainer")
        puzzle_layout = QVBoxLayout(self.puzzle_container)
        
        self.puzzle_content = QLabel("Puzzle content will be loaded here...")
        self.puzzle_content.setObjectName("puzzleContent")
        self.puzzle_content.setWordWrap(True)
        self.puzzle_content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.puzzle_content.setMinimumHeight(300)
        puzzle_layout.addWidget(self.puzzle_content)
        
        right_layout.addWidget(self.puzzle_container, 1)  # 1 = stretch factor
        
        # Answer section
        answer_frame = QFrame()
        answer_frame.setObjectName("answerFrame")
        answer_layout = QVBoxLayout(answer_frame)
        
        answer_title = QLabel("Your Solution")
        answer_title.setObjectName("sectionTitle")
        answer_layout.addWidget(answer_title)
        
        answer_input_layout = QHBoxLayout()
        
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Enter your answer here...")
        self.answer_input.returnPressed.connect(self.submit_answer)
        answer_input_layout.addWidget(self.answer_input)
        
        self.submit_button = QPushButton("Submit")
        self.submit_button.setObjectName("submitButton")
        self.submit_button.setProperty("class", "primary")
        self.submit_button.clicked.connect(self.submit_answer)
        answer_input_layout.addWidget(self.submit_button)
        
        answer_layout.addLayout(answer_input_layout)
        
        right_layout.addWidget(answer_frame)
        
        # Add widgets to splitter
        self.splitter.addWidget(left_widget)
        self.splitter.addWidget(right_widget)
        
        # Set initial sizes (40% left, 60% right)
        self.splitter.setSizes([400, 600])
        
        main_layout.addWidget(self.splitter)
        
        # Set stylesheet
        self.setStyleSheet("""
            #infoBar {
                background-color: #1e1e1e;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 10px;
            }
            
            #puzzleTitle {
                font-size: 20px;
                font-weight: bold;
                color: #00ff99;
            }
            
            #difficultyLabel.easy {
                color: #00cc66;
                font-weight: bold;
            }
            
            #difficultyLabel.medium {
                color: #ffcc00;
                font-weight: bold;
            }
            
            #difficultyLabel.hard {
                color: #ff3333;
                font-weight: bold;
            }
            
            #pointsLabel {
                font-weight: bold;
                color: #ffcc00;
            }
            
            #instructionsFrame, #hintsFrame, #puzzleContainer, #answerFrame {
                background-color: #262626;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 10px;
            }
            
            #sectionTitle {
                font-size: 16px;
                font-weight: bold;
                color: #00ff99;
                margin-bottom: 10px;
            }
            
            #instructionsText {
                color: #ddd;
                line-height: 1.5;
            }
            
            #puzzleContent {
                color: #fff;
                font-size: 16px;
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
            
            #timerLabel {
                font-size: 16px;
                font-weight: bold;
                color: #fff;
            }
            
            #timerLabel.warning {
                color: #ffcc00;
            }
            
            #timerLabel.danger {
                color: #ff3333;
            }
            
            #hintButton {
                background-color: #333;
                border: 1px solid #444;
            }
            
            #hintButton:hover {
                background-color: #444;
                border: 1px solid #555;
            }
            
            #submitButton {
                min-width: 100px;
            }
            
            .hint {
                background-color: #333;
                border-radius: 4px;
                padding: 10px;
                margin-bottom: 10px;
                color: #eee;
            }
            
            .hintLabel {
                font-weight: bold;
                color: #00ff99;
                margin-bottom: 5px;
            }
            
            .hintText {
                color: #ccc;
            }
            
            .hintDeduction {
                color: #ff6666;
                font-style: italic;
                text-align: right;
                margin-top: 5px;
            }
        """)
    
    def set_puzzle(self, puzzle_id, puzzle_data):
        """Set the current puzzle and load its data"""
        self.puzzle_id = puzzle_id
        self.puzzle_data = puzzle_data
        self.hints = []
        self.hints_used = 0
        self.attempt_id = None
        self.time_elapsed = 0
        
        # Stop any existing timer
        if self.timer and self.timer.isActive():
            self.timer.stop()
        
        # Load puzzle data
        self._load_puzzle_data()
        
        # Start a new attempt
        self._start_attempt()
        
        # Start timer
        self._start_timer()
        
        # Enable/disable UI elements
        self.answer_input.setEnabled(True)
        self.submit_button.setEnabled(True)
        self.hint_button.setEnabled(True)
    
    def _load_puzzle_data(self):
        """Load puzzle data from JSON puzzle"""
        if not self.puzzle_data:
            return
        
        try:
            # Set puzzle title and info
            self.puzzle_title.setText(self.puzzle_data.get('name', 'Unknown Puzzle'))
            
            # Set difficulty with appropriate class
            difficulty = self.puzzle_data.get('difficulty', 'Medium')
            self.difficulty_label.setText(difficulty)
            self.difficulty_label.setProperty("class", difficulty.lower())
            self.style().unpolish(self.difficulty_label)
            self.style().polish(self.difficulty_label)
            
            # Set points based on difficulty if not specified
            points = 100  # Default points based on difficulty
            if difficulty.lower() == 'easy':
                points = 100
            elif difficulty.lower() == 'medium':
                points = 200
            elif difficulty.lower() == 'hard':
                points = 300
                
            self.points_label.setText(str(points))
            
            # Set instructions
            instructions = self.puzzle_data.get('description', 'No instructions available.')
            objective = self.puzzle_data.get('learning_objective', '')
            
            if objective:
                instructions += f"\n\nLearning Objective: {objective}"
                
            self.instructions_text.setText(instructions)
            
            # Store hints
            self.hints = self.puzzle_data.get('hints', [])
            
            # Clear hint container
            while self.hints_container_layout.count():
                item = self.hints_container_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            
            # Add placeholder if hints are available
            if self.hints:
                hint_placeholder = QLabel("Hints are available if you get stuck.")
                hint_placeholder.setObjectName("hintPlaceholder")
                hint_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
                hint_placeholder.setWordWrap(True)
                self.hints_container_layout.addWidget(hint_placeholder)
            else:
                no_hints_label = QLabel("No hints available for this puzzle.")
                no_hints_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                no_hints_label.setWordWrap(True)
                self.hints_container_layout.addWidget(no_hints_label)
                self.hint_button.setEnabled(False)
            
            # Set a default time limit based on difficulty if not specified
            self.time_limit = None
            if difficulty.lower() == 'easy':
                self.time_limit = 300  # 5 minutes
            elif difficulty.lower() == 'medium':
                self.time_limit = 600  # 10 minutes
            elif difficulty.lower() == 'hard':
                self.time_limit = 900  # 15 minutes
            
            # Load puzzle content based on category
            self._load_puzzle_content()
            
        except Exception as e:
            logger.error(f"Error loading puzzle data: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Failed to load puzzle: {str(e)}")
            self.main_window.goto_challenges()
    
    def _load_puzzle_content(self):
        """Load puzzle content based on category"""
        category = self.puzzle_data.get('category', 'Uncategorized')
        name = self.puzzle_data.get('name', 'Unknown Puzzle')
        
        # Different formatting based on category
        content = f"<h2>{name}</h2>\n"
        content += f"<p><b>Category:</b> {category}</p>\n"
        
        if category == "Cryptography":
            content += """
            <div style="background-color: #1a1a2e; border-radius: 5px; padding: 15px; margin-top: 10px;">
                <p>Decrypt the message according to the instructions.</p>
                <p style="font-family: monospace; background-color: #0f3460; padding: 10px; border-radius: 3px;">
                    {0}
                </p>
            </div>
            """.format(self.puzzle_data.get('description').split(': ')[1] if ': ' in self.puzzle_data.get('description', '') else '')
        
        elif category == "Hashing":
            content += """
            <div style="background-color: #1f2833; border-radius: 5px; padding: 15px; margin-top: 10px;">
                <p>Answer the question about hash functions:</p>
                <p style="background-color: #0b0c10; padding: 10px; border-radius: 3px;">
                    {0}
                </p>
            </div>
            """.format(self.puzzle_data.get('description', ''))
        
        elif category == "Social Engineering":
            content += """
            <div style="background-color: #321e3e; border-radius: 5px; padding: 15px; margin-top: 10px;">
                <p>Identify the social engineering attack scenario:</p>
                <p style="font-style: italic; background-color: #240b36; padding: 10px; border-radius: 3px;">
                    {0}
                </p>
            </div>
            """.format(self.puzzle_data.get('description', ''))
        
        elif category == "Malware":
            content += """
            <div style="background-color: #3c1642; border-radius: 5px; padding: 15px; margin-top: 10px;">
                <p>Identify the malware type based on the scenario:</p>
                <p style="color: #ff6b6b; background-color: #1e0f21; padding: 10px; border-radius: 3px;">
                    {0}
                </p>
            </div>
            """.format(self.puzzle_data.get('description', ''))
        
        elif category == "Encryption":
            content += """
            <div style="background-color: #052233; border-radius: 5px; padding: 15px; margin-top: 10px;">
                <p>Answer the question about encryption standards:</p>
                <p style="font-family: monospace; background-color: #001219; padding: 10px; border-radius: 3px;">
                    {0}
                </p>
            </div>
            """.format(self.puzzle_data.get('description', ''))
        
        elif category == "Authentication":
            content += """
            <div style="background-color: #2c294f; border-radius: 5px; padding: 15px; margin-top: 10px;">
                <p>Determine the correct authentication approach:</p>
                <p style="background-color: #1b1942; padding: 10px; border-radius: 3px;">
                    {0}
                </p>
            </div>
            """.format(self.puzzle_data.get('description', ''))
        
        elif category == "Attacks":
            content += """
            <div style="background-color: #3a0d27; border-radius: 5px; padding: 15px; margin-top: 10px;">
                <p>Identify the attack vector described below:</p>
                <p style="color: #e43f5a; background-color: #200016; padding: 10px; border-radius: 3px;">
                    {0}
                </p>
            </div>
            """.format(self.puzzle_data.get('description', ''))
        
        else:
            # Default formatting for other categories
            content += """
            <div style="background-color: #2d3e50; border-radius: 5px; padding: 15px; margin-top: 10px;">
                <p>Please solve the following challenge:</p>
                <p style="background-color: #1c2630; padding: 10px; border-radius: 3px;">
                    {0}
                </p>
            </div>
            """.format(self.puzzle_data.get('description', ''))
        
        self.puzzle_content.setText(content)
    
    def _start_attempt(self):
        """Start a new puzzle attempt"""
        if not self.puzzle_id:
            return
            
        try:
            self.attempt_id = self.main_window.game_state.start_puzzle_attempt(self.puzzle_id)
            
            if not self.attempt_id:
                QMessageBox.warning(self, "Error", "Could not start a new attempt. You may have reached the maximum number of attempts for this puzzle.")
                self.main_window.goto_challenges()
                return
                
            logger.info(f"Started puzzle attempt {self.attempt_id} for puzzle {self.puzzle_id}")
            
        except Exception as e:
            logger.error(f"Error starting puzzle attempt: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Failed to start puzzle attempt: {str(e)}")
            self.main_window.goto_challenges()
    
    def _start_timer(self):
        """Start or resume the timer"""
        if not self.timer:
            self.timer = QTimer()
            self.timer.timeout.connect(self._update_timer)
        
        if not self.timer.isActive():
            self.timer.start(1000)  # Update every second
    
    def _update_timer(self):
        """Update the timer display"""
        self.time_elapsed += 1
        
        # Format time as MM:SS
        minutes = self.time_elapsed // 60
        seconds = self.time_elapsed % 60
        time_str = f"Time: {minutes:02d}:{seconds:02d}"
        
        # Check if approaching time limit
        if self.time_limit:
            remaining = self.time_limit - self.time_elapsed
            
            # Color timer based on remaining time
            if remaining <= 0:
                self.timer_label.setStyleSheet("color: #ff3333; font-weight: bold;")
                self._time_expired()
            elif remaining <= self.time_limit * 0.25:  # Last 25% of time
                self.timer_label.setStyleSheet("color: #ff3333; font-weight: bold;")
            elif remaining <= self.time_limit * 0.5:  # Last 50% of time
                self.timer_label.setStyleSheet("color: #ffcc00; font-weight: bold;")
            
            # Add remaining time to display
            time_str += f" (Remaining: {remaining // 60:02d}:{remaining % 60:02d})"
        
        self.timer_label.setText(time_str)
    
    def _time_expired(self):
        """Handle time expiration"""
        if self.timer.isActive():
            self.timer.stop()
            
            QMessageBox.warning(self, "Time Expired", "Your time for this puzzle has expired!")
            
            # Complete the attempt as unsuccessful
            self._complete_attempt(False)
    
    def reveal_hint(self):
        """Reveal the next available hint"""
        if not self.hints or self.hints_used >= len(self.hints):
            return
        
        # Get next hint
        hint_text = self.hints[self.hints_used]
        
        # Record hint usage in database (for tracking)
        if self.attempt_id:
            # Note: Our JSON hints don't have IDs, so we'll just pass the hint index
            success = self.main_window.game_state.use_hint(self.attempt_id, self.hints_used)
            if not success:
                logger.warning(f"Failed to record hint usage for attempt {self.attempt_id}")
        
        # Remove placeholder if it exists
        placeholder = self.hints_container.findChild(QLabel, "hintPlaceholder")
        if placeholder:
            placeholder.deleteLater()
        
        # Create hint widget
        hint_widget = QFrame()
        hint_widget.setObjectName(f"hint{self.hints_used + 1}")
        hint_widget.setProperty("class", "hint")
        hint_layout = QVBoxLayout(hint_widget)
        
        # Hint number
        hint_number = QLabel(f"Hint #{self.hints_used + 1}")
        hint_number.setProperty("class", "hintLabel")
        hint_layout.addWidget(hint_number)
        
        # Hint text
        hint_label = QLabel(hint_text)
        hint_label.setProperty("class", "hintText")
        hint_label.setWordWrap(True)
        hint_layout.addWidget(hint_label)
        
        # Point deduction (based on difficulty and hint number)
        deduction = 10 * (self.hints_used + 1)  # Progressive deduction: 10, 20, 30...
        if self.puzzle_data.get('difficulty') == 'Medium':
            deduction *= 1.5  # Higher deduction for medium difficulty
        elif self.puzzle_data.get('difficulty') == 'Hard':
            deduction *= 2  # Even higher for hard difficulty
            
        deduction = int(deduction)
        
        deduction_label = QLabel(f"-{deduction} points")
        deduction_label.setProperty("class", "hintDeduction")
        hint_layout.addWidget(deduction_label)
        
        # Add to container
        self.hints_container_layout.insertWidget(0, hint_widget)
        
        self.hints_used += 1
        
        # Disable hint button if all hints used
        if self.hints_used >= len(self.hints):
            self.hint_button.setEnabled(False)
            self.hint_button.setText("No More Hints")
    
    def submit_answer(self):
        """Submit the answer for evaluation"""
        # Get the answer
        answer = self.answer_input.text().strip()
        
        if not answer:
            return
            
        # Stop the timer
        if self.timer and self.timer.isActive():
            self.timer.stop()
        
        # Check the answer using the puzzle manager
        is_correct = False
        if self.puzzle_data and 'answer' in self.puzzle_data:
            # Make comparisons case-insensitive and ignore extra whitespace
            correct_answer = self.puzzle_data['answer'].lower().strip()
            user_answer = answer.lower().strip()
            
            # Handle multiple acceptable answers (if answer contains comma-separated values)
            if ',' in correct_answer:
                correct_parts = [part.strip() for part in correct_answer.split(',')]
                for part in correct_parts:
                    if part == user_answer:
                        is_correct = True
                        break
            # Also allow partial answers for longer answers
            elif len(correct_answer) > 20:
                if user_answer in correct_answer or correct_answer in user_answer:
                    is_correct = True
            else:
                is_correct = correct_answer == user_answer
        
        # Complete the attempt
        self._complete_attempt(is_correct)
        
        # Show result dialog
        self._show_result(is_correct)
    
    def _complete_attempt(self, successful):
        """Complete the current attempt"""
        if not self.attempt_id:
            return
            
        try:
            result = self.main_window.game_state.complete_puzzle_attempt(self.attempt_id, successful)
            if not result:
                logger.warning(f"Failed to complete attempt {self.attempt_id}")
                
            # Disable input and submit
            self.answer_input.setEnabled(False)
            self.submit_button.setEnabled(False)
            self.hint_button.setEnabled(False)
            
        except Exception as e:
            logger.error(f"Error completing puzzle attempt: {e}", exc_info=True)
    
    def _show_result(self, successful):
        """Show the result dialog"""
        dialog = ResultDialog(self, successful, self.time_elapsed, self.hints_used)
        dialog.exec()
        
        # Return to challenges screen
        self.main_window.goto_challenges()
    
    def confirm_exit(self):
        """Confirm before exiting the puzzle"""
        if self.timer and self.timer.isActive():
            reply = QMessageBox.question(
                self, 
                "Exit Puzzle", 
                "Are you sure you want to exit? Your progress will be lost.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # Stop timer and complete as unsuccessful
                self.timer.stop()
                if self.attempt_id:
                    self._complete_attempt(False)
                self.main_window.goto_challenges()
        else:
            self.main_window.goto_challenges()
    
    def refresh(self):
        """Reset puzzle display"""
        # Nothing to do here since the puzzle is always set explicitly
        pass


class ResultDialog(QDialog):
    """Dialog showing puzzle attempt results"""
    
    def __init__(self, parent, successful, time_taken, hints_used):
        """Initialize result dialog"""
        super().__init__(parent)
        self.successful = successful
        self.time_taken = time_taken
        self.hints_used = hints_used
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI components"""
        # Set up dialog
        self.setWindowTitle("Puzzle Result")
        self.setFixedSize(400, 300)
        self.setModal(True)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Result heading
        if self.successful:
            result_text = "Challenge Completed!"
            result_color = "#00ff99"
        else:
            result_text = "Challenge Failed"
            result_color = "#ff3333"
        
        result_label = QLabel(result_text)
        result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {result_color};")
        layout.addWidget(result_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        # Stats grid
        stats_grid = QGridLayout()
        stats_grid.setColumnStretch(1, 1)
        stats_grid.setVerticalSpacing(10)
        
        # Time taken
        stats_grid.addWidget(QLabel("Time taken:"), 0, 0)
        minutes = self.time_taken // 60
        seconds = self.time_taken % 60
        time_label = QLabel(f"{minutes:02d}:{seconds:02d}")
        time_label.setStyleSheet("font-weight: bold;")
        stats_grid.addWidget(time_label, 0, 1)
        
        # Hints used
        stats_grid.addWidget(QLabel("Hints used:"), 1, 0)
        hints_label = QLabel(f"{self.hints_used}")
        hints_label.setStyleSheet("font-weight: bold;")
        stats_grid.addWidget(hints_label, 1, 1)
        
        # Add stats to layout
        layout.addLayout(stats_grid)
        
        # Feedback message
        if self.successful:
            feedback = "Great job! You've successfully completed this challenge."
            if self.hints_used == 0:
                feedback += " Perfect score with no hints used!"
        else:
            feedback = "Don't worry! Learning from mistakes is part of the process. Try again with a different approach."
        
        feedback_label = QLabel(feedback)
        feedback_label.setWordWrap(True)
        feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(feedback_label)
        
        layout.addStretch()
        
        # Continue button
        continue_button = QPushButton("Continue")
        continue_button.setProperty("class", "primary")
        continue_button.clicked.connect(self.accept)
        layout.addWidget(continue_button)
        
        # Set dialog style
        self.setStyleSheet("""
            QDialog {
                background-color: #262626;
            }
            
            QLabel {
                color: #f0f0f0;
            }
            
            QPushButton {
                background-color: #0066cc;
                color: white;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #0077ee;
            }
        """) 