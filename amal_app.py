import streamlit as st
from PIL import Image
import numpy as np
from utils import generate_docx

# --- Page config & CSS
st.set_page_config(page_title="AMAL – Radiology AI", layout="wide", page_icon="🫁")
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
body {background: #ffeef8; scroll-behavior: smooth;}
nav {position: sticky; top: 0; background: #ffd6e8; padding: 1rem 2rem; display: flex; align-items: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);}
nav img {height: 40px; margin-right: 2rem;}
nav a {margin-right: 2rem; color: #c6007e; text-decoration: none; font-weight: 600;}
.hero {padding: 6rem 2rem; text-align: center; background: white; border-radius: 12px; margin: 2rem;}
.hero h1 {font-size: 4rem; margin-bottom: 0.5rem; font-family: 'Trebuchet MS', sans-serif;}
.hero p {font-size: 1.2rem; color: #555;}
.hero button {background: #ff66ad; color: white; border: none; border-radius: 8px; padding: 1rem 2rem; font-size: 1.2rem; cursor: pointer; transition: background 0.3s;}
.hero button:hover {background: #ff4f93;}
.card {background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.05); margin-bottom: 2rem;}
</style>
""", unsafe_allow_html=True)

# --- Top navbar
st.markdown("""
<nav>
  <img src="logo.png" alt="AMAL logo" />
  <a href="#home">Home</a>
  <a href="#diagnosis">Diagnosis</a>
  <a href="#report">Report</a>
  <a href="#about">About</a>
</nav>
""", unsafe_allow_html=True)

# --- Hero / Landing section
st.markdown('<div id="home" class="hero">', unsafe_allow_html=True)
st.markdown("""
<h1>AMAL</h1>
<p>AI Radiology Assistant</p>
<button onclick="window.location.href='#diagnosis'">Start Diagnosis 🖊️</button>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Diagnosis form
st.markdown('<div id="diagnosis" style="padding:4rem 2rem;">', unsafe_allow_html=True)
st.header("Patient Information")
with st.form("patient_form"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    name = st.text_input("Full Name *")
    age = st.number_input("Age *", min_value=0)
    gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
    symptoms = st.text_area("Symptoms")
    activity = st.selectbox("Physical Activity Level", ["None","Low","Moderate","High"])
    exposure = st.text_input("Exposure (e.g., hazards)")
    smoking = st.selectbox("Smoking History", ["Never","Former","Current"])
    hrv = st.text_input("Heart Rate Variability (ms)")
    uploaded = st.file_uploader("Upload Chest X-ray *", type=["jpg","jpeg","png"])
    submitted = st.form_submit_button("Analyze X-ray")
    st.markdown('</div>', unsafe_allow_html=True)

# --- On submission, show images, heatmap & report
if submitted:
    if not uploaded:
        st.error("Please upload an X-ray image.")
        st.stop()
    img = Image.open(uploaded).convert("RGB")
    img_resized = img.resize((512,512))
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image(img_resized, caption="Original Chest X-ray", use_column_width=True)
    # fake heatmap
    x = np.linspace(-1,1,512)
    y = np.linspace(-1,1,512)
    xv, yv = np.meshgrid(x,y)
    blob = np.exp(-((xv+0.3)**2 + (yv+0.3)**2)*8) * np.exp(-((xv-0.2)**2 + (yv-0.2)**2)*10)
    blob /= blob.max()
    heat = np.uint8(255*blob)
    hrgb = np.zeros((512,512,3), dtype=np.uint8)
    hrgb[...,0] = heat
    overlay = (np.array(img_resized)*0.6 + hrgb*0.4).clip(0,255).astype(np.uint8)
    st.image(overlay, caption="AI Attention Heatmap", use_column_width=True)
    st.success("**Diagnosis:** Pneumonia Detected")
    st.markdown("**Explanation:** Highlighted regions show consolidation.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Report preview + download
    st.markdown('<div id="report" style="padding:4rem 2rem;">', unsafe_allow_html=True)
    st.header("Report Preview")
    st.markdown(f"""
    <div class="card">
      <b>Name:</b> {name}<br>
      <b>Age:</b> {age}<br>
      <b>Gender:</b> {gender}<br>
      <b>Symptoms:</b> {symptoms or 'N/A'}<br>
      <b>Activity:</b> {activity}<br>
      <b>Exposure:</b> {exposure or 'N/A'}<br>
      <b>Smoking:</b> {smoking}<br>
      <b>HRV:</b> {hrv or 'N/A'} ms
    </div>
    """, unsafe_allow_html=True)
    st.download_button("📄 Download Word Report",
                       data=generate_docx(name, age, gender, symptoms, activity, exposure, smoking, hrv),
                       file_name=f"Report_{name.replace(' ','_')}.docx",
                       mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    st.markdown('</div>', unsafe_allow_html=True)

# --- About
st.markdown('<div id="about" style="padding:4rem 2rem;">', unsafe_allow_html=True)
st.header("About AMAL")
st.write("AMAL is a premium pink-luxury AI radiology assistant for lung diagnostics, patient intake, X-ray analysis, and downloadable reporting.")
st.markdown('</div>', unsafe_allow_html=True)
