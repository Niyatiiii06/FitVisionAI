import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


class ReportGenerator:

    def __init__(self):
        os.makedirs("reports", exist_ok=True)

    def generate(
        self,
        exercise,
        reps,
        posture_score,
        best_confidence,
        avg_confidence,
        session_time
    ):

        now = datetime.now()

        filename = now.strftime(
            "reports/FitVisionAI_%Y-%m-%d_%H-%M-%S.pdf"
        )

        exercise_name = (
            "Push-up"
            if exercise == "pushup"
            else "Squat"
        )

        # -------------------------------
        # Grade
        # -------------------------------

        if posture_score >= 95:
            grade = "A+"
            grade_color = "green"

        elif posture_score >= 90:
            grade = "A"
            grade_color = "green"

        elif posture_score >= 80:
            grade = "B"
            grade_color = "blue"

        elif posture_score >= 70:
            grade = "C"
            grade_color = "orange"

        else:
            grade = "D"
            grade_color = "red"

        # -------------------------------
        # Performance
        # -------------------------------

        if reps == 0:
            performance = "No Workout Completed"

        elif reps < 5:
            performance = "Good Start"

        elif reps < 15:
            performance = "Great Job"

        elif reps < 30:
            performance = "Excellent Workout"

        else:
            performance = "Outstanding Performance"

        # -------------------------------
        # Recommendation
        # -------------------------------

        if posture_score >= 90:

            recommendations = [

                "Excellent posture maintained.",
                "Keep the same consistency.",
                "Maintain full range of motion."

            ]

        elif posture_score >= 75:

            recommendations = [

                "Lower a little more.",
                "Maintain body alignment.",
                "Control movement speed."

            ]

        else:

            recommendations = [

                "Practice proper posture.",
                "Reduce speed and focus on form.",
                "Keep your core engaged."

            ]

        doc = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        title = styles["Heading1"]
        title.alignment = TA_CENTER
        title.textColor = colors.darkblue

        heading = styles["Heading2"]

        story = []

        # ==================================================
        # TITLE
        # ==================================================

        story.append(Paragraph("FitVisionAI", title))

        story.append(
            Paragraph(
                "<b>AI Powered Exercise Analysis Report</b>",
                styles["Heading3"]
            )
        )

        story.append(Spacer(1, 20))

        # ==================================================
        # BASIC DETAILS
        # ==================================================

        info = [

            ["Exercise", exercise_name],
            ["Date", now.strftime("%d-%m-%Y")],
            ["Time", now.strftime("%H:%M:%S")]

        ]

        table = Table(info, colWidths=[170,250])

        table.setStyle(TableStyle([

            ("BACKGROUND",(0,0),(-1,-1),colors.whitesmoke),
            ("GRID",(0,0),(-1,-1),1,colors.grey),
            ("BOTTOMPADDING",(0,0),(-1,-1),8)

        ]))

        story.append(table)

        story.append(Spacer(1,20))

        # ==================================================
        # SUMMARY
        # ==================================================

        story.append(
            Paragraph("Workout Summary", heading)
        )

        summary = [

            ["Total Repetitions", reps],
            ["Workout Score", f"{posture_score}/100"],
            ["Workout Grade", f"<font color='{grade_color}'><b>{grade}</b></font>"]

        ]

        table = Table(summary, colWidths=[170,250])

        table.setStyle(TableStyle([

            ("BACKGROUND",(0,0),(-1,-1),colors.beige),
            ("GRID",(0,0),(-1,-1),1,colors.black),
            ("BOTTOMPADDING",(0,0),(-1,-1),8)

        ]))

        story.append(table)

        story.append(Spacer(1,20))

        # ==================================================
        # PERFORMANCE
        # ==================================================

        story.append(
            Paragraph("Performance Metrics", heading)
        )

        metrics = [

            ["Best Confidence", f"{best_confidence:.1f}%"],
            ["Average Confidence", f"{avg_confidence:.1f}%"],
            ["Workout Duration", session_time]

        ]

        table = Table(metrics, colWidths=[170,250])

        table.setStyle(TableStyle([

            ("BACKGROUND",(0,0),(-1,-1),colors.lightgrey),
            ("GRID",(0,0),(-1,-1),1,colors.black),
            ("BOTTOMPADDING",(0,0),(-1,-1),8)

        ]))

        story.append(table)

        story.append(Spacer(1,20))

        # ==================================================
        # PERFORMANCE
        # ==================================================

        story.append(
            Paragraph("Performance", heading)
        )

        story.append(
            Paragraph(
                f"<b>{performance}</b>",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1,15))

        # ==================================================
        # RECOMMENDATIONS
        # ==================================================

        story.append(
            Paragraph("Recommendations", heading)
        )

        for tip in recommendations:

            story.append(
                Paragraph(
                    f"• {tip}",
                    styles["BodyText"]
                )
            )

        story.append(Spacer(1,25))

        # ==================================================
        # FOOTER
        # ==================================================

        story.append(
            Paragraph(
                "<b><font color='darkgreen'>Generated Automatically by FitVisionAI</font></b>",
                styles["Heading3"]
            )
        )

        doc.build(story)

        print(f"\nPDF Report Saved Successfully!\n{filename}")