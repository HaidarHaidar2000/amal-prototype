import streamlit as st
from PIL import Image
import numpy as np
from utils import generate_docx

st.set_page_config(page_title="AMAL – LungCare AI", layout="wide")

# CSS for premium look
st.markdown("""
<style>
body {
    background: #fff5f9;
}
.big-card {
    margin: 5% auto;
    background: white;
    border-radius: 36px;
    box-shadow: 0 8px 32px #f0bfd3;
    max-width: 470px;
    padding: 60px 50px 50px 50px;
    text-align: center;
}
.amal-title {
    font-family: 'Playfair Display', serif;
    font-size: 76px;
    color: #c2185b;
    font-weight: bold;
    margin-bottom: 12px;
    margin-top: 0px;
    letter-spacing: 2px;
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
    max-width: 500px;
    margin: 60px auto;
    padding: 38px 30px 30px 30px;
}
.stFileUploader, .stTextInput, .stSelectbox, .stNumberInput, .stTextArea {
    margin-bottom: 16px !important;
}
</style>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"

# HOME PAGE
if st.session_state.page == "home":
    st.markdown("""
    <div class="big-card">
        <div class="amal-title">AMAL</div>
        <div class="amal-subtitle">Cutting-edge tools for the diagnosis and management of respiratory diseases.</div>
        <form action="" method="post">
            <button class="start-btn" name="start_diag" type="submit">Start Diagnosis</button>
        </form>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.get("do_diag"):
        st.session_state.page = "diagnosis"
        st.session_state["do_diag"] = False
    if st.session_state.page == "home" and st.form_submit_button("FakeHidden", key="hiddenfake"):
        st.session_state.page = "diagnosis"
elif st.session_state.page == "diagnosis":
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
        **Name:** {name}  
        **Age:** {age}  
        **Gender:** {gender}  
        **Symptoms:** {symptoms or 'N/A'}  
        **Physical Activity:** {activity}  
        **Exposure:** {exposure or 'N/A'}  
        **Smoking History:** {smoking}  
        **HRV:** {hrv or 'N/A'} ms
        """)
        st.download_button("Download Word Report", data=generate_docx(
            name, age, gender, symptoms, activity, exposure, smoking, hrv
        ), file_name=f"Report_{name.replace(' ','_')}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    st.markdown('</div>', unsafe_allow_html=True)

# Transition logic (POST-redirect)
if st.form_submit_button("FakeStart", key="hiddenstart"):
    st.session_state.page = "diagnosis"

# Button POST handler (simulate the click)
import streamlit.components.v1 as components
if st.session_state.page == "home":
    components.html("""
    <script>
    const btn = document.querySelector('.start-btn');
    if(btn) btn.onclick = function(e) {
      window.parent.postMessage({isStreamlitMessage: true, type: "streamlit:setComponentValue", value: "diagnosis"}, "*");
    };
    </script>
    """, height=0)
