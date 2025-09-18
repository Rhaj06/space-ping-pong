<div align="center">
  <h1>🛰️ Space Ping Pong</h1>
  <p><i>An arcade-style, neon space-themed ping pong game built with Python & Pygame</i></p>

  <!-- Gameplay preview (ensure the filename below matches your gifs folder) -->
  <img src="gifs/SpacePingPongDemo.gif" alt="Space Ping Pong gameplay" width="700">
</div>

<br>

<div align="center">
  <!-- Update the repo path in the href and badge if your repo name differs -->
  <a href="https://github.com/brej-29/space-ping-pong">
    <img alt="Last Commit" src="https://img.shields.io/github/last-commit/brej-29/space-ping-pong">
  </a>
  <img alt="Python Language" src="https://img.shields.io/badge/Language-Python-blue">
  <img alt="Pygame" src="https://img.shields.io/badge/Library-Pygame-brightgreen">
  <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow">
  <img alt="OS" src="https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey">
</div>

<div align="center">
  <br>
  <b>Built with the tools and technologies:</b>
  <br><br>
  <code>Python</code> | <code>Pygame</code> | <code>dataclasses</code> | <code>Enum</code> | <code>JSON (local storage)</code> | <code>OOP</code>
</div>

---

## **Table of Contents**
* [Overview](#overview)
* [Features](#features)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Configuration](#configuration)
  * [Usage](#usage)
* [Project Structure](#project-structure)
* [Controls](#controls)
* [Difficulty & Power-ups](#difficulty--power-ups)
* [License](#license)
* [Contact](#contact)

---

## **Overview**

**Space Ping Pong** is a colorful, fast-paced desktop game. It features a starfield background, particle effects, power-ups, screen shake, a high-score table, and both **Single-player (vs Computer)** and **Local Two-player** modes. The animated menu lets you pick a mode, toggle difficulty (E/M/H), view high scores, and exit.

> The game stores high scores locally (JSON), so your top results persist between runs.

<br>

### **Project Highlights**
- **Two Modes:** Play vs Computer (AI) or Local Human vs Human.
- **Dynamic Feel:** Particle bursts, pulsing menu text, starfield, and subtle screen shake.
- **Power-ups:** Speed Boost, Paddle Grow/Shrink, Shield, Multi-Ball, and Freeze.
- **High Scores:** Auto-saved locally and shown in a dedicated screen.
- **Lightweight:** Only external dependency is `pygame`.

---

## **Features**
- Animated main menu with difficulty toggle (E/M/H).
- AI opponent with difficulty scaling.
- Local 2-player option (separate key bindings).
- Multiple power-ups with visual feedback.
- Particle effects for hits/scoring and a trailing ball effect.
- Persistent high scores (JSON file).
- Clean, modular Python code split across multiple files.

---

## **Getting Started**

Follow these steps to set up and run the project on your machine.

### **Prerequisites**
- **Python 3.8+**
- **pip** (Python package manager)

### **Installation**
1. **Clone the repository (or download the source code):**  
   ``` sh
   git clone https://github.com/brej-29/space-ping-pong.git
   cd <repo-name>
     ```

2. **Install dependencies:**
  ``` sh
  pip install -r requirements.txt
  ```

### Configuration
 This game runs out-of-the-box. Optional tweaks:
- **Window & FPS:** edit SCREEN_WIDTH, SCREEN_HEIGHT, and FPS in settings.py.
- **Default Difficulty:** in game.py (self.difficulty = Difficulty.MEDIUM), change to EASY or HARD.
- **High Scores file path:** adjust in storage.py if you want to store it somewhere else (e.g., a data/ folder).

### Usage
Run the game from the project root:
``` sh
python main.py
```
> If you’re using a virtual environment, activate it first (see above).

---

## Project Structure

``` bash
.
├─ LICENSE
├─ README.md
├─ requirements.txt
├─ gifs/
│  └─ space-ping-pong.gif        # gameplay preview (update name if different)
├─ main.py                       # entrypoint (runs the game)
├─ game.py                       # Game loop, states, drawing, event handling
├─ settings.py                   # screen size, FPS, colors, etc.
├─ enums.py                      # GameState, Difficulty, PowerUpType
├─ vector.py                     # lightweight Vector2D
├─ ball.py                       # Ball entity, physics & trail
├─ paddle.py                     # Paddle entity, player/AI logic & effects
├─ particles.py                  # Particle & Star classes
├─ powerups.py                   # PowerUp entity & visuals
└─ storage.py                    # load/save high scores (JSON)

```

---

## **Controls**

**Menu**
- `1` → Play vs Computer  
- `2` → Play vs Human  
- `3` → High Scores  
- `E / M / H` → Change difficulty  
- `ESC` → Quit

**Gameplay**
- **Player 1 (Right):** Arrow `↑` / `↓`  
- **Player 2 (Left, only in Human vs Human):** `W` / `S`  
- `SPACE` → Pause / Resume

---

## **Difficulty & Power-ups**

- **Difficulty**
  - The AI paddle behavior changes based on `Difficulty` (EASY / MEDIUM / HARD).  
  - You can toggle it from the menu using `E`, `M`, or `H`.  
  - To change the default, set `self.difficulty` in `game.py`.

- **Power-ups**
  - **Speed Boost** – temporarily increases ball speed.  
  - **Paddle Grow / Shrink** – temporarily changes paddle size.  
  - **Shield** – gives a paddle a one-time protective barrier.  
  - **Multi-Ball** – spawns an additional ball.  
  - **Freeze** – briefly pauses ball/paddle updates.
  
> Power-ups spawn periodically and are collected when the ball collides with them. Particle bursts and highlights indicate pickups.

---

## **License**
This project is licensed under the **MIT License**. See the [`LICENSE`](LICENSE) file for details.

---

## **Contact**
Questions or feedback or want to collaborate? Reach out via my  
**LinkedIn:** [Brejesh Balakrishnan](https://www.linkedin.com/in/brejesh-balakrishnan-7855051b9/)
