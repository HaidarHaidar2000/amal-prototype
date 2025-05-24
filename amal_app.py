
import streamlit as st
from PIL import Image
import numpy as np
from utils import generate_docx

# --- Page Config ---
st.set_page_config(page_title="AMAL – LungCare AI", layout="wide", page_icon="🫁")

# --- Custom CSS & Animations ---
st.markdown("""
<style>
html {scroll-behavior: smooth;}
@keyframes fadeIn {from{opacity:0;}to{opacity:1;}}
body {background-color:#FFF8FA;}
.stButton button {
    background-color:#FFADC6;color:white;border:none;border-radius:8px;padding:0.8em 1.5em;transition:background 0.3s;
}
.stButton button:hover {background-color:#ff8fb7;}
.stDownloadButton button {
    background-color:#ffffff;border:2px solid #FFADC6;color:#FFADC6;border-radius:8px;padding:0.6em 1.2em;transition:background 0.3s, color 0.3s;
}
.stDownloadButton button:hover {background-color:#FFADC6;color:white;}
h1,h2,h3,h4 {color:#CC0E74;font-family:sans-serif;}
.form-card, .block {
    background:white;padding:2rem;border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,0.05);transition:transform 0.3s;
}
.form-card:hover {transform: translateY(-4px);}
.stImage img {animation: fadeIn 1s ease-in;}
.sidebar .sidebar-content {
    background: #FFF8FA; border-right:none;
}
</style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("AMAL")
page = st.sidebar.radio("Navigation", ["Home", "Diagnosis", "Reports", "About"])

# --- Home Page ---
if page == "Home":
    st.markdown("""<div style='text-align:center; padding:5rem 0;'>
        <img src='logo.png' width='160'><br>
        <h1 style='font-size:3rem; margin:1rem 0;'>AI Lung Diagnostics, Reimagined</h1>
        <p style='font-size:1.2rem; color:#333;'>A friendly demo to assist clinicians & patients.</p>
        <a href='#diagnosis'><button style='font-size:1rem; margin-top:1.5rem;'>Start Diagnosis 💡</button></a>
    </div>""", unsafe_allow_html=True)

# --- Diagnosis Page ---
if page == "Diagnosis":
    st.markdown("<h2 id='diagnosis'>Patient Information</h2>", unsafe_allow_html=True)
    with st.form("diagnosis_form"):
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        name = st.text_input("Full Name *")
        age = st.number_input("Age *", min_value=0)
        gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
        symptoms = st.text_area("Symptoms")
        physical_activity = st.selectbox("Physical Activity Level", ["None", "Low", "Moderate", "High"])
        exposure = st.text_input("Exposure (e.g., occupational hazards)")
        smoking = st.selectbox("Smoking History", ["Never", "Former", "Current"])
        hrv = st.text_input("Heart Rate Variability (ms)")
        uploaded = st.file_uploader("Upload Chest X‑ray *", type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("Analyze X‑ray")
        st.markdown('</div>', unsafe_allow_html=True)
    if submitted:
        if not uploaded:
            st.error("Please upload an X‑ray image.")
            st.stop()
        img = Image.open(uploaded).convert("RGB")
        img_resized = img.resize((512, 512))
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.image(img_resized, caption="Original Chest X‑ray", use_column_width=True)
        # Generate fake heatmap
        x = np.linspace(-1, 1, 512); y = np.linspace(-1, 1, 512)
        xv, yv = np.meshgrid(x, y)
        blob = np.exp(-((xv+0.3)**2 + (yv+0.3)**2)*8) + np.exp(-((xv-0.2)**2 + (yv-0.2)**2)*10)
        blob /= blob.max()
        heat = np.uint8(255*blob); heat_rgb = np.zeros((*heat.shape,3),dtype=np.uint8)
        heat_rgb[:,:,0] = heat
        overlay = np.clip(np.array(img_resized)*0.6 + heat_rgb*0.4,0,255).astype(np.uint8)
        st.image(overlay, caption="AI Attention Heatmap (simulated)", use_column_width=True)
        st.success(":mag: **Diagnosis:** Pneumonia Detected")
        st.markdown("**Explanation:** AI highlights regions consistent with consolidation.")
        st.markdown("</div><br>", unsafe_allow_html=True)
        # Report Preview
        st.markdown("### Report Preview")
        st.markdown(f"""<div class="block">
            <b>Name:</b> {name}<br>
            <b>Age:</b> {age}<br>
            <b>Gender:</b> {gender}<br>
            <b>Symptoms:</b> {symptoms or 'N/A'}<br>
            <b>Physical Activity:</b> {physical_activity}<br>
            <b>Exposure:</b> {exposure or 'N/A'}<br>
            <b>Smoking History:</b> {smoking}<br>
            <b>Heart Rate Variability:</b> {hrv or 'N/A'} ms
        </div>""", unsafe_allow_html=True)
        st.download_button(
            "📄 Download Radiology Report",
            data=generate_docx(name, age, gender, symptoms, physical_activity, exposure, smoking, hrv),
            file_name=f"AMAL_Report_{name.replace(' ', '_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

# --- Reports Page ---
if page == "Reports":
    st.markdown("### Reports")
    st.info("Generate a report in the Diagnosis tab.")

# --- About Page ---
if page == "About":
    st.markdown("### About AMAL")
    st.write("AMAL is a prototype AI lung diagnosis tool designed for clinicians and patients.")

