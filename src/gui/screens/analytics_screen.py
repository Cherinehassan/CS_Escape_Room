#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analytics screen for Cybersecurity Escape Room
Shows detailed statistics and analysis of user progress
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                           QPushButton, QFrame, QGridLayout, QSpacerItem,
                           QSizePolicy, QScrollArea)
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
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header section
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("PERFORMANCE ANALYTICS")
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #00ccff;")
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        self.back_button = QPushButton("← BACK TO DASHBOARD")
        self.back_button.setFixedSize(180, 30)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.5);
                color: #cccccc;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 6px;
                font-size: 12px;
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
        self.kpi_layout = QHBoxLayout()
        self.kpi_layout.setSpacing(10)
        
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
            "Completion Rate", f"{completion_rate}%", indicator_color="#00cc99"
        )
        self.kpi_layout.addWidget(completion_indicator)
        
        # Average time indicator
        avg_time_indicator = PerformanceIndicator(
            "Avg. Completion Time", avg_completion_time, indicator_color="#ff9900"
        )
        self.kpi_layout.addWidget(avg_time_indicator)
        
        # Fastest completion indicator
        fastest_time = "00:00"
        if self.user_data.puzzle_completion_times:
            fastest = min(self.user_data.puzzle_completion_times.values())
            minutes = int(fastest) // 60
            seconds = int(fastest) % 60
            fastest_time = f"{minutes:02d}:{seconds:02d}"
        
        fastest_indicator = PerformanceIndicator(
            "Fastest Solve", fastest_time, indicator_color="#00ccff"
        )
        self.kpi_layout.addWidget(fastest_indicator)
        
        # Average attempts indicator
        avg_attempts = 0
        if self.user_data.puzzle_attempts and self.user_data.completed_puzzles:
            completed_attempts = sum(self.user_data.puzzle_attempts.get(pid, 1) 
                                  for pid in self.user_data.completed_puzzles)
            avg_attempts = completed_attempts / len(self.user_data.completed_puzzles)
            
        attempts_indicator = PerformanceIndicator(
            "Avg. Attempts", f"{avg_attempts:.1f}", indicator_color="#cc00ff"
        )
        self.kpi_layout.addWidget(attempts_indicator)
        
        main_layout.addLayout(self.kpi_layout)
        
        # Category analytics section
        category_frame = QFrame()
        category_frame.setFrameShape(QFrame.Shape.StyledPanel)
        category_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 5px;")
        
        category_layout = QVBoxLayout(category_frame)
        category_layout.setContentsMargins(10, 10, 10, 10)
        
        category_title = QLabel("CATEGORY ANALYTICS")
        category_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;")
        category_layout.addWidget(category_title)
        
        # Create scroll area for categories
        categories_scroll = QScrollArea()
        categories_scroll.setWidgetResizable(True)
        categories_scroll.setFrameShape(QFrame.Shape.NoFrame)
        categories_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Create container for category analytics
        self.categories_container = QWidget()
        self.categories_layout = QVBoxLayout(self.categories_container)
        self.categories_layout.setSpacing(8)
        self.categories_layout.setContentsMargins(0, 0, 0, 0)
        
        # Get category data
        categories = {}
        difficulty_ratings = {
            "Easy": 3,
            "Medium": 6,
            "Hard": 9
        }
        
        for puzzle in self.puzzle_manager.get_all_puzzles():
            category = puzzle.category
            if category not in categories:
                categories[category] = {
                    "total": 0,
                    "completed": 0,
                    "times": [],
                    "difficulty_sum": 0
                }
            
            categories[category]["total"] += 1
            categories[category]["difficulty_sum"] += difficulty_ratings.get(puzzle.difficulty, 5)
            
            if puzzle.id in self.user_data.completed_puzzles:
                categories[category]["completed"] += 1
                if puzzle.id in self.user_data.puzzle_completion_times:
                    categories[category]["times"].append(self.user_data.puzzle_completion_times[puzzle.id])
        
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
        
        # Sort categories by completion rate (highest first)
        sorted_categories = sorted(
            categories.items(),
            key=lambda x: (x[1]["completed"] / x[1]["total"]) if x[1]["total"] > 0 else 0,
            reverse=True
        )
        
        # Add category analytics widgets
        for category_name, data in sorted_categories:
            # Calculate metrics
            completion_rate = int((data["completed"] / data["total"]) * 100) if data["total"] > 0 else 0
            
            avg_time = "N/A"
            if data["times"]:
                time_in_seconds = sum(data["times"]) / len(data["times"])
                minutes = int(time_in_seconds) // 60
                seconds = int(time_in_seconds) % 60
                avg_time = f"{minutes:02d}:{seconds:02d}"
            
            difficulty_rating = round(data["difficulty_sum"] / data["total"]) if data["total"] > 0 else 0
            
            # Create widget
            color = category_colors.get(category_name, default_color)
            category_widget = CategoryAnalytics(
                category_name, completion_rate, avg_time, difficulty_rating, color
            )
            self.categories_layout.addWidget(category_widget)
        
        categories_scroll.setWidget(self.categories_container)
        category_layout.addWidget(categories_scroll)
        main_layout.addWidget(category_frame)
        
        # Performance charts section
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(10)
        
        # Performance over time chart
        performance_frame = QFrame()
        performance_frame.setFrameShape(QFrame.Shape.StyledPanel)
        performance_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 5px;")
        
        performance_layout = QVBoxLayout(performance_frame)
        performance_layout.setContentsMargins(10, 10, 10, 10)
        
        self.performance_chart_label = QLabel("PERFORMANCE OVER TIME")
        self.performance_chart_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;")
        performance_layout.addWidget(self.performance_chart_label)
        
        # Create container for performance chart
        self.performance_chart_container = QWidget()
        self.performance_chart_layout = QVBoxLayout(self.performance_chart_container)
        self.performance_chart_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add placeholder chart
        chart_placeholder = QLabel("Chart placeholder - would show completion times over time")
        chart_placeholder.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.3);
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 20px;
            color: #aaaaaa;
            font-size: 12px;
        """)
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.performance_chart_layout.addWidget(chart_placeholder)
        
        performance_layout.addWidget(self.performance_chart_container)
        charts_layout.addWidget(performance_frame)
        
        # Difficulty distribution chart
        difficulty_frame = QFrame()
        difficulty_frame.setFrameShape(QFrame.Shape.StyledPanel)
        difficulty_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 5px;")
        
        difficulty_layout = QVBoxLayout(difficulty_frame)
        difficulty_layout.setContentsMargins(10, 10, 10, 10)
        
        self.difficulty_chart_label = QLabel("PUZZLE DIFFICULTY DISTRIBUTION")
        self.difficulty_chart_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;")
        difficulty_layout.addWidget(self.difficulty_chart_label)
        
        # Create container for difficulty chart
        self.difficulty_chart_container = QWidget()
        self.difficulty_chart_layout = QVBoxLayout(self.difficulty_chart_container)
        self.difficulty_chart_layout.setContentsMargins(0, 0, 0, 0)
        
        # Count puzzles by difficulty
        difficulty_counts = {"Easy": 0, "Medium": 0, "Hard": 0}
        for puzzle in self.puzzle_manager.get_all_puzzles():
            if puzzle.difficulty in difficulty_counts:
                difficulty_counts[puzzle.difficulty] += 1
        
        # Create difficulty distribution display
        difficulty_display_layout = QHBoxLayout()
        
        for difficulty, count in difficulty_counts.items():
            if difficulty == "Easy":
                color = "#00cc00"
            elif difficulty == "Medium":
                color = "#ff9900"
            else:  # Hard
                color = "#ff3333"
            
            difficulty_widget = QFrame()
            difficulty_widget.setStyleSheet(f"""
                background-color: rgba(0, 0, 0, 0.3);
                border: 1px solid {color};
                border-radius: 5px;
                padding: 8px;
            """)
            
            diff_layout = QVBoxLayout(difficulty_widget)
            
            diff_title = QLabel(difficulty)
            diff_title.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 14px;")
            diff_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            diff_layout.addWidget(diff_title)
            
            diff_count = QLabel(f"{count} puzzles")
            diff_count.setStyleSheet("color: #ffffff; font-size: 12px;")
            diff_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
            diff_layout.addWidget(diff_count)
            
            # Calculate completion percentage for this difficulty
            completed_count = sum(1 for pid in self.user_data.completed_puzzles 
                               if self.puzzle_manager.get_puzzle_by_id(pid) and 
                               self.puzzle_manager.get_puzzle_by_id(pid).difficulty == difficulty)
            
            completion_pct = int((completed_count / count) * 100) if count > 0 else 0
            
            diff_completion = QLabel(f"{completion_pct}% completed")
            diff_completion.setStyleSheet(f"color: {color}; font-size: 12px;")
            diff_completion.setAlignment(Qt.AlignmentFlag.AlignCenter)
            diff_layout.addWidget(diff_completion)
            
            difficulty_display_layout.addWidget(difficulty_widget)
        
        self.difficulty_chart_layout.addLayout(difficulty_display_layout)
        difficulty_layout.addWidget(self.difficulty_chart_container)
        charts_layout.addWidget(difficulty_frame)
        
        main_layout.addLayout(charts_layout)
    
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
        # Clear existing UI
        self._clear_ui()
        
        # Get user statistics
        stats = self.user_data.get_statistics()
        
        # Update KPIs
        total_puzzles = len(self.puzzle_manager.get_all_puzzles())
        completed_puzzles = len(self.user_data.completed_puzzles)
        completion_rate = int((completed_puzzles / total_puzzles) * 100) if total_puzzles > 0 else 0
        
        # Format time values
        avg_completion_time = "00:00"
        if self.user_data.puzzle_completion_times:
            avg_time = sum(self.user_data.puzzle_completion_times.values()) / len(self.user_data.puzzle_completion_times)
            minutes = int(avg_time) // 60
            seconds = int(avg_time) % 60
            avg_completion_time = f"{minutes:02d}:{seconds:02d}"
        
        fastest_time = "00:00"
        if self.user_data.puzzle_completion_times:
            fastest = min(self.user_data.puzzle_completion_times.values())
            minutes = int(fastest) // 60
            seconds = int(fastest) % 60
            fastest_time = f"{minutes:02d}:{seconds:02d}"
        
        # Create KPI indicators
        completion_indicator = PerformanceIndicator(
            "Completion Rate", f"{completion_rate}%", indicator_color="#00cc99"
        )
        self.kpi_layout.addWidget(completion_indicator)
        
        avg_time_indicator = PerformanceIndicator(
            "Avg. Completion Time", avg_completion_time, indicator_color="#ff9900"
        )
        self.kpi_layout.addWidget(avg_time_indicator)
        
        fastest_indicator = PerformanceIndicator(
            "Fastest Solve", fastest_time, indicator_color="#00ccff"
        )
        self.kpi_layout.addWidget(fastest_indicator)
        
        attempts_indicator = PerformanceIndicator(
            "Avg. Attempts", f"{stats['avg_attempts']:.1f}", indicator_color="#cc00ff"
        )
        self.kpi_layout.addWidget(attempts_indicator)
        
        # Create category analytics
        categories = {}
        difficulty_ratings = {
            "Easy": 3,
            "Medium": 6,
            "Hard": 9
        }
        
        # Collect data by category
        for puzzle in self.puzzle_manager.get_all_puzzles():
            category = puzzle.category
            if category not in categories:
                categories[category] = {
                    "total": 0,
                    "completed": 0,
                    "times": [],
                    "difficulty_sum": 0
                }
            
            categories[category]["total"] += 1
            categories[category]["difficulty_sum"] += difficulty_ratings.get(puzzle.difficulty, 5)
            
            if puzzle.id in self.user_data.completed_puzzles:
                categories[category]["completed"] += 1
                if puzzle.id in self.user_data.puzzle_completion_times:
                    categories[category]["times"].append(self.user_data.puzzle_completion_times[puzzle.id])
        
        # Create category analytics widgets
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
        
        # Sort categories by completion rate (highest first)
        sorted_categories = sorted(
            categories.items(),
            key=lambda x: (x[1]["completed"] / x[1]["total"]) if x[1]["total"] > 0 else 0,
            reverse=True
        )
        
        # Add category analytics widgets
        for category_name, data in sorted_categories:
            # Calculate metrics
            completion_rate = int((data["completed"] / data["total"]) * 100) if data["total"] > 0 else 0
            
            avg_time = "N/A"
            if data["times"]:
                time_in_seconds = sum(data["times"]) / len(data["times"])
                minutes = int(time_in_seconds) // 60
                seconds = int(time_in_seconds) % 60
                avg_time = f"{minutes:02d}:{seconds:02d}"
            
            difficulty_rating = round(data["difficulty_sum"] / data["total"]) if data["total"] > 0 else 0
            
            # Create widget
            color = category_colors.get(category_name, default_color)
            category_widget = CategoryAnalytics(
                category_name, completion_rate, avg_time, difficulty_rating, color
            )
            self.categories_layout.addWidget(category_widget)
        
        # Create performance over time chart (placeholder)
        self.performance_chart_label.setText("Performance Over Time")
        
        # Add sample chart data (this would be replaced with actual chart in a real implementation)
        chart_placeholder = QLabel("Chart placeholder - would show completion times over time")
        chart_placeholder.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.3);
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 40px;
            color: #aaaaaa;
        """)
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.performance_chart_layout.addWidget(chart_placeholder)
        
        # Create difficulty distribution chart (placeholder)
        self.difficulty_chart_label.setText("Puzzle Difficulty Distribution")
        
        # Count puzzles by difficulty
        difficulty_counts = {"Easy": 0, "Medium": 0, "Hard": 0}
        for puzzle in self.puzzle_manager.get_all_puzzles():
            if puzzle.difficulty in difficulty_counts:
                difficulty_counts[puzzle.difficulty] += 1
        
        # Create difficulty distribution display
        difficulty_layout = QHBoxLayout()
        
        for difficulty, count in difficulty_counts.items():
            if difficulty == "Easy":
                color = "#00cc00"
            elif difficulty == "Medium":
                color = "#ff9900"
            else:  # Hard
                color = "#ff3333"
            
            difficulty_widget = QFrame()
            difficulty_widget.setStyleSheet(f"""
                background-color: rgba(0, 0, 0, 0.3);
                border: 1px solid {color};
                border-radius: 5px;
                padding: 10px;
            """)
            
            diff_layout = QVBoxLayout(difficulty_widget)
            
            diff_title = QLabel(difficulty)
            diff_title.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 16px;")
            diff_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            diff_layout.addWidget(diff_title)
            
            diff_count = QLabel(f"{count} puzzles")
            diff_count.setStyleSheet("color: #ffffff; font-size: 14px;")
            diff_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
            diff_layout.addWidget(diff_count)
            
            # Calculate completion percentage for this difficulty
            completed_count = sum(1 for pid in self.user_data.completed_puzzles 
                               if self.puzzle_manager.get_puzzle_by_id(pid) and 
                               self.puzzle_manager.get_puzzle_by_id(pid).difficulty == difficulty)
            
            completion_pct = int((completed_count / count) * 100) if count > 0 else 0
            
            diff_completion = QLabel(f"{completion_pct}% completed")
            diff_completion.setStyleSheet(f"color: {color}; font-size: 14px;")
            diff_completion.setAlignment(Qt.AlignmentFlag.AlignCenter)
            diff_layout.addWidget(diff_completion)
            
            difficulty_layout.addWidget(difficulty_widget)
        
        self.difficulty_chart_layout.addLayout(difficulty_layout)
    
    def _clear_ui(self):
        """Clear UI elements before refreshing"""
        # Clear KPI layout
        for i in reversed(range(self.kpi_layout.count())):
            item = self.kpi_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
        
        # Clear categories layout
        for i in reversed(range(self.categories_layout.count())):
            item = self.categories_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
        
        # Clear performance chart layout
        for i in reversed(range(self.performance_chart_layout.count())):
            item = self.performance_chart_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                # Remove all widgets from the nested layout
                nested_layout = item.layout()
                for j in reversed(range(nested_layout.count())):
                    nested_item = nested_layout.itemAt(j)
                    if nested_item.widget():
                        nested_item.widget().deleteLater()
                # Remove the layout itself
                self.performance_chart_layout.removeItem(item)
        
        # Clear difficulty chart layout
        for i in reversed(range(self.difficulty_chart_layout.count())):
            item = self.difficulty_chart_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                # Remove all widgets from the nested layout
                nested_layout = item.layout()
                for j in reversed(range(nested_layout.count())):
                    nested_item = nested_layout.itemAt(j)
                    if nested_item.widget():
                        nested_item.widget().deleteLater()
                # Remove the layout itself
                self.difficulty_chart_layout.removeItem(item) 