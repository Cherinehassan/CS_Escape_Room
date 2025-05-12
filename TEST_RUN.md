# Test Run Instructions

This document explains how to test run the Cybersecurity Escape Room application.

## Prerequisites

- Python 3.6+
- PyQt6 (can be installed via pip)

## Running the Application

1. Clone or download the repository
2. Install the required packages:
   ```
   pip install PyQt6
   ```
3. Run the application:
   ```
   python main.py
   ```

## Expected Behavior

When running the application, a window should appear with the "Cybersecurity Escape Room Dashboard" screen showing:

- Stats section at the top with time played, fastest solve, etc.
- Category progress section showing puzzle categories
- Achievements section showing locked/unlocked achievements
- Available challenges section at the bottom

The application includes:
- Animated flickering title
- Cyber-themed styling
- Sample puzzle data

## Troubleshooting

### Missing Sound Files Warning

You may see a warning like:
```
qt.multimedia.ffmpeg: Using Qt multimedia with FFmpeg version 7.1 LGPL version 2.1 or later
qt.multimedia.ffmpeg.mediadataholder: Could not open media. FFmpeg error description: "No such file or directory"
```

This is expected as the application looks for sound files that aren't included in this test setup. The application will run normally despite this warning.

### Import Errors

If you see import errors, make sure all files are in the correct directory structure:

```
.
├── main.py
├── data/
│   └── puzzles.json (will be created automatically)
├── resources/
│   └── sounds/
└── src/
    ├── __init__.py
    ├── app_integration.py
    ├── core/
    │   ├── __init__.py
    │   ├── puzzle_manager.py
    │   └── user_data.py
    └── gui/
        ├── __init__.py
        ├── screens/
        │   ├── __init__.py
        │   └── dashboard_screen.py
        └── utils/
            ├── __init__.py
            ├── animation_effects.py
            ├── screen_manager.py
            ├── sound_effects.py
            └── theme_manager.py
```

## Next Steps

To enhance this test application:
1. Add sound files to the `resources/sounds/` directory
2. Implement additional screens (menu, puzzle screen, etc.)
3. Connect the dashboard to actual puzzle screens
4. Add more visual effects and animations 