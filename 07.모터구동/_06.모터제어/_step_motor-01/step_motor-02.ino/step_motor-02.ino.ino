/*
 *  스탭모터 90도 회전
 */ 

#include <Stepper.h>  // 스텝모터 라이브러리 불러옴

// 한바퀴에 해당하는 값 선언
// (28BYJ-48인 경우 2048로)
int steps = 2048; 

// // 스텝모터 객체 선언 (INT4, INT2, INT3, INT1) 순서
Stepper stepper(steps,  11, 9, 10, 8);  

void setup() {
  // rpm : 1분당 도는 횟수, 너무 큰값을 하면 안돌아감
  stepper.setSpeed(2); 
}

void loop() {
  for(int ii=0; ii<=4; ii++){   // 총 4회 반복
    stepper.step(steps/360*90); // 1회에 90도씩 회전
    delay(500);                 // 0.5초간 쉼
  }
  for(int ii=1; ii<=60; ii++){  // 60회 반복
    stepper.step(steps/360*6);  // 1회에 6도씩 회전(시계 초침)
    delay(500);                 // 0.5초간 쉼 -> 0.5초간 초침 움직이고 0.5초간 쉼: 1초
  }
}
