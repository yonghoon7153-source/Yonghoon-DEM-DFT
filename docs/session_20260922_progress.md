# 세션 진행 2026-09-22 (압축 전 대피소)

> 규율 ③ — 오늘의 수치·판정을 압축에서 지키려고 쓴다.  정본은 각 절이 가리키는 곳이다.

## ① 인계 검증 (`docs/handoff_review_20260922.md`) — **수용**, 1저자 비준 09-22

- 범위 `984874f8d..5b6433f9a` **153 커밋 · 360 파일** 재현 · 조상 YES.
- 두 레인 `check_all.sh --selftest` **RC 0** · `check_all.sh` **RC 0** (파이프 없이 파일로 받아 RC 채집).
- `--ban-sweep` 누수 0 · 원장 자기일관 ✓ (범위 안 등재 76 · open→claimed_fixed 10 · **open 126/328**).
- 셀프테스트: `make_mixer_deck` 84/84 · `phase_a_order_verdict` 23/23 · `phase_a_arms_from_payload` ✓(경계 계약 포함)
  · 추가 `phase_a_receipt_from_sh` 33/33 · `phase_a_preflight` 17/17 · `lhs_harvest_batch` 16 ·
  `measure_mixing_index` 10/10 · `check_contact_validity` 8/8.
- Phase A 한정어 세 줄 — prereg §0·§2 와 판정기 `phase_a_order_verdict.py:17-27, 259-263` 원문에 그대로:
  (i) estimand 는 **순서**뿐 (ii) 증분 % 는 **기술 보고 전용** (iii) QC 는 vox 0.15 · 1 wt% **한 셀**.
- §7 여덟 건은 **열린 채로** 인수.  §7 #6 (Table S3) 은 소스로 모집단 불일치 **확인**:
  분자 `_p998e` = `field_point_cloud(sid ∈ {1,2,3,4,5,7,8})` 도체 복셀 `|J|` 의 99.8 백분위
  (`mpm_webapp_payload.py:1941`), 분모 `_jm_e = sigma_eff/L` 전 단면 거시 (`:2011`).  계산은 payload 부재로 미실행.

### 비준된 셋 (보고 → 설명 → **비준 09-22** → 실행)
| # | 항목 | 상태 |
|---|---|---|
| C-1 | 믹서 층상 사전등록 §2 **판정선 8 칸 미기입** 인 채 13 런 발사 — 완주(~5 일) 전에 R-3·R-4 결정 + §2 기입 + prereg 헤더(*"결정 전에는 띄우지 않는다"*) 정정 | ⬜ **저자 결정 R-3 · R-4 대기** (내용이 저자 판정이라 대신 못 채운다) |
| C-2 | Phase A ORDER-ROBUST 정본 산출물(`verdict_20260921.json` · 영수증 v015/v020/v025 · 104팔 어댑터 JSON)이 **uma 에만** 있다 → `docs/data/phase_a_104arms_20260921/` 로 커밋 | ⬜ 파일이 uma 에 있어 이 컨테이너에서 못 옮긴다 — 아래 명령으로 저자 기계에서 |
| C-3 | `CLAUDE.md` 상단 현재상태 표 3 행이 09-18 에 멈춤 | ✅ 09-22 갱신 (Phase A 판정 완료 + 한정어 · Lee 침대 2/2 · LHS 130/130 · 믹서 행 신설 · 원장 126) |

C-2 명령 (uma → git 이 있는 기계):
```
scp -r uma:~/runyourai/1/pa/verdict_20260921.json uma:~/runyourai/1/pa/receipts/ uma:~/runyourai/1/pa/arms104/ \
    docs/data/phase_a_104arms_20260921/            # 실제 경로는 uma 의 `~/pa_watch.sh` 가 찍는 것을 따른다
python3 scripts/phase_a_order_verdict.py docs/data/phase_a_104arms_20260921/arms/ --json /tmp/v.json   # 재판정 = 커밋된 것으로 같은 답이 나오나
```

## ② ⛔ 믹서 `E0_s32452843` 죽음 — 원인 확정: **실행 중인 덱을 `gen_all.sh` 가 제자리 덮어썼다**

워치(09-22 09:49): `E0_s32452843 ⛔죽음 step 385337 100 % 덤프 385 … ERROR: Unknown command: z radius (../input.cpp:259)`.

**바이트로 증명한다** (이 컨테이너에서 두 세대 생성기로 같은 덱을 다시 만들었다):
- 60f684a71 판(체크포인트 전) `E0 --seed 32452843 --revolutions 0` 덱 = **6,917 바이트**.
- b6d9a2036 판(현행) 같은 덱 = 7,779 바이트 (+862: `restart` 주석 블록 728 B 가 dump 줄 **앞**에, `write_restart` 134 B 가 뒤에).
- 현행 덱에서 dump 줄 꼬리 `… fx fy fz radius` 의 **`z radius` 가 정확히 6,917 번째 바이트**에서 시작한다.
- LIGGGHTS 는 입력을 **읽어 가며** 실행한다.  옛 덱을 끝까지(6,917 B) 읽고 실행한 뒤(두 정착 `run` + `fix mv*` + `run 0`
  = 스텝 1 + 192,668 × 2 = **385,337** ✓) EOF 자리에서 다음 읽기를 했는데, 그 사이 `gen_all.sh` 재실행이 **같은 inode 를
  잘라 새로 썼기** 때문에 오프셋 6,917 부터 새 파일의 바이트 = `z radius` 가 명령으로 들어왔다.
- 워치의 `tot`(현재 `in.mixer` 의 `run` 합) 이 385,337 로 옛 궤적과 같은 것도 이 그림과 맞는다 — 덱 물리는 동일, I/O 줄만 다르다.

⇒ **물리는 끝까지 돌았다.**  잃은 것은 `Total wall time` 표지와 (옛 덱엔 애초에 없던) `settled.bin` 뿐이다.
`measure_mixing_index.py --ref` 는 *"스텝 ≤ 2·steps_fill 인 마지막 프레임"* (`_t0_frame`) 을 쓰므로 `post/mix_385000`
(정착 끝 337 스텝 전 = 0.24 ms) 이 **그대로 기준 프레임**이다.

⚠ 같은 위험이 **지금 도는 12 런 전부**에 있다: 실행 중에 `gen_all.sh` 를 다시 돌리면 각 런이 마지막 `run` 뒤 첫 읽기에서
같은 방식으로 죽는다 (측정 런은 5 일 뒤 마지막 줄에서).  ⛔ **런이 살아 있는 동안 `gen_all.sh` 금지.**

### 다시 시도 (1저자 "다시 시도" 09-22) — 권고 절차
1. 옛 것을 **보존**한다 (덮어쓰지 않는다): `mv runs/E0_s32452843 runs/E0_s32452843_old_20260921`.
2. 그 하나만 새로 만든다 — `gen_all.sh` 는 13 개를 전부 다시 쓰므로 **쓰지 않는다**:
   ```
   d=dem_scripts/mixer_20260921/runs/E0_s32452843
   python3 scripts/make_mixer_deck.py --out "$d" --n-total 100000 --cgf 151.4 --arm E0 --seed 32452843 --revolutions 0 > "$d.gen.log"
   cp dem_scripts/mixer_20260919/{Drum,Front,Back}.stl "$d/"
   grep -oE 'N=[0-9,]+' "$d.gen.log" | head -1 | tr -d 'N=,' > "$d/n_expected"
   grep -oE 'R +[0-9.]+ mm' "$d.gen.log" | head -1 | awk '{printf "%.6f\n", $2/1000}' > "$d/r_container"
   MAXJ=13 bash dem_scripts/mixer_20260921/run_all.sh      # 살아 있는 12 + 이것 = 13, 나머지는 "이미 실행 중"으로 건너뜀
   ```
3. 끝나면 **공짜 결정론 검사**: `cmp runs/E0_s32452843_old_20260921/post/mix_385000.liggghts runs/E0_s32452843/post/mix_385000.liggghts`
   — 같은 바이너리·같은 시드·직렬이라 **바이트 동일**이어야 한다.  다르면 그것이 더 큰 발견이다.

### ⬜ 생성기 수정 제안 (비준 대기 — 코드라 손대지 않았다)
`gen_all.sh` 에 두 가지: ⓐ `pid` 가 살아 있거나 `log.lmp` 가 있는 디렉터리는 **건너뛴다** (`FORCE=1` 로만 강제)
ⓑ 덱을 `"$d.new/"` 에 만들고 `mv` 로 바꿔 넣는다 (rename = 새 inode ⇒ 실행 중인 프로세스는 옛 inode 를 계속 읽는다).
런북 지뢰 표에도 한 줄: *"LIGGGHTS 는 입력을 읽어 가며 실행한다 — 실행 중 덱 덮어쓰기 = `pip` 를 런 중에 도는 것과 같은 사고"*.

## ③ uma — Lee 절대 대조 침대 **2/2 완주** (`VGCF_PTFE_3_1`, mach 0.01 · frames 7500, 09-22 03:26 KST)

- payload 요약: porosity 14.8 % · SE/solid 33.8 % · **thickness 121.7 µm** · 1,498 AM · `econn 100 %` · 입력 digest `5b8911a6efe11e6f`.
- 두께 121.7 = 침대 1/2 (`VGCF_PTFE_3_0.5`, 121.703) 과 같다 — PTFE 0.5 ↔ 1 에서도 **`씨앗 × λ` 두께 항등식**(CL-85) 그대로.
- ⚠ 이 킷 런의 STEP3 는 **vox 0.4 미리보기**(3.3 M dof · 이온·열·STEP4 까지 전부, LEAN 미적용) — Lee 대조에 **쓰지 않는다**.
  대조는 다음 단계 **STEP3 16 팔** (vox 0.15 × origin 8 × 두 침대 · `LEAN=2` · `PTFE_STAMP=centerline` · `--step3-require-gpu`).
  σ_e 는 `[봉인 — --show-results 로 열림]` 으로 가려져 나왔다 = 봉인이 제 일을 했다.
- ⚠ 관찰 (판정 아님): coverage AM_P **plastic 33/62 % vs rigid 55/80 %** — plastic 이 rigid 보다 **낮다** (Δ −22/−18 %p).
  정본(`docs/mpm_coverage_plastic_vs_rigid.md`)은 plastic 증분이 **양**이라 적는다 (real_14 52/74 vs 46/70).  그런데 요약 라벨은
  `Δ +-23/+-18 = plastic conforming` 이라고 **부호가 음수인데도 "conforming"** 을 찍는다 — 라벨 문자열이 부호를 안 본다
  (규율 ⑤ 부류의 표시 결함 후보).  σ_e 판정에는 안 쓰이는 값이나, 침대 1/2 의 같은 두 수와 나란히 놓고 확인할 것.
- pore-τ `no_through_component` · closed-from-top 99.95 % 는 DR3-07/08 그대로 (인용 금지 값 계산 안 함 = LEAN 의 이유).
