class PostureChecker:

    def __init__(self, exercise):

        self.exercise = exercise

    def evaluate(self, angles):

        if self.exercise == "squat":
            return self.check_squat(angles)

        elif self.exercise == "pushup":
            return self.check_pushup(angles)

        return {
            "score": 0,
            "feedback": []
        }

    # =====================================================
    # SQUAT
    # =====================================================

    def check_squat(self, angles):

        score = 100
        feedback = []

        knee = (
            angles["left_knee"] +
            angles["right_knee"]
        ) / 2

        hip = (
            angles["left_hip"] +
            angles["right_hip"]
        ) / 2

        ankle = (
            angles["left_ankle"] +
            angles["right_ankle"]
        ) / 2

        # Knee Depth
        if knee > 110:
            score -= 20
            feedback.append("Go Lower")

        # Hip Position
        if hip > 120:
            score -= 20
            feedback.append("Push Hips Back")

        # Heel Lift
        if ankle < 70:
            score -= 10
            feedback.append("Keep Heels Down")

        score = max(score, 0)

        return {
            "score": score,
            "feedback": feedback
        }

    # =====================================================
    # PUSH-UP
    # =====================================================

    def check_pushup(self, angles):

        score = 100
        feedback = []

        elbow = (
            angles["left_elbow"] +
            angles["right_elbow"]
        ) / 2

        shoulder = (
            angles["left_shoulder"] +
            angles["right_shoulder"]
        ) / 2

        body = (
            angles["left_body"] +
            angles["right_body"]
        ) / 2

        # Elbow Bend
        if elbow > 140:
            score -= 20
            feedback.append("Bend Elbows More")

        # Body Alignment
        if body < 160:
            score -= 20
            feedback.append("Keep Body Straight")

        # Shoulder Position
        if shoulder < 40:
            score -= 10
            feedback.append("Keep Shoulders Stable")

        score = max(score, 0)

        return {
            "score": score,
            "feedback": feedback
        }