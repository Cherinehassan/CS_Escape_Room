#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Game state manager for Cybersecurity Escape Room
Tracks player progress, achievements, and manages game flow
"""

import logging
import json
from datetime import datetime, timedelta

from src.database.db_manager import (
    User, UserProfile, Puzzle, PuzzleAttempt, 
    PuzzleCategory, Achievement, UserAchievement
)

logger = logging.getLogger(__name__)


class GameStateManager:
    """Manages game state and player progress"""
    
    def __init__(self, db_manager, user_id=None):
        """
        Initialize game state manager
        
        Args:
            db_manager: Database manager instance
            user_id (int, optional): Current user ID
        """
        self.db_manager = db_manager
        self.user_id = user_id
        self.session = db_manager.get_session()
    
    def set_user(self, user_id):
        """Set the current user"""
        self.user_id = user_id
    
    def get_user_profile(self):
        """Get the current user's profile"""
        if not self.user_id:
            return None
        
        user = self.session.query(User).filter(User.id == self.user_id).first()
        if not user:
            return None
        
        profile = self.session.query(UserProfile).filter(UserProfile.user_id == self.user_id).first()
        
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'display_name': profile.display_name if profile else user.username,
            'total_points': profile.total_points if profile else 0,
            'current_streak': profile.current_streak if profile else 0,
            'highest_streak': profile.highest_streak if profile else 0,
            'tutorial_completed': profile.tutorial_completed if profile else False,
            'created_at': user.created_at,
            'last_login': user.last_login
        }
    
    def get_available_puzzles(self):
        """Get puzzles available to the current user"""
        if not self.user_id:
            return []
        
        # Get all puzzles
        puzzles = self.session.query(Puzzle).all()
        available_puzzles = []
        
        for puzzle in puzzles:
            # Check if puzzle is unlocked
            if not puzzle.locked:
                available_puzzles.append(self._format_puzzle(puzzle))
                continue
            
            # Check prerequisites
            if not puzzle.prerequisites:
                # If no prerequisites but locked, this is likely a tutorial puzzle
                # Only add if the user has not completed any puzzles yet
                attempts = self.session.query(PuzzleAttempt).filter(
                    PuzzleAttempt.user_id == self.user_id
                ).count()
                
                if attempts == 0:
                    available_puzzles.append(self._format_puzzle(puzzle))
                continue
            
            # Check if all prerequisites are completed
            prereqs = puzzle.prerequisites.split(',')
            all_completed = True
            
            for prereq_id in prereqs:
                prereq_attempt = self.session.query(PuzzleAttempt).filter(
                    PuzzleAttempt.user_id == self.user_id,
                    PuzzleAttempt.puzzle_id == int(prereq_id),
                    PuzzleAttempt.successful == True
                ).first()
                
                if not prereq_attempt:
                    all_completed = False
                    break
            
            if all_completed:
                available_puzzles.append(self._format_puzzle(puzzle))
        
        return available_puzzles
    
    def get_puzzle_details(self, puzzle_id):
        """Get detailed information about a specific puzzle"""
        puzzle = self.session.query(Puzzle).filter(Puzzle.id == puzzle_id).first()
        if not puzzle:
            return None
        
        # Check if user has attempted this puzzle before
        attempts = []
        if self.user_id:
            attempt_records = self.session.query(PuzzleAttempt).filter(
                PuzzleAttempt.user_id == self.user_id,
                PuzzleAttempt.puzzle_id == puzzle_id
            ).order_by(PuzzleAttempt.start_time.desc()).all()
            
            for attempt in attempt_records:
                attempts.append({
                    'id': attempt.id,
                    'start_time': attempt.start_time,
                    'end_time': attempt.end_time,
                    'completed': attempt.completed,
                    'successful': attempt.successful,
                    'points_earned': attempt.points_earned,
                    'hints_used': attempt.hints_used,
                    'attempt_number': attempt.attempt_number
                })
        
        # Get hints
        hints = [
            {'id': hint.id, 'hint_text': hint.hint_text, 'point_deduction': hint.point_deduction, 'order': hint.order}
            for hint in puzzle.hints
        ]
        
        puzzle_details = self._format_puzzle(puzzle)
        puzzle_details.update({
            'attempts': attempts,
            'hints': hints,
            'category_name': puzzle.category.name if puzzle.category else 'Uncategorized'
        })
        
        return puzzle_details
    
    def start_puzzle_attempt(self, puzzle_id):
        """
        Start a new puzzle attempt
        
        Args:
            puzzle_id (int): Puzzle ID
            
        Returns:
            int: Attempt ID or None if failed
        """
        if not self.user_id:
            return None
        
        try:
            # Get puzzle
            puzzle = self.session.query(Puzzle).filter(Puzzle.id == puzzle_id).first()
            if not puzzle:
                return None
            
            # Count previous attempts
            attempt_count = self.session.query(PuzzleAttempt).filter(
                PuzzleAttempt.user_id == self.user_id,
                PuzzleAttempt.puzzle_id == puzzle_id
            ).count()
            
            # Check if maximum attempts reached
            if puzzle.max_attempts and attempt_count >= puzzle.max_attempts:
                return None
            
            # Create new attempt
            attempt = PuzzleAttempt(
                user_id=self.user_id,
                puzzle_id=puzzle_id,
                start_time=datetime.utcnow(),
                completed=False,
                successful=False,
                hints_used=0,
                attempt_number=attempt_count + 1
            )
            
            self.session.add(attempt)
            self.session.commit()
            
            logger.info(f"User {self.user_id} started puzzle {puzzle_id}, attempt #{attempt.attempt_number}")
            return attempt.id
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error starting puzzle attempt: {e}", exc_info=True)
            return None
    
    def use_hint(self, attempt_id, hint_id):
        """
        Record that a hint was used during a puzzle attempt
        
        Args:
            attempt_id (int): Attempt ID
            hint_id (int): Hint ID
            
        Returns:
            bool: Success status
        """
        if not self.user_id:
            return False
        
        try:
            # Get attempt
            attempt = self.session.query(PuzzleAttempt).filter(
                PuzzleAttempt.id == attempt_id,
                PuzzleAttempt.user_id == self.user_id
            ).first()
            
            if not attempt or attempt.completed:
                return False
            
            # Get hint
            hint = self.session.query(PuzzleHint).filter(PuzzleHint.id == hint_id).first()
            if not hint or hint.puzzle_id != attempt.puzzle_id:
                return False
            
            # Update attempt
            attempt.hints_used += 1
            self.session.commit()
            
            logger.info(f"User {self.user_id} used hint {hint_id} for puzzle {attempt.puzzle_id}")
            return True
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error recording hint usage: {e}", exc_info=True)
            return False
    
    def complete_puzzle_attempt(self, attempt_id, successful):
        """
        Complete a puzzle attempt
        
        Args:
            attempt_id (int): Attempt ID
            successful (bool): Whether the attempt was successful
            
        Returns:
            dict: Result information or None if failed
        """
        if not self.user_id:
            return None
        
        try:
            # Get attempt
            attempt = self.session.query(PuzzleAttempt).filter(
                PuzzleAttempt.id == attempt_id,
                PuzzleAttempt.user_id == self.user_id
            ).first()
            
            if not attempt or attempt.completed:
                return None
            
            # Get puzzle
            puzzle = self.session.query(Puzzle).filter(Puzzle.id == attempt.puzzle_id).first()
            if not puzzle:
                return None
            
            # Calculate time spent
            now = datetime.utcnow()
            time_spent = (now - attempt.start_time).total_seconds()
            
            # Calculate points
            points_earned = 0
            if successful:
                # Base points
                points_earned = puzzle.points
                
                # Deduct points for hints used
                if attempt.hints_used > 0:
                    hints = self.session.query(PuzzleHint).filter(PuzzleHint.puzzle_id == puzzle.id).all()
                    hint_deduction = sum(hint.point_deduction for hint in hints[:attempt.hints_used])
                    points_earned -= hint_deduction
                
                # Time bonus for quick completion (if time limit exists)
                if puzzle.time_limit and time_spent < puzzle.time_limit:
                    time_ratio = 1 - (time_spent / puzzle.time_limit)
                    time_bonus = int(puzzle.points * 0.2 * time_ratio)  # Up to 20% bonus
                    points_earned += time_bonus
                
                # Ensure minimum points
                points_earned = max(points_earned, puzzle.points * 0.2)  # At least 20% of base points
            
            # Update attempt
            attempt.completed = True
            attempt.successful = successful
            attempt.end_time = now
            attempt.points_earned = points_earned
            
            # Update user profile
            profile = self.session.query(UserProfile).filter(UserProfile.user_id == self.user_id).first()
            if profile:
                # Add points
                profile.total_points += points_earned
                
                # Update streak
                if successful:
                    profile.current_streak += 1
                    profile.highest_streak = max(profile.highest_streak, profile.current_streak)
                else:
                    profile.current_streak = 0
                
                # Mark tutorial as completed if this was a tutorial puzzle
                if puzzle.category and puzzle.category.name == "Tutorial" and successful:
                    profile.tutorial_completed = True
            
            self.session.commit()
            
            # Check for achievements
            self._check_achievements()
            
            logger.info(f"User {self.user_id} completed puzzle {puzzle.id}, success={successful}, points={points_earned}")
            
            return {
                'attempt_id': attempt.id,
                'puzzle_id': puzzle.id,
                'successful': successful,
                'points_earned': points_earned,
                'time_spent': time_spent,
                'hints_used': attempt.hints_used
            }
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error completing puzzle attempt: {e}", exc_info=True)
            return None
    
    def get_user_achievements(self):
        """Get achievements earned by the current user"""
        if not self.user_id:
            return []
        
        try:
            # Get all achievements
            all_achievements = self.session.query(Achievement).all()
            
            # Get user's earned achievements
            earned_achievement_ids = {
                ua.achievement_id for ua in self.session.query(UserAchievement).filter(
                    UserAchievement.user_id == self.user_id
                ).all()
            }
            
            achievements = []
            for achievement in all_achievements:
                achievements.append({
                    'id': achievement.id,
                    'name': achievement.name,
                    'description': achievement.description,
                    'badge_image': achievement.badge_image,
                    'points': achievement.points,
                    'earned': achievement.id in earned_achievement_ids
                })
            
            return achievements
            
        except Exception as e:
            logger.error(f"Error getting user achievements: {e}", exc_info=True)
            return []
    
    def get_user_stats(self):
        """Get statistics about the user's performance"""
        if not self.user_id:
            return {}
        
        try:
            # Get all categories
            categories = self.session.query(PuzzleCategory).all()
            category_stats = {}
            
            for category in categories:
                # Get puzzles in this category
                puzzle_ids = [p.id for p in self.session.query(Puzzle).filter(Puzzle.category_id == category.id).all()]
                
                if not puzzle_ids:
                    continue
                
                # Get successful attempts for these puzzles
                successful_attempts = self.session.query(PuzzleAttempt).filter(
                    PuzzleAttempt.user_id == self.user_id,
                    PuzzleAttempt.puzzle_id.in_(puzzle_ids),
                    PuzzleAttempt.successful == True
                ).count()
                
                # Get total puzzles in category
                total_puzzles = len(puzzle_ids)
                
                category_stats[category.name] = {
                    'completed': successful_attempts,
                    'total': total_puzzles,
                    'percentage': round((successful_attempts / total_puzzles) * 100) if total_puzzles > 0 else 0
                }
            
            # Get overall stats
            total_attempts = self.session.query(PuzzleAttempt).filter(
                PuzzleAttempt.user_id == self.user_id
            ).count()
            
            successful_attempts = self.session.query(PuzzleAttempt).filter(
                PuzzleAttempt.user_id == self.user_id,
                PuzzleAttempt.successful == True
            ).count()
            
            # Get accuracy
            accuracy = round((successful_attempts / total_attempts) * 100) if total_attempts > 0 else 0
            
            # Get profile info
            profile = self.session.query(UserProfile).filter(UserProfile.user_id == self.user_id).first()
            
            return {
                'total_points': profile.total_points if profile else 0,
                'current_streak': profile.current_streak if profile else 0,
                'highest_streak': profile.highest_streak if profile else 0,
                'total_attempts': total_attempts,
                'successful_attempts': successful_attempts,
                'accuracy': accuracy,
                'categories': category_stats
            }
            
        except Exception as e:
            logger.error(f"Error getting user stats: {e}", exc_info=True)
            return {}
    
    def get_recommended_puzzles(self, limit=3):
        """
        Get recommended puzzles for the user based on performance
        
        Args:
            limit (int): Maximum number of recommendations
            
        Returns:
            list: Recommended puzzles
        """
        if not self.user_id:
            return []
        
        try:
            # Get user profile
            profile = self.session.query(UserProfile).filter(UserProfile.user_id == self.user_id).first()
            if not profile:
                return []
            
            # Get all user attempts
            attempts = self.session.query(PuzzleAttempt).filter(
                PuzzleAttempt.user_id == self.user_id
            ).all()
            
            # Group attempts by puzzle and calculate success rate
            puzzle_stats = {}
            for attempt in attempts:
                if attempt.puzzle_id not in puzzle_stats:
                    puzzle_stats[attempt.puzzle_id] = {
                        'total': 0,
                        'successful': 0
                    }
                
                puzzle_stats[attempt.puzzle_id]['total'] += 1
                if attempt.successful:
                    puzzle_stats[attempt.puzzle_id]['successful'] += 1
            
            # Calculate performance by category
            category_performance = {}
            for puzzle_id, stats in puzzle_stats.items():
                puzzle = self.session.query(Puzzle).filter(Puzzle.id == puzzle_id).first()
                if not puzzle or not puzzle.category:
                    continue
                
                category_id = puzzle.category_id
                success_rate = stats['successful'] / stats['total'] if stats['total'] > 0 else 0
                
                if category_id not in category_performance:
                    category_performance[category_id] = {
                        'success_rate': 0,
                        'count': 0
                    }
                
                # Update category stats
                category_performance[category_id]['success_rate'] = (
                    (category_performance[category_id]['success_rate'] * category_performance[category_id]['count'] + success_rate) /
                    (category_performance[category_id]['count'] + 1)
                )
                category_performance[category_id]['count'] += 1
            
            # Get available puzzles
            available_puzzles = self.get_available_puzzles()
            if not available_puzzles:
                return []
            
            # Filter out already completed puzzles
            completed_puzzle_ids = {
                attempt.puzzle_id for attempt in attempts if attempt.successful
            }
            
            available_puzzles = [p for p in available_puzzles if p['id'] not in completed_puzzle_ids]
            
            # Rank puzzles based on user performance
            ranked_puzzles = []
            for puzzle in available_puzzles:
                puzzle_obj = self.session.query(Puzzle).filter(Puzzle.id == puzzle['id']).first()
                if not puzzle_obj or not puzzle_obj.category:
                    continue
                
                category_id = puzzle_obj.category_id
                
                # Calculate difficulty score (0-1)
                difficulty_score = {
                    'easy': 0.33,
                    'medium': 0.66,
                    'hard': 1.0
                }.get(puzzle_obj.difficulty.lower(), 0.5)
                
                # Adjust difficulty score based on category performance
                if category_id in category_performance:
                    # High success rate → recommend harder puzzles
                    # Low success rate → recommend easier puzzles
                    performance_modifier = category_performance[category_id]['success_rate'] * 0.5
                    ranking_score = difficulty_score + performance_modifier
                else:
                    # If no performance data, use base difficulty score
                    ranking_score = difficulty_score
                
                ranked_puzzles.append((puzzle, ranking_score))
            
            # Sort puzzles by ranking score
            ranked_puzzles.sort(key=lambda x: x[1])
            
            # Return recommended puzzles
            return [p[0] for p in ranked_puzzles[:limit]]
            
        except Exception as e:
            logger.error(f"Error getting recommended puzzles: {e}", exc_info=True)
            return []
    
    def _format_puzzle(self, puzzle):
        """Format puzzle object as dictionary"""
        return {
            'id': puzzle.id,
            'title': puzzle.title,
            'description': puzzle.description,
            'category_id': puzzle.category_id,
            'difficulty': puzzle.difficulty,
            'max_attempts': puzzle.max_attempts,
            'points': puzzle.points,
            'time_limit': puzzle.time_limit,
            'locked': puzzle.locked,
            'prerequisites': puzzle.prerequisites,
            'learning_objective': puzzle.learning_objective
        }
    
    def _check_achievements(self):
        """Check and award achievements based on user activity"""
        if not self.user_id:
            return
        
        try:
            # Get all achievements
            achievements = self.session.query(Achievement).all()
            
            # Get user's earned achievements
            earned_achievement_ids = {
                ua.achievement_id for ua in self.session.query(UserAchievement).filter(
                    UserAchievement.user_id == self.user_id
                ).all()
            }
            
            # Get user profile
            profile = self.session.query(UserProfile).filter(UserProfile.user_id == self.user_id).first()
            if not profile:
                return
            
            # Get user attempts
            attempts = self.session.query(PuzzleAttempt).filter(
                PuzzleAttempt.user_id == self.user_id
            ).all()
            
            new_achievements = []
            
            for achievement in achievements:
                # Skip already earned achievements
                if achievement.id in earned_achievement_ids:
                    continue
                
                # Parse requirement
                req = achievement.requirement
                earned = False
                
                # Tutorial completion
                if req == "tutorial_completed" and profile.tutorial_completed:
                    earned = True
                
                # Category completion
                elif req.startswith("category:"):
                    _, category_name, count = req.split(":")
                    count = int(count)
                    
                    # Get category ID
                    category = self.session.query(PuzzleCategory).filter(
                        PuzzleCategory.name == category_name
                    ).first()
                    
                    if category:
                        # Get puzzles in this category
                        puzzles = self.session.query(Puzzle).filter(
                            Puzzle.category_id == category.id
                        ).all()
                        puzzle_ids = [p.id for p in puzzles]
                        
                        # Count successful attempts for these puzzles
                        successful = set()
                        for attempt in attempts:
                            if attempt.puzzle_id in puzzle_ids and attempt.successful:
                                successful.add(attempt.puzzle_id)
                        
                        if len(successful) >= count:
                            earned = True
                
                # No hints
                elif req.startswith("no_hints:"):
                    _, min_count = req.split(":")
                    min_count = int(min_count)
                    
                    no_hint_count = sum(
                        1 for attempt in attempts
                        if attempt.successful and attempt.hints_used == 0
                    )
                    
                    if no_hint_count >= min_count:
                        earned = True
                
                # Time-based
                elif req.startswith("time:"):
                    _, max_seconds = req.split(":")
                    max_seconds = int(max_seconds)
                    
                    for attempt in attempts:
                        if not attempt.successful or not attempt.end_time:
                            continue
                        
                        time_spent = (attempt.end_time - attempt.start_time).total_seconds()
                        if time_spent <= max_seconds:
                            earned = True
                            break
                
                # Add achievement if earned
                if earned:
                    user_achievement = UserAchievement(
                        user_id=self.user_id,
                        achievement_id=achievement.id,
                        earned_date=datetime.utcnow()
                    )
                    
                    self.session.add(user_achievement)
                    new_achievements.append(achievement)
                    
                    # Add achievement points to user
                    profile.total_points += achievement.points
            
            # Commit changes if any achievements were earned
            if new_achievements:
                self.session.commit()
                logger.info(f"User {self.user_id} earned achievements: {[a.name for a in new_achievements]}")
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error checking achievements: {e}", exc_info=True)
    
    def close(self):
        """Close database session"""
        self.session.close() 