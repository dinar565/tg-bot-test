from enum import Enum
import datetime


class TrainingState(Enum):
    pending = 1
    completed = 2


class TrainingRecord:

    def __init__(self, description, state=TrainingState.pending, creation_date=datetime.datetime.now(), name="Training"):
        self.description = description
        self.state = state
        self.creation_date = creation_date
        self.name = name

    def to_dict(self):
        return {"state": self.state.name, "creation_date": str(self.creation_date), "name": self.name, "description": self.description}
