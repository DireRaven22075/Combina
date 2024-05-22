class Content:
    def __init__(self):
        self.name = str()
        self.platform = str()
        self.time = str()
        self.text = str()
        self.icon = str()
        self.image = str()


class Account:
    def __init__(self):
        self.connected = 0
        self.name = str()
        self.platform = str()
        self.token = str()
        self.icon = str()
        self.tag = str()
    
    def connect(self, token, name, tag):
        self.connected = 1
        self.token = token
        self.name = name
        self.tag = tag

