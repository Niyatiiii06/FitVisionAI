from src.angle_calculator import AngleCalculator


class AngleExtractor:

    def extract(self, landmarks):

        # -----------------------------
        # Left Side
        # -----------------------------
        left_shoulder = (
            landmarks[11].x,
            landmarks[11].y
        )

        left_hip = (
            landmarks[23].x,
            landmarks[23].y
        )

        left_knee = (
            landmarks[25].x,
            landmarks[25].y
        )

        left_ankle = (
            landmarks[27].x,
            landmarks[27].y
        )

        left_foot = (
            landmarks[31].x,
            landmarks[31].y
        )

        # -----------------------------
        # Right Side
        # -----------------------------
        right_shoulder = (
            landmarks[12].x,
            landmarks[12].y
        )

        right_hip = (
            landmarks[24].x,
            landmarks[24].y
        )

        right_knee = (
            landmarks[26].x,
            landmarks[26].y
        )

        right_ankle = (
            landmarks[28].x,
            landmarks[28].y
        )

        right_foot = (
            landmarks[32].x,
            landmarks[32].y
        )

        # -----------------------------
        # Calculate Angles
        # -----------------------------
        angles = {

            "left_knee":
                AngleCalculator.calculate_angle(
                    left_hip,
                    left_knee,
                    left_ankle
                ),

            "right_knee":
                AngleCalculator.calculate_angle(
                    right_hip,
                    right_knee,
                    right_ankle
                ),

            "left_hip":
                AngleCalculator.calculate_angle(
                    left_shoulder,
                    left_hip,
                    left_knee
                ),

            "right_hip":
                AngleCalculator.calculate_angle(
                    right_shoulder,
                    right_hip,
                    right_knee
                ),

            "left_ankle":
                AngleCalculator.calculate_angle(
                    left_knee,
                    left_ankle,
                    left_foot
                ),

            "right_ankle":
                AngleCalculator.calculate_angle(
                    right_knee,
                    right_ankle,
                    right_foot
                )

        }

        return angles