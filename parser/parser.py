from storage.storage import Storage


class Parser:
    def __init__(self, collected):
        self.collected = collected
        self.store = Storage()
        self.parse()

    def parse(self):
        self.store.bulk_insert(self.collected)
        print(self.store.query("system", 5))
        self.store.close()
