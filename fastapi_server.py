# fastapi_server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import time

app = FastAPI()

# Data dummy (akan terus diperbarui)
latest_data = {
    "temperature": 0,
    "humidity": 0,
    "timestamp": time.time()
}

# Allow CORS agar bisa diakses Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Endpoint untuk dapatkan data terbaru
@app.get("/data")
def get_data():
    return latest_data

# Endpoint untuk update data (simulasi ESP32 kirim data)
@app.post("/generate")
def generate_dummy_data():
    global latest_data
    latest_data = {
        "temperature": round(random.uniform(20, 35), 2),
        "humidity": round(random.uniform(40, 80), 2),
        "timestamp": time.time()
    }
    return {"status": "Data updated", "data": latest_data}
