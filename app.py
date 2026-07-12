from src.video_reader import VideoReader
from src.pose_detector import PoseDetector
from src.angle_calculator import AngleCalculator


def main():

    reader = VideoReader("data/videos/squat.mp4")
    detector = PoseDetector()

    frame_number = 0

    while True:

        frame = reader.read_frame()

        if frame is None:
            break

        frame_number += 1

        results = detector.detect(frame)

        if results.pose_landmarks:

            landmarks = results.pose_landmarks[0]

            left_hip = landmarks[23]
            left_knee = landmarks[25]
            left_ankle = landmarks[27]

            angle = AngleCalculator.calculate_angle(
                (left_hip.x, left_hip.y),
                (left_knee.x, left_knee.y),
                (left_ankle.x, left_ankle.y)
            )

            print(f"Frame {frame_number}: {angle:.2f}")

    reader.release()


if __name__ == "__main__":
    main()