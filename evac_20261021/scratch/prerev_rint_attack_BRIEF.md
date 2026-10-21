# Rint 조인 수정 사전 공격 리뷰 (공격 담당 · 읽기 전용 · 10-20)

너는 Codex 를 대신하는 **적대 검토자**다.  목표 = 이 수정이 Codex 에 가면 HOLD 를 받을 반례를 **먼저** 찾는 것.  고치는 사람의 설명은 일부러 주지 않는다 — 코드와 시험만 보고 판단한다.

## 대상
- 커밋 사슬 (로컬 · 원격에 아직 없음): `9845d526c` (기준) → `12d894c09` (시험 먼저) → `a2cfd0365` (수정) → `654385e4c` (문서).
- 코드 diff: `git -C /home/user/Yonghoon-DEM-DFT diff 9845d526c a2cfd0365 -- scripts/rint_iface_join.py scripts/test_rint_g2_join.py`
- 작업 자리: 너만 쓰는 분리 작업 트리를 만든다 — `git -C /home/user/Yonghoon-DEM-DFT worktree add --detach /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/wt_prerev_attack 654385e4c` · 끝나면 `git -C /home/user/Yonghoon-DEM-DFT worktree remove --force <그 경로>`.  탐침 · 임시 파일 = `…/scratchpad/prerev_attack/` 만.
- 근거 문서 (그 작업 트리 안): 계획 `docs/reviews/rimprr_fix_plan_20261020.md` §1 · §2 (Q1–Q4 = 무엇을 고치기로 했나) · Codex 판정문 `docs/reviews/codex_review_rint_join_rimpr_q7_recheck_20261020.md` (전부 · 특히 §3 · §4 · §6 · §7) · 그 앞 판정문 `docs/reviews/codex_review_rint_g2_impl_fix_recheck_20261015.md` (RIMPR-01 · 02 부류) · 원장 `docs/reviews/findings.json` 의 `RIMP-0*` · `RIMPR-*` 항목 · Codex 탐침 `docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/probes/` · 결과 `…/evidence/`.

## 할 일
1. 바뀐 함수를 **모듈 문맥 안에서 전부** 읽는다 (diff 만 보지 말고 호출자 · 피호출자까지).  `grep` 으로 조인 결과를 소비하는 자리 전부 (계획 · 정량 관문 · CLI · 저장된 기록 다시 읽기) 를 찾는다.
2. Codex 탐침 재실행 — 먼저 **전부 읽고** 네트워크 · 묶음 밖 쓰기 · 삭제 · 임의 subprocess 가 없을 때만 `prerev_attack/` 로 복사 · 경로 상수만 바꿔 `python3 -I -X utf8 -B` 로.  고친 트리에서 기대: 헤더 반례 10 = 거부 · 1e160 = 거부 · 전각 정수 = 거부 · 그 밖 판정 = Codex 가 리뷰 핀에서 기록한 것과 같음.  다르면 표에.
3. 지난 HOLD 부류로 반례를 **직접 만들어** 돌린다 (작은 합성 덤프 · 시험 파일의 도우미나 탐침의 생성기를 재사용).  각 반례 = 입력 · 결과 (PASS / 거부 · 사유 코드) · 기대:
   - **헤더 문법 같은 부류**: 소문자 표지 · `ITEM:` 뒤 공백 둘 이상 / 탭 / 공백 없음 · 표지 단어 사이 공백 둘 (`BOX  BOUNDS` · `NUMBER  OF  ATOMS`) · 유니코드 공백 (U+00A0 · U+2003 · U+3000 · U+200B 폭 없는 공백 · U+FEFF BOM) 을 표지 안 · 토큰 사이 · 줄 끝에 · CR 만 · CRLF 섞임 · `\x0c` · `\v` · 열 이름 중복 · 필수 열 결손 · 모르는 절 (`ITEM: UNITS` · `ITEM: TIME` — LAMMPS `dump_modify units/time yes` 가 실제로 쓴다: 받아야 하나 거부해야 하나 · 지금 동작이 의도인지) · 절 순서 바꿈 · 한 프레임 안 TIMESTEP 두 번 · 삼사정 `ITEM: BOX BOUNDS xy xz yz pp pp pp` (줄당 값 셋) · 상자 플래그 `mm` · `fs` · `sm` · `si` · atom 덤프와 contact 덤프의 `NUMBER OF ATOMS` ↔ `ENTRIES` 뒤바뀜.
   - **정상화 뒤 검사 부류 (RIMPR-R01 뿌리)**: 데이터 행 · 머리 줄을 `str.split()` 이 유니코드 공백으로도 자르는지 → 그러면 비-ASCII 구분자가 조용히 통과 (값은 같음) — 같은 부류로 Codex 가 지적할지 판단.
   - **수 토큰 같은 부류 (RIMPR-03 뿌리)**: 실수 토큰의 유니코드 숫자 (`１.５` · 아라비아-인도) · 밑줄 (`1_000.5` — `float()` 가 받는다) · `nan` · `inf` · `infinity` · `+nan` · `1e400` · `-0` · 앞 `+` · 아주 작은 수 (`1e-320`) · 6 유효숫자 `%g` 규칙이 있다면 7 자리 · 다른 표기 (`1.5e+00`) · `_STEP_RE` 등 `\d` 를 아직 쓰는 다른 정규식 전부 (grep).
   - **넘침 · 비유한 같은 부류 (RIMPR-04 뿌리)**: f5 위치 허용폭 inf (1.7e308 근처) · 상자 길이 `hi − lo` 넘침 · inf 상자 주기 감기 · `sim_to_um` 아주 크거나 작음 (면적 0 으로 언더플로 = 유한이지만 무의미) · 반지름 아주 작음 · 차의 제곱 넘침 (1e155) · 중간 inf − inf = NaN 이 `max(0.0, nan)` · `min` 으로 삼켜지는 자리 (파이썬 `max(0.0, nan) = 0.0`) · `-0.0`.
   - **빈 · 중복**: 원자 0 · 접촉 0 (설계상 허용) · 원자 ID 중복 · 접촉 (i, j) 와 (j, i) · 자기 접촉 (i, i) · 없는 원자 ID 를 가리키는 접촉 · ID 0 · 음수 · int64 넘침 · `NUMBER OF ATOMS` ≠ 행 수 · 마지막 프레임 잘림 · gzip 잘림 · gzip 여러 멤버 이어 붙임 · 빈 gzip.
   - **결합 · 판본**: 옛 판 (`JOIN_VERSION` v3) 조인 기록이나 결과를 새 계획 · 정량 관문에 넣으면 받는가 (다른 판본 증서 부류) · 조인을 다시 계산하지 않고 저장된 기록을 믿는 길이 있는가 · `join_gate_failed` 가 **모든** 소비 경로에 닿는가.
   - **고친 사람이 계획과 다르게 한 곳**: "표지로 시작하지만 경계 없음" 줄을 그 절로 읽고 따로 표시한다 — 표시만 되고 거부되지 않는 경로가 있는지.
   - **거짓 거부 위험 (똑같이 중요)**: 실제 LIGGGHTS 꼴 — `ITEM: ATOMS id type x y z ix iy iz vx vy vz fx fy fz omegax omegay omegaz radius` + 줄 끝 공백 · `pp pp ff` · `mm` 계열 · contact local 덤프 `ITEM: NUMBER OF ENTRIES` · `ITEM: ENTRIES c_…[1] …` · 탭 구분 · `%g` 값 (`1e-05` · `-0` · `5`) · 리포 안 real14 · case15 실자료 (시험이 쓰는 자리를 찾아서).
4. **시험이 옳은 이유로 통과하는지** — 새 시험 (J12 · J13 · J14 와 새 양성) 마다 거부 사유가 의도한 검사인지 (앞의 다른 검사에 먼저 걸려 통과하는 것 아닌지) 확인.  변이 시험: 고친 검사 하나씩 되돌린 사본 모듈 (`prerev_attack/` 안) 에 새 시험을 돌려 **실패해야** 한다 — 안 실패하는 시험 = 그 검사를 지키지 못함.
5. 판단 — 찾은 것마다: Codex 가 낼 등급 (P1 / P2 / P3 · 또는 지적 없음) · 같은 부류의 원장 ID · 최소 수정 + 시험 한 줄 · 또는 "요청서에 한정으로 적기" 권고.

## 규칙
- **리포 · 다른 작업 트리를 고치지 않는다 · 커밋 · push 하지 않는다 · `scripts/check_all.sh` 안 돌린다.**  분리 작업 트리 안에서도 파일을 고치지 않는다 (변이 사본은 `prerev_attack/` 에).
- 다른 에이전트가 돈다 — 수천 번 반복 · 몇 분 넘는 전수 탐색은 하지 않는다.
- 보고 (한국어 · 표 중심 · 짧게): ① Codex 탐침 재실행 표 (탐침 · 기대 · 결과) ② 찾은 반례 표 (부류 · 입력 요약 · 결과 · 기대 · Codex 예상 등급 · 같은 부류 ID · 최소 수정) ③ 변이 시험 표 (되돌린 검사 · 새 시험 실패 수) ④ 거짓 거부 확인 표 ⑤ "Codex 에 보내기 전 고쳐야 할 것" 과 "한정으로 적으면 될 것" 두 줄 목록.  재현 파일 경로 (`prerev_attack/…`) 를 같이 적는다.
