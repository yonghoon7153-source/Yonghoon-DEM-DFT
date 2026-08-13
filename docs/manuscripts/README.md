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
