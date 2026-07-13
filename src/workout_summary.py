import cv2
import numpy as np


class WorkoutSummary:

    def show(
        self,
        reps,
        best_confidence,
        avg_confidence,
        session_time
    ):

        width = 900
        height = 600

        summary = np.ones((height, width, 3), dtype=np.uint8) * 255

        # -----------------------------
        # Title
        # -----------------------------
        cv2.putText(
            summary,
            "WORKOUT SUMMARY",
            (180, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.3,
            (0, 150, 0),
            3
        )

        # -----------------------------
        # Workout Statistics
        # -----------------------------
        y = 160

        items = [
            ("Exercise", "Squat"),
            ("Total Repetitions", str(reps)),
            ("Best Confidence", f"{best_confidence:.1f}%"),
            ("Average Confidence", f"{avg_confidence:.1f}%"),
            ("Workout Time", session_time)
        ]

        for title, value in items:

            cv2.putText(
                summary,
                title,
                (120, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 0),
                2
            )

            cv2.putText(
                summary,
                value,
                (500, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 120, 255),
                2
            )

            y += 70

        # -----------------------------
        # Performance Message
        # -----------------------------
        if reps == 0:
            message = "No Repetitions Completed"
            color = (0, 0, 255)          # Red

        elif reps < 5:
            message = "Good Start!"
            color = (0, 165, 255)        # Orange

        elif reps < 15:
            message = "Great Job!"
            color = (0, 180, 0)          # Green

        else:
            message = "Excellent Workout!"
            color = (255, 120, 0)        # Blue

        # Center the message
        (text_width, _), _ = cv2.getTextSize(
            message,
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            3
        )

        x = (width - text_width) // 2

        cv2.putText(
            summary,
            message,
            (x, 530),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            color,
            3
        )

        cv2.imshow("Workout Summary", summary)

        cv2.waitKey(0)

        cv2.destroyAllWindows()