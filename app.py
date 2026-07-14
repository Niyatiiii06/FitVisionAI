import os

# -----------------------------
# Hide TensorFlow & MediaPipe Logs
# -----------------------------
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["GLOG_minloglevel"] = "3"

import warnings
warnings.filterwarnings("ignore")

import cv2
import time

from src.video_reader import VideoReader
from src.pose_detector import PoseDetector
from src.model_predictor import ModelPredictor
from src.prediction_smoother import PredictionSmoother
from src.squat_counter import SquatCounter
from src.ui import UI
from src.session_stats import SessionStats
from src.workout_summary import WorkoutSummary
from src.report_generator import ReportGenerator
from src.dataset_creator import DatasetCreator
from src.sample_filter import SampleFilter


def main():

    print("\n========== FitVisionAI ==========")
    print("1. Webcam")
    print("2. Video File")

    choice = input("\nEnter choice (1/2): ")

    if choice == "1":
        reader = VideoReader(0)

    elif choice == "2":
        reader = VideoReader("data/videos/squat.mp4")

    else:
        print("Invalid choice.")
        return

    detector = PoseDetector()
    predictor = ModelPredictor()
    smoother = PredictionSmoother(window_size=5)
    counter = SquatCounter()
    ui = UI()
    stats = SessionStats()
    summary = WorkoutSummary()
    report = ReportGenerator()
    dataset = DatasetCreator()
    filter = SampleFilter(threshold=5)

    prev_time = time.time()

    # -----------------------------
    # Auto Recording
    # -----------------------------
    recording = False
    save_interval = 0.30      # seconds
    last_saved = time.time()

    while True:

        frame, rgb_frame = reader.read_frame()

        if frame is None:
            break

        angles = None
        state = "----"
        confidence = 0

        results = detector.detect(rgb_frame)

        if results.pose_landmarks:

            landmarks = results.pose_landmarks[0]

            state, confidence = predictor.predict(landmarks)
            state = smoother.smooth(state)

            count = counter.update(state)

            stats.update(confidence)

            angles = detector.get_joint_angles(results)

            current_time = time.time()

            fps = 1 / (current_time - prev_time)
            prev_time = current_time

            detector.draw_landmarks(frame, results)

            ui.draw_panel(
                frame=frame,
                state=state,
                confidence=confidence,
                count=count,
                best_confidence=stats.best_confidence,
                avg_confidence=stats.get_average_confidence(),
                session_time=stats.get_session_time(),
                fps=fps
            )

            # -----------------------------
            # Show Joint Angles
            # -----------------------------
            if angles:

                y = 330

                cv2.putText(frame,
                            "JOINT ANGLES",
                            (20, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0,255,255),
                            2)

                y += 35

                for key, value in angles.items():

                    cv2.putText(
                        frame,
                        f"{key}: {value:.1f}",
                        (20, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (255,255,255),
                        2
                    )

                    y += 28

            # -----------------------------
            # AUTO DATASET RECORDING
            # -----------------------------
            if (
                recording
                and angles is not None
                and confidence >= 95
                and (time.time() - last_saved) > save_interval
            ):

                if filter.should_save(angles):

                    dataset.save_angles(
                        angles,
                        state
                    )

                    last_saved = time.time()

        # ---------------------------------
        # Recording Status
        # ---------------------------------

        color = (0,255,0)

        text = "REC : OFF"

        if recording:
            color = (0,0,255)
            text = "REC : ON"

        cv2.putText(
            frame,
            text,
            (20,30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

        cv2.putText(
            frame,
            f"Samples : {dataset.angle_count}",
            (20,60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,0),
            2
        )

        cv2.putText(
            frame,
            "R=Record  U=UP  D=DOWN  Q=Quit",
            (20, frame.shape[0]-20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,255,255),
            2
        )

        cv2.imshow("FitVisionAI", frame)

        key = cv2.waitKey(1) & 0xFF

        # Quit
        if key == ord("q"):
            break

        # Toggle Recording
        elif key == ord("r"):

            recording = not recording

            if recording:
                print("\nRecording Started\n")
            else:
                print("\nRecording Stopped\n")

        # Manual UP
        elif key == ord("u"):

            if angles:

                dataset.save_angles(
                    angles,
                    "UP"
                )

                print("Saved UP")

        # Manual DOWN
        elif key == ord("d"):

            if angles:

                dataset.save_angles(
                    angles,
                    "DOWN"
                )

                print("Saved DOWN")

    reader.release()

    report.generate(
        reps=counter.count,
        best_confidence=stats.best_confidence,
        avg_confidence=stats.get_average_confidence(),
        session_time=stats.get_session_time()
    )

    summary.show(
        reps=counter.count,
        best_confidence=stats.best_confidence,
        avg_confidence=stats.get_average_confidence(),
        session_time=stats.get_session_time()
    )


if __name__ == "__main__":
    main()