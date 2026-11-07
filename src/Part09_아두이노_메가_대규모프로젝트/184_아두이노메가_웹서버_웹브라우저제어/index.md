---
layout: docs
title: "184_아두이노메가_웹서버_웹브라우저제어 🌍💻"
---

# 184_아두이노메가_웹서버_웹브라우저제어 🌍💻

![](./img/dorothy_digital_portal.jpg)

**도로시와 지니가 함께하는 초소형 HTTP 웹서버와 원격 스마트 제어**

* 👧 **도로시**: "지니야! 크롬이나 사파리 웹 브라우저 주소창에 아두이노 IP를 치면 웹페이지가 열려?"
* 🐱 **지니**: "그럼! 아두이노가 작은 **웹 서버(Web Server)** 가 되어 HTML 홈페이지를 띄우고 버튼을 클릭하면 불을 켤 수 있단다!"
* 🐶 **토토**: "바우! 클릭 한 번으로 불이 번쩍 켜진다 멍!"

* 🖥️ **강의 슬라이드**: [slides.md](./slides.md)

---

## 1. 아두이노 웹서버(Web Server)의 원리

![아두이노 로고](../../img/arduino_logo.png)

### 🌍 HTTP 프로토콜의 대화 규칙
1. **클라이언트 (스마트폰/PC)**:
   * 웹 브라우저 주소창에 `http://192.168.0.50` 입력 후 접속!
2. **아두이노 웹서버 (포트 80)**:
   * "손님이 오셨네!" 하며 HTML 코드를 한 줄씩 손님에게 전송해요.
3. **웹페이지 렌더링**:
   * 브라우저에 **[LED ON]**, **[LED OFF]** 버튼이 예쁘게 나타납니다!

---

## 2. 웹서버 스케치 핵심 코드 구조

![](./img/dorothy_multi_arduino_talk.jpg)

### 💻 `EthernetServer` 클래스 활용

```cpp
#include <SPI.h>
#include <Ethernet.h>

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
EthernetServer server(80); // 80번 표준 웹 포트로 서버 개방

void setup() {
  Ethernet.begin(mac);
  server.begin(); // 웹서버 청취 시작!
  pinMode(8, OUTPUT);
}
```

---

## 3. 클라이언트 요청 분석 및 HTML 응답

![](./img/dorothy_web_buttons.jpg)

### 📄 웹 브라우저로 HTML 홈페이지 전송

```cpp
void loop() {
  EthernetClient client = server.available(); // 접속한 손님 확인
  if (client) {
    // HTTP 헤더 및 HTML 본문 응답 전송
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println();
    client.println("<h1>Dorothy Smart Home</h1>");
    client.println("<p><a href=\"/?on\"><button>LED ON</button></a></p>");
    client.println("<p><a href=\"/?off\"><button>LED OFF</button></a></p>");
    client.stop(); // 클라이언트 접속 종료
  }
}
```

---

## 4. 클라우드 IoT 연동 (MQTT & Blynk)

![](./img/dorothy_cloud_iot.jpg)

### ☁️ 전 세계 어디서든 대시보드로 관찰!

* **MQTT 프로토콜**:
  * 가볍고 빠른 사물인터넷 전용 메시지 규약으로 센서 데이터를 1초마다 클라우드로 전송!
* **씽스피크(ThingSpeak)**:
  * 아두이노 온도/습도 데이터를 24시간 실시간 그래프로 기록해 주는 IoT 분석 서버!
* **블링크(Blynk)**:
  * 스마트폰 앱 위젯으로 전 세계 어디서든 집안 전등을 켜는 클라우드 솔루션!

---

## 🌟 도로시와 지니의 핵심 요약 노트!

![](./img/dorothy_jiny_celebrate.jpg)

* 👧 **도로시**: "아두이노가 웹서버가 되어 HTML 페이지를 띄우고 브라우저 버튼으로 핀을 조종할 수 있구나!"
* 🐱 **지니**: "맞아! 메가 2560의 하드웨어 스펙부터 FreeRTOS, 3D 프린터, 유선 이더넷 웹서버까지 대형 프로젝트의 모든 것을 완벽히 마스터했단다!"
* 🐶 **토토**: "바우! 다음 Part 10에서는 초소형 리눅스 컴퓨터인 라즈베리파이의 세계로 모험을 떠나보자 멍!"
