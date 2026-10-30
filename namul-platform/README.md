# 나물로 (Namullo) — 창업 아이템 발표 세트

> 수업 과제(Problem–Solution–Business–Vision, 8–10분 PPT 발표 + mp4)용 산출물.
> **이 폴더는 연구 프로젝트(`degradation-degeneracy/`, `bms-balancing/` 등)와 무관하며, `claude/namul-platform` 브랜치는 `namul-platform/` 경로만 다룬다.**

## 산출물

| 파일 | 내용 |
|---|---|
| `02_발표자료_나물로.pptx` | 발표 PPT 25장 (기업 보고형). 슬라이드 노트에 대본, 14번에 시연 영상 내장 |
| `02_발표자료_나물로_미리보기.pdf` | LibreOffice 렌더 미리보기 (글꼴 대체로 줄바꿈이 PowerPoint와 조금 다를 수 있음) |
| `03_발표대본_나물로.md` | 장표별 대본 · 시간표(사람 속도 약 9분 19초) · 녹화해서 mp4 만드는 법 · 예상 Q&A 8개 |
| `05_발표영상_초안_AI음성.mp4` | 9분 1초 초안 (오프라인 AI 음성 + 자막, 14번에 실제 앱 화면 녹화). 연습·비상용, 제출은 본인 녹화 권장 |
| `01_사업계획서_나물로.md` | 사업계획서 v3 — AI 엔진 4종, AI 운영비, 나물 도메인, 팀, 자금 사용 계획 |
| `07_나물_도메인리서치.md` | 나물 분류 · 안전(꼭 데쳐 먹는 나물, 독초 혼동) · 원산지 · 가격 · 제철 문화 · 조리 과학 |
| `04_레퍼런스_나물로.md` | 시장 · 벤치마크 · AI · 정책 레퍼런스와 슬라이드별 인용 위치 |
| `06_발표레퍼런스_피치덱.md` | 피치덱 레퍼런스 (공식 가이드 · 유튜브 강의 · 실제 피칭 영상 · 덱 모음) |
| `08_리뷰요청_codex.md` | **Codex 리뷰 요청서** — 검증할 수치 20개 · 산식 · 코드 점검 항목 · 질문 |
| `review/slides_text.md` | PPT 25장의 텍스트 · 표 · 노트 추출본 (텍스트로 리뷰할 때) |
| `prototype/nm_prototype.html` | 클릭형 웹앱 프로토타입 (단일 파일, 브라우저로 열면 시연 모드). 게시본: https://claude.ai/artifact/JinGR2bajKN6bz9NgK85qc |

## 소스

| 경로 | 내용 |
|---|---|
| `prototype/template.html`, `prototype/build.py` | 프로토타입 원본 → Pretendard 서브셋(woff2)과 Fluent Emoji 아이콘을 인라인해 `nm_prototype.html` 생성 |
| `deck_src/` | `deck3.js`(pptxgenjs 4.0.1) · 대본 단일 원천 `script_data.py` · `make_script.py`(대본 문서 + `script.json`) · `ko_norm.py`(숫자 한글 읽기) |
| `video_src/` | `make_video3.py`(슬라이드 + TTS + 자막 + 시연 오버레이) · `tts_lib.py`(sherpa-onnx 1.13.8, 한국어 VITS) |
| `capture_src/` | Playwright 화면 캡처 · 시연 녹화 · 점검 스크립트 |
| `assets/` | 덱에 쓴 앱 화면 PNG, 시연 영상 원본 |

**재현 주의**: 스크립트에는 원래 작업 세션의 절대경로(`/tmp/claude-0/.../scratchpad`)가 하드코딩되어 있다. 다시 돌리려면 각 스크립트 상단의 경로 상수를 이 폴더 기준으로 바꾼다. 영상은 sherpa-onnx **1.13.8** 을 써야 한다(2.x 는 한국어 음소 변환이 빠져 무음).

## 리뷰 받는 법
- PR 댓글에 `@codex review` 를 남기거나, `08_리뷰요청_codex.md` 를 Codex 에 함께 준다.
- 수치는 2026-10-29~30 웹 검색 기준이며 일부 기사 원문은 확인하지 못했다(요청서 §2 '확인 수준' 열).

## 출처 · 라이선스
- 3D 아이콘: Microsoft Fluent Emoji (MIT) — `prototype/FLUENT_LICENSE.txt`
- 글꼴: Pretendard (SIL OFL 1.1), 프로토타입 HTML 에 서브셋 인라인
- 앱 화면 속 매장 · 가격 · 수치는 시연용 예시다.
