import streamlit as st
import requests
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Urban Safety", layout="wide")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN ----------------
def login(username, password):
    return username == "admin" and password == "1234"

if not st.session_state.logged_in:

    st.title("🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(user, pwd):
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ---------------- DASHBOARD ----------------
else:

    st.sidebar.title("🚔 Urban Safety")
    module = st.sidebar.radio("Select Module", [
        "Dashboard", "Hotspots", "Classifier"
    ])

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("🚔 Urban Safety Dashboard")

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

        st.subheader("🔥 Crime Hotspots")

        try:
            data = requests.get("http://127.0.0.1:8000/hotspots").json()
            df = pd.DataFrame(data)

            m = folium.Map(location=[12.97, 77.59], zoom_start=11)

            for _, row in df.iterrows():
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=5,
                    color="red"
                ).add_to(m)

            st_folium(m, width=900)

        except:
            st.error("Backend not running!")

    # ---------------- CLASSIFIER ----------------
    elif module == "Classifier":

        st.subheader("🧾 FIR Classifier")

        text = st.text_area("Enter FIR text")

        if st.button("Predict"):

            try:
                res = requests.post(
                    "http://127.0.0.1:8000/predict",
                    params={"text": text}
                ).json()

                if "crime_type" in res:
                    st.success(f"Crime Type: {res['crime_type']}")
                else:
                    st.error(res)

            except:
                st.error("Backend not running!")