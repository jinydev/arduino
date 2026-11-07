# 📊 원본 슬라이드 2 기준 PPTX 변환 및 자동화 개발자 가이드 (Slide 2 Exact Clone Standard)

본 가이드는 제공된 **기준 파워포인트 파일(`07_1_동적_프로그래밍의_유래_with_audio.pptx`)의 ‘슬라이드 2’ (`prs.slides[1]`)** 디자인과 객체 구조를 100% 보존하고 복제하여, Markdown 형식의 교재 콘텐츠를 완벽한 품질의 프레젠테이션(`{강의명}.pptx`)으로 자동 변환하기 위한 **Python 기반 자동화 개발 표준 지침서**입니다.

강사와 학습자 피드백을 바탕으로, **(1) 원본 비율(Aspect Ratio) 100% 왜곡 없는 대형 이미지 배치**, **(2) 우측 상단 강의 듣기 버튼 제거 및 페이지 번호 단독 깔끔 배치**, **(3) 이미지 캡션 자동 연동 위치 조정**, **(4) 오디오 낭독용 순수 강의 대본 슬라이드 노트 독립 수록**, **(5) PPT 파일명을 `slides.pptx`가 아닌 `{강의명}.pptx`로 명명**하는 규격을 새롭게 표준화하였습니다.

---

## 📑 목차
1. [핵심 디자인 레이아웃 및 변경점 요약](#1-핵심-디자인-레이아웃-및-변경점-요약)
2. [슬라이드 기본 규격 및 캔버스 설정](#2-슬라이드-기본-규격-및-캔버스-설정)
3. [슬라이드 객체별 고유 ID, 좌표 및 서식 명세](#3-슬라이드-객체별-고유-id-좌표-및-서식-명세)
4. [이미지 원본 비율 보존 및 대형 배치(Aspect-Ratio Scaling) 규칙](#4-이미지-원본-비율-보존-및-대형-배치aspect-ratio-scaling-규칙)
5. [Markdown 항목과 슬라이드 슬롯 매핑 규칙](#5-markdown-항목과-슬라이드-슬롯-매핑-규칙)
6. [실행 가능한 전체 Python 변환 코드](#6-실행-가능한-전체-python-변환-코드)
7. [품질 검증 체크리스트 (QA Checklist)](#7-품질-검증-체크리스트-qa-checklist)

---

## 1. 핵심 디자인 레이아웃 및 변경점 요약

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ [07.1 동적 프로그래밍의 유래] (상단 섹션명: 17pt Bold)              01 / 18 (페이지 번호: 단독 깔끔 배치) │ ◀ 강의듣기 버튼 제거
│ 07.1.0 동적 프로그래밍(DP)의 시작과 호기심 (슬라이드 메인 제목: 28pt Bold)                               │
├────────────────────────────────────────────────────────────────────────────────────────┤ ◀ 회색 실선 사각형
│ 강화 학습과 컴퓨터 과학에서 아주 중요한 위치를 차지하는 동적 프로그래밍(DP)이라는...    │ ◀ 주요 설명 요약 (14.5pt 파란색)
│                                                                                        │
│ ┌───────────────────────────────────┐  ┌─────────────────────────────────────────────┐ │
│ │                                   │  │ • 동적 프로그래밍(DP)의 위상 (소제목: 21pt) │ │
│ │                                   │  │   강화 학습과 컴퓨터 과학 전반을...         │ │
│ │       [ 왼쪽 대형 이미지 ]        │  │                                             │ │
│ │    - 원본 비율 100% 무왜곡 보존    │  │ • 이름이 주는 첫인상 (소제목: 21pt)         │ │
│ │    - 가로 최대 5.40", 세로 4.50"   │  │   컴퓨터 메모리(RAM)를 동적으로...          │ │
│ │    - 레이아웃 최적화 중앙 정렬    │  └─────────────────────────────────────────────┘ │
│ └───────────────────────────────────┘  ┌───────────────────────┐ ┌───────────────────┐ │
│       동적 프로그래밍 인트로 개념       │ • 💡 역사적 의문      │ │   [ 강사 아바타 ]   │ │
│       (이미지 바로 아래 자동 배치)      │   컴퓨터가 보급되기도... │ │   X: 10.633"        │ │
│                                         └───────────────────────┘ │   Y: 5.150" (고정)  │ │
│                                                                   └───────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 💡 주요 개선 사항
1. **우측 상단 강의 듣기 버튼(`Shape 5`) 및 오디오 객체(`Shape 13`) 제거**: 슬라이드 상단이 복잡해지지 않도록 불필요한 버튼/아이콘을 삭제하고, 슬라이드 우측 끝 마진(`12.53인치`)에 맞추어 **페이지 번호(`Shape 3`)만 단독으로 우측 정렬**하여 깔끔하게 배치합니다.
2. **이미지 원본 비율(Aspect Ratio) 100% 보존**: 기존 템플릿의 고정 사각형 크기에 강제로 욱여넣어 발생하던 상하 늘어남/좌우 찌그러짐 현상을 완벽히 차단하고, 실제 이미지 파일의 가로세로 비율(`orig_w / orig_h`)을 계산하여 정확한 `shape.width`와 `shape.height`를 설정합니다.
3. **왼쪽 컬럼 대형 배치(Maximize Size)**: 가로 최대 `5.40인치`(13.72cm), 세로 최대 `4.50인치`(11.43cm)의 넉넉한 바운딩 박스를 할당하여 일러스트, 회로도, 사진을 시원하고 큼직하게 볼 수 있도록 배치합니다.
4. **이미지 캡션(`Shape 10`) 동적 위치 연동**: 이미지가 원본 비율에 따라 높이가 결정되면, 캡션 박스를 이미지 바로 아래(`top = image.top + image.height + 0.12인치`)로 자동 이동시켜 여백 불균형과 겹침을 방지합니다.

---

## 2. 슬라이드 기본 규격 및 캔버스 설정

| 속성 | 규격 수치 | 비고 |
| :--- | :--- | :--- |
| **슬라이드 가로 너비** | `13.33333 인치` (`12,192,000 EMU`, `33.86667 cm`) | 16:9 와이드스크린 |
| **슬라이드 세로 높이** | `7.50000 인치` (`6,858,000 EMU`, `19.05000 cm`) | 16:9 와이드스크린 |
| **화면 비율** | `16:9` | 임의 변경 금지 |
| **배경색** | Pure White (`#FFFFFF`) | Blank Layout 기준 |
| **글꼴(Font)** | `Apple SD Gothic Neo` | 문단 기본 서식 `a:defRPr`에 보존 |
| **텍스트 내부 여백** | `lIns="0" tIns="0" rIns="0" bIns="0"` | 상하좌우 여백 0pt 유지 |

---

## 3. 슬라이드 객체별 고유 ID, 좌표 및 서식 명세

| Shape ID | 역할명 | 형태 | Left / Top (인치, EMU) | Width / Height (인치, EMU) | 타이포그래피 & 서식 명세 |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **2** | **상단 섹션명** | TextBox | `0.80000"` (731,520)<br>`0.40000"` (365,760) | `8.50000"` (7,772,400)<br>`0.35000"` (320,040) | `17pt` (`sz="1700"`), **Bold**, `#0284C7`, Left 정렬, `wrap="square"`, `spAutoFit` |
| **3** | **페이지 번호 (단독)** | TextBox | `10.53000"` (9,628,632)<br>`0.40000"` (365,760) | `2.00000"` (1,828,800)<br>`0.35000"` (320,040) | `17pt` (`sz="1700"`), **Bold**, `#64748B`, **Right 정렬**, 우측 마진 `12.53"` 정렬, `wrap="none"` |
| **4** | **슬라이드 제목** | TextBox | `0.80000"` (731,520)<br>`0.78000"` (713,232) | `11.73000"` (10,725,912)<br>`0.53000"` (484,632) | `28pt` (`sz="2800"`), **Bold**, `#0F172A`, Left 정렬, 줄간격 1.03배, 앞/뒤 0pt |
| **6** | **제목 아래 구분선** | rect | `0.80000"` (731,520)<br>`1.36000"` (1,243,584) | `11.73000"` (10,725,912)<br>`0.02100"` (19,202) | 사각형 도형, 채우기 `#E2E8F0`, 테두리 없음, 그림자 없음 |
| **8** | **도입 설명** | TextBox | `0.80000"` (731,520)<br>`1.43000"` (1,307,592) | `11.73000"` (10,725,912)<br>`0.56000"` (512,064) | `14.5pt` (`sz="1450"`), Regular, `#0284C7`, Left 정렬, 줄간격 1.10배, 앞/뒤 0pt |
| **9** | **왼쪽 주요 이미지**| Picture | 원본 비율 맞춤<br>동적 좌표 계산 | 가로 최대 `5.40000"`<br>세로 최대 `4.50000"` | **원본 종횡비 100% 일치**, 왜곡률 0%, `noChangeAspect="1"` |
| **10**| **이미지 캡션** | TextBox | `0.80000"` (731,520)<br>`image.bottom + 0.12"` | `5.40000"` (4,937,760)<br>`0.35000"` (320,040) | `14pt` (`sz="1400"`), Regular, `#64748B`, Center 정렬, 줄간격 1.08배 |
| **11**| **오른쪽 상단 본문**| TextBox | `6.40000"` (5,852,160)<br>`2.36775"` (2,165,067) | `5.88395"` (5,380,286)<br>`2.56000"` (2,340,864) | **소제목**: `21pt` Bold `#0F172A`, 뒤 6pt<br>**설명**: `18pt` Regular `#334155`, 뒤 9pt, 줄간격 1.10배 |
| **12**| **오른쪽 하단 질문**| TextBox | `6.40000"` (5,852,160)<br>`5.18000"` (4,736,592) | `3.95000"` (3,611,880)<br>`1.86000"` (1,700,784) | **소제목**: `19pt` Bold `#0F172A`, 뒤 6pt<br>**설명**: `17.5pt` Regular `#334155`, 뒤 9pt, `anchor="t"` |
| **7** | **우측하단 인물사진**| Picture | `10.63300"` (9,722,815)<br>`5.15000"` (4,709,160) | `1.90000"` (1,737,360)<br>`1.90000"` (1,737,360) | `hojin.png` 투명 배경 원형 아바타 보존, `noChangeAspect="1"`, 회전 0도 |

---

## 4. 이미지 원본 비율 보존 및 대형 배치(Aspect-Ratio Scaling) 규칙

### 📐 계산 공식 및 좌표 산출
이미지가 사각형 슬롯 안에서 늘어나거나 찌그러지는 현상을 방지하기 위해 다음 알고리즘을 필수로 적용합니다.

```python
from PIL import Image
from pptx.util import Inches

# 1. 왼쪽 이미지 허용 최대 영역 정의 (대형 뷰 확보)
X_MIN = Inches(0.80)  # 좌측 시작 마진
Y_MIN = Inches(2.05)  # 상단 시작 마진 (도입 설명문 아래)
W_BOX = Inches(5.40)  # 최대 가로 폭 (우측 본문 시작 6.40" 전까지 충분한 여백 확보)
H_BOX = Inches(4.50)  # 최대 세로 높이 (캡션 공간 0.47" 확보)

# 2. 이미지 원본 해상도 및 종횡비(Aspect Ratio) 추출
with Image.open(img_path) as im:
  orig_w, orig_h = im.size
aspect = orig_w / orig_h
box_aspect = W_BOX / H_BOX

# 3. 무왜곡 비율 맞춤 (Fit without distortion)
if aspect >= box_aspect:
  # 가로가 더 넓은 이미지 (예: 16:9 와이드 일러스트)
  w = W_BOX
  h = int(W_BOX / aspect)
  x = X_MIN
  y = Y_MIN + int((H_BOX - h) / 2)  # 상하 수직 중앙 정렬
else:
  # 세로가 더 길거나 정방형인 이미지 (예: 4:3, 1:1, 세로형 부품 사진)
  h = H_BOX
  w = int(H_BOX * aspect)
  y = Y_MIN
  x = X_MIN + int((W_BOX - w) / 2)  # 좌우 수평 중앙 정렬

# 4. Shape 9에 정확한 좌표와 크기 부여
shape9.left = x
shape9.top = y
shape9.width = w
shape9.height = h

# 5. 이미지 바로 아래에 캡션(Shape 10) 동적 배치
shape10.left = X_MIN
shape10.top = y + h + Inches(0.12)
shape10.width = W_BOX
shape10.height = Inches(0.35)
```

---

## 5. Markdown 항목과 슬라이드 슬롯 매핑 규칙

| Markdown 요소 | 대상 슬롯 (Shape ID) | 세부 배치 및 서식 기준 |
| :--- | :--- | :--- |
| **챕터 / 브레드크럼** | **Shape 2** (상단 섹션명) | `17pt` Bold 파란색 (`#0284C7`) |
| **슬라이드 번호** | **Shape 3** (우측상단 페이지) | `17pt` Bold 그레이 (`#64748B`), 우측 정렬 단독 배치 (`01 / 08`) |
| **# 또는 ## 제목** | **Shape 4** (메인 슬라이드 제목) | `28pt` Bold 다크 차콜 (`#0F172A`) |
| **### 또는 첫 줄 설명** | **Shape 8** (도입 설명) | `14.5pt` Regular 파란색 (`#0284C7`) |
| **![캡션](./img/xxx.jpg)**| **Shape 9** (왼쪽 주요 이미지) | 원본 비율 100% 보존, 최대 `5.40" × 4.50"` 내 자동 스케일링 |
| **대체 텍스트 `캡션`** | **Shape 10** (이미지 캡션) | 이미지 바로 밑 `0.12"` 아래, `14pt` 가운데 정렬 |
| **불릿 1 & 2 (핵심 2개)** | **Shape 11** (오른쪽 상단 본문) | 소제목 2개(`21pt` Bold) + 설명 2개(`18pt` Regular) |
| **불릿 3 (질문 또는 보충)**| **Shape 12** (오른쪽 하단 질문) | 소제목 1개(`19pt` Bold) + 설명 1개(`17.5pt` Regular), 아바타 좌측 배치 |
| **강사 아바타 사진** | **Shape 7** (우측 하단 사진) | 원형 투명 `hojin.png`, `X: 10.633"`, `Y: 5.150"`, `1.90" × 1.90"` (고정) |
| **> 구어체 강의 대본** | **slide.notes_slide** | **오디오 낭독/TTS용 순수 강의 설명문만 단독 수록** (메타 기호/라벨 일체 배제, 독립 `NotesSlidePart` 생성 필수) |

---

### 🎙️ 오디오 낭독용 슬라이드 노트(Notes) 표준 작성 원칙

1. **오디오 TTS/성우 녹음 전용**:
   - 슬라이드 노트의 텍스트는 추후 음성 합성(TTS) 또는 성우 오디오로 녹음되어 슬라이드에 동기화 삽입될 예정입니다.
2. **실제 강의 설명 내용만 삽입**:
   - 불필요한 마크다운 기호(`>`, `*`, `-`), 메타 라벨(`[대본]`, `노트:`, `해설:`, `슬라이드 N:` 등), 지시문(효과음, 안내 등)을 **일절 배제**합니다.
   - 처음부터 끝까지 청자에게 자연스럽게 말하듯이 읽어 내려가는 **100% 순수 구어체 강의 텍스트**로만 구성합니다.
3. **독립된 `NotesSlidePart` 생성 필수 (관계 공유 버그 방지)**:
   - python-pptx에서 템플릿 슬라이드를 복제할 때 `RT.NOTES_SLIDE` 관계를 그대로 복사하면, 모든 슬라이드가 동일한 `notesSlide.xml` 파트를 공유하게 됩니다.
   - 그 결과, 한 슬라이드의 노트를 변경하면 다른 모든 슬라이드의 노트까지 마지막 내용으로 덮어씌워지는 문제가 발생합니다.
   - 따라서 슬라이드를 복제할 때 `RT.NOTES_SLIDE`는 복제 대상에서 제외하고, 각 슬라이드마다 고유한 `NotesSlidePart`를 독립적으로 생성하여 연결해야 합니다.

---

## 6. 실행 가능한 전체 Python 변환 코드

```python
"""
generate_pptx.py

원본 PPTX의 '슬라이드 2'를 100% 디자인 템플릿으로 사용하여
Markdown 내용을 편집 가능한 PowerPoint로 완벽 변환하는 공식 자동화 스크립트.

주요 특징:
1. 슬라이드별 독립적인 NotesSlidePart 생성: 슬라이드 노트 공유 오류를 원천 차단하고
   TTS 오디오 낭독용 순수 강의 스크립트를 각 슬라이드 노트에 100% 독립 수록.
2. 이미지 원본 비율(Aspect Ratio) 100% 왜곡 없이 보존하며 대형 배치.
3. 오른쪽 상단 '강의 듣기' 버튼 및 오디오 객체 제거, 페이지 번호 단독 깔끔 배치.
4. 이미지 바로 아래에 캡션 동적 연동 배치.
"""

import os
import copy
from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.util import Inches
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.parts.slide import SlidePart, NotesSlidePart


def clone_slide_with_unique_notes(prs, src_slide, src_notes_part, notes_text):
    """
    슬라이드 XML과 독자적인 NotesSlidePart를 복제하여
    각 슬라이드가 완전히 독립된 순수 강의 대본(오디오 낭독용)을 갖도록 합니다.
    """
    slide_xml = copy.deepcopy(src_slide._element)
    new_partname = prs.part._next_slide_partname
    new_slide_part = SlidePart(new_partname, src_slide.part.content_type, prs.part.package, slide_xml)
    
    # 1. 슬라이드 관계 복제 (notesSlide 및 불필요한 미디어 관계는 제외)
    sorted_rIds = sorted(src_slide.part.rels.keys(), key=lambda x: int(x.replace("rId", "")))
    for rId in sorted_rIds:
        rel = src_slide.part.rels[rId]
        if rel.reltype == RT.NOTES_SLIDE or "media" in rel.reltype or "video" in rel.reltype:
            continue
        target = rel.target_ref if rel.is_external else rel.target_part
        new_slide_part.rels._add_relationship(rel.reltype, target, rel.is_external)
    
    rel_to_slide = prs.part.relate_to(new_slide_part, RT.SLIDE)
    prs.slides._sldIdLst.add_sldId(rel_to_slide)
    
    # 2. 각 슬라이드별 전용 NotesSlidePart 독립 생성
    notes_xml = copy.deepcopy(src_notes_part._element)
    for sp in notes_xml.xpath(".//p:sp"):
        ph = sp.xpath('.//p:ph[@type="body"]')
        if ph:
            txBody = sp.find("{http://schemas.openxmlformats.org/presentationml/2006/main}txBody")
            if txBody is not None:
                p = txBody.find("{http://schemas.openxmlformats.org/drawingml/2006/main}p")
                if p is not None:
                    for old_r in p.findall("{http://schemas.openxmlformats.org/drawingml/2006/main}r"):
                        p.remove(old_r)
                    r = etree.SubElement(p, "{http://schemas.openxmlformats.org/drawingml/2006/main}r")
                    t = etree.SubElement(r, "{http://schemas.openxmlformats.org/drawingml/2006/main}t")
                    t.text = notes_text
                    
    next_notes_partname = prs.part.package.next_partname("/ppt/notesSlides/notesSlide%d.xml")
    new_notes_part = NotesSlidePart(next_notes_partname, src_notes_part.content_type, prs.part.package, notes_xml)
    
    # NotesSlidePart 관계 연결 (notesMaster 및 슬라이드 파트)
    master_rel = [rel for rel in src_notes_part.rels.values() if "notesMaster" in rel.reltype][0]
    new_notes_part.rels._add_relationship(master_rel.reltype, master_rel.target_part, False)
    new_notes_part.rels._add_relationship(RT.SLIDE, new_slide_part, False)
    
    # 새 슬라이드에 전용 notesSlide 관계 연결
    new_slide_part.relate_to(new_notes_part, RT.NOTES_SLIDE)
    
    return prs.slides[-1]


def set_single_text(shape, text):
    """a:pPr 및 a:defRPr 서식을 100% 보존하면서 텍스트를 교체합니다."""
    txBody = shape.element.find("{http://schemas.openxmlformats.org/presentationml/2006/main}txBody")
    if txBody is None:
        return
    p = txBody.find("{http://schemas.openxmlformats.org/drawingml/2006/main}p")
    if p is None:
        return
    r_list = p.findall("{http://schemas.openxmlformats.org/drawingml/2006/main}r")
    if r_list:
        first_r = r_list[0]
        t = first_r.find("{http://schemas.openxmlformats.org/drawingml/2006/main}t")
        if t is None:
            t = etree.SubElement(first_r, "{http://schemas.openxmlformats.org/drawingml/2006/main}t")
        t.text = text
        for extra_r in r_list[1:]:
            p.remove(extra_r)
    else:
        r = etree.SubElement(p, "{http://schemas.openxmlformats.org/drawingml/2006/main}r")
        t = etree.SubElement(r, "{http://schemas.openxmlformats.org/drawingml/2006/main}t")
        t.text = text


def set_multi_paragraphs(shape, text_list):
    """문단별 a:pPr 서식을 유지하며 문단 목록 텍스트를 순서대로 매핑합니다."""
    txBody = shape.element.find("{http://schemas.openxmlformats.org/presentationml/2006/main}txBody")
    if txBody is None:
        return
    existing_ps = txBody.findall("{http://schemas.openxmlformats.org/drawingml/2006/main}p")
    if not existing_ps:
        return
    for idx, text in enumerate(text_list):
        if idx < len(existing_ps):
            p = existing_ps[idx]
        else:
            p = copy.deepcopy(existing_ps[-1])
            txBody.append(p)
        r_list = p.findall("{http://schemas.openxmlformats.org/drawingml/2006/main}r")
        if r_list:
            first_r = r_list[0]
            t = first_r.find("{http://schemas.openxmlformats.org/drawingml/2006/main}t")
            if t is None:
                t = etree.SubElement(first_r, "{http://schemas.openxmlformats.org/drawingml/2006/main}t")
            t.text = text
            for extra_r in r_list[1:]:
                p.remove(extra_r)
        else:
            r = etree.SubElement(p, "{http://schemas.openxmlformats.org/drawingml/2006/main}r")
            t = etree.SubElement(r, "{http://schemas.openxmlformats.org/drawingml/2006/main}t")
            t.text = text
    if len(text_list) < len(existing_ps):
        for extra_p in existing_ps[len(text_list):]:
            txBody.remove(extra_p)


def set_aspect_ratio_image(prs, slide, shape_img, shape_cap, img_path):
    """이미지 원본 종횡비를 100% 보존하여 대형 배치하고 캡션을 바로 밑에 배치합니다."""
    if not os.path.exists(img_path):
        return

    # 1. 새 이미지 파트 등록 및 blip 바인딩
    image_part = prs.part.package.get_or_add_image_part(img_path)
    new_rId = slide.part.relate_to(image_part, RT.IMAGE)
    blip = shape_img.element.xpath(".//a:blip")
    if blip:
        blip[0].set("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed", new_rId)

    # 2. 원본 이미지 크기 및 비율 추출
    with Image.open(img_path) as im:
        orig_w, orig_h = im.size
    aspect = orig_w / orig_h

    # 3. 허용 바운딩 박스 (가로 최대 5.40", 세로 최대 4.50")
    X_MIN = Inches(0.80)
    Y_MIN = Inches(2.05)
    W_BOX = Inches(5.40)
    H_BOX = Inches(4.50)
    box_aspect = W_BOX / H_BOX

    # 4. 무왜곡 크기 산출
    if aspect >= box_aspect:
        w = W_BOX
        h = int(W_BOX / aspect)
        x = X_MIN
        y = Y_MIN + int((H_BOX - h) / 2)
    else:
        h = H_BOX
        w = int(H_BOX * aspect)
        y = Y_MIN
        x = X_MIN + int((W_BOX - w) / 2)

    shape_img.left = x
    shape_img.top = y
    shape_img.width = w
    shape_img.height = h

    # 5. 캡션 동적 연동 (이미지 바로 밑 0.12인치 간격)
    if shape_cap:
        shape_cap.left = X_MIN
        shape_cap.top = y + h + Inches(0.12)
        shape_cap.width = W_BOX
        shape_cap.height = Inches(0.35)


def build_presentation(template_pptx, slides_data, avatar_path, output_pptx):
    prs = Presentation(template_pptx)
    src_slide = prs.slides[1]  # 원본 슬라이드 2
    src_notes_part = src_slide.part.part_related_by(RT.NOTES_SLIDE)

    total_pages = len(slides_data)

    for idx, s_data in enumerate(slides_data):
        notes_script = s_data.get("notes", "").strip()
        slide = clone_slide_with_unique_notes(prs, src_slide, src_notes_part, notes_script)
        page_str = f"{idx + 1:02d} / {total_pages:02d}"

        # 1. 불필요한 Shape 5 (강의 듣기) 및 Shape 13 (오디오 객체) 영구 제거
        for s in list(slide.shapes):
            if s.shape_id in [5, 13]:
                el = s._element
                el.getparent().remove(el)

        shapes_by_id = {s.shape_id: s for s in slide.shapes}

        # 2. 상단 섹션명 (Shape ID 2)
        if 2 in shapes_by_id and "section" in s_data:
            set_single_text(shapes_by_id[2], s_data["section"])

        # 3. 우측 상단 페이지 번호 (Shape ID 3: 단독 깔끔 배치)
        if 3 in shapes_by_id:
            s3 = shapes_by_id[3]
            s3.left = Inches(10.53)   # 슬라이드 우측 마진 12.53"에 정확히 맞춤
            s3.top = Inches(0.40)
            s3.width = Inches(2.00)
            s3.height = Inches(0.35)
            set_single_text(s3, page_str)

        # 4. 슬라이드 메인 제목 (Shape ID 4)
        if 4 in shapes_by_id and "title" in s_data:
            set_single_text(shapes_by_id[4], s_data["title"])

        # 5. 도입 설명문 (Shape ID 8)
        if 8 in shapes_by_id and "intro" in s_data:
            set_single_text(shapes_by_id[8], s_data["intro"])

        # 6. 왼쪽 주요 이미지 (Shape ID 9) & 캡션 (Shape ID 10) 비율 보존 대형 배치
        shape9 = shapes_by_id.get(9)
        shape10 = shapes_by_id.get(10)
        if shape9 and s_data.get("image"):
            set_aspect_ratio_image(prs, slide, shape9, shape10, s_data["image"])
        if shape10 and "caption" in s_data:
            set_single_text(shape10, s_data["caption"])

        # 7. 오른쪽 상단 본문 (Shape ID 11 - 소제목 2개, 설명 2개)
        if 11 in shapes_by_id and "body_bullets" in s_data:
            set_multi_paragraphs(shapes_by_id[11], s_data["body_bullets"])

        # 8. 오른쪽 하단 질문 (Shape ID 12 - 소제목 1개, 설명 1개)
        if 12 in shapes_by_id and "question_bullets" in s_data:
            set_multi_paragraphs(shapes_by_id[12], s_data["question_bullets"])

        # 9. 인물 사진 (Shape ID 7)
        if 7 in shapes_by_id and os.path.exists(avatar_path):
            image_part = prs.part.package.get_or_add_image_part(avatar_path)
            new_rId = slide.part.relate_to(image_part, RT.IMAGE)
            blip = shapes_by_id[7].element.xpath(".//a:blip")
            if blip:
                blip[0].set("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed", new_rId)

    # 템플릿의 기존 원본 슬라이드들을 안전하게 제거하여 결과물 정돈
    sldIdLst = prs.slides._sldIdLst
    original_sldIds = list(sldIdLst)[:-total_pages]
    for sldId in original_sldIds:
        rId = sldId.rId
        sldIdLst.remove(sldId)
        prs.part.drop_rel(rId)

    prs.save(output_pptx)
    print(f"[성공] 총 {total_pages}장의 슬라이드가 생성되었습니다: {output_pptx}")
```

---

## 7. 품질 검증 체크리스트 (QA Checklist)

- [ ] **강의 듣기 버튼 제거 확인**: 우측 상단에 파란색 버튼(`Shape 5`)과 오디오 아이콘(`Shape 13`)이 완전히 삭제되었는가?
- [ ] **페이지 번호 단독 정렬 확인**: `Shape 3`이 `X: 10.53" ~ 12.53"` 범위에서 우측 정렬되어 깔끔하게 표시되는가?
- [ ] **이미지 비율 왜곡 0% 확인**: `Shape 9`의 `width / height`가 원본 이미지의 `orig_w / orig_h`와 0.001 오차 이내로 정확히 일치하는가?
- [ ] **이미지 크기 극대화 확인**: 가로 `5.40인치` 또는 세로 `4.50인치`의 최대 영역을 활용하여 큼직하게 렌더링되었는가?
- [ ] **캡션 위치 자동 연동 확인**: 캡션 박스(`Shape 10`)가 이미지 바로 아래 `0.12인치` 간격으로 알맞게 배치되었는가?
- [ ] **강사 아바타 보존 확인**: `Shape 7`이 `X: 10.633"`, `Y: 5.150"`의 정확한 위치에 원형 투명 배경으로 유지되었는가?
- [ ] **슬라이드 노트 오디오 낭독용 스크립트 수록 확인**: 
  - 각 슬라이드의 발표자 노트에 **실제 강의 설명 구어체 대본만** 단독으로 수록되었는가?
  - 불필요한 마크다운 기호(`>`, `*`), 메타 라벨(`[대본]`, `노트:` 등), 지시문이 완전히 제거되었는가?
  - 모든 슬라이드가 서로 다른 독립된 `notesSlide`를 가지며, 한 슬라이드의 노트가 다른 슬라이드를 덮어쓰지 않는가?
- [ ] **PPT 파일명 표준 준수 확인**: `slides.pptx`가 아닌 해당 강의 폴더명/강의명과 동일한 `{강의명}.pptx`(예: `000_강의소개_아두이노모험의시작.pptx`)로 생성되었는가?

