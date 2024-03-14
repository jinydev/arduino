/*
 *  스텝모터 정역회전
 */

// 스텝모터 라이브러리
#include <Stepper.h>  

// 한바퀴에 해당하는 값 선언
// (28BYJ-48인 경우 2048로)
int steps = 2048;

// 스텝모터 객체 선언 (INT4, INT2, INT3, INT1) 순서
Stepper stepper(steps,  11, 9, 10, 8);

void setup() {
  // rpm : 1분당 도는 횟수, 너무 큰값을 하면 안돌아감
  stepper.setSpeed(10); 
}

void loop() {
  stepper.step(steps);  // steps, 2048로 두면 정회전 한바퀴
  delay(1000);
  stepper.step(-steps); // -steps, -2048로 두면 역회전 한바퀴
  delay(1000);
}
