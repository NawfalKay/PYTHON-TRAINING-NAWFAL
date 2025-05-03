import streamlit as st
from PIL import Image
import os

# Lokasi file log dan folder foto
LOG_FILE = "absensi_log.txt"
PHOTO_DIR = "absensi_foto"

st.set_page_config(page_title="Rekap Absensi Wajah", layout="wide")
st.title("📋 Rekapitulasi Absensi Wajah")
st.markdown("---")

# Tombol reset
if st.button("🔴 Reset Data Absensi"):
    if os.path.exists(LOG_FILE):
        open(LOG_FILE, "w").close()  # Kosongkan file log
    if os.path.exists(PHOTO_DIR):
        for file in os.listdir(PHOTO_DIR):
            file_path = os.path.join(PHOTO_DIR, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    st.success("✅ Semua data absensi telah dihapus.")
    st.experimental_rerun()

# Fungsi bantu untuk membaca log
def load_absensi_data():
    data = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    timestamp, name = line.split(", ")
                    # Format nama file foto
                    photo_filename = f"{name}_{timestamp.replace(':', '-').replace(' ', '_')}.jpg"
                    photo_path = os.path.join(PHOTO_DIR, photo_filename)
                    data.append({
                        "name": name,
                        "timestamp": timestamp,
                        "photo_path": photo_path if os.path.exists(photo_path) else None
                    })
    return data

# Tampilkan data absensi
absensi_data = load_absensi_data()

if absensi_data:
    for entry in absensi_data[::-1]:
        with st.container():
            cols = st.columns([1, 2])
            with cols[0]:
                if entry["photo_path"]:
                    img = Image.open(entry["photo_path"])
                    st.image(img, width=180)
                else:
                    st.warning("Foto tidak ditemukan")
            with cols[1]:
                st.markdown(f"### 👤 {entry['name']}")
                st.markdown(f"🕒 {entry['timestamp']}")
                st.markdown("---")
else:
    st.info("Belum ada data absensi yang tercatat.")
