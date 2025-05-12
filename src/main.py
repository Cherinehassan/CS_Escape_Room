#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cybersecurity Escape Room - An educational game teaching cybersecurity concepts
Main entry point for the application
"""

import os
import sys
import logging
from PyQt6.QtWidgets import QApplication
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import application components
from src.gui.app import CybersecurityEscapeRoom
from src.database.db_manager import DatabaseManager
from src.core.puzzle_manager import PuzzleManager


def main():
    """Main entry point for the application"""
    try:
        # Initialize the database
        db_manager = DatabaseManager()
        db_manager.init_db()
        
        # Initialize the puzzle manager
        puzzle_manager = PuzzleManager()
        
        # Start the GUI application
        app = QApplication(sys.argv)
        app.setApplicationName("Cybersecurity Escape Room")
        window = CybersecurityEscapeRoom(db_manager, puzzle_manager)
        window.show()
        
        # Run the application
        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"Application failed to start: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main() 