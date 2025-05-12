#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Authentication module for Cybersecurity Escape Room
Handles user registration, login, and password management
"""

import logging
import re
import bcrypt
from datetime import datetime

from src.database.db_manager import User, UserProfile

logger = logging.getLogger(__name__)


class AuthManager:
    """Manages user authentication operations"""
    
    def __init__(self, db_manager):
        """Initialize with database manager"""
        self.db_manager = db_manager
    
    def register_user(self, username, email, password, display_name=None):
        """
        Register a new user
        
        Args:
            username (str): Unique username
            email (str): User's email address
            password (str): User's password
            display_name (str, optional): User's display name
            
        Returns:
            tuple: (success (bool), message (str))
        """
        session = self.db_manager.get_session()
        try:
            # Validate inputs
            if not self._validate_username(username):
                return False, "Username must be 3-50 characters and contain only letters, numbers, and underscores"
                
            if not self._validate_email(email):
                return False, "Invalid email format"
                
            if not self._validate_password(password):
                return False, "Password must be at least 8 characters with at least one uppercase letter, one lowercase letter, and one number"
            
            # Check if username or email already exists
            existing_user = session.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                if existing_user.username == username:
                    return False, "Username already exists"
                else:
                    return False, "Email already exists"
            
            # Hash password
            password_hash = self._hash_password(password)
            
            # Create new user
            new_user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                created_at=datetime.utcnow()
            )
            session.add(new_user)
            session.flush()  # To get the ID
            
            # Create user profile
            profile = UserProfile(
                user_id=new_user.id,
                display_name=display_name if display_name else username,
                total_points=0,
                current_streak=0,
                highest_streak=0,
                tutorial_completed=False
            )
            session.add(profile)
            
            session.commit()
            logger.info(f"New user registered: {username}")
            return True, "Registration successful"
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error registering user: {e}", exc_info=True)
            return False, "An error occurred during registration"
        finally:
            session.close()
    
    def login_user(self, username_or_email, password):
        """
        Authenticate a user
        
        Args:
            username_or_email (str): Username or email
            password (str): User's password
            
        Returns:
            tuple: (success (bool), user_id or message (str))
        """
        session = self.db_manager.get_session()
        try:
            # Find user by username or email
            user = session.query(User).filter(
                (User.username == username_or_email) | (User.email == username_or_email)
            ).first()
            
            if not user:
                return False, "Invalid username or email"
            
            # Check password
            if not self._verify_password(password, user.password_hash):
                return False, "Invalid password"
            
            # Update last login
            user.last_login = datetime.utcnow()
            session.commit()
            
            logger.info(f"User logged in: {user.username}")
            return True, user.id
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error during login: {e}", exc_info=True)
            return False, "An error occurred during login"
        finally:
            session.close()
    
    def change_password(self, user_id, current_password, new_password):
        """
        Change a user's password
        
        Args:
            user_id (int): User ID
            current_password (str): Current password
            new_password (str): New password
            
        Returns:
            tuple: (success (bool), message (str))
        """
        session = self.db_manager.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            
            if not user:
                return False, "User not found"
            
            # Verify current password
            if not self._verify_password(current_password, user.password_hash):
                return False, "Current password is incorrect"
            
            # Validate new password
            if not self._validate_password(new_password):
                return False, "New password must be at least 8 characters with at least one uppercase letter, one lowercase letter, and one number"
            
            # Hash and update new password
            user.password_hash = self._hash_password(new_password)
            session.commit()
            
            logger.info(f"Password changed for user: {user.username}")
            return True, "Password changed successfully"
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error changing password: {e}", exc_info=True)
            return False, "An error occurred while changing the password"
        finally:
            session.close()
    
    def get_user(self, user_id):
        """
        Get user information
        
        Args:
            user_id (int): User ID
            
        Returns:
            User: User object if found, None otherwise
        """
        session = self.db_manager.get_session()
        try:
            return session.query(User).filter(User.id == user_id).first()
        finally:
            session.close()
    
    def _validate_username(self, username):
        """Validate username format"""
        # 3-50 characters, alphanumeric and underscores
        return bool(re.match(r'^[a-zA-Z0-9_]{3,50}$', username))
    
    def _validate_email(self, email):
        """Validate email format"""
        # Simple email validation
        return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))
    
    def _validate_password(self, password):
        """Validate password strength"""
        # At least 8 characters with at least one uppercase, one lowercase, and one number
        return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', password))
    
    def _hash_password(self, password):
        """Hash a password using bcrypt"""
        # Convert to bytes if it's a string
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        # Generate salt and hash
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        
        return hashed.decode('utf-8')
    
    def _verify_password(self, password, stored_hash):
        """Verify a password against a stored hash"""
        # Convert to bytes if they're strings
        if isinstance(password, str):
            password = password.encode('utf-8')
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode('utf-8')
        
        return bcrypt.checkpw(password, stored_hash) 