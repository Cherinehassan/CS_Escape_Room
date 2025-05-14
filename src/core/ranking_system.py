#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ranking system for Cybersecurity Escape Room
Manages global rankings and comparisons between users
"""

import os
import json
import glob
from datetime import datetime
from operator import itemgetter


class RankingSystem:
    """Manages global rankings between users"""
    
    def __init__(self):
        """Initialize the ranking system"""
        self.data_dir = "data/users"
        self.rankings_cache = None
        self.last_update = None
        
    def _load_all_user_data(self):
        """Load data for all users in the system"""
        users_data = []
        
        if not os.path.exists(self.data_dir):
            return users_data
            
        # Find all user data files
        user_files = glob.glob(os.path.join(self.data_dir, "*.json"))
        
        for file_path in user_files:
            try:
                with open(file_path, 'r') as file:
                    user_data = json.load(file)
                    
                    # Calculate metrics for ranking
                    username = user_data.get("username", "Unknown")
                    completed_puzzles = user_data.get("completed_puzzles", [])
                    puzzle_times = user_data.get("puzzle_completion_times", {})
                    
                    # Skip empty user profiles
                    if not completed_puzzles:
                        continue
                        
                    # Calculate average completion time
                    avg_time = sum(puzzle_times.values()) / len(puzzle_times) if puzzle_times else 0
                    
                    # Calculate total points (100 points per puzzle, bonus for fast completion)
                    total_points = 0
                    for puzzle_id in completed_puzzles:
                        # Base points for completion
                        points = 100
                        
                        # Time bonus (faster = more points)
                        if str(puzzle_id) in puzzle_times:
                            time = puzzle_times[str(puzzle_id)]
                            if time < 30:  # Under 30 seconds
                                points += 50
                            elif time < 60:  # Under 1 minute
                                points += 30
                            elif time < 120:  # Under 2 minutes
                                points += 10
                                
                        total_points += points
                    
                    # Add user ranking data
                    users_data.append({
                        "username": username,
                        "completed_count": len(completed_puzzles),
                        "avg_completion_time": avg_time,
                        "points": total_points,
                        "achievements": len(user_data.get("achievements", [])),
                        "time_played": user_data.get("time_played", 0)
                    })
            except Exception as e:
                print(f"Error loading user data for ranking: {e}")
                continue
                
        return users_data
    
    def get_rankings(self, force_refresh=False):
        """
        Get global rankings of all users
        
        Args:
            force_refresh: Whether to force a refresh of cached rankings
            
        Returns:
            list: List of user ranking data sorted by points
        """
        # Check if we need to refresh the cache
        current_time = datetime.now()
        cache_expired = (self.last_update is None or 
                        (current_time - self.last_update).total_seconds() > 300)  # 5 minutes
        
        if self.rankings_cache is None or force_refresh or cache_expired:
            # Load all user data
            users_data = self._load_all_user_data()
            
            # Sort by points (descending) and then by avg_completion_time (ascending - faster is better)
            self.rankings_cache = sorted(
                users_data, 
                key=lambda x: (-x["points"], x["avg_completion_time"])
            )
            self.last_update = current_time
            
            # Add rank to each user
            for i, user in enumerate(self.rankings_cache):
                user["rank"] = i + 1
        
        return self.rankings_cache
    
    def get_user_rank(self, username):
        """
        Get rank information for a specific user
        
        Args:
            username: Username to get rank for
            
        Returns:
            dict: User rank data or None if not found
        """
        rankings = self.get_rankings()
        
        for user in rankings:
            if user["username"] == username:
                return user
                
        return None
    
    def get_leaderboard(self, count=10):
        """
        Get the top users for the leaderboard
        
        Args:
            count: Number of top users to return
            
        Returns:
            list: Top users data
        """
        rankings = self.get_rankings()
        return rankings[:count] 