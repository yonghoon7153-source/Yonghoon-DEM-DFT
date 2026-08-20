# 문서 인덱스

## 설계 결정 (ADR)

| # | 제목 | 요지 |
|---|---|---|
| [0001](adr/0001-store-raw-capacity-only.md) | 정규화된 용량은 저장하지 않는다 | raw mAh 만 저장, mAh/g 는 조회 시 계산 |
| [0002](adr/0002-own-wrd-parser.md) | `.wrd` 를 직접 파싱한다 | 자체 MS-NRBF 리더, numpy 만 의존 |
| [0003](adr/0003-timeseries-on-disk-summaries-in-db.md) | 시계열은 디스크, 요약만 DB | npz + SQLite |
| [0004](adr/0004-cycle-three-reference.md) | 기준 사이클은 3번 | formation 을 열화로 세지 않는다 |
| [0005](adr/0005-multi-criterion-knee.md) | Knee 는 기준 하나로 정하지 않는다 | 4종 계산 + 근거 제시 |
| [0006](adr/0006-frontend-stack.md) | React + TypeScript + uPlot | 대용량 곡선을 가볍게 |

파일명: `adr/0001-store-raw-capacity-only.md` · `adr/0002-own-wrd-parser.md` ·
`adr/0003-timeseries-on-disk-summaries-in-db.md` ·
`adr/0004-cycle-three-reference.md` · `adr/0005-multi-criterion-knee.md` ·
`adr/0006-frontend-stack.md`

## 스펙

- [`raw/specs/wrd-binary-format.md`](raw/specs/wrd-binary-format.md) —
  `.wrd` 바이너리 포맷 전체 구조. 파서 구현의 근거.

## 위키

아직 없음. `python3 tools/new_page.py <type> <slug>` 로 만든다.

Total pages: 0
