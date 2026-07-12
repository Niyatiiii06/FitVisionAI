import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class PoseDetector:

    def __init__(self):

        base_options = python.BaseOptions(
            model_asset_path="data/models/pose_landmarker.task"
        )

        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE
        )

        self.detector = vision.PoseLandmarker.create_from_options(options)

        print("✅ PoseDetector loaded successfully")

    def detect(self, rgb_frame):

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        results = self.detector.detect(mp_image)

        return results