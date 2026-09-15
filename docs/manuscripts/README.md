# docs/manuscripts

AF-ASSB AgNO₃–C–PVP 원고(v5) 대외 산출물.

| 파일 | 무엇 |
|---|---|
| `Table_S2_DFT_parameters.docx` | SI Table S2 (Li₃N(001) / LiC₆(0001) DFT 파라미터, 2열 압축판) |
| `table_s2_build.js` | 위 docx 의 생성 스크립트 (docx-js) |

생성:

```bash
export NODE_PATH=/root/.claude/skills/synced/docx/node_modules   # docx 모듈 위치
TABLE_S2_OUT=<출력폴더> node docs/manuscripts/table_s2_build.js [--compact | --nonotes]
```

각주 3종 — 플래그로 고른다:

| 모드 | 각주 | 쓰는 곳 |
|---|---|---|
| (무플래그) `full` | 2문단 | 자리가 넉넉할 때 |
| `--compact` | 표 각주 2줄 (ᵃ/ᵇ 표시가 표 안에 함께 붙음) | 참고용 — **쓰지 않기로 함 (2026-08-13)** |
| `--nonotes` | 없음 | **SI v6 제출본이 이 형태** |

수치 근거·리비전 방어 논지는 `kb/syntheses/li3n_barrier_revision_defense_2026_08_12.md`,
원본 숫자는 `db/properties/diffusion.json` 과 `db/properties/li3n_barrier_origin.csv`.

**제출본에 없는 것**(2026-08-13): 각주 3항목 — ① 왜 두 표면에 다른 방법을 썼는가
② LiC₆ 0.290 이 보수적 하한인 이유 ③ 0.118 이 문헌 0.133(ref [54])과 정합.
`0.133` 은 원고·SI 전문에 0회 등장한다. **각주는 리비전에도 넣지 않기로 확정** —
필요하면 response letter 본문에 문장으로만 쓴다 (문구는 kb 카드에).

---

## SDCP 원고 v5 (self-doped conducting polymer, dry-processed ASSB cathode)

| 파일 | 무엇 |
|---|---|
| `SDCP_DFT_methods_TableS1.docx` | 본문 `Computational details` 삽입문단 + SI Table S1 (DFT 계산 조건) |
| `sdcp_dft_methods_build.js` | 위 docx 의 생성 스크립트 (docx-js) |
| `sdcp_dft_methods_draft_2026_08_23.md` | 근거·파이프라인 리스트·인용 제약·VASP↔QE 변환표 |

생성:

```bash
NODE_PATH=<docx 설치 경로> SDCP_DFT_OUT=<출력폴더> node docs/manuscripts/sdcp_dft_methods_build.js
```

수치 출처는 발주 번들 `sdcp_wave1_2026_08_12` (MANIFEST.json · INCAR · KPOINTS · POSCAR 실측).
⚠ **Table S1 은 조건 표이지 결과 표가 아니다** — E_ads 수치는 wave1 회수 후 게이트를 통과해야
생긴다. Ref. S4(U = 6.2 eV) · S5(AFM 배열) 은 **출처 미정**으로 비워 뒀다.

> ### ⚠ 위 세 파일은 **08-23 판**이다 (2026-09-14 병합 회수, `47e080690`) — **현행은 아래**
>
> | 08-23 (회수본, 이력) | 현행 (이걸 쓴다) |
> |---|---|
> | `SDCP_DFT_methods_TableS1.docx` · `sdcp_dft_methods_build.js` | **`Table_S1_DFT_parameters.docx` · `table_s1_build.js`** (2026-09-08) — 제목 "adsorption-energy DFT calculations" · 자가도핑 행 제거 · 분자 계산은 Supplementary Note 2 각주 · Ref 번호 본문 계열 |
> | 본문 `Computational details` 초안 | `kb/papers/self_doping_dft_paragraph_2026_09_08.md` (분자 ORCA 문단 + 슬랩 문단 두 문장 개정 · 흡착 문단은 **보류 초안**) |
> | `Methods_DFT_v9_for_coauthors.docx` / `methods_dft_v9_for_coauthors.md` (08-30) | 공저자용 상세판. ⚠ 코드 표기가 **VASP** — 원고·Table S1 은 **QE**. 값 복구 시 맞출 것 (1저자) |
> | *"Ref. S4 · S5 출처 미정"* | S4(U 6.2) 는 08-23 당일 닫힘(Jain 2011) · AFM 배열은 인용 대상 아님 — 위 문장은 신설 시점 문구다 |
>
> ⛔ E_ads 절대값·0.346 eV 헤드라인은 **인용 보류** (`HZ-sdcp-wave1-absolute-eads`, 마감 카드
> `db/properties/sdcp_neutral_closed_2026_08_28.json`). 어느 판의 문서든 값을 채우지 않는다.
