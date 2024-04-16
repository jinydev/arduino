---
typora-root-url: img
typora-copy-images-to: img
---



# 압력센서

이번 시간에는 어떠한 물체의 무게를 측정해 볼 수 있는 압력 센서에 대해서 알아 보도록 하겠습니다.





## 실습 부품

다음과 같이 실습 부품이 필요로 합니다. 압력센서는 크기와 측정 가능한 무게에 따라서 가격이 많이 차이가 납니다.



![image-20220625202137728](/image-20220625202137728.png)









## 시뮬레이션



https://www.tinkercad.com/things/lqXgEmeai1U





![image-20220625203801778](/image-20220625203801778.png)





```
// 센서값을 읽기 위해 아날로그핀 0번을 지정한다.
const int FlexPin = A0; 
const int led =9;

void setup()
{
  // 센서값을 읽기 위해 시리얼 모니터를 사용할 것을 설정.
  Serial.begin(9600); 
  pinMode(led,OUTPUT);
}

void loop()
{
  int FlexVal; // 센서값을 저장할 변수
  
  // 아날로그를 입력 받음 (0~1023)
  FlexVal = analogRead(FlexPin); 

  // 시리얼 모니터로 출력
  // sensor: 라는 텍스트를 프린트한다.
  Serial.print("sensor: "); 
  // flexVal의 값을 출력후 줄바꿈을 한다.
  Serial.println(FlexVal); 
  
  int lightValue = map(FlexVal, 864,1023, 0,255);
  analogWrite(led, lightValue);


  delay(500);
}
```

