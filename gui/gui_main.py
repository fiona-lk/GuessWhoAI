import tkinter as tk
from PIL import Image, ImageTk
import random

from character.character_loader import load_characters
from ai.decision_tree_ai import DecisionTreeAI
from game.game_engine import GameEngine

class GuessWhoGUI:
    MODE_AI_GUESSES = "ai_guesses"
    MODE_PLAYER_GUESSES = "player_guesses"
    MODE_TWOSIDED = "twosided"

    def __init__(self, root):
        self.root = root
        self.root.title("Guess Who AI")

        self.characters = load_characters("data/characters.json")
        self.ai = DecisionTreeAI(self.characters)
        self.engine = GameEngine(self.characters, self.ai)
        self.remaining_characters = self.characters.copy()
        self.player_character = None
        self.ai_secret_character = None

        self.images = {}
        self.button_map = {}

        self.mode = tk.StringVar(value=self.MODE_TWOSIDED)

        self.create_widgets()
            
    def create_widgets(self):
        # --- Mode Selection ---
        self.mode_frame = tk.LabelFrame(self.root, text="Game Mode")
        self.mode_frame.pack(pady=5)

        tk.Radiobutton(self.mode_frame, text="AI guesses your character", variable=self.mode, value=self.MODE_AI_GUESSES).pack(anchor="w")
        tk.Radiobutton(self.mode_frame, text="You guess AI's character", variable=self.mode, value=self.MODE_PLAYER_GUESSES).pack(anchor="w")
        tk.Radiobutton(self.mode_frame, text="Two-sided", variable=self.mode, value=self.MODE_TWOSIDED).pack(anchor="w")

        # --- Character Selection Grid ---
        self.char_frame = tk.LabelFrame(self.root, text="Choose Your Character")
        self.char_frame.pack(padx=10, pady=10, fill="both", expand=True)

        columns = 6
        for idx, character in enumerate(self.characters):
            photo = self.load_image(character.filename)
            self.images[character.name] = photo  # prevent garbage collection

            btn = tk.Button(
                self.char_frame,
                text=character.name,
                image=photo if photo else None,
                compound="top",
                command=lambda c=character: self.handle_player_select(c)
            )
            row = idx // columns
            col = idx % columns
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.button_map[character.name] = btn


        # --- Guess Button ---
        self.guess_button = tk.Button(self.root, text="Guess AI's Character", command=self.show_guess_menu, state="disabled")
        self.guess_button.pack(pady=5)
        # --- Question / Resposne Label ---
        self.answer_label = tk.Label(self.root, text="")
        self.answer_label.pack(pady=10)
        
        self.question_label = tk.Label(self.root, text="Select your character to begin.")
        self.question_label.pack(pady=10)
        

        # --- Response Buttons (for AI guessing mode only) ---
        self.response_frame = tk.Frame(self.root)
        self.response_frame.pack(pady=10)

        self.yes_button = tk.Button(self.response_frame, text="Yes", width=10, command=lambda: self.handle_response(True), state="disabled")
        self.no_button = tk.Button(self.response_frame, text="No", width=10, command=lambda: self.handle_response(False), state="disabled")
        self.yes_button.pack(side="left", padx=5)
        self.no_button.pack(side="left", padx=5)

        # --- Scrollable Frame for Player Trait Questions ---
        canvas = tk.Canvas(self.root, height=120)
        scrollbar = tk.Scrollbar(self.root, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand=scrollbar.set)

        scrollbar.pack(fill="x")
        canvas.pack(fill="x")

        self.player_question_frame = tk.Frame(canvas)
        self.player_question_canvas = canvas
        canvas.create_window((0, 0), window=self.player_question_frame, anchor="nw")

        # Bind resizing
        self.player_question_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))



    def load_image(self, filename):
        try:
            path = f"data/images/{filename}"
            img = Image.open(path).resize((80, 80))
            photo = ImageTk.PhotoImage(img)
            return photo
        except Exception as e:
            print(f"Image load failed for {filename}: {e}")
            return None


    def handle_player_select(self, character):
        self.player_character = character
        

        for name, btn in self.button_map.items():
            btn.config(command=lambda: None)


        # Disable game mode switching
        for child in self.mode_frame.winfo_children():
            child.config(state="disabled")

        selected_mode = self.mode.get()

        if selected_mode == self.MODE_AI_GUESSES:
            self.question_label.config(text=f"You selected: {character.name}. AI will try to guess it.")
            self.yes_button.config(state="normal")
            self.no_button.config(state="normal")
            self.ask_next_question()

        elif selected_mode == self.MODE_PLAYER_GUESSES:
            self.show_player_question_buttons()
            self.guess_button.config(state="normal")
            self.ai_secret_character = random.choice(self.characters)
            self.remaining_characters = self.characters.copy()
            self.question_label.config(text="You will try to guess the AI's secret character!")
            self.show_player_question_buttons()    
            # Player-asks-AI UI will go here soon

        elif selected_mode == self.MODE_TWOSIDED:
            self.guess_button.config(state="normal")
            self.ai_secret_character = random.choice(self.characters)
            self.remaining_characters = self.characters.copy()
            self.question_label.config(text="Ask a question...")
            self.show_player_question_buttons()

    def ask_next_question(self):
        question = self.ai.recommend_question(self.remaining_characters)
        if question:
            trait, value = question
            self.current_trait = trait
            self.current_value = value
            if value is True:
                self.question_label.config(text=f'Does your character have {trait}')
            elif value is False:
                self.question_label.config(text=f'Does your character not have {trait}')
            else:
                self.question_label.config(text=f"Does your character have {trait} = {value}?")
            self.yes_button.config(state="normal")
            self.no_button.config(state="normal")

        else:
            guess = self.ai.guess_character(self.remaining_characters)
            if guess == self.player_character.name:
                self.question_label.config(text=f"AI wins! It guessed your character: {guess} 🎯")
            elif guess is not None:
                self.question_label.config(text=f"AI guessed wrong! It guessed {guess}. ❌")
                self.yes_button.config(state="disabled")
                self.no_button.config(state="disabled")
            else:
                self.question_label.config(text="AI is still unsure who your character is.")
            self.yes_button.destroy()
            self.no_button.destroy()
            for widget in self.player_question_frame.winfo_children():
                    widget.destroy()

    def handle_response(self, user_said_yes):
        if hasattr(self, "current_trait"):
            def coerce(val):
                if isinstance(self.current_value, bool):
                    if isinstance(val, str):
                        return val.lower() == "true"
                    return bool(val)
                return val

            self.remaining_characters = self.engine.remaining_characters = [
                c for c in self.remaining_characters
                if (coerce(c.get_trait(self.current_trait)) == self.current_value) == user_said_yes
            ]

            for c in self.characters:
                if c.name in self.button_map and c not in self.remaining_characters:
                    self.button_map[c.name].config(state="disabled")
            
            # two sided or one sided
            if self.mode.get() == self.MODE_TWOSIDED:
                # disable answer question buttons
                self.yes_button.config(state="disabled")
                self.no_button.config(state="disabled")
                # delete ask question buttons
                for widget in self.player_question_frame.winfo_children():
                    widget.destroy()
                # ask next questionπ
                self.question_label.config(text=f"Ask a question")
                self.show_player_question_buttons()
            else:
                # one sided
                self.ask_next_question()

    def show_player_question_buttons(self):
        # Clear previous buttons
        for widget in self.player_question_frame.winfo_children():
            widget.destroy()

        # Choose useful traits (skip name/filename)
        traits_to_ask = ["gender", "eyes", "hair", "beard", "moustache", "nose", "glasses", "hat", "thick_eyebrows"]
        
        for trait in traits_to_ask:
            values = sorted(set(c.get_trait(trait) for c in self.characters))
            for value in values:
                btn = tk.Button(
                    self.player_question_frame,
                    text=f"{trait}: {value}",
                    command=lambda t=trait, v=value: self.handle_player_question(t, v),
                    width=15
                )
                btn.pack(side="left", padx=2, pady=2)

    def handle_player_question(self, trait, value):
        # Evaluate the trait against the AI's chosen secret character
        correct = self.ai_secret_character.get_trait(trait) == value


        # Update remaining characters
        self.remaining_characters = self.engine.remaining_characters = [
            c for c in self.remaining_characters
            if (c.get_trait(trait) == value) == correct
        ]

        # Update visuals
        for c in self.characters:
            if c.name in self.button_map and c not in self.remaining_characters:
                self.button_map[c.name].config(state="disabled")

        
        if self.mode.get() == self.MODE_TWOSIDED:
            self.answer_label.config(
                text=f"AI says: {'Yes ✅' if correct else 'No ❌'} to {trait} = {value}"
            )
            # delete ask question buttons
            for widget in self.player_question_frame.winfo_children():
                widget.destroy()
            # ask next question
            self.ask_next_question()
            # enable answer question buttons
            self.yes_button.config(state="normal")
            self.no_button.config(state="normal")
        else:
            self.question_label.config(
                text=f"AI says: {'Yes ✅' if correct else 'No ❌'} to {trait} = {value}"
            )

    def show_guess_menu(self):
        guess_window = tk.Toplevel(self.root)
        guess_window.title("Make Your Guess")

        tk.Label(guess_window, text="Who is the AI's character?").pack(pady=5)

        for character in self.remaining_characters:
            tk.Button(
                guess_window,
                text=character.name,
                command=lambda c=character, w=guess_window: self.evaluate_player_guess(c, w)
            ).pack(fill="x", padx=10, pady=2)
    def evaluate_player_guess(self, character, window):
        window.destroy()
        if character.name == self.ai_secret_character.name:
            self.question_label.config(text=f"You guessed {character.name}. Correct! 🎉 You win!")
        else:
            self.question_label.config(text=f"You guessed {character.name}. Incorrect ❌ AI's character was {self.ai_secret_character.name}.")
            
        self.yes_button.config(state='disabled')
        self.no_button.config(state='disabled')
        
        # Lock out further input
        for btn in self.player_question_frame.winfo_children():
            btn.config(state="disabled")
        self.guess_button.config(state="disabled")

    def evaluate_player_guess(self, character, window):
        window.destroy()
        if character.name == self.ai_secret_character.name:
            self.question_label.config(text=f"You guessed {character.name}. Correct! 🎉 You win!")
        else:
            self.question_label.config(text=f"You guessed {character.name}. Incorrect ❌ AI's character was {self.ai_secret_character.name}.")

        # Lock out further input
        for btn in self.player_question_frame.winfo_children():
            btn.config(state="disabled")
        self.guess_button.config(state="disabled")



if __name__ == "__main__":
    root = tk.Tk()
    app = GuessWhoGUI(root)
    root.mainloop()
