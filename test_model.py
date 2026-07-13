from src.video_reader import VideoReader
from src.pose_detector import PoseDetector
from src.model_predictor import ModelPredictor


def main():

    reader = VideoReader("data/videos/squat.mp4")

    detector = PoseDetector()

    predictor = ModelPredictor()

    while True:

        frame, rgb_frame = reader.read_frame()

        if frame is None:
            break

        results = detector.detect(rgb_frame)

        if results.pose_landmarks:

            landmarks = results.pose_landmarks[0]

            state, confidence = predictor.predict(landmarks)

            print(
                f"Prediction: {state} | Confidence: {confidence:.3f}"
            )


if __name__ == "__main__":
    main()