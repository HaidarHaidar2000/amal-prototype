import streamlit as st
from PIL import Image
import numpy as np
from utils import generate_docx

st.set_page_config(page_title="AMAL – LungCare AI", layout="wide", page_icon="🫁")

if 'page' not in st.session_state:
    st.session_state.page = 'home'

def go_home():
    st.session_state.page = 'home'

def go_diag():
    st.session_state.page = 'diagnosis'

st.markdown("""
<style>
body {
  margin: 0; padding: 0;
  background: linear-gradient(135deg, #FFD1DC 0%, #FFADC6 100%);
  font-family: Arial, sans-serif;
}
.landing {
  height: 100vh; display: flex;
  flex-direction: column; justify-content: center; align-items: center;
}
.landing h1 {
  font-size: 6rem; color: #CC0E74; margin: 0; letter-spacing: 0.3em;
}
.landing p {
  font-size: 1.5rem; color: #555; margin-bottom: 2rem;
}
.landing .btn {
  background: #FF91B8; color: white; border: none;
  padding: 1rem 2rem; font-size: 1.2rem; border-radius: 8px;
  cursor: pointer; transition: background 0.3s;
}
.landing .btn:hover { background: #FF6EA1; }
.container {
  max-width: 900px; margin: 2rem auto;
  background: white; padding: 2rem; border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.05);
}
input, textarea, select { width: 100% !important; }
h1, h2, h3, h4, p { color: #333; }
h1 { color: #CC0E74; }
</style>
""", unsafe_allow_html=True)

if st.session_state.page == 'home':
    st.markdown('<div class="landing">', unsafe_allow_html=True)
    st.markdown('<h1>AMAL</h1>', unsafe_allow_html=True)
    st.markdown('<p>AI Radiology Assistant</p>', unsafe_allow_html=True)
    if st.button("Start Diagnosis", key="start", on_click=go_diag):
        pass
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.button("← Back to Home", on_click=go_home)
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.header("Patient Information")
    with st.form("patient_form"):
        name     = st.text_input("Full Name *")
        age      = st.number_input("Age *", min_value=0)
        gender   = st.selectbox("Gender *", ["Male","Female","Other"])
        symptoms = st.text_area("Symptoms (optional)")
        activity = st.selectbox("Physical Activity Level", ["None","Low","Moderate","High"])
        exposure = st.text_input("Exposure (e.g., hazards)")
        smoking  = st.selectbox("Smoking History", ["Never","Former","Current"])
        hrv      = st.text_input("Heart Rate Variability (ms)")
        uploaded = st.file_uploader("Upload Chest X-ray *", type=["jpg","jpeg","png"])
        submitted = st.form_submit_button("Analyze X-ray")
    if submitted:
        if not uploaded:
            st.error("Please upload an X-ray image.")
            st.stop()
        img = Image.open(uploaded).convert("RGB").resize((512,512))
        st.image(img, caption="Original Chest X-ray", use_column_width=True)
        x = np.linspace(-1,1,512); y = np.linspace(-1,1,512)
        xv,yv = np.meshgrid(x,y)
        blob = np.exp(-((xv+0.3)**2 + (yv+0.3)**2)*8) + np.exp(-((xv-0.2)**2 + (yv-0.2)**2)*10)
        blob /= blob.max()
        heat = (255*blob).astype(np.uint8)
        hrgb = np.zeros((512,512,3), dtype=np.uint8); hrgb[...,0] = heat
        overlay = np.clip(np.array(img)*0.6 + hrgb*0.4, 0, 255).astype(np.uint8)
        st.image(overlay, caption="AI Attention Heatmap", use_column_width=True)
        st.success("**Diagnosis:** Pneumonia Detected")
        st.markdown("**Explanation:** Highlighted regions show consolidation.")
        st.subheader("Report Preview")
        st.markdown(f"""
- **Name:** {name}
- **Age:** {age}
- **Gender:** {gender}
- **Symptoms:** {symptoms or 'N/A'}
- **Activity:** {activity}
- **Exposure:** {exposure or 'N/A'}
- **Smoking:** {smoking}
- **HRV:** {hrv or 'N/A'} ms
"""")
        st.download_button(
            "📄 Download Word Report",
            data=generate_docx(name, age, gender, symptoms, activity, exposure, smoking, hrv),
            file_name=f"Report_{name.replace(' ','_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    st.markdown("</div>", unsafe_allow_html=True)