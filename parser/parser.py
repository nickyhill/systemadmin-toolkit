from storage.storage import Storage
import json

class Parser:
    def __init__(self, collected):
        self.collected = collected
        self.store = Storage()
        self.parse()

    def parse(self):
        self.store.bulk_insert(self.collected)
        parsed = self.store.query("system", 5)
        print(json.dumps(parsed, indent=4))
        self.store.close()
