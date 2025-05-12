#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Screen manager for Cybersecurity Escape Room
Handles screen transitions and navigation
"""

from PyQt6.QtWidgets import QStackedWidget, QWidget
from PyQt6.QtCore import Qt, QTimer

from ..utils.animation_effects import SlideTransition, CyberDoorTransition


class ScreenManager(QStackedWidget):
    """Manages application screens and transitions between them"""
    
    # Transition types
    SLIDE_LEFT = 1
    SLIDE_RIGHT = 2
    SLIDE_UP = 3
    SLIDE_DOWN = 4
    CYBER_DOOR = 5
    NO_ANIMATION = 0
    
    def __init__(self, parent=None):
        """
        Initialize screen manager
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.transition_type = self.SLIDE_LEFT
        self.screens = {}  # Screen name to index mapping
        self.current_screen_name = None
        
        # For tracking history
        self.screen_history = []
        self.history_index = -1
        
        # Animation properties
        self.animation_duration = 500
        self.current_animation = None
    
    def add_screen(self, screen_name, screen_widget):
        """
        Add a screen to the manager
        
        Args:
            screen_name: Unique identifier for this screen
            screen_widget: QWidget to add
            
        Returns:
            int: Index of the added screen
        """
        index = self.addWidget(screen_widget)
        self.screens[screen_name] = index
        return index
    
    def get_screen(self, screen_name):
        """
        Get screen widget by name
        
        Args:
            screen_name: Screen identifier
            
        Returns:
            QWidget: The screen widget or None if not found
        """
        if screen_name in self.screens:
            return self.widget(self.screens[screen_name])
        return None
    
    def go_to_screen(self, screen_name, transition=None, add_to_history=True):
        """
        Navigate to a specific screen
        
        Args:
            screen_name: Screen identifier
            transition: Transition type to use (or None for default)
            add_to_history: Whether to add this transition to history
            
        Returns:
            bool: True if navigation was successful
        """
        print(f"Navigating to screen: {screen_name}")
        if screen_name not in self.screens:
            print(f"Screen {screen_name} not found in screens dict!")
            print(f"Available screens: {list(self.screens.keys())}")
            return False
        
        # Use the specified transition or default
        transition_type = transition if transition is not None else self.transition_type
        
        # Get current and next screen widgets
        next_index = self.screens[screen_name]
        current_index = self.currentIndex()
        
        print(f"Current index: {current_index}, Next index: {next_index}")
        
        if current_index == next_index:
            print("Already on this screen")
            return True  # Already on this screen
        
        current_widget = self.currentWidget()
        next_widget = self.widget(next_index)
        
        print(f"Current widget: {current_widget}, Next widget: {next_widget}")
        
        # Add to history if requested
        if add_to_history:
            # If we've navigated back and forth, trim the history
            if self.history_index < len(self.screen_history) - 1:
                self.screen_history = self.screen_history[:self.history_index + 1]
            
            self.screen_history.append(screen_name)
            self.history_index = len(self.screen_history) - 1
        
        # Force NO_ANIMATION transition for main_menu screen to avoid blank screen issues
        if screen_name == "main_menu":
            transition_type = self.NO_ANIMATION
            print("Forcing NO_ANIMATION for main_menu screen")
            
        # Handle transition based on type
        if transition_type == self.NO_ANIMATION:
            # Simply change the screen without animation
            print(f"Changing to screen index {next_index} without animation")
            self.setCurrentIndex(next_index)
            next_widget.show()  # Ensure the widget is visible
        elif transition_type == self.CYBER_DOOR:
            # Cyber door transition
            print("Using cyber door transition")
            self._do_cyber_door_transition(current_widget, next_widget, next_index)
        else:
            # Slide transition
            print(f"Using slide transition type {transition_type}")
            self._do_slide_transition(transition_type, current_widget, next_widget, next_index)
        
        # Save current screen name
        self.current_screen_name = screen_name
        print(f"Navigation to {screen_name} complete")
        
        return True
    
    def go_back(self):
        """
        Navigate to the previous screen in history
        
        Returns:
            bool: True if navigation was successful
        """
        if self.history_index <= 0:
            return False  # No previous screen
        
        self.history_index -= 1
        previous_screen = self.screen_history[self.history_index]
        
        # Use slide right transition for back navigation
        return self.go_to_screen(previous_screen, 
                                transition=self.SLIDE_RIGHT, 
                                add_to_history=False)
    
    def go_forward(self):
        """
        Navigate to the next screen in history (if available)
        
        Returns:
            bool: True if navigation was successful
        """
        if self.history_index >= len(self.screen_history) - 1:
            return False  # No next screen
        
        self.history_index += 1
        next_screen = self.screen_history[self.history_index]
        
        # Use slide left transition for forward navigation
        return self.go_to_screen(next_screen, 
                               transition=self.SLIDE_LEFT, 
                               add_to_history=False)
    
    def set_default_transition(self, transition_type):
        """
        Set default transition type
        
        Args:
            transition_type: One of the transition constants
        """
        self.transition_type = transition_type
    
    def set_animation_duration(self, duration):
        """
        Set animation duration
        
        Args:
            duration: Duration in milliseconds
        """
        self.animation_duration = duration
    
    def _do_slide_transition(self, transition_type, current_widget, next_widget, next_index):
        """
        Perform a slide transition
        
        Args:
            transition_type: Type of slide transition
            current_widget: Current widget
            next_widget: Next widget to transition to
            next_index: Index of next widget
        """
        # Prepare the next widget
        next_widget.hide()
        next_widget.setGeometry(current_widget.geometry())
        
        # Set up transition based on type
        if transition_type == self.SLIDE_LEFT:
            # Slide from right to left
            # Current widget slides out to the left, next widget slides in from the right
            current_anim = SlideTransition.slide_out_to_left(current_widget, self.animation_duration)
            self.setCurrentIndex(next_index)
            next_anim = SlideTransition.slide_in_from_right(next_widget, self.animation_duration)
            
        elif transition_type == self.SLIDE_RIGHT:
            # Implementation for other transition types here...
            pass
            
        elif transition_type == self.SLIDE_UP:
            # Implementation for slide up...
            pass
            
        elif transition_type == self.SLIDE_DOWN:
            # Implementation for slide down...
            pass
            
        else:
            # Default to slide left
            current_anim = SlideTransition.slide_out_to_left(current_widget, self.animation_duration)
            self.setCurrentIndex(next_index)
            next_anim = SlideTransition.slide_in_from_right(next_widget, self.animation_duration)
    
    def _do_cyber_door_transition(self, current_widget, next_widget, next_index):
        """
        Perform a cyber door transition
        
        Args:
            current_widget: Current widget
            next_widget: Next widget to transition to
            next_index: Index of next widget
        """
        # Hide next widget until animation is done
        print(f"In cyber door transition. Next widget: {next_widget}, Next index: {next_index}")
        next_widget.hide()
        
        # Set as current widget
        print("Setting current index")
        self.setCurrentIndex(next_index)
        
        # Perform door open transition
        print("Starting cyber door transition animation")
        CyberDoorTransition.door_open(self, next_widget, "horizontal", self.animation_duration)
        print("Cyber door transition completed")
    
    def resize_event(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        
        # Update geometry of any ongoing animations
        if self.current_animation:
            # Update animation targets as needed
            pass 