# non-Rint 통합 (단계 B) 검증 증거 (2026-10-27)

1저자 10-27 승인 (*"Codex 통합 준비 쪽지가 게시됐어. 첨부 프롬프트대로 통합 진행해줘. 문서 예외 2행 정리, CI 연결 미완료 항목, 통합 후 최종 검증 조건도 확인해줘."* · 뒤이어 *"권고대로 해줘"*).
통합 계획 = `docs/collab/codex_to_claude/20261026-1904_merge-plan.md` §6.  대응표 쪽지 = `docs/collab/claude_to_codex/20261027-0220_nonrint-merge-sha-map.md`.

## 대상

- 검사한 커밋 = `8a2c92da9bf70072c1de197cbb5b1b148881ff69` = 기준 `67d7e2d96` + 반입 37 + §5 기록 + Codex 쪽지 반입.
- 그 tree 객체 = `b1a066ef8540587c7ba18b4031dc1f42613f3bfc`.
- 이 폴더와 대응표 쪽지는 그 다음 커밋이다.  두 파일 묶음은 검사 입력 (스크립트 · 고정 객체 · 증거 fixture) 을 바꾸지 않는다.

## 파일

| 파일 | 무엇 | sha256 |
|---|---|---|
| `gate_8a2c92da9.log` | 전체 게이트 `bash scripts/check_all.sh` (잠금 · 스레드 1) · 157 단계 ✓ · 0 ✗ · EXIT 0 · 끝 01:44:26 UTC | `c65008cf824725b4f2bb17b4cf7014c69648aa79c755ef8c9cb43bbba46d35b4` |
| `t12-consumer-receipt.json` | `scripts/test_dem_gen2_t12_consumer_contract.py` 영수증 (표준 출력과 같은 바이트) · PASS · 52/52 · `physical_T12` NOT_RUN | `d443b2edf0daa100db47a018bf0ddb78c70e6a795aae689cbc20a773b407d262` |
| `t12-offline-result.json` | `scripts/test_dem_gen2_t12_offline.py --check-guard-mutation` 의 `result.json` · PASS | `58b02fb094fd5dae0b69fc70c89fdda72ef74beda2b668980dbfc594fb820b77` |
| `t12-offline.log` | 같은 실행의 표준 출력 요약 | `999549e2ccf0787db9ab9029248a334e7b9b39bf6b3b272b3b072eef13c3ce04` |
| `d2-consumers.log` | `scripts/test_mixer_d2_consumers.py` · 13 OK | `964aed89e0e2cb6ce984d71c7a5e0a6384dd5d6ef09286630be8946466f14cf7` |
| `d3-candidates.log` | `scripts/test_mixer_d3_candidates.py` · 28 OK | `0183129dafde0ca1e92ed10944f822908f049b5abfcbae66e5ebda91f70c9bd2` |

T12 오프라인의 정상 경우는 소비자 52 사례를 다시 대조한다 (`case_count` 52).  이 52 를 따로 더하지 않는다 (계획 §6 과 같은 규칙).

## T12 두 검사의 git (≥ 2.44 가 필요)

- 이 컨테이너의 시스템 git = 2.43.0 → `--no-lazy-fetch` 를 몰라 두 검사가 설계대로 닫힌 실패를 낸다 (소비자 rc 2 · 오프라인 rc 1 · 첫 실행).  시스템 git 은 바꾸지 않았다.
- 대신 쓴 git = 2.53.0 (scratch 빌드 · 두 명령에만 `PATH` 앞에 둠).  출처 사슬:
  - `archive.ubuntu.com` resolute `InRelease` → `gpgv` (`/usr/share/keyrings/ubuntu-archive-keyring.gpg`) *Good signature from "Ubuntu Archive Automatic Signing Key (2018)"*.
  - `main/source/Sources.xz` sha256 `dce0fc8e2a473b26f729b1204fd4c12ae068428f743f96761392a059ab7bbfcd` = Release 값.
  - `git_2.53.0.orig.tar.xz` sha256 `5818bd7d80b061bbbdfec8a433d609dc8818a05991f731ffc4a561e2ca18c653` = Sources 값 = 받은 파일.
  - `make` 옵션 = `NO_CURL NO_EXPAT NO_TCLTK NO_GETTEXT NO_PERL NO_PYTHON` (파일 전송만 쓰는 시험이라 http 지원 없이 빌드).
- kernel.org · launchpad PPA · github 압축본은 이 세션의 네트워크 정책이 막았다 (proxy 403).
- Codex 시험은 git 2.52.0 이다.  Ubuntu 저장소에는 2.51.0 · 2.53.0 · 2.55.0 이 있고 2.52.0 은 없다 → 2.53.0 (resolute = 26.04 LTS) 을 골랐다.  두 판 모두 `--no-lazy-fetch` 를 지원한다.

## 명령 (계획 §6 의 명령 · 경로만 이 checkout 으로)

```bash
PATH=<scratch>/prefix/bin:$PATH python3 -I scripts/test_dem_gen2_t12_consumer_contract.py --repo <checkout> --json <scratch>/t12-consumer-receipt.json
PATH=<scratch>/prefix/bin:$PATH python3 -I scripts/test_dem_gen2_t12_offline.py --repo <checkout> --source <checkout> --output <scratch>/t12-offline --check-guard-mutation
python3 -I scripts/test_mixer_d2_consumers.py
python3 -I scripts/test_mixer_d3_candidates.py
```

## 결과 요약

| 검사 | 결과 |
|---|---|
| 전체 게이트 (공용 검사) | 157 ✓ · 0 ✗ · EXIT 0 |
| T12 소비자 계약 (직접) | PASS · 52/52 (positive · negative · coverage_boundary) · pin `4c29705fa1c4ba94737a858b206fa4f4c5bb2bde` · `physical_ready` false · `physical_T12` NOT_RUN · rc 0 |
| T12 오프라인 (직접) | PASS · rc 0 · 다섯 경우 (여섯 blob 모두 있음 rc 0 · commit · root tree · kit tree · blob 하나 빠짐 = 각 rc 2) · fetch 프로세스 0 · 읽기 전부 `--no-lazy-fetch` · 객체 변화 없음 · 미지원 옵션 가드 (모의 응답) 통과 · 가드 제거 변이 = rc 2 + fetch 프로세스 3 → 탐지 |
| D2 소비자 (직접) | 13 OK · rc 0 |
| D3 후보 (직접) | 28 OK · rc 0 |
| `check_review_findings.py` | rc 0 · 842 (open 281 · claimed_fixed 324 · verified 228 · wontfix 9) |
| `--ban-sweep` | 누수 0 |
| `check_doc_refs.py` | `--quiet` rc 0 · verbose rc 0 (없는 경로 0 · 없는 커밋 0 · 낡은 등재 0) |

## 이 증거가 덮지 않는 것

- T12 두 검사는 고정 커밋 `4c29705fa` 의 원본 소비자만 돈다.  현재 checkout 의 소비자 · 생산자에 결속한 검사는 아직 없다.
- D2 · D3 는 합성 시험이다 (실제 덱 · 관측 · 등록 코호트 아님).
- 언로딩 키트 검사 다섯 (`ul_reader` · `ul_gates` · `ul_runner_test --selftest` · `make_unload_decks` · `seal_kit --check`) 은 돌리지 않았다.
- 실제 자료가 있어야 하는 CLI (LHS `preflight-verify` · D2 `--d2` · D3 `--contract` / `--observations`) 는 돌리지 않았다.
- 물리 T12 = NOT_RUN · RJ 323957 `VALUE_MISMATCH` 그대로 · 실제 contact 진단 NOT_RUN.
- `d2-consumers.log` 의 `ResourceWarning` (`scripts/make_mixer_deck.py` 1122 행의 닫지 않은 파일) 은 경고일 뿐 결과에 영향이 없다.
