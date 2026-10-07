# Codex 재검증 5 첨부 — WSL 사전 점검 2 (2026-10-07 22:24 KST · 1저자 · 코드 `839dbac6b`)

- **무엇**: 요청서 `docs/reviews/codex_gen2_network_reverify5_request_20261007.md` 머리의 "이 요청에 붙일 것" ① ② ③ — 고친 도구 (G2RR4-01 `942e851fd` · G2RR4-02 `4c8f84928` · G2RR4-03 `36ba39070` · `a51e61b05`) 로
  ① 옛 시범 ROOT `~/g2pre_pilot_c3117438a_1007_1415` (읽기만 · 출력 JSON 은 ROOT 밖) 재감사 · 다시 읽기 ② 스모크 (real14 · case15 · `lhs00_055` · `lhs00_128` · `lhsx_007`) + `--smoke-root` 다시 읽기
  ③ 새 시범 pilot3 (`--observe-imports`).  194 생산 실행이 아니다 (194 = Codex GO 뒤).
- **묶음**: `g2rr5_839dbac6b_1007_2224.tar.gz` — 54,375 B · sha256 `41a755974d99aa0d1c8315cf3454cd15a7eeabdca31062c999f25c67118d2939` (1저자 화면의 sha256 줄과 같다 · 받은 그대로).
- **화면**: `wsl_terminal_839dbac6b_1007_2224.txt` — 1저자가 붙여 넣은 그대로.  첫 줄들 (③ 명령 · `tar czf` 가 한 줄에 겹친 것) 은 붙여 넣기 때 화면 줄이 겹쳐 보인 것이다 —
  각 단계가 실제로 돈 것은 단계마다의 `rc=` 줄과 묶음의 `<단계>.stdout` · `<단계>.rc` 로 본다.
- **환경** (`env.txt`): 체크아웃 `839dbac6b` (detached · dirty 0) · numpy 2.5.2 · scipy 1.18.1 · networkx 3.7 (배치 venv).
  명령 = 요청서 머리와 같은 꼴 — 단계마다 전체 출력 → `<단계>.stdout` · 종료 코드 → `<단계>.rc` (화면에는 rc 만).

## 1. 받은 것 (`SELF-94` — 받은 목록 그대로)

| 폴더 (묶음 안) | 파일 | 무엇 |
|---|---|---|
| `g2rr5_839dbac6b_1007_2224/` | `env.txt` · 단계 10 개의 `.stdout` + `.rc` (`st_reread` · `st_runner` · `st_smoke` · `old_audit` · `old_reread` · `smoke` · `smoke_reread` · `pilot` · `pilot_audit` · `pilot_reread`) · `old_audit.json` · `old_reread.json` | 각 원 프로세스의 전체 출력 · 종료 코드 · ① 의 JSON |
| `g2pre_smoke_839dbac6b_1007_2224/` | `smoke_report.json` · `smoke_summary.txt` · `reread.json` | ② |
| `g2pre_pilot_839dbac6b_1007_2224/` | `manifest.json` · `seal_audit.tsv` · `seal_audit.json` · `reread.json` · `progress.tsv` · `merge_report.json` (merged 폴더 안) · `run_001.json` (runs 폴더 안) · `cases/<3 케이스>/{worker.json, log.txt, out/status.json}` · `import_obs/` (hook 1 + 영수증 30 = 시작 15 · 끝맺음 15) | ③ |

- **받지 않은 것**: 케이스 파이프라인 산출물 원파일 (게시된 dual / full_metrics · 망 결과) · 194 전체 dry-run (이번 머리 ①–③ 범위 밖) · 옛 시범 ROOT 자체 (읽기만 했다 · 10-07 14:15 묶음
  `docs/reviews/codex_gen2_network_reverify4_precheck_20261007/` 에 이미 있다).

## 2. 기대 (요청서 머리 · 등록 §9-4 ③ 제안) 와 결과

| 단계 | 기대 (결과 전) | 결과 | 판정 |
|---|---|---|---|
| 0 | dirty 0 · 브랜치 끝 | `839dbac6b` · dirty 0 | 같음 |
| 자체 시험 | 다시 읽기 20/20 · 실행기 117/117 · 스모크 14/14 | rc 0 셋 · ✓ 20 · 117/117 · ✓ 14 (실행기 출력의 ✗ 두 줄 = 시험이 일부러 만든 실패 케이스 `lhs99_001` SIGKILL · `lhs99_002` 정지 계약의 화면 — 판정 117/117) | 같음 |
| ① 옛 시범 audit | rc 0 · 시작 15 = 끝맺음 15 · 완료 시도 3 · 단계 결합 3 (지금 케이스 기록 stages) · 관측 문제 `[]` | rc 0 · 15 · 15 · 3 · 결합 3 (출처 = `out/status.json` 케이스 기록 stages · 기대 = 관측 워커 + parse · 접촉 · 피복 · 망 각 1) · `[]` · SEALED 3 · 실행 형식 current · launch `c3117438a` · seal_fp `e8b2496b…` · 세대 g2 · 세대 · 입력 문제 0 | 같음 |
| ① 옛 시범 reread | rc 0 (상세 계약) | rc 0 · 다시 읽기 v3 · n_fail 0 · pilot3 `set_equal` true · seal_fp `e8b2496b…` | 같음 |
| ② smoke | rc 0 · case15 `[음성 대조]` 넷 PASS · 나머지 지난번 그대로 | rc 0 · 검사 26 · PASS 26 · case15 = failed (게시 차단 · 망 솔버 두 모드) + 음성 대조 넷 PASS (게시 차단 · 숫자 비노출 · 원인 발화 B∩T = 24 · 40 · 57 · 103 · 음수 행 2 · 이온 σ_ratio 0.00032635 · 0.00036225) · real14 done (σ_ion H/P 0.063063 · 0.09492) · `lhs00_055` done (0.01428 · 0.017136) · `lhsx_007` done (0.620685 · 1.401522) — 셋 다 10-07 14:15 와 같은 값 · `lhs00_128` valid_zero · τ NOT_PERCOLATING · C 넷 PASS | 같음 |
| ② smoke reread | rc 0 (S0 · S0b) | rc 0 · n_fail 0 | 같음 |
| ③ pilot | rc 0 · 세 케이스 done | rc 0 | 같음 |
| ③ audit | rc 0 · 결합 출처 = 시도 사본 (`worker.json attempts[].stage_plan`) | rc 0 · 15 · 15 · 3 · 결합 3 (출처 = `worker.json attempts[].stage_plan`) · `[]` · SEALED 3 · launch `839dbac6b` · `observe_imports` true · 세대 g2 · 실행 형식 v3 · seal `code_fp e8b2496b…` | 같음 |
| ③ reread | rc 0 | rc 0 · v3 · n_fail 0 · pilot3 `set_equal` true · seal_fp `e8b2496b…` · manifest sha256 `9e1823dc…` | 같음 |

## 3. 한정

- 이 점검은 고친 도구가 실제 WSL 기록 (옛 실행기 ROOT · 새 ROOT · 스모크) 에서 기대대로 동작함을 보인다.  194 결과도, 등록 제안의 비준도 아니다 — 등록 §3b · §4 · §9-4 는 아직 ⬜ 1저자 비준 전이고,
  위 표의 "기대" 는 §9-4 ③ 의 **제안** 기대다.
- 대조는 이 컨테이너에서 묶음을 새 빈 폴더에 풀어 `python3 -I` 로 JSON 을 읽은 것이다 (묶음 안의 것을 실행하지 않았다).
