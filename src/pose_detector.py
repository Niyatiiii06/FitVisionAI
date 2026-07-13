import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class PoseDetector:

    def __init__(self):

        model_path = "data/models/pose_landmarker.task"

        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            output_segmentation_masks=False,
            num_poses=1
        )

        self.detector = vision.PoseLandmarker.create_from_options(options)

    # --------------------------------------------------
    # Pose Detection
    # --------------------------------------------------

    def detect(self, rgb_frame):

        image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        results = self.detector.detect(image)

        return results

    # --------------------------------------------------
    # Draw Skeleton
    # --------------------------------------------------

    def draw_landmarks(self, frame, results):

        if not results.pose_landmarks:
            return frame

        landmarks = results.pose_landmarks[0]

        h, w, _ = frame.shape

        points = []

        for landmark in landmarks:
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            points.append((x, y))

        # ===========================
        # White Skeleton
        # ===========================

        white_connections = [

            # Shoulders
            (11, 12),

            # Left Arm
            (11, 13),
            (13, 15),

            # Right Arm
            (12, 14),
            (14, 16),

            # Torso
            (11, 23),
            (12, 24),
            (23, 24),

            # Right Leg
            (24, 26),
            (26, 28)

        ]

        for start, end in white_connections:

            cv2.line(
                frame,
                points[start],
                points[end],
                (255, 255, 255),
                3
            )

        # ===========================
        # Highlight Left Leg
        # ===========================

        cv2.line(
            frame,
            points[23],
            points[25],
            (0, 255, 0),
            5
        )

        cv2.line(
            frame,
            points[25],
            points[27],
            (0, 255, 0),
            5
        )

        # ===========================
        # Draw White Joints
        # ===========================

        normal_joints = [
            11,12,
            13,14,
            15,16,
            24,
            26,
            28
        ]

        for joint in normal_joints:

            cv2.circle(
                frame,
                points[joint],
                6,
                (255,255,255),
                -1
            )

        # ===========================
        # Highlight Tracked Joints
        # ===========================

        # Hip (Green)
        cv2.circle(
            frame,
            points[23],
            9,
            (0,255,0),
            -1
        )

        # Knee (Red)
        cv2.circle(
            frame,
            points[25],
            10,
            (0,0,255),
            -1
        )

        # Ankle (Blue)
        cv2.circle(
            frame,
            points[27],
            9,
            (255,0,0),
            -1
        )

        return frame