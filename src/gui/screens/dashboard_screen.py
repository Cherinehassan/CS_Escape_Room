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
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("ESCAPE ROOM DASHBOARD")
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #00ccff;")
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        self.back_button = QPushButton("Return to Menu")
        self.back_button.setFixedSize(120, 30)
        header_layout.addWidget(self.back_button)
        
        main_layout.addLayout(header_layout)
        
        # Stats bar
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(8)
        
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
        content_layout.setSpacing(10)
        
        # Left side - category progress
        category_frame = QFrame()
        category_frame.setFrameShape(QFrame.Shape.StyledPanel)
        category_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 5px;")
        
        category_layout = QVBoxLayout(category_frame)
        category_layout.setContentsMargins(8, 8, 8, 8)
        
        category_label = QLabel("CATEGORY PROGRESS")
        category_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;")
        category_layout.addWidget(category_label)
        
        # Create a scroll area for categories
        categories_scroll = QScrollArea()
        categories_scroll.setWidgetResizable(True)
        categories_scroll.setFrameShape(QFrame.Shape.NoFrame)
        categories_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Create a container for category widgets
        self.categories_container = QWidget()
        self.categories_layout = QVBoxLayout(self.categories_container)
        self.categories_layout.setSpacing(8)
        self.categories_layout.setContentsMargins(0, 0, 0, 0)
        
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
            self.categories_layout.addWidget(category_widget)
        
        self.categories_layout.addStretch()
        
        categories_scroll.setWidget(self.categories_container)
        category_layout.addWidget(categories_scroll)
        
        content_layout.addWidget(category_frame, 1)
        
        # Right side - achievements
        achievement_frame = QFrame()
        achievement_frame.setFrameShape(QFrame.Shape.StyledPanel)
        achievement_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 5px;")
        
        achievement_layout = QVBoxLayout(achievement_frame)
        achievement_layout.setContentsMargins(8, 8, 8, 8)
        
        achievement_label = QLabel("ACHIEVEMENTS")
        achievement_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;")
        achievement_layout.addWidget(achievement_label)
        
        # Achievement scroll area
        achievement_scroll = QScrollArea()
        achievement_scroll.setWidgetResizable(True)
        achievement_scroll.setFrameShape(QFrame.Shape.NoFrame)
        achievement_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.achievements_container = QWidget()
        self.achievements_layout = QVBoxLayout(self.achievements_container)
        self.achievements_layout.setSpacing(8)
        self.achievements_layout.setContentsMargins(0, 0, 0, 0)
        
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
            self.achievements_layout.addWidget(achievement_widget)
        
        self.achievements_layout.addStretch()
        achievement_scroll.setWidget(self.achievements_container)
        achievement_layout.addWidget(achievement_scroll)
        
        content_layout.addWidget(achievement_frame, 1)
        
        main_layout.addLayout(content_layout, 1)
        
        # Bottom section - available challenges
        challenge_frame = QFrame()
        challenge_frame.setFrameShape(QFrame.Shape.StyledPanel)
        challenge_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 5px;")
        
        challenge_layout = QVBoxLayout(challenge_frame)
        challenge_layout.setContentsMargins(8, 8, 8, 8)
        
        challenge_label = QLabel("AVAILABLE CHALLENGES")
        challenge_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;")
        challenge_layout.addWidget(challenge_label)
        
        # Create scroll area for challenges
        challenges_scroll = QScrollArea()
        challenges_scroll.setWidgetResizable(True)
        challenges_scroll.setFrameShape(QFrame.Shape.NoFrame)
        challenges_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Create container for challenge buttons
        self.challenges_container = QWidget()
        self.challenges_layout = QHBoxLayout(self.challenges_container)
        self.challenges_layout.setSpacing(10)
        self.challenges_layout.setContentsMargins(0, 0, 0, 0)
        
        # Show first 6 incomplete puzzles
        incomplete_puzzles = [p for p in self.puzzle_manager.get_all_puzzles() 
                             if p.id not in self.user_data.completed_puzzles]
        puzzles_to_show = incomplete_puzzles[:6]
        
        for i, puzzle in enumerate(puzzles_to_show):
            challenge_button = QPushButton(puzzle.name)
            challenge_button.setProperty("puzzle_id", puzzle.id)
            challenge_button.clicked.connect(self._on_challenge_clicked)
            
            # Style based on difficulty
            if puzzle.difficulty == "Easy":
                challenge_button.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(0, 153, 0, 0.3);
                        color: #ffffff;
                        border: 1px solid #00cc00;
                        border-radius: 5px;
                        padding: 8px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: rgba(0, 204, 0, 0.5);
                    }
                """)
            elif puzzle.difficulty == "Medium":
                challenge_button.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(204, 102, 0, 0.3);
                        color: #ffffff;
                        border: 1px solid #ff9900;
                        border-radius: 5px;
                        padding: 8px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 153, 0, 0.5);
                    }
                """)
            else:  # Hard
                challenge_button.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(204, 0, 0, 0.3);
                        color: #ffffff;
                        border: 1px solid #ff3333;
                        border-radius: 5px;
                        padding: 8px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 51, 51, 0.5);
                    }
                """)
            
            # Add to layout (no row/column parameters for QHBoxLayout)
            self.challenges_layout.addWidget(challenge_button)
        
        # Add "View All" button
        view_all_button = QPushButton("View All Challenges")
        view_all_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.3);
                color: #00ccff;
                border: 1px solid #00ccff;
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(0, 204, 255, 0.2);
            }
        """)
        view_all_button.clicked.connect(lambda: self.challenge_selected.emit(0))
        self.challenges_layout.addWidget(view_all_button)
        
        challenges_scroll.setWidget(self.challenges_container)
        challenge_layout.addWidget(challenges_scroll)
        
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
        # Update time stats
        self.user_data.update_time_played()
        total_time_played = self.user_data.time_played
        hours = int(total_time_played // 3600)
        minutes = int((total_time_played % 3600) // 60)
        time_played_str = f"{hours}h {minutes}m"
        self.time_played_widget.value_label.setText(time_played_str)
        
        # Get fastest completion time
        fastest_time = 0
        if self.user_data.puzzle_completion_times:
            fastest_time = min(self.user_data.puzzle_completion_times.values())
        fastest_time_str = self._format_time(fastest_time)
        self.fastest_solve_widget.value_label.setText(fastest_time_str)
        
        # Calculate completion rate
        total_puzzles = len(self.puzzle_manager.get_all_puzzles())
        completed_puzzles = len(self.user_data.completed_puzzles)
        completion_rate = int((completed_puzzles / total_puzzles) * 100) if total_puzzles > 0 else 0
        self.puzzles_completed_widget.value_label.setText(f"{completed_puzzles}/{total_puzzles} ({completion_rate}%)")
        
        # Calculate average time
        avg_time = 0
        if self.user_data.puzzle_completion_times:
            avg_time = sum(self.user_data.puzzle_completion_times.values()) / len(self.user_data.puzzle_completion_times)
        avg_time_str = self._format_time(avg_time)
        self.avg_time_widget.value_label.setText(avg_time_str)
        
        # Update category progress widgets
        if hasattr(self, 'categories_layout'):
            # Clear existing category widgets
            for i in reversed(range(self.categories_layout.count())):
                item = self.categories_layout.itemAt(i)
                if item and item.widget():
                    item.widget().deleteLater()
            
            # Create category progress widgets
            categories = {}
            for puzzle in self.puzzle_manager.get_all_puzzles():
                category = puzzle.category
                if category not in categories:
                    categories[category] = {"total": 0, "completed": 0}
                categories[category]["total"] += 1
                if puzzle.id in self.user_data.completed_puzzles:
                    categories[category]["completed"] += 1
            
            # Category colors
            category_colors = {
                "Cryptography": "#00ccff",
                "Authentication": "#ff9900",
                "Web Security": "#cc00ff",
                "Network Security": "#00ff99",
                "Social Engineering": "#ff6666",
                "Malware": "#ff3333",
                "Hashing": "#33ccff",
                "Encryption": "#66ff66",
                "Security Management": "#ffcc00",
                "Secure Coding": "#ff99cc"
            }
            
            # Default color for any other categories
            default_color = "#aaaaaa"
            
            # Add category widgets
            for category, stats in categories.items():
                color = category_colors.get(category, default_color)
                category_widget = CategoryProgressWidget(
                    category, stats["total"], stats["completed"], color
                )
                self.categories_layout.addWidget(category_widget)
            
            # Add stretch at the end
            self.categories_layout.addStretch()
        
        # Update achievements
        if hasattr(self, 'achievements_layout'):
            # Clear existing achievement widgets
            for i in reversed(range(self.achievements_layout.count())):
                item = self.achievements_layout.itemAt(i)
                if item and item.widget():
                    item.widget().deleteLater()
            
            # Example achievements (in a real app, these would come from an achievement manager)
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
                    "unlocked": completion_rate >= 50
                },
                {
                    "title": "Master Escapist",
                    "description": "Complete all puzzles",
                    "unlocked": completion_rate == 100
                }
            ]
            
            # Create achievement widgets
            for achievement in achievements:
                achievement_widget = AchievementWidget(
                    achievement["title"],
                    achievement["description"],
                    unlocked=achievement["unlocked"]
                )
                self.achievements_layout.addWidget(achievement_widget)
            
            # Add stretch at the end
            self.achievements_layout.addStretch()
        
        # Update available challenges
        if hasattr(self, 'challenges_layout'):
            # Clear existing challenge widgets
            for i in reversed(range(self.challenges_layout.count())):
                item = self.challenges_layout.itemAt(i)
                if item and item.widget():
                    item.widget().deleteLater()
            
            # Get recommended puzzles
            recommended_puzzles = self.user_data.get_recommended_puzzles(self.puzzle_manager, 3)
            
            # Create challenge widgets
            for puzzle in recommended_puzzles:
                challenge_button = QPushButton(puzzle.title)
                challenge_button.setProperty("puzzle_id", puzzle.id)
                challenge_button.clicked.connect(self._on_challenge_clicked)
                
                # Style based on difficulty
                if puzzle.difficulty == "Easy":
                    challenge_button.setStyleSheet("""
                        QPushButton {
                            background-color: rgba(0, 153, 0, 0.3);
                            color: #ffffff;
                            border: 1px solid #00cc00;
                            border-radius: 5px;
                            padding: 8px;
                            font-size: 12px;
                        }
                        QPushButton:hover {
                            background-color: rgba(0, 204, 0, 0.5);
                        }
                    """)
                elif puzzle.difficulty == "Medium":
                    challenge_button.setStyleSheet("""
                        QPushButton {
                            background-color: rgba(204, 102, 0, 0.3);
                            color: #ffffff;
                            border: 1px solid #ff9900;
                            border-radius: 5px;
                            padding: 8px;
                            font-size: 12px;
                        }
                        QPushButton:hover {
                            background-color: rgba(255, 153, 0, 0.5);
                        }
                    """)
                else:  # Hard
                    challenge_button.setStyleSheet("""
                        QPushButton {
                            background-color: rgba(204, 0, 0, 0.3);
                            color: #ffffff;
                            border: 1px solid #ff3333;
                            border-radius: 5px;
                            padding: 8px;
                            font-size: 12px;
                        }
                        QPushButton:hover {
                            background-color: rgba(255, 51, 51, 0.5);
                        }
                    """)
                
                self.challenges_layout.addWidget(challenge_button)
            
            # Add "View All Challenges" button
            view_all_button = QPushButton("View All Challenges")
            view_all_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(0, 0, 0, 0.3);
                    color: #00ccff;
                    border: 1px solid #00ccff;
                    border-radius: 5px;
                    padding: 8px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: rgba(0, 204, 255, 0.2);
                }
            """)
            view_all_button.clicked.connect(self.challenge_selected.emit)
            self.challenges_layout.addWidget(view_all_button) 