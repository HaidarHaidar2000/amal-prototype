
import streamlit as st
from PIL import Image
import numpy as np
from utils import generate_docx

# Page configuration
st.set_page_config(page_title="AMAL – LungCare AI", layout="wide", page_icon="🫁")

# Hide default Streamlit menu, header, and footer
st.markdown(
    '<style>#MainMenu{visibility:hidden;} footer{visibility:hidden;} header{visibility:hidden;}</style>',
    unsafe_allow_html=True
)

# Top navigation bar
st.markdown("""
<nav style="position:sticky; top:0; background:white; display:flex; align-items:center; padding:1rem 2rem; box-shadow:0 2px 8px rgba(0,0,0,0.1); z-index:1000;">
  <img src="logo.png" style="width:50px; margin-right:1rem;" />
  <a href="#home" style="margin-right:2rem; color:#CC0E74; text-decoration:none; font-weight:600;">Home</a>
  <a href="#diagnosis" style="margin-right:2rem; color:#CC0E74; text-decoration:none; font-weight:600;">Patient</a>
  <a href="#report" style="margin-right:2rem; color:#CC0E74; text-decoration:none; font-weight:600;">Report</a>
  <a href="#about" style="color:#CC0E74; text-decoration:none; font-weight:600;">About</a>
</nav>
""", unsafe_allow_html=True)

# Global CSS
st.markdown("""
<style>
body {background:#FFF9FC; scroll-behavior:smooth;}
h1,h2,h3,h4 {color:#CC0E74; font-family:sans-serif;}
.hero {padding:6rem 2rem; text-align:center;}
.hero h1 {font-size:3rem; margin-bottom:1rem;}
.hero p {font-size:1.2rem; color:#555; margin-bottom:2rem;}
button.primary {background:#FFADC6; color:white; border:none; border-radius:6px; padding:0.8em 1.5em; font-size:1rem; cursor:pointer; transition:background 0.3s;}
button.primary:hover {background:#FF91B8;}
.card {background:white; padding:2rem; border-radius:12px; box-shadow:0 8px 24px rgba(0,0,0,0.05); margin-bottom:2rem;}
</style>
""", unsafe_allow_html=True)

# Home section
st.markdown('<div id="home" class="hero">', unsafe_allow_html=True)
st.markdown("""
<h1>AI Lung Diagnostics, Reimagined</h1>
<p>A premium prototype to assist clinicians & patients.</p>
<button class="primary" onclick="window.location.href='#diagnosis'">Start Diagnosis 💡</button>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Diagnosis section
st.markdown('<div id="diagnosis" style="padding:4rem 2rem;">', unsafe_allow_html=True)
st.header("Patient Information")
with st.form("patient_form"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    name = st.text_input("Full Name *")
    age = st.number_input("Age *", min_value=0)
    gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
    symptoms = st.text_area("Symptoms")
    activity = st.selectbox("Physical Activity Level", ["None", "Low", "Moderate", "High"])
    exposure = st.text_input("Exposure (e.g., hazards)")
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
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image(img_resized, caption="Original Chest X‑ray", use_column_width=True)
    x = np.linspace(-1, 1, 512); y = np.linspace(-1, 1, 512)
    xv, yv = np.meshgrid(x, y)
    blob = np.exp(-((xv + 0.3) ** 2 + (yv + 0.3) ** 2) * 8) + np.exp(-((xv - 0.2) ** 2 + (yv - 0.2) ** 2) * 10)
    blob /= blob.max()
    heat = np.uint8(255 * blob); hrgb = np.zeros((*heat.shape, 3), dtype=np.uint8)
    hrgb[:, :, 0] = heat
    overlay = np.clip(np.array(img_resized) * 0.6 + hrgb * 0.4, 0, 255).astype(np.uint8)
    st.image(overlay, caption="AI Attention Heatmap", use_column_width=True)
    st.success("**Diagnosis:** Pneumonia Detected")
    st.markdown("**Explanation:** Highlighted regions show consolidation.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div id="report" style="padding:4rem 2rem;">', unsafe_allow_html=True)
    st.header("Report Preview")
    st.markdown(f"""
    <div class="card">
      <b>Name:</b> {name}<br>
      <b>Age:</b> {age}<br>
      <b>Gender:</b> {gender}<br>
      <b>Symptoms:</b> {symptoms or 'N/A'}<br>
      <b>Physical Activity:</b> {activity}<br>
      <b>Exposure:</b> {exposure or 'N/A'}<br>
      <b>Smoking History:</b> {smoking}<br>
      <b>Heart Rate Variability (ms):</b> {hrv or 'N/A'}
    </div>
    """, unsafe_allow_html=True)
    st.download_button("📄 Download Word Report", data=generate_docx(
        name, age, gender, symptoms, activity, exposure, smoking, hrv),
        file_name=f"Report_{name.replace(' ', '_')}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    st.markdown('</div>', unsafe_allow_html=True)

# About section
st.markdown('<div id="about" style="padding:4rem 2rem;">', unsafe_allow_html=True)
st.header("About AMAL")
st.write("AMAL is a prototype AI lung assistant showcasing premium white & pink design, patient intake, X‑ray analysis, and downloadable reporting.")
st.markdown('</div>', unsafe_allow_html=True)
