class Character:
    def __init__(self, name, gender, eyes, hair, beard, moustache, nose, glasses, hat, thick_eyebrows, filename):
        self.name = name
        self.gender = gender
        self.eyes = eyes
        self.hair = hair
        self.beard = beard
        self.moustache = moustache
        self.nose = nose
        self.glasses = glasses
        self.hat = hat
        self.thick_eyebrows = thick_eyebrows
        self.filename = filename

    def get_trait(self, trait_name):
        return getattr(self, trait_name, None)

    def get_all_traits(self):
        return {
            "gender": self.gender,
            "eyes": self.eyes,
            "hair": self.hair,
            "beard": self.beard,
            "moustache": self.moustache,
            "nose": self.nose,
            "glasses": self.glasses,
            "hat": self.hat
        }

    def matches(self, trait_name, value):
        return self.get_trait(trait_name) == value

    def __str__(self):
        return f"{self.name}: {self.get_all_traits()}"

    @staticmethod
    def from_dict(data):
        return Character(
            name=data["name"],
            gender=data["gender"],
            eyes=data["eyes"],
            hair=data["hair"],
            beard=data["beard"],
            moustache=data["moustache"],
            nose=data["nose"],
            glasses=data["glasses"],
            hat=data["hat"],
            thick_eyebrows=data.get("thick_eyebrows", False),
            filename=data.get("filename")
        )

    
    def get_filename(self):
        return self.filename or f"{self.name.lower()}.png"
