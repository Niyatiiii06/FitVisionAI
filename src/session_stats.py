import time


class SessionStats:

    def __init__(self):

        self.start_time = time.time()

        self.best_confidence = 0

        self.total_confidence = 0

        self.total_predictions = 0

    def update(self, confidence):

        if confidence > self.best_confidence:
            self.best_confidence = confidence

        self.total_confidence += confidence
        self.total_predictions += 1

    def get_average_confidence(self):

        if self.total_predictions == 0:
            return 0

        return self.total_confidence / self.total_predictions

    def get_session_time(self):

        elapsed = int(time.time() - self.start_time)

        minutes = elapsed // 60

        seconds = elapsed % 60

        return f"{minutes:02}:{seconds:02}"