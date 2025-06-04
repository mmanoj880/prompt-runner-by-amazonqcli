# Prompt Runner Game By AmazonQCLI

A 2D endless runner game built with Python and Pygame where the player collects "good prompts" and avoids "bad prompts".

## Game Features

- Player character that can jump to collect or avoid prompts
- Green "good prompts" that increase your score
- Red "bad prompts" that end the game
- Increasing difficulty as the game progresses
- Score tracking
- Visual effects (particles, animations)
- Sound effects (if sound files are available)

## How to Play

1. Run the game using `python main.py` or `python enhanced_game.py`
2. Press ENTER to start the game
3. Use SPACE to jump
4. Collect green prompts to increase your score
5. Avoid red prompts
6. Press ESC to quit

## Controls

- SPACE: Jump
- ENTER: Start game / Restart after game over
- ESC: Quit game

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Make sure you have Python installed
2. Install Pygame: `pip install pygame`
3. Run the game: `python main.py` or `python enhanced_game.py`

## Game Versions

- `main.py`: Basic version of the game with core functionality
- `enhanced_game.py`: Enhanced version with improved graphics, animations, and effects

## Adding Sound Effects

To add sound effects to the game, place the following WAV files in the `sounds` directory:

- `jump.wav`: Played when the player jumps
- `good_collect.wav`: Played when collecting a good prompt
- `bad_collect.wav`: Played when hitting a bad prompt
- `game_over.wav`: Played when the game ends

## Customization

You can customize various aspects of the game by modifying the constants at the top of the game files:

- Screen dimensions
- Game physics (gravity, jump force)
- Prompt spawn rate and speed
- Colors
- Game speed increase rate

## Credits

Created as a Python Pygame project for learning game development basics using AmazonQCLI
