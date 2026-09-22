# CLAUDE.md — Yonghoon-DEM-DFT 프로젝트 지침

전고체전지(황화물 SE) 계산 캠페인 repo. 아래 규칙은 세션이 바뀌어도 유지되는 표준이다.

## 여기서 시작 (새 세션·압축 후 6줄)

| 묻는 것 | 정본 |
|---|---|
| **지금 상태** — 뭘 이어서 하나 | `kb/open_items.md` 의 **⏭ 절**(머리에 최종 갱신일). 통째로 읽지 말고 grep |
| **판정** — 결정됐나 | `db/governance/decisions.json` (`decision_state: active` 만 유효. proposed 는 아직 아니다) |
| **값** — 숫자가 뭔가 | `db/properties/canonical_registry.json` (값·status·`comparison_group`·`prohibitions`) |
| **금지** — 인용해도 되나 | `db/properties/citation_hazards.json` (BLOCKED / HOLD / CONDITIONAL / SUPERSEDED) |
| **리뷰** — 회신 어디 있나 | `kb/reviews/INDEX.md` (회신 letter A→BI, prompt/reply 짝) |
| **화면** — 남이 보는 표면 | `webapp/` (아래 §화면 규율) |

- 원격 기계가 지금 뭘 돌리는지는 **최신 런북**: `kb/projects/restart_runbook_2026_09_07.md`.
- 세션을 닫을 때 **`kb/open_items.md` ⏭ 절을 갱신한다** — 지금까지 아무도 안 시켜서 8일 낡았었다.

## 소통
- 한국어 대화체로 답한다. 문어체/번역체("-했다") 금지. 짧고 구체적으로.
- 그림 라벨·캡션은 영어만 (사용자 뷰어에서 한글 폰트 깨짐).
- 사용자는 물리는 알지만 계산 세부는 배우는 중 — 새 개념은 한 단계씩 설명.
- 원격 서버 작업은 "붙여넣기 블록 제공 → 사용자가 실행 → 출력 회수" 워크플로.
- ⛔⛔ **`1저자` 는 트랙마다 다르다 — 결정 항목을 쓸 때 트랙을 먼저 쓴다** (2026-09-22 확인).
  · **ESW · cascade · 우리 DFT 기준선** → **사용자가 1저자**다. 결정이 그 자리에서 나고
    통지할 제3자가 **없다**. *"1저자 결정 대기"* 로 적으면 **이미 내려진 결정이 대기로 보인다.**
  · **li2s (소셀 유리 · 회신 letter A→BU)** → **사용자가 1저자가 아니다.** 규칙·판정을 준
    **외부 1저자**가 있고 **회신이 필요하다.** 사용자의 *"진행해"* 는 **실행 승인**이지
    규칙을 준 사람의 **동의를 대신하지 않는다** — 그런 건 **잠정**으로 내리고 그렇게 적는다.
  ⚠ 2026-09-22 에 이걸 **두 번 틀렸다**: ① 넷을 다 "1저자 대기" 로 묶었고
  ② 그걸 고치면서 "1저자 = 사용자라 통지 불필요" 로 **반대쪽으로 과잉 정정**했다.
  트랙을 안 쓰면 어느 쪽인지 알 수 없다.

## 데이터 규율 (어기면 안 되는 것)

> **값을 인용하기 전 30초**: `canonical_registry.json`(값·status·`comparison_group`·`prohibitions`)
> → `citation_hazards.json`(BLOCKED/HOLD/CONDITIONAL/SUPERSEDED) → `db/governance/decisions.json`.
> 검증은 `python3 tools/db/validate_canonical.py`. **아래 규율은 그 원장의 사람용 요약이고,
> 충돌하면 원장이 이긴다.**

- **Band gap**: fixed-occupations nscf의 VBM/CBM 고유값만 인정. DOS-threshold 판독 금지 (~0.3 eV 과소).
  Canonical: comp1 2.066 / modelc(LPSCl1.6) 2.099 / +B2O3 1.9671 / LPSOCl(+O) 2.2309 eV
  (계별 `source_path` 는 `db/properties/canonical_registry.json` — lpsocl 만 `lpsocl_dos_gap.json` 이다).
  ✅ **네 값 다 방법일치 해소됨** — comp1 2026-08-24(2.0656 재현) · **modelc 2026-09-11**
  (fixed-occ nscf 재계산). 레지스트리 `method_integrity_flag.severity` 가 둘 다 *"해소됨"* 이다.
  ⛔ 2026-09-18 정정: 이 줄은 *"modelc 는 실행본이 **영구** 미해소"* 라고 적혀 있었고 **7일 낡았었다**.
  원장이 이미 해소로 바뀐 뒤에도 여기가 안 바뀌어서, 다음 사람이 멀쩡한 값을 의심하게 만든다
  (실제로 그랬다). **원장을 고쳤으면 이 파일도 같이 본다.**
- **BVSE** (tools/comp1_v3/): softBV Li–X R0 = S 2.105 / Cl 2.249 / O 1.466, b=0.37; BVSE=(BVS−1)²;
  ~0.25 Å voxel; 채널% = above-min ≤ iso. **정량·순위는 원본 주기셀 값만** 인용(큐빅 박스는 표시용, ±1.3%p 표본 편차).
- **MLIP-MD** (tools/modelc_v3/, tools/ionic/): UMA-s-1p1(omat), Langevin NVT, dt 2 fs, friction 0.02,
  equilib 5 ps / prod 200 ps, **MSD 창 2–50 ps 고정**, 아레니우스는 600/800/1000 K 3점(400/500 K 제외 판정),
  σ는 Nernst–Einstein(Haven=1) — **절대값 인용 금지, 비율도 멀티시드 판정만**(단일시드 1.33× 철회 사례, SEMIFINAL 2026-07-09).
  · Ea 오차막대는 600 K 3-시드 — ⛔ **이 줄은 결정계(modelc·lpsocl box331 558원자)에만 해당한다.**
    2026-09-22 회신 BS 에서 1저자가 잡았다: 범위를 안 적어 둬서 이 문장이 **소셀 유리 캠페인 서술에
    딸려 들어갔고**, 정작 그 카드는 600 K 를 **감김으로 배제**한다(5 ps lag p90 MSD 48.9 Å² =
    무상관 한계 48.88, 상한은 550 K). 유리 쪽 오차막대는 **구조(담금질) 시드 5 의 IQR** 이고
    **풀링 금지**다 — 속도 시드의 열잡음과 **다른 양**이다. 계마다 카드가 온도·시드를 따로 선언한다.
  ⭐ **1저자 인용정책 2026-09-18**: *"절대값은 안 쓰고, QE 시뮬레이션에서 나온 값의 **상대 차이**가
  난다 이 정도로만 쓴다."* ⇒ σ·D 뿐 아니라 **Ea 도 계 간 상대차로만** 쓴다. 레지스트리에서
  `canonical · citable` 로 올라간 값도 이 정책 아래 있다 — canonical 은 *값이 확정*이라는 뜻이지
  *절대값을 인용해도 된다*는 뜻이 아니다.
- **UMA는 Li₃N에 사용 금지** (2026-06 결정론적 편향 판정). LPSCl 계열 MD에는 UMA가 검증된 표준.
- 평균류 지표(site mean-3p 등)는 **그림 표시 창과 동일한 창**(-8..0 eV)으로 계산·인용.
- 슬랩 계산은 기하 승계(verified-carry: 마지막 ATOMIC_POSITIONS 스플라이스 + 검증) + local-TF/저β 믹싱.

## 그림 하우스 스타일 (모든 새 그림)
- `tools/figures/house_style.py` import (INK #1f2937, MUT #6b7280; 원소 팔레트 Li #0d9488 / P #7c3aed /
  S #c05621 / Cl #65a30d / O #be123c / B #0284c7; gap 밴드 #fef9c3 + #2563eb dashed).
- spines top/right 제거, dpi 300, 같은 계열 그림은 기존 family와 양식 통일.
- 데이터 그림은 **Origin-ready CSV를 동시 출력**해 db/properties/에 등록 (열 이름 명시적).
- .opju 자동화는 클라우드에선 불가 — 로컬 Windows Claude Code + originpro로 (CSV가 우리 쪽 절반).

## 계산 자원 (최종 갱신 2026-09-08)
- **KISTI** neuron(x3430a02): Slurm, QOS 제출 제한 — scancel 직후 재제출 금지(카운터 지연). pseudo는
  /scratch/x3430a02/kgy/manuscript_support/pseudo.
- **kgy** (RTX3090, QE-GPU + uma env): ssh kgy@59.12.161.91.
  ⛔⛔ **QE-GPU 런타임은 추측하지 말고 `ldd` 로 바이너리에게 묻는다.** 2026-09-08 에
  같은 자리에서 **세 번** 틀렸다: ① conda mpirun 탓 → ② 런처를 뺐더니 `libgomp: TODO`
  → ③ hpcx 를 자동탐지했는데 kgy 의 pw.x 는 **`~/apps/openmpi-4.1.6`** 로 빌드돼 있었다
  (hpcx 에서 오는 건 scalapack 뿐). 머신마다 다르므로 규칙이 아니라 링크가 근거다.
  ```
  ldd <pw.x> | grep -E "libmpi|libnvomp|libgomp"   # ← 항상 여기서 시작
  M=$(ldd <pw.x> | awk '/libmpi\.so/{print $3}')   # 실제 링크된 MPI
  export OPAL_PREFIX=$(dirname $(dirname $M)) PATH=$OPAL_PREFIX/bin:$PATH
  export LD_LIBRARY_PATH=$(dirname $M):<nvhpc>/compilers/lib:/usr/local/cuda-12.6/lib64
  export OMP_NUM_THREADS=1     # libnvomp + libgomp 동시 링크 시 필수
  $OPAL_PREFIX/bin/mpirun --oversubscribe -np 1 <pw.x> -nk 1 -in x.in > x.out
  ```
  ★ `libnvomp` 와 `libgomp` 가 **둘 다** 링크돼 있으면(kgy: libfftw3_omp 가 GNU 를 끌고 옴)
  OpenMP 런타임이 둘이라 `libgomp: TODO` 로 즉사한다 → `OMP_NUM_THREADS=1`.
  `tools/doping/run_force_check_scf.sh` 가 이 전부를 ldd 에서 유도하고, 못 읽으면
  **시작하지 않는다**.
  · pw.x 를 던지기 전 `nvidia-smi` 로 **python3(UMA)가 GPU 를 쓰고 있는지** 본다 — kgy 도 공유다.
  · **uma python = `/home/kgy/apps/miniforge3/envs/uma/bin/python`** (실측 2026-09-20 ·
    fairchem ok · torch 2.8.0+cu128). envs 는 `dft · mpm · uma` 셋이다.
    ⚠ `/proc/<pid>/exe` 는 `…/bin/python3.11` 로 풀리는데, **버전이 안 박힌 `…/bin/python` 을
    쓴다** — 3.11 이 올라가도 안 깨진다. base 는 `/home/kgy/apps/miniforge3/bin/python3` 라
    `import fairchem` 이 실패한다. tmux·자식 프로세스엔 **절대경로**를 박는다
    (러너면 `--python <절대경로>` 도 같이 — 자식이 base 로 떨어진다).
  · ⭐ **경로를 모르면 `/proc/<pid>/exe` 에게 묻는다 — 추측·히스토리보다 이게 낫다.**
    ```
    pgrep -af disorder_ensemble_diffusion     # ① PID 를 얻는다 (경로는 여기서 안 나온다)
    readlink -f /proc/<pid>/exe               # ② 실제 인터프리터 — 이게 정답이다
    ```
    `pgrep -af` 는 **친 그대로의 토큰**(`python3`)을 주지 해석된 경로를 안 준다. 종전 지침은
    `~/.bash_history` 를 보라고 했는데, **돌고 있는 잡이 있으면 `/proc` 이 더 정확하다**
    (히스토리는 그 줄이 실제로 성공했는지 모른다). 2026-09-20 에 이걸로 한 번에 잡았다.
- **gabia** (A6000 단일 GPU, QE-GPU + fairchem/UMA): root@121.78.116.27. **pw.x와 UMA 동시 실행 금지**
  (VRAM 47/48 GB 점유 사례) — nvidia-smi로 확인 후 실행.
  · UMA python = **`/data/apps/miniforge3/envs/uma/bin/python`** (envs: dft·mace·mlipx·sevennet·uma).
    tmux 커맨드에는 **절대경로**를 박는다 — base 의 `python3` 는 fairchem 이 없다.
    ⛔ `pgrep -af` 는 **친 그대로의 토큰**(`python3`)을 주지 해석된 경로를 안 준다 — 여기서 경로를 캐지 않는다
    (2026-09-12 실패). 모르면 `~/.bash_history` 의 `conda activate` 줄이 답이다.
  · ⭐ **CPU pw.x 를 1 랭크로 돌리지 마라 (2026-09-19 실측, 6.8 배)**. LOBSTER SCF 가
    `-np 1 · OMP=8` 로 돌고 있었는데 **CPU 118 %** 였다 — 20 코어 중 1.2 개. iteration 1 이
    **4시간 40분**을 넘겼고 그대로면 며칠이었다. `-np 8 -nk 2` 로 **798 %**, 하룻밤으로 줄었다.
    ```
    pw.x = /data/apps/qe-7.4.1-cpu/PW/src/pw.x   (libmpi = /lib/x86_64-linux-gnu, GNU OpenMP)
    mpirun = hpcx (PATH 앞단) + **--allow-run-as-root 필수** (root 계정이라 가드에 막힌다)
    mpirun --allow-run-as-root --bind-to none -np 8 pw.x -nk 2 -inp x.in
    ```
    · **랭크를 올려도 총 메모리가 안 는다** — 실측 `Estimated max dynamical RAM` 총계가
      np 2/4/8 에서 전부 **~33 GB** (16.65 / 8.33 / 4.17 GB per process). 메모리 걱정 말고 올려라.
    · **OMP 는 여기서 거의 일을 안 한다** (8 스레드에 118 %). `OMP_NUM_THREADS=1` + 랭크로 간다.
      kgy 와 달리 `libnvomp` 는 없어서 즉사는 안 하고 **느려지는** 형태로 나타난다.
  · ⭐ **"출력이 멈췄다" 를 죽었다로 읽지 마라 — 90 초 표본으로 가른다** (2026-09-20 실측).
    LOBSTER nscf 가 **20.8 시간** 출력 0 바이트였다. 살아 있었다. 판별은 `/proc` 세 줄이면 된다:
    ```
    PIDS=$(for x in $(pgrep -f <입력파일명>); do [ "$(cat /proc/$x/comm)" = pw.x ] && echo $x; done)
    cpu(){ s=0; for x in $PIDS; do s=$((s+$(awk '{print $14+$15}' /proc/$x/stat))); done; echo $s; }
    T0=$(cpu); sleep 90; echo "$(( ($(cpu)-T0)/100 )) 초 / 90 초 · 랭크 $(echo "$PIDS"|wc -l)"
    ```
    **랭크수 × 90 초에 근접**하면 계산 중이다. 0 이면 멈춘 것. I/O·출력이 0 인 것은 **단서가 아니다** —
    nscf 는 k-점이 **끝나야** 쓰고, Davidson 중엔 디스크를 안 건드린다.
    · 실측 원가 (gabia CPU 8 랭크 · nat 120 · ecutwfc 70/560): **SCF 10h33m** ·
      **nscf 는 k-점 하나에 ~20 h** (`nbnd=920`, 시작 wfc 가 `546 atomic + **374 random**`, `nosym`).
      LOBSTER 용 큰 nbnd + 난수 밴드가 값을 다 먹는다 — 다음에 같은 계를 돌리면 nbnd·k-격자가
      정말 그 값이어야 하는지 **던지기 전에** 확인한다.
  · ⛔⛔ **살아 있는 MPI 잡에 `gdb -p` 를 붙이지 마라** (2026-09-20, 내가 했다).
    gdb 는 붙는 순간 대상을 **정지**시킨다. `timeout` 이 gdb 를 죽이면 랭크가 `T`(stopped) 로
    남을 수 있다 (이번엔 운 좋게 자동 detach 로 풀렸다 — 운이었다). 20 시간짜리 잡에 얹을 위험이
    아니다. ⇒ 진단은 위 `/proc` 표본으로 하고, 그래도 스택이 필요하면 `perf top -p` 를 쓴다
    (읽기만 한다). 상태 확인: `ps -o stat= -p <pid>` 가 `T` 면 `kill -CONT`.
  · ⛔ **살아있는 MPI 잡의 환경을 복사해서 새 mpirun 을 띄우지 마라** (2026-09-19, 세 번 헛발질).
    `/proc/<pid>/environ` 의 `OMPI_MCA_orte_hnp_uri`·`ess_base_jobid` 등은 **그 잡의 런타임 상태**라
    새 mpirun 이 옛 데몬에 붙으려다 `mpirun does not support recursive calls` 로 죽는다.
    ⇒ 가져올 것은 **`PATH`·`LD_LIBRARY_PATH`·`OPAL_PREFIX` 셋뿐**이고, 그 다음
    `unset $(env | grep -oE '^(OMPI|PMIX)_[A-Za-z0-9_]*')` 로 전부 지운 뒤
    **`OMPI_ALLOW_RUN_AS_ROOT=1` 만 다시 넣는다**(같이 지워진다).
  · ⛔⛔ **`pkill -f "pw.x"` 금지 — 이름으로 잡으면 남의 계산을 같이 죽인다.**
    2026-09-19 실측: LOBSTER 를 8 랭크로 재시작하면서 `pkill -f "pw.x"` 를 썼고,
    같은 기계에서 돌던 **NdP5O14 vc-relax 가 이온스텝 5 에서 같이 죽었다** (03:31,
    Davidson 한가운데서 에러 없이 끊김 — 밖에서 죽인 시그니처). 7시간 51분을 모르고 보냈다.
    ⇒ **입력 파일 이름으로 잡는다** (잡마다 유일하다):
    ```
    pgrep -af "lobster_scf.in"          # ① 먼저 보고
    pkill -f "lobster_scf.in"           # ② 그 다음에 죽인다
    ```
    PID 를 직접 쓰는 것도 좋다. `pw.x`·`python3`·`mpirun` 같은 **공용 이름으로는 절대** 안 된다.
    ⛔ **스크립트 이름도 공용이다** — `disorder_ensemble_diffusion` 으로 잡으면 그 드라이버를 쓰는
    **모든** MD 가 걸린다. 2026-09-21 kgy 에서 `for x in $(pgrep -f disorder_ensemble_diffusion); do
    kill $x; done` 으로 **lpsocl s6/T800 을 43 %(≈7.4 h)에서 죽였다** (cascade 를 잡으려던 것).
    잡을 가르는 것은 `--out_root`·`--label` 같은 **잡 고유 인자**다: `pgrep -af "lpsocl_box331_400ps/s6"`.
  · ⭐ **랭크를 바꾸기 전에 스크래치에서 프로브한다** — 돌던 잡을 죽이고 나서 안 되는 걸 알면 최악이다.
    별도 폴더 + `ESPRESSO_TMPDIR=<scratch>` 로 90 초만 띄워 `Parallel version` 헤더와
    `Estimated max dynamical RAM` 만 보고 죽인다. `ESPRESSO_TMPDIR` 이 입력의 `outdir` 을 덮으므로
    **라이브 잡의 `.save` 가 안 다친다**. 2026-09-19 에 이 프로브가 값어치를 했다 —
    바로 죽였으면 LOBSTER 는 죽고 재시작은 segfault 였다.
- **Materials Project REST 조회**: ⛔ **403 을 키 문제로 읽지 마라 — Cloudflare 가 UA 를 막는다**
  (2026-09-21 gabia 실측). `urllib` 기본 UA 로 치면 `error 1010 · browser_signature_banned` 로
  **무키 요청도 똑같이 403** 이다. 키는 멀쩡했다(32자 신 API 키).
  ```
  # 판별: 무키 요청도 403 이면 인증이 아니라 문턱이다
  UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
  # urllib: headers={"X-API-KEY": KEY, "User-Agent": UA}   ← UA 를 반드시 준다
  curl -s -H "X-API-KEY: $MP_API_KEY" -H "accept: application/json" <url>   # curl UA 는 대개 통과
  ```
  · gabia 의 **어느 conda env 에도 `mp_api` 가 없다** (dft·mace·mlipx·sevennet·uma 전부). stdlib REST 로 친다.
  · ⚠ **MP 가 id 를 옮기는 중이다** — `mp-1211324` 로 물으면 `mp-aaacqxxk` 가 돌아온다. 기록엔 둘 다 남긴다.
- **desktop WSL**: ORCA r2SCAN-3c (SDCP 분자 계열).
- 공통: 실행 스크립트에 pgrep 중복실행 가드, 출력 grep은 `grep -a`(NUL 오염 대비), watch 스크립트 관례 유지.
- ⛔⛔ **`pgrep -f <패턴>` 은 자기 자신을 센다 — 개수로 쓰면 틀린다** (2026-09-20 에 **하루 두 번** 밟았다).
  패턴이 명령줄에 들어간 것은 **전부** 걸린다: `watch` 프로세스 · 그 `sh -c` · pgrep 을 감싼 서브셸 ·
  그 패턴을 쓰는 다른 watch. 실측: MD 파이썬이 **2 개**인데 `pgrep -c -f disorder_ensemble_diffusion`
  이 **5** 를 줬다. 같은 함정의 앞선 판 — tmux 대기 스크립트가 자기 래퍼를 세서 **영원히 안 끝났다**.
  ```
  # ⛔ 이렇게 세지 마라
  pgrep -c -f disorder_ensemble_diffusion
  # ✅ comm 으로 거른다 (진짜 그 프로그램만)
  for x in $(pgrep -f disorder_ensemble_diffusion); do
    case "$(cat /proc/$x/comm 2>/dev/null)" in python*) echo $x;; esac; done | wc -l
  ```
  · **살았나 죽었나**만 볼 때는 개수 말고 **PID 를 잡아 `kill -0 <PID>`** 를 쓴다.
  · watch 문자열 안에서 그 패턴을 쓰면 **watch 자신이 걸린다** — 특히 조심.
- ⭐ **진행 신호는 "끝난 것" 이 아니라 "시작한 것" 으로 본다.** MD 러너는 `ensemble_results.json` 을
  런이 **끝나야** 쓴다(`disorder_ensemble_diffusion.py:507`) — 7 시간짜리면 그동안 0 으로 보여서
  멈춘 것처럼 읽힌다. `run_meta.json`(시작 시 기록) 개수를 같이 찍는다.
- **산출물 회수 기본 경로 = `C:\Users\Administrator\Downloads\`** (1저자 지정 2026-09-01).
  scp 블록은 이 경로를 기본으로 쓰고, 받은 뒤 해시 대조까지 한 블록에 넣는다
  (PowerShell `Get-FileHash -Algorithm SHA256` · cmd `certutil -hashfile <경로> SHA256`).

## Git
- 브랜치 **claude/friendly-meitner-lldvar** 에만 커밋/푸시. PR 생성 금지(요청 시에만).
- force-push는 --force-with-lease만. 커밋 메시지에 모델 ID 넣지 않기.

## VESTA 산출물
- .vesta 파일은 **ASCII 전용 + CRLF** (em-dash 등 비ASCII가 IMPORT_DENSITY 파싱을 깨뜨린 사례).
- 부피 데이터 cube는 aboveMin 관례(맵 최소 빼기), .vesta + .cube를 쌍으로 배포(같은 폴더).
- 구조 배포는 xyz + POSCAR(.vasp) 페어 (xyz는 격자 없음 → Boundary 타일링은 vasp).

## litdb (문헌)
- "논문 에이전트" 요청 = litdb-curator 서브에이전트: litdb/papers/ digest + INDEX.md + comparison_vs_ours.md 갱신.
- 문헌 수치는 소환값 — 우리 db 절대값과 섞지 않기 (방법 명시 없이 이식 금지).
- **litdb 를 볼 때는 `litdb/figures/<slug>/` 의 크로핑 PNG 를 Read 로 같이 본다** (digest 텍스트만
  보고 답하지 않기). 어느 그림인지는 그 폴더의 figures.json caption 으로 찾고, 없으면
  `tools/litdb/extract_figures.py --inbox` 로 먼저 만든다. **본 그림/안 본 그림을 구분해 말한다.**
  그림에서만 읽은 값은 `figure-read ≈` 표기. 표(tab_*.png)는 PDF 텍스트가 더 정확하다.

## 화면(webapp)·claim 결속 규율 (2026-09-08 도입 · 2026-09-09 문서화)

> 규율이 원장에만 있고 **화면에 안 실리면** 사람은 화면을 인용한다. 그래서 결속(binding)이다.
> 대상은 `webapp/` 전체와, 화면이 읽어 가는 문서다.

- **철회·비인용 값은 자기 claim id 를 단 요소 *안*에 있어야 한다** (`data-claim`).
  근처에 ⛔ 표지를 두는 것은 **결속이 아니다** — 값이 복사·발췌될 때 표지가 따라가지 않는다.
  우연 일치는 면제가 아니라 **부인을 선언**한다 (`data-claim-not`, id 를 이름으로 대서 · 셀 단위로).
- **표식은 텍스트 노드다** (`.claim-mark`). CSS `content:` 로 그리면 **복사·인쇄·텍스트 추출·
  보조기기에 안 나간다** — 화면에만 있는 경고는 경고가 아니다.
- **매처는 숫자를 값으로 본다** (`0.199 ≡ 0.1990`). 문자열 일치가 아니다.
  조건 셋을 같이 본다: **부호 · 단위 · 출처**(`origin="external"`).
- **litdb 는 남의 문서다** → `origin="external"`. 우리 계 이름이 없으면 `suspect` 로 두고
  **목록에는 남긴다** (조용히 버리지 않는다).
- **철회에는 "대체값 없음" 을 적을 자리가 있다** — `retracted.instead_kind`
  (`sentinel_none` | `claim_ref` | `prose`). 이 자리가 없으면 사람이 아무 문장이나 채운다
  (2026-09-08 실측 사고: 죽은 키 `FINAL_for_paper.Ea_eV_PAPER` 를 3주간 "이것만 인용하라" 고 가리켰다).
- **`validate_hazards()` — 인용위험 원장도 검사 대상이다**: level 어휘 · claim 실재 ·
  **점표기 키 실재** · id 중복.
- ⛔ **`unbound == 0` 은 지표가 아니다.** 자동 결속 경로가 지나가면 구조적으로 0 이 된다.
  지표는 **표면별 음성시험**이다 — 렌더된 HTML 에서 선언만 지우고 다시 스캔해서 잡히는지 본다.
  래칫(`_LEGACY_UNBOUND`)을 **다시 채우는 것이 완화다** (시험이 `== {}` 를 강제한다).
- **브라우저에서 마크다운을 다시 파싱하지 않는다** (`marked.parse` 금지 린트).
  판정은 **서버 한 곳**에서 한다 — 두 곳에서 파싱하면 두 판정이 갈린다.
- 새 화면·새 숫자를 올릴 때: 숫자는 레지스트리에서만 오고(화면이 자체 보관 금지),
  표면을 추가하면 **음성시험 표면 목록에도 추가**한다.

## 원고 작성
- kb/templates/manuscript_prompts.md 의 템플릿 사용 (figure 단위 요청, Wiley 스타일 R&D, 학술 5문장 재번역,
  로컬 PDF 기반 reference list).
- 레퍼런스는 링크가 아니라 **로컬 PDF/litdb digest 기준**으로 작성, 인용 역할 확인 후 삽입(2026-07 Kim/Cui 교훈).

## 코드 규율 (2026-08-11 채택)
- **새 스크립트 쓰기 전 기존 것부터 찾는다** (tools/ 에 py 305 · sh 106 · 62k줄 — 중복이 진짜 위험).
  사다리: ① 이게 있어야 하나 → ② tools/ 에 이미 있나(`grep -rl`) → ③ 기존 도구에 플래그 추가로 되나
  → ④ stdlib 로 되나 → 그 다음에 새 파일. **기존 도구 확장이 새 파일보다 항상 낫다.**
- 물리 규약(MSD 창 2–50 ps, 자유절편 D)은 여러 파일에 복사돼 있다 — 수정하면
  `python3 tools/convention_check.py` 로 갈라졌는지 확인 (0 위반 유지, 예외는 EXEMPT 에 **사유 명시**).
- **새 도구는 `--selftest` 를 단다 — 음성 경로(틀린 입력을 잡아내는지) 포함.**
  양성만 있는 selftest 는 통과해도 아무것도 보증 못 한다 (vasp 번들 v2 선례).
- 도구 docstring 에 **"이 도구가 못 하는 것"** 을 적는다 (한계 은폐가 제일 비싼 버그).
- ⛔ **조용히 틀린 경로** — 선언은 맞는데 실행 경로가 다른 일을 하고 오류가 안 난다.
  2026-09-13 하루에 **여섯 건**이 나왔고 전부 selftest 초록이었다 (`kb/methodology/silent_wrong_path_2026_09_13.md`).
  · 새 필드를 기록에 넣을 때 **"이 값을 읽는 게이트가 어디냐"** 를 한 줄로 답하지 못하면 배선이 없는 것이다.
  · `x or DEFAULT` 전에 **0·""·[] 가 유효한지** 묻는다 — 특히 정렬·min·max 키에서 치명적이다
    (`e_above_hull or 9e9`: 최선값 0.0 이 최악값으로 둔갑, **81일** 생존).
  · 잘린 창에서 메타를 찾을 때 **"못 찾음"과 "없음"을 구분**한다. 창이 우연이면 넓히고,
    **정책이면 유지하되 창 밖 발견을 보고**한다 (그래야 다음 사람이 정책을 우연으로 안 읽는다).
  · 화면·출력에서 **없는 값을 0 으로 그리지 않는다** (`or 0.0` → `—`).
- ⚠ **시험을 쓴 뒤 대상을 일부러 깨서 빨간불을 확인한다.** 안 하면 헛것을 잰다 —
  2026-09-13 에 내가 쓴 시험 **셋이 엉뚱한 것을 쟀고** 셋 다 통과했다 (창이 아니라 다른 필터가
  막고 있었음 · 호출부만 되돌려 함수는 그대로 · 리스트의 *존재*만 보고 *채워짐*은 안 봄).
- 진행 보고·붙여넣기 출력 해석은 **짧게**. 단, 새 개념 설명은 위 소통 규칙대로 한 단계씩 — 압축하지 않는다.
- **도구 출력은 기본이 요약이다.** 매번 찍히는 목록은 플래그 뒤로 숨긴다
  (`kb_wiki.py lint` 은 레거시 49건을 한 줄로 — 목록은 `--legacy`. 이 한 건이 출력 81% 감소).

## 계산 규율 — **던지기 전에 보고량 정의** (2026-08-28 채택 · 용어 2026-09-01 개정)

> **용어 규율 (2026-09-01, 1저자 결정).** 사람이 읽는 표면 — 원고·SI·슬라이드·발표·
> 웹앱 화면·리뷰 프롬프트·1저자 설명 — 에는 **필드에서 쓰는 말**만 쓴다.
> · `estimand` → **보고량** / 정의된 측정량 (영문: *the reported quantity* ·
>   *target quantity* · *well-defined observable*)
> · `canary`·`카나리` → **대조 잡** / 검증용 대조 계산 (영문: *control calculation* ·
>   *sanity-check job*)
> · `claim ceiling` → **허용 서술 범위**
> ⚠ **코드 필드명·과거 기록은 안 바꾼다** — `kind: "estimand"`, `canary_geometry`,
> `estimand_card.md` 같은 기계 경로를 개서하면 원장·게이트가 끊기고, 회신 원문을
> 고쳐 쓰면 이력이 깨진다. 바꾸는 것은 **앞으로 쓰는 산문**이다.

- **새 물리량을 계산하기 전에 `kb/templates/estimand_card.md` 를 채운다** (파일명은 기계
  경로라 그대로, 부르는 이름은 **보고량 카드**).
  리뷰에 보내는 것은 번들이 아니라 그 카드의 §1–3 이다 — *"무엇을 원하고, 어떤 식으로 재고,
  **이 계에서 그게 잘 정의되는가**"*.
- 채택 배경: SDCP-doped 흡착에너지를 **여덟 번** 계산했고 여덟 번 반려됐다. 받은 리뷰는
  전부 *"제대로 돌렸나"*(무결성·해시·INCAR·pin·게이트)였고 전부 통과했다.
  *"맞는 양을 재고 있나"* 는 여덟 번째에야 물었고 즉시 P0 가 나왔다.
  (⚠ 회신 N: "일곱 번은 안 돌려도 됐다" 는 철회 — 카드 블라인드 재생 시 확실히 잡는 것은
  #7–8 정도다. 여덟 실패의 원인은 하나가 아니라 층위다.)
- **판정 기준 (회신 N 문구): admissible state 가 여럿인데 선택·집계 규칙이 없으면
  스칼라 보고량은 정의되지 않는다.** 열린 껍질 · 자성 기판 · 산화환원 활성은 그 위험
  신호다. 걸리면 상태를 선언해 `X(상태)` 로 정의하거나, 집계 규칙(최저/앙상블/분포)을
  미리 적거나, 질문을 바꾼다.
- 보고량·마감 판정은 **`db/governance/decisions.json` 에 등록**한다 (proposed → 사람이
  ratify 해야 active). 해석 레지스트리는 이미 있다 — 새로 만들지 말고 그 그래프에 붙인다.
- **검증 게이트를 결과 보기 전에 정한다.** 그리고 게이트는 **"기준과 대상이 같은 제약인가"**
  까지 물어야 한다. 실측 두 층: phaseB 는 `mol_doped` 자화가 **0.175**(ISMEAR=1 결함)였고,
  wave1 은 **1.0000** 이지만 `NUPDOWN=1` 로 **강제**한 값이라 검증이 아니다 — 정작 복합체는
  `NUPDOWN=−1` 자유로 돌아 −0.31/3.72 μB 에 떨어졌다. **제약된 기준에서 자유로운 복합체를
  뺐다** (2026-08-28 정정, `kb/methodology/estimand_before_running_2026_08_28.md` §2.1).
  ⚠ 회신 O: 고치는 법은 "전 계에 같은 NUPDOWN 값" 이 **아니라** 같은 **state-selection
  policy** 다 — 전부 자유 바닥상태이거나, 선언된 해리채널과 양립하는 대응 제약.
- **규약 대조 30초**: `grep -rl "<양이름>" kb/` — 이미 판정이 있으면 그게 이긴다.

## 마감 규율 — **닫힘 조건을 먼저 박는다** (2026-08-28 채택)

- 캠페인을 닫을 때 **`db/properties/<계>_closed_<날짜>.json`** 를 남긴다:
  확정값 · **허용 서술(이대로만)** · **금지 서술** · **재개 조건(이것들만)**.
- 순서가 핵심이다 — 데이터를 보고 "닫혔다" 고 판단하지 않는다. **조건을 먼저 정하고,
  그게 채워졌으므로 닫는다.** SDCP 는 조건 없이 두 번 닫았다가 두 번 물렸다
  (2026-07-17 doped v1 철회 · 2026-08-28 회신 M 마감보류).
- **재개 조건 밖의 이유로 다시 열지 않는다.** "새 자세를 하나 더 봤다" 는 재개 사유가 아니다.
- 선례: `db/properties/sdcp_neutral_closed_2026_08_28.json`

## 컨텍스트 절약 (2026-08-11)
- 자동 compact 은 **기본값(실제 한계 근처)** 으로 둔다. `autoCompactWindow` 로 창을 좁혀
  50% 발동을 걸었다가 **압축 루프**를 맞았다(2026-08-11 철회 — 요약+파일 재독이 곧바로
  임계를 다시 넘겨 연속 3회 압축, 다른 브랜치 세션 사실상 정지). 다시 넣지 않는다.
  대신 상태줄(`tools/claude/statusline.py`)이 사용률을 상시 표시 — 70%↑ 에서 손으로 `/compact`.
- 읽기는 **부분 읽기 우선**: 큰 파일은 offset/limit, 검색은 head_limit.
  `kb/index.md`(25 KB)·`kb/open_items.md`(72 KB)는 **통째로 읽지 말고 grep**.
- **방금 쓴 파일을 다시 읽지 않는다.** 만든 파일 내용을 답변에 다시 붙여넣지 않는다.
- 긴 출력은 파일로 떨군 뒤 grep (`… > /tmp/x.log` → 필요한 줄만).
- 세션을 새로 여는 것보다 **이어가는 게 싸다**(프롬프트 캐시). 정리는 `/clear` 말고 `/compact` —
  `/clear` 는 CLAUDE.md·kb 재독을 다시 유발한다.
- 진짜 절감은 **재논증 방지**다: 이미 판정된 건 kb 카드에서 확인하고 다시 논증하지 않는다.

## kb 위키 규율 (2026-08-11 채택)
- kb 문서를 만들거나 크게 고치기 전에 **kb/SCHEMA.md 를 읽는다** (규칙 원본).
- 새 문서는 `python3 tools/kb_wiki.py new <dir> <slug>` 로 생성 (frontmatter 필수 — 기존 문서 소급 없음).
- 답이 안 난 반복 질문 → `kb/questions/` 카드, 논지 방어 → `kb/syntheses/` 카드 (반론 절 삭제 금지).
- `explored:` 는 **사람만** true 로 바꾼다. 근거가 하나뿐이면 `confidence: high` 금지.
- 마무리: `python3 tools/kb_wiki.py index` 재생성 + `lint` **0 errors** (kb/index.md 손편집 금지).
- 채택 배경: kb/methodology/llm_wiki_adoption_2026_08_11.md.

## 하위 폴더 지침
- **`research-agent/`** (논문 자동비서 — Scholar alert → triage → 분석 큐 → vault/litdb → 디제스트 메일):
  규칙은 **`research-agent/CLAUDE.md`** 다. 2026-09-09 에 이 파일에서 분리했다 —
  여기 있는 동안 상대경로 10개가 repo 루트에서 안 풀렸고 "이 폴더는 논문 에이전트다" 가
  이 계산 캠페인 repo 를 가리켰다.
  ⚠ 위 §litdb 의 *"논문 에이전트 요청 = litdb-curator"* 와 **이름만 같고 다른 것**이다.
