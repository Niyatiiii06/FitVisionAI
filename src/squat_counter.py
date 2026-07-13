class SquatCounter:

    def __init__(self):

        self.count = 0

        self.previous_state = "UP"

    def update(self, current_state):

        if (
            self.previous_state == "DOWN"
            and current_state == "UP"
        ):
            self.count += 1

        self.previous_state = current_state

        return self.count