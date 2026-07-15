import cv2


class UI:

    def __init__(self):
        pass

    # ==========================================================
    # Helper: Confidence Badge (Excellent / Good / Low)
    # ==========================================================
    def get_confidence_badge(self, confidence):

        if confidence >= 85:
            return "EXCELLENT", (0, 255, 0)

        elif confidence >= 60:
            return "GOOD", (0, 255, 255)

        else:
            return "LOW", (0, 0, 255)

    # ==========================================================
    # Helper: Posture Score Color
    # ==========================================================
    def get_score_color(self, score):

        if score >= 85:
            return (0, 255, 0)

        elif score >= 60:
            return (0, 255, 255)

        else:
            return (0, 0, 255)

    # ==========================================================
    # Helper: FPS Color
    # ==========================================================
    def get_fps_color(self, fps):

        if fps >= 20:
            return (0, 255, 0)

        elif fps >= 12:
            return (0, 255, 255)

        else:
            return (0, 0, 255)

    # ==========================================================
    # Helper: Workout Grade
    # ==========================================================
    def get_grade(self, score):

        if score >= 95:
            return "A+"

        elif score >= 85:
            return "A"

        elif score >= 75:
            return "B"

        elif score >= 60:
            return "C"

        else:
            return "D"

    # ==========================================================
    # Main Panel
    # ==========================================================
    def draw_panel(
        self,
        frame,
        exercise,
        state,
        confidence,
        count,
        best_confidence,
        avg_confidence,
        session_time,
        fps,
        posture_score,
        feedback,
        angles
    ):

        height, width = frame.shape[:2]

        panel_x = width - 320

        # ===========================
        # Right Panel Background
        # ===========================
        cv2.rectangle(
            frame,
            (panel_x, 0),
            (width, height),
            (25, 25, 25),
            -1
        )

        # Accent strip on panel edge
        cv2.rectangle(
            frame,
            (panel_x, 0),
            (panel_x + 4, height),
            (0, 255, 255),
            -1
        )

        x = width - 300
        y = 30

        # ===========================
        # Title
        # ===========================
        cv2.putText(
            frame,
            "FitVisionAI",
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.85,
            (0, 255, 255),
            2
        )

        y += 30

        cv2.line(
            frame,
            (x, y),
            (width - 20, y),
            (80, 80, 80),
            1
        )

        y += 30

        # ===========================
        # Exercise + Status
        # ===========================
        exercise_name = (
            "Push-up"
            if exercise == "pushup"
            else "Squat"
        )

        tracking = state not in ("----", None)

        status_text = "TRACKING" if tracking else "NO PERSON"
        status_color = (0, 255, 0) if tracking else (0, 0, 255)

        cv2.putText(
            frame,
            f"{exercise_name}",
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        cv2.circle(frame, (x + 250, y - 6), 6, status_color, -1)

        cv2.putText(
            frame,
            status_text,
            (x + 130, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            status_color,
            1
        )

        y += 45

        # ===========================
        # Big UP / DOWN Indicator
        # ===========================
        pose_color = (0, 255, 0) if state == "UP" else (0, 100, 255)

        cv2.rectangle(
            frame,
            (x - 5, y - 30),
            (x + 250, y + 15),
            (45, 45, 45),
            -1
        )

        cv2.putText(
            frame,
            state if state != "----" else "-----",
            (x + 10, y + 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.1,
            pose_color,
            3
        )

        y += 55

        # ===========================
        # Confidence Badge
        # ===========================
        badge_text, badge_color = self.get_confidence_badge(confidence)

        cv2.putText(
            frame,
            f"Confidence : {confidence:.1f}%",
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.58,
            (255, 255, 255),
            2
        )

        cv2.rectangle(
            frame,
            (x + 195, y - 18),
            (x + 260, y + 4),
            badge_color,
            -1
        )

        cv2.putText(
            frame,
            badge_text[:4],
            (x + 199, y - 3),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.38,
            (0, 0, 0),
            1
        )

        y += 30

        bar_width = int((max(0, min(confidence, 100)) / 100) * 260)

        cv2.rectangle(
            frame,
            (x, y),
            (x + 260, y + 14),
            (70, 70, 70),
            -1
        )

        cv2.rectangle(
            frame,
            (x, y),
            (x + bar_width, y + 14),
            badge_color,
            -1
        )

        y += 40

        # ===========================
        # Reps + Progress Bar
        # ===========================
        rep_target = 10
        reps_in_set = count % rep_target if rep_target else count

        cv2.putText(
            frame,
            f"Reps : {count}",
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.85,
            (0, 255, 255),
            2
        )

        y += 20

        rep_bar_width = int((reps_in_set / rep_target) * 260)

        cv2.rectangle(
            frame,
            (x, y),
            (x + 260, y + 12),
            (70, 70, 70),
            -1
        )

        cv2.rectangle(
            frame,
            (x, y),
            (x + rep_bar_width, y + 12),
            (0, 255, 255),
            -1
        )

        y += 35

        # ===========================
        # Posture Score + Grade
        # ===========================
        score_color = self.get_score_color(posture_score)
        grade = self.get_grade(posture_score)

        cv2.putText(
            frame,
            f"Score : {posture_score}/100",
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            score_color,
            2
        )

        cv2.rectangle(
            frame,
            (x + 220, y - 20),
            (x + 265, y + 6),
            score_color,
            -1
        )

        cv2.putText(
            frame,
            grade,
            (x + 226, y - 3),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 0, 0),
            2
        )

        y += 40

        # ===========================
        # Angles
        # ===========================
        cv2.putText(
            frame,
            "Joint Angles",
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (200, 200, 200),
            2
        )

        y += 26

        for name, value in angles.items():

            text = f"{name.replace('_', ' ').title()} : {value:.1f}"

            cv2.putText(
                frame,
                text,
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.48,
                (220, 220, 220),
                1
            )

            y += 22

        y += 10

        # ===========================
        # Feedback
        # ===========================
        cv2.putText(
            frame,
            "Feedback",
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2
        )

        y += 26

        for msg in feedback:

            cv2.putText(
                frame,
                f"- {msg}",
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.48,
                (0, 255, 0),
                1
            )

            y += 20

        y += 10

        # ===========================
        # FPS (color-coded)
        # ===========================
        fps_color = self.get_fps_color(fps)

        cv2.putText(
            frame,
            f"FPS : {fps:.1f}",
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            fps_color,
            1
        )

        y += 22

        # ===========================
        # Session Stats
        # ===========================
        cv2.putText(
            frame,
            f"Best : {best_confidence:.1f}%",
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (255, 255, 0),
            1
        )

        y += 20

        cv2.putText(
            frame,
            f"Average : {avg_confidence:.1f}%",
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (0, 255, 0),
            1
        )

        y += 20

        cv2.putText(
            frame,
            f"Time : {session_time}",
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (255, 255, 255),
            1
        )