# db/ — 값과 **값의 자격**

이 폴더는 계산 결과 저장소가 아니라 **"이 값을 써도 되나"** 를 정하는 원장이다.
숫자만 찾으러 왔다면 여기가 아니라 `webapp` 화면(`/explorer`)이 편하다.
숫자를 **원고·그림·발표에 넣으려고** 왔다면 아래 순서를 지킨다.

## 값을 인용하기 전에 — 세 파일, 이 순서

| 순서 | 파일 | 무엇을 정하나 |
|---|---|---|
| ① | `properties/canonical_registry.json` | **정본 값** 42항목. 그 값이 어느 원자료의 어느 키에서 나왔고, 어떤 method_id·comparison_group 에 속하며, 무엇이 금지(`prohibitions`)인가 |
| ② | `properties/citation_hazards.json` | **인용 금지·보류** 29건. 파일마다 흩어져 있던 단서를 모은 표. `level` 이 BLOCKED 면 어떤 형태로도 인용 금지 |
| ③ | `governance/decisions.json` | **판정** 22건. 규약·보고량·마감·게이트를 사람이 비준한 기록. ①②가 서로 다르게 말하면 여기가 이긴다 |

레지스트리 42항목의 지위: canonical 25 · provisional 13 · source_pending 3 · retracted 1.
**provisional 은 "아직 아니다" 이지 "거의 맞다" 가 아니다.** retracted 는 값이 살아 있어도 인용하면 안 된다 —
지운 게 아니라 무엇이 왜 틀렸는지를 남긴 것이다.

## 검증은 명령 한 줄

```bash
python3 tools/db/validate_canonical.py          # 42항목 ↔ 원자료 대조 + 거버넌스 그래프 무결성
python3 tools/db/validate_canonical.py --audit  # 죽은 출처·미배선 계보까지
```

화면 쪽에서 같은 것을 부르려면:

```bash
cd webapp && python3 -c "import canonical as C; r=C.registry(); \
  print(len(C.validate(r)), len(C.validate_governance(r)), len(C.validate_hazards()))"
# 0 0 0 이어야 한다 (레지스트리↔원자료 · 결정↔판정 · 인용위험 원장 자체)
```

⛔ 이 검사들이 **못 하는 것**: 값이 물리적으로 맞는지는 아무도 검사하지 않는다.
초록은 "원장이 자기 원자료와 일치한다" 는 뜻이지 "이 수가 옳다" 는 뜻이 아니다.

## 지문으로 봉인된 파일 — 한 글자도 고치지 마라

`ratification.content_digest` 가 박힌 카드 **8건**은 `ratification` 을 뺀 본문의 sha256 에 묶여 있다.
오탈자 하나만 고쳐도 지문이 어긋나고 승인이 무효로 보인다. (2026-09-09 재계산 대조: 8/8 일치)

```
properties/b2o3_cell_expansion_prereg_2026_09_07.json
properties/b2o3_md_closed_retrospective_2026_08_25.json
properties/b2o3_uma_vs_dft_force_prereg_2026_09_08.json
properties/cascade_d_rel_estimand_2026_09_08.json
properties/lpsocl_box331_closure_conditions_2026_09_07.json
properties/sdcp_c12_claim_prereg_2026_08_31.json
properties/sdcp_c12_protocol_2026_08_30.json
properties/sdcp_polaron_pilot_prereg_S0_2026_08_31.json
```

`governance/decisions.json` 의 비준된 결정 **18건**도 같은 규약(`ratification.decision_digest`,
`sha256:` 접두사)으로 묶여 있다 — 18/18 일치.
표시를 붙이고 싶으면 손으로 고치지 말고 **재비준 절차**(`tools/sdcp/prereg_ratify.py`)를 탄다.

같은 이유로 **사전등록 파일은 사후 편집 금지**다(`prereg_d_rel_2026_08_28.json` 등).
SUPERSEDED 표시만 붙이고 값은 그대로 둔다 — 기준을 측정 뒤에 고치지 않는 것이 사전등록의 실체다.
`status_history` 배열도 압축·요약·삭제하지 않는다. 그 항목 하나하나가 "결과를 보기 전이었다" 는 증거다.

기계 필드명도 개서 금지다 — `kind: "estimand"` · `estimand_card/v1` · `canary_geometry` ·
hazard id `HZ-…` · 결정 id `D-2026-…`. CLAUDE.md 의 2026-09-01 용어 규율이 바꾸라고 한 것은
**사람이 읽는 산문**(보고량 카드 · 대조 잡)이지 경로가 아니다.

## 폴더 지도

| 경로 | 무엇 | 지금 상태 |
|---|---|---|
| `properties/` | 401 파일 (csv 197 · json 181). 수치 산출물이 대부분이고 그 사이에 **원장 2개**(canonical_registry · citation_hazards)와 **사전등록·마감 카드 19장**이 이름으로만 섞여 있다 | 색인 없음 — 카드 축은 `decisions.json` 의 `card`/`record` 필드로 역추적하는 것이 유일한 진입로다 |
| `governance/` | `decisions.json`(결정 22) · `assessments.json`(게이트 판정 4) · `artifacts.json`(repo 밖 원자료 12) | 결정 그래프는 끊긴 참조 0건. **판정은 값 옆이 아니라 assessments 에 쓴다** — 값 옆에 쓰면 consumer 마다 '현재 판정' 을 다르게 고른다 |
| `structures/` | 369 파일. 좌표 저장소. xyz + POSCAR(.vasp) **페어**가 배포 규약이라 "아무도 참조 안 하는 파일" 로 보이는 것 상당수가 짝의 다른 쪽이다 | 안내문 `STRUCTURES_NOTE.md` 는 하위 12폴더 중 3개만 다룬다 |
| `interphases/` · `compositions/` · `doping/` · `pipelines/` | 2026-06 초기 스냅샷. 계획서인지 결과인지 파일만 봐선 안 갈린다 | `interphases/li3n.json` 의 UMA 값 2건은 2026-09-09 에 `_RETRACTED_` 로 격리했다 |
| `external/` · `knowledge/` | 외부 소환값·fairchem 기록. `external/PENDING.md` 는 TODO 가 아니라 **차단 목록**이다 | 활성 |
| `literature/` | 레거시 사본 9편. **문헌 정본은 `litdb/`** (digest 219편) — 산문은 litdb, 표(csv)만 여기 | 2026-06 에서 멈춤 |
| `_index.json` | ⚠ **2026-06-02 스냅샷.** 이름이 `_index` 라 목차로 오인하기 쉽지만 **값의 근거가 아니다** | 3개월 낡음 |
| `file_comments.json` · `file_highlights.json` | litdb 그림·문서에 달린 사람 주석. 계산 결과가 아니다 | 활성 |

## 401개를 어떻게 읽나

파일 이름에 **지위가 안 들어 있다.** `sdcp_stageA_closure_conditions_2026_08_29.json`(SUPERSEDED)과
`lpsocl_box331_closure_conditions_2026_09_07.json`(active·비준)은 이름만으로 구분이 안 된다.
그래서 순서가 이렇다:

1. **먼저 `governance/decisions.json` 을 연다.** 22건의 `id`·`decision_state`·`card`/`record` 필드가
   지금 살아 있는 캠페인의 지도다. `decision_state: active` 만 집행된다 —
   `proposed` 는 사람이 비준하기 전이라 **규칙이 아니다**.
2. 값이 필요하면 `properties/canonical_registry.json` 을 `metric`/`system` 으로 찾는다.
   `blocking_gate` 가 있으면 `gate_detail.lineage.gate_outcome` 을 같이 본다 —
   **`not_assessed` 는 실패가 아니다**(D-2026-08-20-no-retro-gate-without-artifact).
3. 그 값을 문장으로 쓰기 전에 `properties/citation_hazards.json` 을 `claim`(`<metric>@<system>`)
   또는 파일 경로로 조회한다. `forbidden_phrases` 는 숫자 결속이 못 잡는 **산문**을 잡는다.
4. 캠페인이 닫혔는지는 `properties/<계>_closed_<날짜>.json` 을 본다 —
   확정값 · 허용 서술(이대로만) · 금지 서술 · 재개 조건이 그 안에 있다.
   처음 오는 사람에게 가장 잘 복원되는 파일은 `lpsocl_box331_closure_conditions_2026_09_07.json` 이다
   (§0 "먼저 박는 사실" 부터 시작한다).

## 이 README 가 **안 하는 것**

- 401개 파일의 목록이 아니다. 카드 19장을 세우는 색인은 **아직 없다** —
  `db/_index.json` 은 2026-06-02 스냅샷이라 이 축을 한 건도 담고 있지 않다.
- 값의 타당성을 보증하지 않는다. 이 폴더의 어떤 게이트도 물리를 검사하지 않는다.
- 원격 서버 원자료의 존재를 보증하지 않는다. `governance/artifacts.json` 에 등재된 것은 12건이고,
  db 텍스트 안의 원격 경로는 그보다 훨씬 많다.

---
*신설 2026-09-09 (묶음 J). 숫자(42 · 29 · 22 · 401 · 8 · 18)는 그날 실측이다 — 갱신할 때 다시 센다.*
