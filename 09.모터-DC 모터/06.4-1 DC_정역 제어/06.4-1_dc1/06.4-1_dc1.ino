// L298n 모터연결
const int IN1 = 8;
const int IN2 = 9;

// 아두이노 포트 초기화
void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
}

void loop() {
  
  // 정방향 회전
  M1_CW();  delay(1000);

  // 멈춤
  M1_stop();  delay(1000);

  // 역방향 회전
  M1_CCW();  delay(1000);

  // 멈춤
  M1_stop();  delay(1000);

}

// Motor1 정방향 회전
void M1_CW() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
}

// Motor1 역방향 회전
void M1_CCW()
{
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
}

// Motor1 멈춤
void M1_stop()
{
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
}
