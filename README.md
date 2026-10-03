
<div align="center">
   ![logo](<img width="2051" height="767" alt="logo" src="https://github.com/user-attachments/assets/fef71e7d-46d3-43d6-be31-4944e5b2a32d" />)
   
   # Rocky Rush
   
   **An Arcade Runner Game Built with Python**
   
   [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
   [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
   [![pygame](https://img.shields.io/badge/pygame-2.x-green.svg)](https://pygame.org/)
</div>

---

## 📋 Overview

**Rocky Rush** is a fast-paced arcade runner game inspired by the classic Chrome Dinosaur game. Navigate through a dynamic environment by jumping over cacti, ducking under flying pterosaurs, and collecting points. Built in 2022, this project demonstrates clean game development architecture using Python and pygame.

## 🎮 Features

- **Keyboard-driven gameplay** with intuitive controls
- **Animated sprites** - dinosaur, cactus, pterosaur, clouds, and ground
- **Progressive difficulty** - challenge increases as you progress
- **Audio feedback** - jump, checkpoint, and collision sound effects
- **Score tracking** - real-time scoring with persistent high-score display
- **Clean architecture** - well-structured Python package with console entry point

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.10+ |
| **Game Engine** | pygame 2.x |
| **Package Management** | pip |
| **Build System** | setuptools (via pyproject.toml) |
| **Project Type** | Python Package |

## 🎮 Controls

| Action | Key(s) |
|--------|--------|
| Jump | `Space` / `Up Arrow` |
| Duck | `Down Arrow` |
| Restart | `Enter` / `Space` (on game over) |
| Quit | `Esc` (on game over) |

## 🚀 Quick Start

### Installation & Setup

```bash
# Clone the repository
git clone https://github.com/KPROsoft21/rocky-rush.git
cd rocky-rush

# Create and activate virtual environment
python3.12 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### Alternative: Run as a Module

```bash
PYTHONPATH=src python -m rocky_rush
```

**Python Version Support:** 3.10–3.13 (recommended)
- Python 3.14 may require additional configuration for pygame audio/image modules on some systems

## 📁 Project Structure

```
rocky-rush/
├── src/
│   └── rocky_rush/          # Main game package
│       ├── __main__.py       # Module entry point
│       ├── game.py           # Core game logic
│       ├── sprites.py        # Game sprite definitions
│       ├── assets/           # Game assets (images, audio)
│       └── ...
├── main.py                   # Direct entry point
├── pyproject.toml            # Project metadata & dependencies
├── requirements.txt          # Runtime dependencies
└── README.md                 # This file
```

## 📦 Dependencies

- **pygame** - Cross-platform game development library
- Python 3.10+ standard library

See `requirements.txt` for pinned versions.

## 👤 About

**Rocky Rush** was developed in **2022** as a modern take on the classic browser-based runner game. The project emphasizes clean code architecture and maintainability while delivering engaging arcade gameplay.

This repository preserves the original author attribution while applying modern Python best practices and improved project structure for better code review and long-term maintenance.

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs via GitHub Issues
- Submit feature requests
- Open pull requests with improvements

## 🎯 Future Enhancements

Potential improvements for future versions:
- [ ] Mobile/touch controls
- [ ] Additional game modes
- [ ] Leaderboard system
- [ ] Power-ups and special items
- [ ] Enhanced visual effects

---

<div align="center">
   
   **Made with ❤️ using Python and pygame**
   
   [Report Bug](https://github.com/KPROsoft21/rocky-rush/issues) • [Request Feature](https://github.com/KPROsoft21/rocky-rush/issues)
   
</div>
