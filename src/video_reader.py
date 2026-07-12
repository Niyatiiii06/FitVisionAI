import cv2


class VideoReader:

    def __init__(self, video_path):

        self.video_path = video_path

        self.cap = cv2.VideoCapture(video_path)

        if not self.cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        print("✅ Video opened successfully")

    def read_frame(self):

        success, frame = self.cap.read()

        if not success:
            return None

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return rgb_frame

    def release(self):
        self.cap.release()