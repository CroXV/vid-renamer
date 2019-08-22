class NameDatabase:
    def __init__(self):
        self.database = {}
        self.own_keys = []

    def set(self, key, value):
        if key not in self.own_keys:
            self.own_keys.append(key)

        self.database[key] = value

    def add(self, old, new):
        self.database[old] = new

    def get(self, key):
        return self.database[key]

    def update(self):
        # removes same key value and program set keys from instance database
        updated_database = {}
        for k, v in self.database.items():
            if k != v and k not in self.own_keys:
                updated_database[k] = v

        self.database = updated_database

