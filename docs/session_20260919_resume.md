# 복귀 프롬프트 — 2026-09-19 (압축 대비)

브랜치 `claude/stoic-knuth-NObVQ` · 게이트 양 레인 rc=0.

⚠ **구속 조건** (압축돼도 살려야 한다)
- 작업 브랜치는 `claude/stoic-knuth-NObVQ` **뿐**.  WSL 의 worktree = `~/dem-web`.
  ⛔ `~/Yonghoon-DEM-DFT` 는 **friendly 체크아웃**이다 — 거기서 pull/switch 금지.
  (2026-09-19 실측: friendly 위에서 stoic-knuth 를 pull 하려다 git 이 divergent 로 막았다.
   그 오류가 **가드가 문 것**이고, 힌트대로 `pull.rebase` 를 설정했으면 섞였다.)
- litdb 정본은 `origin/claude/friendly-meitner-lldvar` 의 `litdb/` — **읽기만**.
  중복 확인은 INDEX 가 아니라 `git ls-tree FETCH_HEAD litdb/papers/ --name-only`.
- 커밋·PR·코드 주석에 **모델 식별자 금지**.
- `bash scripts/check_all.sh` 는 **절대 파이프하지 않는다**.  커밋 전 `--selftest` **와** 무인자 둘 다.
- 부분 삽입으로 끝난 LIGGGHTS 런은 통째로 폐기.
- **1.2 배출 하한은 근거 있는 하한이지 충분조건이 아니다** — 그 한정어를 지우지 말 것.
- **dft 계열은 범위 밖** (`GAP3-21` · `GAP3-22`).
- 사용자 운영 규칙: **보고 → 설명 → 비준 → 실행.**
- ⛔ 덤프 짝 스텝을 `ls | tail` 로 고르지 말 것 — 사전순이라 `995000` > `3560000` 이 된다.
  `sed 's/.*_//' | sort -n | tail -1`.

---

## 1. 2026-09-18~19 에 닫은 것 (9건)

| 원장 | 무엇 |
|---|---|
| `GAP3-41` | 조상 검사 타임아웃 fail-open 을 셋(조상/미도달/판정불가)으로 가름 |
| `PASL-05` | `_code_sha` 가 dirty 탐침 지연에 SHA 까지 버렸다 (git status 실측 23.1 s vs timeout 20) |
| `GAP3-DOC` | 7건 중 여섯은 이미 고쳐져 있었고 **원장만 낡아** 있었다 |
| `GAP3-18` | `porosity_close.py` 의 **사후 래칫** 제거 |
| `PASL-06` | 사전등록 §8-1 이 **폐기된 도구**의 실행 절차를 적고 있었다 |
| `PASL-04` | ★ 근본 원인 — 선언이 축과 함께 침묵했다.  **길목**에서 막음 |
| `PASL-03` | 출처 없는 배치가 어댑터를 그냥 지나갔다 (이중 fail-open) |
| `PA12-07` | 판정기가 **QC 전수를 요구하지 않고** primary 중복을 파일명 순서로 골랐다 |
| `GAP3-42` | (A) 계약 한정 · (B) 산출물 배너 — **측정만 남음** |

### 살려야 할 수치·판정

- **`GAP3-18`**: 정당화 클래스(코너·SE-rich) **36건**을 클래스로 빼면 LOOCV **0.583 → 0.516
  으로 내려간다**.  옛 코드는 그 36 중 지표를 올려 주는 **한 건만**(`input_1mAh_9_S1`,
  0.583 → 0.603) 골라 뺐다 ⇒ 기준이 물성이 아니었다.  **보고 수치는 안 움직인다**
  (정본 헤드라인이 애초에 트림 전 `n=129 · 0.583`).
- **`PASL-04`** 기전: `sdcp_gain_vox015_8arm.sh:688` 이 `[ -n "$PS_FLAG" ] && XP=…` 로
  **조건부** 선언이라, 셸에 `PTFE_STAMP` 이 없으면 플래그도 안 붙고 **선언에서도 빠졌다**.
  ★ `resolve_ptfe_stamp` 의 둘째 반환값(`legacy`)이 *"말한 값이냐 유도한 값이냐"* 를
  이미 알고 있었는데 **대입만 되고 소비처가 0** 이었다.
  ⚠ **남는 한계**: `CONTRACT_SEALED_AXES` 는 아직 **손목록**이다 (사전등록 §5 를 안 읽는다).
  길목은 *"선언했는가"* 만 강제하고 값 대조는 어댑터 소관.  **축이 늘면 손으로 늘려야 한다.**
- **`PASL-03`** 면제 규약: `--code-sha-missing-ok "<이유>"` (이유 필수) →
  요약에 `code_sha_status: "MISSING — <이유>"` 도장.  정상은 `SEALED`.  불필요한 면제도 거부.
- **`PA12-07`**: QC 를 `(조성, vox)` 로 묶어 `n_origin` **전수** 요구 · primary 중복 거부.
  ⚠ **등록 밖 게이트가 아니다** — §1 이 `QC × 8 origin` 을, §2 가 셀당 팔 하나를 등록했다.
- **ρ 탐침 실측 (2026-09-19, WSL `~/lhs_local`, 127 케이스)**:
  `lhs00_000` electronic **6.7 s**, `ρ(조임)=3.186e-06 %` · **`ρ(치환)=2.571e-08 %`**,
  경로 `['cg']` — **반복해 1 · 직접해 0**.
  ★★ `GAP3-42` 의 전제 *"spsolve 30/30 전부 직접해"* 와 **어긋난다** (n=1, 전수 필요).
  ★ 치환 프로브가 **작동한다** ⇒ 전자 채널 ρ 증서를 낼 수 있다.

---

## 1-B. 2026-09-19 (밤) 에 **끝난** 것 — 코호트·수확 트랙 닫힘

| | 결과 |
|---|---|
| 코호트 | **RAW_OK 130** · `gap≠0` **0건** · 빈 지문 0 |
| 전수 수확 | **130 / 130 성공** (`--verify-sha`, 한 런) |
| 산출물 | `docs/data/lhs_descriptors_20260919/` — 케이스 130 + `_batch_summary.json` |
| 원장 | `LHS-07` 신설·수리 (P1) |

★★ **`LHS-07` 이 오늘의 가장 큰 건이다** — 봉인기(`gap ≤ 5000`)와 수확기(`gap ≠ 0`)가 **같은 축에서
반대 계약**을 써서 `RAW_OK` 129 중 **62 (48 %)** 가 원리적으로 수확 불가였다.  ⚠ **어느 쪽도
단독으로는 틀리지 않아 각자 초록**이었고, 파일 하나씩 보는 전수감사는 계약 **사이의** 모순을
원리적으로 못 본다.  ⇒ 그래서 수리를 **길목**과 **돌연변이 시험**으로 한다.

★ 검증: `lhs00_000` 이 이제 `timestep 2,420,000` (contact 와 짝 맞은 프레임).  재봉인 전에는
atom 2,425,000 을 가리켰다.

★ **경위를 별도 파일로 뺐다** — `docs/data/area_s2_cohort_provenance.md`.
`seal_area_cohort.write_tsv` 가 헤더를 **자동 생성**해서 재봉인마다 손기록이 사라졌다
(하루에 **두 번** 잃었다).  이제 헤더에 **포인터 한 줄이 자동으로** 박히고, 그 줄이 빠지면
selftest `★⑨h` 가 빨간불을 낸다 (돌연변이로 확인).

★ **이 130개는 결함 경로에서 나온 것이 아니다** (사용자 질문에 대한 답, 증거로 확인):
`lhs_descriptor_harvest.py` 는 `numpy` 와 `lhs_perc_extract` **만** import 하고 나머지를 자기가
구현한다.  `DESC-01`~`06` 이 겨누는 `dem_analysis_core` · `analyze_contacts` · `plastic_coverage` ·
`parse_liggghts` 를 **하나도 안 쓴다**.  오히려 `DESC-06` 은 수확기가 `:403` 에서 **강제**하는
쪽이고, 안 지킨 것이 봉인기였다.
⚠ 남은 `DESC-07`·`08`·`09` 는 그 숫자를 **쓰는 쪽**의 결함이라 `LHS-02` 를 닫을 때 같이 봐야 한다.

---

## 2. 지금 당장 할 일

### (가) Phase A 96팔 — v100 에서 진행 중
- 끝나면 **v015 팔당 실측 시간**이 나온다.  **QC 8팔 = 그 × 8**.
- QC 는 `VGCF 1 wt% @ vox 0.15` · origin 0~7 의 **exact replay** (출력 경로만 다름).
  계획기 `q_v1_o{i}` · 판정기 selftest 둘 다 `w=1.0`.
- 어댑터: `--code-sha-missing-ok "대역 밖 봉인 — docs/reviews/phase_a_seal_breach_20260918.md §5"`
  (박스 코드가 옛것이라 `code_sha=null` 로 나온다 — `PASL-05`).
- ⚠ **QC 없이 판정하면 `HOLD`** 다.  이제 **8 전수**를 요구한다 (`PA12-07`).

### (나) 코호트 증보 — `lhs00_034` · `lhs00_089`
TSV `docs/data/area_s2_cohort.tsv` `:49` · `:104` 에 행은 **이미 있고** `RAW_OK` 인데
`atom_sha256` · `contact_sha256` 가 **빈칸**이라 `--verify-sha` 가 `NO_SEAL_SHA` 로 건너뛴다.

**ibb 기준 지문** (2026-09-19 실측):
```
034 atom_3560000     ad8041675ad79ddfa4d2776a88f64802affea017ad7f38062f227484e4ad96a3
034 contact_3560000  08818556c0711ee941ba0466a63d8b64ab668bbbd3b2485c8b77762c83544d93
089 atom_2855000     b775db1c616dbd2096e83abbb1bb4f35221b39f03d2fbc92d8061f7e6170b362
089 contact_2850000  670ed92b061b17e2362e710fd72c1c924586e091d9f60e8d897b11b94bf8f4ea
```
⛔ **WSL 에 파일이 없다** — 전송 필요.  ibb = `ssh -p 43612 yonghoon@166.104.39.171`
(⚠ `scp` 는 **`-P`**).  ibb 의 `lhs` 경로가 `~/lhs` 가 **아니다** — `pwd` 로 확인 필요
(`find /data /home /scratch /work -maxdepth 6 -name lhs00_034` 가 빈손이었다).
전송 후 **양쪽 sha256 이 일치**해야 봉인한다.  덱 기대값:
`034 93dcfca7f70c43b0…` · `089 141a581d0fccfe24…`

### (다) `lhs00_098` — 130 번째
`r5` 진행 중.  **relaxation 시작 스텝 = 3,110,000** (`logs/output_lhs00_098_r5_191415.out:792`).
속도 ≈ **125 step/min** (watcher 2점).  종료 스텝은 덱의 PHASE 4 `run` 값 + 3,110,000.
완주(`sacct` State=COMPLETED) 후 034·089 와 같은 절차 ⇒ RAW_OK **129 → 130**.

### (라) `GAP3-42 (B)` 전수 ρ — **분 단위**
```bash
cd ~/dem-web
nohup ~/Yonghoon-DEM-DFT/venv/bin/python3 scripts/measure_rho.py \
    --webapp ~/lhs_local --deck-dir ~/lhs_local \
    --channels ionic,electronic,thermal \
    --out-csv /tmp/rho_full.csv --out-json /tmp/rho_full.json > /tmp/rho_full.log 2>&1 &
```
★ 볼 것 셋: ① 전자 채널의 **경로 분포**(`cg` vs `spsolve`) ② `rho_pct_max_permutation`
이 수로 채워지는가 ③ `ρ > 3 %` 채널이 있는가.
⚠ 실패 1건이라도 있으면 도구가 집계를 **발행하지 않는다** (rc=3).

---

## 3. 원장 상태

`docs/reviews/findings.json` — open **113** (P1 49 · P2 62 · P3 2).
그중 **리포 안에서 닫히는 것 93건** · 데이터/GPU 필요 12 · 참조불명 11.

### 남은 Phase A 사슬
- `PASL-01` (96팔 봉인 이탈) — 재실행 완주로 닫힌다
- `PASL-02` (LEAN=2 미적용) — 같음
- `PA12-04` (조성 교차확인 비독립) — **진짜 독립 확인은 계산기 밖 소스 번들 해시**, 아직 없다

---

## 4. 오늘 배운 것 — 압축해도 남길 두 줄

**① 실행이 판정을 두 번 뒤집었다.**  `phase_a_plan.py` 의 낡은 브리지 상수를 보고
*"격자마다 다른 브리지를 낳는다"* 고 P1 을 보고할 뻔했는데, 돌려 보니 그 파일은 폐기·
fail-closed 라 **아무것도 안 낳는다**.  `measure_rho` 의 거짓 0 도 *"코드 결함"* 으로
잡으려 했는데 코드는 이미 고쳐져 있었고 **파일이 낡은 것**이었다.
⇒ 소스만 읽고 판정하지 말 것.

**② 내 시험이 두 번 빈 시험이었다.**
· `_strip_sha` 가 엉뚱한 자리를 지워 **code_sha 가 안 지워졌는데도** 다른 게이트가 죽여 ✓.
  `neg()` 는 *SystemExit 이 났는지*만 보고 **어느 이유인지는 안 본다** → `neg_msg()` 로 교체.
· `verdict()` 에 리스트를 직접 넘겨 **파일명 정렬을 안 타** 깨진 코드에서도 PASS.
  → 실제 파일 + `load_arms` 로 다시 씀.
⇒ **초록이 나오면 "변이를 줘도 초록인가"를 먼저 물을 것.**

---

## ★★ 130 수확 요약 — **지금 낼 수 있는 것과 없는 것** (2026-09-19 밤)

| 양 | n | min | 중앙 | max |
|---|---|---|---|---|
| `phi_se` | 130 | 0.0433 | **0.1882** | 0.4164 |
| `phi_am` | 130 | 0.2622 | **0.3694** | 0.5149 |
| `coverage_AM_total` % | 130 | 2.44 | **21.43** | 50.01 |
| `coverage_AM_P` % | 100 | 2.31 | 22.11 | 49.17 |
| `coverage_AM_S` % | 100 | 2.53 | 23.75 | 50.05 |

★ `closure_residual` **130 건 전부 0** (φ 닫힘 정확).
★ `coverage_AM_P/S` 의 n=100 은 결손이 아니라 mono 설계 30 건의 `N_A_PHASE_ABSENT` = **정상**.

⛔⛔ **τ 는 130 중 14 에서만 나온다** (`NOT_PERCOLATING` 116).  SE 부피분율로 설명 안 된다 —
OK 최소(0.1860)보다 SE 가 많은데 미관통인 케이스가 **53** 건.  ⇒ **`LHS-08` 로 등재**.
⚠ *"89 % 가 미관통"* 을 **결론으로 쓰지 말 것** — 의심 신호다.
⇒ 먼저 `NOT_PERCOLATING` 의 **두 원인(ⓐ 전극 밴드가 빔 / ⓑ 진짜 미관통)을 가르는 status** 를
  넣고 재측정한다.  GPU 불요, 원자료는 사용자 기계에 있다.

---

## ★ 내일 (2026-09-20) — 사용자 지시

1. **MPM 보기**
2. **이종기술 해체 분석** — 업로드된 20분 회의록(`81f54418-___333.txt`, 2026-09-18)을
   타임별로 낱낱이 해체해 **webapp 별도 페이지 + DB화**.
   ⬜ **비준 대기**: **(가)** 61 발화 전수에 `raw`+`decoded`+`claim` / (나) `raw` 전수 + 선택 해독(~35).
   ★ 내 권고는 **(가)** — 선택 해독은 "무엇을 안 골랐나" 가 기록에 안 남는다.
   ⚠ 기존 `webapp/templates/hetero.html` (`/hetero`, 커밋 `6c13f19c8`) 이 이미 있으니 그 옆에 붙인다.

### 그 전에 정리돼 있어야 하는 것
- `LHS-02` 닫기 — 설계 CSV 의 빈 측정 3열을 `docs/data/lhs_descriptors_20260919/` 로 채운다.
  ⚠ `DESC-07`(7열을 7 독립 회귀로 세면 안 된다) · `DESC-08`(291 코퍼스와 그대로 합치면 안 된다) ·
  `DESC-09`(미실행 8개는 무작위 결측이 아니다) 를 **같이** 처리한다.
- **Phase A** — 96팔이 v100 에서 진행 중.  완주하면
  `phase_a_arms_from_payload.py --code-sha-missing-ok "대역 밖 봉인 — seal_breach §5"` 로 어댑터,
  그 다음 `phase_a_order_verdict.py`.  ⚠ **QC 8팔 미실행이면 `HOLD`** 다 (이제 8 전수를 요구한다).
- **ibb** — `lhsx_` 7잡 5코어 · `040` 11코어 · CPU 60/60.  `ps_` 는 **건드리지 않는다**.
