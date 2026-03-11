# Hangman Game 🎮

A modern, interactive Hangman game built with **Streamlit** and Python.

## Features

✨ **Gameplay**
- 3 difficulty levels (Easy, Medium, Hard)
- 6+ categories (Animals, Space, Programming, Food, Technology)
- Progressive hint system (free → costs attempts)
- Timer mode on Medium/Hard
- Streak tracking & scoring system

🎯 **UI/UX**
- Dark theme with cyan accent colors
- Animated hangman SVG drawing
- Interactive keyboard with letter states
- Visual progress bar for attempts
- Confetti animation on win
- Responsive design (mobile-friendly)

📊 **Game Features**
- Smart word filtering by difficulty & length
- Anti-repeat word system (no duplicates until all words used)
- Score = base + streak bonus + remaining attempts - hints cost
- Category & difficulty selectors
- Real-time hint reveal with cost display

## Installation

```bash
git clone https://github.com/yourusername/hangman-game.git
cd hangman-game
pip install -r requirements.txt
```

## Running the Game

```bash
streamlit run src/app.py
```

Then open `http://localhost:8501` in your browser.

## How to Play

1. **Select Difficulty** (Easy/Medium/Hard) → affects word length & attempts
2. **Pick Category** (All/Animals/Space/etc.)
3. **Guess letters** by clicking keyboard buttons
4. **Reveal hints** (costs attempts) to get clues
5. **Win** by completing the word before running out of attempts
6. Build your **streak** and maximize your **score**

## Difficulty Settings

| Difficulty | Attempts | Time Limit | Word Length | Base Score |
|-----------|----------|-----------|------------|-----------|
| Easy      | 8        | ∞         | 3-5 letters| 80 pts   |
| Medium    | 6        | 60 sec    | 5-7 letters| 120 pts  |
| Hard      | 5        | 40 sec    | 7+ letters | 170 pts  |

## Scoring System

```
Score = base_score + (streak × 20) + (remaining_attempts × 12) - (hints_used × 10)
```

## File Structure

```
hangman-game/
├── src/
│   ├── app.py              # Main Streamlit UI
│   └── hangman_logic.py    # Game logic & word bank
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Technology Stack

- **Frontend**: Streamlit 1.28.0
- **Language**: Python 3.11+
- **Data**: In-memory word bank (can be extended with APIs)

## Future Enhancements

- 🌙 Dark/Light mode toggle
- 🏆 Local leaderboard (JSON-based)
- 🔊 Sound effects
- 🎖️ Achievement badges
- 👥 Multiplayer mode
- 📡 Word API integration

## Author

Divyansh Mathur

## License

MIT License
