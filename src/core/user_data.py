#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User data management for Cybersecurity Escape Room
Handles user progress, statistics, and achievements
"""

import json
import os
import time
from datetime import datetime


class UserData:
    """Manages user data and progress"""
    
    def __init__(self, username=None):
        """
        Initialize user data
        
        Args:
            username: Username for this user data
        """
        self.username = username
        self.data_dir = "data/users"
        
        # Clear all data first to ensure we start fresh
        self._reset_data()
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Load existing data if username is provided
        if username:
            self.load()
    
    def _reset_data(self):
        """Reset all user data to default values"""
        self.completed_puzzles = set()  # Set of completed puzzle IDs
        self.viewed_puzzles = set()     # Set of viewed puzzle IDs
        self.puzzle_completion_times = {}  # Puzzle ID to completion time (seconds)
        self.puzzle_attempts = {}       # Puzzle ID to number of attempts
        self.achievements = set()       # Set of unlocked achievement IDs
        self.time_played = 0            # Total time played in seconds
        self.last_login = datetime.now().isoformat()
        self.session_start_time = time.time()
    
    def mark_puzzle_completed(self, puzzle_id, completion_time=None):
        """
        Mark a puzzle as completed
        
        Args:
            puzzle_id: ID of the completed puzzle
            completion_time: Time taken to complete the puzzle (in seconds)
        """
        self.completed_puzzles.add(puzzle_id)
        
        if completion_time is not None:
            # Update fastest completion time if better or first completion
            if puzzle_id not in self.puzzle_completion_times or completion_time < self.puzzle_completion_times[puzzle_id]:
                self.puzzle_completion_times[puzzle_id] = completion_time
        
        # Add to viewed puzzles as well
        self.viewed_puzzles.add(puzzle_id)
    
    def mark_puzzle_viewed(self, puzzle_id):
        """
        Mark a puzzle as viewed
        
        Args:
            puzzle_id: ID of the viewed puzzle
        """
        self.viewed_puzzles.add(puzzle_id)
    
    def record_puzzle_attempt(self, puzzle_id):
        """
        Record an attempt at solving a puzzle
        
        Args:
            puzzle_id: ID of the attempted puzzle
        """
        if puzzle_id in self.puzzle_attempts:
            self.puzzle_attempts[puzzle_id] += 1
        else:
            self.puzzle_attempts[puzzle_id] = 1
    
    def unlock_achievement(self, achievement_id):
        """
        Unlock an achievement
        
        Args:
            achievement_id: ID of the achievement to unlock
            
        Returns:
            bool: True if newly unlocked, False if already unlocked
        """
        if achievement_id in self.achievements:
            return False
        
        self.achievements.add(achievement_id)
        return True
    
    def update_time_played(self):
        """Update the total time played by adding the current session time"""
        current_time = time.time()
        session_duration = current_time - self.session_start_time
        self.time_played += session_duration
        self.session_start_time = current_time
    
    def get_recommended_puzzles(self, puzzle_manager, count=3):
        """
        Get recommended puzzles based on user progress
        
        Args:
            puzzle_manager: PuzzleManager instance
            count: Number of puzzles to recommend
            
        Returns:
            list: List of recommended puzzle objects
        """
        # Get all incomplete puzzles
        incomplete_puzzles = [p for p in puzzle_manager.get_all_puzzles() 
                             if p.id not in self.completed_puzzles]
        
        if not incomplete_puzzles:
            return []
        
        # Get any puzzles in categories the user has started but not completed
        started_categories = set()
        for puzzle_id in self.viewed_puzzles:
            puzzle = puzzle_manager.get_puzzle_by_id(puzzle_id)
            if puzzle and puzzle.id not in self.completed_puzzles:
                started_categories.add(puzzle.category)
        
        # First, try to recommend puzzles from started categories
        recommendations = []
        if started_categories:
            for category in started_categories:
                category_puzzles = [p for p in incomplete_puzzles if p.category == category]
                if category_puzzles:
                    # Sort by difficulty (easy to hard)
                    difficulty_order = {"Easy": 1, "Medium": 2, "Hard": 3}
                    sorted_puzzles = sorted(category_puzzles, 
                                           key=lambda p: difficulty_order.get(p.difficulty, 4))
                    recommendations.extend(sorted_puzzles)
        
        # If we need more, add puzzles the user hasn't seen at all
        if len(recommendations) < count:
            unseen_puzzles = [p for p in incomplete_puzzles if p.id not in self.viewed_puzzles]
            # Sort by difficulty (easy to hard)
            difficulty_order = {"Easy": 1, "Medium": 2, "Hard": 3}
            sorted_unseen = sorted(unseen_puzzles, key=lambda p: difficulty_order.get(p.difficulty, 4))
            recommendations.extend(sorted_unseen)
        
        # Return the requested number of recommendations
        return recommendations[:count]
    
    def get_statistics(self):
        """
        Get user statistics
        
        Returns:
            dict: Dictionary of user statistics
        """
        # Update time played first
        self.update_time_played()
        
        # Calculate statistics
        total_puzzles_attempted = len(self.viewed_puzzles)
        total_puzzles_completed = len(self.completed_puzzles)
        completion_rate = total_puzzles_completed / total_puzzles_attempted if total_puzzles_attempted > 0 else 0
        
        avg_attempts = 0
        if self.puzzle_attempts and self.completed_puzzles:
            completed_attempts = sum(self.puzzle_attempts.get(pid, 1) for pid in self.completed_puzzles)
            avg_attempts = completed_attempts / len(self.completed_puzzles)
        
        avg_completion_time = 0
        if self.puzzle_completion_times:
            avg_completion_time = sum(self.puzzle_completion_times.values()) / len(self.puzzle_completion_times)
        
        fastest_completion = min(self.puzzle_completion_times.values()) if self.puzzle_completion_times else 0
        
        return {
            "total_puzzles_attempted": total_puzzles_attempted,
            "total_puzzles_completed": total_puzzles_completed,
            "completion_rate": completion_rate,
            "avg_attempts": avg_attempts,
            "avg_completion_time": avg_completion_time,
            "fastest_completion": fastest_completion,
            "time_played": self.time_played,
            "achievements_unlocked": len(self.achievements)
        }
    
    def save(self):
        """Save user data to file"""
        if not self.username:
            return False
        
        # Update time played before saving
        self.update_time_played()
        
        # Prepare data for serialization
        # Convert sets to lists and ensure dictionary keys are strings for JSON
        data = {
            "username": self.username,
            "completed_puzzles": list(self.completed_puzzles),
            "viewed_puzzles": list(self.viewed_puzzles),
            "puzzle_completion_times": {str(k): v for k, v in self.puzzle_completion_times.items()},
            "puzzle_attempts": {str(k): v for k, v in self.puzzle_attempts.items()},
            "achievements": list(self.achievements),
            "time_played": self.time_played,
            "last_login": datetime.now().isoformat()
        }
        
        # Save to file
        filename = os.path.join(self.data_dir, f"{self.username}.json")
        try:
            with open(filename, 'w') as file:
                json.dump(data, file, indent=2)
            print(f"Saved data for user {self.username}: {len(self.completed_puzzles)} completed puzzles")
            return True
        except Exception as e:
            print(f"Error saving user data: {e}")
            return False
    
    def load(self):
        """Load user data from file"""
        if not self.username:
            return False
        
        # Reset data before loading to ensure we don't keep any old data
        self._reset_data()
        
        filename = os.path.join(self.data_dir, f"{self.username}.json")
        
        if not os.path.exists(filename):
            print(f"No saved data found for user {self.username}, creating new profile")
            return False
        
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                
                # Update attributes
                self.completed_puzzles = set(data.get("completed_puzzles", []))
                self.viewed_puzzles = set(data.get("viewed_puzzles", []))
                self.puzzle_completion_times = data.get("puzzle_completion_times", {})
                
                # Convert puzzle completion time keys to integers
                # (JSON serializes dictionary keys as strings)
                if self.puzzle_completion_times:
                    self.puzzle_completion_times = {
                        int(k): v for k, v in self.puzzle_completion_times.items()
                    }
                
                self.puzzle_attempts = data.get("puzzle_attempts", {})
                # Convert puzzle attempt keys to integers
                if self.puzzle_attempts:
                    self.puzzle_attempts = {
                        int(k): v for k, v in self.puzzle_attempts.items()
                    }
                
                self.achievements = set(data.get("achievements", []))
                self.time_played = data.get("time_played", 0)
                self.last_login = data.get("last_login", datetime.now().isoformat())
                
                print(f"Loaded data for user {self.username}: {len(self.completed_puzzles)} completed puzzles")
                return True
        except Exception as e:
            print(f"Error loading user data: {e}")
            # Reset data if there was an error
            self._reset_data()
            return False


class Achievement:
    """Represents an achievement in the game"""
    
    def __init__(self, achievement_id, title, description, icon_path=None):
        """
        Initialize achievement
        
        Args:
            achievement_id: Unique identifier for this achievement
            title: Achievement title
            description: Achievement description
            icon_path: Path to achievement icon
        """
        self.id = achievement_id
        self.title = title
        self.description = description
        self.icon_path = icon_path


class AchievementManager:
    """Manages achievements and checks for unlocks"""
    
    def __init__(self):
        """Initialize achievement manager"""
        self.achievements = {}
        self._define_achievements()
    
    def _define_achievements(self):
        """Define standard achievements"""
        # First completion achievements
        self.achievements["first_steps"] = Achievement(
            "first_steps",
            "First Steps",
            "Complete your first puzzle"
        )
        
        # Category mastery achievements
        categories = ["Cryptography", "Social Engineering", "Hashing", "Authentication", "Encryption"]
        for category in categories:
            category_id = category.lower().replace(" ", "_")
            self.achievements[f"{category_id}_master"] = Achievement(
                f"{category_id}_master",
                f"{category} Master",
                f"Complete all {category} puzzles"
            )
        
        # Performance achievements
        self.achievements["speed_demon"] = Achievement(
            "speed_demon",
            "Speed Demon",
            "Complete a puzzle in under 30 seconds"
        )
        
        self.achievements["half_way"] = Achievement(
            "half_way",
            "Half Way There",
            "Complete 50% of all puzzles"
        )
        
        self.achievements["master_escapist"] = Achievement(
            "master_escapist",
            "Master Escapist",
            "Complete all puzzles"
        )
    
    def get_achievement(self, achievement_id):
        """
        Get achievement by ID
        
        Args:
            achievement_id: Achievement ID
            
        Returns:
            Achievement: Achievement object or None if not found
        """
        return self.achievements.get(achievement_id)
    
    def get_all_achievements(self):
        """
        Get all achievements
        
        Returns:
            list: List of all achievement objects
        """
        return list(self.achievements.values())
    
    def check_achievements(self, user_data, puzzle_manager):
        """
        Check for newly unlocked achievements
        
        Args:
            user_data: UserData instance
            puzzle_manager: PuzzleManager instance
            
        Returns:
            list: List of newly unlocked achievement objects
        """
        newly_unlocked = []
        
        # First steps achievement
        if len(user_data.completed_puzzles) > 0 and user_data.unlock_achievement("first_steps"):
            newly_unlocked.append(self.achievements["first_steps"])
        
        # Category mastery achievements
        categories = set(puzzle.category for puzzle in puzzle_manager.get_all_puzzles())
        for category in categories:
            category_id = category.lower().replace(" ", "_")
            achievement_id = f"{category_id}_master"
            
            # Check if all puzzles in this category are completed
            category_puzzles = puzzle_manager.get_puzzles_by_category(category)
            if all(puzzle.id in user_data.completed_puzzles for puzzle in category_puzzles):
                if user_data.unlock_achievement(achievement_id) and achievement_id in self.achievements:
                    newly_unlocked.append(self.achievements[achievement_id])
        
        # Speed demon achievement
        if any(time < 30 for time in user_data.puzzle_completion_times.values()):
            if user_data.unlock_achievement("speed_demon"):
                newly_unlocked.append(self.achievements["speed_demon"])
        
        # Progress achievements
        total_puzzles = len(puzzle_manager.get_all_puzzles())
        completed_count = len(user_data.completed_puzzles)
        
        if total_puzzles > 0:
            # Half way achievement
            if completed_count >= total_puzzles / 2:
                if user_data.unlock_achievement("half_way"):
                    newly_unlocked.append(self.achievements["half_way"])
            
            # Master escapist achievement
            if completed_count == total_puzzles:
                if user_data.unlock_achievement("master_escapist"):
                    newly_unlocked.append(self.achievements["master_escapist"])
        
        return newly_unlocked 