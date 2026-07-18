import time
import cv2

from src.video_reader import VideoReader
from src.pose_detector import PoseDetector
from src.model_predictor import ModelPredictor

from src.squat_counter import SquatCounter
from src.pushup_counter import PushupCounter

from src.posture_checker import PostureChecker
from src.feedback_generator import FeedbackGenerator

from src.report_generator import ReportGenerator
from src.workout_history import WorkoutHistory
from src.workout_analytics import WorkoutAnalytics


class StreamlitProcessor:

    def __init__(self, exercise):

        self.exercise = exercise.lower()

        self.pose_detector = PoseDetector()

        self.model = ModelPredictor(
            self.exercise
        )

        if self.exercise == "squat":
            self.counter = SquatCounter()
        else:
            self.counter = PushupCounter()

        self.posture_checker = PostureChecker(
            self.exercise
        )

        self.feedback_generator = FeedbackGenerator(
            self.exercise
        )

        self.report_generator = ReportGenerator()

        self.history = WorkoutHistory()

        self.analytics = WorkoutAnalytics()

    def process(
        self,
        video_path,
        frame_callback=None,
        progress_callback=None
    ):

        reader = VideoReader(video_path)
        fps= reader.cap.get(cv2.CAP_PROP_FPS)
        if fps<= 0:
            fps= 30  # Default to 30 if FPS is not available

        width = 1280
        height = 720

        start = time.time()

        best_confidence = 0

        confidence_list = []

        posture_scores = []

        last_feedback = []

        total_frames = int(
            reader.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        current_frame = 0

        while True:

            frame, rgb = reader.read_frame()

            if frame is None:
                break

            current_frame += 1

            results = self.pose_detector.detect(rgb)

            if results.pose_landmarks:

                landmarks = results.pose_landmarks[0]

                state, confidence = self.model.predict(
                    landmarks
                )

                angles = self.pose_detector.get_joint_angles(
                    results
                )

                knee=(
                    angles["left_knee"] +
                    angles["right_knee"]
                ) / 2

                if self.exercise == "squat":
                    reps = self.counter.update(state, knee)
                else:
                    reps = self.counter.update(state)

                posture = self.posture_checker.evaluate(
                    angles
                )

                feedback = self.feedback_generator.generate(
                    posture
                )

                confidence_list.append(
                    confidence
                )

                posture_scores.append(
                    posture["score"]
                )

                best_confidence = max(
                    best_confidence,
                    confidence
                )

                last_feedback = feedback

                frame = self.pose_detector.draw_landmarks(
                    frame,
                    results
                )

                frame = cv2.resize(frame, (640, 480))

            else:

                reps = self.counter.count

                confidence = 0

                posture = {
                    "score": 0,
                    "feedback": []
                }

                feedback = []
            frame = cv2.resize(frame, (640, 480))

            if frame_callback:

                frame_callback(
                    frame,
                    reps,
                    confidence,
                    posture["score"],
                    feedback
                )

            if progress_callback and total_frames > 0:

                progress_callback(
                    current_frame / total_frames
                )

        reader.release()

        session_time = round(
            time.time() - start,
            1
        )

        if len(confidence_list) == 0:

            avg_confidence = 0

        else:

            avg_confidence = sum(
                confidence_list
            ) / len(confidence_list)

        if len(posture_scores) == 0:

            avg_score = 0

        else:

            avg_score = sum(
                posture_scores
            ) / len(posture_scores)

        # ---------------------------------
        # Save Workout History
        # ---------------------------------

        self.history.save(

            exercise=self.exercise,

            reps=self.counter.count,

            posture_score=avg_score,

            best_confidence=best_confidence,

            avg_confidence=avg_confidence,

            session_time=session_time

        )

        # ---------------------------------
        # Generate Analytics
        # ---------------------------------

        self.analytics.generate()

        # ---------------------------------
        # Generate PDF Report
        # ---------------------------------

        pdf_path = self.report_generator.generate(

            exercise=self.exercise,

            reps=self.counter.count,

            posture_score=avg_score,

            best_confidence=best_confidence,

            avg_confidence=avg_confidence,

            session_time=session_time

        )

        return {

            "exercise": self.exercise,

            "repetitions": self.counter.count,

            "score": round(avg_score, 1),

            "best_confidence": round(best_confidence, 1),

            "average_confidence": round(avg_confidence, 1),

            "feedback": last_feedback,

            "duration": session_time,

            "pdf": pdf_path,

            "analytics": {

                "reps": "reports/reps_history.png",

                "score": "reports/score_history.png",

                "confidence": "reports/confidence_history.png",

            }

        }