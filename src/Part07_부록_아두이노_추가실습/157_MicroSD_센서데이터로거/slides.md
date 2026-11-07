# 157_MicroSD_센서데이터로거 💾📁

![도로시와 지니의 MicroSD 센서 데이터 로거 탐구](./img/dorothy_microsd_datalogger.jpg)

**도로시와 지니가 함께하는 SPI 통신 기반 MicroSD 모듈 제어, FAT 파일 시스템, CSV 데이터 기록 및 엑셀(Excel) 그래프 시각화**
* 👧 **도로시**: "지니야! 식물 화분의 온도와 습도가 하루 종일, 일주일 내내 어떻게 변하는지 컴퓨터 연결 없이도 차곡차곡 기록해 둘 수 있어?"
* 🐱 **지니**: "그럼! 스마트폰이나 블랙박스에 들어가는 **마이크로 SD 카드(MicroSD Card)** 를 아두이노에 연결하면 기가바이트(GB) 단위의 대용량 텍스트 파일(`datalog.csv`)로 센서 측정값을 끝없이 기록할 수 있단다!"
* 🐶 **토토**: "바우! 기록된 SD 카드를 컴퓨터에 꽂아 엑셀로 멋진 꺾은선 그래프를 그려보자 멍!"
* 📖 **상세 강의 교재**: [index.md](./index.md)


> 여러분 안녕하세요! 이번 시간에는 '157. MicroSD 센서데이터로거 💾📁'을 주제로 함께 흥미진진한 탐험을 떠나보겠습니다. 오늘 강의에서는 특히 도로시와 지니가 함께하는 SPI 통신 기반 MicroSD 모듈 제어, FAT 파일 시스템, CSV 데이터 기록 및 엑셀(Excel) 그래프 시각화, 👧 도로시: "지니야! 식물 화분의 온도와 습도가 하루 종일, 일주일 내내 어떻게 변하는지 컴퓨터 연결 없이도 차곡차곡 기록해 둘 수 있어?"를 중심으로 핵심 원리와 응용 방법을 차근차근 배워보겠습니다. 마법 멘토 지니와 호기심 많은 탐험가 도로시, 그리고 귀여운 토토와 함께 신나는 아두이노 모험을 힘차게 시작해 봅시다. 준비되셨나요?

---
## 1. MicroSD 모듈과 파일 시스템의 이해


![](./img/dorothy_fat32_csv_structure.jpg)

1. **FAT(File Allocation Table) 파일 시스템**:
* 아두이노 표준 `SD.h` 라이브러리는 **FAT16** 및 **FAT32** 형식으로 포맷된 32GB 이하의 마이크로 SD 카드를 완벽하게 지원합니다. (exFAT는 지원하지 않으므로 PC에서 포맷할 때 FAT32로 지정해야 합니다.)
2. **8.3 파일 이름 규칙**:
* 아두이노의 메모리 절약을 위해 파일 이름은 **영문 최대 8자 + 확장자 3자** (예: `DATALOG.CSV`, `TEMP_LOG.TXT`)를 사용합니다.
3. **CSV(쉼표로 구분된 값)의 마법**:
* 각 측정값을 쉼표(`,`)로 구분하여 한 줄씩 기록하면(`시간,온도,습도`), 마이크로소프트 엑셀(Excel)이나 구글 스프레드시트에서 더블 클릭만으로 바로 열어 표와 꺾은선 그래프로 시각화할 수 있습니다!

### 📁 FAT16/FAT32 파일 시스템과 CSV(Comma-Separated Values) 형식

> 이번 슬라이드에서는 '1. MicroSD 모듈과 파일 시스템의 이해'에 대해 자세히 살펴보겠습니다. 첫 번째 핵심은 FAT(File Allocation Table) 파일 시스템이며, 두 번째로는 아두이노 표준 SD.h 라이브러리는 FAT16 및 FAT32 형식으로 포맷된 32GB 이하의 마이크로 SD 카드를 완벽하게 지원합니다. (exFAT는 지원하지 않으므로 PC에서 포맷할 때 FAT32로 지정해야 합니다.)입니다. 여기에 덧붙여 파일 이름 규칙 내용까지 함께 이해해 두시면 완벽합니다. 이 원리는 아두이노 시스템 전체를 관통하는 핵심 논리이므로 머릿속에 꼭 정리해 두시기 바랍니다.
---
## 2. MicroSD 모듈 핀 구조와 SPI 배선표


![](./img/dorothy_microsd_spi_pinmap.jpg)

* [!NOTE]
* MicroSD 모듈에는 내부에 5V ➔ 3.3V LDO 레귤레이터와 74LVC125 레벨 시프터 IC가 내장되어 있어 아두이노의 5V 신호와 안전하게 직결할 수 있습니다.

* **환경 센서 (DHT11 온습도 센서)**:
* 신호(DATA)선 ➔ **D2**
* VCC ➔ 5V, GND ➔ GND

| MicroSD 모듈 핀 | 기능 설명 | 아두이노 우노(Uno) 연결 핀 |
| :---: | :--- | :---: |
| **VCC** | 모듈 전원 공급선 (5V) | **5V** |
| **GND** | 공통 접지선 | **GND** |
| **MISO** | SPI 마스터 수신 데이터선 | **D12 (MISO)** |
| **MOSI** | SPI 마스터 송신 데이터선 | **D11 (MOSI)** |
| **SCK** | SPI 공통 클록 동기화선 | **D13 (SCK)** |
| **CS** | 슬레이브 선택선 (Chip Select) | **D4** (또는 D10) |

> 이번에 살펴볼 내용은 '2. MicroSD 모듈 핀 구조와 SPI 배선표'입니다. 슬라이드에 정리된 표를 통해 각 항목의 특징과 수치, 차이점을 한눈에 비교해 보실 수 있습니다. 첫째로 환경 센서 (DHT11 온습도 센서)에 유의해야 하며, 둘째로 신호(DATA)선 ➔ D2라는 점이 핵심입니다. 이 기본 개념을 확실히 잡아두셔야 실제 부품을 브레드보드에 꽂고 코딩할 때 실수 없이 완성할 수 있습니다.
---
## 3. 실습 예제: 온습도 데이터를 CSV 파일로 기록하는 독립형 데이터 로거


![](./img/dorothy_sd_logger_code_flow.jpg)

내장된 `SPI.h`, `SD.h` 및 `DHT sensor library`를 활용한 데이터 로깅 스케치입니다.

```cpp
#include <SPI.h>
#include <SD.h>
#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11
#define CS_PIN 4      // SD 모듈 Chip Select 핀
#define LED_WRITE 8   // 데이터 쓰기 알림 LED

DHT dht(DHTPIN, DHTTYPE);
unsigned long recordCount = 0;

void setup() {
  Serial.begin(9600);
  pinMode(LED_WRITE, OUTPUT);
  dht.begin();
  
  Serial.println("==========================================");
  Serial.println("💾 도로시의 스마트 환경 데이터 로거 가동!");
  Serial.println("MicroSD 카드를 초기화합니다...");
  
  // SD 카드 마운트 초기화
  if (!SD.begin(CS_PIN)) {
    Serial.println("❌ SD 카드 초기화 실패! 카드가 제대로 꽂혀 있는지, FAT32 포맷인지 확인하세요.");
    while (1) {
      // 에러 알림: LED 무한 깜빡임
      digitalWrite(LED_WRITE, HIGH); delay(200);
      digitalWrite(LED_WRITE, LOW); delay(200);
    }
  }
  Serial.println("✅ SD 카드 인식 성공!");
  
  // CSV 파일 헤더(열 제목) 최초 작성
  File dataFile = SD.open("DATALOG.CSV", FILE_WRITE);
  if (dataFile) {
    // 파일이 처음 생성되는 경우 헤더 작성
    if (dataFile.size() == 0) {
      dataFile.println("Index,Time_sec,Temperature_C,Humidity_pct");
      Serial.println("📄 신규 DATALOG.CSV 파일 헤더 작성 완료.");
    }
    dataFile.close();
  }
}

void loop() {
  // 1. 센서 값 측정
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  
  // 측정 오류 검사
  if (isnan(h) || isnan(t)) {
    Serial.println("⚠️ DHT 센서 측정 실패!");
    delay(2000);
    return;
  }
  
  recordCount++;
  unsigned long timeSec = millis() / 1000;
  
  // 2. CSV 형식 문자열 조립: "1,2,24.5,58.0"
  String dataString = String(recordCount) + "," +
                      String(timeSec) + "," +
                      String(t, 1) + "," +
                      String(h, 1);
                      
  // 3. 파일 쓰기 동작 (LED 점등)
  digitalWrite(LED_WRITE, HIGH);
  File dataFile = SD.open("DATALOG.CSV", FILE_WRITE);
  
  if (dataFile) {
    dataFile.println(dataString);
    dataFile.close(); // 반드시 close() 해야 실제 플래시 메모리에 버퍼가 저장됨!
    
    Serial.print("📥 [기록 완료] ");
    Serial.println(dataString);
  } else {
    Serial.println("❌ DATALOG.CSV 파일 열기 실패!");
  }
  digitalWrite(LED_WRITE, LOW);
  
  // 5초 간격으로 주기적 로깅 (원하는 주기로 변경 가능)
  delay(5000);
}
```

> 이번 슬라이드에서는 '3. 실습 예제: 온습도 데이터를 CSV 파일로 기록하는 독립형 데이터 로거'에 대한 실제 동작 코드를 분석해 보겠습니다. 화면의 코드를 살펴보시면, 컴퓨터가 아두이노 하드웨어에 단계별로 명령을 내리는 흐름을 명확하게 확인할 수 있습니다. 각 함수의 역할과 괄호 안의 매개변수가 하드웨어 핀과 어떤 관계를 맺고 동작하는지 주의 깊게 살펴보시기 바랍니다.
---
## 4. 실습 결과 및 SD 카드 파일 확인


![](./img/dorothy_excel_csv_chart_view.jpg)

* **엑셀 꿀팁**:
* 엑셀에서 열고 **[삽입] ➔ [추천 차트] ➔ [꺾은선형]** 을 클릭하면 시간에 따른 온도 및 습도의 일일 변화 추이를 한눈에 볼 수 있습니다!

SD 카드를 분리하여 PC에 꽂고 `DATALOG.CSV` 파일을 메모장이나 엑셀로 열면 다음과 같이 정갈하게 저장되어 있습니다:

```csv
Index,Time_sec,Temperature_C,Humidity_pct
1,5,24.5,58.0
2,10,24.6,58.2
3,15,24.8,57.9
4,20,25.0,57.5
5,25,25.1,57.1
```

> 이번 슬라이드에서는 '4. 실습 결과 및 SD 카드 파일 확인'에 대한 실제 동작 코드를 분석해 보겠습니다. 화면의 코드를 살펴보시면, 컴퓨터가 아두이노 하드웨어에 단계별로 명령을 내리는 흐름을 명확하게 확인할 수 있습니다. 여기서 핵심은 엑셀 꿀팁입니다. 각 함수의 역할과 괄호 안의 매개변수가 하드웨어 핀과 어떤 관계를 맺고 동작하는지 주의 깊게 살펴보시기 바랍니다.
---
## 5. 핵심 요약 정리 💡


![도로시와 지니의 핵심 정리 및 축하](./img/dorothy_jiny_celebrate.jpg)

1. **독립형 임베디드 로거**: 컴퓨터와 USB로 연결되어 있지 않은 야외나 온실에서도 배터리만으로 수 주일 동안 센서 데이터를 자동 저장합니다.
2. **`close()` 함수의 중요성**: `dataFile.print()`는 내부 RAM 버퍼에 먼저 기록되므로, **`dataFile.close()`**를 호출해야 플래시 메모리에 물리적으로 기록이 완료됩니다.
3. **8.3 파일명 제약**: 파일명은 반드시 영문 대소문자 8글자 이내와 확장자 3글자(예: `SENSOR01.CSV`)로 지어야 합니다.
4. **CSV 호환성**: 쉼표로 구분된 데이터는 엑셀, 파이썬(Pandas), 매트랩 등 모든 데이터 과학 도구에서 즉시 분석할 수 있는 산업 표준 포맷입니다.

> 오늘 배운 '5. 핵심 요약 정리 💡'의 핵심 내용을 모두 정리해 보았습니다. 오늘 다룬 내용 중에서도 독립형 임베디드 로거: 컴퓨터와 USB로 연결되어 있지 않은 야외나 온실에서도 배터리만으로 수 주일 동안 센서 데이터를 자동 저장합니다. 부분은 앞으로의 아두이노 실습과 프로젝트에서 계속 사용되는 매우 중요한 기초 지식입니다. 오늘 배운 내용을 꼭 다시 한번 복습해 보시고, 다음 강의에서 더욱 신나고 유익한 모험으로 다시 만나겠습니다. 모두 수고 많으셨습니다!