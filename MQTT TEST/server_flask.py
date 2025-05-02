from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    # Simulasi nilai sensor yang berubah-ubah
    temperature = round(random.uniform(25.0, 35.0), 2)
    humidity = round(random.uniform(40.0, 80.0), 2)

    # Tentukan status berdasarkan suhu
    if temperature > 30:
        status = "Panas"
    elif temperature < 26:
        status = "Dingin"
    else:
        status = "Normal"

    # Mengirimkan data dalam format JSON
    return jsonify({
        "temperature": temperature,
        "humidity": humidity,
        "status": status
    })

if __name__ == '__main__':
    app.run(port=5000)
