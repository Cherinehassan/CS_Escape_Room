#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Puzzle manager for Cybersecurity Escape Room
Loads and manages puzzles from JSON file
"""

import json
import os


class Puzzle:
    """Represents a puzzle in the game"""
    
    def __init__(self, puzzle_data):
        """
        Initialize a puzzle from data
        
        Args:
            puzzle_data: Dictionary with puzzle data
        """
        self.id = puzzle_data.get("id", 0)
        self.name = puzzle_data.get("name", "Unnamed Puzzle")
        self.description = puzzle_data.get("description", "")
        self.learning_objective = puzzle_data.get("learning_objective", "")
        self.category = puzzle_data.get("category", "General")
        self.difficulty = puzzle_data.get("difficulty", "Medium")
        self.hints = puzzle_data.get("hints", [])
        self.answer = puzzle_data.get("answer", "")
        self.alternate_answers = puzzle_data.get("alternate_answers", [])
    
    def check_answer(self, user_answer, partial_match=False):
        """
        Check if an answer is correct
        
        Args:
            user_answer: User's answer to check
            partial_match: Whether to allow partial matches
            
        Returns:
            bool: True if answer is correct
        """
        # Normalize answers for comparison
        normalized_user = user_answer.strip().lower()
        normalized_correct = self.answer.strip().lower()
        
        # Check main answer
        if normalized_user == normalized_correct:
            return True
        
        # Check alternate answers
        for alt in self.alternate_answers:
            if normalized_user == alt.strip().lower():
                return True
        
        # Check for partial match if allowed
        if partial_match and normalized_correct and normalized_user:
            # Check if user answer is part of the correct answer
            if normalized_user in normalized_correct:
                return True
            
            # Check if correct answer is part of the user answer
            if normalized_correct in normalized_user:
                return True
            
            # Check alternate answers for partial matches
            for alt in self.alternate_answers:
                normalized_alt = alt.strip().lower()
                if normalized_user in normalized_alt or normalized_alt in normalized_user:
                    return True
        
        return False


class PuzzleManager:
    """Manages puzzles for the application"""
    
    def __init__(self):
        """Initialize puzzle manager"""
        self.puzzles = []
        self.puzzles_by_id = {}
        self.puzzles_by_category = {}
    
    def load_puzzles(self, json_file):
        """
        Load puzzles from a JSON file
        
        Args:
            json_file: Path to the JSON file
            
        Returns:
            bool: True if puzzles were loaded successfully
        """
        # If file doesn't exist, create sample data
        if not os.path.exists(json_file):
            self._create_sample_data(json_file)
        
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
                
                # Clear existing puzzles
                self.puzzles = []
                self.puzzles_by_id = {}
                self.puzzles_by_category = {}
                
                # Process puzzles
                for puzzle_data in data:
                    puzzle = Puzzle(puzzle_data)
                    self.puzzles.append(puzzle)
                    self.puzzles_by_id[puzzle.id] = puzzle
                    
                    # Group by category
                    if puzzle.category not in self.puzzles_by_category:
                        self.puzzles_by_category[puzzle.category] = []
                    self.puzzles_by_category[puzzle.category].append(puzzle)
                
                return True
        except Exception as e:
            print(f"Error loading puzzles: {e}")
            
            # Create sample data if there was an error
            self._create_sample_data(json_file)
            return self.load_puzzles(json_file)
    
    def _create_sample_data(self, json_file):
        """
        Create sample puzzle data
        
        Args:
            json_file: Path to save the sample data
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(json_file), exist_ok=True)
        
        # Sample puzzle data
        sample_data = [
            {
                "id": 1,
                "name": "Password Strength",
                "description": "Evaluate which of these passwords is the strongest: 'password123', 'P@ssw0rd!', 'LongButSimplePasswordPhrase'",
                "learning_objective": "Understand password strength factors",
                "category": "Authentication",
                "difficulty": "Easy",
                "hints": ["Consider length vs. complexity", "Special characters add strength"],
                "answer": "LongButSimplePasswordPhrase",
                "alternate_answers": ["the third one", "3"]
            },
            {
                "id": 2,
                "name": "Caesar Cipher",
                "description": "Decrypt this message: 'Fdhvdu flskhu lv edvlf'. The key is 3.",
                "learning_objective": "Learn basic substitution ciphers",
                "category": "Cryptography",
                "difficulty": "Easy",
                "hints": ["Shift each letter backwards by the key amount", "A becomes X, B becomes Y, etc."],
                "answer": "Caesar cipher is basic",
                "alternate_answers": []
            },
            {
                "id": 3,
                "name": "Phishing Email",
                "description": "Identify the signs of phishing in this email: 'Dear customer, we've noticed suspicious activity on your account. Click here to verify: www.amaz0n-security.net'",
                "learning_objective": "Recognize phishing attempts",
                "category": "Social Engineering",
                "difficulty": "Medium",
                "hints": ["Check the URL carefully", "Look for urgency tactics"],
                "answer": "fake domain",
                "alternate_answers": ["suspicious url", "misspelled domain", "urgency", "not amazon.com"]
            },
            {
                "id": 4,
                "name": "SQL Injection",
                "description": "What would this input do to a vulnerable login form? username: admin' --",
                "learning_objective": "Understand SQL injection attacks",
                "category": "Authentication",
                "difficulty": "Medium",
                "hints": ["The -- is a comment in SQL", "What happens to the rest of the query?"],
                "answer": "bypass password check",
                "alternate_answers": ["log in as admin", "comment out password verification"]
            },
            {
                "id": 5,
                "name": "Hash Verification",
                "description": "Which of these files has been modified? Original SHA-256: a8d4b32c98b7e3f96576da286da72964. File 1: a8d4b32c98b7e3f96576da286da72964. File 2: a8d4b32c98b7e3f96576da286da72965.",
                "learning_objective": "Understand hash verification",
                "category": "Hashing",
                "difficulty": "Medium",
                "hints": ["Compare the hash values carefully", "Even a small change creates a completely different hash"],
                "answer": "File 2",
                "alternate_answers": ["the second file", "2"]
            }
        ]
        
        # Save sample data
        with open(json_file, 'w') as file:
            json.dump(sample_data, file, indent=2)
    
    def get_all_puzzles(self):
        """
        Get all puzzles
        
        Returns:
            list: List of all puzzles
        """
        return self.puzzles
    
    def get_puzzle_by_id(self, puzzle_id):
        """
        Get a puzzle by ID
        
        Args:
            puzzle_id: Puzzle ID
            
        Returns:
            Puzzle: Puzzle object or None if not found
        """
        return self.puzzles_by_id.get(puzzle_id)
    
    def get_puzzles_by_category(self, category):
        """
        Get puzzles by category
        
        Args:
            category: Category name
            
        Returns:
            list: List of puzzles in the category
        """
        return self.puzzles_by_category.get(category, [])
    
    def get_puzzles_by_difficulty(self, difficulty):
        """
        Get puzzles by difficulty
        
        Args:
            difficulty: Difficulty level
            
        Returns:
            list: List of puzzles with the specified difficulty
        """
        return [p for p in self.puzzles if p.difficulty == difficulty] 