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
from src.pushup_counter import PushupCounter

from src.angle_extractor import AngleExtractor
from src.posture_checker import PostureChecker
from src.feedback_generator import FeedbackGenerator
from src.workout_history import WorkoutHistory
from src.workout_analytics import WorkoutAnalytics

from src.ui import UI

from src.session_stats import SessionStats
from src.workout_summary import WorkoutSummary
from src.report_generator import ReportGenerator


def main():

    print("\n========== FitVisionAI ==========")

    print("\nExercise")
    print("1. Squat")
    print("2. Push-up")

    exercise_choice = input("\nChoose Exercise (1/2): ")

    if exercise_choice == "1":
        exercise = "squat"

    elif exercise_choice == "2":
        exercise = "pushup"

    else:
        print("Invalid Choice")
        return


    print("\nInput Source")
    print("1. Video")
    print("2. Webcam")

    choice = input("\nChoose Input (1/2): ")

    if choice == "1":

        video_path = input(
            "\nEnter video path : "
        )

        if not os.path.exists(video_path):
            print("\nVideo not found.")
            return

        reader = VideoReader(video_path)

    elif choice == "2":

        reader = VideoReader(0)

    else:

        print("Invalid Choice")
        return

    detector = PoseDetector()

    predictor = ModelPredictor(exercise)

    smoother = PredictionSmoother(window_size=5)

    if exercise == "squat":
        counter = SquatCounter()
    else:
        counter = PushupCounter()

    angle_extractor = AngleExtractor(exercise)

    posture_checker = PostureChecker(exercise)

    feedback_generator = FeedbackGenerator(exercise)

    ui = UI()

    stats = SessionStats()

    summary = WorkoutSummary()

    report = ReportGenerator()

    history = WorkoutHistory()

    analytics = WorkoutAnalytics()

    prev_time = time.time()

    while True:

        frame, rgb_frame = reader.read_frame()

        if frame is None:
            break

        state = "----"
        confidence = 0

        posture_score = 0

        feedback = []

        angles = {}

        results = detector.detect(rgb_frame)

        if results.pose_landmarks:

            landmarks = results.pose_landmarks[0]

            # ----------------------------------
            # ANN Prediction
            # ----------------------------------
            state, confidence = predictor.predict(landmarks)

            state = smoother.smooth(state)

            # ----------------------------------
            # Angle Extraction
            # ----------------------------------
            angles = angle_extractor.extract(landmarks)

            # ----------------------------------
            # Posture Analysis
            # ----------------------------------
            posture = posture_checker.evaluate(angles)

            posture_score = posture["score"]

            # ----------------------------------
            # Feedback
            # ----------------------------------
            feedback = feedback_generator.generate(posture)

            # ----------------------------------
            # Rep Counter
            # ----------------------------------
            count = counter.update(state)

            # ----------------------------------
            # Session Stats
            # ----------------------------------
            stats.update(confidence)

            # ----------------------------------
            # FPS
            # ----------------------------------
            current_time = time.time()

            fps = 1 / (current_time - prev_time)

            prev_time = current_time

            # ----------------------------------
            # Draw Pose
            # ----------------------------------
            detector.draw_landmarks(frame, results)

            # ----------------------------------
            # Dashboard
            # ----------------------------------
            ui.draw_panel(
                frame=frame,
                exercise=exercise,
                state=state,
                confidence=confidence,
                count=count,
                best_confidence=stats.best_confidence,
                avg_confidence=stats.get_average_confidence(),
                session_time=stats.get_session_time(),
                fps=fps,
                posture_score=posture_score,
                feedback=feedback,
                angles=angles
            )

        cv2.imshow("FitVisionAI", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    reader.release()

    cv2.destroyAllWindows()

    report.generate(
        exercise=exercise,
        reps=counter.count,
        posture_score=posture_score,
        best_confidence=stats.best_confidence,
        avg_confidence=stats.get_average_confidence(),
        session_time=stats.get_session_time()
    )

    history.save(
        exercise=exercise,
        reps=counter.count,
        posture_score=posture_score,
        best_confidence=stats.best_confidence,
        avg_confidence=stats.get_average_confidence(),
        session_time=stats.get_session_time()
    )

    analytics.generate()

    summary.show(
        reps=counter.count,
        best_confidence=stats.best_confidence,
        avg_confidence=stats.get_average_confidence(),
        session_time=stats.get_session_time()
    )


if __name__ == "__main__":
    main()