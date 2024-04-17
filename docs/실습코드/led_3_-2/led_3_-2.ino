
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(2, HIGH);
  delay(1000);
  digitalWrite(2, LOW); 
  delay(1000);
  
  digitalWrite(3, HIGH);
  delay(1000);
  digitalWrite(3, LOW);
  delay(1000);
  
  digitalWrite(4, HIGH);
  delay(1000);                       
  digitalWrite(4, LOW);
  delay(1000);                       
  
}
