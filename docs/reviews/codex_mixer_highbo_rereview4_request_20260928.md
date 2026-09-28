# Codex 5차 리뷰 요청 — 믹서 고-Bo 확장 LH (4차 HOLD 해제 목록 반영, 2026-09-28)

- 브랜치 **`claude/sdcp-dem-manuscript-si-pqwtv8`** (= `claude/stoic-knuth-NObVQ` 의 fast-forward 연장 — stoic-knuth 로 되돌려 합치는 것은 1저자 비준 뒤) · 고정 스냅샷 = **§0 의 수정 커밋**.
- 4차 판정문 = `docs/reviews/codex_review_mixer_highbo_round4_20260928.md` (HOLD · HBR4-01 ~ 08 · Q1 ~ Q5) · 증거 = `docs/reviews/codex_mixer_highbo_round4_evidence_20260928/`
  (우리가 핀 `ba33a4939` 의 blob 과 `sources.json` 18/18 일치를 확인).
- 사전등록 = `docs/reviews/mixer_highbo_prereg_20260927.md` §2-2 · §2-4 (⛔⛔ 4 차 수정 블록) · §2-5 · §8 · §12 (새 행 다섯).
- 이번 수정은 **반례를 셀프테스트로 먼저 옮겨 옛 코드에서 실패 (= 결함 재현) 를 확인한 뒤** 고쳤다 — 검사기 11 건 · 생산자 3 건 · 런처 9 건.
  시뮬레이션은 돌리지 않았다.  **문턱 1 % · Bo · seed · LC · 칸 규약은 바꾸지 않았다.**
- `HBR4-04` 는 판정문이 준 선택지 중 **(나) mesh-dump 판정 분기 비활성화** 를 1저자가 골랐다 (09-28).

## 0. 수정 커밋

수정 커밋 = **`999a5bf85`** (게이트: selftest 레인 · 리포 레인 둘 다 0).  원장 등재 (HBR4-01~08 → `claimed_fixed 999a5bf85`) 는 이 요청서와 같은 커밋이다.

## 1. 항목별 — 무엇을 바꿨고 어느 셀프테스트가 지키나

| 항목 | 수정 | 셀프테스트 (옛 코드에서 먼저 실패 확인) |
|---|---|---|
| HBR4-01 영수증 무결성 | 생산자: B 에도 shape · 유한성 검사 (비유한이면 `ab = inf`) · 봉인 파일 목록 = {두 덱 + 부분마다 벽 STL} **정확히** · run_status 덤프 해시 목록 = 실제 덤프 집합 **정확히** (빈 · 부분 거부) · 내보내는 지표 전부 유한 강제.  소비자: 봉인 목록 정확 · `dumps_n` = 실측 step 수 (> 0) · A↔B · 잔차 · 위치 경계 유한 ≥ 0 · 스키마 v2 만 | 생산자 ⑩ (B 전부 NaN) · ⑪ (빈 봉인) · ⑫ (빈 덤프 목록) · 검사기 ㉖b ×3 |
| HBR4-02 이식 전제 | 소비자가 **판정할 런의 발사 봉인** (`launch_record.json`, `launch_highbo.sh` 가 발사 직전에 씀) 을 읽어 바이너리 sha256 = 영수증 · 봉인 때 `in.mixer` · STL = 지금 파일 (없으면 미상 → 잇지 않는다 — 지금 파일을 해시해 채우지 않는다) · **운동 시계** (`motion_clock`: mover 생성 · 해제 step · read_restart · run 끝) 와 회전 시작 step = 이 덱 · **재개 흔적** (in.resume · post_pre_resume_* · restart/resume_from_*) 이 있으면 거부.  생산자가 운동 시계 · 회전 시작 (소비자와 같은 정의) 을 영수증에 남긴다 | 검사기 ㉗ (배너 같고 바이너리 다름) · ㉗b (봉인 없음) · ㉗c (시작 2001 ↔ 3001) · ㉗d (재개 런) · 생산자 ④b (A 덱 시계 = 캠페인) · ⑥ (봉인 둔 런은 수용) |
| HBR4-03 오차 예산 | 생산자: 허용한 형상 잔차 + 출력 반올림을 **거리** `pos_bound_m` = √3 · (잔차 + 반올림) (좌표별 최대 → 유클리드) 로 남기고, 각 경계 = 실측 + 해상도 (**합** — 옛 max 는 합성의 상한이 아니다).  소비자: 구간 극값에 ± u/r (상한 + · 하한 −) | 검사기 ㉘ (원 STL 0.95 % 가 +80 nm 경계로 TECH) · ㉘b (대조: 경계 0 이면 PASS) · 생산자 ⑬ (+80 nm 는 허용 안이라 통과하되 경계 ≥ √3·잔차) |
| HBR4-04 대체 기하 | **(나)** `MESH_DUMP_BASIS = False` — post_mesh/ 덤프는 판정 근거가 아니다 (있으면 `notes` 에만).  `mesh_dump_container` 함수는 (가) 를 세울 때를 위해 남기고 그 자체의 거부는 계속 시험한다 | 검사기 ㉙ (퇴화 Front → 이제 끝판 2 % 가 상·하한으로 REJECT) · ⑩c · ㉓~㉓d (근거 아님 · 회전 무관 끝판은 REJECT) · ㉓e (함수는 끝판 없는 덤프를 여전히 거부) |
| HBR4-05 발사 관문 (증서) | 판독기가 증서에 **출처 블록** (`provenance`: 판독기 sha256 · 규약 인자 전부 · 평가/기준 덱 sha256 · 판독 프레임과 E0 기준 프레임의 step · 파일명 · sha256 · 평가 런 발사 봉인 sha256).  `rest` 관문이 규약 = 등록 (16×16×4 · n_min 20 · x · r 0.013138) · 판독기 = 지금 리포 · run = 첫 시드 · 덱 = 첫 봉인 때 · 본 봉인 = 지금 봉인 · 프레임을 **첫 시드 폴더와 E0 폴더에서 다시 해시**해 대조.  mtime 은 참고로만 | 판독기 ㉖ · ㉖b (다른 폴더의 **실제** 판독은 다시 해시하면 어긋남) · 런처 HL④g (옛 봉인) · ④h (칸 규약) · ④i (다른 폴더 · 같은 이름 · 봉인 사본) · ④j (판독기 sha) · ④k (출처 없음) |
| HBR4-06 발사 관문 (덱) | 런처 `deckdiff` 가 `mixer_deck_diff.expected_deck('LH', 32452843)` (생성기 CLI 와 바이트 동일, 비교기 ㉒) 로 기대 덱을 만들어 **`--expect-deck`** 로 넘기고, 발사 봉인 `gate_deckdiff` 에 argv · 기대 덱 sha256 을 적는다 | 런처 **HL②e (대역 없음 — 진짜 비교기 · 진짜 생성 덱, 허용 다섯 CED ×2: 약한 호출 rc 0 인데 옛 런처는 받아서 발사 · 새 런처는 거부)** · HL②f (대조: 참 LH 덱 통과) · HL③b · ③c · ⑤b |
| HBR4-07 정지 기준 | 검사기에 **정지 벽 계약** (`static`): 창 전체가 회전 전 (모든 운동 fix 시작 ≥ 창 끝 → θ = 0 정확) · fresh (read_restart · 재개 흔적 없음) · 덱 = 기대 덱 (`--expect-deck`) · STL = 캠페인 원본 (`--stl-ref`) → 원 STL 로 판정.  step 포함 · 1 % 는 그대로.  ⚠ E0 는 봉인 이전 세대라 *"디스크 덱 = 실행 덱"* 은 `gen_all.sh` 덮어쓰기 가드에 기댄다고 출력에 적는다 | 검사기 ㉚ (꼭짓점 옆 0.5 % → 옛: TECH · 새: static PASS) · ㉚b (2 % REJECT) · ㉚c 음성 대조 셋 (STL · 덱 · 재개 흔적) · ㉚d (기대 덱 없으면 계약 없음) |
| HBR4-08 문구 | v09 표 머리 = *"SE–SE 목표 Bo_code (SE 관련 CED 행렬 요소는 팔 사이 고정)"* · 옛 문장 취소선 + 쌍별 Bo_eq (0.17551 · 0.13868 · 0.21244) · **v09 PNG 범례 확인 — LA · LC 의 AM–AM(+벽) Bo_code 와 L0 대조만 적고 SE 쌍 Bo 문구 없음** (고칠 것 없음) | — |

## 2. 설계 판단 — 동의 · 반대를 받고 싶은 것

**Q1 — 발사 봉인을 이식의 조건으로 삼은 것.**  영수증을 쓸 수 있는 런 = `launch_highbo.sh` 로 봉인 · 발사된 런뿐이다 (LH).  L · LC 는 봉인이 없고 재개됐으므로
영수증 경로가 **서지 않는다** → 벽은 상·하한으로만 판정된다 (`unidentified` 면 판정 없음).  이것이 3차 Q5 의 *"런별 상태 확인은 별도 증거"* 와 맞는가.

**Q2 — 위치 경계의 크기.**  `pos_bound_m` = √3 · (잔차 + 반올림).  09-28 WSL 실측 규모 (STL 6 유효숫자 · 드럼 ≈ 13 mm) 로는 ≈ 2.6 × 10⁻⁷ m = 입자 반경 (mm 급) 의 ≈ 0.03 % 다.
좌표별 최대를 √3 배로 부풀리는 것 (평면 법선이 대각일 때의 최악) 이 과하다면 법선별 투영으로 줄일 수 있다 — 보수적인 쪽을 골랐다.

**Q3 — E0 정지 계약의 입력 동일성.**  기대 덱을 **지금 생성기**로 만든다.  E0 가 생성기의 체크포인트 추가 (`b6d9a2036`, 09-21 13:13 UTC) **이전** 판으로 만들어졌다면 명령이
달라 *"덱 ≠ 기대 덱"* 으로 정직하게 거부된다 — 그때는 E0 를 만든 생성기 판 (git) 으로 기대 덱을 다시 만든다.  이 절차가 적절한가, 아니면 E0 덱 자체를 정본으로 등록해야 하는가.

**Q4 — mesh-dump (나) 의 범위.**  덤프를 **읽기는 하되** 근거로 쓰지 않는 대신 아예 열지 않는다 (`notes` 에 장 수만).  나중에 (가) 면 연결 검증을 세우면 `MESH_DUMP_BASIS` 로 되살린다.

## 3. 재현

```bash
python3 scripts/check_contact_validity.py --selftest    # 73/73
python3 scripts/mixer_restart_phase_test.py --selftest  # 26/26
python3 scripts/measure_mixing_index.py --selftest      # 34/34
python3 scripts/mixer_deck_diff.py --selftest           # 24/24 (변경 없음)
bash dem_scripts/mixer_20260921/test_launcher.sh        # 64/64 (HL②e 는 진짜 비교기 · 진짜 생성 덱)
```
4차 프로브 (`…_round4_evidence_20260928/review_round4_probe.py`) 는 옛 동작을 **기대**하는 assert 가 있어 새 코드에서는 그것들이 실패하는 것이 정상이다.

## 4. 실데이터 순서 (5차 GO 뒤) — ⬜ 는 아직 안 한 것

⬜ WSL `~/phase_v1` 에서 고친 도구로 `analyze` 만 다시 → **영수증 v2** 커밋 (LIGGGHTS 재실행 불요 — 봉인 · 덤프 · 로그는 그대로) ·
⬜ E0 세 개에 정지 벽 계약 (§2-4 ③ 명령) · ⬜ L 완주 → ⬜ 생산 덱 3 쌍 대조 (`--expect-deck`) → `launch_highbo.sh first` (봉인) → bin 0 스모크 증서 (출처 블록) → `launch_highbo.sh rest`.
⚠ 이 요청서가 **발송됐는지는 1저자가 확인한 뒤에만** 정본에 적는다 (`SELF-59`).

## 5. 추가 (09-28 오후, 발송 전) — **ibb SLURM 경로** (1저자 결정 · 한 번에 리뷰받기 위해 이 요청서에 합친다)

**결정** (사전등록 §0 Q5 · §2-5b · §3-2 · §12 새 행 넷): LH 세 시드를 WSL 직렬이 아니라 **ibb SLURM 20 코어 × 3** (`lmp_mpi`) 에서 돌린다 (마감).
Q4 (*"L 10 런 완주 뒤"*) 는 해제 — 그 근거였던 J8 은 WSL CPU 경합이었고 ibb 는 L 을 늦추지 않는다.  기계 · 바이너리 · MPI 분할 차이는 1저자 판단으로
**판정 차단 사유가 아니다** (결론 한정어로 붙인다).  문턱 · Bo · seed · LC · 칸 규약 · 관문 (덱 비교 · first/rest · 스모크 증서 · 출처 · 코호트) 은 **안 바꿨다**.

**바꾼 것** (전부 셀프테스트를 먼저 쓰고 옛 코드에서 실패 = 부재 재현 뒤 구현):
- `launch_highbo.sh` `BACKEND=slurm` — 러너 `<런>/run_lh.sbatch` (ibb 실물 형식 `docs/data/pure_se_*_20260927/run_pse_*.sh` 그대로: `#SBATCH -n N` ↔
  `mpirun --oversubscribe --bind-to none -np N` · qos · partition · 5 일 · conda) → 봉인 (`backend` · `slurm` 블록 = np · 플래그 · 러너 sha256 · 시작 대조기 sha256) → 런 폴더에서
  `sbatch --parsable` → `jobid`.  "아직 안 뜬 런" 에 `jobid` 없음을 더했다 (대기열에만 있는 job 은 `log.lmp` 가 없다 — 두 번 제출 방지).  로컬 경로는 그대로 (HL 64/64 유지).
- `dem_scripts/mixer_20260921/start_check.py` (새, 표준 라이브러리) — job 이 **시작할 때** 러너가 LIGGGHTS 앞에서 봉인을 다시 대조: 바이너리 realpath · sha256 · 덱 · STL ·
  **실행 중인 러너 자신** (`$0` = SLURM 사본) · 대조기 자신 · `SLURM_NTASKS` = np · `log.lmp` / `job_start.json` 없음.  통과 = `job_start.json` · 거부 = `job_start.refused.<job>.json` + exit 3.
- `check_contact_validity.launch_binding` — 봉인이 `backend: slurm` 이면 `job_start.json` (ok · 바이너리 · 실행된 러너 · 대조기 · 봉인 sha256 · ntasks) 이 봉인과 맞아야 영수증을 잇는다.
- `mixer_restart_phase_test.py` `run.sh` — `LMP_LAUNCH` 실행 접두사 (ibb: `mpirun … -np 1`, 비우면 옛 동작) · 봉인에 `launch_prefix`.

**시험**: `test_launcher.sh` **81/81** (HS①–⑦b 17 새로 — 가짜 sbatch · squeue · mpirun 으로 **러너를 실제로 돌려** 시작 대조가 덱 · STL · 러너 · 바이너리 · ntasks ·
SLURM 밖 · 두 번째 시작을 막는지) · `check_contact_validity.py --selftest` **83/83** (㉛ 10) · `mixer_restart_phase_test.py --selftest` **28/28** (⑭ 2 — 생성된 `run.sh` 를 실제로 돌린다).

**§S 질문 — 동의 · 반대를 받고 싶은 것**
- **S1 대기열 틈.**  Q5 의 *"실행 직전 봉인"* 을 SLURM 에서 **제출 때 봉인 + 시작 때 재대조** 로 대신했다.  재대조 목록 (위) 에 빠진 것이 있는가 (예: `mpirun` 자체 · conda 환경 · 노드).
- **S2 영수증 `-np 1` → 런 `-np 20`.**  영수증 A/B 를 같은 `lmp_mpi` 로 **`-np 1`** 에서 잰다 — 병렬 `dump mesh/stl` 은 삼각형을 프로세서 소유 순서로 써서 생산자의
  *"원 STL 과 꼭짓점 순서대로"* 대조가 서지 않기 때문이다.  처방 회전은 요소마다 같은 산술이라 분할과 무관하다는 **가정**을 등록했다.  이 가정을 받는가, 아니면
  `-np 20` 영수증 (삼각형 순서 무관 대조로 생산자 수정) 을 요구하는가.
- **S3 소비자의 `job_start.json` 잇기.**  SLURM 봉인에 시작 대조 통과 기록이 없으면 영수증을 거부한다 (실행 바이너리 미상).  충분한가, 과한가.
- **S4 짝의 기계 차이.**  LC (WSL 직렬 · 08-25 빌드) ↔ LH (ibb MPI 20).  1저자는 차단 사유가 아니라고 판단했다 (결론 한정어).  같은 시드의 병렬 `insert/pack` 이 직렬과
  같은 초기 침대를 주는지는 **확인하지 않았다**.  한정어 외에 요구할 것이 있는가.

**추기 (Q3 에 대한 사실)**: 생성기 `b6d9a2036` · `6963632a0` · `20568797b` · HEAD 네 판이 E0 세 시드에서 **바이트 동일**한 덱을 낸다 (7,779 B · sha256 앞 16 자리
`a38cdc7494671979` · `b8ba25ace11e1300` · `f38f0093433d251a`).  09-22 에 E0 를 다시 만든 판이 `b6d9a2036` 이므로 지금 생성기의 기대 덱 = 실행 덱으로 **예상**된다
(WSL 해시 대조는 1저자가 실행 중).

