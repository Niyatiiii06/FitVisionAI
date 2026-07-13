import cv2


class UI:

    def draw_panel(self, frame, angle, count, stage):

        # Background Panel
        cv2.rectangle(frame, (10, 10), (350, 170), (40, 40, 40), -1)

        # Title
        cv2.putText(
            frame,
            "FITVISION AI",
            (25, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        # Exercise
        cv2.putText(
            frame,
            "Exercise : Squat",
            (25, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        # Reps
        cv2.putText(
            frame,
            f"Reps : {count}",
            (25, 105),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        # Angle
        cv2.putText(
            frame,
            f"Angle : {int(angle)}",
            (25, 135),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        # Stage
        cv2.putText(
            frame,
            f"Stage : {stage}",
            (25, 165),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )