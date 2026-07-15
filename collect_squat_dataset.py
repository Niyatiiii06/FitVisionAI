import os
import cv2
import pandas as pd

from src.pose_detector import PoseDetector
from src.utils import calculate_angle

VIDEO_FOLDER = "data/videos/squat"

detector = PoseDetector()

dataset = []

print(f"Found {len(os.listdir(VIDEO_FOLDER))} videos")

for video_name in os.listdir(VIDEO_FOLDER):

    print(f"Processing : {video_name}")

    cap = cv2.VideoCapture(
        os.path.join(VIDEO_FOLDER, video_name)
    )

    frame_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = detector.detect(rgb)

        if results.pose_landmarks:

            landmarks = results.pose_landmarks[0]

            sample = []

            for lm in landmarks:

                sample.extend([
                    lm.x,
                    lm.y,
                    lm.z,
                    lm.visibility
                ])

            # ---------- Label using Knee Angle ----------

            hip = landmarks[23]
            knee = landmarks[25]
            ankle = landmarks[27]

            angle = calculate_angle(
                hip,
                knee,
                ankle
            )

            if angle < 150:
                label = "DOWN"
            else:
                label = "UP"

            sample.append("squat")
            sample.append(label)

            dataset.append(sample)

        frame_count += 1

    cap.release()

    print("Frames :", frame_count)

columns = []

for i in range(33):

    columns.extend([
        f"x{i}",
        f"y{i}",
        f"z{i}",
        f"v{i}"
    ])

columns.extend([
    "exercise",
    "label"
])

df = pd.DataFrame(
    dataset,
    columns=columns
)

os.makedirs(
    "data/dataset",
    exist_ok=True
)

df.to_csv(
    "data/dataset/squat_dataset.csv",
    index=False
)

print()
print("Saved", len(df), "samples")
print("data/dataset/squat_dataset.csv")