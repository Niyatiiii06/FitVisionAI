import os
import pandas as pd
import matplotlib.pyplot as plt


class WorkoutAnalytics:

    def __init__(self):

        os.makedirs("reports", exist_ok=True)

        self.file = "reports/workout_history.csv"

    def generate(self):

        if not os.path.exists(self.file):
            return

        df = pd.read_csv(self.file)

        if len(df) == 0:
            return

        # -----------------------------
        # Repetitions Trend
        # -----------------------------

        plt.figure(figsize=(8,4))

        plt.plot(
            range(1, len(df)+1),
            df["Repetitions"],
            marker="o",
            linewidth=2
        )

        plt.title("Workout Repetitions")

        plt.xlabel("Workout Session")

        plt.ylabel("Repetitions")

        plt.grid(True)

        plt.tight_layout()

        plt.savefig("reports/reps_history.png")

        plt.close()

        # -----------------------------
        # Workout Score
        # -----------------------------

        plt.figure(figsize=(8,4))

        plt.plot(
            range(1, len(df)+1),
            df["Workout Score"],
            marker="o",
            linewidth=2
        )

        plt.title("Workout Score History")

        plt.xlabel("Workout Session")

        plt.ylabel("Score")

        plt.grid(True)

        plt.tight_layout()

        plt.savefig("reports/score_history.png")

        plt.close()

        # -----------------------------
        # Confidence
        # -----------------------------

        plt.figure(figsize=(8,4))

        plt.plot(
            range(1, len(df)+1),
            df["Average Confidence"],
            marker="o",
            linewidth=2
        )

        plt.title("Average Confidence")

        plt.xlabel("Workout Session")

        plt.ylabel("Confidence (%)")

        plt.grid(True)

        plt.tight_layout()

        plt.savefig("reports/confidence_history.png")

        plt.close()

    
        print("\nAnalytics Generated Successfully.")
