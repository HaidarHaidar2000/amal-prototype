import streamlit as st
from PIL import Image
import numpy as np
from utils import generate_docx

st.set_page_config(page_title="AMAL – LungCare AI", layout="wide")

# Hide Streamlit default header/footer/menu
st.markdown(
    """<style>
    #MainMenu, footer, header {visibility:hidden;}
    </style>""",
    unsafe_allow_html=True,
)

# Global CSS for pink-luxury theme
st.markdown(
    """<style>
    body {background:#fff0f6; scroll-behavior:smooth;}
    .nav {background:#ffd1e8; padding:1rem; text-align:center;}
    .nav a {margin:0 1rem; color:#d6336c; font-weight:bold; text-decoration:none;}
    .hero {background:#ffe8f0; padding:4rem; text-align:center;}
    .hero h1 {font-size:4rem; color:#d6336c; margin:0;}
    .hero p {font-size:1.25rem; color:#333; margin:0.5rem 0 2rem;}
    .button-primary {background-color:#d6336c; color:white; border:none; padding:1rem 2rem; font-size:1rem; border-radius:0.5rem; transition:background 0.3s;}
    .button-primary:hover {background-color:#c2255c; cursor:pointer;}
    .container {max-width:800px; margin:2rem auto; background:white; padding:2rem; border-radius:0.5rem; box-shadow:0 4px 12px rgba(0,0,0,0.1);}
    </style>""",
    unsafe_allow_html=True,
)

# Read query parameters
params = st.query_params
page = params.get("page", ["home"])[0]

# Navigation bar
st.markdown(
    f'<div class="nav"><a href="?page=home">Home</a><a href="?page=diagnosis">Diagnosis</a></div>',
    unsafe_allow_html=True,
)

if page == "home":
    # Hero section
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.markdown(
        '<h1>AMAL</h1><p>Cutting-edge tools for the diagnosis and management of respiratory diseases.</p>',
        unsafe_allow_html=True,
    )
    # Start Diagnosis button
    if st.button("Start Diagnosis"):
        st.experimental_set_query_params(page="diagnosis")
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Diagnosis page
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.image("logo.png", width=120)
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
        uploaded = st.file_uploader("Upload Chest X‑ray *", type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("Analyze X‑ray")

    if submitted:
        if not uploaded:
            st.error("Please upload an X‑ray image.")
        else:
            # Display original image
            img = Image.open(uploaded).convert("RGB")
            img = img.resize((512, 512))
            st.image(img, caption="Original Chest X‑ray", use_column_width=True)

            # Generate fake heatmap
            arr = np.array(img)
            x = np.linspace(-1, 1, 512)
            y = np.linspace(-1, 1, 512)
            xv, yv = np.meshgrid(x, y)
            blob = np.exp(-((xv + 0.3) ** 2 + (yv + 0.3) ** 2) * 8) + np.exp(-((xv - 0.2) ** 2 + (yv - 0.2) ** 2) * 10)
            blob /= blob.max()
            heat = np.uint8(255 * blob)
            heatmap = np.zeros((512, 512, 3), dtype=np.uint8)
            heatmap[..., 0] = heat

            overlay = np.clip(arr * 0.6 + heatmap * 0.4, 0, 255).astype(np.uint8)
            st.image(overlay, caption="AI Attention Heatmap", use_column_width=True)

            # Diagnosis & explanation
            st.success("**Diagnosis:** Pneumonia Detected")
            st.write("**Explanation:** Highlighted regions show consolidation.")

            # Report preview & download
            st.header("Report Preview")
            st.write(f"**Name:** {name}")
            st.write(f"**Age:** {age}")
            st.write(f"**Gender:** {gender}")
            st.write(f"**Symptoms:** {symptoms or 'N/A'}")
            st.write(f"**Physical Activity:** {activity}")
            st.write(f"**Exposure:** {exposure or 'N/A'}")
            st.write(f"**Smoking History:** {smoking}")
            st.write(f"**Heart Rate Variability:** {hrv or 'N/A'}")

            st.download_button(
                "Download Word Report",
                data=generate_docx(name, age, gender, symptoms, activity, exposure, smoking, hrv),
                file_name=f"Report_{name.replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

    st.markdown("</div>", unsafe_allow_html=True)
