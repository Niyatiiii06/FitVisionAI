import cv2

from src.video_reader import VideoReader
from src.pose_detector import PoseDetector
from src.angle_calculator import AngleCalculator
from src.squat_counter import SquatCounter
from src.ui import UI


def main():

    # Initialize modules
    reader = VideoReader("data/videos/squat.mp4")
    detector = PoseDetector()
    counter = SquatCounter()
    ui = UI()

    while True:

        # Read frame
        frame, rgb_frame = reader.read_frame()

        if frame is None:
            break

        # Detect pose
        results = detector.detect(rgb_frame)

        # Check if pose is detected
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
            counter.update(angle)

            # Convert normalized coordinates to pixel coordinates
            knee_x = int(left_knee.x * frame.shape[1])
            knee_y = int(left_knee.y * frame.shape[0])

            # Draw knee angle near the knee
            cv2.putText(
                frame,
                f"{int(angle)}",
                (knee_x, knee_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),
                2
            )

            # Draw professional UI panel
            ui.draw_panel(
                frame,
                angle,
                counter.count,
                counter.state
            )
            ui.draw_progress_bar(frame, angle)
            ui.draw_feedback(
                frame,
                angle,
                counter.state
            )

        # Display video
        cv2.imshow("FitVisionAI", frame)

        # Exit on pressing Q
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release resources
    reader.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()