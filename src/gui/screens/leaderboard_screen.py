#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Leaderboard screen for Cybersecurity Escape Room
Displays global rankings and comparisons between users
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QFrame, QGridLayout, QSpacerItem,
                           QSizePolicy, QScrollArea, QTableWidget, QTableWidgetItem,
                           QHeaderView)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont, QColor, QIcon

from ..utils.animation_effects import FlickerEffect


class RankingItem(QFrame):
    """Widget showing a single user's ranking"""
    
    def __init__(self, rank, username, points, completed_count, avg_time, is_current_user=False):
        """
        Initialize ranking item
        
        Args:
            rank: User's rank position (1st, 2nd, etc)
            username: Username
            points: Total points
            completed_count: Number of completed puzzles
            avg_time: Average completion time
            is_current_user: Whether this item represents current user
        """
        super().__init__()
        
        # Set style based on rank
        background_color = "rgba(0, 0, 0, 0.3)"
        border_color = "#555555"
        
        if rank == 1:  # 1st place
            border_color = "#ffd700"  # Gold
        elif rank == 2:  # 2nd place
            border_color = "#c0c0c0"  # Silver
        elif rank == 3:  # 3rd place
            border_color = "#cd7f32"  # Bronze
            
        if is_current_user:
            background_color = "rgba(0, 204, 255, 0.15)"
            
        self.setStyleSheet(f"""
            RankingItem {{
                background-color: {background_color};
                border: 1px solid {border_color};
                border-radius: 5px;
                padding: 8px;
                margin: 2px 0px;
            }}
        """)
        
        # Create layout
        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        
        # Rank
        rank_label = QLabel(f"#{rank}")
        if rank <= 3:
            rank_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {border_color};")
        else:
            rank_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #aaaaaa;")
        layout.addWidget(rank_label)
        
        # Username
        username_label = QLabel(username)
        if is_current_user:
            username_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #00ccff;")
        else:
            username_label.setStyleSheet("font-size: 16px; color: #ffffff;")
        layout.addWidget(username_label)
        
        layout.addStretch()
        
        # Completed puzzles
        puzzles_label = QLabel(f"{completed_count} puzzles")
        puzzles_label.setStyleSheet("color: #cccccc;")
        layout.addWidget(puzzles_label)
        
        # Average time
        minutes = int(avg_time) // 60
        seconds = int(avg_time) % 60
        time_label = QLabel(f"Avg time: {minutes:02d}:{seconds:02d}")
        time_label.setStyleSheet("color: #cccccc;")
        layout.addWidget(time_label)
        
        # Points
        points_label = QLabel(f"{points} pts")
        points_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #00cc99;")
        layout.addWidget(points_label)


class LeaderboardScreen(QWidget):
    """Screen for displaying global rankings and user comparisons"""
    
    # Signals
    return_to_menu = pyqtSignal()  # Emitted when back button is clicked
    
    def __init__(self, ranking_system, current_username=None, parent=None):
        """
        Initialize leaderboard screen
        
        Args:
            ranking_system: RankingSystem instance
            current_username: Current user's username
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.ranking_system = ranking_system
        self.current_username = current_username
        
        self._create_ui()
        self._connect_signals()
        self._apply_animations()
    
    def _create_ui(self):
        """Create the leaderboard UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header section
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("GLOBAL LEADERBOARD")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #00ccff;")
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.5);
                color: #00ccff;
                border: 1px solid #00ccff;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
            }
            
            QPushButton:hover {
                background-color: rgba(0, 204, 255, 0.2);
            }
        """)
        header_layout.addWidget(self.refresh_button)
        
        self.back_button = QPushButton("← Back to Menu")
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.5);
                color: #cccccc;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 6px 12px;
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
        
        # Current user ranking (if logged in)
        if self.current_username:
            current_user_rank = self.ranking_system.get_user_rank(self.current_username)
            
            if current_user_rank:
                current_user_frame = QFrame()
                current_user_frame.setStyleSheet("""
                    background-color: rgba(0, 0, 0, 0.2);
                    border-radius: 5px;
                    padding: 12px;
                """)
                
                current_user_layout = QVBoxLayout(current_user_frame)
                
                current_user_title = QLabel("YOUR RANKING")
                current_user_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
                current_user_layout.addWidget(current_user_title)
                
                rank_item = RankingItem(
                    current_user_rank["rank"],
                    current_user_rank["username"],
                    current_user_rank["points"],
                    current_user_rank["completed_count"],
                    current_user_rank["avg_completion_time"],
                    True
                )
                current_user_layout.addWidget(rank_item)
                
                main_layout.addWidget(current_user_frame)
        
        # Top rankings
        rankings_frame = QFrame()
        rankings_frame.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 5px;
            padding: 12px;
        """)
        
        rankings_layout = QVBoxLayout(rankings_frame)
        
        rankings_title = QLabel("TOP PLAYERS")
        rankings_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        rankings_layout.addWidget(rankings_title)
        
        # Create scroll area for rankings
        rankings_scroll = QScrollArea()
        rankings_scroll.setWidgetResizable(True)
        rankings_scroll.setFrameShape(QFrame.Shape.NoFrame)
        rankings_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        rankings_scroll.setStyleSheet("""
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
        
        # Container for ranking items
        self.rankings_container = QWidget()
        self.rankings_layout = QVBoxLayout(self.rankings_container)
        self.rankings_layout.setSpacing(8)
        self.rankings_layout.setContentsMargins(0, 0, 0, 0)
        
        # Load rankings
        self._load_rankings()
        
        rankings_scroll.setWidget(self.rankings_container)
        rankings_layout.addWidget(rankings_scroll)
        
        main_layout.addWidget(rankings_frame, 1)
        
        # Statistics table
        stats_frame = QFrame()
        stats_frame.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 5px;
            padding: 12px;
        """)
        
        stats_layout = QVBoxLayout(stats_frame)
        
        stats_title = QLabel("STATISTICS BREAKDOWN")
        stats_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        stats_layout.addWidget(stats_title)
        
        # Create table for detailed stats
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(5)
        self.stats_table.setHorizontalHeaderLabels(["Rank", "Username", "Points", "Puzzles", "Avg Time"])
        self.stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.stats_table.verticalHeader().setVisible(False)
        self.stats_table.setStyleSheet("""
            QTableWidget {
                background-color: rgba(0, 0, 0, 0.3);
                border: none;
                gridline-color: #333333;
                color: #ffffff;
            }
            
            QHeaderView::section {
                background-color: rgba(0, 0, 0, 0.5);
                color: #00ccff;
                border: 1px solid #333333;
                padding: 5px;
                font-weight: bold;
            }
            
            QTableWidget::item {
                padding: 5px;
            }
            
            QTableWidget::item:selected {
                background-color: rgba(0, 204, 255, 0.3);
            }
        """)
        
        # Load table data
        self._load_table_data()
        
        stats_layout.addWidget(self.stats_table)
        
        main_layout.addWidget(stats_frame, 1)
        
        # Footer note
        footer_note = QLabel("Rankings are updated every 5 minutes. Earn points by completing challenges faster!")
        footer_note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_note.setStyleSheet("color: #888888; font-size: 12px;")
        main_layout.addWidget(footer_note)
    
    def _connect_signals(self):
        """Connect signals to slots"""
        self.back_button.clicked.connect(self.return_to_menu.emit)
        self.refresh_button.clicked.connect(self._refresh_rankings)
    
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
    
    def _load_rankings(self):
        """Load and display rankings"""
        # Clear existing ranking items
        while self.rankings_layout.count():
            item = self.rankings_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Get top rankings
        top_users = self.ranking_system.get_leaderboard(10)
        
        # Create ranking items
        for user in top_users:
            rank_item = RankingItem(
                user["rank"],
                user["username"],
                user["points"],
                user["completed_count"],
                user["avg_completion_time"],
                user["username"] == self.current_username
            )
            self.rankings_layout.addWidget(rank_item)
        
        # Add stretch at the end
        self.rankings_layout.addStretch()
    
    def _load_table_data(self):
        """Load detailed statistics into the table"""
        # Clear existing rows
        self.stats_table.setRowCount(0)
        
        # Get all rankings
        all_users = self.ranking_system.get_rankings()
        
        # Add rows to table
        self.stats_table.setRowCount(len(all_users))
        
        for i, user in enumerate(all_users):
            # Rank
            rank_item = QTableWidgetItem(str(user["rank"]))
            rank_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.stats_table.setItem(i, 0, rank_item)
            
            # Username
            username_item = QTableWidgetItem(user["username"])
            if user["username"] == self.current_username:
                username_item.setForeground(QColor("#00ccff"))
                username_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            self.stats_table.setItem(i, 1, username_item)
            
            # Points
            points_item = QTableWidgetItem(str(user["points"]))
            points_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.stats_table.setItem(i, 2, points_item)
            
            # Completed puzzles
            puzzles_item = QTableWidgetItem(str(user["completed_count"]))
            puzzles_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.stats_table.setItem(i, 3, puzzles_item)
            
            # Average time
            avg_time = user["avg_completion_time"]
            minutes = int(avg_time) // 60
            seconds = int(avg_time) % 60
            time_str = f"{minutes:02d}:{seconds:02d}"
            time_item = QTableWidgetItem(time_str)
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.stats_table.setItem(i, 4, time_item)
            
            # Highlight current user's row
            if user["username"] == self.current_username:
                for col in range(self.stats_table.columnCount()):
                    item = self.stats_table.item(i, col)
                    item.setBackground(QColor(0, 204, 255, 40))
    
    def _refresh_rankings(self):
        """Refresh the rankings display"""
        # Force refresh of rankings cache
        self.ranking_system.get_rankings(force_refresh=True)
        
        # Reload UI
        self._load_rankings()
        self._load_table_data()
    
    def set_current_username(self, username):
        """
        Update the current username
        
        Args:
            username: Current user's username
        """
        self.current_username = username
        
        # Refresh rankings to highlight current user
        self._load_rankings()
        self._load_table_data()
    
    def showEvent(self, event):
        """Handle show event to refresh data"""
        super().showEvent(event)
        self._refresh_rankings() 