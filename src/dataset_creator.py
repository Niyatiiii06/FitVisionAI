import csv
import os


class DatasetCreator:

    def __init__(self):

        self.landmark_file = "data/dataset/squat_dataset.csv"
        self.angle_file = "data/dataset/angle_dataset.csv"

        os.makedirs("data/dataset", exist_ok=True)

        self.angle_count = 0

        # -------------------------
        # Landmark Dataset
        # -------------------------
        if (
            not os.path.exists(self.landmark_file)
            or os.path.getsize(self.landmark_file) == 0
        ):

            with open(self.landmark_file, "w", newline="") as file:

                writer = csv.writer(file)

                header = []

                for i in range(33):
                    header.append(f"x{i}")
                    header.append(f"y{i}")

                header.append("exercise")
                header.append("label")

                writer.writerow(header)

        # -------------------------
        # Angle Dataset
        # -------------------------
        if (
            not os.path.exists(self.angle_file)
            or os.path.getsize(self.angle_file) == 0
        ):

            with open(self.angle_file, "w", newline="") as file:

                writer = csv.writer(file)

                writer.writerow([
                    "left_knee",
                    "right_knee",
                    "left_hip",
                    "right_hip",
                    "left_ankle",
                    "right_ankle",
                    "label"
                ])

        # -------------------------
        # Count Existing Angle Samples
        # -------------------------
        with open(self.angle_file, "r", newline="") as file:

            self.angle_count = max(0, sum(1 for _ in file) - 1)

    # ------------------------------------------------
    # Save Landmark Dataset
    # ------------------------------------------------
    def save_landmarks(self, landmarks, exercise, label):

        row = []

        for landmark in landmarks:
            row.append(landmark.x)
            row.append(landmark.y)

        row.append(exercise)
        row.append(label)

        with open(self.landmark_file, "a", newline="") as file:

            writer = csv.writer(file)
            writer.writerow(row)

    # ------------------------------------------------
    # Save Angle Dataset
    # ------------------------------------------------
    def save_angles(self, angles, label):

        row = [

            angles["left_knee"],
            angles["right_knee"],
            angles["left_hip"],
            angles["right_hip"],
            angles["left_ankle"],
            angles["right_ankle"],
            label

        ]

        with open(self.angle_file, "a", newline="") as file:

            writer = csv.writer(file)
            writer.writerow(row)

        # Update sample count
        self.angle_count += 1