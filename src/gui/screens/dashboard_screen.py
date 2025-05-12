#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dashboard screen for Cybersecurity Escape Room
Shows user progress, stats, and available challenges
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QProgressBar, QFrame, QScrollArea,
                            QGridLayout, QSizePolicy)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon

from ..utils.animation_effects import FlickerEffect, PulseAnimation


class CategoryProgressWidget(QFrame):
    """Widget showing progress in a specific puzzle category"""
    
    def __init__(self, category_name, total_puzzles, completed_puzzles, category_color):
        """
        Initialize category progress widget
        
        Args:
            category_name: Name of the category
            total_puzzles: Total number of puzzles in this category
            completed_puzzles: Number of completed puzzles
            category_color: Color hex code for this category
        """
        super().__init__()
        
        # Set up frame
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setStyleSheet(f"""
            CategoryProgressWidget {{
                border: 1px solid {category_color};
                border-radius: 5px;
                background-color: rgba(0, 0, 0, 0.3);
                padding: 10px;
            }}
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Category name
        self.name_label = QLabel(category_name)
        self.name_label.setStyleSheet(f"color: {category_color}; font-weight: bold; font-size: 14px;")
        layout.addWidget(self.name_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, total_puzzles)
        self.progress_bar.setValue(completed_puzzles)
        self.progress_bar.setFormat(f"%v/%m puzzles completed")
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {category_color};
                border-radius: 5px;
                background-color: rgba(0, 0, 0, 0.6);
                color: white;
                text-align: center;
            }}
            
            QProgressBar::chunk {{
                background-color: {category_color};
            }}
        """)
        layout.addWidget(self.progress_bar)
        
        # Completion rate
        completion_rate = int((completed_puzzles / total_puzzles) * 100) if total_puzzles > 0 else 0
        self.rate_label = QLabel(f"Completion: {completion_rate}%")
        self.rate_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.rate_label)


class AchievementWidget(QFrame):
    """Widget showing an achievement"""
    
    def __init__(self, title, description, icon_path=None, unlocked=False):
        """
        Initialize achievement widget
        
        Args:
            title: Achievement title
            description: Achievement description
            icon_path: Path to achievement icon
            unlocked: Whether achievement is unlocked
        """
        super().__init__()
        
        # Set up frame
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        
        # Set style based on unlock status
        if unlocked:
            self.setStyleSheet("""
                AchievementWidget {
                    border: 1px solid #00cc99;
                    border-radius: 5px;
                    background-color: rgba(0, 204, 153, 0.1);
                    padding: 5px;
                }
            """)
        else:
            self.setStyleSheet("""
                AchievementWidget {
                    border: 1px solid #555555;
                    border-radius: 5px;
                    background-color: rgba(50, 50, 50, 0.3);
                    padding: 5px;
                    color: #888888;
                }
            """)
        
        # Create layout
        layout = QHBoxLayout(self)
        
        # Icon
        self.icon_label = QLabel()
        if icon_path and unlocked:
            icon = QPixmap(icon_path)
            self.icon_label.setPixmap(icon.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            # Show a locked icon
            self.icon_label.setText("🔒")
            self.icon_label.setStyleSheet("font-size: 24px; color: #888888;")
        
        self.icon_label.setFixedSize(40, 40)
        layout.addWidget(self.icon_label)
        
        # Text information
        text_layout = QVBoxLayout()
        
        self.title_label = QLabel(title)
        if unlocked:
            self.title_label.setStyleSheet("font-weight: bold; color: #00cc99;")
        else:
            self.title_label.setStyleSheet("font-weight: bold; color: #888888;")
        text_layout.addWidget(self.title_label)
        
        desc_text = description if unlocked else "???"
        self.description_label = QLabel(desc_text)
        self.description_label.setWordWrap(True)
        text_layout.addWidget(self.description_label)
        
        layout.addLayout(text_layout)
        layout.setStretchFactor(text_layout, 1)


class TimeStatWidget(QFrame):
    """Widget showing time statistics"""
    
    def __init__(self, title, value, icon_name=None):
        """
        Initialize time stat widget
        
        Args:
            title: Stat title
            value: Stat value
            icon_name: Icon name
        """
        super().__init__()
        
        # Set frame style
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setStyleSheet("""
            TimeStatWidget {
                border: 1px solid #3c3c3c;
                border-radius: 5px;
                background-color: rgba(30, 30, 30, 0.5);
                padding: 8px;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setSpacing(2)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Title
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: bold;")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.value_label)


class DashboardScreen(QWidget):
    """Main dashboard screen showing user progress"""
    
    # Signals
    challenge_selected = pyqtSignal(int)  # Emitted when a challenge is selected
    return_to_menu = pyqtSignal()        # Emitted when back button is clicked
    
    def __init__(self, puzzle_manager, user_data, parent=None):
        """
        Initialize dashboard screen
        
        Args:
            puzzle_manager: PuzzleManager instance
            user_data: UserData instance for the current user
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.puzzle_manager = puzzle_manager
        self.user_data = user_data
        
        self._create_ui()
        self._connect_signals()
        self._apply_animations()
    
    def _create_ui(self):
        """Create the dashboard UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("ESCAPE ROOM DASHBOARD")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #00ccff;")
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        self.back_button = QPushButton("Return to Menu")
        self.back_button.setFixedSize(150, 40)
        header_layout.addWidget(self.back_button)
        
        main_layout.addLayout(header_layout)
        
        # Stats bar
        stats_layout = QHBoxLayout()
        
        # Get user stats
        completed_puzzles = len(self.user_data.completed_puzzles)
        total_puzzles = len(self.puzzle_manager.get_all_puzzles())
        completion_pct = int((completed_puzzles / total_puzzles) * 100) if total_puzzles > 0 else 0
        
        # Time played stats
        self.time_played_widget = TimeStatWidget("Time Played", 
                                               self._format_time(self.user_data.time_played))
        stats_layout.addWidget(self.time_played_widget)
        
        # Fastest solve stat
        fastest_time = min(self.user_data.puzzle_completion_times.values()) if self.user_data.puzzle_completion_times else 0
        self.fastest_solve_widget = TimeStatWidget("Fastest Solve", 
                                                self._format_time(fastest_time))
        stats_layout.addWidget(self.fastest_solve_widget)
        
        # Average time stat
        avg_time = sum(self.user_data.puzzle_completion_times.values()) / len(self.user_data.puzzle_completion_times) \
            if self.user_data.puzzle_completion_times else 0
        self.avg_time_widget = TimeStatWidget("Average Solve Time", 
                                           self._format_time(avg_time))
        stats_layout.addWidget(self.avg_time_widget)
        
        # Puzzles completed stat
        self.puzzles_completed_widget = TimeStatWidget("Puzzles Completed", 
                                                    f"{completed_puzzles}/{total_puzzles} ({completion_pct}%)")
        stats_layout.addWidget(self.puzzles_completed_widget)
        
        main_layout.addLayout(stats_layout)
        
        # Content section
        content_layout = QHBoxLayout()
        
        # Left side - category progress
        category_frame = QFrame()
        category_frame.setFrameShape(QFrame.Shape.StyledPanel)
        category_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 5px;")
        
        category_layout = QVBoxLayout(category_frame)
        category_layout.setContentsMargins(10, 10, 10, 10)
        
        category_label = QLabel("CATEGORY PROGRESS")
        category_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        category_layout.addWidget(category_label)
        
        # Add category progress widgets
        categories = set(puzzle.category for puzzle in self.puzzle_manager.get_all_puzzles())
        
        for category in categories:
            category_puzzles = self.puzzle_manager.get_puzzles_by_category(category)
            total_in_category = len(category_puzzles)
            completed_in_category = sum(1 for puzzle in category_puzzles 
                                     if puzzle.id in self.user_data.completed_puzzles)
            
            category_color = "#00ccff"  # Default color
            if hasattr(self, "theme_manager"):
                category_color = self.theme_manager.get_category_color(category)
                
            category_widget = CategoryProgressWidget(
                category, total_in_category, completed_in_category, category_color)
            category_layout.addWidget(category_widget)
        
        category_layout.addStretch()
        content_layout.addWidget(category_frame, 1)
        
        # Right side - achievements
        achievement_frame = QFrame()
        achievement_frame.setFrameShape(QFrame.Shape.StyledPanel)
        achievement_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 5px;")
        
        achievement_layout = QVBoxLayout(achievement_frame)
        achievement_layout.setContentsMargins(10, 10, 10, 10)
        
        achievement_label = QLabel("ACHIEVEMENTS")
        achievement_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        achievement_layout.addWidget(achievement_label)
        
        # Achievement scroll area
        achievement_scroll = QScrollArea()
        achievement_scroll.setWidgetResizable(True)
        achievement_scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        achievement_container = QWidget()
        achievement_container_layout = QVBoxLayout(achievement_container)
        
        # Example achievements
        achievements = [
            {
                "title": "First Steps",
                "description": "Complete your first puzzle",
                "unlocked": len(self.user_data.completed_puzzles) > 0
            },
            {
                "title": "Crypto Master",
                "description": "Complete all Cryptography puzzles",
                "unlocked": self._is_category_complete("Cryptography")
            },
            {
                "title": "Social Guru",
                "description": "Complete all Social Engineering puzzles",
                "unlocked": self._is_category_complete("Social Engineering")
            },
            {
                "title": "Hash Cracker",
                "description": "Complete all Hashing puzzles",
                "unlocked": self._is_category_complete("Hashing")
            },
            {
                "title": "Secure Access",
                "description": "Complete all Authentication puzzles",
                "unlocked": self._is_category_complete("Authentication")
            },
            {
                "title": "Encryption Expert",
                "description": "Complete all Encryption puzzles",
                "unlocked": self._is_category_complete("Encryption")
            },
            {
                "title": "Speed Demon",
                "description": "Complete a puzzle in under 30 seconds",
                "unlocked": any(time < 30 for time in self.user_data.puzzle_completion_times.values())
            },
            {
                "title": "Half Way There",
                "description": "Complete 50% of all puzzles",
                "unlocked": completion_pct >= 50
            },
            {
                "title": "Master Escapist",
                "description": "Complete all puzzles",
                "unlocked": completion_pct == 100
            }
        ]
        
        for achievement in achievements:
            achievement_widget = AchievementWidget(
                achievement["title"],
                achievement["description"],
                unlocked=achievement["unlocked"]
            )
            achievement_container_layout.addWidget(achievement_widget)
        
        achievement_container_layout.addStretch()
        achievement_scroll.setWidget(achievement_container)
        achievement_layout.addWidget(achievement_scroll)
        
        content_layout.addWidget(achievement_frame, 1)
        
        main_layout.addLayout(content_layout, 1)
        
        # Bottom section - available challenges
        challenge_frame = QFrame()
        challenge_frame.setFrameShape(QFrame.Shape.StyledPanel)
        challenge_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 5px;")
        
        challenge_layout = QVBoxLayout(challenge_frame)
        
        challenge_header = QLabel("AVAILABLE CHALLENGES")
        challenge_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        challenge_layout.addWidget(challenge_header)
        
        # Challenge grid
        challenge_grid = QGridLayout()
        challenge_grid.setHorizontalSpacing(10)
        challenge_grid.setVerticalSpacing(10)
        
        # Show first 6 incomplete puzzles
        incomplete_puzzles = [puzzle for puzzle in self.puzzle_manager.get_all_puzzles() 
                             if puzzle.id not in self.user_data.completed_puzzles]
        
        for i, puzzle in enumerate(incomplete_puzzles[:6]):
            challenge_button = QPushButton(puzzle.name)
            challenge_button.setProperty("puzzle_id", puzzle.id)
            challenge_button.setMinimumHeight(60)
            challenge_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(10, 10, 10, 0.8);
                    color: #ffffff;
                    border: 1px solid #3c3c3c;
                    border-radius: 4px;
                    font-weight: bold;
                    text-align: left;
                    padding: 8px;
                }}
                
                QPushButton:hover {{
                    background-color: rgba(30, 30, 30, 0.8);
                    border: 1px solid #00ccff;
                }}
            """)
            challenge_button.clicked.connect(self._on_challenge_clicked)
            
            # Position in grid (3 columns)
            row = i // 3
            col = i % 3
            challenge_grid.addWidget(challenge_button, row, col)
        
        challenge_layout.addLayout(challenge_grid)
        main_layout.addWidget(challenge_frame)
    
    def _connect_signals(self):
        """Connect signals to slots"""
        self.back_button.clicked.connect(self.return_to_menu.emit)
    
    def _on_challenge_clicked(self):
        """Handle challenge button click"""
        button = self.sender()
        puzzle_id = button.property("puzzle_id")
        self.challenge_selected.emit(puzzle_id)
    
    def _apply_animations(self):
        """Apply animations to dashboard elements"""
        # Flicker effect on title
        self.title_flicker = FlickerEffect(
            self.title_label, 
            color="#00ccff", 
            intensity=0.3,
            interval_range=(2000, 5000)
        )
        self.title_flicker.start()
    
    def _format_time(self, seconds):
        """
        Format time in seconds to mm:ss format
        
        Args:
            seconds: Time in seconds
            
        Returns:
            str: Formatted time string
        """
        if not seconds:
            return "00:00"
            
        minutes = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{minutes:02d}:{secs:02d}"
    
    def _is_category_complete(self, category):
        """
        Check if all puzzles in a category are completed
        
        Args:
            category: Category name
            
        Returns:
            bool: True if all puzzles in the category are completed
        """
        category_puzzles = self.puzzle_manager.get_puzzles_by_category(category)
        return all(puzzle.id in self.user_data.completed_puzzles for puzzle in category_puzzles)
    
    def set_theme_manager(self, theme_manager):
        """
        Set theme manager for styling
        
        Args:
            theme_manager: ThemeManager instance
        """
        self.theme_manager = theme_manager
        
    def showEvent(self, event):
        """Handle show event to refresh data"""
        super().showEvent(event)
        # Refresh data whenever shown
        self._refresh_data()
    
    def _refresh_data(self):
        """Refresh dashboard data"""
        # Update stats
        completed_puzzles = len(self.user_data.completed_puzzles)
        total_puzzles = len(self.puzzle_manager.get_all_puzzles())
        completion_pct = int((completed_puzzles / total_puzzles) * 100) if total_puzzles > 0 else 0
        
        # Update time played
        self.time_played_widget.value_label.setText(self._format_time(self.user_data.time_played))
        
        # Update fastest solve
        fastest_time = min(self.user_data.puzzle_completion_times.values()) if self.user_data.puzzle_completion_times else 0
        self.fastest_solve_widget.value_label.setText(self._format_time(fastest_time))
        
        # Update average time
        avg_time = sum(self.user_data.puzzle_completion_times.values()) / len(self.user_data.puzzle_completion_times) \
            if self.user_data.puzzle_completion_times else 0
        self.avg_time_widget.value_label.setText(self._format_time(avg_time))
        
        # Update puzzles completed
        self.puzzles_completed_widget.value_label.setText(
            f"{completed_puzzles}/{total_puzzles} ({completion_pct}%)"
        ) 