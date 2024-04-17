---
layout: home
typora-root-url: img
typora-copy-images-to: img
---

# 플랙스 센서



## 실습부품

실습을 위하여 다음과 같은 플렉스 센서를 준비 합니다. 플렉스 센서는 길이에 따라서 가격이 틀려집니다.

![image-20220625185409265](/image-20220625185409265.png)







## 플랙스 센서 알아보기

`플렉스` 센서 또는 `휨`센서 라고도 합니다.



![image-20220625185558079](/image-20220625185558079.png)

플렉스 센서는 휘어지는 정보에 따라 내부의 저항을 변화하는 가변저항의 일종입니다.

#### 특징

* 극성이 존재하지 않는다.



## 연결하기

플렉스 센서는 가변저항의 일종으로 두개의 저항을 연결하고, 저항에 걸리는 전압을 측정하여 힘 정도를 알아 냅니다.



![image-20220625190752604](/image-20220625190752604.png)





## 측정값 읽기

분배된 전압값을 읽기 위해서는 아두이노의 `아날로그 입력핀`을 사용합니다. 

> 아날로그 입력: 아두이노는  A0~A5 까지 6개의 아날로그 입력 핀을 가지고 있습니다.



아날로그 함수

```
출력값 = analogRead(핀);
```



`analogRead()` 함수는 입력된 핀의 전압을 측정하여 10bit 값으로 출력합니다.



## 시뮬레이션

싱커캐드를 이용하여 플렉스 센서의 동작을 사전 연습해 보도록 합니다. 다음과 같이 회로를 연결합니다.



https://www.tinkercad.com/things/1Ef6aSUe7oG?sharecode=bULrDaiJcrFi-nxPkBtEv1kpaQqlSUYqD9UI0eWfFSo





![image-20220625190005179](/image-20220625190005179.png)



```
// 센서값을 읽기 위해 아날로그핀 0번을 FlexPin에 지정한다.
const int FlexPin = A0; 

void setup()
{
  // 센서값을 읽기 위해 시리얼 모니터를 사용할 것을 설정.
  Serial.begin(9600); 
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

  delay(500);
}
```





## 시뮬레이션2 : 플렉스 센서 움직임에 따라 LED 불 밝기 변화하기



https://www.tinkercad.com/things/1Ef6aSUe7oG?sharecode=bULrDaiJcrFi-nxPkBtEv1kpaQqlSUYqD9UI0eWfFSo



![image-20220625201619869](/image-20220625201619869.png)



```
// 센서값을 읽기 위해 아날로그핀 0번을 FlexPin에 지정한다.
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
  
  int lightValue = map(FlexVal, 990,1017, 0,255);
  analogWrite(led, lightValue);


  delay(500);
}
```





#### 매핑으로 값 변환하기

아두이노의 아날로그 입력은  10bit의 값으로 0~1024 사이의 값을 가지고 있습니다. 또한 플랙스 센서와 외부 저항을 같이 직열로 연결하여 센서에만 가해진 저항의 전압값 만을 측정하게 됩니다.



예를들어) 플렉스 센서와 외부저항 1kΩ을 연결할때 최소값 990과 최대값 1017을 가지게 됩니다. 즉 플렉스 센서의 움직임의 폭은 27사이의 값이 됩니다. 이를 PWM을 통하여 LED 밝기를 조절하고자 할때 990~1017 사이의 값을 PWM 0~255 사이의 값으로 적절히 변환을 해주어야 합니다.



아두이노는 이러한 범위를 쉽게 변환할 수 있도록 `map()` 함수를 제공합니다. 



![image-20220625200634326](/image-20220625200634326.png)