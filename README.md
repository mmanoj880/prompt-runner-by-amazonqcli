# 🕹️ Prompt Runner Game By AmazonQCLI

**Prompt Runner** is a 2D endless runner game built using **Python**, **Pygame**, and **Amazon Q CLI**. In this game, you collect *good prompts* and avoid *bad prompts* to earn a high score. The project blends classic game mechanics with GenAI tooling, making it a fun and educational coding experiment.

---

## 🤖 Built with Amazon Q CLI

This game was developed using **Amazon Q CLI** as an AI-powered coding assistant. It was instrumental in:

- Generating reusable game logic (player movement, collisions, etc.)
- Debugging runtime issues and optimizing performance
- Refactoring code into modular components
- Accelerating game development by suggesting features and fixes

Example Amazon Q CLI prompt:
```bash
q ask "How do I implement gravity-based jump in Pygame?"
````

---

## 🧩 Game Features

### 🎮 Player Character

* Jumping using the **spacebar**
* Running and jumping animations
* Collision detection

### ✉️ Prompt System

* **Good prompts** (green): Increase score
* **Bad prompts** (red): End the game
* Animated with rotation and pulsing
* Random spawn locations and fall speeds

### ⚙️ Mechanics

* Score tracker
* Increasing difficulty (faster fall speed over time)
* Jump physics (gravity, velocity)
* Start and Game Over screens

### 🎨 Visual Effects

* Scrolling animated backgrounds (clouds, grass)
* Particle effects when collecting prompts
* Clean and colorful UI

---

## 📁 Project Structure

* `main.py`: Basic version with essential features
* `enhanced_game.py`: Advanced version with sounds, effects, and polished gameplay

---

## ▶️ How to Run the Game

### 1. Install Dependencies

```bash
pip install pygame
```

### 2. Run the Game

```bash
python prompt_runner/main.py
# or
python prompt_runner/enhanced_game.py
```

---

## 🎮 Controls

| Key   | Action               |
| ----- | -------------------- |
| SPACE | Jump                 |
| ENTER | Start / Restart Game |
| ESC   | Quit Game            |

---

## 🔊 Optional Sound Effects

Add `.wav` files to a `sounds/` folder to enable sound support in the enhanced version:

* `jump.wav`
* `good_collect.wav`
* `bad_collect.wav`
* `game_over.wav`

---

## ⚙️ Customization

You can easily tweak these values in the script:

* `SCREEN_WIDTH`, `SCREEN_HEIGHT`
* `GRAVITY`, `JUMP_FORCE`
* `SPAWN_RATE`, `FALL_SPEED`
* `SPEED_INCREASE_RATE`
* Prompt colors and effects

---

## 🚀 Ideas for Expansion

* Use Amazon Q CLI to **evaluate collected prompts live**
* Add online leaderboard with Flask or Django
* Add a prompt suggestion system powered by GenAI
* Multiplayer support with sockets

---

## 📢 About Amazon Q CLI

Amazon Q CLI is a GenAI tool that helps developers:

* Ask coding questions from the command line
* Generate and refactor code
* Get real-time help on bugs and features

This game is a real-world showcase of what you can build with **AI + Python**.

---

## 📸 Screenshots and Videos

> ![image](https://github.com/user-attachments/assets/43d6ad57-b3ef-4d73-95c1-5ed1c3864f1c)


## 📄 License

MIT License. See `LICENSE` file for details.

---

Happy Coding! 🎉
Built with ❤️ using Python, Pygame & Amazon Q CLI

```
