import cv2


class UI:

    def __init__(self):
        pass

    def draw_panel(
        self,
        frame,
        state,
        confidence,
        count,
        best_confidence,
        avg_confidence,
        session_time,
        fps
    ):

        height, width = frame.shape[:2]

        # ===========================
        # Right Side Panel
        # ===========================
        cv2.rectangle(
            frame,
            (width - 270, 0),
            (width, height),
            (40, 40, 40),
            -1
        )

        # ===========================
        # Title
        # ===========================
        cv2.putText(
            frame,
            "FitVisionAI",
            (width - 245, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        # ===========================
        # Exercise
        # ===========================
        cv2.putText(
            frame,
            "Exercise",
            (width - 245, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Squat",
            (width - 245, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        # ===========================
        # State
        # ===========================
        cv2.putText(
            frame,
            "State",
            (width - 245, 170),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        state_color = (0, 255, 0) if state == "UP" else (0, 0, 255)

        cv2.putText(
            frame,
            state,
            (width - 245, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            state_color,
            2
        )

        # ===========================
        # Confidence
        # ===========================
        cv2.putText(
            frame,
            "Confidence",
            (width - 245, 250),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"{confidence:.1f}%",
            (width - 245, 280),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

        # ===========================
        # Confidence Bar
        # ===========================
        cv2.rectangle(
            frame,
            (width - 245, 300),
            (width - 45, 320),
            (80, 80, 80),
            -1
        )

        bar_width = int((confidence / 100) * 200)

        cv2.rectangle(
            frame,
            (width - 245, 300),
            (width - 245 + bar_width, 320),
            (0, 255, 0),
            -1
        )

        # ===========================
        # Repetitions
        # ===========================
        cv2.putText(
            frame,
            "Repetitions",
            (width - 245, 370),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            str(count),
            (width - 245, 410),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.3,
            (0, 255, 255),
            3
        )

        # ===========================
        # Divider
        # ===========================
        cv2.line(
            frame,
            (width - 250, 445),
            (width - 20, 445),
            (120, 120, 120),
            1
        )

        # ===========================
        # Session Statistics
        # ===========================
        cv2.putText(
            frame,
            "Session Stats",
            (width - 245, 480),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Best : {best_confidence:.1f}%",
            (width - 245, 520),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Average : {avg_confidence:.1f}%",
            (width - 245, 555),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Time : {session_time}",
            (width - 245, 590),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"FPS : {fps:.1f}",
            (width - 245, 625),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0),
            2
        )