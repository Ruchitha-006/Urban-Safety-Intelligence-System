import streamlit as st
import requests
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Urban Safety", layout="wide")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- GLASS UI CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.glass {
    backdrop-filter: blur(15px);
    background: rgba(255,255,255,0.1);
    padding: 30px;
    border-radius: 15px;
    width: 350px;
    margin: auto;
    margin-top: 120px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN ----------------
def login_api(username, password):
    # dummy backend logic
    return username == "admin" and password == "1234"

if not st.session_state.logged_in:

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.title("🔐 Secure Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_api(user, pwd):
            st.session_state.logged_in = True
            st.success("Welcome 🚀")
            st.rerun()
        else:
            st.error("Invalid login")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DASHBOARD ----------------
else:

    st.sidebar.title("🚔 Urban Safety")
    module = st.sidebar.radio("Navigate", [
        "Dashboard", "Hotspots", "Classifier"
    ])

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("🚔 Urban Safety Analytics")

    # ---------------- DASHBOARD ----------------
    if module == "Dashboard":

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Crimes", "12,450")
        col2.metric("Hotspots", "38")
        col3.metric("Alerts", "245")

        st.line_chart(pd.DataFrame({
            "Crimes": np.random.randint(100, 500, 10)
        }))

    # ---------------- HOTSPOTS ----------------
    elif module == "Hotspots":

        st.subheader("🔥 Crime Hotspots Map")

        # Fetch data from backend
        data = requests.get("http://127.0.0.1:8000/hotspots").json()
        df = pd.DataFrame(data)

        m = folium.Map(location=[12.97, 77.59], zoom_start=11)

        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=5,
                color="red"
            ).add_to(m)

        st_folium(m, width=700)

    # ---------------- CLASSIFIER ----------------
    elif module == "Classifier":

        st.subheader("🧾 FIR Classifier")

        text = st.text_area("Enter FIR text")

        if st.button("Predict"):
            res = requests.post(
                "http://127.0.0.1:8000/predict",
                params={"text": text}
            ).json()

            st.success(f"Crime Type: {res['crime_type']}")