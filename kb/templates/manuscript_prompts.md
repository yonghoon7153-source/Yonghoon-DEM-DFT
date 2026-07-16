# Manuscript 프롬프트 템플릿 모음 (강준희 슬라이드 워크플로의 Claude Code 이식판, 2026-07-16)

Claude Code에서 그대로 붙여 쓰는 템플릿. `{}` 부분만 채운다.
원칙(슬라이드 6): **figure 단위로 요청**이 최선 — 전체 한 방 요청은 세부 수정이 괴로워진다.
순서: ① Abstract + figure set + figure별 rough 설명 → rough draft ② figure별 세부 요청 ③ 문장 단위 다듬기.

---

## 1. Results & Discussion 초안 (Wiley 스타일; 프로젝트 지침급 상용문)

```
I would like you to draft a high-quality Results and Discussion section for my manuscript
by referring to the reference manuscripts in {litdb/papers/ 또는 첨부 경로}. Adopt their
style of scientific storytelling — how figures are introduced, how individual panels are
discussed, and how observations are connected to mechanistic interpretations — without
copying their formatting.

Materials I provide:
- The manuscript abstract.
- The complete figure set with per-panel descriptions ({경로}).
- Registered data: db/properties/{관련 json/csv 목록}.

Write ~{2500} words of publication-ready academic English. Rules:
- Every single figure panel must be explicitly discussed; no panel skipped.
- Smooth transitions between figures — one coherent narrative, not per-figure blurbs.
- Interpret significance rather than describing data; connect electrochemical results with
  structural/mechanistic analyses wherever possible.
- Reference figures as "Figure 2a,b", "Figure 3c–f".
- Use ONLY numbers from the registered db files above — never invent or import literature
  values without citing them as literature.
```

## 2. Figure 단위 세부 요청 (슬라이드 6 형식)

```
Figure {N}에 해당하는 Results and Discussion 파트를 작성해줘.
Figure {N}a : {이 패널이 보여주는 것, 실험/계산 조건, 대표 수치}
Figure {N}b : {...}
...
강조할 메시지: {이 figure가 논문에서 하는 주장 한 줄}
참고: {관련 db 파일 / litdb digest 경로}. 값은 반드시 그 파일에서 가져와.
```

## 3. 학술 문장 5가지 재번역 (슬라이드 7)

```
아래 문장을 학술 논문(Wiley 계열)에 적합한 서로 다른 5가지 영어 문장으로 다시 써줘.
뉘앙스 차이(단정↔신중, 능동↔수동, 결과강조↔방법강조)를 한 줄씩 설명 붙여줘.
문장: "{...}"
```

## 4. Reference list 생성 (슬라이드 8 — 링크 금지, 로컬 PDF 기준)

```
{폴더}에 있는 PDF들(및 litdb/papers/ digest 메타데이터)로 reference list를 만들어줘.
포맷은 아래 예시 3개와 완전히 동일하게 (bold/italic/약어/DOI 표기까지):
[1] {예시 1}
[2] {예시 2}
[3] {예시 3}
출력: 번호 순서대로 word에 붙일 수 있는 텍스트. 각 항목 옆에 (근거 PDF 파일명) 주석.
확인 안 되는 서지 항목은 추측하지 말고 [CHECK]로 표시해.
```

## 5. Raw data → 고정 포맷 그림 (슬라이드 2의 우리 버전)

```
{raw 파일}를 읽어서 {기존 그림 파일/family 이름}과 동일한 포맷으로 그려줘
(tools/figures/house_style.py 스타일: 축·폰트·범례·크기 통일).
png(300 dpi) + svg + Origin-ready csv(db/properties/{이름}_origin.csv) 각 1개씩.
csv 열 이름은 명시적으로 ({예: cycle, areal_capacity_mAh_cm2, CE_pct}).
```

## 6. 이미지 정량화 (슬라이드 10의 void ratio류)

```
{SEM 이미지}를 threshold + morphology로 binary map 변환해서 {void ratio 등}을 정량해줘.
전처리(스케일바 제거/크롭), threshold 방법(Otsu 등), 면적비 계산 과정을 그림으로 보여주고
경계 케이스(threshold ±10%)의 민감도도 같이 보고해.
```

## 주의 (슬라이드 10 + 우리 교훈)
- 기호/첨자/그리스 문자는 자주 깨진다 → 최종본은 텍스트로 뽑아 검수.
- 결과물의 methodology·코드는 반드시 읽어본다 (특히 fitting 창, 단위).
- 인용 문헌은 역할까지 확인 후 삽입 (Kim/Cui 사례: 내부 별칭 ≠ 실제 방법).
- 웹 검색으로 최신 문헌 반영 요청 시 "참고한 문헌 list-up"을 함께 요구.
