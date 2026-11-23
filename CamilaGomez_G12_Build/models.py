
import json
import os

DATA_FILE = "data.json"


class BalanceIQModel:

    def __init__(self):
        self.data = {
            "scores": {
                "academic_pressure": 50,
                "focus_score": 70,
                "balance_score": 65
            },
            "activity": {
                "name": "Studying",
                "duration": 60,
                "exertion": "Moderate"
            }
        }

        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as file:
                    self.data = json.load(file)
            except (json.JSONDecodeError, OSError):
                self.save_data()

        else:
            self.save_data()

        return self.data

    def save_data(self):
        with open(DATA_FILE, "w") as file:
            json.dump(self.data, file, indent=4)

    def get_scores(self):
        return self.data["scores"]

    def update_scores(self, scores):
        self.data["scores"] = scores
        self.save_data()

    def get_activity(self):
        return self.data["activity"]

    def update_activity(self, name, duration, exertion):
        self.data["activity"] = {
            "name": name,
            "duration": duration,
            "exertion": exertion
        }
        self.save_data()
