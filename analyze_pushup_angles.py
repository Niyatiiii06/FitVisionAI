import os
import cv2
import numpy as np

from src.pose_detector import PoseDetector
from src.angle_calculator import AngleCalculator

VIDEO_FOLDER = "data/videos/pushup"

detector = PoseDetector()

angles = []

for video in sorted(os.listdir(VIDEO_FOLDER)):

    if not video.endswith((".mp4", ".avi", ".mov", ".mkv")):
        continue

    print(f"Processing {video}")

    cap = cv2.VideoCapture(os.path.join(VIDEO_FOLDER, video))

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = detector.detect(rgb)

        if not results.pose_landmarks:
            continue

        lm = results.pose_landmarks[0]

        left = AngleCalculator.calculate_angle(
            [lm[11].x, lm[11].y],
            [lm[13].x, lm[13].y],
            [lm[15].x, lm[15].y]
        )

        right = AngleCalculator.calculate_angle(
            [lm[12].x, lm[12].y],
            [lm[14].x, lm[14].y],
            [lm[16].x, lm[16].y]
        )

        angles.append((left + right) / 2)

    cap.release()

angles = np.array(angles)

print("\n========== Statistics ==========")
print(f"Minimum : {angles.min():.2f}")
print(f"Maximum : {angles.max():.2f}")
print(f"Mean    : {angles.mean():.2f}")
print(f"Median  : {np.median(angles):.2f}")

print("\nPercentiles")
print(f"5%   : {np.percentile(angles,5):.2f}")
print(f"10%  : {np.percentile(angles,10):.2f}")
print(f"25%  : {np.percentile(angles,25):.2f}")
print(f"50%  : {np.percentile(angles,50):.2f}")
print(f"75%  : {np.percentile(angles,75):.2f}")
print(f"90%  : {np.percentile(angles,90):.2f}")
print(f"95%  : {np.percentile(angles,95):.2f}")