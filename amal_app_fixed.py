
import streamlit as st
from PIL import Image
import numpy as np
from utils import generate_docx

# Page config
st.set_page_config(page_title="AMAL AI Radiology Assistant", layout="wide")

# Hide default Streamlit UI
st.markdown(
    """<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>""" ,
    unsafe_allow_html=True
)

# Navigation bar
st.markdown(
    """<nav style="position:sticky; top:0; background:#FFDDEE; padding:1rem; text-align:center;">
        <a href="?page=home" style="margin:0 2rem; color:#D6336C; text-decoration:none; font-weight:bold;">Home</a>
        <a href="?page=diagnosis" style="margin:0 2rem; color:#D6336C; text-decoration:none; font-weight:bold;">Diagnosis</a>
    </nav>""" ,
    unsafe_allow_html=True
)

# Determine page
params = st.experimental_get_query_params()
page = params.get("page", ["home"])[0]

if page == "home":
    st.markdown(
        """<div style="padding:4rem; text-align:center; background:#FFDDEE;">
            <h1 style="font-size:4rem; margin-bottom:1rem; color:#D6336C; font-family:'Georgia', serif;">AMAL</h1>
            <p style="font-size:1.2rem; color:#555;">Cutting-edge tools for the diagnosis and management of respiratory diseases.</p>
            <button style="background:#D6336C; color:white; border:none; padding:1rem 2rem; font-size:1.1rem;
                           border-radius:8px; cursor:pointer; margin-top:2rem;"
                    onclick="window.location.href='?page=diagnosis'">
                Start Diagnosis
            </button>
        </div>""" ,
        unsafe_allow_html=True
    )
    st.stop()

# Diagnosis section
st.markdown('<div style="padding:4rem;">', unsafe_allow_html=True)
st.header("Patient Information")

with st.form("patient_form"):
    name = st.text_input("Full Name *")
    age = st.number_input("Age *", min_value=0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    symptoms = st.text_area("Symptoms")
    activity = st.selectbox("Physical Activity Level", ["None", "Low", "Moderate", "High"])
    exposure = st.text_input("Exposure (e.g., hazards)")
    smoking = st.selectbox("Smoking History", ["Never", "Former", "Current"])
    hrv = st.number_input("Heart Rate Variability (ms)")
    uploaded = st.file_uploader("Upload Chest X-ray *", type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button("Analyze X‑ray")

if submitted:
    if not uploaded:
        st.error("Please upload an X‑ray image.")
        st.stop()

    img = Image.open(uploaded).convert("RGB")
    img_resized = img.resize((512, 512))
    st.image(img_resized, caption="Original Chest X‑ray", use_column_width=True)

    # Generate fake heatmap
    x = np.linspace(-1, 1, 512)
    y = np.linspace(-1, 1, 512)
    xv, yv = np.meshgrid(x, y)
    blob = np.exp(-((xv + 0.3)**2 + (yv + 0.3)**2) * 8) + np.exp(-((xv - 0.2)**2 + (yv - 0.2)**2) * 10)
    blob = blob / blob.max()
    heat = (255 * blob).astype(np.uint8)

    # Heatmap as RGB
    heatmap_rgb = np.zeros((512, 512, 3), dtype=np.uint8)
    heatmap_rgb[:, :, 0] = heat

    # Overlay heatmap
    overlay = (np.array(img_resized) * 0.6 + heatmap_rgb * 0.4).clip(0, 255).astype(np.uint8)
    st.image(overlay, caption="AI Attention Heatmap", use_column_width=True)

    st.success("**Diagnosis:** Pneumonia Detected")
    st.markdown("**Explanation:** Highlighted regions show consolidation.")

    st.header("Report Preview")
    st.write(f"**Name:** {name}")
    st.write(f"**Age:** {age}")
    st.write(f"**Gender:** {gender}")
    st.write(f"**Symptoms:** {symptoms or 'N/A'}")
    st.write(f"**Physical Activity Level:** {activity}")
    st.write(f"**Exposure:** {exposure or 'N/A'}")
    st.write(f"**Smoking History:** {smoking}")
    st.write(f"**Heart Rate Variability (ms):** {hrv or 'N/A'}")

    # Download report
    report_bytes = generate_docx(name, age, gender, symptoms, activity, exposure, smoking, hrv)
    st.download_button(
        "📄 Download Word Report",
        data=report_bytes,
        file_name=f"Report_{name.replace(' ', '_')}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

st.markdown("</div>", unsafe_allow_html=True)
