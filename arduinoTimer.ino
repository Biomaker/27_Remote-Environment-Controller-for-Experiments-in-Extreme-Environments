// This programs the pi to swith the power mosfet on and off. 
// The power mosfet gate is connected to pin 3

int mosfetSwitchPin=3;
int timeOn=1; // Time raspberry pi is powered in seconds [s]
int timeOff=10 ; // Time raspberry pi is off [s]

void setup(){
  pinMode(mosfetSwitchPin, OUTPUT); 
}

void loop(){

  digitalWrite(mosfetSwitchPin,HIGH); // Switch pi on
  delay(timeOn*1000);
  
  digitalWrite(mosfetSwitchPin, LOW); // Switch pi off
  delay(timeOff*1000);
  
}
