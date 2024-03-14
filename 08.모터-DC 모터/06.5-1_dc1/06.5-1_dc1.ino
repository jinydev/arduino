// L298n 모터연결
const int IN1 = 8;
const int IN2 = 9;

// 아두이노 포트 초기화
void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
}

void loop() {
  // =====
  // 정방향 : IN1 - LOW, IN2 - HIGH
  digitalWrite(IN1, LOW);

  // IN2 : PWM (펄스폭)
  for(int i=0;i<255;i++) {
    analogWrite(IN2,i);
    delay(50);
  }

  // 점점 속도 감소
  for(int i=255;i>0;i--) {
    analogWrite(IN2,i);
    delay(50);
  }

  // =====
  // 역방향 : IN1 - HIGH, IN2 - LOW
  digitalWrite(IN2, LOW);

  // IN1 : PWM (펄스폭)
  for(int i=0;i<255;i++) {
    analogWrite(IN1,i);
    delay(50);
  }

  // 점점 속도 감소
  for(int i=255;i>0;i--) {
    analogWrite(IN1,i);
    delay(50);
  }
  
}
