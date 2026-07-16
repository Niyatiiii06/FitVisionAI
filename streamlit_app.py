import os
import tempfile
import streamlit as st

from src.streamlit_processor import StreamlitProcessor

st.set_page_config(
    page_title="FitVisionAI",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# Custom CSS — Force Dark Mode
# ======================================================
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background-color: #0E1117;
}

[data-testid="stSidebar"] {
    background-color: #161A22;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3, h4, h5, h6 {
    color: white;
}

p, label {
    color: #D6D6D6;
}

.metric-card {
    background: #1E1E1E;
    padding: 15px;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# Better Hero Section
# ======================================================
st.markdown("""
<h1 style='text-align:center;color:#00E5FF;'>
🏋️ FitVisionAI
</h1>

<h3 style='text-align:center;color:white;'>
AI-Powered Workout Analysis
</h3>

<p style='text-align:center;font-size:18px;'>
Analyze Squats and Push-ups using
<b>MediaPipe</b>,
<b>TensorFlow ANN</b>,
and
<b>OpenCV</b>.
</p>
""", unsafe_allow_html=True)

st.divider()
st.markdown("## 🚀 Features")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info("🧠 Pose Detection\n\nMediaPipe")

with c2:
    st.info("🤖 Deep Learning\n\nTensorFlow ANN")

with c3:
    st.info("📄 PDF Reports")

with c4:
    st.info("📈 Workout Analytics")

st.divider()

# ======================================================
# Sidebar
# ======================================================
if os.path.exists("assets/logo.png"):
    st.sidebar.image("assets/logo.png", width=120)

st.sidebar.title("🏋️ FitVisionAI")
st.sidebar.markdown("---")

exercise_display = st.sidebar.selectbox(
    "Exercise",
    [
        "Select Exercise",
        "Squat",
        "Push-up"
    ]
)

if exercise_display == "Squat":
    exercise = "squat"

elif exercise_display == "Push-up":
    exercise = "pushup"

else:
    exercise = ""

mode = st.sidebar.radio(
    "Mode",
    [
        "📁 Upload Video (Recommended)",
        "🎥 Live Webcam (Experimental)"
    ]
)

if "Webcam" in mode:

    st.warning(
    "⚠️ Webcam Mode (Experimental)\n\n"
    "• Real-time webcam analysis is currently disabled in the web application.\n"
    "• The core pose estimation and exercise analysis pipeline is fully supported through video uploads.\n"
    "• Upload Video mode provides the best performance and most reliable results."
    )

    st.stop()

st.sidebar.markdown("---")

st.sidebar.success("### Recommended Workflow")

st.sidebar.write(
"""
1. Select Exercise

2. Upload Workout Video

3. Click **Start Analysis**

4. Download PDF Report
"""
)

# ======================================================
# Better Upload Area
# ======================================================
st.markdown("### 📁 Upload Workout Video")

uploaded_video = None

if "Upload" in mode:
    uploaded_video = st.file_uploader(
        "",
        type=["mp4", "avi", "mov"]
    )

# ======================================================
# Layout
# ======================================================
left, right = st.columns([2, 1])

# ======================================================
# Left Column
# ======================================================
with left:
    st.subheader("Workout Video")
    video_placeholder = st.empty()

    if uploaded_video:
        video_placeholder.video(uploaded_video)
    else:
        video_placeholder.markdown("""
        <div style='
        padding:60px;
        border:2px dashed #555;
        border-radius:15px;
        text-align:center;
        font-size:20px;
        color:#AAA;
        '>
        📹

        Upload a workout video to begin analysis
        </div>
        """, unsafe_allow_html=True)

# ======================================================
# Right Column
# ======================================================
with right:
    st.subheader("📊 Live Metrics")

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Exercise", exercise_display)
        st.metric("🔢 Reps", 0)
        st.metric("📈 Confidence", "0%")

    with c2:
        st.metric("⭐ Score", "0/100")
        st.metric("🏋️ State", "Waiting")
        st.metric("💬 Feedback", "Ready")

# ======================================================
# Analyze Button
# ======================================================
st.divider()

analyze = st.button(
    "🚀 Start Analysis",
    type="primary",
    use_container_width=True
)

if analyze:

    if exercise == "":
        st.warning("Please select an exercise.")
        st.stop()

    if uploaded_video is None:
        st.warning("Please upload a workout video.")
        st.stop()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp4"
    ) as temp:
        temp.write(uploaded_video.read())
        video_path = temp.name

    processor = StreamlitProcessor(exercise)
    progress = st.progress(0)
    status = st.empty()
    video_placeholder = left.empty()
    metrics_placeholder = right.empty()

    # ======================================================
    # Better Progress Messages
    # ======================================================
    def update_progress(value):
        progress.progress(value)
        if value < 0.3:
            status.info("🔍 Detecting Pose...")
        elif value < 0.6:
            status.info("🧠 Running Deep Learning Model...")
        elif value < 0.9:
            status.info("📊 Calculating Workout Metrics...")
        else:
            status.info("📄 Generating PDF Report...")

    def update_frame(frame, reps, confidence, score, feedback):
        video_placeholder.image(
            frame,
            channels="BGR",
            use_container_width=True
        )

        with metrics_placeholder.container():
            c1, c2 = st.columns(2)

            with c1:
                st.metric("🏋 Exercise", exercise_display)
                st.metric("🔢 Reps", reps)
                st.metric("📈 Confidence", f"{confidence:.1f}%")

            with c2:
                st.metric("⭐ Score", score)
                if len(feedback):
                    st.metric("💬 Feedback", feedback[0])
                else:
                    st.metric("💬 Feedback", "Excellent")

    results = processor.process(
        video_path,
        frame_callback=update_frame,
        progress_callback=update_progress
    )

    # ======================================================
    # Delete Temporary Video
    # ======================================================
    if os.path.exists(video_path):
        os.remove(video_path)

    status.success("✅ Analysis Complete!")
    st.balloons()
    progress.progress(100)

    st.divider()
    st.subheader("🏆 Workout Summary")

    # ======================================================
    # Show Workout Grade
    # ======================================================
    score = results["score"]
    if score >= 95:
        grade = "A+"
    elif score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    else:
        grade = "D"

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Reps", results["repetitions"])
    c2.metric("Score", results["score"])
    c3.metric("Grade", grade)
    c4.metric("Confidence", f"{results['average_confidence']}%")

    # ======================================================
    # Handle Empty Recommendations
    # ======================================================
    st.subheader("💡 AI Recommendations")
    if results["feedback"]:
        for tip in results["feedback"]:
            st.success("✔ " + tip)
    else:
        st.success("🏆 Excellent posture maintained throughout the workout.")

    # ======================================================
    # Download Report
    # ======================================================
    st.subheader("📄 Download Report")
    with open(results["pdf"], "rb") as pdf:
        st.download_button(
            "📄 Download PDF Report",
            pdf,
            file_name="FitVisionAI_Report.pdf",
            mime="application/pdf"
        )

    # ======================================================
    # Analytics with Captions
    # ======================================================
    st.divider()
    st.subheader("📊 Workout Analytics")

    c1, c2 = st.columns(2)

    with c1:
        st.image(
            results["analytics"]["reps"],
            caption="Workout Repetitions"
        )

        st.image(
            results["analytics"]["confidence"],
            caption="Confidence Trend"
        )

    with c2:
        st.image(
            results["analytics"]["score"],
            caption="Workout Score"
        )

# ======================================================
# Footer
# ======================================================

st.divider()

st.caption(
    "Built with ❤️ using TensorFlow, MediaPipe, OpenCV and Streamlit"
)