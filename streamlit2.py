import streamlit as st
import requests
import time

FASTAPI_URL = "http://127.0.0.1:8000/"

st.title("Monitoring Data dari ESP32 (Dummy Realtime)")

# Tempat untuk menampilkan metrik
temp_placeholder = st.empty()
hum_placeholder = st.empty()
time_placeholder = st.empty()

# Loop realtime
while True:
    try:
        # Panggil endpoint untuk generate data dummy baru
        requests.post(f"{FASTAPI_URL}/generate")

        # Ambil data dari FastAPI
        res = requests.get(f"{FASTAPI_URL}/data")
        if res.status_code == 200:
            data = res.json()
            temp_placeholder.metric("Suhu (°C)", data['temperature'])
            hum_placeholder.metric("Kelembaban (%)", data['humidity'])
            time_placeholder.write("Terakhir diperbarui: " + time.ctime(data['timestamp']))
        else:
            st.error("Gagal mengambil data")
    except Exception as e:
        st.error(f"Error: {e}")

    # Tunggu 2 detik sebelum update lagi
    time.sleep(2)
