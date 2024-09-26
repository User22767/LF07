import serial
import time

def readserial():
    # Hier den richtigen Port angeben (z.B. 'COM3' auf Windows oder '/dev/ttyUSB0' auf Linux)
    ser = serial.Serial('COM7', 9600, timeout=1)
    time.sleep(2)  # Warte auf den Start der seriellen Kommunikation

    while True:
        if ser.in_waiting > 0:
        # Lese die Daten vom seriellen Port
            data = ser.readline().decode('utf-8').rstrip()
            if data:
                print(data)
    
          
        
readserial()
