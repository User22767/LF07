from flask import Flask, jsonify, render_template
import serial
import time
import threading
import json 


app = Flask(__name__)

# Globale Variablen zum Speichern der Temperatur- und Luftfeuchtigkeitsdaten
sensor_data = {'temperature': None, 'humidity': None}

# Funktion zum Lesen der seriellen Daten
def readserial():
    global sensor_data
    ser = serial.Serial('COM7', 9600, timeout=1)
    time.sleep(2)  # Warte auf den Start der seriellen Kommunikation

    while True:
        if ser.in_waiting > 0:
            # Lese die Daten vom seriellen Port
            data = ser.readline().decode('utf-8').rstrip()
            if data:
                try:
                    # Die empfangenen Daten sind bereits im JSON-Format
                    sensor_data = json.loads(data)
                    print(f"Empfangene Daten: {sensor_data}")
                except json.JSONDecodeError as e:
                    print(f"Fehler beim Parsen der JSON-Daten: {e}")
                    sensor_data = {'temperature': None, 'humidity': None}
        time.sleep(1)  # Warte 1 Sekunde

# Flask-Routen
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def api_data():
    return jsonify(sensor_data)

if __name__ == '__main__':
    # Starte den seriellen Leseprozess in einem separaten Thread
    serial_thread = threading.Thread(target=readserial)
    serial_thread.daemon = True  # Der Thread wird beendet, wenn der Hauptprozess endet
    serial_thread.start()

    # Starte den Flask-Server
    app.run(host='0.0.0.0', port=5000)