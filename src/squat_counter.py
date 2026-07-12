class SquatCounter:

    def __init__(self,
                 up_threshold=160,
                 down_threshold=100):

        self.up_threshold = up_threshold
        self.down_threshold = down_threshold

        self.count = 0
        self.state = "UP"

    def update(self, angle):

        if angle < self.down_threshold:
            self.state = "DOWN"

        elif angle > self.up_threshold and self.state == "DOWN":
            self.count += 1
            self.state = "UP"

        return self.count