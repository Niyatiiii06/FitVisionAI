class PushupCounter:

    def __init__(self):

        self.count = 0
        self.stage = "UP"

    def update(self, state):

        if state == "DOWN" and self.stage == "UP":
            self.stage = "DOWN"

        elif state == "UP" and self.stage == "DOWN":
            self.stage = "UP"
            self.count += 1

        return self.count