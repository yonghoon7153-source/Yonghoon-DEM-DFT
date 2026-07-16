# 랩 AI 워크플로 규약 — "AI coding agent 설치 및 활용" 2편 digest (2026-07-16)

출처: Battery Mater. Lab (한양대) 내부 공유 슬라이드 11쪽 (터미널 스샷 기준 작성자 강준희).
성격: 논문 아님 — **랩원들이 실제로 쓰는 AI 작업 패턴**. 이 레포에서 사용자(안용훈)를
지원할 때 따라야 할 실행 규약으로 소화한다. (사용자 지시: "이 내용도 확실히 알고 있음 좋을듯")

## 슬라이드별 핵심

1. **Coding agent 설치·활용**: 터미널 구동형(Codex, Claude Code) — 로컬 파일 읽고 프로그램
   직접 구동, 자연어로 복잡한 작업 수행. (Codex는 ChatGPT Plus로도 충분, 무거운 작업 제외.)
2. **Raw data → 그림 파일**: `raw data.xlsx` → 기존 Figure와 **x/y-axis·boundary·font·size
   format 완전 동일**하게 그려서 **png/svg/Origin(opju) 각 1개씩** 생성 요청. 셀 면적
   (예 1.3273 cm²) 등 환산 조건을 프롬프트에 명시. 결과 확인→수정 요청→**format 저장·고정
   해서 재사용**이 핵심 패턴. 예시 그림: areal capacity + C.E. vs cycle number 이중축.
3. **SVG → Figma figure set**: svg(벡터) export 후 Figma에서 조립이 최선 (Illustrator 유사,
   GPT 연동·개별 객체 편집이 더 쉬움). "Origin 열었다 닫았다"보다 벡터 직접 편집 + codex
   데이터 가공 조합이 가장 편함.
4. **ChatGPT 프로젝트**: 소스 파일(원고 docx 등) + 프로젝트 지침 설정. **지침은 한글로 쓰고
   "영어로 더 구체화/체계화해달라"고 시킨 뒤 그 영어 지침을 다시 넣는** 2단계 부트스트랩.
5. **원고 지침 예시** (Wiley R&D 섹션): 참조 원고 2편의 스타일(figure 도입 방식, 패널별 논의,
   관찰→기전 해석 연결)을 모방; abstract + figure set + 패널별 설명 제공 → ~2,500단어 R&D
   초안; **모든 패널 빠짐없이 논의**, figure 간 자연 전환, 단순 기술이 아닌 해석 동반,
   "Figure 2a,b" 표기 통일, publication-ready 초안 수준 요구.
6. **Manuscript 작성 단위**: **Figure 단위 요청이 최선** (통짜 요청은 세부 수정이 괴로움).
   추천 플로우 = Abstract + figure set + 캡션 + rough 설명 → rough draft → figure별 정련.
   실제 예: Figure 1a~1g 패널별 내용·키메시지를 한글로 조목조목 지정 (두께별 areal capacity,
   단면 SEM, 율속, porous-electrode theory 기반 reaction-distribution δ, 두께×전류밀도 δ
   contour까지 — 후막 전극 reaction heterogeneity 서사).
7. **세부 수정**: 초안 보고 수정 필요 부분만 재요청 (프로젝트에 소스 넣어두고). 마음에 안
   드는 문장은 **"학술자료에 적합한 5가지 문장으로 재번역"** 전용 프로젝트에 넣고 후보 중
   선택 (어떤 문장이 적합한지는 본인이 판단할 줄 알아야 함).
8. **Reference list**: 링크 수십 개 던지면 오류·접근불가 많음 → **로컬에 PDF 전부 다운받고
   + 정확한 서지 format 예시 몇 개(bold/italic까지)** 주고 word로 뽑아달라 하면 몇십 개든
   정확. (뭐가 제일 효율적인지는 미확정이라고 솔직히 적음.)
9. **기타 1**: figure set 고화질 export는 ppt 그룹화→export 요청 또는 Figma면 그냥 export.
   Schematic illustration은 요청사항(그림체·배경·text 유무·색감)을 한글로 상세히 →
   **프롬프트 보강 요청 → 보강된 프롬프트+참고 이미지로 생성**; 통짜보다 **개별 component
   추출이 유용**. 웬만한 FEM은 AI가 가능(복잡 geometry 제외), **구동 중인 COMSOL 오류를
   coding agent가 직접 확인·수정**, dQ/dV 등 전기화학 신호분석·이미지 처리도 자연어 요청,
   fitting·데이터 처리는 전부 agent에게 코드 짜게 해서 활용 (오리진 말고).
10. **기타 2**: 요청 시 **"웹 검색"·"최신 문헌 참고" 키워드 + 참고문헌 list-up 요구**가
    효과적; github 관련 코드 검색 요청; `codex --yolo` (승인 생략 모드); **기호/첨자 오류
    잦음 → text 복붙 후 수정 필요**; 온라인 DB에 방법 있으면 DFT급 무거운 계산도 리소스만
    있으면 가능; **하고 나서 methodology·코드를 읽어볼 필요는 있음**. 예시: 전극 미세구조
    SEM → 참고문헌 2편 + 웹 최신문헌 검색 → **binary map 변환 기반 void ratio 정량화**
    (LPSC SEM, dendrite-vulnerable sites 마킹, void ratio=0.148).
11. **기타 3 (Origin/ppt 위생)**: boundary thickness·font·size 반드시 통일(copy-paste
    format), ppt 빠른실행 메뉴 정비, align 맞추기, Origin export 그림들 사이즈% 통일.

## 이 레포에서 내가 따를 실행 규약 (적용 지침)

- **그림 산출 규약**: 사용자가 그림을 요청하면 (i) 기존 figure의 format(축·경계·폰트·크기)
  재현을 우선 확인, (ii) **svg + png 동시 산출** + 원데이터 csv 병치 (Origin 재현용),
  (iii) 포맷 파라미터(폰트, 축 범위, 크기)를 스크립트 상수로 고정해 재사용 가능하게.
  ⚠ opju(Origin 네이티브)는 Windows Origin 필요 — 클라우드/WSL에서는 svg/png/csv까지
  만들고 opju는 사용자 로컬 Origin에서 여는 흐름으로 안내.
- **원고 작업 규약**: R&D 섹션은 **figure 단위**로 작성/수정; 모든 패널 빠짐없이 논의;
  관찰→기전 해석 연결; 참조 원고 스타일 모방 요청이 오면 스타일 요소(도입·전환·표기)를
  명시적으로 추출해 적용. 문장 다듬기는 후보 5개 제시 패턴.
- **Reference 규약**: 로컬 PDF + 형식 예시 기반으로 정확 서지 생성; 링크만으로 만들지 않음;
  기호/첨자(µ, ₓ, ³⁺ 등) 오류를 산출 후 자체 검수.
- **문헌 반영 규약**: "웹 검색/최신 문헌 참고" 요청엔 반드시 **참고한 문헌 list-up 동봉**
  (우리 §F1 날조금지 규약과 합치).
- **이미지 정량화**: SEM/미세구조 이미지 → binary map → void ratio/피복률 정량화는 우리
  파이프라인과 직결 (extract_2d_microstructure, MPM morphology 비교) — 요청 시 스크립트로
  즉시 구현 가능.
- **검증 문화**: agent 산출물은 methodology/코드를 반드시 되읽는다 (deck의 마지막 경고 =
  우리 2-agent 리뷰 관행과 동일 정신).

## 우리 파이프라인과의 접점

| Deck 항목 | 우리 쪽 대응물 |
|---|---|
| raw→고정format 그림 | scripts/generate_comparison_plots.py 계열 (포맷 상수화 관행 강화) |
| porous-electrode δ (reaction distribution) | **STEP4-v2가 상위호환** (복셀-DFN 반응분포 실계산) |
| SEM binary-map void ratio | extract_2d_microstructure + MPM 형상 비교 (스크립트화 후보) |
| COMSOL 오류를 agent가 직접 | 우리 COMSOL-패리티 selftest/에너지 감사 문화 |
| dQ/dV 신호분석 | STEP4 곡선 후처리 후보 (V(t)→dQ/dV 즉시 가능) |
| 참고문헌 로컬 PDF 규약 | litdb (digest + pdfs/ 보관) — 이미 동일 철학 |
