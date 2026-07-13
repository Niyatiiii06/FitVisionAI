import cv2


class VideoReader:

    def __init__(self, source=0):

        self.cap = cv2.VideoCapture(source)

        if not self.cap.isOpened():
            raise Exception("Unable to open video source.")

    def read_frame(self):

        ret, frame = self.cap.read()

        if not ret:
            return None, None

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        return frame, rgb_frame

    def release(self):

        self.cap.release()