#include "max6675.h"

int thermoDO = 5;
int thermoCS = 6;
int thermoCLK = 7;
int flow = 2;
int valve = 4;
int serial_out = 0;

MAX6675 thermocouple(thermoCLK, thermoCS, thermoDO);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(flow, OUTPUT);
  pinMode(valve, OUTPUT);
  // wait for MAX chip to stabilize
  delay(500);
}

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.print("C = "); 
  Serial.println(thermocouple.readCelsius());
  // reply only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    serial_out = Serial.parseInt(); 
    Serial.read();
  if (serial_out==0) {
    digitalWrite(flow, LOW);
  }
  else if (serial_out==1) {
    digitalWrite(flow, HIGH);
  }
  else if (serial_out==2) {
    digitalWrite(valve, LOW);
  }
  else if (serial_out==3) {
    digitalWrite(valve, HIGH);
  }
  else {
    digitalWrite(flow, LOW);
    digitalWrite(valve, LOW);
  }
  }
  // For the MAX6675 to update, you must delay AT LEAST 250ms between reads!
  delay(250);
}
