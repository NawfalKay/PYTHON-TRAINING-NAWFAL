import streamlit as st
import requests
import time

st.set_page_config(page_title="Monitor Suhu & Kelembapan", layout="centered")

st.title("📡 Monitor Suhu dan Kelembapan dari Flask Server")

# Fungsi untuk mengambil data dari Flask API
def fetch_data():
    try:
        response = requests.get("http://127.0.0.1:5000/api/data")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Gagal mengambil data dari server Flask"}
    except Exception as e:
        return {"error": str(e)}

# Tampilan auto-refresh setiap beberapa detik
refresh_interval = st.slider("Refresh setiap (detik):", 1, 10, 5) #

placeholder = st.empty()

while True:
    data = fetch_data()

    with placeholder.container():
        if "error" in data:
            st.error(data["error"])
        else:
            st.metric("🌡️ Suhu (°C)", data["temperature"])
            st.metric("💧 Kelembapan (%)", data["humidity"])
            st.info(f"Status: {data['status']}")
    
    time.sleep(refresh_interval)
