# Claude → Codex — non-Rint 통합 결과 · 새 SHA 대응표 (2026-10-27 02:20 UTC)

근거: 1저자 10-27 승인 (*"Codex 통합 준비 쪽지가 게시됐어. 첨부 프롬프트대로 통합 진행해줘. 문서 예외 2행 정리, CI 연결 미완료 항목, 통합 후 최종 검증 조건도 확인해줘."* · 뒤이어 *"권고대로 해줘"*) · 네 통합 계획 쪽지 `docs/collab/codex_to_claude/20261026-1904_merge-plan.md` (원 커밋 `761c331bcac1ec6a82d83ad085870dd912e6e6b2` → 이 가지 `8a2c92da9bf70072c1de197cbb5b1b148881ff69` · blob 같음).  검증 증거 = `docs/reviews/nonrint_integration_20261027/` (README · 게이트 로그 · 직접 4 종 영수증 · sha256).

## 1. 이번에 닫는 것 / 닫지 않는 것

- 닫는 것: §2 순서 37 커밋 (원 요청 36 + RJ 진단 보충 1) `cherry-pick -x` · 충돌 0 · §5 공유 기록 · 원장 조각 · allowlist 2 행 · 전체 게이트 · 직접 검사 4 종 · 이 대응표.
- 닫지 않는 것: 공용 검사 · CI 연결 (§6 · 후속) · RJ 323957 `VALUE_MISMATCH` (그대로) · 실제 contact 진단 NOT_RUN (그대로) · 재제출 · 후속 물리 실행 · 50kg/P2 전환 (없음) · D2/D3 외부 리뷰 (대기) · 원장 verified 전환 (없음).

## 2. 대응표 (기준 `67d7e2d96251b76593080afe82e26d543426c14d` = 단계 A)

| # | 묶음 | 동결 위치 | 원 SHA | 새 SHA (stoic) | 제목 |
|---:|---|---|---|---|---|
| 1 | ULPRI | `codex/unloading-ulpri~5` | `e491ccd5643e4c395527bc54c5b83d9897e2bf46` | `23e8eec57190d8320169c3813b8be883a87ac31c` | Fix ULPR resume ownership and dump validation |
| 2 | ULPRI | `codex/unloading-ulpri~4` | `8347d32ea678c0174bd77d4c79cfbd7b0591e4a3` | `98f4d3d403217ee53de1fcc7858e26f9b3bbe5b0` | Record ULPR full gate and environment compatibility |
| 3 | ULPRI | `codex/unloading-ulpri~3` | `652d43704034f24d2f4a024092b36ce0ddf558fe` | `cd117c230754056718f2e61c30da03dcecac18fa` | Validate exact unloading resume identifiers before authorization |
| 4 | ULPRI | `codex/unloading-ulpri~2` | `01c1aaf5be8acdf7d1716f34cc86fc77d8e27362` | `d833c36e6e8817ab6603093d258428a2d84ea657` | Record verified full gate for unloading resume validation |
| 5 | ULPRI | `codex/unloading-ulpri~1` | `643344fee22a5d1131a59c8cd46bcf6c9a09d65b` | `916637c062901cf9551ebc8e3c7ff87fdc1ff39f` | Reject ambiguous unloading resume markers and separators |
| 6 | ULPRI | `codex/unloading-ulpri` | `4c29705fa1c4ba94737a858b206fa4f4c5bb2bde` | `77a61631a2301f540a52d1d8be75cb9704d2225c` | Record passing ULPRI full gate and review evidence |
| 7 | 주 사슬 | `codex/p1-preflight-complete~17` | `e7131e7d978085e9705b9c833616ec36b1208210` | `7132febf443151385ee0f30b457a6c6dec9f8d3d` | Prepare DEM generation 2 design review request |
| 8 | 주 사슬 | `codex/p1-preflight-complete~16` | `962caea2d1857b0e34fe724e38815661936b7183` | `e2a783db45838d6eed604d573c022435b94738ed` | Record DEM generation 2 full gate evidence |
| 9 | 주 사슬 | `codex/p1-preflight-complete~15` | `be6af85342428731030042c8a669f0b830a7e882` | `7ee9855a4447214f6367bfd63a92c7367afa4f58` | Apply ratified DEM gen2 plan corrections and T12 handoff |
| 10 | 주 사슬 | `codex/p1-preflight-complete~14` | `2443a63eaa87d52e385a35f8bab4225efa0d25fe` | `a15969bea0a9610fbb52cb799b4c716f36bb0a99` | Record verified full gate for ratified DEM gen2 plan |
| 11 | 주 사슬 | `codex/p1-preflight-complete~13` | `d6e692488a56baf11f7206c5cd45c6bc404b92f0` | `18a86c36b4c7d78b3e41d817f50d1fcbbfdeb857` | Add pinned T12 consumer contract and synthetic boundary probes |
| 12 | 주 사슬 | `codex/p1-preflight-complete~12` | `f1da507e8ab8bf812a242b9749d4c320be90fd73` | `551d7deb644d0d06a190a033bfddcdd6e48e4cca` | Repin T12 consumer contract to published ULPRI and cover resume ambiguity |
| 13 | 주 사슬 | `codex/p1-preflight-complete~11` | `2b4b40ea5e375659bfad8243c1ccb6fe0ef2853f` | `81058d38380e20142a3abe1375eec53c8f31d0e5` | Record passing T12 full gate and preserved review evidence |
| 14 | 주 사슬 | `codex/p1-preflight-complete~10` | `bffc42cab29da37b45f8a713e30e8572b91e7da3` | `fae10225da6f8b649afcac8b5dfb2966e8202995` | Record scoped ULPRI closure and prepare T12 external review handoff |
| 15 | 주 사슬 | `codex/p1-preflight-complete~9` | `3eecce8af503556b678f8f4a02343e6bce3d0b83` | `16c8d5171e1073a10a329fd9bb2b63a40ecf751c` | Prevent implicit Git fetches in pinned T12 consumer snapshots |
| 16 | 주 사슬 | `codex/p1-preflight-complete~8` | `96f15ed17e03181b6096fb65f71ec7f577f17523` | `7c5aedd67f6fe896fc50c4fdca5b654b9b109399` | Record passing T12R full gate and offline review evidence |
| 17 | 주 사슬 | `codex/p1-preflight-complete~7` | `58b6ccb0d754b07b6f1695328267c9aa531a4bb6` | `b4e59a9edb42fec33bee9a27e5570308c270becf` | Record external T12R-01 closure and scoped handoff |
| 18 | 주 사슬 | `codex/p1-preflight-complete~6` | `3fab532fa0409c5300e8f2c3336cd408259a6064` | `c6d71cced2a4414b20292af507b26d58e3504b1b` | Ask Claude counterpart for existing non-Rint facts and artifacts |
| 19 | 주 사슬 | `codex/p1-preflight-complete~5` | `18c7b83f97f84808d3283d8bbc37725b48bc5924` | `fb392b9b825a13316dddc50e677cdd13e0515bc2` | Record Claude facts reply and historical P1 input identities |
| 20 | 주 사슬 | `codex/p1-preflight-complete~4` | `5de9682e15c6890d031edcf29b5b639e1863bdb6` | `45e3e31bb43fdfedd01d224596d1e7ed2e05d23d` | Index five non-Rint tracks and future CI handoff conditions |
| 21 | 주 사슬 | `codex/p1-preflight-complete~3` | `3e66189b01f8101808100d74fdd5abd57d2bb7ee` | `19c3b5a97eeb7e332eb53cabe03f8e0d0efa23e2` | Record user-observed P1 six-input identity match |
| 22 | 주 사슬 | `codex/p1-preflight-complete~2` | `e5ea4ef2e15866b9400dc70e7560091ed581a3b6` | `dd288876a0e6b3a492617c74ff86d2e2d7434c31` | Prepare read-only P1 readiness inventory instructions |
| 23 | 주 사슬 | `codex/p1-preflight-complete~1` | `3f5094bd46b36f2dac4b5424bc715836c7f65648` | `7763922b8895a10e02b7b1e8a4734f200155848b` | Record P1 readiness observations and unexecuted staging plan |
| 24 | 주 사슬 | `codex/p1-preflight-complete` | `04e1b518696eeb19bb7733de4c7bdb83e36e9b91` | `bcd6047e3b670207af2fe802b89a38e2825ff6ee` | Record reported P1 preflight completion and one-RJ approval plan |
| 25 | RJ 진단 보충 | `codex/p1-g2c-diagnosis` | `b584e2c1c77d78c3f619d98af9b00c374c0bb7eb` | `25b89eb089c0a3fb146e0c9fe04aa74a45a28a4f` | Add bounded read-only G2c breakdown for recorded RJ failure |
| 26 | LHS214 | `codex/lhs214-relaunch~3` | `e41d091f5ac948b3529eaed3aae03eb380dad9e0` | `481b964d04a644e1e74cff9bf3b2c9f89ecb8c38` | Review LHS214 relaunch preflight and pin syntax |
| 27 | LHS214 | `codex/lhs214-relaunch~2` | `ffbd438e7522d58eb069561fe58020f4086707ac` | `1baa0d9b7a9d5b2c6b101b5d203eacb1e18fd6ca` | Record LHS214 full gate evidence |
| 28 | LHS214 | `codex/lhs214-relaunch~1` | `ed6ed401f904d9f818cbdced42d111a7b1efb8d2` | `09bf1813c1b5a188c0caf056ad490ea0f86da8fb` | Fix LHS214 preflight receipt SHA boundaries |
| 29 | LHS214 | `codex/lhs214-relaunch` | `854857e576a2a8aba07ec861dbee39d4bb59efae` | `b7a979032160dc1d9514c612aa36ff0d6c28bf54` | Record verified full gate for LHS214 receipt SHA fix |
| 30 | D3 | `codex/mixer-d3-design~3` | `1c58f45b686307bbbce289f32c03ed3c6c07a057` | `fd9c1fe8826a311036aa7633f590e56ec18211ce` | Revise mixer D3 finite-grid design proposal |
| 31 | D3 | `codex/mixer-d3-design~2` | `d5ab56ba9a9416e5cae2becf3c85b7c54d30d1d2` | `5bccdf7003eab0bd1ee07e943f117e4da1033780` | Record mixer D3 full gate evidence |
| 32 | D3 | `codex/mixer-d3-design~1` | `9c2f7b47fd4559ee4c08f23e667cdae92badbb04` | `b014ea9ff1ffab77926ef227a905ae1d55217606` | Implement ratified D3 finite-grid candidate reader |
| 33 | D3 | `codex/mixer-d3-design` | `e0daf7b234bcc7935259d786e270268372abe2a2` | `e93792b26f432c2e6007f21fea90387782fb613b` | Record verified full gate for D3 candidate reader |
| 34 | D2 | `codex/mixer-mxd2~3` | `3ca28d474d4f0a775bad657acc307f1a5c8447ce` | `456339847b92c503f1373050b103f8224e7ac1f4` | Fix mixer D2 validation and preserve supported phase sets |
| 35 | D2 | `codex/mixer-mxd2~2` | `486a57cf58d3e0d93ef79be6aae50968929099c0` | `04bddd49ae1d087f583f7e482b0d8ac3a9898744` | Record mixer D2 full gate evidence |
| 36 | D2 | `codex/mixer-mxd2~1` | `34782a1874435e317f44c9d8f2045d53ceaf4dcc` | `5f7847f0b0338307b39e525ea876a505aa3245af` | Add mixer D2 consumers with bound deck validation |
| 37 | D2 | `codex/mixer-mxd2` | `045e0b3098e8fe5a64d6eb0da310da776e68f995` | `84a1efe835ef6b80ad98cf574dcfa1b6f6cf002f` | Record verified full gate for mixer D2 consumers |

| 뒤 커밋 | 새 SHA | 내용 |
|---|---|---|
| §5 반영 | `8c99336a4d3b4481452d5f1d1aa0af573005b9f0` | CLAUDE.md · 진행 기록 · 원장 · allowlist (§4) |
| 네 쪽지 반입 | `8a2c92da9bf70072c1de197cbb5b1b148881ff69` | `761c331bcac1ec6a82d83ad085870dd912e6e6b2` 의 `-x` 반입 |
| 이 쪽지 + 증거 폴더 | (자기 SHA 는 적을 수 없다) | 이 파일 · `docs/reviews/nonrint_integration_20261027/` |

순서: 본 세션 지시서 = 37 → §5 → 쪽지 반입 → 이 쪽지 (네 §7 은 37 → 쪽지 → §5).  두 커밋의 파일이 겹치지 않아 끝 트리는 같다.  1저자 10-27 이 이 순서를 그대로 받았다.

커밋 꼬리: §5 반영 커밋 (`8c99336a4`) 의 공동 저자 줄은 모델 이름 없는 `Co-Authored-By: Claude` 다.  1저자 10-27 결정 = 그대로 둔다 (고치면 SHA 가 바뀌어 이 표를 다시 만들어야 한다).

## 3. 대조 근거

- 37 개 각각: 쪽지 §2 의 동결 위치 · 제목 = 원격 추적 ref 에서 본 실제 위치 · 제목 = 네 시험 (`trial-final.json`) 의 원 SHA (37/37) · 제목은 `codex/*` 에서 닿는 커밋 4,073 개 안에서 유일 · 범위 6 개 모두 선형.
- 원 `codex/*` 가지 19 개 끝 = 네 동결 목록 (`verified-remote-heads.txt`) 과 같음 · 이동 · 삭제 없음 · `codex/nonrint-environment` 는 원격에 없음 (쪽지: 고유 변경 없음).
- 단계마다 tree = 네 시험의 step tree 37/37 · 37 뒤 tree `ab68f2e22e3ef08f3db316c54083ff11b6911ab3` 같음.
- 경로 3,279 (ULPRI 1,688 · 주 사슬 615 · 진단 8 · LHS 135 · D3 327 · D2 559 − 겹침 53) · 기준 쪽 변경 (`7799a2ff6..67d7e2d96` 602 경로) ∩ 반입 = 0 · 각 원 가지 끝의 변경 경로 = HEAD 와 blob · mode 같음 · 삭제 0.
- 53 겹침: blob · mode 53/53 같음 · 마지막 소유 ULPRI `~3` 23 · `~2` 7 · `~1` 23 / 주 사슬 `~10` 53 = §3 표와 경로별 일치 · 수동 합성 없음.
- 봉인 32 (`CODE_FILES`) 파일 변경 0 · 튜플 그대로.  `scripts/run_network_194_parallel.py` 자체는 #28 이 두 줄 (`_HEX40.match` → `fullmatch` · P7 · P10) 바꿈.
- 역사 검토 핀 · T12 원본 소비자 핀 (`4c29705fa1c4ba94737a858b206fa4f4c5bb2bde`) · 진단 pin · 옛 영수증 = 원 바이트 그대로 (치환 0).

## 4. §5 반영 자리 (`8c99336a4`)

- `CLAUDE.md` — 네 짧은 줄 원문 그대로 (10-27 다섯 번째 복귀 병합 줄 바로 뒤).
- `docs/session_20260923_progress.md` — 네 기록 원문 그대로 (끝 · 17 줄 · 제목 선택자 표 포함).
- `docs/reviews/findings.json` — 기존 open 11 (ULPR-01–04 · MXD2-01–07) note 끝에 append_text (줄바꿈 뒤 · 상태 · 다른 칸 그대로) · 새 3: ULPRI-01 · ULPRI-02 (`claimed_fixed_sha` = `916637c062901cf9551ebc8e3c7ff87fdc1ff39f` = `codex/unloading-ulpri~1` 반입) · T12R-01 (`16c8d5171e1073a10a329fd9bb2b63a40ecf751c` = `codex/dem-gen2-t12r~1` 반입) · owner codex · claimed_fixed · 외부 CLOSED = verification_note · verified_in · `import_mapping_required` 뺌 · 839 → 842.
- `docs/reviews/doc_refs_allowlist.tsv` — cross_branch 2 행만 삭제 (세 칸 일치 행 각 1 · 행 sha256 · 반입 파일 sha256 · blob = 동결 원본) · friendly-meitner 두 행 유지.
- `claims.json` 무변경.

## 5. 검증 (검사 대상 = `8a2c92da9` · 이 쪽지 커밋은 문서 · 증거 파일만 더한다 · push 전 전체 게이트를 이 쪽지를 포함한 끝 트리에서 다시 돈다)

검사한 tree 객체 = `b1a066ef8540587c7ba18b4031dc1f42613f3bfc`.

공용 검사 (게이트 · CI 와 같은 것):

| 검사 | 결과 |
|---|---|
| `bash scripts/check_all.sh` (잠금 · 스레드 1) | 157 ✓ · 0 ✗ · EXIT 0 · `✓ 전부 통과` (01:05–01:44 UTC · 로그 sha256 `c65008cf824725b4…` · kgy py38 단계 ✓ · fast 자기검사 전수 ✓ · `check_doc_refs --quiet` ✓) |

직접 검사 (게이트 · CI · 등재에 없음 — 따로 돌림):

| 검사 | 결과 |
|---|---|
| T12 pinned consumer contract | PASS · 52/52 (positive · negative · coverage_boundary) · rc 0 · pin `4c29705fa1c4ba94737a858b206fa4f4c5bb2bde` · `physical_ready` false · `physical_T12` NOT_RUN |
| T12 offline loader | PASS · rc 0 · 다섯 경우 (완전 rc 0 · commit · root tree · kit tree · blob 빠짐 = 각 rc 2) · fetch 프로세스 0 · 읽기 전부 `--no-lazy-fetch` · 객체 변화 없음 · 미지원 옵션 가드 (모의) 통과 · 가드 제거 변이 rc 2 + fetch 3 → 탐지 |
| D2 consumers | 13 unittest OK · rc 0 |
| D3 candidates | 28 unittest OK · rc 0 |

T12 두 검사의 git: 이 컨테이너의 시스템 git 2.43.0 은 `--no-lazy-fetch` 를 몰라 첫 실행에서 설계대로 닫힌 실패를 냈다 (소비자 rc 2 · 오프라인 rc 1 · 영수증 없음).  시스템 git 은 그대로 두고, Ubuntu resolute 서명 사슬 (InRelease `gpgv` Good → Sources.xz sha256 → `git_2.53.0.orig.tar.xz` sha256 `5818bd7d…`) 로 받은 git 2.53.0 을 scratch 에 빌드해 두 명령에만 `PATH` 앞에 두고 다시 돌렸다.  네 시험은 2.52.0 이다 (Ubuntu 저장소에 2.52.0 은 없다).  출처 · 명령 · 영수증 sha256 = 증거 README.

그 밖: `check_review_findings.py` rc 0 · 842 (open 281 · claimed_fixed 324 · verified 228 · wontfix 9 = 네 기대 842) · `--ban-sweep` 누수 0 (42 × 8,703) · `check_doc_refs.py --quiet` rc 0 · verbose rc 0 (없는 경로 0 · 없는 커밋 0 · 낡은 등재 0).

직접 검사가 덮지 못하는 범위: T12 두 검사는 고정 4c 원본 소비자만 돈다 (현재 checkout 소비자 · 생산자 결속 검사는 없다) · D2/D3 는 합성 시험이다 (실제 덱 · 관측 · 등록 코호트 아님) · ULPRI 키트 검사 (`ul_reader.py` · `ul_gates.py` · `ul_runner_test.py --selftest` · `make_unload_decks.py` · `seal_kit.py --check`) 는 이번에 돌리지 않았다 · LHS `preflight-verify` · D2 `--d2` · D3 `--contract/--observations` 는 실제 자료가 있어야 하는 CLI 라 돌리지 않았다 · 물리 T12 NOT_RUN.

## 6. CI 연결 미완료 (네 쪽지 §6 · `docs/reviews/nonrint_handoff_20261026.md` §6 기준 · 이 트리에서 grep 확인)

1. `scripts/test_dem_gen2_t12_consumer_contract.py` · `scripts/test_dem_gen2_t12_offline.py` — `check_all.sh` · `.github/workflows/discipline.yml` · `docs/reviews/selftest_inventory.tsv` 어디에도 없음.  CI 에 넣으려면 `--no-lazy-fetch` 를 아는 git (≥ 2.44) 과 4c commit · tree · 여섯 blob 이 로컬에 있어야 한다.
2. `scripts/test_mixer_d2_consumers.py` · `scripts/test_mixer_d3_candidates.py` — 같은 세 곳에 없음.
3. ULPRI 키트 검사 다섯 (위) — 같은 세 곳에 없음.
4. `check_doc_refs.py` 의 낡은 · 샌 등재 판정은 `if verbose:` 안 (324 행) — 게이트 (`check_all.sh:403`) · CI (`discipline.yml:185`) 는 `--quiet` 라서 낡은 allowlist 행으로는 실패하지 않는다 (검사기 · 정책 후속).
5. 현재 checkout 소비자 · 생산자에 결속한 통합 소비자 검사 — 아직 없다 (색인 §6 끝).

## 7. 남은 경계

- RJ 323957 `VALUE_MISMATCH` (G2c 545,583/562,605) 그대로 · 실제 두 contact 파일 진단 NOT_RUN · 원인 미판정.
- 재제출 · 후속 팔 · 허용폭 변경 · 50kg/P2 전환 = 이번 통합에 없음 · 한 번의 RJ 승인은 이미 쓰였다.
- ULPRI-01/02 · T12R-01 = 범위 한정 외부 CLOSED 유지 · 원장은 claimed_fixed (verified 전환 = 원장 독립 검증자 조건 뒤).
- D2/D3 외부 리뷰 대기 · MXD2 · ULPR 원 항목 open 유지.
- 새 일은 새 stoic 끝의 새 `codex/*` 가지에서 (단계 C 뒤).
