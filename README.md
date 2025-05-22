# Queens-Game
Created a game using Amaon Q CLI 
Your goal is to place exactly **one Queen** in each **row, column, and color region** without any of them attacking each other — not even diagonally.

## 🛠 Built With

- [Amazon Q Developer CLI](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-cli.html)
-  Python 3.8+
-  Pygame
-  Custom region-based color logic

---

## 📦 Prerequisites

- Python 3.8 or above
- pip (Python package manager)
- Linux system (for AppImage installation method)
- Git (optional, for cloning)

---

## 🚀 How to Install Amazon Q CLI (Linux)

1. **Download** the AppImage from [Amazon Q CLI](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-cli.html)

2. **Make it executable**:
   ```bash
   chmod +x amazon-q.appimage
3. Run the CLI:
    ./amazon-q.appimage
4. Install Python dependencies:
    pip install pygame
5. Run the Game
    python queens_game.py


## Steps to play Game: 

Your goal is to have exactly one  in each row, column, and color region.
Tap once to place X and tap twice for  . Use X to mark where  cannot be placed.
Two  cannot touch each other, not even diagonally.
Examples:
Each row can only have one Queen.
Each row can only have one  .
Each column can also only have one Queen.
Each column can also only have one  .
Each color region can also only have one Queen.
Each color region can also only have one  .
Two Queen cannot touch each other, not even diagonally.
Two  cannot touch each other, not even diagonally.
