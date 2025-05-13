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
        
        
        #self.print_tree()
        
        
    def print_tree(self):
        '''
        Prints the trained decision tree to the terminal as text.
        '''
        feature_names = self.vectorizer.get_feature_names_out()
        tree_text = export_text(self.classifier, feature_names=list(feature_names))
        print(tree_text)
        
        

    def recommend_question(self, remaining_characters):
        """
        Recommends the next best question (trait, value) to ask using the decision tree.
        Returns a tuple like ("hair", "blonde").
        """
        if not remaining_characters:
            return None

        # Transform remaining characters into feature vectors
        X_remain = self.vectorizer.transform([c.get_all_traits() for c in remaining_characters])
        tree = self.classifier.tree_
        feature_names = self.vectorizer.get_feature_names_out()

        # Start at the root node
        node = 0
        while tree.feature[node] != -2:  # -2 means it's a leaf node
            feature_idx = tree.feature[node]
            threshold = tree.threshold[node]
            feature_name = feature_names[feature_idx]

            # Check how remaining characters split at this node
            left_indices = X_remain[:, feature_idx] <= threshold
            right_indices = X_remain[:, feature_idx] > threshold

            # If all remaining characters go to one side, continue down that branch
            if left_indices.all():
                node = tree.children_left[node]
            elif right_indices.all():
                node = tree.children_right[node]
            else:
                # This is the best split for the current group
                # For categorical features, threshold is usually 0.5 (one-hot encoded)
                # Find the value that splits the group
                # For one-hot, feature_name will be like "hair=blonde"
                if "=" in feature_name:
                    trait, value = feature_name.split("=")
                    print(trait, value)
                    return (trait, value)
                else:
                    # print(feature_name, threshold)
                    return (feature_name, False)
        return None

    def _parse_split_line(self, line):
        """
        Parses the first line of the decision tree to extract (trait, value).
        """
        try:
            line = line.strip()
            if "<=" in line:
                feature_expr = line.split("<= ")[0] 
                parts = feature_expr.split()
                if not parts:
                    return None
                feature = parts[-1] 
                if "=" in feature:
                    trait, value = feature.split("=")
                    value = self._coerce_value(value)
                    return trait, value
        except Exception as e:
            print(f"Failed to parse split line: {line}, error: {e}")
        return None


    def _coerce_value(self, val):
        """
        Converts string value into appropriate type
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
        Guesses solution when one option is remaining
        """
        if len(remaining_characters) == 1:
            return remaining_characters[0].name
        return None
