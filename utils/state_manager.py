import json, os

class StateManager:
    def __init__(self, file='state.json'):
        self.file = file
        self.state = self.load()

    def load(self):
        return json.load(open(self.file)) if os.path.exists(self.file) else []

    def is_processed(self, zip): return zip in self.state

    def mark_as_processed(self, zip):
        self.state.append(zip)
        json.dump(self.state, open(self.file, 'w'))
