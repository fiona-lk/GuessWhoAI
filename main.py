# main.py
from gui.gui_main import GuessWhoGUI
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = GuessWhoGUI(root)
    root.mainloop()
