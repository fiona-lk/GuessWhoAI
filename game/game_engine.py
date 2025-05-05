class GameEngine:
    def __init__(self, characters, ai_player):
        self.original_characters = characters
        self.remaining_characters = characters.copy()
        self.ai_player = ai_player

    def is_over(self):
        return len(self.remaining_characters) <= 1

    def update_state(self, trait, value, user_said_yes):
        if user_said_yes:
            self.remaining_characters = [
                c for c in self.remaining_characters if c.get_trait(trait) == value
            ]
        else:
            self.remaining_characters = [
                c for c in self.remaining_characters if c.get_trait(trait) != value
            ]
