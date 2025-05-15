# main.py
from gui.gui_main import GuessWhoGUI
import tkinter as tk
import argparse

parser = argparse.ArgumentParser(prog='GuessWhoAI',description='Play a game Guess Who where you can play against a bot!')
parser.add_argument('--tree', action='store_true')
args = parser.parse_args()
tree = args.tree

if __name__ == "__main__":
    root = tk.Tk()
    app = GuessWhoGUI(root, tree)
    root.mainloop()
