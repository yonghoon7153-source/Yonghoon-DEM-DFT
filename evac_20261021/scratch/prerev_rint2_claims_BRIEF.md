# Rint ② 설계 v1 · 등록 R 초안 · Codex 요청서 — 사전 리뷰 (문장 · 숫자 · 출처 대조 · 읽기 전용 · 10-20)

너는 기록 감사자다.  세 문서의 **모든 숫자 · 출처 · 전칭 문장** 을 리포 · git · litdb 정본 카드에 한 줄씩 대조한다.  Codex 는 범위 없는 전칭 ("무변경" · "전부") · 서로 다른 판을 섞은 숫자 · 출처 없는 값을 매번 결함으로 잡는다 (`SELF-124` · `SELF-51` · `CL-90` · `CL-91`).

## 대상
- 커밋 `b694369b5` (부모 `f507bdc74`): `docs/reviews/rint_carbon_additive_design_v1_20261020.md` · `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` · `docs/reviews/codex_rint_carbon_additive_design_request_20261020.md`.
- 작업 자리: `git -C /home/user/Yonghoon-DEM-DFT worktree add --detach /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/wt_prerev2_claims b694369b5` · 끝나면 `git -C /home/user/Yonghoon-DEM-DFT worktree remove --force <그 경로>`.  임시 파일 = `…/scratchpad/prerev2_claims/` 만 · 큰 사본 금지 (디스크 여유가 작다).
- litdb 정본 (fetch 하지 않는다 — 메인에서 게이트가 돈다): `git -C /home/user/Yonghoon-DEM-DFT show origin/claude/friendly-meitner-lldvar:litdb/papers/<card>.md` (읽기만).  파일 목록 = `git -C /home/user/Yonghoon-DEM-DFT ls-tree origin/claude/friendly-meitner-lldvar litdb/papers/ --name-only`.

## 대조할 것
1. **숫자**: 문서에 나오는 숫자마다 출처 (리포 파일:줄 · 카드 · 산술) 를 찾아 같은지.  산술은 직접 다시 계산한다 (예: G0 = ln(4.68/1.8877) · σ 대비 1.9e6 · ×7.54 · 0.454 · 0.908 · 캡슐 부피 비 · 직경 보존 7,854 S/cm · 표현 부피 0.16 배 등).  [우리 산술] · [추정] 표지가 맞게 붙었는지.
2. **서지 · 값**: 카드에서 온 값은 카드 문장과 대조 (값 · 단위 · 조건 · 그림 번호) — 카드에 없는데 적힌 값 = 결함.  `[미확인]` 이어야 할 것이 값으로 적혔는지.
3. **코드 사실**: "vox 0.20 은 SDCP 구 스탬프 게이트 (d/vox ≥ 2) 때문에 불가" · `ptfe_stamp` 값 목록 · 예약값 `capsule` 의 뜻 · `physics_protocol_id` · 매니페스트 키 · "끄면 매니페스트 바이트 같음" 을 주장할 근거 · "봉인 p2 코호트 32 팔" · 러너 환경변수 이름 — 실제 코드 (파일:줄) 와 같은지.
4. **결정 대조**: 1저자 결정 (`docs/reviews/rint_carbon_additive_plan_20261020.md` §2 Q1–Q12 · 머리 보탬 · `docs/reviews/rimprr_fix_plan_20261020.md` Q6 (나)) 과 문서가 어긋나는 곳 · 결정 안 된 것을 결정된 것처럼 쓴 곳.
5. **등록 v2 · 결과 문장**: SDCP 등록 v2 §7 (`docs/reviews/sdcp_sigma_e_dcp_anchor_registration_v2_20261019.md`) 의 값 (1.6209 · 1.8877 · 0.347 · 2.618 · 4.7524 · 2.54) 인용이 같은지 · "결과 0 건" 문서에 결과가 섞였는지.
6. **커밋 번호 · 경로**: 문서에 적힌 커밋 번호가 원격에 있거나 이 사슬 (`f507bdc74` 의 조상 또는 `b694369b5`) 에 있는지 (`SELF-116`) · 경로가 실제로 있는지 · `python3 scripts/check_doc_refs.py` (분리 작업 트리에서).

## 규칙
- **리포 · 다른 작업 트리를 고치지 않는다 · 커밋 · push 안 함 · `scripts/check_all.sh` 안 돌림.**  다른 게이트가 돈다 — CPU · 디스크 적게.
- 보고 (한국어 · 표 중심 · 짧게): 문장 | 자리 (파일:줄) | 대조 결과 (맞음 / 틀림 / 범위 부족 / 출처 없음) | 근거 | 고칠 문안.  끝에 "틀림 · 범위 부족 · 출처 없음" 만 모은 목록.
