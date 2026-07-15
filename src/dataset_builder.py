import os
import csv
import cv2

from src.pose_detector import PoseDetector
from src.angle_calculator import AngleCalculator


class DatasetBuilder:

    def __init__(self):

        self.detector = PoseDetector()

    def build(self, exercise):

        video_folder = os.path.join("data", "videos", exercise)

        output_file = os.path.join(
            "data",
            "dataset",
            f"{exercise}_dataset.csv"
        )

        header = []

        for i in range(33):
            header.extend([
                f"x{i}",
                f"y{i}",
                f"z{i}",
                f"v{i}"
            ])

        header.append("label")

        samples = []

        videos = sorted(os.listdir(video_folder))

        print(f"\nFound {len(videos)} videos")

        for video in videos:

            if not video.lower().endswith(
                (".mp4", ".avi", ".mov", ".mkv")
            ):
                continue

            path = os.path.join(video_folder, video)

            print(f"Processing : {video}")

            cap = cv2.VideoCapture(path)

            frame_count = 0

            while True:

                ret, frame = cap.read()

                if not ret:
                    break

                frame_count += 1

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                results = self.detector.detect(rgb)

                if not results.pose_landmarks:
                    continue

                landmarks = results.pose_landmarks[0]

                row = self.create_sample(landmarks)

                label = self.get_label(
                    landmarks,
                    exercise
                )

                if label is None:
                    continue

                row.append(label)

                samples.append(row)

            cap.release()

            print(f"Frames : {frame_count}")

        with open(
            output_file,
            "w",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow(header)

            writer.writerows(samples)

        print(f"\nSaved {len(samples)} samples")
        print(output_file)

    def create_sample(self, landmarks):

        row = []

        for point in landmarks:

            row.extend([
                point.x,
                point.y,
                point.z,
                point.visibility
            ])

        return row

    def get_label(self, landmarks, exercise):

        # =====================================================
        # PUSH-UP
        # =====================================================
        if exercise == "pushup":

            left_elbow = AngleCalculator.calculate_angle(
                [landmarks[11].x, landmarks[11].y],
                [landmarks[13].x, landmarks[13].y],
                [landmarks[15].x, landmarks[15].y]
            )

            right_elbow = AngleCalculator.calculate_angle(
                [landmarks[12].x, landmarks[12].y],
                [landmarks[14].x, landmarks[14].y],
                [landmarks[16].x, landmarks[16].y]
            )

            # -----------------------------
            # Use the arm with better visibility
            # -----------------------------
            if landmarks[13].visibility >= landmarks[14].visibility:
                elbow = left_elbow
            else:
                elbow = right_elbow

            # -----------------------------
            # Auto Label
            # -----------------------------
            if elbow >= 160:
                return "UP"

            elif elbow <= 120:
                return "DOWN"

            else:
                return None

        # =====================================================
        # SQUAT
        # =====================================================
        elif exercise == "squat":

            left_knee = AngleCalculator.calculate_angle(
                [landmarks[23].x, landmarks[23].y],
                [landmarks[25].x, landmarks[25].y],
                [landmarks[27].x, landmarks[27].y]
            )

            right_knee = AngleCalculator.calculate_angle(
                [landmarks[24].x, landmarks[24].y],
                [landmarks[26].x, landmarks[26].y],
                [landmarks[28].x, landmarks[28].y]
            )

            if landmarks[25].visibility >= landmarks[26].visibility:
                knee = left_knee
            else:
                knee = right_knee

            if knee >= 165:
                return "UP"

            elif knee <= 110:
                return "DOWN"

            else:
                return None

        # =====================================================
        # LUNGE
        # =====================================================
        elif exercise == "lunge":

            left_knee = AngleCalculator.calculate_angle(
                [landmarks[23].x, landmarks[23].y],
                [landmarks[25].x, landmarks[25].y],
                [landmarks[27].x, landmarks[27].y]
            )

            right_knee = AngleCalculator.calculate_angle(
                [landmarks[24].x, landmarks[24].y],
                [landmarks[26].x, landmarks[26].y],
                [landmarks[28].x, landmarks[28].y]
            )

            if landmarks[25].visibility >= landmarks[26].visibility:
                knee = left_knee
            else:
                knee = right_knee

            if knee >= 160:
                return "UP"

            elif knee <= 95:
                return "DOWN"

            else:
                return None

        return None