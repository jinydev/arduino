void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("hello");
  Serial.println("world");

  Serial.println(10);
  Serial.println(10,DEC);
  Serial.println(10,HEX);
  Serial.println(10,BIN);
  
}
