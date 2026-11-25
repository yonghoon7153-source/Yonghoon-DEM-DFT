---
title: "EB 회신 (내부 반박 리뷰) — li2s-3 판독 도구 · 카드 개정 DZ: NO-GO (P0 1 · P1 6 · P2 7) — 생산 프레임 수 기대값이 실제 드라이버보다 하나 많다 (4001 대 4000) · 접근 (v1 런 사후 검증) 은 조건부 찬성"
date: 2026-11-10
updated: 2026-11-10
tags: [review, li2s, li2s3, glass, uma, md, internal, reply, letter]
letter: EB
track: li2s
channel: internal
kind: reply
status: 수령 2026-11-10 — 원문 그대로 (에이전트 최종 보고 · 저장소 파일 안 고침 · 스텁 계산기로 실제 큐 · 러너 · 드라이버 재현)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = li2s (외부 1저자 · 위임 10-30 — 이 트랙의 결정은 내가 정하고 보고한다). 프롬프트 `codex_EB_prompt_li2s3_dz_fixes_2026_11_10.md` (Codex 토큰이 없어 내부 독립 리뷰 에이전트로 보냈다).
> 아래는 리뷰 에이전트의 최종 보고 **원문 그대로**다. 재현에 쓴 스크래치 파일은 세션 스크래치에만 있다 (저장소 밖).

# 내부 반박 리뷰 EB — li2s-3 판독 도구와 카드 개정 DZ

- **기준**: 도구 `tools/ionic/li2s3_stage2_readout.py` sha16 `8482ccad7225dbf4` · 큐 `run_stage2_kgy.sh` sha16 `d930f9b209d68097` · 커밋 `025eef73`.
  - 리뷰 중 HEAD 가 `c60c20a8` 로 올라갔지만, 리뷰 대상 파일 (도구 · 큐 · 카드) 은 바뀌지 않았다.
- **한 것**: 저장소 파일은 하나도 안 고쳤다 (`git status` 깨끗). GPU · 원격 기계 · 실제 2 단계 결과는 안 썼다.
- **재현 방법**: 실제 v1 큐 → 실제 v2 러너 → 실제 MD 드라이버 를 이 컨테이너에서 그대로 돌렸다.
  - fairchem 만 스텁 계산기로 바꿨다: P · S · Cl 은 조화 구속, Li 는 힘 없음.
  - 합성 120 원자 입력 (A · B × 11 · 12) 은 저장소의 `build_random_cell` 로 만들었다. A11 · B12 에는 실제와 같은 꼴의 결함 (3 배위 P 하나 + S–S 2.10 Å) 을 넣었다.
  - 스텁 런이라 물리값은 의미가 없고, 아래에도 싣지 않는다.

---

## 1. 판정

### NO-GO — 지금 판본으로 16 런을 읽으면 안 된다

이유 하나로 충분하다 (P0-1):
- 실제 드라이버가 쓰는 생산 프레임 수는 `prod/save` 다 (400 ps → 4000).
- 도구는 `prod/save + 1` (4001) 을 요구한다.
- 그래서 올바른 v1 런이 **전부 invalid** 가 되고, `readout` 은 **`W = [] · 닫는다 (S2 허용 문구 + 구조군 문구) · cond550 자격 False`** 를 낸다.
- 이것을 실제 큐 · 러너 · 드라이버로 만든 올바른 8 런에서 재현했다.
- selftest 36/36 이 초록인 이유: 양성 픽스처가 같은 잘못된 가정 (+1) 으로 만들어졌다. 올바르게 고치면 selftest 가 빨개진다.

그 밖에 P1 이 여섯이다: 실행된 코드 · 실제 추론 모드 · 궤적 ↔ 입력 결속 · 검증 실패의 처리 · 허가 문 우회 · 압력 계산기.

### 접근 자체는 조건부 찬성

v1 런을 다시 돌리지 않고 사후 검증으로 한 번 읽는 방식은 선다.
- 입력 구조와 run_meta 인수는 사후 증거가 실행 직전 재해시만큼, 또는 그보다 직접 결속한다.
- 실행된 코드와 추론 모드는 kgy 에 이미 있는 실행 시점 로그를 읽으면 결속된다.
- 16 런 재실행 (3–4 일) 은 필요 없다.

### GO 로 바뀌는 최소 조건

1. P0-1 을 고친다. selftest 양성 픽스처는 실제 드라이버 `run_md` 출력 (싼 계산기) 으로 만든다.
2. P1-1 ~ P1-3 을 verify 에 넣는다.
3. P1-4: 검증 실패는 판정 보류로 처리한다 (W 밖이 아니다).
4. P1-5 · P1-6 을 고친다.
5. kgy 에서 이미 끝난 v1 런에 `verify` 를 돌린다 (허가 전에 허용된다 · 수송을 안 읽는다). 대조 잡 `same = True` 도 받는다. 둘 다 같은 도구 sha16 이어야 한다. 그 다음에 판독 허가를 커밋한다.

### 범위 질문 (큐 v2 를 '추가 런 전' 으로 미루기)

**조건부 예.** 조건은 Q6 에 적었다.

---

## 2. P0 / P1 / P2

### P0-1 — 생산 프레임 수 기대값이 실제 드라이버와 한 개 어긋난다

**위치** (`li2s3_stage2_readout.py`)
- check_trajectory: `:123` (`n_exp = …/SAVE_FS)) + 1`) · `:131-132` · `:164-166`
- run_pressure: `:391-393` · `:404-406`
- selftest 픽스처: `:573` · `:584`

**원인**
- 드라이버 `disorder_ensemble_diffusion.py` 의 순서: `:277` 평형 `md.run` → `:299` `_snap` 붙임 → `:302` 생산 `md.run`.
- ASE `Dynamics.irun` 은 `nsteps == 0` 일 때만 시작 관측을 부른다 (설치본 `ase/optimize/optimize.py` 에서 확인).
- 그래서 첫 저장은 평형 끝 + 0.1 ps 이고, 프레임 수 = prod/save 다. `aimd_results.n_frames` 도 `len(frames)` 다 (`:314-316`).
- 저장소도 이미 이 사실을 안다:
  - `glass_v2_readout.py:465-466` — "400 ps 가 4000 프레임 (0–399.9 ps)"
  - 10-14 판독 기록 `readout_control.json` 의 p90² `n_frames 4000` (같은 드라이버 `c3e2d358ee53cefa`)
- 편지 EB §2 표의 "프레임 수 = prod/save + 1" 도 같은 오류다.

**재현**
1. 실제 `run_md` (LJ 계산기) 2 ps → `n_frames 20`. 도구 기대값은 21.
2. 실제 v1 큐 · 러너 · 드라이버, 3 ps 4 런 → 넷 다 `invalid — aimd_results n_frames 30 ≠ 계획 31`.
3. 120 ps 8 런 (600 · 650 K) + 허가 있는 시험 카드 → 지금 도구 `readout` 결과:
   - `W = [] · 닫는다 · cond550 False`
   - 제외 사유는 전부 `사후 검증 invalid`
4. `+1` 만 지운 사본:
   - 8 런 모두 valid · `W [600, 650]`
   - 그러나 그 사본에서 selftest 가 빨갛다. 양성 "사후 검증 ①–⑦ 통과" 가 실패하고, 이어서 크래시한다.

**최소 고침**
- `n_exp = round(prod/save)`.
- 시각 규약: 프레임 k ↔ t = (k+1)·save.
- 압력 프레임은 k = 10j − 1 (j = 1…400).
- selftest 양성 픽스처를 실제 `run_md` 로 만든다. +1 꼴은 음성 픽스처로 남긴다.

---

### P1-1 — 실행된 드라이버 · 러너가 결속되지 않는다

⑦ 은 판독 시점 worktree 의 파일을 해시할 뿐이다.

**위치**
- 도구: `:254-260` (⑦) · `:87-94` (끝 줄 하나만 읽음)
- 큐 `run_stage2_kgy.sh`:
  - `:40-44` — `RUNNER · RUNNER_SHA16 · PY · DRV · DRV_SHA16` 를 환경변수로 받는다.
  - `:96-97` — 러너 지문은 큐 시작 때 한 번만 본다.
- 러너 `glass_kgy_q_v2.sh`: `:219-220` 드라이버 지문 → `:237-239` GPU 대기 → `:243` 실행.

**재현** (실제 v1 큐로)
- (a) `RUNNER` = friction 0.5 로 바꾼 러너 사본 + 그 sha16 → 큐 exit 0 · verify **valid**.
- (b) `DRV` = 열욕을 1.5 T 로 바꾼 드라이버 사본 + 그 sha16 → 큐 exit 0 · verify **valid**.
  - md.log 생산 평균 T 는 892.7 K (설정 600 K) 였다.
- 두 경우 흔적은 로그에만 있다:
  - 큐 로그: `문지기 ✓ … 러너 sha16 6be496dc715551d7`
  - 러너 로그: `드라이버 sha16 7cbd8c3701892dc6 ✅`
- verify 는 이 줄들을 읽지 않는다.
- 런로그 기준으로 kgy 큐 로그의 머리 줄 (`문지기 ✓` · `판 —`) 은 아직 회수되지 않았다.

**최소 고침**
- 러너 로그 `$BASE/<계>/queue_kgy.log` 에서 그 런의 호출 블록을 **정확히 하나** 찾는다 (`▶ v2 큐 시작 · T:S:400` ~ `■ 큐 끝 · T:S:400`). 그 블록 안에 다음이 모두 있어야 한다:
  - `드라이버 sha16 c3e2d358ee53cefa ✅`
  - `OK run_meta = 본 런 설정 (… prod 400 · seed 30SS)`
  - `dt = 기준과 같다 (0.0020 ps/행)`
  - `▶ T<T> seed<S> PID … · prod 400 ps · --seed 30SS`
  - `✅ T<T> seed<S> 끝 (rc 0)`
- 큐 로그 `$BASE/stage2_kgy.log` 에서 다음을 요구하고 기록한다:
  - 시작 줄: PHASE ladder · 온도 600 650 700 750 · 시드 11 12 · 계 A B · prod 400
  - `문지기 ✓ … 러너 sha16 3aef029aced0de77`
  - `판 —` 줄 (패키지 판 · repo HEAD)
  - `■ 큐 끝 · PHASE ladder`
- ⑦ 은 보조 검사로 남긴다.

---

### P1-2 — 실제 추론 모드를 안 본다

**위치**
- 도구 `:210-213` — `uma_inference_mode_requested` 만 본다.
- 드라이버 `:535-540` — run_meta 의 `uma_inference_mode` 가 실제 모드다.
- 드라이버 `:616-631` — `ensemble_results.json` 에 `uma_inference_mode` · `uma_task` 가 있다.

**재현**
- turbo 요청이 실패하는 스텁으로 실제 v1 큐를 돌렸다.
- 드라이버가 기본 모드로 내려갔다 (`run_meta.uma_inference_mode = default`).
- 큐 exit 0 · verify **valid**.
- 드라이버 주석 `:519` 는 "한 캠페인의 모든 런이 같은 모드여야 한다" 인데, 판독이 이것을 확인하지 않는다.
- 압력 도구는 turbo 를 요구하면서 MD 쪽 모드는 안 본다.

**최소 고침**
- `run_meta.uma_inference_mode == "turbo"`.
- `ensemble_results.uma_inference_mode == "turbo"` · `uma_task == "omat"`.
- `ensemble_results` 의 temperatures · prod_ps · n_atoms = 카드 값.

---

### P1-3 — 카드 ③ 의 궤적 ↔ 입력 결속이 구현되지 않았다

**위치**
- 카드 `사후_검증_v1_런.③` 원문: "생산 궤적 첫 프레임과 입력: 셀 같음 · 원자 수 · 원소 순서 · P 와 S 최소상 변위 중앙값 < 1.0 Å".
- 도구 `:226-239` 는 config.xyz ↔ init 만 본다.
- `:153-157` 은 셀을 그 궤적 자기 첫 프레임과만 비교한다.

**재현**
- 실제 체인 런에서 A12 의 traj.xyz · msd.json · aimd_results.json · md.log 를 A11 폴더 (같은 경로) 에 넣었다 → verify **valid**.
- 카드 ③ 식으로 재면 P/S 변위 중앙값이 7.28 Å 다 (문턱 < 1.0).
- 같은 계 · 같은 밀도라 셀과 원소 순서로는 갈리지 않는다.

**최소 고침**
- 생산 첫 프레임 셀 = config.xyz 셀 (1e-6 Å).
- P/S 최소상 변위 중앙값 < 1.0 Å (카드 값).
- 아니면 invalid.

---

### P1-4 — 검증 실패가 물리 판정 (W 밖 · 닫는다) 으로 넘어간다

'끝나지 않음' 의 정의도 좁다.

**위치**
- `:339-341` — incomplete 만 거부한다.
- `:354-355` — invalid → `measurable False`.
- `:357-361` — |W| = 0 → '닫는다'.
- `:193-202` — msd.json 이 있으면 '끝 줄 없음' · 'ensemble 없음' 은 incomplete 가 아니라 invalid 로 간다.

**재현**
- (a) P0 가 그대로면 올바른 8 런이 전부 invalid → '닫는다'.
- (b) 마지막 런이 msd.json 을 쓰고 아직 안 끝난 상태 (러너 끝 줄 · ensemble_results.json 없음):
  - verify 는 invalid.
  - readout 은 그대로 진행해 `W [600]` 을 냈다. 650 K 가 `사후 검증 invalid` 로 W 밖에 나갔다.
  - 드라이버가 msd.json 을 쓴 뒤 정리 단계에서 멈추면 이 창이 길어진다.

**최소 고침**
- invalid · incomplete 가 하나라도 있으면 W · 갈래 · cond550 을 내지 않고 종료한다 (판정 보류).
- 러너 끝 줄이 없으면 incomplete 로 센다.
- 큐 끝 줄 (`■ 큐 끝 · PHASE ladder`) 과 큐 잠금 해제를 판독의 전제로 둔다.
- 보류된 런의 처리 (v2 로 같은 카드 값 재실행) 를 결과 전에 카드에 박는다. 이것은 개정 DZ 의 "그 온도는 W 밖" 을 바꾸는 것이다.

---

### P1-5 — 판독 허가 문의 우회 (control · pressure)

**위치**
- control `:449-493` — 카드 · 결정 · 허가를 읽지 않는다. 루트 · 시드 제한도 없다.
- pressure `:414-437` — 미완 런 거부가 없다.

**재현**
- (a) 허가 없는 카드 상태에서 `control(root_a=$BASE/A, root_b=$BASE/B, seeds=(11, 12))`:
  - 2 단계 600 K 네 런의 C1 · C1 값 · β_MTO · C2 판정을 출력했다.
  - 지금은 P0 가 check_trajectory 에서 우연히 막고 있다. P0 를 고치면 바로 열린다.
- (b) 허가가 있는 상태에서 B12 650 K 의 msd.json 을 치우고 pressure 를 돌렸다 → 나머지 일곱 런의 압력을 냈다. 거부하지 않았다.

**최소 고침**
- control 은 10-14 기록에 있는 시드만 받는다. 루트의 run_meta 라벨이 10-14 대조 계 라벨인지 확인하고, 아니면 거부한다.
- pressure 에 readout 과 같은 조건을 건다: 16 런 모두 끝 · 모두 valid.

---

### P1-6 — 압력: turbo 계산기 하나를 두 조성에 쓴다

P0 를 고친 뒤에도 프레임 하나 어긋남이 남는다.

**위치**
- `:424-427` — 계산기를 하나만 만든다.
- `:429-437` — 그 계산기로 A → B 를 순회한다.
- `:391-393` · `:404` — 프레임 선택과 시각 라벨.

**근거**
- turbo 는 `merge_mole` 을 켠다.
- 저장소 기록 두 곳이 `merge_mole` 의 '조성 캐시 단언' 을 적어 두었다:
  - `kb/methodology/li_adatom_neb_protocol.md:46`
  - `kb/projects/sdcp_linio2_binding.md:58`
- `melt_quench_uma.make_calc` 주석도 "원자 수·조성이 고정된 MD 전용" 이다.

**재현**
- 조성 고정 규칙을 흉내 낸 스텁으로 `pressure()` 를 돌렸다:
  - A 런을 다 계산한 뒤 첫 B 단일점에서 AssertionError 가 났다.
  - 출력 파일은 끝에 한 번만 쓰므로 아무것도 남지 않았다.
- 실제 fairchem 이 단언하지 않는다면 더 나쁘다: B 응력이 A 조성에 병합된 모델 값이 되고, 아무 경고도 없다.
- `+1` 만 지운 사본의 3 ps 런:
  - 프레임 2 개를 골랐다. 라벨은 1.0 · 2.0 ps, 실제 시각은 1.1 · 2.1 ps 다.
  - 카드 의도는 3 개 (t = 1 · 2 · 3 ps) 다.
  - 400 ps 런이면 399 개가 된다.

**최소 고침**
- 계마다 (또는 런마다) 새 계산기를 만든다.
- 런마다 점진 저장한다.
- 프레임 k = 10j − 1 을 고른다.
- kgy 에서 1 분 탐침으로 실제 동작을 확인한다: A 프레임 하나 → 같은 계산기로 B 프레임 하나.

---

### P2-1 — `v0_xyz` 절대경로 일치

- **위치**: `:220-225`.
- **문제**: BASE 를 옮기거나 사본에서 읽으면 전부 invalid 가 된다.
- **재현**: 사본 폴더 두 곳에서 `run_meta v0_xyz … ≠ init 사본`.
- **고침**: BASE 기준 상대 비교 · 원래 BASE 를 기록.

### P2-2 — 러너 끝 줄을 로그 전체의 마지막 일치로 읽는다

- **위치**: `:87-94`.
- **문제**: 앞선 호출의 `rc 0` 줄이 남아 있고 이번 호출의 끝 줄이 없어도 valid 가 된다.
- **재현**: 그렇게 만든 로그에서 valid.
- **고침**: P1-1 의 블록 짝짓기로 해결된다.

### P2-3 — 궤적 · 기록 유효성의 빈칸

**재현된 빈칸**
- 프레임 연속성을 안 본다:
  - Li 두 개의 index 를 15 번째 프레임부터 바꿨다 → 0.1 ps 에 14 Å 점프 → valid.
- md.log 는 첫 두 행 간격과 마지막 시각만 본다:
  - 행 수 · 단조 증가 · 머리줄 하나 · 생산 평균 T 를 안 본다.
  - 그래서 1.5 T 드라이버의 893 K 가 통과했다.
- ⑤ 는 `times_ps` · `msd_Li_A2` 만 보고, `read_run` 이 쓰는 `*_mto` 배열은 안 본다:
  - MTO[0] = NaN → valid → read_run 의 C1 = NaN → 'C1 미통과' 로 조용히 넘어간다.
  - MTO 배열을 5 점으로 자르면 → valid → '판독 오류' → W 밖.

**고침** (결과 전에 고정)
- 원소별 프레임 간 최대 변위 상한. 예: P · S · Cl 2.5 Å · Li 4 Å / 0.1 ps.
- md.log 행 수 = (eq+prod)/dt + 1 · 단조 · 생산 평균 T ± 2 %.
- MTO 배열 유한 · 단조 · 길이 확인.

### P2-4 — 기록 · 기술표 · 세 층

- ⓑ 가 P 별이 아니라 전체 합이다 (`:290-296`). 카드는 "P 마다" 다.
- 기술표 결함 표지에 S–S 가 빠졌다 (`:68-69`). 카드 표지는 "3 배위 P + S–S" 다.
- 기술표에 ⓐ–ⓒ 요약과 골격 기준별 판정이 없다.
- '골격 이동' 과 '골격 못 잼' 이 한 사유로 합쳐진다.
- 세 층 수는 카드 시드 수를 복사한 것이지 계산한 것이 아니다. 계별 제외 수 · 사유 표도 없다.
- ⓐ 는 컷이 하나 (2.30 Å) 라, 컷 근처 쌍의 깜빡임을 끊김 · 재형성으로 센다.
  - 합성 2.22 Å 쌍에서 끊김 5 · 재형성 5.
  - 쌍별 거리 최소 · 중앙 · 최대를 같이 싣는다.

### P2-5 — 출력에 출처 기록이 없다

- readout · pressure · control 출력에 도구 sha16 · git HEAD · 작업 트리 깨끗함 · BASE · 시각이 없다. `card_sha256` 만 있다.
- '한 번만 읽는다' 는 `--out` 이름만 막는다 (`:821-822`).

### P2-6 — selftest 가 못 잡는 변이 둘

- `measurable` 에서 골격 게이트를 빼도 (`in_R_set` → `counts_in_N`) 36/36 이다.
- cond550 의 `all` → `any` 도 36/36 이다. 런로그의 "깨기 … cond550 any 빨강" 은 이 selftest 로 재현되지 않는다.
- 양성 픽스처가 실제 생산자의 출력이 아니다 (P0 의 원인).
- 참고로 W 의 `all` → `any` 는 잡혔다 (34/36).

### P2-7 — 카드에 적힌 것과 다르거나 도구가 따로 박은 값

- ⑥ 의 "장부가 없으면 로그 · 파일 시각으로 재구성" 이 구현되지 않았다.
- ⑦ 의 큐 파일 sha256 기록이 없다.
- n_atoms 120 (`:67`) · `SAVE_FS` · `DT_FS` (`:50`) 를 카드가 아니라 도구가 박았다.
- cond550 이 남아 있는데 갈래를 확정처럼 찍는다. "잠정 — cond550 판독 전" 이어야 한다.

---

### 확인한 것 (맞게 돈다)

- selftest 36/36 재현 (11.6 s).
- config.xyz ↔ init: 드라이버가 실제로 읽은 구조를 본다. DZ P1-5 반례 (대기 중 0.5 Å) 를 바꾼 채로도, 되돌린 뒤에도 잡는다. 실행 직전 재해시보다 직접적이다.
- run_meta 대조: DZ P1-4 의 T · prod · seed 반례를 사후에 잡는다.
- 러너 로그 rc: 실제 체인에서 우연히 생긴 DZ P1-1 꼴 런 넷을 invalid 로 잡았다.
  - 상황: 드라이버 rc 1 인데 큐 exit 0 · 장부 rc 0.
  - 원인: 2 ps 런에서 D 가 None 이라 출력 줄이 터졌다.
- 궤적 유효성: DZ P1-6 반례 (NaN · 원소 바뀜 · 1 프레임) · 깨진 msd.json 을 잡는다. 비용 미확정은 None 이다.
- 기록 ⓐ 가 DZ P2-1 반례를 잡는다.
- 실제 체인의 결함 구조에서 ⓒ 가 입력 P 배위 {3: 1, 4: 11} · S–S 1 쌍 유지를 맞게 낸다.
- readout 출력에 D 가 없다. 결정 · 허가 · 미완 (msd.json 없음) 거부가 돈다.

---

## 3. Q1–Q7

### Q1 — 사후 결속의 충분성: 부분적으로 충분

**충분한 것**
- 입력 구조. config.xyz 는 드라이버가 읽은 구조 그 자체다.
- run_meta 에 적힌 인수.

**지금 판본에서 불충분한 것**
- 실행된 코드 · 실제 모드 · run_meta 밖 인수 (friction · task) — P1-1 · P1-2.
- 이것들은 kgy 의 실행 시점 로그와 `ensemble_results` 로 사후에 닫힌다.

**남는 잔여 위험** (기록으로 남긴다)
- 러너의 지문 검사와 실행 사이 (GPU 대기 최대 3600 s) 에 파일이 바뀌었다가 되돌아간 경우.
- 큐 도중의 러너 파일 교체 (큐는 시작 때 한 번만 본다).
- 패키지 판 변경.

**결론**: 16 런을 v2 로 다시 돌릴 필요는 없다.

### Q2 — 궤적 유효성 ④

- 프레임 수 P0 와 P1-3 · P2-3 이 빠진 검사다.
- 저장 간격은 프레임에 시각이 없어서 직접 확인할 수 없다.
- 대신 넷이 서로 맞는지로 본다: `aimd_results.save_fs` · 프레임 수 · md.log 행 수 · 끝 시각. 지금은 이 중 프레임 수 식이 틀렸다.

### Q3 — ⓐ–ⓒ 기록만

**선택은 선다.** 구조를 본 뒤라 새 문턱을 만들지 않는 것이 맞다.

**단, 결함 시드에서 생산 첫 프레임 대비 게이트는 비대칭이다**
- 결함 P 의 3→4 '치유' 는 ① 으로, 새 S 짝이 생기면 ③ 으로 탈락시킨다.
- 기존 S–S 쌍의 해체는 소속 이동이 없으면 보지 못한다.
- 따라서 W · R 은 결함이 생산 중 안 바뀐 시드에 조건부다. 결함 안정성과 상관된 선택이다.

**결과 전에 할 것**
- 이 비대칭을 문장으로 박는다 (아래 4 절).
- 기술표에 ⓐ–ⓒ 를 싣는다.
- ⓑ 를 P 별로 바꾼다.

### Q4 — 판독 허가 문: 조용한 경로가 있다

**경로**
- P1-5: control · pressure 우회.
- P1-4 (b): 아직 안 끝난 런이 invalid 로 분류돼 판독이 진행된다.
- 허가 키는 '근거' · 'by' 에 빈 문자열만 아니면 된다. 작업 트리에 커밋 안 된 수정이 있어도 통과한다.
- 출력에 도구 sha16 · HEAD 가 없어서 다음 순서를 증명할 수 없다: 도구 커밋 → 대조 잡 통과 → 허가 커밋 → 판독.

**고침**
- 허가 키에 EB 회신 경로와 대조 잡 출력 경로 · sha256 를 넣는다. 그 출력이 `same = True` 이고 도구 sha16 이 같아야 한다.
- 출력에 도구 sha16 · HEAD 를 싣고, 작업 트리가 더러우면 거부한다.
- 판독 출력 경로를 하나로 고정하고, 이미 있으면 거부한다.

### Q5 — 압력

**맞는 것**: 식이 li2s-2 카드 §2 와 같다.
- P_vir = −tr σ/3 (turbo 단일점) + N k_B T_set / V.
- 1 ps 간격 · 런 평균 · 표준편차.

**틀린 것**
- P0 — 실제 궤적에서 SystemExit.
- P0 뒤에도 남는 프레임 하나 어긋남.
- 조성이 다른 두 계에 계산기 하나 (P1-6).
- 미완 거부 없음 (P1-5).
- MD 의 실제 모드 미확인 (P1-2).

**더 남길 것**
- 런별 V · P_kin.
- 블록 평균 표준오차. 1 ps 표본은 서로 상관되어 있어 sd 만으로는 평균의 불확실성이 아니다.
- 실측 비용 (카드: "첫 런에서 실측").
- fairchem · torch 판과 실제 모드.
- 운동 항 규약: fixcm 이라 자유도는 3N−3 이다. N 과 N−1 의 차이는 운동 항의 0.8 % (≈ 0.004 GPa) 로 무시할 수 있다. 규약만 적어 둔다.

### Q6 — 큐 v2 미루기: 조건부 예

조건:
1. P0 · P1 고침 뒤, v1 런이 kgy 로그 기준으로 검증된다.
2. v1 큐가 16 런 전에 멈추면 판독하지 않는다. 다음을 지금 박는다:
   - 남은 런만 v2 로 돌릴지, 16 런 전부를 v2 로 다시 돌릴지.
   - v1 · v2 런을 한 판독에 넣을 때의 검증 대응표.
   - v2 는 자기 런 폴더에 실행 기록을 남겨서 같은 verify 가 v1 · v2 둘 다 읽게 한다.
3. 검증 실패 런은 판정 보류 → v2 재실행. 그래서 v2 가 그 시점에 필요하다.
4. cond550 은 v2 로만 돈다. 판독 결과를 보고 v2 를 고치지 않도록 v2 리뷰를 16 런 판독 전에 끝낸다.

### Q7 — 대조 잡 합격 기준

**정확 일치 (β 1e-9)**: 맞다. 결정적 계산이다.

**네 행 (kgy 시드 1 · 3 × 두 계) 으로 충분한가**
- read_run · skeleton_gate 회귀 확인으로는 충분하다.
- 그러나 덮는 갈래가 좁다: C2 통과 · 경계, 골격 통과 (① 0–0.006 · ④ 0–1) 뿐이다.
- 안 덮는 것: 골격 탈락 · C1 탈락 · 첫 프레임 결함 (li2s-3 결함 시드의 핵심 경로).
- verify ①②③⑤⑥⑦ · 기록 · W · pressure 는 하나도 안 거친다.
- 계획된 대조 잡은 지금 판본에서 `same = False` 와 '궤적 유효성 실패 … 검사 결함 의심' 4 건을 낼 것이다. 이것은 P0 가 드러나는 것이지 옛 런의 문제가 아니다.
- σ 열만 어긋나면 numpy · 난수 판 차이일 수 있다. 해석을 미리 정해 둔다.

**더할 것**
- (a) 실제 드라이버 `run_md` (싼 계산기) · 실제 러너 · 실제 v1 큐로 만든 런 폴더를 쓰는 통합 시험. 내 재현은 4 런에 30 초였다.
- (b) kgy 에서 지금 끝난 v1 런에 `verify`. 허가 전에 허용되고, 수송을 안 읽는다.
- (c) 대조 잡 결과를 허가 조건으로 묶는다 (도구 sha16 결속).
- (d) control 이 받는 시드 · 루트를 제한한다.
- (e) selftest 에 음성 두 개를 더한다: '골격 탈락 → 측정 가능 아님' · '600 K 에서 한 계만 측정 가능 → cond550 없음'.

---

## 4. 카드에 넣을 문장

1. **사후 검증의 범위**: "v1 큐로 돈 런의 사후 검증은 입력 구조 (드라이버가 쓴 config.xyz = init 사본 = 카드 sha256) 와 run_meta 에 적힌 인수를 결속한다. 실행된 드라이버 · 러너 · 추론 모드와 run_meta 밖 인수 (friction · task) 는 실행 시점 기록 — 큐 로그의 '문지기 ✓ … 러너 sha16' · '판 —' 줄, 러너 로그의 그 런 블록 ('드라이버 sha16' · 'run_meta = 본 런 설정' · 'dt = 기준과 같다' · 끝 줄 rc), run_meta · ensemble_results.json 의 uma_inference_mode · uma_task — 로만 결속한다. 러너의 지문 검사와 드라이버 실행 사이 (GPU 대기) 에 파일이 바뀌었다가 되돌아간 경우는 보지 못한다 (잔여 위험)."

2. **검증 실패의 처리**: "사후 검증 invalid · incomplete 런이 하나라도 있으면 2 단계 판정 (W · 갈래 · cond550 자격) 을 내지 않는다 (판정 보류). 검증 실패는 수송 게이트 미통과가 아니다 — 그 온도를 W 밖으로 세지 않고, 그 런은 고친 큐 v2 로 같은 카드 값으로 다시 돌린다 (그 밖은 사용자 결정)."

3. **판독 순서**: "판독 (readout · pressure) 은 ① 고친 판독 도구 커밋 ② 실제 드라이버 출력으로 만든 통합 시험과 대조 잡 (same = True) 을 같은 도구 sha16 으로 통과 ③ 판독 허가 커밋 (EB 회신 파일 · 대조 잡 출력 경로와 sha256) 순서로만 하고, 16 런의 러너 끝 줄과 큐 끝 줄이 모두 있을 때 한 번 한다. 출력에는 도구 sha16 · git HEAD · 작업 트리 깨끗함을 남긴다."

4. **결함 시드**: "생산 첫 프레임 대비 골격 게이트는 결함 시드 (A11 · B12) 에서 결함의 변화 (결함 P 의 3→4 · 새 S 짝) 는 탈락으로 세고 기존 S–S 쌍의 해체는 보지 못한다. 그래서 W · R 은 생산 중 결함 P 의 배위가 바뀌지 않은 시드에 조건부다 — 결함 보존 · 결함 안정성 · 결함이 수송에 미치는 영향을 주장하지 않는다. 시드별 기술표에 기록 ⓐ (입력 S–S 쌍의 유지 분율 · 마지막 유지) · ⓑ (P 별 전이) · ⓒ 를 같이 싣는다."

5. **압력**: "MD 압력은 생산 프레임 k (t = (k+1)·0.1 ps) 중 t = 1, 2, …, 400 ps 의 400 개에서 낸다. 계마다 새 UMA turbo 계산기를 만들고 (조성이 바뀌면 같은 계산기를 쓰지 않는다), MD 의 실제 추론 모드가 turbo 인 런만 쓴다. 판정에 안 쓴다."

6. **범위**: "v1 큐가 16 런 전에 멈추면 판독하지 않는다. 남은 런은 리뷰를 통과한 큐 v2 로 같은 카드 값으로 돌리고, v1 · v2 런을 한 판독에 넣는 검증 대응표를 결과 전에 박는다. cond550 은 v2 로만 돌리며 v2 리뷰는 16 런 판독 전에 끝낸다."

---

## 5. 재현에 쓴 스크래치 파일

뿌리: `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/`

**로그 · 탐침**
- `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/selftest_main.log` — 36/36 재현
- `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/probe_driver_frames.py` — 실제 run_md 프레임 수

**재현 도구**
- `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/fakefc/` — fairchem 스텁
  - `FAKE_NO_TURBO` = turbo 요청 실패
  - `FAKE_STRICT_TURBO` = 조성 고정 규칙
- `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/bin/nvidia-smi` — 가짜 GPU 조회
- `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/make_inputs.py`
- `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/harness.py`
- `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/make_card.py`
- `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/probe_pressure.py`
- `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/probe_readout.py` (+ 출력 `probe_readout.log`)
- `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/probe_validity.py`

**실제 체인 런 트리**
- `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/e2e/base3` — 4 런 × 3 ps
- `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/e2e/base120` — 8 런 × 120 ps
- `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/e2e/base_rc1` — 드라이버 rc 1 · 큐 exit 0
- `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/e2e/baseNT` — turbo 꺼짐
- `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/e2e/baseALTR` — 다른 러너
- `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/e2e/baseALTD` — 다른 드라이버
- `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/alt/` — 바꾼 러너 · 드라이버 사본

**사본**
- `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/repo_copy` — `+1` 을 지운 사본 (`REVIEW-PATCH` 줄 123 · 392)
- `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EB/repo_mut` — 변이 시험용

### 하지 않은 것 · 못 본 것

- 실제 fairchem · GPU 는 쓰지 않았다. merge_mole 의 조성 단언은 스텁과 저장소 기록 두 곳으로만 근거를 댔다.
- kgy 의 실제 로그 · 런은 보지 않았다.
- 10-14 판독 시점의 numpy 판은 확인하지 않았다.
