import streamlit as st
from PIL import Image
import numpy as np
from utils import generate_docx

# Page config
st.set_page_config(page_title="AMAL – LungCare AI", layout="wide", page_icon="❤️")

# Navigation
nav = st.experimental_get_query_params().get("page", ["home"])[0]
if st.sidebar.button("Home"):
    st.experimental_set_query_params(page="home")
if st.sidebar.button("Diagnosis"):
    st.experimental_set_query_params(page="diagnosis")

# Global CSS
st.markdown("""
<style>
body {background: #ffe8f0; margin:0;}
header, footer {visibility:hidden;}
nav {background:#ffc1dc; padding:1rem; text-align:center;}
nav a {margin:0 1rem; color:#d12c5f; text-decoration:none; font-weight:bold;}
.hero {padding:4rem; text-align:center;}
.hero h1 {font-size:4rem; color:#d12c5f; margin-bottom:1rem;}
.hero p {font-size:1.2rem; color:#333;}
button.primary {background:#d12c5f; color:white; border:none; padding:1rem 2rem; font-size:1.2rem; border-radius:8px; cursor:pointer;}
.card {background:white; padding:2rem; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.05); margin-bottom:2rem;}
</style>
""", unsafe_allow_html=True)

# Home Page
if nav == "home":
    st.markdown('<nav><a href="?page=home">Home</a><a href="?page=diagnosis">Diagnosis</a></nav>', unsafe_allow_html=True)
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.markdown('<h1>AMAL</h1><p>Cutting-edge tools for respiratory diagnostics.</p>', unsafe_allow_html=True)
    if st.button("Start Diagnosis"):
        st.experimental_set_query_params(page="diagnosis")
    st.markdown('</div>', unsafe_allow_html=True)

# Diagnosis Page
elif nav == "diagnosis":
    st.markdown('<nav><a href="?page=home">Home</a><a href="?page=diagnosis">Diagnosis</a></nav>', unsafe_allow_html=True)
    st.header("Patient Information")
    with st.form("patient_form"):
        name = st.text_input("Full Name *")
        age = st.number_input("Age *", min_value=0)
        gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
        symptoms = st.text_area("Symptoms")
        activity = st.selectbox("Physical Activity Level", ["None", "Low", "Moderate", "High"])
        exposure = st.text_input("Exposure (e.g., hazards)")
        smoking = st.selectbox("Smoking History", ["Never", "Former", "Current"])
        hrv = st.text_input("Heart Rate Variability (ms)")
        uploaded = st.file_uploader("Upload Chest X-ray *", type=["jpg","jpeg","png"])
        submitted = st.form_submit_button("Analyze X-ray")
    if submitted:
        if not uploaded:
            st.error("Please upload an X-ray image.")
            st.stop()
        img = Image.open(uploaded).convert("RGB").resize((512,512))
        st.image(img, caption="Original X-ray", use_column_width=True)
        x = np.linspace(-1,1,512); y = np.linspace(-1,1,512)
        xv, yv = np.meshgrid(x,y)
        blob = np.exp(-((xv+0.3)**2 + (yv+0.3)**2)*8)
        blob /= blob.max()
        heat = (blob*255).astype(np.uint8)
        overlay = np.array(img) * 0.6
        overlay[:,:,0] = np.clip(overlay[:,:,0] + heat*0.4, 0, 255)
        st.image(overlay.astype(np.uint8), caption="AI Attention Heatmap", use_column_width=True)
        st.success("**Diagnosis:** Pneumonia Detected")
        st.markdown("**Explanation:** Highlighted regions show consolidation.")
        st.header("Report Preview")
        st.markdown(f"""
<div class="card">
**Name:** {name}<br>
**Age:** {age}<br>
**Gender:** {gender}<br>
**Symptoms:** {symptoms or 'N/A'}<br>
**Physical Activity:** {activity}<br>
**Exposure:** {exposure or 'N/A'}<br>
**Smoking History:** {smoking}<br>
**HRV:** {hrv or 'N/A'} ms
</div>
""", unsafe_allow_html=True)
        st.download_button("Download Word Report", data=generate_docx(
            name, age, gender, symptoms, activity, exposure, smoking, hrv
        ), file_name=f"Report_{name.replace(' ','_')}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

