#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Database manager for Cybersecurity Escape Room
Handles all database operations and models
"""

import os
import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session

logger = logging.getLogger(__name__)

# Define base class for SQLAlchemy models
Base = declarative_base()


class User(Base):
    """User model for authentication and profile information"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    account_type = Column(String(20), default='player')  # player, admin
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    attempts = relationship("PuzzleAttempt", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


class UserProfile(Base):
    """Extended user profile information"""
    __tablename__ = 'user_profiles'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    display_name = Column(String(50))
    total_points = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    highest_streak = Column(Integer, default=0)
    tutorial_completed = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="profile")
    
    def __repr__(self):
        return f"<UserProfile(display_name='{self.display_name}', points={self.total_points})>"


class PuzzleCategory(Base):
    """Categories for puzzles (Network Security, Application Security, etc.)"""
    __tablename__ = 'puzzle_categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    icon_path = Column(String(255))
    
    # Relationships
    puzzles = relationship("Puzzle", back_populates="category")
    
    def __repr__(self):
        return f"<PuzzleCategory(name='{self.name}')>"


class Puzzle(Base):
    """Puzzle definitions"""
    __tablename__ = 'puzzles'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey('puzzle_categories.id'))
    difficulty = Column(String(20), nullable=False)  # easy, medium, hard
    max_attempts = Column(Integer, default=3)
    points = Column(Integer, default=100)
    time_limit = Column(Integer)  # in seconds, null means no limit
    locked = Column(Boolean, default=True)
    prerequisites = Column(String(255))  # comma-separated puzzle IDs
    learning_objective = Column(Text)
    
    # Relationships
    category = relationship("PuzzleCategory", back_populates="puzzles")
    hints = relationship("PuzzleHint", back_populates="puzzle", cascade="all, delete-orphan")
    attempts = relationship("PuzzleAttempt", back_populates="puzzle", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Puzzle(title='{self.title}', difficulty='{self.difficulty}')>"


class PuzzleHint(Base):
    """Hints for puzzles"""
    __tablename__ = 'puzzle_hints'
    
    id = Column(Integer, primary_key=True)
    puzzle_id = Column(Integer, ForeignKey('puzzles.id'))
    hint_text = Column(Text, nullable=False)
    point_deduction = Column(Integer, default=10)
    order = Column(Integer, default=1)  # sequence order of hints
    
    # Relationships
    puzzle = relationship("Puzzle", back_populates="hints")
    
    def __repr__(self):
        return f"<PuzzleHint(puzzle_id={self.puzzle_id}, order={self.order})>"


class PuzzleAttempt(Base):
    """Records of user attempts at puzzles"""
    __tablename__ = 'puzzle_attempts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    puzzle_id = Column(Integer, ForeignKey('puzzles.id'))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    completed = Column(Boolean, default=False)
    successful = Column(Boolean, default=False)
    points_earned = Column(Integer, default=0)
    hints_used = Column(Integer, default=0)
    attempt_number = Column(Integer, default=1)
    
    # Relationships
    user = relationship("User", back_populates="attempts")
    puzzle = relationship("Puzzle", back_populates="attempts")
    
    def __repr__(self):
        return f"<PuzzleAttempt(user_id={self.user_id}, puzzle_id={self.puzzle_id}, successful={self.successful})>"


class Achievement(Base):
    """Achievement definitions"""
    __tablename__ = 'achievements'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    badge_image = Column(String(255))
    requirement = Column(Text, nullable=False)  # JSON or text describing achievement conditions
    points = Column(Integer, default=0)
    
    # Relationships
    users = relationship("UserAchievement", back_populates="achievement")
    
    def __repr__(self):
        return f"<Achievement(name='{self.name}')>"


class UserAchievement(Base):
    """Achievements earned by users"""
    __tablename__ = 'user_achievements'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    achievement_id = Column(Integer, ForeignKey('achievements.id'))
    earned_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="users")
    
    def __repr__(self):
        return f"<UserAchievement(user_id={self.user_id}, achievement_id={self.achievement_id})>"


class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, db_path=None):
        """Initialize database connection"""
        if db_path is None:
            # Create data directory if it doesn't exist
            data_dir = Path('data')
            data_dir.mkdir(exist_ok=True)
            db_path = data_dir / 'cybersecurity_escape_room.db'
            
        self.db_path = str(db_path)
        self.engine = create_engine(f'sqlite:///{self.db_path}')
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        logger.info(f"Database initialized at {self.db_path}")
    
    def init_db(self):
        """Create all tables if they don't exist"""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Database tables created successfully")
            
            # Initialize with default data if needed
            self._create_default_data()
        except Exception as e:
            logger.error(f"Error initializing database: {e}", exc_info=True)
            raise
    
    def _create_default_data(self):
        """Populate database with default data if tables are empty"""
        session = self.Session()
        try:
            # Check if categories exist
            if session.query(PuzzleCategory).count() == 0:
                logger.info("Creating default puzzle categories")
                categories = [
                    PuzzleCategory(name="Network Security", description="Puzzles related to network protocols, firewalls, and traffic analysis", icon_path="assets/images/network_icon.png"),
                    PuzzleCategory(name="Application Security", description="Puzzles related to secure coding, vulnerability detection, and web security", icon_path="assets/images/app_icon.png"),
                    PuzzleCategory(name="Cryptography", description="Puzzles involving encryption, hashing, and secure communication", icon_path="assets/images/crypto_icon.png"),
                    PuzzleCategory(name="Social Engineering", description="Puzzles related to psychological manipulation and social hacking", icon_path="assets/images/social_icon.png"),
                    PuzzleCategory(name="System Security", description="Puzzles focusing on operating systems and infrastructure security", icon_path="assets/images/system_icon.png")
                ]
                session.add_all(categories)
            
            # Check if achievements exist
            if session.query(Achievement).count() == 0:
                logger.info("Creating default achievements")
                achievements = [
                    Achievement(name="First Steps", description="Complete the tutorial", badge_image="assets/images/badges/tutorial.png", requirement="tutorial_completed", points=10),
                    Achievement(name="Cryptography Novice", description="Complete 3 cryptography puzzles", badge_image="assets/images/badges/crypto_novice.png", requirement="category:Cryptography:3", points=25),
                    Achievement(name="Network Defender", description="Complete 5 network security puzzles", badge_image="assets/images/badges/network_defender.png", requirement="category:Network Security:5", points=50),
                    Achievement(name="Perfect Score", description="Complete a puzzle without using hints", badge_image="assets/images/badges/perfect.png", requirement="no_hints:1", points=15),
                    Achievement(name="Speed Hacker", description="Complete a puzzle in under 60 seconds", badge_image="assets/images/badges/speed.png", requirement="time:60", points=20)
                ]
                session.add_all(achievements)
            
            # Commit changes
            session.commit()
            logger.info("Default data created successfully")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating default data: {e}", exc_info=True)
        finally:
            session.close()
    
    def get_session(self):
        """Get a database session"""
        return self.Session()
    
    def close(self):
        """Close all sessions"""
        self.Session.remove()
        logger.info("Database sessions closed") 