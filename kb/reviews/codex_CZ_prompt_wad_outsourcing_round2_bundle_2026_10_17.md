---
title: "CZ 프롬프트 — W_ad 외주 2차 묶음 리뷰: 탄소 P2′ · C–C · 은 a4 VASP 묶음 (코드 · 러너 사다리 · 판정 계약 · 검사기·집계기 · 봉인) · 발송 승인 여부"
tags: [review, wad, adhesion, vasp, outsourcing, graphite, dipole, scf, runner, codex, prompt, letter]
letter: CZ
date: 2026-10-17
track: wad
channel: codex
kind: prompt
status: 발송 가능 — 봉인 · ④ UMA 단일점 · 실제 묶음 빌드 2026-10-22 (기준 커밋 8d41e4e0 · 묶음 MANIFEST 31e47474…) · 발송 전
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = W_ad (DEM 협업 · 1저자 = 사용자). CY (설계 · 조건부 GO · 최소 수정 여섯 묶음 뒤 빌드 · **발송 승인은 CZ**) 다음 편지다.
> ⛔ 점착 W 값은 kb 문서에 싣지 않는다 — 이 편지에도 W 숫자를 쓰지 않는다 (문턱 · 비율 · 벽시계만).
> 기준 커밋 `8d41e4e0`. ⬇ 아래 **보내는 글**만 발송한다. 회신이 오면 `codex_CZ_reply_…` 로 원문 보존.

---

**[W_ad · 외주 2차] 묶음 리뷰 요청 — 탄소 P2′ · C–C 대조 · 은 a4 VASP 묶음 (발송 승인 여부)**

## 0. 무엇을 묻나

CY 에서 설계를 고친 뒤 (카드 v2 · 개정 4 v2 · 1저자 비준 10-17 — 선택 2 + 80 % 발동 규칙 · 단계 누적 상한 1.5 배 · 전자 스텝 ≥ 1 뒤 충돌 = 실행 실패) 빌드를 마쳤다. 이번에는 **이 묶음을 업체에 보내도 되나** 를 묻는다 — 설계를 다시 열자는 것이 아니라, 설계가 코드·러너·검사기에 **그대로** 옮겨졌는지, 조용히 틀린 길이 없는지.

## 1. 지금 상태 (사실)

- 결정: `D-2026-10-15-wad-p2small-vasp-card` · `D-2026-10-15-wad-aprime-v5-e70-a4-rerun` (active · 비준 2026-10-17). 빌드 기록 `db/properties/wad_round2_build_log_2026_10_17.json`.
- ① 빌더 `tools/wad/build_aprime_interfaces.py --build P2S` (SE 2층 V5 절단 1×3 + 흑연 AB 2층 · registry A · 끝점 10 Å) · `p05_probe` · `check_rigid_shift` — selftest 75/75 · 일부러 깨기 11/11 빨강.
- ② 부모 둘 UMA+D3 이완 (kgy · fairchem 2.21.0 · 체크포인트 S1 결박값 · simple-dftd3 1.6.0) — 10-21 21:24 → 21:42 (S_A 12 분 · Li_A 6 분) · G1 S_A FIRE 894 스텝 fmax 0.0164 · Li_A 430 스텝 0.0192 eV/Å (문턱 0.02 · 3000 스텝 안) · G2 깃발 0 · 회수 커밋 `6d3538d9` (SHA256SUMS 13 줄 · 기계·레포·클라우드 일치) → 봉인 `tools/wad/build_aprime_s3.py --seal_p2s` (계보 · G1 · G2 · 계산기 결박 · p05 · S_A G3 세 구조 · 발송 전 D3 만 G3 예측 80 % 규칙) — selftest 41/41 · 깨기 12/12 빨강 + 아래 고침 깨기 3/3 빨강 · 봉인 커밋 `d640e8e7`. D3 만 예측: **끝점 10 Å 유지** — 80 % 문턱 (0.008 J/m²) 대비 검사 (i) 19 % · (ii) 30 % · 발동 안 함 (봉인 manifest `d3_g3_prediction`).
- 봉인 중 고침 (Q-CZ-9 에서 리뷰 요청) — 1차 봉인이 **G1p ③ 마스크 깃발**로 거부됐다 (S_A_p05 '고정 마스크가 정책 집합과 다르다 — 빠짐 0 · 남음 6' · Li_A_p05 '남음 3'). p05 탐침의 `interface_check` 가 마스크 정책 (기판 중심면 아래 · 동률은 '고정') 을 **이완된 부모로 만든 탐침**에서 다시 계산했다. 이완이 기판 위끝을 내려 (S_A 0.36 Å · Li_A 0.57 Å) 중심면이 옮겨졌고, 빌드 때 중심면 위에 정확히 놓였던 동률 S 원자 (S_A 6 · Li_A 3) 가 '남음' 이 됐다. 마스크 자체는 빌드 초기 구조의 정책 집합과 같다 (S_A 90 = 90 · Li_A 69 = 69 · 부모 G2 통과). 카드 G1p ③ 'G2 와 같다' 를 '기준 = 부모 빌드 초기 구조 (sha = meta)' 로 읽고 고쳤다 — `se_sym_slab.interface_check(policy_ref=)` (원자 수·순서가 다른 기준은 거부) · `build_aprime_interfaces.p05_probe(policy_ref=)` · `seal_p2s` 가 부모 빌드 초기 구조를 넘기고 manifest p05 에 `mask_policy_ref` 를 적는다 · 기본값 None = 옛 동작. 시험: se_sym_slab 122/122 · build_aprime_interfaces 75/75 · build_aprime_s3 41/41 (새 시험 = 가짜 이완에서 Li_A 맨 위 Li 를 0.6 Å 내려 정책 집합을 바꿔도 봉인 p05 깃발 0 · 실제와 같은 '남음' 꼴 재현).
- ③ 묶음 `tools/wad/build_round2_vasp_package.py` — 24 잡 (P 5 · 1 4 · 2 9 · 3 4 · 4 2) · 러너 (bash · 업체 쪽 python 가정 없음) · 검사기 · 집계기 · 등록부 봉인 · 해제 파일 — selftest 53/53 · 깨기 23 (1차 22 중 18 빨강 → 안 잡힌 넷에 시험을 더해 넷 다 빨강 · 그 과정에서 러너가 ISTART·ICHARG 를 OUTCAR 첫 줄에서 읽던 버그를 고쳤다 — INCAR 를 되울리는 빌드면 입력값을 실제값으로 읽는다). 실제 묶음은 10-22 에 봉인으로 빌드했다 (같은 명령으로 다시 빌드 = 바이트 동일 · 묶음 안 `sha256sum -c MANIFEST.sha256` OK · 쌍극자 구간 여유 = 위 원자·아래 영상 둘 다 5.0 Å).
- V5 도구 (개정 4): 시도별 NELM 을 검증된 INCAR 에서 읽고 · `adopt_a4` (부모 자격 · a4 OK 만 채택 · 이력 셋) · **실물 V5 반송 재검사·재집계가 저장본과 바이트 일치** · selftest 228/228.
- 묶음 MANIFEST.sha256 의 sha256 `31e4747450d154085b070f8c03936a2c4eb0b5b60962841bb022a0846f9ca61a` · P2′ 봉인 manifest sha256 `65a0ca0e376b3c67737399128bee753f506f8ae32122a5308d97ca8436dac2fe` · UMA 단일점 (④) — 10-22 kgy 봉인 구조 9 개 · 벽시계 16 초 · 결박 ✓ (fairchem 2.21.0 · uma-s-1p1 omat · 체크포인트 07068e9c76702ca1 · 행 9 = 봉인 sha) · `db/raw/wad_p2small_uma_sp_2026_10_17/` (회수 커밋 `eb48146b`). 결과 전에 돌려 묶어 두었고 **집계기에는 아직 안 넣었다** (집계는 반송 뒤 한 번).

## 2. 리뷰할 것

- 묶음 폴더 `db/inputs/wad_round2_vasp_2026_10_22/` 전체 (README · run_all.sh · jobs.json · STAGES.tsv · JOBS.txt · jobs/*/INCAR* · MANIFEST.sha256) · 봉인 폴더 `db/inputs/wad_p2small_seal_2026_10_17/` (p2s_seal_manifest.json · structures/).
- 코드: `tools/wad/build_round2_vasp_package.py` (빌더 · RUN_ALL · judge_text · check_attempt · resolve_job · collect · seal_registry · release_text · FAKE_VASP · selftest) · `tools/wad/build_v5_vasp_package.py` (adopt_a4 · NELM) · `tools/wad/build_aprime_s3.py` (seal_p2s) · `tools/wad/build_aprime_interfaces.py` (build_p2small · p05_probe) · `tools/wad/se_sym_slab.py` (interface_check · policy_ref).
- 카드 `db/properties/wad_p2small_vasp_card_2026_10_15.json` · 개정 4 `db/properties/wad_aprime_pilot_prereg_v5_amendment_4_e70_rerun_2026_10_15.json` · CY 회신 `kb/reviews/codex_CY_reply_wad_outsourcing_round2_design_2026_10_15.md`.

## 3. 확인 요청 (질문마다 GO / 조건부 / NO-GO 와 P0·P1·P2 로)

- **Q-CZ-1 (판정 계약)** — 러너 `judge()` (awk) 와 검사기 `judge_text()` (python) 가 같은 규칙·같은 순서인가 (selftest 는 탐침 26 개로 대조): ① 행 0 → 미확인 ② 스텝 번호·이온 요약 뒤 행 → 미확인 ③ N > 그 시도 INCAR 의 NELM → 미확인 ④ rc ≠ 0 · 미종료 → 실행 실패 ⑤ 실행 머리줄 ≠ 1 ⑥ OUTCAR 마지막 전자 반복 번호 ≠ N ⑦ 비유한 ⑧ |dE|·|d eps| ≤ EDIFF. 순서 (③ 을 ④ 앞에 · 구조 검사를 실행 실패 앞에) 가 맞나? 0 행 + rc ≠ 0 을 '실행 실패' 가 아니라 '미확인' 으로 둔 것 (카드 어휘: 실행 실패 = 유효한 전자 반복행 1 개 이상) 이 맞나?
- **Q-CZ-2 (사다리 · ⓐ 자격 · 재시작 확인)** — 다음 단 = 확인된 미수렴 · 실행 실패만 · ⓐ 자격 (정상 종료·유한 · WAVECAR 머리 RECL/NSPIN/RTAG 다음 레코드의 NKPTS·NBANDS·ENCUT = ⓐ OUTCAR · 복사본 sha) · 재시작 확인 = Startparameter 의 ISTART 1 · ICHARG 0 · 'WAVECAR not read' 없음 · src = 복사본 = ⓑ 끝 sha. VASP 5.4.4 는 WAVECAR 를 **읽었다는** 긍정 문구가 없는 것으로 보여 (실물 stdout 은 안 읽었을 때 'WAVECAR not read' 만) 긍정 문구는 파일럿 뒤 해제 파일 `restart_read_regex` 로 더하게 해 두었다 — 이것으로 'ⓑ 가 실제로 읽었다' 를 충분히 말하나? ⓐ WAVECAR 를 미확인·재시작 미이행·기록 없음에서 남기는 규칙 (0 스텝 중단 기록 뒤 이어 돌리기 · 1저자 검토 뒤 다음 단) 이 맞나?
- **Q-CZ-3 (단계 · 상한 · 해제 · 공통 환경)** — STAGES 기본 P · P 밖은 해제 파일 (sha) 필수 · 단계·전체 누적 상한 (attempt.json 벽시계 + 0 스텝 중단 기록) 을 **잡을 띄우기 전에만** 본다 (사다리 안 다음 단은 막지 않는다 — '돌던 잡은 끝까지') · 공통 환경 고장 (해제 뒤 PP 종별 sha · VASP 빌드 줄 · vdW 커널 sha · 파일럿부터 커널 없음) = 전체 정지 종료 6. 빈틈은?
- **Q-CZ-4 (0 스텝 인프라 중단)** — `--infra-abort <잡> <단> <스케줄러 id> <취소 UTC> <사유>` 는 전자 반복행 0 일 때만 · 잡마다 2 회 · 시도를 run_aborted/ 로 옮기고 다시 돌리면 같은 단부터 · 벽시계는 WALL_S 로 업체가 준다. 업체가 이 절차를 오용할 길 (예: 행이 있는 실패를 지우고 다시 돌리기) 이 막혔나?
- **Q-CZ-5 (optB88)** — INCAR (GGA = BO · PARAM1 0.1833333333 · PARAM2 0.22 · AGGAC 0.0 · LUSE_VDW · ZAB_VDW −0.8491 · IVDW 0 · D3 줄 없음) · 커널 신원 (러너가 잡 폴더에 복사하고 sha 기록 · 반송 금지 목록) · 되울림 판독 (PARAM1/2 · Zab_vdW · AGGAC · LUSE_VDW · 커널 읽기 문구) 은 **파일럿 원문으로 확정**하게 해 두었다 (없으면 SETTINGS_UNVERIFIED / KERNEL_UNVERIFIED — OK 아님). 5.4.4 에서 이 판독 줄이 실제로 무엇인지 알면 알려 주길.
- **Q-CZ-6 (집계)** — Δ_C = W_VASP − (W_UMA + ΔD3_VASP) · G3 (S_A · D3 차이의 차이 예산 0.001) · G4 세 단계 (k · σ · ENCUT · 같은 기하 Edisp ≤ 1e-4 eV) · G5_C 상태 순서 (UMA → 등록부 → 분모 → G3/G4 → FAIL → PASS) · 80 % 발동은 **기록만** (판정 불변) · δ 라벨 (s = max(0.01, S_A 등록 검사 |ΔW| 최대) · Li_A 는 0.01) · ②′ 는 두 방법 차이만 · 질문별 실패 전파. 카드와 다른 곳은?
- **Q-CZ-7 (far 진단 · 전하이동 신호 — 카드가 CZ 에 확인을 미룬 것)** — 신호 ⓐ |Δp_z| ≥ 0.02 e·Å (S_A far ↔ G3 far_ii) · ⓑ G3 (ii) PBE 몫 |ΔW_ii − ΔD3_ii| ≥ 0.001 J/m² 는 우리 제안이다. 문턱이 맞나? **파일럿 S_A far 하나에 LOCPOT 면평균 (LVHAR = .TRUE. · 1차원 텍스트만 반송 · awk 로)** 을 더할지 — 더하면 INCAR 가 바뀌므로 지금 정해야 한다.
- **Q-CZ-8 (은 a4)** — a4 입력 = V5 봉인 INCAR + 개정 4 차이만 (ⓐ LDIPOL F · LWAVE T / ⓑ ISTART 1 · ICHARG 0 · AMIN 0.01 · NELM 300) · POSCAR·KPOINTS·POTCAR.spec = V5 MANIFEST sha · 채택은 V5 검사기 (`--a4_result` sha 고정) · 등록부 봉인이 V5 등록부와 같은 빌드·같은 PP 가 아니면 거부. 빈틈은?
- **Q-CZ-9 (봉인)** — P2′ 봉인의 계보 (이완 시작 sha = 레포 초기 구조 = build_record) · 계산기 결박 (kgy fairchem 2.21.0 — S1 측정 기계는 gabia 2.19.0 · UMA_REQ 허용 목록에 2.21.0 · 체크포인트 sha 같음) · p05 가 부모 far 를 공유해도 되는 조건 (규칙이 탐침에 주는 c 가 같다 · 파일 왕복 강체 검사) · D3 만 예측 80 % 규칙의 실행 결과 (끝점 10 Å 유지 · 80 % 문턱 대비 (i) 19 % · (ii) 30 %). 그리고 **봉인 중 고친 G1p ③ 기준** (§1): 마스크 정책을 부모 빌드 초기 구조에서 재는 것이 맞나, 아니면 이완된 부모에서 다시 재고 동률 규칙을 바꾸는 것이 맞나? `policy_ref` 를 넘기는 길이 다른 검사 (부모 G2 · 강체 이동 검사 · 고정 원자 좌표 일치) 를 조용히 약하게 만들지 않았나? 기본값 None (옛 동작) 을 남긴 것이 다른 호출부에서 같은 거짓 깃발을 다시 낼 길은?
- **Q-CZ-10 (업체 지시 · 메타)** — README 대로 하면 업체가 의도와 다른 일을 할 수 있는 곳은? 이번에도 '제대로 돌렸나' 만 보고 '맞는 양을 재나' 를 놓치는 곳이 있나?
