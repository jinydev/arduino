// L298N motor driver
//
#define ENB 6
#define IN3 9
#define IN4 10

#define ENCODER_B_A 2
#define ENCODER_B_B A0

byte encoderBLast;
bool encoderBDir = true;
int encoderBCount = 0;
bool active_A = false;

int distance= 0;
unsigned long speedTime;
unsigned long lastTime = 0;
bool logging = false;

int speed = 50;
void setSpeed(int s)
{
  speed = s;
}



void ISR_encoderB() {
  byte encoderBA = digitalRead(ENCODER_B_A);

  // 펄스 스피드 millis(); //
  unsigned long currTime = micros();
  speedTime = currTime - lastTime;
  lastTime = currTime;
  

  // 방향체크
  if (encoderBLast == LOW && encoderBA == HIGH) {
    byte encoderBB = digitalRead(ENCODER_B_B);
    if (encoderBB == LOW) {
      encoderBDir = true;
    } else if (encoderBB == HIGH) {
      encoderBDir = false;
    }
  }
  encoderBLast = encoderBA;

  // 회전 카운트
  if (encoderBDir) {
    encoderBCount++;
  } else {
    encoderBCount--;
  }

  if (encoderBDir) {
    if(encoderBCount > distance) {
      dc_stop();
    }
  } else {
    
    if(encoderBCount < distance) {
      dc_stop();
    }
  }
  
  
  
}

void setup() {
  Serial.begin(115200);
  
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  pinMode(ENCODER_B_A, INPUT);
  pinMode(ENCODER_B_B, INPUT);
  
  attachInterrupt(digitalPinToInterrupt(ENCODER_B_A), ISR_encoderB, FALLING);

  
}


void loop() {

  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == 'f') {
      Serial.println("forward");
      distance = 0;
      
      dc_forward();
      logging = true;
    } if (cmd == 'b') {
      Serial.println("backward");
      distance = 960; // 8펄스 * 120 기어비 = 960 한바퀴
      // 정밀도 = 360 / 960 = 0.09
      dc_backward();
      logging = true;
    } else if (cmd == 's') {
      Serial.println("stop");

      Serial.print(", distance = ");
      Serial.print(distance);

      Serial.print(" encoderB = ");
      Serial.print(encoderBCount);
      
      dc_stop();
      logging = false;
    } 
  }

  unsigned long currTime = millis();
  if (active_A ) {
    Serial.print("speedB = ");
    Serial.print(speedTime);

    Serial.print(", distance = ");
    Serial.print(distance);

    Serial.print(" encoderB = ");
    Serial.print(encoderBCount);
    
    Serial.println();
    //lastTime = currTime;
  }
  
}






void dc_backward()
{
  
    if(!active_A) {
      //digitalWrite(IN3, HIGH);
      analogWrite(IN3, speed); // 모터 스피드 pwm 
      
      digitalWrite(IN4, LOW);    
      
      
      analogWrite(ENB, 125);
  
      //동작시작
      active_A = true;
    } 

}

void dc_forward()
{
 
    if(!active_A) {
      digitalWrite(IN3, LOW);

      //digitalWrite(IN4, HIGH);
      analogWrite(IN4, speed); // 모터 스피드 pwm
    
      analogWrite(ENB, 125);
  
      //동작시작
      active_A = true;
    }

    
}

void dc_stop()
{
  if(active_A) {
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
    analogWrite(ENB, 0);

    //동작시작s
    active_A = false;
  }
}
