import csv
import os


class DatasetCreator:

    def __init__(self):

        self.landmark_path = "data/dataset/squat_dataset.csv"
        self.angle_path = "data/dataset/angle_dataset.csv"

        os.makedirs(
            os.path.dirname(self.landmark_path),
            exist_ok=True
        )

        # -----------------------------
        # Landmark Dataset
        # -----------------------------
        if (not os.path.exists(self.landmark_path)) or (
            os.path.getsize(self.landmark_path) == 0
        ):

            with open(self.landmark_path, "w", newline="") as file:

                writer = csv.writer(file)

                header = []

                for i in range(33):
                    header.append(f"x{i}")
                    header.append(f"y{i}")

                header.append("exercise")
                header.append("label")

                writer.writerow(header)

        # -----------------------------
        # Angle Dataset
        # -----------------------------
        if (not os.path.exists(self.angle_path)) or (
            os.path.getsize(self.angle_path) == 0
        ):

            with open(self.angle_path, "w", newline="") as file:

                writer = csv.writer(file)

                writer.writerow([
                    "left_knee",
                    "right_knee",
                    "left_hip",
                    "right_hip",
                    "label"
                ])

        self.angle_count = self.get_angle_count()

    # ---------------------------------
    # Landmark Dataset
    # ---------------------------------

    def save_landmarks(self, landmarks, exercise, label):

        row = []

        for landmark in landmarks:
            row.append(landmark.x)
            row.append(landmark.y)

        row.append(exercise)
        row.append(label)

        with open(self.landmark_path, "a", newline="") as file:

            writer = csv.writer(file)
            writer.writerow(row)

    # ---------------------------------
    # Angle Dataset
    # ---------------------------------

    def save_angles(self, angles, label):

        with open(self.angle_path, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                angles["left_knee"],
                angles["right_knee"],
                angles["left_hip"],
                angles["right_hip"],
                label
            ])

        self.angle_count += 1

    # ---------------------------------
    # Count Samples
    # ---------------------------------

    def get_angle_count(self):

        if not os.path.exists(self.angle_path):
            return 0

        with open(self.angle_path) as file:

            return max(sum(1 for _ in file) - 1, 0)