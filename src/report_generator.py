import os
from datetime import datetime


class ReportGenerator:

    def __init__(self):
        os.makedirs("reports", exist_ok=True)

    def generate(
        self,
        reps,
        best_confidence,
        avg_confidence,
        session_time
    ):

        now = datetime.now()

        filename = now.strftime(
            "reports/workout_%Y-%m-%d_%H-%M-%S.txt"
        )

        if reps == 0:
            performance = "No Repetitions Completed"

        elif reps < 5:
            performance = "Good Start"

        elif reps < 15:
            performance = "Great Job"

        else:
            performance = "Excellent Workout"

        report = f"""
=========================================
          FITVISION AI REPORT
=========================================

Date                : {now.strftime('%d-%m-%Y')}
Time                : {now.strftime('%H:%M:%S')}

Exercise            : Squat

Total Repetitions   : {reps}

Best Confidence     : {best_confidence:.1f}%
Average Confidence  : {avg_confidence:.1f}%

Workout Time        : {session_time}

Performance         : {performance}

=========================================
"""

        with open(filename, "w", encoding="utf-8") as file:
            file.write(report)

        print(f"\n✅ Workout report saved to:\n{filename}")