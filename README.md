# Chess Bot ♟️

A Python-based **chess automation bot** that reads the board, calculates the best move using Stockfish, and moves your mouse to perform the move. Designed for personal practice and offline play.

> **Note:** Do not use this bot to cheat in online multiplayer games.

---

## Features

- Detects and reads the current chess board from the screen.  
- Uses Stockfish engine to calculate the optimal move.  
- Automates mouse movement to perform the move.  
- Works with both desktop applications and web-based chess platforms.  

---

## How It Works

1. **Board Detection**  
   The bot captures a screenshot of the chess board and analyzes the positions using computer vision.

2. **Move Calculation**  
   Stockfish evaluates the board and determines the best move to make.

3. **Move Execution**  
   The bot controls your mouse to move the pieces on the board automatically.

4. **Repeat**  
   Steps 1–3 repeat for each turn until the game ends.

---

## Tech Stack

- **Python 3** – Core logic and automation scripts.  
- **Stockfish** – Chess engine for move calculation.  
- **OpenCV** – Screen capture and board recognition.  
- **PyAutoGUI** – Mouse automation.  
- **NumPy** – Data handling for board analysis.  

---

## Installation

1. Clone the repository:  
```bash
git clone https://github.com/Shaan50/chess-bot.git
cd chess-bot
pip install -r requirements.txt
```
Download Stockfish:

Visit Stockfish Download

Download the correct version for your OS

Place the executable inside a stockfish folder in the project root

Update the Stockfish path in chess_bot.py:
import os
from stockfish import Stockfish

base_dir = os.path.dirname(__file__)
stockfish_path = os.path.join(base_dir, "stockfish", "stockfish_15_x64_avx2.exe")
stockfish = Stockfish(stockfish_path)

Run the bot:
python chess_bot.py

## Folder Structure

chess-bot/
│
├─ chess_bot.py # Main bot script
├─ stockfish/ # Folder containing Stockfish executable
├─ requirements.txt # Python dependencies
└─ README.md # Project documentation

## License

This project is open-source and available under the MIT License.

## Author

Shaan Cheruvu
https://github.com/Shaan50
