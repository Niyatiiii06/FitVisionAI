import os

# Hide TensorFlow logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Disable oneDNN info message
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Hide MediaPipe/GLOG logs
os.environ["GLOG_minloglevel"] = "3"

# Hide TensorFlow Python warnings
os.environ["TF_CPP_MIN_VLOG_LEVEL"] = "3"

import warnings
warnings.filterwarnings("ignore")

import cv2
import time

from src.video_reader import VideoReader
from src.pose_detector import PoseDetector
from src.model_predictor import ModelPredictor
from src.squat_counter import SquatCounter
from src.ui import UI
from src.session_stats import SessionStats
from src.workout_summary import WorkoutSummary


def main():

    # -----------------------------
    # Initialize Modules
    # -----------------------------
    reader = VideoReader("data/videos/squat.mp4")

    detector = PoseDetector()

    predictor = ModelPredictor()

    counter = SquatCounter()

    ui = UI()

    stats = SessionStats()

    summary = WorkoutSummary()

    prev_time = time.time()

    # -----------------------------
    # Main Loop
    # -----------------------------
    while True:

        frame, rgb_frame = reader.read_frame()

        if frame is None:
            break

        results = detector.detect(rgb_frame)

        if results.pose_landmarks:

            landmarks = results.pose_landmarks[0]

            # -----------------------------
            # Deep Learning Prediction
            # -----------------------------
            state, confidence = predictor.predict(landmarks)

            # -----------------------------
            # Squat Counter
            # -----------------------------
            count = counter.update(state)

            # -----------------------------
            # Session Statistics
            # -----------------------------
            stats.update(confidence)

            # -----------------------------
            # FPS
            # -----------------------------
            current_time = time.time()
            fps = 1 / (current_time - prev_time)
            prev_time = current_time

            # -----------------------------
            # Draw Skeleton
            # -----------------------------
            detector.draw_landmarks(frame, results)

            # -----------------------------
            # Draw UI
            # -----------------------------
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

        cv2.imshow("FitVisionAI", frame)

        key = cv2.waitKey(1)

        if key == ord("q"):
            break

    reader.release()

    summary.show(
        reps=counter.count,
        best_confidence=stats.best_confidence,
        avg_confidence=stats.get_average_confidence(),
        session_time=stats.get_session_time()
    )


if __name__ == "__main__":
    main()