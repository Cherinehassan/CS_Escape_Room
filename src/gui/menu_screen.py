#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main menu screen for Cybersecurity Escape Room
"""

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGridLayout, QFrame, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont
import random

logger = logging.getLogger(__name__)


class MenuScreen(QWidget):
    """Main menu screen with navigation options"""
    
    def __init__(self, main_window):
        """Initialize menu screen"""
        super().__init__()
        self.main_window = main_window
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Welcome header
        self.welcome_label = QLabel("Welcome to Cybersecurity Escape Room")
        self.welcome_label.setObjectName("welcomeLabel")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.welcome_label)
        
        # Subtitle with intro text
        intro_text = (
            "Test your cybersecurity knowledge and skills through interactive puzzles. "
            "Navigate through different challenges, earn points, and track your progress."
        )
        intro_label = QLabel(intro_text)
        intro_label.setObjectName("introLabel")
        intro_label.setWordWrap(True)
        intro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(intro_label)
        
        # Menu options in a grid
        menu_frame = QFrame()
        menu_frame.setObjectName("menuFrame")
        menu_layout = QGridLayout(menu_frame)
        menu_layout.setSpacing(20)
        
        # Tutorial button
        self.tutorial_button = MenuButton(
            "Tutorial",
            "Begin with an introduction to the platform",
            "assets/images/menu/tutorial_icon.png",
            self.goto_tutorial
        )
        menu_layout.addWidget(self.tutorial_button, 0, 0)
        
        # Challenge button
        self.challenge_button = MenuButton(
            "Challenges",
            "Access the main puzzle challenges",
            "assets/images/menu/challenges_icon.png",
            self.goto_challenges
        )
        menu_layout.addWidget(self.challenge_button, 0, 1)
        
        # Profile button
        self.profile_button = MenuButton(
            "Profile",
            "View and edit your profile",
            "assets/images/menu/profile_icon.png",
            self.goto_profile
        )
        menu_layout.addWidget(self.profile_button, 1, 0)
        
        # Achievements button
        self.achievements_button = MenuButton(
            "Achievements",
            "Track badges and accomplishments",
            "assets/images/menu/achievements_icon.png",
            self.goto_achievements
        )
        menu_layout.addWidget(self.achievements_button, 1, 1)
        
        # Analytics button
        self.analytics_button = MenuButton(
            "Analytics",
            "Review your performance statistics",
            "assets/images/menu/analytics_icon.png",
            self.goto_analytics
        )
        menu_layout.addWidget(self.analytics_button, 2, 0)
        
        # Settings button
        self.settings_button = MenuButton(
            "Settings",
            "Configure application settings",
            "assets/images/menu/settings_icon.png",
            self.goto_settings
        )
        menu_layout.addWidget(self.settings_button, 2, 1)
        
        # Add menu grid to main layout
        main_layout.addWidget(menu_frame)
        
        # Add flexible space
        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Recommended challenges section
        rec_label = QLabel("Recommended Challenges")
        rec_label.setObjectName("sectionLabel")
        main_layout.addWidget(rec_label)
        
        # We'll create the container in the refresh method,
        # so we don't need to do anything with it here.
        # Just reserve a place for it in the layout
        recommended_placeholder = QWidget()
        main_layout.addWidget(recommended_placeholder)
        
        # Set stylesheet
        self.setStyleSheet("""
            #welcomeLabel {
                font-size: 28px;
                font-weight: bold;
                color: #00ff99;
                margin-bottom: 10px;
            }
            
            #introLabel {
                font-size: 16px;
                color: #cccccc;
                margin-bottom: 20px;
            }
            
            #menuFrame {
                background-color: transparent;
            }
            
            #sectionLabel {
                font-size: 18px;
                font-weight: bold;
                color: #00ff99;
                margin-top: 10px;
            }
            
            #recommendedContainer {
                background-color: #1e1e1e;
                border-radius: 8px;
                padding: 15px;
                min-height: 150px;
            }
        """)
    
    def refresh(self):
        """Refresh menu contents based on user state"""
        # Update welcome label with username if available
        profile = self.main_window.game_state.get_user_profile()
        if profile and 'display_name' in profile:
            self.welcome_label.setText(f"Welcome, {profile['display_name']}!")
        else:
            self.welcome_label.setText("Welcome to Cybersecurity Escape Room")
            
        # Create/reload recommended challenges
        self._load_recommended_challenges()
    
    def _load_recommended_challenges(self):
        """Load and display recommended challenges"""
        # First delete the old container if it exists
        if hasattr(self, 'recommended_container') and self.recommended_container is not None:
            old_container = self.recommended_container
            old_container.deleteLater()
        
        # Create a new container widget
        self.recommended_container = QFrame()
        self.recommended_container.setObjectName("recommendedContainer")
        
        # Create new horizontal layout
        recommended_layout = QHBoxLayout(self.recommended_container)
        recommended_layout.setSpacing(15)
        
        # Get recommended puzzles - select 3 random puzzles from puzzle manager
        # In a real implementation, this would use the game_state to get personalized recommendations
        all_puzzles = self.main_window.puzzle_manager.get_all_puzzles()
        recommended_puzzles = random.sample(all_puzzles, min(3, len(all_puzzles)))
        
        if not recommended_puzzles:
            # Show message if no recommendations
            no_rec_label = QLabel("Complete more challenges to get personalized recommendations")
            no_rec_label.setObjectName("noRecLabel")
            no_rec_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_rec_label.setWordWrap(True)
            recommended_layout.addWidget(no_rec_label)
        else:
            # Add each recommendation
            for puzzle in recommended_puzzles:
                challenge_card = ChallengeCard(puzzle, self.main_window)
                recommended_layout.addWidget(challenge_card)
        
        # Add stretch at the end
        recommended_layout.addStretch()
        
        # Add the new container to the main layout
        # Find the placeholder widget (last widget in the layout)
        # and replace it with our new container
        layout = self.layout()
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, QWidget) and widget.objectName() == "":
                layout.replaceWidget(widget, self.recommended_container)
                widget.hide()  # Hide the placeholder
                break
        else:
            # If no placeholder found (subsequent calls), just add at the end
            layout.addWidget(self.recommended_container)
    
    def goto_tutorial(self):
        """Navigate to tutorial screen"""
        self.main_window.goto_tutorial()
    
    def goto_challenges(self):
        """Navigate to challenges screen"""
        self.main_window.goto_challenges()
    
    def goto_profile(self):
        """Navigate to profile screen"""
        self.main_window.goto_profile()
    
    def goto_achievements(self):
        """Navigate to achievements screen"""
        self.main_window.goto_achievements()
    
    def goto_analytics(self):
        """Navigate to analytics screen"""
        self.main_window.goto_analytics()
    
    def goto_settings(self):
        """Navigate to settings screen"""
        # TODO: Implement settings screen
        pass


class MenuButton(QFrame):
    """Custom button for main menu options"""
    
    def __init__(self, title, description, icon_path, callback):
        """Initialize menu button"""
        super().__init__()
        self.title = title
        self.description = description
        self.icon_path = icon_path
        self.callback = callback
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI components"""
        # Set frame properties
        self.setObjectName("menuButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumSize(200, 150)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add icon
        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setMinimumSize(64, 64)
        icon_label.setMaximumSize(64, 64)
        
        # Try to load icon
        try:
            pixmap = QPixmap(self.icon_path)
            if not pixmap.isNull():
                icon_label.setPixmap(pixmap.scaled(
                    QSize(64, 64),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ))
            else:
                # Fallback to text if icon not found
                icon_label.setText(self.title[0])
                icon_label.setObjectName("menuButtonFallbackIcon")
        except Exception as e:
            logger.warning(f"Could not load menu icon {self.icon_path}: {e}")
            # Fallback to text
            icon_label.setText(self.title[0])
            icon_label.setObjectName("menuButtonFallbackIcon")
        
        layout.addWidget(icon_label)
        
        # Add title
        title_label = QLabel(self.title)
        title_label.setObjectName("menuButtonTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Add description
        desc_label = QLabel(self.description)
        desc_label.setObjectName("menuButtonDesc")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Set style
        self.setStyleSheet("""
            #menuButton {
                background-color: #1e1e1e;
                border-radius: 8px;
                border: 1px solid #333;
                padding: 15px;
            }
            
            #menuButton:hover {
                background-color: #2a2a2a;
                border: 1px solid #444;
            }
            
            #menuButtonTitle {
                font-size: 16px;
                font-weight: bold;
                color: #00ff99;
                margin-top: 10px;
                margin-bottom: 5px;
            }
            
            #menuButtonDesc {
                font-size: 13px;
                color: #aaa;
            }
            
            #menuButtonFallbackIcon {
                background-color: #333;
                color: #00ff99;
                font-size: 24px;
                font-weight: bold;
                border-radius: 32px;
            }
        """)
    
    def mousePressEvent(self, event):
        """Handle mouse press event"""
        super().mousePressEvent(event)
        self.setStyleSheet("""
            #menuButton {
                background-color: #151515;
                border-radius: 8px;
                border: 1px solid #333;
                padding: 15px;
            }
            
            #menuButtonTitle {
                font-size: 16px;
                font-weight: bold;
                color: #00ff99;
                margin-top: 10px;
                margin-bottom: 5px;
            }
            
            #menuButtonDesc {
                font-size: 13px;
                color: #aaa;
            }
            
            #menuButtonFallbackIcon {
                background-color: #333;
                color: #00ff99;
                font-size: 24px;
                font-weight: bold;
                border-radius: 32px;
            }
        """)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release event"""
        super().mouseReleaseEvent(event)
        self.setStyleSheet("""
            #menuButton {
                background-color: #1e1e1e;
                border-radius: 8px;
                border: 1px solid #333;
                padding: 15px;
            }
            
            #menuButton:hover {
                background-color: #2a2a2a;
                border: 1px solid #444;
            }
            
            #menuButtonTitle {
                font-size: 16px;
                font-weight: bold;
                color: #00ff99;
                margin-top: 10px;
                margin-bottom: 5px;
            }
            
            #menuButtonDesc {
                font-size: 13px;
                color: #aaa;
            }
            
            #menuButtonFallbackIcon {
                background-color: #333;
                color: #00ff99;
                font-size: 24px;
                font-weight: bold;
                border-radius: 32px;
            }
        """)
        
        # Call the callback function
        if self.callback:
            self.callback()


class ChallengeCard(QFrame):
    """Card displaying a challenge/puzzle"""
    
    def __init__(self, puzzle_data, main_window):
        """Initialize challenge card"""
        super().__init__()
        self.puzzle_data = puzzle_data
        self.main_window = main_window
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI components"""
        # Set frame properties
        self.setObjectName("challengeCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(250, 120)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        # Add title with difficulty indicator
        title_layout = QHBoxLayout()
        
        # Difficulty indicator
        difficulty = self.puzzle_data.get('difficulty', 'Unknown').lower()
        difficulty_label = QLabel()
        difficulty_label.setFixedSize(12, 12)
        difficulty_label.setObjectName(f"difficulty{difficulty.capitalize()}")
        title_layout.addWidget(difficulty_label)
        
        # Title
        title_label = QLabel(self.puzzle_data.get('name', 'Unknown Puzzle'))
        title_label.setObjectName("challengeTitle")
        title_layout.addWidget(title_label)
        
        layout.addLayout(title_layout)
        
        # Description (truncated)
        description = self.puzzle_data.get('description', '')
        if len(description) > 100:
            description = description[:97] + '...'
        
        desc_label = QLabel(description)
        desc_label.setObjectName("challengeDesc")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Learning objective
        objective = self.puzzle_data.get('learning_objective', '')
        if objective:
            if len(objective) > 70:
                objective = objective[:67] + '...'
            
            obj_label = QLabel(f"Objective: {objective}")
            obj_label.setObjectName("challengeObjective")
            obj_label.setWordWrap(True)
            layout.addWidget(obj_label)
        
        # Category and points
        info_layout = QHBoxLayout()
        
        # Category label
        category = self.puzzle_data.get('category', '')
        if category:
            category_label = QLabel(category)
            category_label.setObjectName("challengeCategory")
            info_layout.addWidget(category_label)
        
        info_layout.addStretch()
        
        # Points
        # Calculate points based on difficulty
        points = 100  # Default
        if difficulty == 'easy':
            points = 100
        elif difficulty == 'medium':
            points = 200
        elif difficulty == 'hard':
            points = 300
            
        points_label = QLabel(f"{points} pts")
        points_label.setObjectName("challengePoints")
        points_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        info_layout.addWidget(points_label)
        
        layout.addLayout(info_layout)
        
        # Set style
        self.setStyleSheet(f"""
            #challengeCard {{
                background-color: #262626;
                border-radius: 6px;
                border: 1px solid #333;
                padding: 10px;
            }}
            
            #challengeCard:hover {{
                background-color: #2d2d2d;
                border: 1px solid #444;
            }}
            
            #challengeTitle {{
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
            }}
            
            #challengeDesc {{
                font-size: 12px;
                color: #bbbbbb;
            }}
            
            #challengeObjective {{
                font-size: 11px;
                color: #00ff99;
                font-style: italic;
            }}
            
            #challengeCategory {{
                font-size: 11px;
                color: #0099cc;
                background-color: #1a3c4d;
                border-radius: 3px;
                padding: 2px 6px;
            }}
            
            #challengePoints {{
                font-size: 12px;
                font-weight: bold;
                color: #ffcc00;
            }}
            
            #difficultyEasy {{
                background-color: #00cc66;
                border-radius: 6px;
            }}
            
            #difficultyMedium {{
                background-color: #ffcc00;
                border-radius: 6px;
            }}
            
            #difficultyHard {{
                background-color: #ff3333;
                border-radius: 6px;
            }}
        """)
    
    def mousePressEvent(self, event):
        """Handle mouse press event"""
        super().mousePressEvent(event)
        self.setStyleSheet(f"""
            #challengeCard {{
                background-color: #1a1a1a;
                border-radius: 6px;
                border: 1px solid #333;
                padding: 10px;
            }}
            
            #challengeTitle {{
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
            }}
            
            #challengeDesc {{
                font-size: 12px;
                color: #bbbbbb;
            }}
            
            #challengeObjective {{
                font-size: 11px;
                color: #00ff99;
                font-style: italic;
            }}
            
            #challengeCategory {{
                font-size: 11px;
                color: #0099cc;
                background-color: #1a3c4d;
                border-radius: 3px;
                padding: 2px 6px;
            }}
            
            #challengePoints {{
                font-size: 12px;
                font-weight: bold;
                color: #ffcc00;
            }}
            
            #difficultyEasy {{
                background-color: #00cc66;
                border-radius: 6px;
            }}
            
            #difficultyMedium {{
                background-color: #ffcc00;
                border-radius: 6px;
            }}
            
            #difficultyHard {{
                background-color: #ff3333;
                border-radius: 6px;
            }}
        """)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release event"""
        super().mouseReleaseEvent(event)
        self.setStyleSheet(f"""
            #challengeCard {{
                background-color: #262626;
                border-radius: 6px;
                border: 1px solid #333;
                padding: 10px;
            }}
            
            #challengeCard:hover {{
                background-color: #2d2d2d;
                border: 1px solid #444;
            }}
            
            #challengeTitle {{
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
            }}
            
            #challengeDesc {{
                font-size: 12px;
                color: #bbbbbb;
            }}
            
            #challengeObjective {{
                font-size: 11px;
                color: #00ff99;
                font-style: italic;
            }}
            
            #challengeCategory {{
                font-size: 11px;
                color: #0099cc;
                background-color: #1a3c4d;
                border-radius: 3px;
                padding: 2px 6px;
            }}
            
            #challengePoints {{
                font-size: 12px;
                font-weight: bold;
                color: #ffcc00;
            }}
            
            #difficultyEasy {{
                background-color: #00cc66;
                border-radius: 6px;
            }}
            
            #difficultyMedium {{
                background-color: #ffcc00;
                border-radius: 6px;
            }}
            
            #difficultyHard {{
                background-color: #ff3333;
                border-radius: 6px;
            }}
        """)
        
        # Start the puzzle
        puzzle_id = self.puzzle_data.get('id')
        if puzzle_id:
            self.main_window.start_puzzle(puzzle_id) 