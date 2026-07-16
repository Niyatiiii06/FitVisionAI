class SquatCounter:

    def __init__(self):

        self.count = 0
        self.previous_state = "UP"

    def update(self, current_state, knee_angle):

        if current_state == "DOWN" and knee_angle < 100:
            self.previous_state = "DOWN"

        elif (
            self.previous_state == "DOWN"
            and current_state == "UP"
            and knee_angle > 160
        ):
            self.count += 1
            self.previous_state = "UP"

        return self.count