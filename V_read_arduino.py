import serial

# Define the Arduino board port
port = 'COM3'  # Replace with the appropriate port
baudrate = 9600  # Replace with the appropriate baudrate

# Create a serial connection
arduino = serial.Serial(port, baudrate, timeout=0.5)

# Main loop
while True:
    V_in = 5
    # Read the voltage from the analog pins
    voltage1 = float(arduino.readline().decode().strip())
    voltage2 = float(arduino.readline().decode().strip())
    voltage4 = float(arduino.readline().decode().strip())
    
    v_termo = abs(voltage1-voltage2)
    v_diff_abs = V_in-voltage4
    
    # Print the voltage values
    #print(f"Voltage on pin 0: {voltage1}")
    #print(f"Voltage on pin 1: {voltage2}")
