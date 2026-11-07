"""generate_pptx.py

원본 PPTX의 '슬라이드 2'를 100% 디자인 템플릿으로 사용하여
000. 강의소개 마크다운 내용을 파워포인트로 완벽 변환하는 공식 스크립트.

주요 특징:
1. 슬라이드별 독립적인 NotesSlidePart 생성: 슬라이드 노트 공유 오류를 원천 차단하고
   TTS 오디오 낭독용 순수 강의 스크립트를 각 슬라이드 노트에 100% 독립 수록.
2. 이미지 원본 비율(Aspect Ratio) 100% 왜곡 없이 보존하며 대형 배치.
3. 오른쪽 상단 '강의 듣기' 버튼 및 오디오 객체 제거, 페이지 번호 단독 깔끔 배치.
4. 이미지 바로 아래에 캡션 동적 연동 배치.
"""

import copy
import os
import sys
from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.parts.slide import NotesSlidePart, SlidePart
from pptx.util import Inches

CH_DIR = "/Users/hojin9/Library/CloudStorage/OneDrive-개인/070.강의/아두이노2_ppt_ai/Part01_아두이노_우노와_기초/000_강의소개_아두이노모험의시작"
TEMPLATE_PPTX = "/Users/hojin9/Library/CloudStorage/OneDrive-개인/070.강의/인공지능4_강화학습/07_동적프로그래밍/07_1_동적_프로그래밍의_유래_output/07_1_동적_프로그래밍의_유래_with_audio.pptx"
AVATAR_PATH = (
    "/Users/hojin9/Library/CloudStorage/OneDrive-개인/070.강의/아두이노2_ppt_ai/img/hojin.png"
)
LECTURE_NAME = os.path.basename(CH_DIR)
OUTPUT_PPTX = os.path.join(CH_DIR, f"{LECTURE_NAME}.pptx")

slides_data = [
    {
        "section": "Part 01. 아두이노 우노와 기초  |  000. 강의소개",
        "title": "000. 강의소개: 아두이노 모험의 시작 🧭",
        "intro": (
            "이호진 교수님의 친절한 설명과 함께하는 도로시와 토토의 신기한 전자"
            " 세상 대모험에 오신 것을 환영합니다!"
        ),
        "image": os.path.join(CH_DIR, "img/dorothy_jiny_arduino_intro.jpg"),
        "caption": "이호진 교수님의 아두이노 첫 강의와 도로시·지니·토토",
        "body_bullets": [
            "• 🎯 강좌 대상",
            "초등학생부터 코딩과 피지컬 컴퓨팅을 처음 접하는 모든 어른이",
            "• 🎒 준비물",
            "호기심 가득한 눈망울 + 재미있게 따라 해볼 열린 마음가짐!",
        ],
        "question_bullets": [
            "• 📖 공식 연계 교재",
            (
                "아두이노 & IoT 피지컬 컴퓨팅 완전 정복 193개 강좌 마스터"
                " 코스 (index.md)"
            ),
        ],
        "notes": (
            "여러분, 안녕하세요! 오늘부터 친절한 이호진 교수님의 설명과 함께"
            " 똑똑한 조수 고양이 지니, 수업을 듣는 호기심 많은 학생 도로시,"
            " 그리고 도로시를 돕는 친구 강아지 토토와 함께 신기하고 재미있는"
            " 아두이노 전자 세상 탐험을 시작합니다. 코딩이나 전자를 한 번도"
            " 배워본 적 없어도 괜찮습니다. 초등학생부터 코딩을 처음 시작하는"
            " 어른들까지, 누구나 쉽고 재미있게 나만의 스마트 기기와 로봇을"
            " 만들 수 있도록 알기 쉽게 안내해 드리겠습니다. 준비되셨나요? 출발해"
            " 봅시다!"
        ),
    },
    {
        "section": "Part 01. 아두이노 우노와 기초  |  주인공 소개",
        "title": "000.1 우리 모험을 함께할 주인공들을 소개합니다! 👥",
        "intro": "이호진 교수님, 조수 고양이 지니, 학생 도로시, 친구 강아지 토토",
        "image": os.path.join(CH_DIR, "img/dorothy_jiny_character_intro.jpg"),
        "caption": "아두이노 모험의 주인공 4총사",
        "body_bullets": [
            "• 👨‍🏫 이호진 교수님 (공학 & 메이커 멘토)",
            "어려운 전자 회로와 프로그래밍을 알기 쉽게 설명해 주시는 교수님!",
            "• 🐱 지니 (교수님의 조수 고양이)",
            (
                "둥근 안경을 쓴 똑똑한 턱시도 고양이! 교수님 곁에서 회로와 코드를"
                " 꼼꼼히 점검해 주는 든든한 조수"
            ),
        ],
        "question_bullets": [
            "• 👧 도로시 (수업을 듣는 9세 학생 메이커)",
            (
                "교수님 설명을 반짝이는 눈으로 듣고 직접 만들어보는"
                " 열정 학생!"
            ),
            "• 🐶 토토 (도로시의 단짝 친구 강아지)",
            (
                "도로시 곁에서 항상 함께 수업을 듣고, 부품을 챙겨주며 활기차게"
                " 응원하는 귀염둥이 친구!"
            ),
        ],
        "notes": (
            "이번 여정을 함께할 주인공들을 소개합니다. 먼저 어려운 전자 회로와"
            " 컴퓨터 코딩을 쉽고 친절하게 가르쳐 주시는 이호진 교수님과 교수님의"
            " 곁을 든든하게 지키는 조수 고양이 지니, 그리고 반짝이는 눈으로"
            " 수업을 들으며 무엇이든 직접 만들어보는 열혈 학생 도로시, 마지막으로"
            " 도로시 곁에서 함께 수업을 듣고 부품을 챙겨주며 응원하는 토토입니다."
            " 앞으로 강의를 듣는 동안 여러분도 도로시가 되어 하나씩 멋진 발명품을"
            " 완성해 나가게 될 것입니다."
        ),
    },
    {
        "section": "Part 01. 아두이노 우노와 기초  |  첫 연결 실습",
        "title": "000.2 1단계: 컴퓨터에 USB 선을 꽂아보자! 💡",
        "intro": (
            "파란색 USB 케이블 연결과 보드 속 내장 깜빡이 프로그램의 첫 시동"
        ),
        "image": (
            "/Users/hojin9/Library/CloudStorage/OneDrive-개인/070.강의/아두이노2_ppt_ai/img/arduino_logo.png"
        ),
        "caption": "아두이노 공식 오픈소스 하드웨어 로고",
        "body_bullets": [
            "• 🔌 첫 만남의 설렘",
            "파란색 USB 케이블로 아두이노 보드와 컴퓨터를 꽂아 연결합니다.",
            "• 💡 도로시의 놀라운 발견",
            '"노트북에 선을 꽂자마자 작은 불빛이 깜빡깜빡 춤을 춰요!"',
        ],
        "question_bullets": [
            "• ⚙️ 지니의 친절한 설명",
            (
                "공장에서 미리 넣어둔 '깜빡이(Blink)' 프로그램이 전기를"
                " 받자마자 스스로 깨어나 작동한 것입니다!"
            ),
        ],
        "notes": (
            "자, 첫 번째 실습 단계입니다. 컴퓨터에 파란색 USB 케이블을 꽂고"
            " 아두이노 보드에 연결해 보세요. 놀랍게도 연결하자마자 보드 위에"
            " 작은 LED 불빛이 1초 간격으로 깜빡깜빡 춤을 추기 시작합니다. 아무런"
            " 명령도 주지 않았는데 왜 불이 켜질까요? 바로 아두이노를 만든 공장에서"
            " 미리 테스트용으로 '깜빡이' 프로그램을 칩 속에 넣어두었기 때문입니다."
            " 전기가 공급되는 순간, 아두이노는 잠에서 깨어나 이 프로그램을 스스로"
            " 실행합니다."
        ),
    },
    {
        "section": "Part 01. 아두이노 우노와 기초  |  전원 및 보드 상태",
        "title": "000.3 2단계: 전기가 흐르면 스스로 생각해요! ⚡",
        "intro": (
            "보드 상태 표시등(ON 램프, L 램프)의 의미와 독립적 실행 원리"
        ),
        "image": os.path.join(CH_DIR, "img/image_2_3.jpg"),
        "caption": "USB 전원 공급 및 13번 온보드 LED 점등 상태",
        "body_bullets": [
            "• ⚡ 1. 전원 공급 (5V USB Power)",
            (
                "컴퓨터의 5V 전기가 USB 선을 타고 아두이노 내부로 안정적으로"
                " 유입됩니다."
            ),
            "• 🟢 2. 초록색 ON 램프 & 주황색 L 램프",
            (
                "전원 정상 공급 알림등과 13번 핀에 연결된 내장 테스트 LED 점멸"
                " 증명"
            ),
        ],
        "question_bullets": [
            "• 📌 핵심 요약",
            (
                "아두이노는 전원만 연결되면 칩에 저장된 프로그램을 쉬지 않고"
                " 24시간 실행합니다!"
            ),
        ],
        "notes": (
            "슬라이드 사진을 보며 보드 위의 램프들을 확인해 볼까요? USB 케이블을"
            " 꽂으면 먼저 초록색으로 'ON'이라고 적힌 불이 켜집니다. 이건 '전기가"
            " 정상적으로 들어왔다'는 신호입니다. 그리고 그 옆에 주황색으로 'L'이라고"
            " 적힌 작은 램프가 보이시죠? 이 램프는 13번 핀에 연결된 테스트 전등으로,"
            " 아두이노가 지금 살아서 명령을 수행하고 있다는 확실한 증거입니다."
            " 아두이노는 전원만 들어가면 24시간 쉬지 않고 스스로 생각하며 일하는"
            " 기계입니다."
        ),
    },
    {
        "section": "Part 01. 아두이노 우노와 기초  |  하드웨어 구조",
        "title": "000.4 3단계: 아두이노는 '작은 손바닥 컴퓨터'예요! 🧠",
        "intro": (
            "두뇌(MCU), 감각기관(입력 핀), 손발(출력 핀)로 구성된 피지컬"
            " 컴퓨팅 구조"
        ),
        "image": os.path.join(CH_DIR, "img/image_3_4.png"),
        "caption": "아두이노 우노의 두뇌(MCU)와 입출력 핀 구조",
        "body_bullets": [
            "• 🧠 마이크로컨트롤러 (MCU - 중앙 두뇌)",
            (
                "보드 한가운데 자리 잡은 까만 칩(ATmega328P)으로 생각하고"
                " 기억하는 제어 센터"
            ),
            "• 👁️ 입력 핀 (Input - 눈과 귀)",
            (
                "스위치 버튼, 빛 센서, 온도 센서로 바깥세상의 물리적 물리량을"
                " 전기 신호로 감지"
            ),
        ],
        "question_bullets": [
            "• 🦾 출력 핀 (Output - 손과 발)",
            (
                "LED 램프, 모터 바퀴, 부저 스피커 등으로 현실 세계에 직접"
                " 물리적 동작을 수행"
            ),
        ],
        "notes": (
            "그렇다면 이 작은 보드가 어떻게 전등을 켜고 모터를 움직일까요?"
            " 아두이노는 손바닥 위에 올라가는 작은 컴퓨터이기 때문입니다. 사람의"
            " 몸과 비교해 보면 아주 쉽게 이해할 수 있습니다. 보드 한가운데의"
            " 네모난 까만 칩은 생각하고 기억하는 '두뇌(MCU)'입니다. 그리고 양옆에"
            " 뚫려 있는 구멍들 중 '입력 핀'은 눈과 귀처럼 외부의 빛이나 소리를"
            " 감지하고, '출력 핀'은 손과 발처럼 LED를 켜거나 모터를 돌려 실제로"
            " 행동합니다."
        ),
    },
    {
        "section": "Part 01. 아두이노 우노와 기초  |  개발 파이프라인",
        "title": "000.5 4단계: 컴퓨터로 주문(코드)을 써서 보내요! 💻",
        "intro": (
            "Arduino IDE 스케치 작성, USB 업로드, 배터리 독립 구동의 전체 흐름"
        ),
        "image": os.path.join(CH_DIR, "img/image_4_5.jpg"),
        "caption": (
            "PC 개발환경과 아두이노 간의 코드 업로드 및 독립 실행 파이프라인"
        ),
        "body_bullets": [
            "• 💻 1. 마법 스케치북 (Arduino IDE)",
            (
                "컴퓨터 키보드로 아두이노에게 시킬 일을 편지(C++ 코드)로 작성"
                " (예: digitalWrite)"
            ),
            "• 🚀 2. 업로드 (코드 전송)",
            (
                "화살표 버튼(➔)을 누르면 USB 케이블을 타고 칩 내부 메모리에"
                " 영구 저장"
            ),
        ],
        "question_bullets": [
            "• 🔋 3. 독립 실행 (Standalone)",
            (
                "코드가 한번 저장되면 PC를 분리하고 배터리만 연결해도 혼자서"
                " 완벽하게 동작!"
            ),
        ],
        "notes": (
            "이제 우리가 아두이노에게 일을 시키는 과정을 살펴보겠습니다. 우리는"
            " 컴퓨터에서 'Arduino IDE'라는 마법의 프로그램을 열고, 아두이노에게"
            " 시킬 일을 코드로 작성합니다. 예를 들어 \"13번 불을 켜라!\"라고 쓰는"
            " 거죠. 그런 다음 업로드 버튼을 콕 누르면, USB 케이블을 타고 명령어가"
            " 아두이노의 까만 칩 속으로 쏙 들어갑니다. 이렇게 코드가 한 번 저장되면"
            " 컴퓨터를 뽑아버리고 건전지만 연결해도 아두이노 혼자서 언제 어디서든"
            " 그 일을 해냅니다."
        ),
    },
    {
        "section": "Part 01. 아두이노 우노와 기초  |  커리큘럼 로드맵",
        "title": "000.6 5단계: 이호진 교수님과 함께하는 아두이노 모험 로드맵! 🗺️",
        "intro": (
            "기초 실습부터 센서, 디스플레이, 무선 RC카 로봇까지 이어지는 5대"
            " 관문"
        ),
        "image": os.path.join(CH_DIR, "img/dorothy_jiny_arduino_roadmap.jpg"),
        "caption": "이호진 교수님의 5단계 아두이노 탐험 로드맵 강의",
        "body_bullets": [
            "• 🔴 1장 기본 & 🟡 2장 출력 실습",
            (
                "전기의 흐름과 IDE 설치, 알록달록 무지개 RGB LED와 멜로디"
                " 피아노 연주"
            ),
            "• 🟢 3장 디스플레이 & 🔵 4장 센서 탐험",
            "글자가 흐르는 LCD/OLED 화면, 스마트 가로등과 초음파 거리 측정기",
        ],
        "question_bullets": [
            "• 🟣 5장 모터 & 로봇 완성",
            (
                "빙글빙글 회전 모터와 스마트폰으로 원격 조종하는 나만의 무선"
                " RC카!"
            ),
        ],
        "notes": (
            "앞으로 우리가 함께 떠날 신나는 아두이노 모험 로드맵을 한눈에"
            " 보여드립니다. 1장에서는 기초 전기와 코딩 도구를 준비하고, 2장에서는"
            " 빛과 소리를 만드는 출력 장치를 다룹니다. 3장에서는 글자를 띄우는"
            " 디스플레이를 배우고, 4장에서는 세상의 정보를 읽는 온갖 센서를"
            " 탐험합니다. 그리고 마지막 5장에서는 모터를 달아 스마트폰으로 직접"
            " 조종하는 자율주행 로봇 자동차까지 완성하게 됩니다."
        ),
    },
    {
        "section": "Part 01. 아두이노 우노와 기초  |  출발 준비 완료",
        "title": '000.7 출발 준비 완료! "다음 모험으로 떠나요!" 🚀',
        "intro": "설레는 메이커 탐험의 시작과 001강 에너지 탐구 예고",
        "image": os.path.join(CH_DIR, "img/dorothy_jiny_celebrate.jpg"),
        "caption": "성공적인 첫 만남과 다음 강의로의 힘찬 출발",
        "body_bullets": [
            "• 👧 도로시의 당찬 다짐",
            (
                '"교수님, 저도 얼른 멋진 로봇이랑 반짝이는 무지개 램프를'
                ' 만들어보고 싶어요!"'
            ),
            "• 👨‍🏫 교수님의 따뜻한 응원",
            (
                '"좋아 도로시! 그럼 가장 먼저 컴퓨터에 아두이노와 대화할 마법'
                ' 스케치북을 설치해보자!"'
            ),
        ],
        "question_bullets": [
            "• 👉 다음 탐험 (001강 예고)",
            (
                '"001. 에너지란? 세상을 움직이는 힘 ⚡" 전기 에너지의 비밀을'
                " 파헤칩니다!"
            ),
        ],
        "notes": (
            "이제 아두이노 모험을 떠날 모든 준비가 끝났습니다! 도로시와 토토의"
            " 눈빛이 반짝이는 것 보이시나요? 여러분도 나만의 발명품을 만들 수"
            " 있다는 설레는 마음만 챙겨오시면 됩니다. 다음 001강에서는 전자 기기를"
            " 움직이는 근본적인 힘, '에너지'의 비밀을 파헤치러 떠나보겠습니다."
            " 다음 시간에 만나요!"
        ),
    },
]


def clone_slide_with_unique_notes(prs, src_slide, src_notes_part, notes_text):
  """슬라이드 XML과 독자적인 NotesSlidePart를 복제하여 각 슬라이드가 고유한 강의 대본을 갖도록 합니다."""
  slide_xml = copy.deepcopy(src_slide._element)
  new_partname = prs.part._next_slide_partname
  new_slide_part = SlidePart(
      new_partname, src_slide.part.content_type, prs.part.package, slide_xml
  )

  # 슬라이드 관계 복제 (notesSlide 및 불필요한 미디어 제외)
  sorted_rIds = sorted(
      src_slide.part.rels.keys(), key=lambda x: int(x.replace("rId", ""))
  )
  for rId in sorted_rIds:
    rel = src_slide.part.rels[rId]
    if (
        rel.reltype == RT.NOTES_SLIDE
        or "media" in rel.reltype
        or "video" in rel.reltype
    ):
      continue
    target = rel.target_ref if rel.is_external else rel.target_part
    new_slide_part.rels._add_relationship(rel.reltype, target, rel.is_external)

  rel_to_slide = prs.part.relate_to(new_slide_part, RT.SLIDE)
  prs.slides._sldIdLst.add_sldId(rel_to_slide)

  # 각 슬라이드별 전용 NotesSlidePart 독립 생성
  notes_xml = copy.deepcopy(src_notes_part._element)
  for sp in notes_xml.xpath(".//p:sp"):
    ph = sp.xpath('.//p:ph[@type="body"]')
    if ph:
      txBody = sp.find(
          "{http://schemas.openxmlformats.org/presentationml/2006/main}txBody"
      )
      if txBody is not None:
        p = txBody.find(
            "{http://schemas.openxmlformats.org/drawingml/2006/main}p"
        )
        if p is not None:
          for old_r in p.findall(
              "{http://schemas.openxmlformats.org/drawingml/2006/main}r"
          ):
            p.remove(old_r)
          r = etree.SubElement(
              p, "{http://schemas.openxmlformats.org/drawingml/2006/main}r"
          )
          t = etree.SubElement(
              r, "{http://schemas.openxmlformats.org/drawingml/2006/main}t"
          )
          t.text = notes_text

  next_notes_partname = prs.part.package.next_partname(
      "/ppt/notesSlides/notesSlide%d.xml"
  )
  new_notes_part = NotesSlidePart(
      next_notes_partname, src_notes_part.content_type, prs.part.package, notes_xml
  )

  # NotesSlidePart 관계 연결
  master_rel = [
      rel
      for rel in src_notes_part.rels.values()
      if "notesMaster" in rel.reltype
  ][0]
  new_notes_part.rels._add_relationship(
      master_rel.reltype, master_rel.target_part, False
  )
  new_notes_part.rels._add_relationship(RT.SLIDE, new_slide_part, False)

  # 새 슬라이드에 전용 notesSlide 관계 연결
  new_slide_part.relate_to(new_notes_part, RT.NOTES_SLIDE)

  return prs.slides[-1]


def set_single_text(shape, text):
  """a:pPr 및 a:defRPr 서식을 100% 보존하면서 텍스트를 교체합니다."""
  txBody = shape.element.find(
      "{http://schemas.openxmlformats.org/presentationml/2006/main}txBody"
  )
  if txBody is None:
    return
  p = txBody.find("{http://schemas.openxmlformats.org/drawingml/2006/main}p")
  if p is None:
    return
  r_list = p.findall("{http://schemas.openxmlformats.org/drawingml/2006/main}r")
  if r_list:
    first_r = r_list[0]
    t = first_r.find(
        "{http://schemas.openxmlformats.org/drawingml/2006/main}t"
    )
    if t is None:
      t = etree.SubElement(
          first_r, "{http://schemas.openxmlformats.org/drawingml/2006/main}t"
      )
    t.text = text
    for extra_r in r_list[1:]:
      p.remove(extra_r)
  else:
    r = etree.SubElement(
        p, "{http://schemas.openxmlformats.org/drawingml/2006/main}r"
    )
    t = etree.SubElement(
        r, "{http://schemas.openxmlformats.org/drawingml/2006/main}t"
    )
    t.text = text


def set_multi_paragraphs(shape, text_list):
  """문단별 a:pPr 서식을 유지하며 문단 목록 텍스트를 순서대로 매핑합니다."""
  txBody = shape.element.find(
      "{http://schemas.openxmlformats.org/presentationml/2006/main}txBody"
  )
  if txBody is None:
    return
  existing_ps = txBody.findall(
      "{http://schemas.openxmlformats.org/drawingml/2006/main}p"
  )
  if not existing_ps:
    return
  for idx, text in enumerate(text_list):
    if idx < len(existing_ps):
      p = existing_ps[idx]
    else:
      p = copy.deepcopy(existing_ps[-1])
      txBody.append(p)
    r_list = p.findall(
        "{http://schemas.openxmlformats.org/drawingml/2006/main}r"
    )
    if r_list:
      first_r = r_list[0]
      t = first_r.find(
          "{http://schemas.openxmlformats.org/drawingml/2006/main}t"
      )
      if t is None:
        t = etree.SubElement(
            first_r, "{http://schemas.openxmlformats.org/drawingml/2006/main}t"
        )
      t.text = text
      for extra_r in r_list[1:]:
        p.remove(extra_r)
    else:
      r = etree.SubElement(
          p, "{http://schemas.openxmlformats.org/drawingml/2006/main}r"
      )
      t = etree.SubElement(
          r, "{http://schemas.openxmlformats.org/drawingml/2006/main}t"
      )
      t.text = text
  if len(text_list) < len(existing_ps):
    for extra_p in existing_ps[len(text_list) :]:
      txBody.remove(extra_p)


def set_aspect_ratio_image(prs, slide, shape_img, shape_cap, img_path):
  """이미지 원본 종횡비(Aspect Ratio)를 100% 보존하여 대형 배치하고 캡션을 바로 밑에 자동 배치합니다."""
  if not os.path.exists(img_path):
    return

  # 1. 새 이미지 파트 등록 및 blip 연결
  image_part = prs.part.package.get_or_add_image_part(img_path)
  new_rId = slide.part.relate_to(image_part, RT.IMAGE)
  blip = shape_img.element.xpath(".//a:blip")
  if blip:
    blip[0].set(
        "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed",
        new_rId,
    )

  # 2. 원본 이미지 크기 및 비율 계산
  with Image.open(img_path) as im:
    orig_w, orig_h = im.size
  aspect = orig_w / orig_h

  # 3. 왼쪽 대형 바운딩 박스 (가로 최대 5.40인치, 세로 최대 4.50인치)
  X_MIN = Inches(0.80)
  Y_MIN = Inches(2.05)
  W_BOX = Inches(5.40)
  H_BOX = Inches(4.50)
  box_aspect = W_BOX / H_BOX

  # 4. 무왜곡 비율 맞춤 (Fit without distortion)
  if aspect >= box_aspect:
    w = W_BOX
    h = int(W_BOX / aspect)
    x = X_MIN
    y = Y_MIN + int((H_BOX - h) / 2)  # 상하 중앙 정렬
  else:
    h = H_BOX
    w = int(H_BOX * aspect)
    y = Y_MIN
    x = X_MIN + int((W_BOX - w) / 2)  # 좌우 중앙 정렬

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


def build_presentation():
  prs = Presentation(TEMPLATE_PPTX)
  src_slide = prs.slides[1]  # 원본 슬라이드 2
  src_notes_part = src_slide.part.part_related_by(RT.NOTES_SLIDE)

  total_pages = len(slides_data)

  for idx, s_data in enumerate(slides_data):
    notes_script = s_data.get("notes", "").strip()
    slide = clone_slide_with_unique_notes(
        prs, src_slide, src_notes_part, notes_script
    )
    page_str = f"{idx + 1:02d} / {total_pages:02d}"

    # 1. 불필요한 Shape 5 (강의 듣기 버튼) 및 Shape 13 (오디오 객체) 영구 제거
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
      s3.left = Inches(10.53)  # 슬라이드 우측 마진 12.53"에 맞춤
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
      set_aspect_ratio_image(
          prs, slide, shape9, shape10, s_data["image"]
      )
    if shape10 and "caption" in s_data:
      set_single_text(shape10, s_data["caption"])

    # 7. 오른쪽 상단 본문 (Shape ID 11 - 소제목 2개, 설명 2개)
    if 11 in shapes_by_id and "body_bullets" in s_data:
      set_multi_paragraphs(shapes_by_id[11], s_data["body_bullets"])

    # 8. 오른쪽 하단 질문 (Shape ID 12 - 소제목 1개, 설명 1개)
    if 12 in shapes_by_id and "question_bullets" in s_data:
      set_multi_paragraphs(shapes_by_id[12], s_data["question_bullets"])

    # 9. 인물 사진 (Shape ID 7)
    if 7 in shapes_by_id and os.path.exists(AVATAR_PATH):
      image_part = prs.part.package.get_or_add_image_part(AVATAR_PATH)
      new_rId = slide.part.relate_to(image_part, RT.IMAGE)
      blip = shapes_by_id[7].element.xpath(".//a:blip")
      if blip:
        blip[0].set(
            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed",
            new_rId,
        )

  # 템플릿의 기존 원본 슬라이드들을 안전하게 제거하여 결과물 정돈
  sldIdLst = prs.slides._sldIdLst
  original_sldIds = list(sldIdLst)[:-total_pages]
  for sldId in original_sldIds:
    rId = sldId.rId
    sldIdLst.remove(sldId)
    prs.part.drop_rel(rId)

  prs.save(OUTPUT_PPTX)
  print(f"[성공] 총 {total_pages}장의 슬라이드가 생성되었습니다: {OUTPUT_PPTX}")


if __name__ == "__main__":
  build_presentation()
