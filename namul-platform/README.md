# 나물로 (Namullo) — 창업 아이템 발표 세트

> 수업 과제(Problem–Solution–Business–Vision, 8–10분 PPT 발표 + mp4)용 산출물.
> 중심 문장: **레시피로 고른 나물을 전통시장에서 쉽게 사고, 그 장보기가 지역 상권을 돕는 서비스** (나물 접근성 · 지역 상권 상생 · AI 기반 · 레시피 연계).
> **이 폴더는 연구 프로젝트(`degradation-degeneracy/`, `bms-balancing/` 등)와 무관하며, `claude/namul-platform` 브랜치는 `namul-platform/` 경로만 다룬다.**

## 제출용 (v4.5)

| 파일 | 내용 |
|---|---|
| `02_발표자료_나물로.pptx` | 본문 12장 + 부록 2장 (Problem 2 · Solution 3 · Business 3 · Vision 2 + 표지·마무리). 슬라이드 노트에 대본, 6번 장표에 시연 영상 내장 |
| `02_발표자료_나물로_미리보기.pdf` | LibreOffice 렌더 미리보기 (글꼴 대체로 줄바꿈이 PowerPoint와 조금 다를 수 있음) |
| `03_발표대본_나물로.md` | 장표별 대본, 시간표(사람 속도 추정 약 9분 02초), 녹화해서 mp4 만드는 법, 길 때 줄일 문장, 예상 Q&A 16개 |
| `05_발표영상_초안_AI음성.mp4` | 리허설용 초안 9분 02초 (오프라인 AI 음성 + 자막, 6번에 실제 앱 화면 녹화). 제출은 본인 녹화본으로 |

발표 전에 표지·마무리의 `○○학과 ○○○` 를 바꾸고, 부록 2의 출처 링크를 한 번 열어 본다. 녹화는 9분 안팎을 목표로 한다.

## 참고용

| 파일 | 내용 |
|---|---|
| `01_사업계획서_나물로.md` | 상세 참고본 (리뷰 4차까지 반영). 받는 방법(픽업·저녁 배달)과 배달비 차액·시험 조건, 구독 제외 결정, 상향 목표·보수 시나리오, 수익 정의·시장 범위·자금 가정 |
| `04_레퍼런스_나물로.md` | 시장·경쟁·AI·정책 레퍼런스와 v4 슬라이드별 인용 위치 |
| `06_발표레퍼런스_피치덱.md` | 피치덱 레퍼런스 (공식 가이드, 유튜브 강의, 실제 피칭 영상) |
| `07_나물_도메인리서치.md` | 나물 분류·안전·원산지·가격·제철·조리 과학 |
| `08_리뷰요청_codex.md` | Codex 리뷰 요청서 (v3 상세본 기준) |
| `09_리뷰반영_내역.md` | 1~4차 리뷰 지적과 발표자 요청(배달 옵션·구독 제외·P-S-B-V 점검·전통시장과 지역 상권 중심)을 어떻게 반영했는지 |
| `10_리뷰요청_codex_2차.md` | Codex 2차 리뷰 요청서 (v4 기준: 대학원생 자료로서의 자연스러움 · 검색 가능성 · 수정 확인) |
| `11_리뷰요청_codex_3차.md` | Codex 3차 리뷰 요청서 (v4.2 기준: 배달·구독 결정의 타당성 · 과제 구성 충족 · 파일 간 일관성) |
| `12_리뷰요청_codex_4차.md` | Codex 4차 리뷰 요청서 (v4.3 기준: 3차 지적 반영 판정 · 늘어난 설명 덜어내기 · 새 가정 · 제출 전 최종 점검) |
| `13_리뷰요청_codex_5차.md` | Codex 5차 리뷰 요청서 (v4.5 기준: 중심 문장과 네 가지 축의 흐름 · 지역 상권 메시지의 설득력 · 옛 표현과 회귀 · 새 문장의 자연스러움) |
| `상세본_v3/` | 이전 상세본 (25장 PPT, 대본). 저장소에만 있고 리뷰용 zip에는 넣지 않는다 |
| `review/slides_text.md` | v4.5 PPT의 텍스트·표·노트 추출본 |
| `prototype/nm_prototype.html` | 클릭형 웹앱 프로토타입 (한 파일, 브라우저로 열면 시연 모드). 게시본: https://claude.ai/artifact/JinGR2bajKN6bz9NgK85qc |

## 다시 만들기

모든 스크립트는 이 폴더 기준 상대경로로 동작한다. 저장소 루트의 `package.json` 이 ES 모듈이라, 하위 폴더마다 CommonJS `package.json` 을 두었다.

```bash
# 1) 프로토타입 (Python 3) — PRETENDARD_TTF 를 주면 페이지 글자로 서브셋을 새로 만든다 (fonttools)
python3 prototype/build.py

# 2) 앱 화면 캡처 · 시연 녹화 · 점검 (Node 18+, Playwright + Chromium, ffmpeg) — 버전은 package-lock.json 기준
cd capture_src && npm ci && npx playwright install chromium
node stills.js && node record.js && node check2.js && cd ..

# 3) 대본 → 슬라이드 노트용 script.json + 03 문서, 그리고 덱 (pptxgenjs 4.0.1)
cd deck_src && npm ci
python3 make_script.py ../03_발표대본_나물로.md && node build_deck.js && cd ..

# 4) 미리보기 PDF와 영상용 슬라이드 이미지 (LibreOffice, poppler)
soffice --headless --convert-to pdf 02_발표자료_나물로.pptx
mkdir -p /tmp/namul_slides && pdftoppm -r 192 -png 02_발표자료_나물로.pdf /tmp/namul_slides/s

# 5) AI 음성 초안 영상 (sherpa-onnx 1.13.8 — 2.x 는 한국어 음소 변환이 빠져 무음)
pip install -r video_src/requirements.txt
mkdir -p .cache/tts && curl -L https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-mimic3-ko_KO-kss_low.tar.bz2 | tar xj -C .cache/tts
NAMUL_SUB_FONT=/path/to/NanumGothic-Bold.ttf python3 video_src/make_video.py /tmp/namul_slides 05_발표영상_초안_AI음성.mp4 0.86
```

| 경로 | 내용 |
|---|---|
| `prototype/` | `template.html`(원본) · `build.py` · `icons.json`(Fluent Emoji PNG, base64) · `pretendard-subset.woff2` · 라이선스 |
| `capture_src/` | `stills.js`(→ `assets/screens`) · `record.js`(→ `assets/demo`) · `check.js` · `check2.js`(리뷰 재현 시나리오) |
| `deck_src/` | `script_data.py`(대본 단일 원천) · `make_script.py` · `ko_norm.py`(숫자 한글 읽기) · `build_deck.js` · `theme.js`(테마 색) |
| `video_src/` | `make_video.py`(슬라이드 + TTS + 자막 + 시연 오버레이) · `tts_lib.py` · `requirements.txt` |
| `assets/` | 덱에 쓴 앱 화면 PNG, 시연 녹화 |

받아쓰기로 발음을 점검하려면(`tts_lib.cer`) ASR 모델 `sherpa-onnx-zipformer-korean-2024-06-24` 를 같은 `.cache/tts` 에 풀어 둔다 (asr-models 릴리스).

## 출처 · 라이선스
- 3D 아이콘: Microsoft Fluent Emoji (MIT) — `prototype/FLUENT_LICENSE.txt`
- 글꼴: Pretendard (SIL OFL 1.1) — `prototype/PRETENDARD_LICENSE.txt`, 프로토타입 HTML 에 서브셋 인라인
- 앱 화면 속 매장·가격·선호도·예측 수치는 시연용 예시다.
