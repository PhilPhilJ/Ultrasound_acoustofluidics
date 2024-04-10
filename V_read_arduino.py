import pyfirmata

# Define the Arduino board port
board = pyfirmata.Arduino('/dev/ttyACM0')  # Replace with the appropriate port

# Define the analog pins
analog_pin1 = board.get_pin('a:0:i')  # Replace 'a:0:i' with the pin number you want to read from
analog_pin2 = board.get_pin('a:1:i')  # Replace 'a:1:i' with the pin number you want to read from

# Main loop
while True:
    # Read the voltage from the analog pins
    voltage1 = analog_pin1.read()
    voltage2 = analog_pin2.read()

    # Print the voltage values
    print(f"Voltage on pin 0: {voltage1}")
    print(f"Voltage on pin 1: {voltage2}")