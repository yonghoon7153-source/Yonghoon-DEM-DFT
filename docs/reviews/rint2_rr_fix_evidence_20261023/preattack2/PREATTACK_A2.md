# 사전 공격 리뷰 2 회차 — 대상 `fdb48d378..a32fcf32f` (C1–C5 · 묶음 A′ · A″) + Q9 설계 개정 1 (Rint ② RR · 10-23)

> 옮겨 적음 = 메인 (10-23) · 원문 = 독립 에이전트의 마지막 보고 (지시 = 1 회차와 같은 꼴 · 고친 사람의 보고 · 지시 `REPORT_A*` · `BRIEF*` 안 읽음 · CLAUDE.md "Codex 요청 전 사전 공격 리뷰" ③) ·
> 메인 메모 = 맨 끝 절.  숫자 · 전칭은 에이전트 실행 출력이다 — 메인이 다시 돌린 것은 메인 메모에 따로 적는다.

- **방법** — 독립 검토 · 트리 = `a32fcf32f` 사본 · 고치지 않음 · 커밋 없음 · CPU · BLAS 스레드 1 · nice 19.
- **결론** — 코드 P1 0 · P2 1 (X6 · 기록을 편집해야만 닿음) · P3 3 · 변이 33 중 32 잡힘 (살아남은 1 = 동등 변이) · Q9 설계 개정 1 = P2 1 · P3 4 · 질문 2.

## A. 코드 발견

| 등급 | 항목 | 반례 (입력 → 실제 → 기대) | 재현 | 고칠 자리 제안 |
|---|---|---|---|---|
| **P2** | **X6: 못 가른 덩어리 수를 0 으로 바꿔 위 끝을 통째로 숨긴다** (C1 밖 · 알려진 한정 목록에도 없음) | 실제 생산자 기록 5 (QD2-3 · QDX · RAIL5 · QD2-1 · QD4) 의 `n_unsplit_bridging_components` 와 증거 `census` 같은 칸을 둘 다 0 · `upper` → None · 위 끝 칸 = 아래 끝 값 · `ratio_cert_interval` 다시 셈 → 계약 None 5/5 · 판정 SV_UNCHECKED → `[]` (거짓 clear) · QD2-3 [1.0, 2.2898] → [1.0, 1.0000000000000566] (t 1.2) · QD2-1 · QD4 (위 끝 +∞) t 1.2 에서 `[]` · QDX t 2.0 에서 `[]` · census 를 안 고치면 `_census_problem` 이 5/5 거부 → 기대 = 거부 | `tools/atk2_census.py` · `tools/atk2_sv.py` X6 | census 를 기록 밖 출처에 묶는다 — 증서 결합 칸에 census 다이제스트를 넣어 `read_run` 이 step3 주 증서와 대조 · 또는 RCA2-03 의 S0 결합에 census 세 칸 · `cjunc_block_problem` 에는 census 대조 없음 (grep) |
| P3 | **X3: 아래 끝 ← 위 끝 증서** (알려진 것은 반대 방향 "위 끝 ← 아래 끝" 뿐) | QDX (k 2 · ku 8 · ne 6 · npc 0) 아래 끝의 증서 · G_cut · 비 = 위 끝 것 · 끊은 수 칸 무편집 → 계약 None · 구간 [1.378, 3.155] → [3.155, 3.155] · t 2.0 에서 UNCHECKED → DEPENDENT (보수 쪽) · QD2-3 · RAIL5 = `c==0 ∧ L≠M` 거부 · QD11R · UPLATE = 판 결합 수 대조 거부 | `tools/atk2_sv.py` X3 | 위 끝에 "아래 끝 판에 닿는 계 대비 끊은 쌍 수" 를 생산자가 따로 내고 `U≠L ⇔ 그 수 + npc > 0` 대조 (지금 ⑧ 의 `U≤L` 은 같음을 허용) |
| P3 | **X5: 새 칸 꼴 · 관계 검사가 비를 싣는 끝 (computed) 이 있을 때만 돈다** | QD2-2 (두 끝 +∞) 아래 끝 `n_reach_pairs_cut` = True · False · −1 · 1.0 · "1" · None · 2**63 · NaN · inf · [1] · "0" · 0.0 · 결손 · 10**6 (> c) → 14/14 받음 · QD4 · QD2-1 (위 끝 +∞) 위 끝 ku = 10**6 (> k + ne) → 받음 · 판정 영향 없음 (그 칸을 판정에 안 쓰는 경로) | `tools/atk2_sv.py` X5 | 새 칸 꼴 검사 · ⑧ 관계 검사를 `_topo_problem` 의 `if not (lo_c or up_c): return None` 앞으로 · 위 끝은 상태와 무관하게 대조 |
| P3 | **C4 이후 Codex 등록 탐침 3/10 이 다른 이유로 멈춘다** (증거 호환) | `probe_registration_current.py` 의 `dbe_nonmonotone` · `dbe_origin` · `sv_origin_scope` 무변경 → 셋 다 `ARM_UNREADABLE` (합성 팔에 target_lo · target_hi · scale 없음) · `dbe_nonmonotone` (Codex 의 RCA2-09 원 반례) = 고치기 전 R_MONOTONE_VIOLATION → 지금 ARM_UNREADABLE (단조 검사에 닿지 못함) · `dbe_origin` · `sv_origin_scope` = 고치기 전 정상 → 지금 ARM_UNREADABLE · 1 회차 `atk_rmono` · `atk_rmono2` 도 같음 · 나머지 7 함수 · `probe_certificate` (출처 경로 한 줄만 다름) · `run_review` (137 줄 동일) = 고치기 전과 같음 | `probes.sh` → `logs/r2_*` (고치기 전 = `docs/reviews/rint2_rr_fix_evidence_20261023/preattack/logs/`) | Codex 회차 ① 요청서에 적는다 · 증서 칸을 더한 탐침 어댑터 (`tools/atk2_rmono.py` 의 `rec()` 꼴) |

**알려진 한정의 경계 (새 결함 아님 · 참고)**
- A2 편집을 그대로 (끊은 수 칸 무편집) 했을 때 받는 기록 = 11 (k = 0 인 기록: QD2-1 · QD2-3 · QD4 · RAIL5 · QD11R · FLOAT · PARc1 · UFLOAT · UPLATE 외).
- 이것은 (a′) 꼴에서 새 칸 편집이 0 번인 경우다.
- 13 고정물에서는 정직한 구간이 이미 ≈ [1, 1] 이라 판정이 바뀌지 않았다 (PARc1 비 1.0000000000000067).
- 해가 되려면 k = 0 이면서 병렬 간선 때문에 G 가 실제로 줄어야 한다 — 그런 기록은 찾지 못함 (추정: 원리상 가능).
- ⇒ 한정 문장 "새 칸만 0 으로 맞춘" 은 "k = 0 기록은 편집 없이도" 로 넓히는 것이 정확하다.

## B. 깨지 못한 보장

| 보장 | 시도 | 결과 |
|---|---|---|
| C1 바꿔 끼우기 거부 | 위 끝 ← 주 해 증서 (QD2-3 · RAIL5 · QDX · QD11R · UPLATE) · 아래 끝 ← 주 해 증서 (k > 0 인 SVX · QDX · PARc0) | 전부 거부 (예외 = k = 0 또는 ku + npc = 0 기록 = 위 경계) |
| C1 새 칸 꼴 (computed 끝) | 65 건 (아래 끝 3 기록 × 13 꼴 · 위 끝 2 기록 × 13 꼴) | 65/65 자기 문장으로 거부 |
| C1 독립 출처 ⑦ | QDX 위 끝 `n_sv_faces_cut` 지우고 (a) 편집 | ⑧ 이 거부 |
| C1 생산자 정상 기록 | 13 회로 | 계약 13/13 통과 (FLOAT · UFLOAT · PARc1 받음) |
| 끈 경로 비트 | `atk_bitid` 7 꼴 old ↔ new | 차이 = SV 기록 2 곳의 새 칸 `n_reach_pairs_cut` 하나뿐 |
| C2 칼날 | 텍스트 변이 4 (M1 그냥 a/b · M7 방향 맞바꿈 · 위만 반올림 · 아래만 반올림) | 4/4 를 QD6 이 잡음 (tcj 122 · 119 · 123 · 123/126) · `atk_m7` t = 10.29125393534654 · 2.289808917197574 에서 SV_UNCHECKED · `atk_divdir` 20,081 쌍 위반 0 |
| C3 origin 마다 | 네 꼴 | 넘침 없는 arm1 4.80/4.85/4.40 → `origin_a1` 에서 멈춤 · 넘친 모서리 origin8 a3 · a0 → `origin8_a3` · `origin8_a0` 에서 멈춤 · 단조 · 평탄 → 통과 · `origins` 3 개 기록 |
| C4 띠 | 실제 증서 구간 R2 | 맞닿음 → 멈추지 않음 · 1 ULP 떨어짐 → 멈춤 · 칸 꼴 13 종 (scale True/0/음수/NaN/inf/str · lo > hi · lo 0 · lo None · hi 10**400 · err None · σ NaN/True) → 전부 ARM_UNREADABLE · σ ↔ 띠 결합 = `run_contract` 의 1e-9 대조 |
| C5 | 13 꼴 (옛 이름 · 끝 공백 · 대문자 · 키릴 a · None · 결손 · 개행 · list · rule = kind · requested 1/"true") | 13/13 거부 · 생산자 상수 = 검증기 상수 |

**변이 33 (한 줄 되돌림 · `tools/mut2.py`)** — 32 가 tcj QD2–7 · trc 15 건 · b6 S 중 하나에 걸림 · 살아남은 1 = `c == 0 and L != M` 지운 변이 (앞에서 `k ≤ c` 를 강제하므로 c = 0 이면 k = 0 · 같은 조건을 `k == 0 and L != M` 이 잡는다 = 동등 변이) · C5 kind · rule 변이는 V35 (trc) 만 잡는다 (tcj · b6 S 는 통과).

## C. Q9 설계 개정 1

| 등급 | 항목 | 작은 반례 | 제안 |
|---|---|---|---|
| **P2** | **§3-5 원장으로는 "결과 전" 을 기계적으로 보장하지 못한다** | 단위 시도 #1 (kgy) 완주 · origin 퍼짐 0.0999·W0 → 결과 줄에 "결과 전 멈춤 (OOM)" 이라 쓰고 폴더 지움 · #2 (gabia) 0.1001·W0 → adjusted · 규칙상 "폴더 없는 시도" 는 결과 줄에 사유가 있으면 허용 → #1 = 결과 전 멈춤 분류 · #2 채택 · 그 밖에 결과 줄에 폴더 sha 없음 · 한 원장 항목에 폴더가 둘이어도 하나만 넘길 수 있음 · 결과 줄 여러 번 덧붙이기 금지 없음 | 시도 폴더 모두 보존 · "결과 전 멈춤" = 폴더에 팔 payload (p2_*.json) 없고 러너가 만든 멈춤 코드가 있을 때만 · 결과 줄에 폴더 요약 sha · 항목당 폴더 1 · 결과 줄 1 |
| P3 | §3-1 no-op 을 **기계 이름**에 묶었다 | D2 실측 = 한 기계에서 `OPENBLAS_CORETYPE` 만 바꿔 σ 상대차 1.3e-10–5.8e-10 · 기계 이름이 같아도 BLAS 경로가 다르면 정상 런이 SAME_P_CONSISTENCY 로 멈춤 · 사다리 요약 (`summary_base`) 에는 machine · code 만 | no-op 과 사다리 확인 팔의 환경 지문 (BLAS 경로 · backend · 라이브러리) 대조 · 사다리 요약에 환경 지문 기록 |
| P3 | D1 의 "같은 상태" 와 §3-4 · §3-5 사전 대조의 순서 | 단위 U2 모서리 = NOT_COMPUTED → 한 기계 사슬 결과 = NOT_COMPUTED · 런 4 · 그런데 뒤쪽 U9 가 결과 전 멈춤으로 최대 시도를 넘김 → 단위 대조를 다시 계산 **전에** 하면 원장 멈춤으로 바뀜 (fail-closed 지만 같음 주장이 깨짐) | 단위 대조를 다시 계산이 그 단위를 요청할 때 (lazy) · 또는 우선순위를 명시하고 §8 에 시험 |
| P3 | §5 "기계를 넘는 비교" 목록에 SID_GRID 없음 | `read_run` 의 `sid_reg` = 같은 래스터 · 같은 origin 런 사이 **정확히 같음** 대조 · 단위가 기계를 넘으면 이 대조도 기계를 넘음 | 목록에 SID_GRID · 기계 간 래스터 결정성 시험 (추정: CPU numpy 라 같을 것) |
| P3 | §3-2 "런 폴더 통째 복사" 의 이름 충돌 | 단위마다 Runner 번호가 R01 부터 → `R01_corner` 같은 폴더 · `logs/*.log` 가 단위끼리 겹침 · Replay 는 `self.dir / outdir` 로 찾음 | 단위 하위 폴더 · `runs[].outdir` 상대 경로 규칙 명시 |
| 질문 | §3-5 의 "칼날 판정 … 단조 띠" | C4 이후 단조 띠 = 증서 구간 → 정직한 런이면 기계와 무관하게 안 멈춤 · SV 판정은 DEPENDENT ↔ UNCHECKED 또는 clear ↔ UNCHECKED 로만 뒤집힘 · DEPENDENT ↔ clear 불가 (두 구간 모두 참값을 품음) | 칼날 목록을 "origin W0 · SV 걸침" 으로 줄인다 |
| 질문 | 첫 합치기와 C3 | corner a0 · origin a1 · a2 의 R 단조 위반은 첫 합치기에서 이미 셀 수 있다 · 같음을 지키면 넘침 (+87 h/모서리) 을 다 돈 뒤에야 멈춘다 | 의도라면 문서에 · 아니면 1저자가 정한다 |

## D. 탐침 파일 (리포 반입 = 이 폴더)

- 새 탐침 `tools/atk2_sv.py` (C1 X1–X7) · `tools/atk2_census.py` (X6) · `tools/atk2_rmono.py` (C3 · C4) · `tools/atk2_c5.py` (C5) · `tools/mut2.py` (변이 37 · C2 4 포함 · `$ATK_ROOT/new_src` · `$ATK_ROOT/tools_r1/run.py` 전제) · `tools/show.py` (출력 보기).
- 실행기 `r.sh` (`RINT_REVIEW_SOURCE=<트리>`) · `probes.sh` (판정문 탐침).
- 로그 `logs/` — `atk2_*.out` · `mut2.json` · `mut2_*.log` · `r2_*.out` · `r2_reg_each.json` · `r2_summary.txt` · `bitid_{old,new}.json` · `new_atk_sv.out` (1 회차 A2 = 이제 거부).

---

## 메인 메모 (10-23)

- **반입**: 에이전트 작업 폴더 1.9 MB 전부 · 작업 폴더 경로가 박힌 세 곳 (`tools/mut2.py` 한 줄 · `r.sh` · `probes.sh` 의 `W=`) 만 환경 변수 `ATK_ROOT` 로 바꿈 (README) · 로그 원자료 안의 scratchpad 경로는 원자료라 고치지 않음.
- **메인 재확인 (X6 · 리포 트리 `46abdde9e` = 코드 `a32fcf32f` 와 같음 · Linux · BLAS 스레드 1)** — `tools/atk2_census.py` → `logs/main_recheck_atk2_census.json`: 다섯 기록 모두 census 까지 고치면 계약 None · 판정 SV_UNCHECKED → `[]` (QD2-3 · RAIL5 · QD2-1 · QD4 t 1.2 · QDX t 2.0) · census 를 안 고치면 계약 거부 (기록 0 ≠ 증거 census) = 에이전트 보고와 같음.
- **처분** = 1저자 결정 (진행 기록 10-23 줄 · Codex 회차 ① 요청서의 사전 공격 리뷰 절 · 알려진 한정 절에 반영 예정).
