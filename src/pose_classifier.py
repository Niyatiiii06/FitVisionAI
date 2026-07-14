class PoseClassifier:

    def classify(self, angles):

        left_knee = angles["left_knee"]
        right_knee = angles["right_knee"]

        # Standing
        if left_knee > 160 and right_knee > 160:
            return "UP"

        # Squatting
        elif left_knee < 110 and right_knee < 110:
            return "DOWN"

        # Ignore intermediate positions
        return None