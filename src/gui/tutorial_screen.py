#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tutorial screen for Cybersecurity Escape Room
"""

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QStackedWidget
)
from PyQt6.QtCore import Qt

logger = logging.getLogger(__name__)


class TutorialScreen(QWidget):
    """Tutorial screen introducing the game"""
    
    def __init__(self, main_window):
        """Initialize tutorial screen"""
        super().__init__()
        self.main_window = main_window
        self.current_page = 0
        self.total_pages = 5
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
        title_label = QLabel("Tutorial: Introduction to Cybersecurity Escape Room")
        title_label.setObjectName("screenTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Tutorial content container
        self.content_frame = QFrame()
        self.content_frame.setObjectName("contentFrame")
        content_layout = QVBoxLayout(self.content_frame)
        
        # Stacked widget for tutorial pages
        self.page_stack = QStackedWidget()
        content_layout.addWidget(self.page_stack)
        
        # Create tutorial pages
        self._create_tutorial_pages()
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        
        self.prev_button = QPushButton("← Previous")
        self.prev_button.clicked.connect(self.goto_prev_page)
        self.prev_button.setEnabled(False)
        nav_layout.addWidget(self.prev_button)
        
        nav_layout.addStretch()
        
        self.page_indicator = QLabel("1 / 5")
        self.page_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_layout.addWidget(self.page_indicator)
        
        nav_layout.addStretch()
        
        self.next_button = QPushButton("Next →")
        self.next_button.clicked.connect(self.goto_next_page)
        self.next_button.setProperty("class", "primary")
        nav_layout.addWidget(self.next_button)
        
        content_layout.addLayout(nav_layout)
        
        # Add content frame to main layout
        main_layout.addWidget(self.content_frame)
        
        # Set stylesheet
        self.setStyleSheet("""
            #screenTitle {
                font-size: 24px;
                font-weight: bold;
                color: #00ff99;
                margin-bottom: 20px;
            }
            
            #contentFrame {
                background-color: #1e1e1e;
                border-radius: 8px;
                padding: 20px;
            }
            
            #tutorialPage {
                background-color: #262626;
                border-radius: 6px;
                padding: 15px;
                margin-bottom: 20px;
            }
            
            #pageTitle {
                font-size: 20px;
                font-weight: bold;
                color: #00ff99;
                margin-bottom: 10px;
            }
            
            #pageContent {
                font-size: 14px;
                color: #ddd;
                line-height: 1.5;
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
        """)
    
    def _create_tutorial_pages(self):
        """Create the tutorial pages"""
        # Page 1: Welcome
        page1 = self._create_page(
            "Welcome to Cybersecurity Escape Room!",
            """
            Welcome to the Cybersecurity Escape Room, an interactive educational game designed 
            to teach cybersecurity concepts through engaging puzzles and challenges.
            
            This tutorial will guide you through the basic features of the application and
            help you get started with your cybersecurity learning journey.
            
            Navigate through this tutorial using the Previous and Next buttons below.
            """
        )
        self.page_stack.addWidget(page1)
        
        # Page 2: Account System
        page2 = self._create_page(
            "Account System",
            """
            The Cybersecurity Escape Room uses an account-based system to track your progress
            and customize your learning experience:
            
            - Your profile stores your points, achievements, and progress
            - Points are earned by completing challenges and puzzles
            - Your streak increases when you solve multiple puzzles correctly
            - Performance analytics help identify your strengths and areas for improvement
            
            You can view and edit your profile information at any time by clicking on the
            "Profile" option in the main menu.
            """
        )
        self.page_stack.addWidget(page2)
        
        # Page 3: Challenges
        page3 = self._create_page(
            "Challenges & Puzzles",
            """
            The core of the Cybersecurity Escape Room experience is the challenge system:
            
            - Challenges are organized by difficulty (Easy, Medium, Hard)
            - Each challenge focuses on a specific cybersecurity domain
            - Clear learning objectives help you understand what you're learning
            - Limited attempts encourage careful thinking and planning
            - Hints are available if you get stuck, but using them reduces your points
            
            New challenges unlock as you complete the prerequisites, creating a
            progressive learning path tailored to your skills.
            """
        )
        self.page_stack.addWidget(page3)
        
        # Page 4: Adaptive Learning
        page4 = self._create_page(
            "Adaptive Learning System",
            """
            The Cybersecurity Escape Room includes an adaptive learning system that
            analyzes your performance to customize your experience:
            
            - Performance analysis tracks your accuracy, speed, and hint usage
            - Recommendations suggest appropriate challenges based on your skill level
            - Easier challenges are recommended if you're struggling
            - Advanced challenges are suggested when you demonstrate mastery
            - You can always replay challenges to improve your score
            
            The system helps ensure you're always challenged at the right level for
            optimal learning and engagement.
            """
        )
        self.page_stack.addWidget(page4)
        
        # Page 5: Getting Started
        page5 = self._create_page(
            "Getting Started",
            """
            Now that you understand the basics, here's how to get started:
            
            1. Complete this tutorial (you're almost done!)
            2. Visit the Challenges section from the main menu
            3. Start with Easy difficulty challenges
            4. Track your progress in the Profile and Analytics sections
            5. Earn achievements as you demonstrate your skills
            
            Remember, cybersecurity is a continuously evolving field, and regular
            practice is key to maintaining your skills.
            
            Click "Complete Tutorial" below to finish and start your journey!
            """
        )
        self.page_stack.addWidget(page5)
    
    def _create_page(self, title, content):
        """Create a tutorial page"""
        page = QWidget()
        page.setObjectName("tutorialPage")
        layout = QVBoxLayout(page)
        
        # Title
        title_label = QLabel(title)
        title_label.setObjectName("pageTitle")
        layout.addWidget(title_label)
        
        # Content in scrollable area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        content_label = QLabel(content)
        content_label.setObjectName("pageContent")
        content_label.setWordWrap(True)
        content_layout.addWidget(content_label)
        content_layout.addStretch()
        
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)
        
        return page
    
    def refresh(self):
        """Update tutorial content"""
        # Reset to first page
        self.goto_page(0)
    
    def goto_page(self, page_index):
        """Go to a specific page"""
        if 0 <= page_index < self.total_pages:
            self.current_page = page_index
            self.page_stack.setCurrentIndex(page_index)
            self.page_indicator.setText(f"{page_index + 1} / {self.total_pages}")
            
            # Update buttons
            self.prev_button.setEnabled(page_index > 0)
            
            if page_index == self.total_pages - 1:
                self.next_button.setText("Complete Tutorial")
            else:
                self.next_button.setText("Next →")
    
    def goto_prev_page(self):
        """Go to previous page"""
        self.goto_page(self.current_page - 1)
    
    def goto_next_page(self):
        """Go to next page or complete tutorial"""
        if self.current_page == self.total_pages - 1:
            # Mark tutorial as completed
            self._complete_tutorial()
            # Return to menu
            self.goto_menu()
        else:
            self.goto_page(self.current_page + 1)
    
    def _complete_tutorial(self):
        """Mark tutorial as completed"""
        # In a full implementation, this would update the user's profile
        try:
            from src.database.db_manager import UserProfile
            
            profile = self.main_window.game_state.get_user_profile()
            if profile and 'id' in profile:
                session = self.main_window.db_manager.get_session()
                user_profile = session.query(UserProfile).filter_by(user_id=profile['id']).first()
                if user_profile:
                    user_profile.tutorial_completed = True
                    session.commit()
                session.close()
        except Exception as e:
            logger.error(f"Error marking tutorial as completed: {e}")
    
    def goto_menu(self):
        """Return to menu screen"""
        self.main_window.goto_menu() 