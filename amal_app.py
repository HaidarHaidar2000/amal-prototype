
import streamlit as st
from PIL import Image
import time
from utils import generate_docx

st.set_page_config(page_title="AMAL – Radiology AI", layout="centered", page_icon="🫁")

# Centered logo and title using HTML
st.markdown(
    """
    <div style='text-align: center;'>
        <img src='https://raw.githubusercontent.com/HaidarHaidar2000/amal-prototype/main/logo.png' width='120'>
        <h1 style='margin-bottom: 0;'>AMAL</h1>
        <h4 style='margin-top: 0;'>AI Radiology Assistant</h4>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")
st.header("Patient Information")

with st.form("patient_form"):
    name = st.text_input("Full Name *")
    age = st.number_input("Age *", min_value=0, format="%d")
    gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
    symptoms = st.text_area("Symptoms")
    physical_activity = st.selectbox("Physical Activity Level", ["None", "Low", "Moderate", "High"])
    exposure = st.text_input("Exposure (e.g., occupational hazards)")
    smoking = st.selectbox("Smoking History", ["Never", "Former", "Current"])
    hrv = st.text_input("Heart Rate Variability (ms)")
    uploaded = st.file_uploader("Upload Chest X-ray", type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button("Analyze X-ray")

if submitted and uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Chest X-ray", use_column_width=True)
    with st.spinner("Running AMAL inference..."):
        time.sleep(2)

    st.success("🔍 Diagnosis: Pneumonia Detected")
    st.markdown("**Explanation:** The AI indicates bilateral lower lung opacities suggestive of consolidation.")
    st.markdown("---")

    st.header("Patient Summary")
    st.markdown(f"- **Name**: {name}")
    st.markdown(f"- **Age**: {age}")
    st.markdown(f"- **Gender**: {gender}")
    st.markdown(f"- **Symptoms**: {symptoms or 'N/A'}")
    st.markdown(f"- **Physical Activity Level**: {physical_activity}")
    st.markdown(f"- **Exposure**: {exposure or 'N/A'}")
    st.markdown(f"- **Smoking History**: {smoking}")
    st.markdown(f"- **Heart Rate Variability**: {hrv or 'N/A'}")

    st.markdown("---")
    st.caption("⚠️ This is a demo. Not for clinical use.")

    st.download_button(
        label="📄 Download Radiology Report",
        data=generate_docx(name, age, gender, symptoms, physical_activity, exposure, smoking, hrv),
        file_name=f"AMAL_Report_{name.replace(' ', '_')}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

elif submitted and not uploaded:
    st.error("Please upload an X-ray image.")
