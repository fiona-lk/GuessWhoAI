from character.character import Character
import json

def load_characters(filepath):
    with open(filepath, "r") as file:
        data = json.load(file)
        return [Character.from_dict(c) for c in data]
