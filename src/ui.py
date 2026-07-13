import cv2


class UI:

    def draw_panel(self, frame, angle, count, stage):

        # ==========================
        # Background Panel
        # ==========================
        cv2.rectangle(
            frame,
            (10, 10),
            (360, 220),
            (35, 35, 35),
            -1
        )

        # ==========================
        # Border
        # ==========================
        cv2.rectangle(
            frame,
            (10, 10),
            (360, 220),
            (0, 255, 255),
            2
        )

        # ==========================
        # Title
        # ==========================
        cv2.putText(
            frame,
            "FITVISION AI",
            (25, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2
        )

        # Divider
        cv2.line(
            frame,
            (20, 60),
            (350, 60),
            (80, 80, 80),
            2
        )

        # ==========================
        # Exercise
        # ==========================
        cv2.putText(
            frame,
            "Exercise",
            (25, 95),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (180, 180, 180),
            2
        )

        cv2.putText(
            frame,
            "Squat",
            (190, 95),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        # ==========================
        # Reps
        # ==========================
        cv2.putText(
            frame,
            "Reps",
            (25, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (180, 180, 180),
            2
        )

        cv2.putText(
            frame,
            str(count),
            (190, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        # ==========================
        # Angle
        # ==========================
        cv2.putText(
            frame,
            "Angle",
            (25, 155),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (180, 180, 180),
            2
        )

        cv2.putText(
            frame,
            f"{int(angle)}°",
            (190, 155),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        # ==========================
        # Stage Color
        # ==========================
        if stage == "UP":
            stage_color = (0, 255, 0)      # Green

        elif stage == "DOWN":
            stage_color = (0, 0, 255)      # Red

        else:
            stage_color = (0, 255, 255)    # Yellow

        cv2.putText(
            frame,
            "Stage",
            (25, 185),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (180, 180, 180),
            2
        )

        cv2.putText(
            frame,
            stage,
            (190, 185),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            stage_color,
            2
        )

    # =======================================
    # Progress Bar
    # =======================================

    def draw_progress_bar(self, frame, angle):

        # Convert angle into squat depth percentage
        progress = int(((180 - angle) / (180 - 80)) * 100)

        # Keep value between 0 and 100
        progress = max(0, min(progress, 100))

        # Title
        cv2.putText(
            frame,
            "Squat Depth",
            (20, 245),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        # Background Bar
        cv2.rectangle(
            frame,
            (20, 260),
            (320, 290),
            (70, 70, 70),
            -1
        )

        # Filled Bar
        cv2.rectangle(
            frame,
            (20, 260),
            (20 + int(progress * 3), 290),
            (0, 255, 0),
            -1
        )

        # Border
        cv2.rectangle(
            frame,
            (20, 260),
            (320, 290),
            (255, 255, 255),
            2
        )

        # Percentage Text
        cv2.putText(
            frame,
            f"{progress}%",
            (330, 283),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )
    def draw_feedback(self, frame, angle, stage):

        # Determine feedback message
        if stage == "UP":
            message = "Stand Up"
            color = (0, 255, 0)          # Green

        elif angle > 120:
            message = "Go Lower"
            color = (0, 255, 255)        # Yellow

        elif 80 <= angle <= 120:
            message = "Perfect Depth"
            color = (0, 255, 0)          # Green

        else:
            message = "Too Low"
            color = (0, 0, 255)          # Red

        # Background box
        cv2.rectangle(
            frame,
            (10, 320),
            (360, 390),
            (35, 35, 35),
            -1
        )

        # Border
        cv2.rectangle(
            frame,
            (10, 320),
            (360, 390),
            color,
            2
        )

        # Heading
        cv2.putText(
            frame,
            "Feedback",
            (25, 345),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        # Message
        cv2.putText(
            frame,
            message,
            (25, 375),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )