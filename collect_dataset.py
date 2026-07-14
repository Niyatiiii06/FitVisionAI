import os

# ---------------------------------------
# Hide TensorFlow / MediaPipe Logs
# ---------------------------------------
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["GLOG_minloglevel"] = "3"

import warnings
warnings.filterwarnings("ignore")

import cv2
import time

from src.video_reader import VideoReader
from src.pose_detector import PoseDetector
from src.angle_extractor import AngleExtractor
from src.pose_classifier import PoseClassifier
from src.dataset_creator import DatasetCreator
from src.sample_filter import SampleFilter


def main():

    print("\n========== FitVisionAI Dataset Collector ==========\n")
    print("Press R to Start/Stop Recording")
    print("Press Q to Quit\n")

    reader = VideoReader(0)

    detector = PoseDetector()

    extractor = AngleExtractor()

    classifier = PoseClassifier()

    dataset = DatasetCreator()

    sample_filter = SampleFilter(threshold=5)

    recording = False

    save_interval = 0.30

    last_saved = time.time()

    while True:

        frame, rgb = reader.read_frame()

        if frame is None:
            break

        label = None
        angles = None

        results = detector.detect(rgb)

        if results.pose_landmarks:

            landmarks = results.pose_landmarks[0]

            detector.draw_landmarks(frame, results)

            angles = extractor.extract(landmarks)

            label = classifier.classify(angles)

            display_label = label if label else "UNKNOWN"

            # ---------------------------------------
            # Pose Label
            # ---------------------------------------

            cv2.putText(
                frame,
                f"Pose : {display_label}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

            # ---------------------------------------
            # Joint Angles
            # ---------------------------------------

            y = 80

            for key, value in angles.items():

                cv2.putText(
                    frame,
                    f"{key}: {value:.1f}",
                    (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (255, 255, 255),
                    2
                )

                y += 25

            # ---------------------------------------
            # Save Dataset
            # ---------------------------------------

            if (
                recording
                and label is not None
                and (time.time() - last_saved) > save_interval
            ):

                if sample_filter.should_save(angles):

                    dataset.save_angles(
                        angles,
                        label
                    )

                    last_saved = time.time()

        # ---------------------------------------
        # Recording Status
        # ---------------------------------------

        if recording:
            rec_text = "REC : ON"
            rec_color = (0, 0, 255)
        else:
            rec_text = "REC : OFF"
            rec_color = (0, 255, 0)

        cv2.putText(
            frame,
            rec_text,
            (20, 420),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            rec_color,
            2
        )

        # ---------------------------------------
        # Sample Count
        # ---------------------------------------

        cv2.putText(
            frame,
            f"Samples : {dataset.angle_count}",
            (20, 455),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )

        # ---------------------------------------
        # Controls
        # ---------------------------------------

        cv2.putText(
            frame,
            "R = Start/Stop Recording",
            (20, 490),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Q = Quit",
            (20, 520),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 255),
            2
        )

        cv2.imshow("FitVisionAI Dataset Collector", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        elif key == ord("r"):

            recording = not recording

            if recording:
                print("\n========== RECORDING STARTED ==========\n")
            else:
                print("\n========== RECORDING STOPPED ==========\n")

    reader.release()

    detector.detector.close()

    print("\n========== DATASET COLLECTION FINISHED ==========")
    print(f"Total Samples Collected : {dataset.angle_count}")

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()