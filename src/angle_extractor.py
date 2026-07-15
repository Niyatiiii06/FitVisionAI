from src.angle_calculator import AngleCalculator


class AngleExtractor:

    def __init__(self, exercise):

        self.exercise = exercise

    def extract(self, landmarks):

        if self.exercise == "squat":
            return self.extract_squat(landmarks)

        elif self.exercise == "pushup":
            return self.extract_pushup(landmarks)

        return {}

    # =====================================================
    # SQUAT
    # =====================================================

    def extract_squat(self, lm):

        angles = {}

        angles["left_knee"] = AngleCalculator.calculate_angle(
            [lm[23].x, lm[23].y],
            [lm[25].x, lm[25].y],
            [lm[27].x, lm[27].y]
        )

        angles["right_knee"] = AngleCalculator.calculate_angle(
            [lm[24].x, lm[24].y],
            [lm[26].x, lm[26].y],
            [lm[28].x, lm[28].y]
        )

        angles["left_hip"] = AngleCalculator.calculate_angle(
            [lm[11].x, lm[11].y],
            [lm[23].x, lm[23].y],
            [lm[25].x, lm[25].y]
        )

        angles["right_hip"] = AngleCalculator.calculate_angle(
            [lm[12].x, lm[12].y],
            [lm[24].x, lm[24].y],
            [lm[26].x, lm[26].y]
        )

        angles["left_ankle"] = AngleCalculator.calculate_angle(
            [lm[25].x, lm[25].y],
            [lm[27].x, lm[27].y],
            [lm[31].x, lm[31].y]
        )

        angles["right_ankle"] = AngleCalculator.calculate_angle(
            [lm[26].x, lm[26].y],
            [lm[28].x, lm[28].y],
            [lm[32].x, lm[32].y]
        )

        return angles

    # =====================================================
    # PUSH-UP
    # =====================================================

    def extract_pushup(self, lm):

        angles = {}

        angles["left_elbow"] = AngleCalculator.calculate_angle(
            [lm[11].x, lm[11].y],
            [lm[13].x, lm[13].y],
            [lm[15].x, lm[15].y]
        )

        angles["right_elbow"] = AngleCalculator.calculate_angle(
            [lm[12].x, lm[12].y],
            [lm[14].x, lm[14].y],
            [lm[16].x, lm[16].y]
        )

        angles["left_shoulder"] = AngleCalculator.calculate_angle(
            [lm[23].x, lm[23].y],
            [lm[11].x, lm[11].y],
            [lm[13].x, lm[13].y]
        )

        angles["right_shoulder"] = AngleCalculator.calculate_angle(
            [lm[24].x, lm[24].y],
            [lm[12].x, lm[12].y],
            [lm[14].x, lm[14].y]
        )

        angles["left_body"] = AngleCalculator.calculate_angle(
            [lm[11].x, lm[11].y],
            [lm[23].x, lm[23].y],
            [lm[27].x, lm[27].y]
        )

        angles["right_body"] = AngleCalculator.calculate_angle(
            [lm[12].x, lm[12].y],
            [lm[24].x, lm[24].y],
            [lm[28].x, lm[28].y]
        )

        return angles