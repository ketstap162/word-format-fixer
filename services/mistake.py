class Mistake:
    def __init__(self, parameter, correct_value, incorrect_value):
        self.parameter = parameter
        self.correct_value = correct_value
        self.incorrect_value = incorrect_value

    def __repr__(self):
        return f"Mistake object ({self.parameter} {self.correct_value}:{self.incorrect_value})"

    def __str__(self):
        return f"Mistake: {self.parameter}: {self.incorrect_value}. Correct value: {self.correct_value}"

    def to_dict(self):
        return {
            "parameter": self.parameter,
            "correct": self.correct_value,
            "incorrect": self.incorrect_value,
        }
