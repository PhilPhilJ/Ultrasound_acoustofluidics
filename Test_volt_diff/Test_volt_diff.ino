int tc_pin_1 = 0; // Pins thermocouples are allocated
int tc_pin_2 = 2;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // Sets data rate to 9600 bits/second
  pinMode(tc_pin_1, INPUT); // Define pin tc_pin_1 and tc_pin_2
  pinMode(tc_pin_2, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int tc_sensor_1 = analogRead(tc_pin_1);
  int tc_sensor_2 = analogRead(tc_pin_2);
  // Convert analog voltage (0-1023) to volts (0-5V)
  float tc_volt_1 = tc_sensor_1 * (5.0 / 1023);
  float tc_volt_2 = tc_sensor_2 * (5.0 / 1023);
  float volt_diff = abs(tc_volt_2 - tc_volt_1)*1000 ;
  // print voltages
  Serial.println("Pin 1 voltage (V)");
  Serial.println(tc_volt_1, 5);
  Serial.println("Pin 2 voltage (V)");
  Serial.println(tc_volt_2, 5);
  Serial.println("Volt diff (mV)");
  Serial.println(volt_diff, 5);

  delay(5000); 
}
