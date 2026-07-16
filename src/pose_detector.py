import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from src.angle_calculator import AngleCalculator


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
    # Joint Angles
    # --------------------------------------------------

    def get_joint_angles(self, results):

        if not results.pose_landmarks:
            return None

        landmarks = results.pose_landmarks[0]

        def point(index):
            return (
                landmarks[index].x,
                landmarks[index].y
            )

        def angle(a, b, c):
            return AngleCalculator.calculate_angle(
                point(a),
                point(b),
                point(c)
            )

        # ==========================
        # Squat Angles
        # ==========================

        left_knee = angle(23, 25, 27)
        right_knee = angle(24, 26, 28)

        left_hip = angle(11, 23, 25)
        right_hip = angle(12, 24, 26)

        left_ankle = angle(25, 27, 31)
        right_ankle = angle(26, 28, 32)

        # ==========================
        # Push-up Angles
        # ==========================

        left_elbow = angle(11, 13, 15)
        right_elbow = angle(12, 14, 16)

        left_shoulder = angle(13, 11, 23)
        right_shoulder = angle(14, 12, 24)

        left_body = angle(11, 23, 27)
        right_body = angle(12, 24, 28)

        return {

            # ---------- Squat ----------

            "left_knee": round(left_knee, 1),
            "right_knee": round(right_knee, 1),

            "left_hip": round(left_hip, 1),
            "right_hip": round(right_hip, 1),

            "left_ankle": round(left_ankle, 1),
            "right_ankle": round(right_ankle, 1),

            # ---------- Push-up ----------

            "left_elbow": round(left_elbow, 1),
            "right_elbow": round(right_elbow, 1),

            "left_shoulder": round(left_shoulder, 1),
            "right_shoulder": round(right_shoulder, 1),

            "left_body": round(left_body, 1),
            "right_body": round(right_body, 1)

        }

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

            (11, 12),

            (11, 13),
            (13, 15),

            (12, 14),
            (14, 16),

            (11, 23),
            (12, 24),
            (23, 24),

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
        # Left Leg Highlight
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
        # Normal Joints
        # ===========================

        normal_joints = [

            11, 12,
            13, 14,
            15, 16,
            24,
            26,
            28

        ]

        for joint in normal_joints:

            cv2.circle(
                frame,
                points[joint],
                6,
                (255, 255, 255),
                -1
            )

        # ===========================
        # Highlight Left Leg
        # ===========================

        cv2.circle(
            frame,
            points[23],
            9,
            (0, 255, 0),
            -1
        )

        cv2.circle(
            frame,
            points[25],
            10,
            (0, 0, 255),
            -1
        )

        cv2.circle(
            frame,
            points[27],
            9,
            (255, 0, 0),
            -1
        )

        return frame