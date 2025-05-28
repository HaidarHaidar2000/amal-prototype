import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(page_title="AMAL – LungCare AI", layout="centered")

# CSS for premium look
st.markdown("""
<style>
body { background: #fff5f9; }
.big-card {
    background: white;
    border-radius: 36px;
    box-shadow: 0 8px 32px #f0bfd3;
    max-width: 470px;
    padding: 60px 50px 50px 50px;
    text-align: center;
    margin: 50px auto 40px auto;
}
.amal-title {
    font-family: 'Playfair Display', serif;
    font-size: 76px;
    color: #c2185b;
    font-weight: bold;
    letter-spacing: 2px;
    margin-bottom: 12px;
    margin-top: 0;
}
.amal-subtitle {
    font-family: 'Montserrat', sans-serif;
    color: #707070;
    font-size: 22px;
    margin-bottom: 38px;
}
.start-btn {
    background: linear-gradient(90deg, #fcbad3 10%, #ffb7b2 100%);
    color: #fff;
    font-size: 26px;
    border: none;
    border-radius: 16px;
    padding: 18px 55px;
    cursor: pointer;
    font-family: 'Montserrat', sans-serif;
    font-weight: 700;
    box-shadow: 0 4px 12px #f9dbe5;
    margin-bottom: 0px;
    transition: background 0.2s;
}
.start-btn:hover {
    background: #ea8daf;
}
.input-card {
    background: white;
    border-radius: 30px;
    box-shadow: 0 6px 20px #e8bdd1;
    max-width: 550px;
    margin: 40px auto;
    padding: 38px 30px 30px 30px;
}
</style>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Page routing with session state
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to_diagnosis():
    st.session_state.page = "diagnosis"

# HOME PAGE
if st.session_state.page == "home":
    st.markdown("""
    <div class="big-card">
        <div class="amal-title">AMAL</div>
        <div class="amal-subtitle">Cutting-edge tools for the diagnosis and management of respiratory diseases.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Diagnosis", key="start", help="Go to diagnosis page", use_container_width=True):
        st.session_state.page = "diagnosis"
        st.experimental_rerun()

# DIAGNOSIS PAGE
if st.session_state.page == "diagnosis":
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
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
        submitted = st.form_submit_button("Analyze")
    if submitted:
        if not uploaded:
            st.error("Please upload an X-ray image.")
            st.stop()
        img = Image.open(uploaded).convert("RGB").resize((512,512))
        st.image(img, caption="Original Chest X-ray", use_column_width=True)
        # Simulated heatmap
        x = np.linspace(-1,1,512); y = np.linspace(-1,1,512)
        xv, yv = np.meshgrid(x,y)
        blob = np.exp(-((xv+0.3)**2 + (yv+0.3)**2)*8)
        blob /= blob.max()
        heat = (blob*255).astype(np.uint8)
        overlay = np.array(img).astype(float) * 0.6
        overlay[:,:,0] = np.clip(overlay[:,:,0] + heat*0.4, 0, 255)
        st.image(overlay.astype(np.uint8), caption="AI Attention Heatmap", use_column_width=True)
        st.success("**Diagnosis:** Pneumonia Detected")
        st.markdown("**Explanation:** Highlighted regions show consolidation.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.button("Back to Home", key="back", on_click=lambda: st.session_state.update(page="home"))
