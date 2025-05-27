import streamlit as st

st.set_page_config(page_title="AMAL – LungCare AI", layout="wide")

# CSS for premium home page look
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
</style>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# State-driven page navigation
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    st.markdown("""
    <div class="big-card">
        <div class="amal-title">AMAL</div>
        <div class="amal-subtitle">Cutting-edge tools for the diagnosis and management of respiratory diseases.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Diagnosis", key="diagnose_btn", help="Begin patient assessment", use_container_width=True):
        st.session_state.page = "diagnosis"

if st.session_state.page == "diagnosis":
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.header("Patient Information")
    # ... (rest of your diagnosis code goes here) ...
    st.markdown('</div>', unsafe_allow_html=True)
