# 🏋️ FitVisionAI

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue)

![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)

![MediaPipe](https://img.shields.io/badge/MediaPipe-Pose-green)

![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-red)

![License](https://img.shields.io/badge/License-MIT-yellow)

</p>

---

## 📌 Overview

FitVisionAI is an AI-powered fitness analysis system that evaluates exercise posture using **MediaPipe Pose Estimation**, **TensorFlow Artificial Neural Networks**, and **OpenCV**.

The application detects body landmarks, classifies exercise stages, counts repetitions, evaluates posture quality, provides live feedback, and generates workout reports with analytics.

---

## ✨ Features

- ✅ Squat Detection
- ✅ Push-up Detection
- ✅ Real-time Pose Estimation
- ✅ ANN-based Exercise Classification
- ✅ Joint Angle Calculation
- ✅ Repetition Counter
- ✅ Workout Score
- ✅ Live Confidence Meter
- ✅ Posture Feedback
- ✅ Workout Summary
- ✅ PDF Workout Report
- ✅ Workout History
- ✅ Analytics Dashboard

---

## 🖥️ Screenshots

### Squat Detection

![Squat](assets/screenshots/02_squat_detection.png)

---

### Push-up Detection

![Pushup](assets/screenshots/03_pushup_detection.png)

---

### Dashboard

![Dashboard](assets/screenshots/04_dashboard.png)

---

### PDF Report

![PDF](assets/screenshots/06_pdf_report.png)

---

## ⚙️ Project Architecture

```
Video / Webcam
        │
        ▼
Video Reader
        │
        ▼
MediaPipe Pose Detection
        │
        ▼
Landmark Extraction
        │
        ▼
Joint Angle Calculator
        │
        ├──────────────► ANN Classifier
        │                     │
        ▼                     ▼
Rep Counter          Exercise State
        │                     │
        └──────────────┬──────┘
                       ▼
             Posture Evaluation
                       ▼
              Workout Dashboard
                       ▼
      Report + Analytics Generation
```

---

## 🛠️ Tech Stack

- Python
- TensorFlow
- OpenCV
- MediaPipe
- NumPy
- Pandas
- Matplotlib
- Scikit-learn
- ReportLab
- Joblib

---

## 📂 Folder Structure

```text
FitVisionAI
│
├── app.py
├── src/
├── models/
├── data/
├── reports/
├── assets/
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

```bash
git clone https://github.com/YOUR_USERNAME/FitVisionAI.git

cd FitVisionAI

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

---

## ▶️ Run

```bash
python app.py
```

---

## 📈 Results

| Exercise | Accuracy |
|-----------|----------|
| Squat ANN | **99%** |
| Push-up ANN | **(Add your result here)** |

---

## 📄 License

This project is licensed under the MIT License.

---

## 👩‍💻 Author

**Niyati Singh**

AI & Data Science Undergraduate

Passionate about Computer Vision, Machine Learning and AI.
