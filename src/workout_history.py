import os
import csv
from datetime import datetime


class WorkoutHistory:

    def __init__(self):

        os.makedirs("reports", exist_ok=True)

        self.file = "reports/workout_history.csv"

        if not os.path.exists(self.file):

            with open(self.file, "w", newline="", encoding="utf-8") as f:

                writer = csv.writer(f)

                writer.writerow([
                    "Date",
                    "Time",
                    "Exercise",
                    "Repetitions",
                    "Workout Score",
                    "Grade",
                    "Best Confidence",
                    "Average Confidence",
                    "Duration"
                ])

    def save(
        self,
        exercise,
        reps,
        posture_score,
        best_confidence,
        avg_confidence,
        session_time
    ):

        if posture_score >= 95:
            grade = "A+"

        elif posture_score >= 90:
            grade = "A"

        elif posture_score >= 80:
            grade = "B"

        elif posture_score >= 70:
            grade = "C"

        elif posture_score >= 60:
            grade = "D"

        else:
            grade = "F"

        now = datetime.now()

        exercise_name = (
            "Push-up"
            if exercise == "pushup"
            else "Squat"
        )

        with open(self.file, "a", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)

            writer.writerow([
                now.strftime("%d-%m-%Y"),
                now.strftime("%H:%M:%S"),
                exercise_name,
                reps,
                posture_score,
                grade,
                f"{best_confidence:.1f}",
                f"{avg_confidence:.1f}",
                session_time
            ])

        print("\nWorkout history updated.")