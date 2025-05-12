#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Animation effects for Cybersecurity Escape Room
Provides animation utilities to create escape room atmosphere
"""

import random
from PyQt6.QtCore import (QPropertyAnimation, QEasingCurve, 
                         QParallelAnimationGroup, QSequentialAnimationGroup,
                         QPoint, QSize, Qt, QTimer, pyqtProperty, QObject, QRect)
from PyQt6.QtWidgets import QWidget, QLabel, QGraphicsOpacityEffect, QFrame
from PyQt6.QtGui import QColor, QPalette, QLinearGradient


class FlickerEffect(QObject):
    """Creates a neon light flickering effect on a widget"""
    
    def __init__(self, target_widget, color="#00ff99", intensity=0.2, interval_range=(500, 3000)):
        """
        Initialize flickering effect
        
        Args:
            target_widget: Widget to apply effect to
            color: Base color to flicker
            intensity: How much the color changes (0.0-1.0)
            interval_range: Tuple of (min_ms, max_ms) for random intervals
        """
        super().__init__()
        self.target = target_widget
        self.base_color = QColor(color)
        self.intensity = intensity
        self.interval_range = interval_range
        self.original_stylesheet = self.target.styleSheet()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._flicker)
        self.active = False

    def start(self):
        """Start the flickering effect"""
        if not self.active:
            self.active = True
            self._flicker()
            self.timer.start(random.randint(*self.interval_range))
    
    def stop(self):
        """Stop the flickering effect"""
        if self.active:
            self.active = False
            self.timer.stop()
            self.target.setStyleSheet(self.original_stylesheet)
    
    def _flicker(self):
        """Create one flicker"""
        if not self.active:
            return
            
        # Calculate a random dimming factor
        dimming = 1.0 - (random.random() * self.intensity)
        
        # Create dimmed color
        dimmed_color = QColor(
            int(self.base_color.red() * dimming),
            int(self.base_color.green() * dimming),
            int(self.base_color.blue() * dimming),
            self.base_color.alpha()
        )
        
        # Apply to stylesheet by adding or modifying color property
        current_style = self.target.styleSheet()
        
        # Simple replacement for now - in a real app with complex styles 
        # you'd use a CSS parser or more sophisticated approach
        if "color:" in current_style:
            new_style = current_style.replace(
                f"color: {self.base_color.name()}", 
                f"color: {dimmed_color.name()}"
            )
            self.target.setStyleSheet(new_style)
        
        # Schedule next flicker
        self.timer.start(random.randint(*self.interval_range))


class SlideTransition:
    """Creates slide transitions between widgets or screens"""
    
    @staticmethod
    def slide_in_from_right(widget, duration=500, show=True):
        """
        Slide a widget in from the right
        
        Args:
            widget: Widget to animate
            duration: Animation duration in milliseconds
            show: Whether to show the widget after animation
        
        Returns:
            QPropertyAnimation: The animation object
        """
        parent_width = widget.parent().width() if widget.parent() else widget.width() * 2
        
        # Start position (outside right edge)
        start_pos = QPoint(parent_width, widget.y()) 
        
        # End position (target position)
        end_pos = QPoint(0, widget.y())
        
        # Create the animation
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(start_pos)
        animation.setEndValue(end_pos)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Show widget if requested
        if show:
            widget.show()
        
        # Start animation
        animation.start()
        
        return animation
    
    @staticmethod
    def slide_out_to_left(widget, duration=500, hide=True):
        """
        Slide a widget out to the left
        
        Args:
            widget: Widget to animate
            duration: Animation duration in milliseconds
            hide: Whether to hide the widget after animation
        
        Returns:
            QPropertyAnimation: The animation object
        """
        parent_width = widget.parent().width() if widget.parent() else widget.width() * 2
        
        # Start position (current position)
        start_pos = widget.pos()
        
        # End position (outside left edge)
        end_pos = QPoint(-widget.width(), widget.y())
        
        # Create the animation
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(start_pos)
        animation.setEndValue(end_pos)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        if hide:
            animation.finished.connect(lambda: widget.hide())
        
        # Start animation
        animation.start()
        
        return animation
    
    @staticmethod
    def slide_in_from_top(widget, duration=500, show=True):
        """
        Slide a widget in from the top
        
        Args:
            widget: Widget to animate
            duration: Animation duration in milliseconds
            show: Whether to show the widget after animation
            
        Returns:
            QPropertyAnimation: The animation object
        """
        # Start position (above top edge)
        start_pos = QPoint(widget.x(), -widget.height())
        
        # End position (target position)
        end_pos = QPoint(widget.x(), 0)
        
        # Create the animation
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(start_pos)
        animation.setEndValue(end_pos)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Show widget if requested
        if show:
            widget.show()
        
        # Start animation
        animation.start()
        
        return animation


class PulseAnimation:
    """Creates a pulsing highlight animation"""
    
    class ColorPropertyAdapter(QObject):
        """Helper class for animating color properties on QWidgets that don't have built-in color property"""
        
        def __init__(self, target_widget, style_prop="color"):
            """Initialize adapter for color animations
            
            Args:
                target_widget: The widget to animate
                style_prop: The style property name (e.g., "color", "background-color")
            """
            super().__init__()
            self._target = target_widget
            self._color = QColor(Qt.GlobalColor.black)
            self._style_prop = style_prop
            self._original_stylesheet = target_widget.styleSheet()
        
        @pyqtProperty(QColor)
        def color(self):
            """Getter for color property"""
            return self._color
            
        @color.setter
        def color(self, new_color):
            """Setter for color property"""
            if self._color != new_color:
                self._color = new_color
                
                # Apply to stylesheet
                current_style = self._target.styleSheet()
                
                # Extract the original style if it exists or create a new one
                if f"{self._style_prop}:" in current_style:
                    style_parts = current_style.split(";")
                    new_parts = []
                    for part in style_parts:
                        if part.strip().startswith(f"{self._style_prop}:"):
                            new_parts.append(f"{self._style_prop}: {new_color.name()}")
                        elif part.strip():
                            new_parts.append(part.strip())
                    new_style = "; ".join(new_parts)
                    if not new_style.endswith(";"):
                        new_style += ";"
                else:
                    # No existing style property, add it
                    new_style = current_style
                    if new_style and not new_style.endswith(";"):
                        new_style += ";"
                    new_style += f" {self._style_prop}: {new_color.name()};"
                
                self._target.setStyleSheet(new_style)
    
    @staticmethod
    def create(widget, property_name, start_value, end_value, duration=1000, loop_count=3):
        """
        Create a pulsing animation by animating a property
        
        Args:
            widget: Target widget
            property_name: Property to animate (as bytes)
            start_value: Starting value
            end_value: End value
            duration: Duration in milliseconds
            loop_count: Number of loops (-1 for infinite)
            
        Returns:
            QPropertyAnimation: The animation object
        """
        # Special handling for color properties on labels and similar widgets
        if property_name == b"color":
            color_adapter = PulseAnimation.ColorPropertyAdapter(widget)
            animation = QPropertyAnimation(color_adapter, b"color")
            animation.setDuration(duration)
            animation.setStartValue(start_value)
            animation.setEndValue(end_value)
            animation.setLoopCount(loop_count)
            animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
            
            # Store the adapter to prevent it from being garbage collected
            widget._color_adapter = color_adapter
            
            animation.start()
            return animation
        else:
            # Standard property animation
            animation = QPropertyAnimation(widget, property_name)
            animation.setDuration(duration)
            animation.setStartValue(start_value)
            animation.setEndValue(end_value)
            animation.setLoopCount(loop_count)
            animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
            
            animation.start()
            return animation


class TerminalLoadingAnimation:
    """Creates a terminal-like loading animation"""
    
    def __init__(self, label, format_str="Loading... {}", frames=["|", "/", "-", "\\"]):
        """
        Initialize loading animation
        
        Args:
            label: QLabel to show animation on
            format_str: String format with {} for frame placement
            frames: List of characters for animation frames
        """
        self.label = label
        self.format_str = format_str
        self.frames = frames
        self.current_frame = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_frame)
    
    def start(self, interval=100):
        """
        Start the animation
        
        Args:
            interval: Frame change interval in milliseconds
        """
        self.timer.start(interval)
    
    def stop(self):
        """Stop the animation"""
        self.timer.stop()
        self.label.setText("")
    
    def _update_frame(self):
        """Update to the next animation frame"""
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        frame = self.frames[self.current_frame]
        self.label.setText(self.format_str.format(frame))


class AccessAnimation:
    """Creates access granted/denied animations"""
    
    @staticmethod
    def access_granted(widget, duration=800):
        """
        Create an 'access granted' animation (green flash)
        
        Args:
            widget: Target widget
            duration: Animation duration in milliseconds
            
        Returns:
            QSequentialAnimationGroup: The animation group
        """
        # Original style
        original_style = widget.styleSheet()
        
        # Create opacity effect
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        
        # Flash animation
        flash = QPropertyAnimation(effect, b"opacity")
        flash.setDuration(duration // 2)
        flash.setStartValue(1.0)
        flash.setEndValue(0.7)
        flash.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        # Restore animation
        restore = QPropertyAnimation(effect, b"opacity")
        restore.setDuration(duration // 2)
        restore.setStartValue(0.7)
        restore.setEndValue(1.0)
        restore.setEasingCurve(QEasingCurve.Type.InQuad)
        
        # Set the "granted" style with green border
        widget.setStyleSheet(original_style + "border: 2px solid #00cc66; background-color: rgba(0, 204, 102, 0.2);")
        
        # Animation group
        animation_group = QSequentialAnimationGroup()
        animation_group.addAnimation(flash)
        animation_group.addAnimation(restore)
        
        # Reset style when done
        animation_group.finished.connect(lambda: widget.setStyleSheet(original_style))
        
        # Start animation
        animation_group.start()
        
        return animation_group
    
    @staticmethod
    def access_denied(widget, duration=800):
        """
        Create an 'access denied' animation (red flash)
        
        Args:
            widget: Target widget
            duration: Animation duration in milliseconds
            
        Returns:
            QSequentialAnimationGroup: The animation group
        """
        # Original style
        original_style = widget.styleSheet()
        
        # Create opacity effect
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        
        # Flash animation
        flash = QPropertyAnimation(effect, b"opacity")
        flash.setDuration(duration // 2)
        flash.setStartValue(1.0)
        flash.setEndValue(0.7)
        flash.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        # Restore animation
        restore = QPropertyAnimation(effect, b"opacity")
        restore.setDuration(duration // 2)
        restore.setStartValue(0.7)
        restore.setEndValue(1.0)
        restore.setEasingCurve(QEasingCurve.Type.InQuad)
        
        # Set the "denied" style with red border
        widget.setStyleSheet(original_style + "border: 2px solid #cc0000; background-color: rgba(204, 0, 0, 0.2);")
        
        # Animation group
        animation_group = QSequentialAnimationGroup()
        animation_group.addAnimation(flash)
        animation_group.addAnimation(restore)
        
        # Reset style when done
        animation_group.finished.connect(lambda: widget.setStyleSheet(original_style))
        
        # Start animation
        animation_group.start()
        
        return animation_group


class CyberDoorTransition:
    """Simulates a cyber door opening transition"""
    
    @staticmethod
    def door_open(container_widget, new_content_widget, direction="horizontal", duration=800):
        """
        Create a door opening transition to reveal new content
        
        Args:
            container_widget: Widget that contains both panels
            new_content_widget: Widget to reveal
            direction: "horizontal" or "vertical" door split
            duration: Animation duration in milliseconds
            
        Returns:
            QParallelAnimationGroup: The animation group
        """
        print(f"CyberDoorTransition.door_open: container={container_widget}, new_content={new_content_widget}")
        # Create left/top and right/bottom door panels
        left_panel = QFrame(container_widget)
        right_panel = QFrame(container_widget)
        
        # Set door panel styles
        panel_style = """
            background-color: #1a1a2e;
            border: 1px solid #0f3460;
        """
        left_panel.setStyleSheet(panel_style)
        right_panel.setStyleSheet(panel_style)
        
        # Calculate positions based on direction
        if direction == "horizontal":
            # Horizontal split (left/right doors)
            panel_width = container_widget.width() // 2
            panel_height = container_widget.height()
            
            print(f"Container dimensions: {container_widget.width()}x{container_widget.height()}")
            print(f"Panel dimensions: {panel_width}x{panel_height}")
            
            left_panel.setGeometry(0, 0, panel_width, panel_height)
            right_panel.setGeometry(panel_width, 0, panel_width, panel_height)
            
            # Create animations
            left_anim = QPropertyAnimation(left_panel, b"geometry")
            left_anim.setDuration(duration)
            left_anim.setStartValue(left_panel.geometry())
            left_anim.setEndValue(QRect(-panel_width, 0, panel_width, panel_height))
            left_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            right_anim = QPropertyAnimation(right_panel, b"geometry")
            right_anim.setDuration(duration)
            right_anim.setStartValue(right_panel.geometry())
            right_anim.setEndValue(QRect(container_widget.width(), 0, panel_width, panel_height))
            right_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        else:
            # Vertical split (top/bottom doors)
            panel_width = container_widget.width()
            panel_height = container_widget.height() // 2
            
            left_panel.setGeometry(0, 0, panel_width, panel_height)
            right_panel.setGeometry(0, panel_height, panel_width, panel_height)
            
            # Create animations
            left_anim = QPropertyAnimation(left_panel, b"geometry")
            left_anim.setDuration(duration)
            left_anim.setStartValue(left_panel.geometry())
            left_anim.setEndValue(QRect(0, -panel_height, panel_width, panel_height))
            left_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            right_anim = QPropertyAnimation(right_panel, b"geometry")
            right_anim.setDuration(duration)
            right_anim.setStartValue(right_panel.geometry())
            right_anim.setEndValue(QRect(0, container_widget.height(), panel_width, panel_height))
            right_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Show the content before starting the animation
        print(f"Making the new content widget visible: {new_content_widget}")
        new_content_widget.show()
        
        # Bring the door panels to the front
        left_panel.raise_()
        right_panel.raise_()
        
        # Animation group
        animation_group = QParallelAnimationGroup()
        animation_group.addAnimation(left_anim)
        animation_group.addAnimation(right_anim)
        
        # Clean up when done
        print("Setting up animation finished callbacks")
        animation_group.finished.connect(lambda: print("Animation finished - content already visible"))
        animation_group.finished.connect(lambda: left_panel.deleteLater())
        animation_group.finished.connect(lambda: right_panel.deleteLater())
        
        # Start animation
        print("Starting door animation")
        animation_group.start()
        print("Door animation started")
        
        return animation_group
    
    @staticmethod
    def cyber_unlock(widget, duration=1200):
        """
        Create a cyber unlock animation
        
        Args:
            widget: Target widget
            duration: Animation duration in milliseconds
            
        Returns:
            QSequentialAnimationGroup: The animation group
        """
        # Save original style
        original_style = widget.styleSheet()
        
        # Border light up
        border_styles = [
            "border: 1px solid #00ff99;",
            "border: 2px solid #00ff99;",
            "border: 3px solid #00ff99;",
            "border: 4px solid #00ff99;"
        ]
        
        # Animation group
        animation_group = QSequentialAnimationGroup()
        
        # Add border animations
        step_duration = duration // (len(border_styles) * 2)
        for style in border_styles:
            # Create timer for this step
            timer = QTimer()
            timer.setSingleShot(True)
            timer.timeout.connect(lambda s=style: widget.setStyleSheet(original_style + s))
            timer.start(animation_group.duration() + step_duration)
            
            # Add delay
            delay_anim = QPropertyAnimation(widget, b"pos")
            delay_anim.setDuration(step_duration)
            delay_anim.setStartValue(widget.pos())
            delay_anim.setEndValue(widget.pos())
            animation_group.addAnimation(delay_anim)
        
        # Restore original style at the end
        animation_group.finished.connect(lambda: widget.setStyleSheet(original_style))
        
        # Start animation
        animation_group.start()
        
        return animation_group 