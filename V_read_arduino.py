import serial

# Define the Arduino board port
port = 'COM3'  # Replace with the appropriate port
baudrate = 9600  # Replace with the appropriate baudrate

# Create a serial connection
arduino = serial.Serial(port, baudrate, timeout=0.5)

# Main loop
while True:
    # Read the voltage from the analog pins
    voltage1 = arduino.readline().decode().strip()
    voltage2 = arduino.readline().decode().strip()
    
    # Print the voltage values
    #print(f"Voltage on pin 0: {voltage1}")
    #print(f"Voltage on pin 1: {voltage2}")
