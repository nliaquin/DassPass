class service:
    def __init__(self, name, username, password, note):
        self.name = name
        self.username = username
        self.password = password
        self.note = note

    def set_name(self, name):
        self.name = name
    def get_name(self):
        return self.name

    def set_username(self, username):
        self.username = username
    def get_username(self):
        return self.username

    def set_password(self, password):
        self.password = password
    def get_password(self):
        return self.password

    def set_note(self, note):
        self.note = note
    def get_note(self):
        return self.note