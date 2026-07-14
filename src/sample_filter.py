class SampleFilter:

    def __init__(self, threshold=5):

        self.threshold = threshold
        self.previous_angles = None

    def should_save(self, angles):

        if self.previous_angles is None:

            self.previous_angles = angles.copy()
            return True

        total_difference = 0

        for key in angles:

            total_difference += abs(
                angles[key] - self.previous_angles[key]
            )

        average_difference = total_difference / len(angles)

        if average_difference >= self.threshold:

            self.previous_angles = angles.copy()
            return True

        return False