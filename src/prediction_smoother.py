from collections import deque


class PredictionSmoother:

    def __init__(self, window_size=7):

        self.history = deque(maxlen=window_size)

    def smooth(self, state):

        self.history.append(state)

        up = self.history.count("UP")
        down = self.history.count("DOWN")

        if up > down:
            return "UP"

        if down > up:
            return "DOWN"

        return self.history[-1]