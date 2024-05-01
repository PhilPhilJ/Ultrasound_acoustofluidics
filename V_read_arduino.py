import serial
import numpy as np

# Thermocouple function
def thermocouple(V_thermocouple_1, V_thermocouple_2):
    # Polynominal coefficients (0C - 500C) - Source: https://srdata.nist.gov/its90/type_k/kcoefficients_inverse.html
    d0 = 0
    d1 = 2.508355 * 10
    d2 = 7.860106 * 10 ** -2
    d3 = -2.503131 * 10 ** -1
    d4 = 8.315270 * 10 ** -2
    d5 = -1.228034 * 10 ** -2
    d6 = 9.804036 * 10 ** -4
    d7 = -4.413030 * 10 ** -5
    d8 = 1.057734 * 10 ** -6
    d9 = -1.052755 * 10 ** -8

    # Voltage of the thermocouple
    V_thermocouple = abs(V_thermocouple_1 - V_thermocouple_2)*10**(3)

    # Temperature of the thermocouple
    temp_thermocouple = d0 + d1 * V_thermocouple + d2 * V_thermocouple ** 2 + d3 * V_thermocouple ** 3 + d4 * V_thermocouple ** 4 + d5 * V_thermocouple ** 5 + d6 * V_thermocouple ** 6 + d7 * V_thermocouple ** 7 + d8 * V_thermocouple ** 8 + d9 * V_thermocouple ** 9

    return temp_thermocouple


# Define the Arduino board port
port = 'COM3'  # Replace with the appropriate port
baudrate = 9600  # Replace with the appropriate baudrate

# Create a serial connection
arduino = serial.Serial(port, baudrate, timeout=1)

# Main loop
while True:
    if arduino.readline().decode().strip("utf-8"):
        # Read the voltage from the analog pins
        raw_temp_tc = arduino.readline().decode().strip("utf-8")
        temp_tc = float(np.copy(raw_temp_tc))



