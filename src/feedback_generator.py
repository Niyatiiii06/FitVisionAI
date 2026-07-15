class FeedbackGenerator:

    def __init__(self, exercise):

        self.exercise = exercise

    def generate(self, posture):

        feedback = []

        score = posture["score"]

        # ==========================================
        # Overall Workout Rating
        # ==========================================

        if score >= 95:
            feedback.append("Excellent Form")
            feedback.append("Perfect Technique")

        elif score >= 85:
            feedback.append("Very Good Form")

        elif score >= 75:
            feedback.append("Good Form")

        elif score >= 60:
            feedback.append("Average Form")

        else:
            feedback.append("Poor Form")

        # ==========================================
        # Exercise Specific Feedback
        # ==========================================

        feedback.extend(posture["feedback"])

        # ==========================================
        # General Suggestions
        # ==========================================

        if self.exercise == "squat":

            if score >= 90:

                feedback.append("Maintain Depth")
                feedback.append("Control Movement")

            elif score >= 75:

                feedback.append("Go Slightly Lower")
                feedback.append("Keep Knees Stable")

            else:

                feedback.append("Keep Back Straight")
                feedback.append("Drive Through Heels")

        elif self.exercise == "pushup":

            if score >= 90:

                feedback.append("Maintain Full Range")
                feedback.append("Excellent Control")

            elif score >= 75:

                feedback.append("Lower Chest More")
                feedback.append("Keep Core Tight")

            else:

                feedback.append("Straighten Back")
                feedback.append("Keep Elbows Controlled")

        # ==========================================
        # Remove Duplicate Messages
        # ==========================================

        feedback = list(dict.fromkeys(feedback))

        return feedback