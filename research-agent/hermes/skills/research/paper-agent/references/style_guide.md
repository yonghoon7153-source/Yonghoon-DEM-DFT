# 문체·표기 규칙 (모든 노트·디제스트·메일 공통)

## 어체
- 자연스러운 한국어 평서체("~다", "~했다", "~로 보인다"). 개조식은 표·리스트 안에서만.
- **번역투 금지**: "~에 의해 수행되었다", "~되어진다", "~함에 있어", "~를 통해 ~하는 것을 가능하게 한다", "~로 여겨진다" 같은 표현을 쓰지 않는다. 능동태 위주로 짧게 쓴다.
  - 나쁨: "본 연구에서는 DEM 시뮬레이션을 통해 공극률이 예측되어졌다."
  - 좋음: "이 논문은 DEM으로 공극률을 예측했다."
- 한 문장에 한 가지 주장. 접속사로 늘어지는 문장은 끊는다.
- 확신 정도를 구분해 쓴다: "측정했다"(논문이 보고) / "~로 해석한다"(저자 해석) / "내 생각에는"(에이전트 판단).

## 고유명사·전문용어
- 재료명, 기법명, 장비명, 물리량 기호, 저널명, 사람 이름은 **영어 원문 유지**: NCM811, Li₆PS₅Cl(LPSCl), argyrodite, DEM, DFT, MLIP, LIGGGHTS, COMSOL, percolation threshold, Hertz–Mindlin, W_ad, C₄₄, Nature Communications, Zeier.
- 한국어로 굳어진 개념어는 한국어 + 필요시 괄호 영어: 공극률(porosity), 접촉수(coordination number), 배위, 소성 변형(plastic deformation).
- 수치는 반드시 단위·조건과 함께: "porosity 25 % (370 MPa, 25 °C)".
- 아래첨자는 유니코드(Li₆PS₅Cl)나 Obsidian 수식(`$C_{44}$`) 중 하나로 통일 — 본문은 유니코드, 수식 블록은 LaTeX.

## Obsidian 문법
- 노트 상단 YAML frontmatter 필수(`tags`, `aliases`, `doi`, `journal`, `if`, `tier`, `relevance`, `status`, `keywords`, `date_added`).
- 링크는 위키링크: `[[2026 - Kissel - Mechanofusion-derived cathode composite]]`, 키워드 MOC는 `[[dem battery]]`.
- 콜아웃 활용: `> [!abstract]` 원문 요약, `> [!tip] 내 연구 연결`, `> [!warning] 비판 포인트`, `> [!quote]` 인용문.
- 태그는 `#paper/dem`, `#paper/dft`, `#paper/anode-free`, `#tier/A`처럼 계층형.
- Dataview 인라인 필드는 frontmatter로 대체(중복 금지).
- 파일명에 `: / \ * ? " < > | # ^ [ ]` 금지.

## 디제스트(메일) 톤
- 첫 두 줄은 해요체 인사 + 오늘 요약 한 문장. 본문은 평서체.
- 논문마다 "왜 골랐나 → 무엇을 했나 → 내 연구에 어떻게 쓰나" 순서.
- 마지막에 References 섹션: `저자. 제목. 저널 연도. DOI` 형식, DOI 링크 포함.
