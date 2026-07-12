import cv2

from src.video_reader import VideoReader
from src.pose_detector import PoseDetector
from src.angle_calculator import AngleCalculator
from src.squat_counter import SquatCounter


def main():

    # Initialize modules
    reader = VideoReader("data/videos/squat.mp4")
    detector = PoseDetector()
    counter = SquatCounter()

    frame_number = 0

    while True:

        # Read one frame
        frame, rgb_frame = reader.read_frame()

        if frame is None:
            break

        frame_number += 1

        # Detect pose
        results = detector.detect(rgb_frame)

        # If a person is detected
        if results.pose_landmarks:

            landmarks = results.pose_landmarks[0]

            # Extract landmarks
            left_hip = landmarks[23]
            left_knee = landmarks[25]
            left_ankle = landmarks[27]

            # Calculate knee angle
            angle = AngleCalculator.calculate_angle(
                (left_hip.x, left_hip.y),
                (left_knee.x, left_knee.y),
                (left_ankle.x, left_ankle.y)
            )

            # Update squat counter
            count = counter.update(angle)

            # Convert normalized coordinates to pixel coordinates
            knee_x = int(left_knee.x * frame.shape[1])
            knee_y = int(left_knee.y * frame.shape[0])

            # Draw knee angle
            cv2.putText(
                frame,
                f"{int(angle)}",
                (knee_x, knee_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),
                2
            )

            # Draw squat count
            cv2.putText(
                frame,
                f"Squats: {count}",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        # Display video
        cv2.imshow("FitVisionAI", frame)

        # Press Q to quit
        if cv2.waitKey(20) & 0xFF == ord("q"):
            break

    reader.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()