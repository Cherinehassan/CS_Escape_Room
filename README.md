# Cybersecurity Escape Room

An educational game that teaches cybersecurity concepts through interactive puzzles and challenges in an immersive escape room experience.

## Overview

The Cybersecurity Escape Room is a PyQt6-based educational game designed to teach cybersecurity concepts in an engaging way. Players must solve puzzles across various cybersecurity domains to progress through the virtual escape room.

## Features

- **Interactive Puzzles**: 15+ cybersecurity challenges across different categories
- **Educational Content**: Each puzzle teaches specific cybersecurity concepts
- **Progress Tracking**: Track completion rates and achievements
- **Rich User Interface**: Immersive design with animations and sound effects
- **Multiple Difficulty Levels**: Challenges for beginners to advanced users

## Categories

The game includes puzzles in these cybersecurity domains:

- **Cryptography**: Encryption and decryption challenges
- **Social Engineering**: Identifying phishing and manipulation tactics
- **Hashing**: Understanding hash functions and their applications
- **Authentication**: Password security and multi-factor authentication
- **Encryption**: Public/private key encryption concepts

## Technical Details

### Technologies Used

- **Python**: Core programming language
- **PyQt6**: GUI framework
- **JSON**: Puzzle data storage
- **Animation Framework**: Custom effects for immersive experience
- **Sound System**: Audio feedback and ambience

### Components

- **Puzzle Manager**: Loads and manages puzzles from JSON
- **Animation Effects**: Provides visual feedback and transitions
- **Sound System**: Manages audio effects and background sounds
- **Theme Manager**: Handles application styling and themes
- **User Data**: Tracks progress and achievements

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/cybersecurity-escape-room.git
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python main.py
   ```

## Project Structure

```
.
├── main.py                      # Application entry point
├── app.py                       # Main application logic
├── requirements.txt             # Python dependencies
├── resources/                   # Resource files
│   ├── sounds/                  # Sound effects
│   └── images/                  # Images and icons
├── data/                        # Data files
│   └── puzzles.json             # Puzzle definitions
└── src/                         # Source code
    ├── core/                    # Core logic
    │   └── puzzle_manager.py    # Puzzle management
    └── gui/                     # GUI components
        ├── screens/             # Application screens
        │   ├── menu_screen.py
        │   ├── puzzle_screen.py
        │   ├── dashboard_screen.py
        │   └── ...
        └── utils/               # GUI utilities
            ├── animation_effects.py
            ├── sound_effects.py
            ├── theme_manager.py
            └── ...
```

## Usage

1. Start the application
2. Create a user account or log in
3. Select puzzles from the menu or dashboard
4. Solve puzzles to progress through the escape room
5. Track your progress in the dashboard

## License

[MIT License](LICENSE)

## Acknowledgements

- Icons by [Font Awesome](https://fontawesome.com/)
- Sound effects from [FreeSound](https://freesound.org/) 