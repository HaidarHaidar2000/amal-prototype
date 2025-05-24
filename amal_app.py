
import streamlit as st
from PIL import Image
import numpy as np
from utils import generate_docx

st.set_page_config(page_title="AMAL – LungCare AI", layout="wide", page_icon="🫁")

# Sidebar Navigation
st.sidebar.title("AMAL Navigation")
page = st.sidebar.radio("Go to", ["Home", "Diagnosis", "Report", "About"])

# Custom CSS
st.markdown('''
<style>
body {background-color:#FFF8FA;}
.stButton button {
    background-color:#FFADC6;color:white;border:none;border-radius:6px;padding:0.6em 1.2em;
}
.stButton button:hover {
    background-color:#ff8fb7;
}
.stDownloadButton button {
    background-color:#ffffff;border:2px solid #FFADC6;color:#FFADC6;border-radius:6px;padding:0.5em 1.1em;
}
.stDownloadButton button:hover {
    background-color:#FFADC6;color:white;
}
h1,h2,h3,h4 {color:#CC0E74;font-family:sans-serif;}
.block {
    background:white;padding:2rem;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,0.05);
}
</style>
''', unsafe_allow_html=True)

# Home Page
if page == "Home":
    st.markdown("<div style='text-align:center;'>"
                "<img src='https://raw.githubusercontent.com/HaidarHaidar2000/amal-prototype/main/logo.png' width='120'><br>"
                "<h1>AMAL</h1>"
                "<h4>AI Lung Diagnostics, Reimagined for Care</h4><br>"
                "<a href='#diagnosis'><button style='font-size:18px;padding:10px 20px;'>Start Diagnosis</button></a>"
                "</div>", unsafe_allow_html=True)

# Diagnosis Page
if page == "Diagnosis":
    st.markdown("<h2 id='diagnosis'>Patient Information</h2>", unsafe_allow_html=True)
    with st.form("diagnosis_form"):
        name = st.text_input("Full Name *")
        age = st.number_input("Age *", min_value=0, format="%d")
        gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
        symptoms = st.text_area("Symptoms")
        physical_activity = st.selectbox("Physical Activity Level", ["None", "Low", "Moderate", "High"])
        exposure = st.text_input("Exposure (e.g., occupational hazards)")
        smoking = st.selectbox("Smoking History", ["Never", "Former", "Current"])
        hrv = st.text_input("Heart Rate Variability (ms)")
        uploaded = st.file_uploader("Upload Chest X‑ray *", type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("Analyze X‑ray")

    if submitted:
        if not uploaded:
            st.error("Please upload an X‑ray image.")
            st.stop()

        img = Image.open(uploaded).convert("RGB")
        img_resized = img.resize((512, 512))
        st.image(img, caption="Original Chest X‑ray", use_column_width=True)

        x = np.linspace(-1, 1, 512)
        y = np.linspace(-1, 1, 512)
        xv, yv = np.meshgrid(x, y)
        blob = np.exp(-((xv + 0.3) ** 2 + (yv + 0.3) ** 2) * 8) + np.exp(-((xv - 0.2) ** 2 + (yv - 0.2) ** 2) * 10)
        blob /= blob.max()
        heat = np.uint8(255 * blob)
        heat_rgb = np.zeros((*heat.shape, 3), dtype=np.uint8)
        heat_rgb[:, :, 0] = heat
        base_arr = np.array(img_resized)
        overlay = np.clip(base_arr * 0.6 + heat_rgb * 0.4, 0, 255).astype(np.uint8)
        st.image(overlay, caption="AI Attention Heatmap (simulated)", use_column_width=True)

        st.success(":mag: **Diagnosis:** Pneumonia Detected")
        st.markdown("**Explanation:** AI highlights regions of increased opacity consistent with consolidation.")

        st.markdown("---")
        st.markdown("### Report Preview")
        st.markdown(f'''
        <div class="block">
        <b>Name:</b> {name}<br>
        <b>Age:</b> {age}<br>
        <b>Gender:</b> {gender}<br>
        <b>Symptoms:</b> {symptoms or 'N/A'}<br>
        <b>Physical Activity:</b> {physical_activity}<br>
        <b>Exposure:</b> {exposure or 'N/A'}<br>
        <b>Smoking History:</b> {smoking}<br>
        <b>HRV:</b> {hrv or 'N/A'} ms
        </div>
        ''', unsafe_allow_html=True)

        st.download_button(
            "📄 Download Radiology Report",
            data=generate_docx(name, age, gender, symptoms, physical_activity, exposure, smoking, hrv),
            file_name=f"AMAL_Report_{name.replace(' ', '_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

# Report Page
if page == "Report":
    st.markdown("### Report Section")
    st.info("Submit a patient in the Diagnosis tab to generate a report.")

# About Page
if page == "About":
    st.markdown("### About AMAL")
    st.write("AMAL is a prototype AI lung diagnosis tool designed to assist clinicians and patients in early identification of respiratory illnesses using deep learning.")
