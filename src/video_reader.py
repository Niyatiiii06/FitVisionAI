import cv2


class VideoReader:

    def __init__(self, source=0):

        self.cap = cv2.VideoCapture(source)

        if not self.cap.isOpened():
            raise Exception("Unable to open source.")

        # Lower resolution = faster inference
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def read_frame(self):

        ret, frame = self.cap.read()

        if not ret:
            return None, None

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        return frame, rgb

    def release(self):

        self.cap.release()