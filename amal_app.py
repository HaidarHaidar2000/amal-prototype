
import streamlit as st
from PIL import Image
import time

st.set_page_config(page_title="AMAL Prototype", layout="centered")

st.title("🫁 AMAL - AI-Powered Lung Diagnosis")
st.markdown("**Hope Begins With a Breath**")

# Patient Info
st.header("1. Patient Information")
name = st.text_input("Name")
age = st.number_input("Age", min_value=0, step=1)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
symptoms = st.text_area("Symptoms (optional)")

# Upload X-ray
st.header("2. Upload Chest X-ray")
uploaded_file = st.file_uploader("Upload image (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Chest X-ray", use_column_width=True)

    with st.spinner("Analyzing X-ray with AI..."):
        time.sleep(2.5)

    st.header("3. Diagnosis Result")
    st.success("🔍 Pneumonia detected")

    st.header("4. Explanation")
    st.markdown(
        """
        The AI model detected abnormal opacities in the lower left lung zone,
        with irregular patterns suggestive of fluid buildup. This pattern is commonly associated with **Pneumonia**.
        """
    )

    st.header("5. Patient Summary")
    st.markdown(f"- **Name**: {name or 'Not provided'}")
    st.markdown(f"- **Age**: {age if age else 'Not provided'}")
    st.markdown(f"- **Gender**: {gender}")
    st.markdown(f"- **Symptoms**: {symptoms or 'None provided'}")

    st.markdown("---")
    st.caption("🧪 This is a demo prototype for ITEX 2025. Not for clinical use.")
