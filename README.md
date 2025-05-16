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


## Description of Modules

### AI
> Holds the code for the DecisionTreeClassifier implementation.

- Implemented as a class
- Generates the tree
- Recomends the next most efficient question
- Has a few additional functions for parsing


### Character
> A simple module for importing each json object as a python object

- Lists the traits of each character
- exports as a json object
- exports character portrait filename

### Data
> Holds the character portraits and all the character json objects


### Game
> Holds a few simple functions for handling the game


### GUI
> Most of the codebase. Holds all GUI generation and the logic / rules for the game.

- GUI initalization
- Handles 3 modes of play (Bot only, Human only, Human vs Bot)
- Shows the portrait of each character as a button
- Handles yes / no responses
- Passes on question to DecisionTreeClassifier 
- Winner / looser  logic

Have fun playing Guess Who AI! 🎉🧑‍💻