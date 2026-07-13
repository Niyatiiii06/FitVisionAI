import csv
import os


class DatasetCreator:

    def __init__(self):

        self.file_path = "data/dataset/squat_dataset.csv"

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        if (not os.path.exists(self.file_path)) or (os.path.getsize(self.file_path) == 0):

            with open(self.file_path, "w", newline="") as file:

                writer = csv.writer(file)

                header = []

                # 33 landmarks
                for i in range(33):
                    header.append(f"x{i}")
                    header.append(f"y{i}")

                # New Column
                header.append("exercise")

                # Target Label
                header.append("label")

                writer.writerow(header)

    def save(self, landmarks, exercise, label):

        row = []

        for landmark in landmarks:
            row.append(landmark.x)
            row.append(landmark.y)

        row.append(exercise)
        row.append(label)

        with open(self.file_path, "a", newline="") as file:

            writer = csv.writer(file)
            writer.writerow(row)