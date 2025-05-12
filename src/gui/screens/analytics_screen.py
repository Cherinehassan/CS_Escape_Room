#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analytics screen for Cybersecurity Escape Room
Shows detailed statistics and analysis of user progress
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                           QPushButton, QFrame, QGridLayout, QSpacerItem,
                           QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont, QColor

from ..utils.animation_effects import FlickerEffect


class PerformanceIndicator(QFrame):
    """Widget to display a performance metric with visual indicator"""
    
    def __init__(self, title, value, icon_name=None, indicator_color="#00ccff"):
        """
        Initialize performance indicator widget
        
        Args:
            title: Metric title
            value: Metric value
            icon_name: Optional icon name
            indicator_color: Color for the indicator
        """
        super().__init__()
        
        # Set style
        self.setStyleSheet(f"""
            PerformanceIndicator {{
                background-color: rgba(0, 0, 0, 0.3);
                border: 1px solid {indicator_color};
                border-radius: 5px;
                padding: 8px;
            }}
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        # Title
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        
        # Value
        self.value_label = QLabel(str(value))
        self.value_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {indicator_color};")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.value_label)


class CategoryAnalytics(QFrame):
    """Widget to display analytics for a specific challenge category"""
    
    def __init__(self, category_name, completion_rate, avg_time, difficulty_rating, color="#00ccff"):
        """
        Initialize category analytics widget
        
        Args:
            category_name: Name of category
            completion_rate: Percentage of completion
            avg_time: Average time to complete challenges
            difficulty_rating: Difficulty rating (1-10)
            color: Color for styling
        """
        super().__init__()
        
        # Set style
        self.setStyleSheet(f"""
            CategoryAnalytics {{
                background-color: rgba(0, 0, 0, 0.3);
                border: 1px solid {color};
                border-radius: 5px;
                padding: 10px;
            }}
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # Category name
        self.name_label = QLabel(category_name)
        self.name_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {color};")
        layout.addWidget(self.name_label)
        
        # Stats grid
        stats_layout = QGridLayout()
        stats_layout.setSpacing(5)
        
        # Completion rate
        stats_layout.addWidget(QLabel("Completion:"), 0, 0)
        completion_label = QLabel(f"{completion_rate}%")
        completion_label.setStyleSheet("font-weight: bold; color: #ffffff;")
        stats_layout.addWidget(completion_label, 0, 1)
        
        # Average time
        stats_layout.addWidget(QLabel("Avg Time:"), 1, 0)
        time_label = QLabel(f"{avg_time}")
        time_label.setStyleSheet("font-weight: bold; color: #ffffff;")
        stats_layout.addWidget(time_label, 1, 1)
        
        # Difficulty
        stats_layout.addWidget(QLabel("Difficulty:"), 2, 0)
        difficulty_label = QLabel(f"{difficulty_rating}/10")
        difficulty_label.setStyleSheet("font-weight: bold; color: #ffffff;")
        stats_layout.addWidget(difficulty_label, 2, 1)
        
        layout.addLayout(stats_layout)


class AnalyticsScreen(QWidget):
    """Screen for displaying detailed user performance analytics"""
    
    # Signals
    return_to_dashboard = pyqtSignal()  # Emitted when back button is clicked
    
    def __init__(self, puzzle_manager, user_data, parent=None):
        """
        Initialize analytics screen
        
        Args:
            puzzle_manager: PuzzleManager instance
            user_data: UserData instance
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.puzzle_manager = puzzle_manager
        self.user_data = user_data
        
        self._create_ui()
        self._connect_signals()
        self._apply_animations()
    
    def _create_ui(self):
        """Create the analytics UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Header section
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("PERFORMANCE ANALYTICS")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #00ccff;")
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        self.back_button = QPushButton("← BACK TO DASHBOARD")
        self.back_button.setFixedSize(200, 40)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.5);
                color: #cccccc;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
            }
            
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.7);
                color: #ffffff;
                border-color: #00ccff;
            }
        """)
        header_layout.addWidget(self.back_button)
        
        main_layout.addLayout(header_layout)
        
        # Key performance indicators
        kpi_layout = QHBoxLayout()
        kpi_layout.setSpacing(20)
        
        # Calculate KPIs
        total_puzzles = len(self.puzzle_manager.get_all_puzzles())
        completed_puzzles = len(self.user_data.completed_puzzles)
        completion_rate = int((completed_puzzles / total_puzzles) * 100) if total_puzzles > 0 else 0
        
        # Average completion time
        avg_completion_time = "00:00"
        if self.user_data.puzzle_completion_times:
            avg_time = sum(self.user_data.puzzle_completion_times.values()) / len(self.user_data.puzzle_completion_times)
            minutes = int(avg_time) // 60
            seconds = int(avg_time) % 60
            avg_completion_time = f"{minutes:02d}:{seconds:02d}"
        
        # Completion rate indicator
        completion_indicator = PerformanceIndicator(
            "Completion Rate", 
            f"{completion_rate}%", 
            indicator_color="#00ff99" if completion_rate > 75 else "#ffcc00" if completion_rate > 30 else "#ff6666"
        )
        kpi_layout.addWidget(completion_indicator)
        
        # Average time indicator
        time_indicator = PerformanceIndicator(
            "Avg. Completion Time",
            avg_completion_time,
            indicator_color="#00ccff"
        )
        kpi_layout.addWidget(time_indicator)
        
        # Fastest solve indicator
        fastest_solve = "N/A"
        if self.user_data.puzzle_completion_times:
            fastest_time = min(self.user_data.puzzle_completion_times.values())
            minutes = int(fastest_time) // 60
            seconds = int(fastest_time) % 60
            fastest_solve = f"{minutes:02d}:{seconds:02d}"
        
        fastest_indicator = PerformanceIndicator(
            "Fastest Solve",
            fastest_solve,
            indicator_color="#ff9900"
        )
        kpi_layout.addWidget(fastest_indicator)
        
        # Skill rating (0-100 based on completion and speed)
        skill_rating = 0
        if completed_puzzles > 0:
            time_factor = 0
            if self.user_data.puzzle_completion_times:
                avg_time = sum(self.user_data.puzzle_completion_times.values()) / len(self.user_data.puzzle_completion_times)
                # Faster times = higher score (max 50 points)
                time_factor = max(0, 50 - min(50, int(avg_time / 10)))
            
            # Completion factor (max 50 points)
            completion_factor = int((completion_rate / 100) * 50)
            
            skill_rating = time_factor + completion_factor
        
        skill_indicator = PerformanceIndicator(
            "Skill Rating",
            f"{skill_rating}/100",
            indicator_color="#cc33ff"
        )
        kpi_layout.addWidget(skill_indicator)
        
        main_layout.addLayout(kpi_layout)
        
        # Category performance section
        category_frame = QFrame()
        category_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 5px;")
        category_layout = QVBoxLayout(category_frame)
        
        category_title = QLabel("CATEGORY PERFORMANCE")
        category_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff;")
        category_layout.addWidget(category_title)
        
        # Grid for category analytics
        category_grid = QGridLayout()
        category_grid.setSpacing(15)
        
        # Get categories
        categories = set(puzzle.category for puzzle in self.puzzle_manager.get_all_puzzles())
        
        # Sample color palette for categories
        colors = [
            "#00ccff",  # Cyan
            "#00ff99",  # Green
            "#ff9900",  # Orange
            "#ff3366",  # Red
            "#cc33ff",  # Purple
            "#ffcc00"   # Yellow
        ]
        
        # Add category analytics widget for each category
        for i, category in enumerate(categories):
            category_puzzles = self.puzzle_manager.get_puzzles_by_category(category)
            total_in_category = len(category_puzzles)
            
            # Skip if no puzzles in category
            if total_in_category == 0:
                continue
                
            completed_in_category = sum(1 for puzzle in category_puzzles 
                                     if puzzle.id in self.user_data.completed_puzzles)
            
            completion_pct = int((completed_in_category / total_in_category) * 100)
            
            # Calculate average time for this category
            category_times = [self.user_data.puzzle_completion_times.get(puzzle.id, 0) 
                            for puzzle in category_puzzles 
                            if puzzle.id in self.user_data.puzzle_completion_times]
            
            avg_time = "N/A"
            if category_times:
                time_avg = sum(category_times) / len(category_times)
                minutes = int(time_avg) // 60
                seconds = int(time_avg) % 60
                avg_time = f"{minutes:02d}:{seconds:02d}"
            
            # Estimate difficulty based on average completion time and category
            # This is a placeholder - in a real app, difficulty would be determined by more factors
            difficulty_rating = 5  # Default middle difficulty
            if category_times:
                time_avg = sum(category_times) / len(category_times)
                # Higher times suggest higher difficulty
                difficulty_rating = min(10, max(1, int(time_avg / 60) + 3))
            
            color = colors[i % len(colors)]
            category_widget = CategoryAnalytics(
                category, completion_pct, avg_time, difficulty_rating, color
            )
            
            # Position in grid (3 columns)
            row = i // 3
            col = i % 3
            category_grid.addWidget(category_widget, row, col)
        
        category_layout.addLayout(category_grid)
        main_layout.addWidget(category_frame)
        
        # Challenge success rates section
        success_frame = QFrame()
        success_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 5px;")
        success_layout = QVBoxLayout(success_frame)
        
        success_title = QLabel("CHALLENGE INSIGHTS")
        success_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff;")
        success_layout.addWidget(success_title)
        
        # Details about completion rates, struggle areas, etc.
        insights_text = "Insights:"
        
        # Find most challenging puzzle (longest completion time)
        challenging_puzzle_name = "N/A"
        if self.user_data.puzzle_completion_times:
            challenging_puzzle_id = max(self.user_data.puzzle_completion_times, 
                                    key=self.user_data.puzzle_completion_times.get)
            challenging_puzzle = self.puzzle_manager.get_puzzle_by_id(challenging_puzzle_id)
            if challenging_puzzle:
                challenging_puzzle_name = challenging_puzzle.name
                challenging_time = self.user_data.puzzle_completion_times[challenging_puzzle_id]
                minutes = int(challenging_time) // 60
                seconds = int(challenging_time) % 60
                insights_text += f"\n• Most challenging puzzle: {challenging_puzzle_name} ({minutes:02d}:{seconds:02d})"
        
        # Find strongest category (highest completion percentage)
        strongest_category = "N/A"
        strongest_pct = 0
        
        for category in categories:
            category_puzzles = self.puzzle_manager.get_puzzles_by_category(category)
            total_in_category = len(category_puzzles)
            
            if total_in_category == 0:
                continue
                
            completed_in_category = sum(1 for puzzle in category_puzzles 
                                     if puzzle.id in self.user_data.completed_puzzles)
            
            completion_pct = int((completed_in_category / total_in_category) * 100)
            
            if completion_pct > strongest_pct:
                strongest_pct = completion_pct
                strongest_category = category
        
        if strongest_category != "N/A":
            insights_text += f"\n• Strongest category: {strongest_category} ({strongest_pct}% complete)"
        
        # Find areas for improvement (lowest completion rate)
        weakest_category = "N/A"
        weakest_pct = 100
        
        for category in categories:
            category_puzzles = self.puzzle_manager.get_puzzles_by_category(category)
            total_in_category = len(category_puzzles)
            
            if total_in_category == 0:
                continue
                
            completed_in_category = sum(1 for puzzle in category_puzzles 
                                     if puzzle.id in self.user_data.completed_puzzles)
            
            completion_pct = int((completed_in_category / total_in_category) * 100)
            
            if completed_in_category < total_in_category and completion_pct < weakest_pct:
                weakest_pct = completion_pct
                weakest_category = category
        
        if weakest_category != "N/A":
            insights_text += f"\n• Area for improvement: {weakest_category} ({weakest_pct}% complete)"
        
        # Overall progress assessment
        if completion_rate < 25:
            insights_text += "\n• You're just getting started! Try completing more challenges to build your skills."
        elif completion_rate < 50:
            insights_text += "\n• Good progress! You're developing your cybersecurity knowledge."
        elif completion_rate < 75:
            insights_text += "\n• Great work! You've mastered many of the challenges."
        elif completion_rate < 100:
            insights_text += "\n• Excellent! You're close to becoming a cybersecurity master."
        else:
            insights_text += "\n• Perfect! You've completed all challenges. Try to beat your best times!"
        
        insights_label = QLabel(insights_text)
        insights_label.setStyleSheet("color: #cccccc; font-size: 14px; line-height: 1.5;")
        insights_label.setWordWrap(True)
        success_layout.addWidget(insights_label)
        
        main_layout.addWidget(success_frame)
    
    def _connect_signals(self):
        """Connect signals to slots"""
        self.back_button.clicked.connect(self.return_to_dashboard.emit)
    
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
    
    def showEvent(self, event):
        """Handle show event"""
        super().showEvent(event)
        # Refresh data when shown
        self._refresh_data()
    
    def _refresh_data(self):
        """Refresh analytics data"""
        # This would update all widgets with fresh data
        # For now, we'll just recreate the UI since that handles everything
        self._clear_ui()
        self._create_ui()
        self._connect_signals()
        self._apply_animations()
    
    def _clear_ui(self):
        """Clear existing UI elements"""
        # Remove all widgets from layout
        if self.layout():
            while self.layout().count():
                item = self.layout().takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            
            # Delete layout
            QWidget().setLayout(self.layout()) 