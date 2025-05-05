from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.feature_extraction import DictVectorizer
import random

class DecisionTreeAI:
    def __init__(self, characters):
        """
        Initializes the AI with a list of Character objects.
        """
        self.characters = characters
        self.vectorizer = DictVectorizer(sparse=False)
        self.X_raw = [char.get_all_traits() for char in characters]
        self.y = [char.name for char in characters]

        self.X = self.vectorizer.fit_transform(self.X_raw)
        self.classifier = DecisionTreeClassifier(criterion="entropy")
        self.classifier.fit(self.X, self.y)

    def recommend_question(self, remaining_characters):
        """
        Recommends the next best question (trait=value) to ask based on the current
        remaining characters. Returns a tuple like ("hair", "blonde").
        """
        best_trait = None
        best_value = None
        min_diff = float('inf')

        traits = ["gender", "eyes", "hair", "beard", "moustache", "nose", "glasses", "hat", "thick_eyebrows"]


        for trait in traits:
            values = set(c.get_trait(trait) for c in remaining_characters)
            for value in values:
                yes_group = [c for c in remaining_characters if c.get_trait(trait) == value]
                no_group = [c for c in remaining_characters if c.get_trait(trait) != value]
                diff = abs(len(yes_group) - len(no_group))

                if 0 < len(yes_group) < len(remaining_characters) and diff < min_diff:
                    best_trait = trait
                    best_value = value
                    min_diff = diff

        return (best_trait, best_value) if best_trait else None


    def _parse_split_line(self, line):
        """
        Parses the first line of the decision tree to extract (trait, value).
        Expected format: "|--- trait=value <= 0.50"
        """
        try:
            line = line.strip()
            if "<=" in line:
                feature_expr = line.split("<= ")[0]  # e.g., "nose=small"
                parts = feature_expr.split()
                if not parts:
                    return None
                feature = parts[-1]  # last token: nose=small
                if "=" in feature:
                    trait, value = feature.split("=")
                    value = self._coerce_value(value)
                    return trait, value
        except Exception as e:
            print(f"Failed to parse split line: {line}, error: {e}")
        return None


    def _coerce_value(self, val):
        """
        Converts string value into appropriate type: bool, int, or str.
        """
        if val.lower() == "true":
            return True
        elif val.lower() == "false":
            return False
        elif val.isdigit():
            return int(val)
        return val

    def guess_character(self, remaining_characters):
        """
        If one character remains, return its name. Otherwise, return None.
        """
        if len(remaining_characters) == 1:
            return remaining_characters[0].name
        return None
