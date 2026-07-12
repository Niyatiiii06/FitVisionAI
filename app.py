from src.video_reader import VideoReader
from src.pose_detector import PoseDetector


def main():

    reader = VideoReader("data/videos/squat.mp4")

    detector = PoseDetector()

    frame = reader.read_frame()

    if frame is not None:

        results = detector.detect(frame)

        print(type(results))

    reader.release()


if __name__ == "__main__":
    main()