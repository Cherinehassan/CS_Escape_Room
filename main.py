#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main entry point for Cybersecurity Escape Room
"""

import sys
from PyQt6.QtWidgets import QApplication
from src.app_integration import CyberEscapeRoomApp

def main():
    """Start the application"""
    app = QApplication(sys.argv)
    window = CyberEscapeRoomApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 