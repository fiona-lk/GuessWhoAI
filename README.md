# 🕵️‍♂️ Guess Who AI 🎲

A Python implementation of the classic "Guess Who?" board game, powered by an AI opponent using a decision tree. Play against the AI, let the AI guess your character, or play a two-sided game where both you and the AI ask questions!

## ✨ Features

- 🤖 **AI Opponent:** Uses a decision tree to ask strategic questions and guess your character.
- 🎮 **Multiple Game Modes:** 
  - 🧑‍💼 AI guesses your character
  - 🕵️ You guess the AI's character
  - 🔄 Two-sided mode (take turns asking questions)
- 🖼️ **Graphical Interface:** Built with Tkinter and PIL for an interactive experience.
- 🧑‍🎨 **Custom Characters:** Easily add or modify characters in `data/characters.json`.

## 🚀 Getting Started

### 🛠️ Prerequisites

- 🐍 Python 3.7+
- 📦 Required packages: `scikit-learn`, `Pillow`, `tkinter`

Install dependencies:
```bash
pip3 install scikit-learn pillow
```

### ▶️ Running the Game

```bash
python3 main.py
```

#### 📝 Arguments

`--tree`: prints out the calculated decision tree into the terminal window.

---

Have fun playing Guess Who AI! 🎉🧑‍💻