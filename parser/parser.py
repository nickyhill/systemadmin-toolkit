from storage.storage import Storage
import json

class Parser:
    def __init__(self, collected):
        self.collected = collected
        self.store = Storage()
        self.parse()

    def parse(self):
        return self.collected
