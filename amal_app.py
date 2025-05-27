import streamlit as st
from PIL import Image
import numpy as np
from utils import generate_docx

# Page config
st.set_page_config(page_title="AMAL – Radiology AI", layout="wide", page_icon="🫁")

# Global CSS + Navbar
st.markdown("""
<style>
body {background:#ffeef8; margin:0; padding:0; font-family:sans-serif;}
nav {background:#ffd6e8; padding:1rem 2rem; display:flex; justify-content:center; gap:2rem; position:sticky; top:0; z-index:100;}
nav a {color:#333; text-decoration:none; font-weight:600;}
.hero {max-width:600px; margin:80px auto; padding:4rem 2rem; background:white; border-radius:16px; box-shadow:0 8px 24px rgba(0,0,0,0.05); text-align:center;}
.hero h1 {font-size:4rem; color:#333; margin-bottom:0.5rem;}
.hero p {font-size:1.2rem; color:#555; margin-bottom:2rem;}
.hero .btn {display:inline-block; padding:1rem 2rem; background:#ff99bb; color:white; border-radius:8px; text-decoration:none; font-size:1.1rem; transition:background 0.3s;}
.hero .btn:hover {background:#ff77aa;}
.card {max-width:800px; margin:40px auto; padding:2rem; background:white; border-radius:12px; box-shadow:0 8px 24px rgba(0,0,0,0.05);}
</style>
<nav>
  <a href="?page=home">Home</a>
  <a href="?page=diagnosis">Diagnosis</a>
</nav>
""", unsafe_allow_html=True)

# Router
params = st.experimental_get_query_params()
page = params.get("page", ["home"])[0]

# Home
if page == "home":
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.markdown("""
        <h1>AMAL</h1>
        <p>Cutting-edge tools for the diagnosis and management of respiratory diseases.</p>
        <a class="btn" href="?page=diagnosis">Start Diagnosis</a>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Diagnosis page
elif page == "diagnosis":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Patient Information")
    with st.form("patient_form"):
        name     = st.text_input("Full Name *")
        age      = st.number_input("Age *", min_value=0)
        gender   = st.selectbox("Gender *", ["Male","Female","Other"])
        symptoms = st.text_area("Symptoms")
        activity = st.selectbox("Physical Activity", ["None","Low","Moderate","High"])
        exposure = st.text_input("Exposure (e.g., hazards)")
        smoking  = st.selectbox("Smoking History", ["Never","Former","Current"])
        hrv      = st.text_input("Heart Rate Variability (ms)")
        uploaded = st.file_uploader("Upload Chest X-ray *", type=["jpg","jpeg","png"])
        submit   = st.form_submit_button("Analyze X-ray")
    st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if not uploaded:
            st.error("Please upload an X-ray image.")
            st.stop()

        img = Image.open(uploaded).convert("RGB")
        img512 = img.resize((512,512))
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.image(img512, caption="Original Chest X-ray", use_column_width=True)

        # Fake heatmap
        x = np.linspace(-1,1,512); y = np.linspace(-1,1,512)
        xv, yv = np.meshgrid(x,y)
        blob = np.exp(-((xv+0.3)**2+(yv+0.3)**2)*8)*np.exp(-((xv-0.2)**2+(yv-0.2)**2)*10)
        blob /= blob.max()
        heat = (255*blob).astype(np.uint8)
        hrgb  = np.zeros((512,512,3),dtype=np.uint8); hrgb[...,0] = heat
        overlay = (np.array(img512)*0.6 + hrgb*0.4).clip(0,255).astype(np.uint8)
        st.image(overlay, caption="AI Attention Heatmap", use_column_width=True)
        st.success("**Diagnosis:** Pneumonia Detected")
        st.markdown("**Explanation:** Highlighted regions show consolidation.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Report preview & download
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("Report Preview")
        st.markdown(f"""
        <b>Name:</b> {name}<br>
        <b>Age:</b> {age}<br>
        <b>Gender:</b> {gender}<br>
        <b>Symptoms:</b> {symptoms or 'N/A'}<br>
        <b>Activity:</b> {activity}<br>
        <b>Exposure:</b> {exposure or 'N/A'}<br>
        <b>Smoking:</b> {smoking}<br>
        <b>HRV:</b> {hrv or 'N/A'} ms
        """, unsafe_allow_html=True)
        st.download_button(
            "📄 Download Word Report",
            data=generate_docx(name, age, gender, symptoms, activity, exposure, smoking, hrv),
            file_name=f"Report_{name.replace(' ','_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        st.markdown('</div>', unsafe_allow_html=True)
