
<div align="center">
   <img width="87" height="93" alt="Pixel Green Dinosaur Logo" src="https://github.com/user-attachments/assets/a89f4cc5-0360-4511-bfa1-02d796dcd768" />
  
  # Rocky Rush
</div>

Rocky Rush (2022) is a small arcade runner built with Python and pygame. It is inspired by the classic Chrome Dino game: jump over cacti, duck under flying obstacles, and chase a higher score as the game speeds up.

## Features

- Keyboard-driven runner gameplay
- Animated dinosaur, cactus, ptera, cloud, and ground sprites
- Score and high-score display
- Jump, checkpoint, and collision sound effects
- Clean Python package layout with a console entry point

## Gameplay

- `Space` or `Up Arrow`: jump
- `Down Arrow`: duck
- `Enter` or `Space`: restart after game over
- `Esc`: quit from the game-over screen

## Quick Start

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

You can also run it as a module:

```bash
PYTHONPATH=src python -m rocky_rush
```

Python 3.10 through 3.13 is recommended. Python 3.14 can currently build pygame without optional image/audio modules on some systems.

## Project Structure

```text
.
├── src/rocky_rush/       # Game package and bundled assets
├── main.py               # Simple local entry point
├── pyproject.toml        # Package metadata
└── requirements.txt      # Runtime dependency
```

## Notes

This repository preserves the original author attribution from the source code while modernizing the project structure and Python style for easier review and maintenance.
