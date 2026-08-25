# 다음에 할 일 (2026-08-25, R4 대응 직후)

정본은 `codex_absorb_verdict_20260825.md` 와 `findings.json` 이다.  이 파일은 **순서**만 정한다.

---

## A. 흡수 전 (코드 규율) — R4 잔여 5건 + 배터리 3건

### A0. 배터리 잔여 3건 ⟵ **지금 바로**
31 돌연변이 중 29 는 계약을 만족했다.  남은 셋:

| 항목 | 증상 | 뜻 |
|---|---|---|
| `R4 계획 스키마 검사 제거` | rc≠0 인데 파싱된 FAIL 0 | 배터리가 결과를 못 읽었거나 시험이 안 물었다 |
| `R4 PTFE 기록 계약 제거` | ㊸c 만 물고 ㊵e 는 안 물림 | 기대집합이 넓다 (㊵e 는 타입 게이트가 먼저 문다) |
| `조건7 규칙 K` | L-11 이 같이 물림 | 시험이 얽혔다 — K 와 L 이 같은 판정기를 공유하므로 |

⇒ 앞의 둘은 **기대집합 정정**, 셋째는 K/L 공유를 명시적으로 기대에 넣는다.
⚠ "정정" 이 아니라 **구멍**일 수도 있다 — 고치기 전에 각각 손으로 재현할 것.

### A1. solver-affecting CLI **전수 생성** (R4-CX-03 잔여)
지금은 allow 목록이 손으로 유지된다.  `argparse` 파서를 순회해 물리에 영향을 주는
옵션을 **뽑아내고**, 그 전부가 `PROTOCOL_FIELDS` 또는 numeric schema 에 **정확히 한 번**
등재됐는지 검사한다.  등재 안 된 옵션이 있으면 오류.
· 근거: `--sigma-superp` 가 전자 solver 에 실제로 쓰이는데 `PROTOCOL_FIELDS` 에 없다.

### A2. cross-dir raw diff-set == `expect_differ` (R4-CX-05 잔여)
지금은 "등록 축이 하나라도 다르면 파생 id 차이를 허용" 이다.  Codex 반례: 등록 축과
`plate_rule` 을 **같이** 바꾸면 추가 confound 가 숨는다.
⇒ 두 디렉터리의 raw 차이 집합을 계산해 `expect_differ` 와 **정확히 일치**를 요구한다.

### A3. 선언 뒤집기 pass-mutant 봉인 (R4-CX-05 잔여)
`backend.across_dir=True→False` 같은 것이 아직 통과한다 (생성 시험이 그 필드를
대상에서 빼기 때문).  ㊷d/e 처럼 **선언과 무관한 불변식**을 축마다 세운다.

### A4. selftest 를 구조화 결과로 (R4-CX-06 잔여)
지금 harness 는 stdout 문자열을 읽는다.  `--selftest-json` 을 붙여 exact ID·rc·
timeout 을 기계로 읽게 하고, 배터리가 **failed-ID multiset** 을 비교한다.

### A5. standalone full bundle (R4-CX-08 잔여)
`git bundle create --all` 또는 base+target object 포함.  이번 것은 incremental 이라
빈 저장소에서 `Repository lacks these prerequisite commits` 로 실패했다.

---

## B. 그 다음 — CPU census (GPU 아님)

R4 §7-10 이 정한 순서: **위를 닫은 한 clean SHA 에서** CPU raster-only 로
`bed × origin × side × phase` 접촉 census 를 먼저 낸다.

· 지금 있는 것은 **합성 침대** census 뿐이다 (bottom −28.7 % · top −32.8 %) —
  실침대 σ 감소율이 아니고 인용 불가.
· 이것이 GPU 를 돌리기 전에 p1→p2 가 무엇을 바꿨는지 **싸게** 아는 유일한 방법이다.
· 실침대가 필요하다 (`kit_SBE` / `kit_DBE`).  GPU 없이 CPU rasterize 로 가능.

---

## C. 그 다음 — GPU 8팔 재실행

R4 조건 전부:
· 같은 8 origins 의 SBE/DBE **둘 다** (한쪽만 새로 돌려 옛 값과 섞지 않는다)
· 하나의 새 protocol schema (`p2-`) · **하나의 clean code SHA**
· raw manifest 재계산을 통과한 receipt
· input digest + required component/backend/convergence seal
· bed × origin × side × phase 별 p1→p2 접촉 수 · Σg_plate · plate-energy 몫 census

⚠ 옛 팔(`p1-`)과 새 팔(`p2-`)은 섞이지 않는다 — 이제 규약 해시가 **기계로 집행**한다.

---

## D. 병렬로 — 물성 앵커 (사용자 회신 대기)

· **`σ_SDCP = 250`** 출처: cast film 인가 pressed pellet 인가.  절대값·실험 앵커 주장
  전에 닫아야 한다.  지금은 scenario/assumption 으로만 라벨.
· **`ρ_SDCP`**: 코드 주석이 PROXY 라고 적고 원고 값을 요구한다.

---

## E. 원고 (이 트랙이 원래 목적)

⚠ **C 가 끝나기 전에는 σ_e 절대값·비를 원고에 쓸 수 없다.**  지금 쓸 수 있는 것:
· 기전 서술 (SDCP 표현 부피 · 격자 의존) — CL-25/33/34/41 하향판
· 방법 (STEP1~4 파이프라인 · 규약 정체성 · 계약 검사)
· 격자 미수렴을 **결과로** 적기 (세 값 나란히 + "외삽 불가")
쓸 수 없는 것: 새 σ_e 절대값 · SBE/DBE 비 · p1 시절 값(CL-33/41/58) 전부.
