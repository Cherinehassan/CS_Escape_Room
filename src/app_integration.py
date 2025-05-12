#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Application integration example for Cybersecurity Escape Room
Shows how to incorporate all components into the main application
"""

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt, QTimer

# Import core components
from src.core.puzzle_manager import PuzzleManager
from src.core.user_data import UserData

# Import utility components
from src.gui.utils.animation_effects import FlickerEffect, CyberDoorTransition
from src.gui.utils.theme_manager import ThemeManager
from src.gui.utils.screen_manager import ScreenManager

# Import screens
from src.gui.screens.dashboard_screen import DashboardScreen
from src.gui.screens.login_screen import LoginScreen
from src.gui.screens.signup_screen import SignupScreen
from src.gui.screens.main_menu_screen import MainMenuScreen
from src.gui.screens.challenges_screen import ChallengesScreen
from src.gui.screens.settings_screen import SettingsScreen
from src.gui.screens.puzzle_screen import PuzzleScreen
from src.gui.screens.analytics_screen import AnalyticsScreen
from src.gui.tutorial_screen import TutorialScreen


class CyberEscapeRoomApp(QMainWindow):
    """Main application window for Cybersecurity Escape Room"""
    
    def __init__(self):
        """Initialize the application"""
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("Cybersecurity Escape Room")
        self.setMinimumSize(1024, 768)
        
        # Initialize components
        self._init_managers()
        self._init_ui()
        self._connect_signals()
        
        # Apply theme
        self.theme_manager.apply_theme(ThemeManager.NEON_HACKER)
    
    def _init_managers(self):
        """Initialize managers and core components"""
        # Initialize puzzle manager
        self.puzzle_manager = PuzzleManager()
        self.puzzle_manager.load_puzzles("data/puzzles.json")
        
        # Initialize user data
        self.user_data = UserData()
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        
        # Initialize screen manager
        self.screen_manager = ScreenManager()
        self.setCentralWidget(self.screen_manager)
        
        # Configure screen manager
        self.screen_manager.set_default_transition(ScreenManager.NO_ANIMATION)
    
    def _init_ui(self):
        """Initialize user interface components"""
        # Create and add login screen
        self.login_screen = LoginScreen()
        self.screen_manager.add_screen("login", self.login_screen)
        
        # Create and add signup screen
        self.signup_screen = SignupScreen()
        self.screen_manager.add_screen("signup", self.signup_screen)
        
        # Create and add main menu screen
        self.main_menu_screen = MainMenuScreen("User")  # Default username
        self.screen_manager.add_screen("main_menu", self.main_menu_screen)
        
        # Create and add dashboard screen
        self.dashboard_screen = DashboardScreen(self.puzzle_manager, self.user_data)
        self.dashboard_screen.set_theme_manager(self.theme_manager)
        self.screen_manager.add_screen("dashboard", self.dashboard_screen)
        
        # Create and add challenges screen
        self.challenges_screen = ChallengesScreen(self.puzzle_manager)
        self.screen_manager.add_screen("challenges", self.challenges_screen)
        
        # Create and add settings screen
        self.settings_screen = SettingsScreen()
        self.screen_manager.add_screen("settings", self.settings_screen)
        
        # Create and add puzzle screen
        self.puzzle_screen = PuzzleScreen(self.puzzle_manager)
        self.screen_manager.add_screen("puzzle", self.puzzle_screen)
        
        # Create and add analytics screen
        self.analytics_screen = AnalyticsScreen(self.puzzle_manager, self.user_data)
        self.screen_manager.add_screen("analytics", self.analytics_screen)
        
        # Create and add tutorial screen
        self.tutorial_screen = TutorialScreen(self)
        self.screen_manager.add_screen("tutorial", self.tutorial_screen)
        
        # Navigate to the initial screen
        self.screen_manager.go_to_screen("login")
    
    def _connect_signals(self):
        """Connect signals and slots"""
        # Connect login screen signals
        self.login_screen.login_successful.connect(self._on_login_successful)
        self.login_screen.signup_requested.connect(self._on_signup_requested)
        
        # Connect signup screen signals
        self.signup_screen.signup_successful.connect(self._on_signup_successful)
        self.signup_screen.login_requested.connect(self._on_return_to_login)
        
        # Connect main menu screen signals
        self.main_menu_screen.start_game_requested.connect(self._on_start_game)
        self.main_menu_screen.continue_game_requested.connect(self._on_continue_game)
        self.main_menu_screen.view_puzzles_requested.connect(self._on_view_puzzles)
        self.main_menu_screen.view_dashboard_requested.connect(self._on_view_dashboard)
        self.main_menu_screen.view_analytics_requested.connect(self._on_view_analytics)
        self.main_menu_screen.view_settings_requested.connect(self._on_view_settings)
        self.main_menu_screen.view_tutorial_requested.connect(self._on_view_tutorial)
        self.main_menu_screen.logout_requested.connect(self._on_logout)
        
        # Connect dashboard signals
        self.dashboard_screen.challenge_selected.connect(self._on_challenge_selected)
        self.dashboard_screen.return_to_menu.connect(self._on_return_to_menu)
        
        # Connect challenges screen signals
        self.challenges_screen.challenge_selected.connect(self._on_challenge_selected)
        self.challenges_screen.return_to_menu.connect(self._on_return_to_menu)
        
        # Connect settings screen signals
        self.settings_screen.settings_saved.connect(self._on_settings_saved)
        self.settings_screen.return_to_menu.connect(self._on_return_to_menu)
        
        # Connect puzzle screen signals
        self.puzzle_screen.puzzle_completed.connect(self._on_puzzle_completed)
        self.puzzle_screen.return_to_challenges.connect(self._on_return_to_challenges)
        
        # Connect analytics screen signals
        self.analytics_screen.return_to_dashboard.connect(self._on_return_to_dashboard)
    
    def _on_login_successful(self, username):
        """Handle successful login"""
        print(f"Login successful for user: {username}")
        print(f"Main menu screen exists: {self.main_menu_screen is not None}")
        self.main_menu_screen.update_username(username)
        print("Going to main menu screen")
        self.screen_manager.go_to_screen("main_menu")
        print("Navigation complete")
        
    def _on_signup_requested(self):
        """Handle signup request from login screen"""
        self.screen_manager.go_to_screen("signup")
        
    def _on_signup_successful(self, username):
        """Handle successful signup"""
        self.main_menu_screen.update_username(username)
        self.screen_manager.go_to_screen("main_menu")
        
    def _on_return_to_login(self):
        """Handle return to login from signup screen"""
        self.screen_manager.go_to_screen("login")
        
    def _on_start_game(self):
        """Handle start game request"""
        # Navigate to challenges screen to start a new game
        self.screen_manager.go_to_screen("challenges")
        self.main_menu_screen.update_status("GAME STARTED")
        print("Start game requested")
        
    def _on_continue_game(self):
        """Handle continue game request"""
        # Navigate to challenges screen with progress loaded
        self.screen_manager.go_to_screen("challenges")
        self.main_menu_screen.update_status("GAME CONTINUED")
        print("Continue game requested")
        
    def _on_view_puzzles(self):
        """Handle view puzzles request"""
        self.screen_manager.go_to_screen("challenges")
        
    def _on_view_dashboard(self):
        """Handle view dashboard request"""
        self.screen_manager.go_to_screen("dashboard")
        
    def _on_view_analytics(self):
        """Handle view analytics request"""
        self.screen_manager.go_to_screen("analytics")
        
    def _on_view_tutorial(self):
        """Handle view tutorial request"""
        self.screen_manager.go_to_screen("tutorial")
        
    def _on_view_settings(self):
        """Handle view settings request"""
        self.screen_manager.go_to_screen("settings")
        
    def _on_logout(self):
        """Handle logout request"""
        self.screen_manager.go_to_screen("login")
        
    def _on_challenge_selected(self, puzzle_id):
        """
        Handle challenge selection from dashboard or challenges screen
        
        Args:
            puzzle_id: ID of the selected puzzle
        """
        # Load the selected puzzle
        self.puzzle_screen.load_puzzle(puzzle_id)
        
        # Navigate to puzzle screen
        self.screen_manager.go_to_screen("puzzle")
        print(f"Challenge {puzzle_id} selected")
        
    def _on_puzzle_completed(self, puzzle_id, time):
        """
        Handle puzzle completion
        
        Args:
            puzzle_id: ID of the completed puzzle
            time: Time taken to complete the puzzle in seconds
        """
        # Update user data with completed puzzle
        # self.user_data.add_completed_puzzle(puzzle_id, time)
        
        # Return to challenges screen after delay
        QTimer.singleShot(3000, self._on_return_to_challenges)
        
    def _on_return_to_challenges(self):
        """Return to challenges screen from puzzle screen"""
        self.screen_manager.go_to_screen("challenges")
        
    def _on_return_to_menu(self):
        """Handle return to menu request"""
        self.screen_manager.go_to_screen("main_menu")
        
    def _on_return_to_dashboard(self):
        """Handle return to dashboard request"""
        self.screen_manager.go_to_screen("dashboard")
        
    def _on_settings_saved(self, settings):
        """
        Handle settings save
        
        Args:
            settings: Dictionary of settings
        """
        # Apply settings
        # Update fullscreen mode
        if settings.get("fullscreen", False):
            self.showFullScreen()
        else:
            self.showNormal()
    
    def closeEvent(self, event):
        """Handle application close event"""
        # Save user data
        # self.user_data.save()
        
        # Clean up resources
        super().closeEvent(event)


# Example usage
def main():
    """Main application entry point"""
    import sys
    
    app = QApplication(sys.argv)
    window = CyberEscapeRoomApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 