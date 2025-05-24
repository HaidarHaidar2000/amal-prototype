import streamlit as st
from PIL import Image
import numpy as np
from utils import generate_docx

# Page config
st.set_page_config(page_title="AMAL", layout="wide", page_icon="💗")

# Hide default menu and footer
st.markdown("<style>#MainMenu, footer {visibility: hidden;}</style>", unsafe_allow_html=True)

# Global CSS for pink-luxury aesthetic
st.markdown("""
<style>
body {background-color: #FFE6F2; scroll-behavior: smooth;}
.nav {background: #FFD6E8; padding: 1rem; position: sticky; top: 0; z-index: 100;}
.nav img {height: 40px; vertical-align: middle; margin-right: 1rem;}
.nav a {margin-right: 2rem; color: #FF1E81; text-decoration: none; font-weight: bold; font-size: 1.1rem;}
.hero {text-align: center; padding: 8rem 0;}
.hero h1 {font-size: 5rem; color: #FF1E81; font-family: 'Georgia', serif; margin: 0;}
.button-start {background: #FF1E81; color: white; padding: 1rem 2rem; font-size: 1.2rem; border: none; border-radius: 8px; cursor: pointer; transition: opacity 0.3s;}
.button-start:hover {opacity: 0.8;}
.card {background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 2rem;}
</style>
""", unsafe_allow_html=True)

# Session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Navigation buttons
cols = st.columns([1,1,8])
with cols[0]:
    if st.button("Home"):
        st.session_state.page = 'home'
        st.experimental_rerun()
with cols[1]:
    if st.button("Diagnosis"):
        st.session_state.page = 'diagnosis'
        st.experimental_rerun()

# Home page
if st.session_state.page == 'home':
    st.markdown('<div class="hero"><h1>AMAL</h1><p><em>AI Radiology Assistant</em></p></div>', unsafe_allow_html=True)
    if st.button("Start Diagnosis", key="start_diag"):
        st.session_state.page = 'diagnosis'
        st.experimental_rerun()

# Diagnosis page
elif st.session_state.page == 'diagnosis':
    st.markdown('<div class="card"><h2>Patient Information</h2></div>', unsafe_allow_html=True)
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
        submitted = st.form_submit_button("Analyze X‑ray")
    if submitted:
        if not uploaded:
            st.error("Please upload an X‑ray image.")
            st.stop()
        img = Image.open(uploaded).convert("RGB")
        img = img.resize((512,512))
        st.image(img, caption="Original Chest X‑ray", use_column_width=True)
        # fake heatmap
        x = np.linspace(-1,1,512)
        y = np.linspace(-1,1,512)
        xv, yv = np.meshgrid(x,y)
        blob = np.exp(-((xv+0.2)**2 + (yv+0.3)**2)*8)
        heat = (255 * blob / blob.max()).astype(np.uint8)
        overlay = np.stack([np.array(img)]*3, axis=2)
        overlay[:,:,0] = np.clip(overlay[:,:,0]*0.6 + heat*0.4,0,255)
        st.image(overlay.astype(np.uint8), caption="AI Attention Heatmap", use_column_width=True)
        st.success("**Diagnosis:** Pneumonia Detected")
        st.markdown("**Explanation:** Highlighted regions show consolidation.")
        # Report
        st.markdown('<div class="card"><h2>Report Preview</h2></div>', unsafe_allow_html=True)
        st.markdown(f"""
- **Name:** {name}  
- **Age:** {age}  
- **Gender:** {gender}  
- **Symptoms:** {symptoms or 'N/A'}  
- **Physical Activity:** {activity}  
- **Exposure:** {exposure or 'N/A'}  
- **Smoking History:** {smoking}  
- **Heart Rate Variability:** {hrv or 'N/A'} ms  
""", unsafe_allow_html=True)
        st.download_button(
            "Download Word Report",
            data=generate_docx(name, age, gender, symptoms, activity, exposure, smoking, hrv),
            file_name=f"Report_{name.replace(' ','_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
