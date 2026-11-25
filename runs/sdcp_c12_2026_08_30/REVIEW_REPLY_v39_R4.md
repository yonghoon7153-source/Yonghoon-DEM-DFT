# v39 재검토 회신 (4차) — P1 1건 · P2 2건 처리 · v40 재생성 (2026-09-08)

받은 판정 그대로 받습니다: **생산 실행 NO-GO · 큐 문의는 문구 보완 후 GO.**
P1-1(잠금) · P1-2 wrapper · P1-3(4.46) · P2(mem=0) 해제 확인. 시간 P0-2 는 다시 열지 않습니다.

**v40** 을 clean tree 에서 재생성했습니다.

```
커밋      e992da738da0b7b9d1e9abe1cf792714cdb372b4   (origin 도달 · provenance.clean=true)
ZIP       9621a438919a0e32083feb8a32587633e426ba52e2196b37399bdd2b19ff92b0
MANIFEST  a3121ba7517564216fef6b43758ee79369a35ac5d68a5a24f4eb8747adcac1bc
생성기    tools/sdcp/vasp_handoff_bundle.py @ 그 커밋 sha 684caa44378c1e94… (IDENTITY_v40 에 전체)
```

**v39 대비 POSCAR/INCAR/KPOINTS 57파일 바이트 동일.** 바뀐 것은 러너(프로브·판정기)·추정기 CLI·문서·문의문입니다.

---

## P1 — 미관측 제한을 물리 RAM 으로 대체하던 경로, 폐기 ✅

지적이 맞았습니다. 회신 3차 63–64행의 *"제한을 `none` 으로 받으면 멈춘다"* 는 **코드와 달랐습니다** —
프로브가 커널의 `max`(무제한)와 읽기 실패를 둘 다 `none` 으로 냈고, 판정기는 `none` 을 None 으로 읽은
뒤 MemTotal 만 남겨 통과시켰습니다. 문서가 코드보다 앞서 말한 것이라 그 문장은 철회하고, 이번에 코드를
문장에 맞췄습니다.

### 프로브 (`_probe_node.sh`) — 세 상태를 스크립트가 직접 가른다
출력 5필드 `host · 제한(bytes|max|none) · MemTotal · 상태 · 근거`.

| 상태 | 뜻 | 근거 필드 |
|---|---|---|
| `finite` | 계층(리프→루트) 어디서든 **유한값을 읽었다** → 최소값 | 그 파일 경로 (`…/job_N/memory.max`) |
| `unlimited` | 제한 파일을 **실제로 읽었고** 전부 `max`(v2)/무제한 센티널(v1) — 또는 `cgroup.controllers` 에 memory 가 보이는 v2 루트(루트엔 memory.max 가 없다는 커널 규약) | `all-readable-levels-max:<읽은 계층 수>` · `root-cgroup-v2(…)` |
| `unobserved` | /proc/self/cgroup 없음 · memory 계층 줄 없음 · 경로가 이 마운트에 없음 · 루트인데 memory 컨트롤러가 안 보임(namespace 밖 제한을 못 봄) · 어느 파일도 못 읽음 | `cgroup-path-not-mounted:<경로>` 등 |

- 우선순위: 유한 > 읽은 계층이 전부 max > 경로 미마운트 > memory 계층 없음 > 루트(컨트롤러 보임) > 미관측.
  hybrid(v1 memory + `0::/`) 에서 v2 루트 검사가 헛돌아도 **v1 을 읽었으면 그것이 판정**입니다.
- `none` 은 이제 **"못 읽었다"만** 뜻합니다. `max` 와 합치지 않습니다.
- MemTotal 은 awk 로 **필드만** 뽑고 곱셈은 셸 64비트 산술로 합니다 — §4 의 awk 지수표기 → `int()` 탈락 위험을
  없앴습니다 (스텁도 같은 방식).

### 판정기 (PYPROBE)
- `unobserved` → **정지.** 사유별로 접어 기록합니다 (96 노드가 같은 사유면 한 줄).
  구판 3필드 `none` 출력도 unobserved 로 읽습니다 — v39 까지는 이 경로가 통과였습니다.
- `finite` → 상한 = min(제한, MemTotal).
- `unlimited` → 상한 = min(**스케줄러 할당**, MemTotal). 할당은 러너 호스트의 SLURM_MEM_PER_NODE /
  MEM_PER_CPU×CPUS 관측을 `MEMG_SCHED_GB` 로 넘긴 값이고, 미관측이면 근거에 *"스케줄러 할당 미관측"* 을 적고
  MemTotal 만 씁니다 (물리 RAM 이 실제 상한인 경우).
- `PLACEMENT_PROBE.json` 에 노드별 `state · limit_GiB · memtotal_GiB · bound_GiB · basis`, 프로브별 `limit_states`,
  전체 `limit_state_rule` · `scheduler_alloc_GiB_runner` 를 남깁니다. 성공 메시지에도 상태 분포가 찍힙니다.

### 회귀시험 — 요구하신 "유한 · 명시적 무제한 · 읽기 실패" 구분
- **프로브 스크립트 픽스처 12종** (생산 스크립트에 시험용 훅을 두지 않고, `/proc/self/cgroup` · `/sys/fs/cgroup` ·
  `/proc/meminfo` 를 임시 트리로 치환한 **사본**을 `/bin/sh` 로 실행): v2 유한(리프 max·job 64 GiB → 64 GiB, 근거 job 파일) ·
  v2 무제한(읽은 계층 2) · **경로 미마운트 → unobserved** · **proc 없음 → unobserved** · v2 루트 컨트롤러 보임 → unlimited ·
  **루트인데 안 보임 → unobserved** · v1 유한 128 GiB · v1 센티널 → unlimited · **memory 계층 없음 → unobserved** ·
  hybrid → unlimited(v1) · 리프에 memory.max 없음(컨트롤러 미활성)+부모 유한 → 부모 값 · 항상 5필드.
- **e2e (실제 `run_staged.sh 1` 경로 · 스텁 launcher)**: unobserved → rc 2 + 노드별 사유 기록 · legacy `none` → rc 2 ·
  finite 1 GiB → rc 2 ("필요 … > 가용 1.0×0.85") · finite 64 → 통과 + state/limit/basis · unlimited+SLURM 16 GiB →
  근거 "min(스케줄러 할당 16.0, MemTotal …)" · 할당 미관측 → 근거 "미관측".
- 소스 단언 3건 (스크립트 3상태 · 판정기 정지 문구/legacy · MEMG_SCHED_GB export).

### v40 실물 시연 I–O (번들 사본 · 스텁 launcher · 96호스트 · 48노드×2동시 · 필요 6.1 GiB/노드)

| | 조건 | 결과 |
|---|---|---|
| I | **실물 `_probe_node.sh` 를 이 호스트에서 직접 실행** (스텁 없음) | `vm · 14327676928 · 16856092672 · finite · /sys/fs/cgroup/memory/…/memory.limit_in_bytes` — v1 유한 13.3 GiB, 근거 경로 기록 |
| J | unlimited(검증) · 스케줄러 할당 미관측 | 통과 · 상태 {unlimited: 96} · basis *"상한 = MemTotal 15.7 (러너 호스트에서 스케줄러 할당 미관측)"* |
| K | unlimited + SLURM_MEM_PER_NODE=128 GiB | 통과 · basis *"min(스케줄러 할당 128.0, MemTotal 15.7)"* · JSON `scheduler_alloc_GiB_runner` 128.0 |
| L | finite 64 GiB | 통과 · 상태 {finite: 96} · basis *"cgroup 유한 제한 64.0 GiB (…/memory.max) · MemTotal 15.7"* |
| M | finite 4 GiB (MemTotal 15.7 넉넉) | **정지** rc 2 — *"48 노드: 노드당 필요 6.1 GiB > 가용 4.0×0.85=3.4 GiB"* (제한값으로 판정) |
| N | unobserved — 경로 미마운트 (MemTotal 15.7 넉넉) | **정지** rc 2 — *"48 노드 메모리 제한 **미관측** (cgroup-path-not-mounted:… ) — 물리 RAM 으로 대체하지 않고 멈춘다"* |
| O | 구판 3필드 `none` | **정지** rc 2 — *"미관측 (legacy-probe-format(none))"* — v39 는 이 경로를 통과시켰습니다 |

잔재 0 (사본·원본 모두).

### ⚠ 남은 한계 (범위를 넓히지 않았습니다)
- cgroup 마운트 경로는 `/sys/fs/cgroup`(v2) · `/sys/fs/cgroup/memory`(v1) 고정입니다. 다른 배치는 **unobserved → 정지**로
  떨어지며 통과시키지 않습니다. 지원 범위는 이번 인수처(Slurm · 통상 마운트)입니다.
- `unlimited` 는 *cgroup 이 안 막는다* 는 뜻이지 스케줄러가 코어·메모리를 **예약했다는 증거가 아닙니다** (JSON 의
  `⛔_이_기록이_보증하지_않는_것` 에 명시). CPU 예약은 인수처 답변 항목으로 넘겼습니다 (P2-1).
- 프로브는 프로브 프로세스의 배치이고 VASP 의 배치가 아닙니다 (종전과 같음).
- 스텁 시연(J–O)은 실행 노드의 프로브 **출력을 흉내낸** 것입니다 — 노드 위 실제 실행은 I 한 건(이 호스트)뿐입니다.

## P2-1 — 문의문 보완 ✅ (`INQUIRY_queue_2026_09_08.md`)
- 21행 → *"중앙 추정은 55.6/51.5시간이고, NELM=200 시나리오는 148.2/137.4시간이야. 스텝당 시간 모형이 ±2배라 보장된
  상한은 아니고, 156시간은 계획 요청값이야."* — "최악" 표현 삭제 · 금지어에 추가.
- 1-b) 추가: *"잡당 192랭크를 4노드에 나눠 노드당 48랭크 … 노드별 CPU 예약량(물리코어/SMT 구분)과 실제 할당 메모리·cgroup
  제한을 단위까지 … 현재 메모리 계획은 노드당 188 GB"*.
- 292/73 GB → **"지금 우리 모형값 · 예약 요구량이나 안전 보장이 아님"**. README 의 같은 문장에도 "(모형값 · 실측 아님)" 을
  붙였습니다.
- 코어 수·동시잡 수가 계획과 달라지면 **재계산**해서 보내고 4.46일·156 h 를 그대로 옮기지 않는다는 문장 추가
  (site_contract 기록 항목에도 CPU/메모리/cgroup 필드 추가).
- 발송은 1저자가 합니다 (ZIP 미첨부 · 코드 수정과 병행 가능하다는 판정대로).

## P2-2 — 독립 추정기 CLI ✅ (`vasp_cost_estimate.py`)
- `★ 추정` 을 `stage_alloc_h`(경로 사전순 FIFO + 물결 장벽) 합으로: **4.46 일** (1단계 55.6 h + 2단계 51.5 h).
- LPT 값(4.14 일)은 *"참고 (러너 순서 아님 · 계약에 쓰지 않는다) — 낙관"* 으로만 찍습니다. 동시 실행별 표도 FIFO+장벽 열,
  권고(`--recommend`)·목표 탐색(`--target_days`)의 LPT 출력에 "LPT 가정 · 참고" 라벨.
- 표현 정정: *"추정기 전체가 통일됐다"* 고 하지 않습니다. **계약 숫자가 나오는 경로(생성기 MANIFEST · CLI ★ · 단계 할당 절)는
  FIFO+장벽으로 통일**했고, LPT 는 참고 표시로 남아 있습니다.

## v40 확인 (9가지)
① README=SUBMIT 8/8 · 토큰 15종(v39 13종 + "유한 / 무제한(검증) / 미관측" · "모형값") · 금지문구 부재 · 단계 요청 숫자 1
② verify_zip ③ governance rc 0 · 4/4 ④ 분석기 437/437 + k-selftest ⑤ census 19 · 12/7
⑥ files 129 · POTCAR 0 · 4.46 일 · 156 h · 4노드/16 · clean=true ⑦ 종 순서 19/19 · KPAR {4: 13, 1: 6} · NCORE 4
⑧ 커밋 origin 도달 ⑨ **v39 대비 계산 입력 57파일 동일**

생성기 selftest exit 0 · verify 30/30 · e2e 15/15 · 프로브 픽스처 12/12 · 추정기 PASS · convention 0 위반 · `run_staged.sh` `bash -n` 통과.

## 재승인 조건 대조

| | 조건 | 상태 |
|---|---|---|
| 1 | §2 미관측/무제한 상태 구분 + 미관측 중단 + 근거 기록 + 재생성 해시 | ✅ v40 (위 표 · IDENTITY_v40) |
| 2 | 문의문 보완 → 인수처 CPU·메모리·큐/운영 답변 | 문구 ✅ · **답변 대기** (1저자 발송) |
| 3 | 독립 CLI 의 LPT 표시 정정 | ✅ 참고 라벨 · 계약 경로 FIFO |

**코드 P1 이 닫혀도 인수처의 자원·큐 확인 전까지 생산 실행 보류** — 그대로 지킵니다. 발송메일(v40)에도
*"이 답을 받기 전에는 시작하지 말아 주십시오"* 가 있고, 노드별 상태·사유가 찍혀 멈추면 `PLACEMENT_PROBE.json` 을
보내 달라는 문장을 추가했습니다.

## 발송메일의 "잡당 84 h"
v40 메일에도 1회 — 종전 메일의 옛 숫자를 버리라는 **철회 안내 문장 안**에서만입니다. 지시로 쓰인 곳은 없습니다.
