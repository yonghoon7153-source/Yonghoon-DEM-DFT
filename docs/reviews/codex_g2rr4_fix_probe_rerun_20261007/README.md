# Codex 재검증 4 탐침 — 고친 트리 재실행 (G2RR4-01 · 02 · 03 · 2026-10-07)

- 기준 판정: `docs/reviews/codex_review_gen2_network_reverify4_20261007.md` (핀 `87f0906a2` · 194 · v1.3 HOLD · 새 P1 없음 · 새 P2 `G2RR4-01` 다시 읽기 상세 ↔ 요약 · `G2RR4-02` 보조 단계 영수증 쌍 결손 · P3 `G2RR4-03` 본 실행 관측 미등록).
- 고친 커밋: `942e851fd` (G2RR4-01) · `4c8f84928` (G2RR4-02) · `36ba39070` · `a51e61b05` (G2RR4-03).  재실행 트리 = `a51e61b05` (fixed_source_rev.json · 판정 묶음 manifest 의 고유 경로 446 · 빠진 경로 0) · 비교 = 핀 `87f0906a2` (pin_source_rev.json).
- 방법: 커밋된 판정 묶음 `docs/reviews/codex_gen2_network_reverify4_evidence_20261007/` (source 는 manifest 만 · submitted 는 리포의 사전 점검 tar 둘) 을 리포 밖 새 폴더에 다시 세우고 (source = `git archive <REV>` · submitted = tar 를 경로 · 타입 검사해 풂) Codex 다섯 탐침을 **무변경**으로 Codex README 순서대로 돌린다 → 이 폴더의 파생 탐침 둘 → 회귀 넷 — `drive_fix_probe.py` 한 번 (run_checks 호출마다 `python3 -I` · CWD = 묶음 밖).
- 파생 탐침 둘 (파일 머리에 Codex 탐침과 다른 줄을 적었다):
  `release_gate_detailed.py` — Codex release_gate 는 정상 대조까지 모든 변이의 reread meta · cases 를 최소 꼴 (meta 한 줄 · 케이스마다 K1 하나) 로 덮어쓴다 → 고친 트리의 상세 계약에서 control 까지 거부되어 "정상을 막는가 / 변이를 막는가" 가 갈리지 않는다 → 고친 트리 시험 픽스처 (생산자 계약 꼴 상세 기록 · 관측 객체 · 단계 결합 기록) 를 덮어쓰지 않고 같은 변이만 넣는다 (+ 같은 부류 하나 = 관측 객체 그대로 · 내부 문제만).
  `observation_cli_staged.py` — Codex observation_cli 의 합성 픽스처 (재검증 3 의 옛 실행기 ROOT) 에는 케이스 기록 단계 (`stages`) 가 없다 → 고친 실행기는 네 행 모두 "실행 단계 기록 없음" 으로 거부해 쌍 결손 자체를 잡는지 갈리지 않는다 → 단계 기록만 더한다 (케이스 기록 · merged 사본 · 시도 봉인 record_sha 를 실행기 함수로 다시 맞춤 · 영수증 · 네 변이 · 실제 audit CLI 는 같다).  핀에서도 같은 파생 탐침을 돌려 전 · 후를 같은 픽스처로 맞댄다.

```bash
python3 -I docs/reviews/codex_g2rr4_fix_probe_rerun_20261007/drive_fix_probe.py /tmp/g2rr4_probe_fixed a51e61b05     # 기대 rc 0 (단계별 rc 1 · 0 · 0 · 1 — 아래 §1)
python3 -I docs/reviews/codex_g2rr4_fix_probe_rerun_20261007/drive_fix_probe.py /tmp/g2rr4_probe_pin 87f0906a2      # 기대 rc 0 (단계별 rc 0 · 0 · 0 · 1)
```

## 1. 결과 (Linux · Python 3.11.15 · numpy 2.4.6 · scipy 1.17.1 · 두 driver rc 0)

| 사례 | 핀 `87f0906a2` | 고친 트리 `a51e61b05` |
|---|---|---|
| **release_gate (Codex 무변경 · G2RR4-01)** — control · reread 없음 · n_fail null · 감사 input_problems · manifest_sha256 다름 · **M2 ok=false · cases=[] · meta=[] · 감사 관측 {problems · outside}** | control 생성 · 넷 거부 · **셋 생성** (Codex 와 같음) | **8 전부 거부** — control 도 (최소 꼴 = 상세 계약의 필수 검사 ID 결손: meta M0 · M-plan · M-reg · M3 · 코호트마다 M1 · M2 · H1 · 케이스마다 K2–K7 · 'M2 all completed' 의 코호트 'all' = 등록 밖) — fixed_release_gate.json |
| **release_gate_detailed (파생 · 고친 트리 상세 픽스처 meta 10 · 194 × K1–K7 · 관측 객체 · stage_binding)** | — (핀의 픽스처에 상세 꼴이 없다 · 건너뜀) | **control 생성 · check_v13 문제 0** · reread 없음 · n_fail null · input_problems · manifest 다름 = 거부 · **M2 ok=false (n_fail 0) = 거부** ("상세 실패 재계수 1 ≠ n_fail 0") · **cases=[] · meta=[] (read_n 194) = 거부** (meta ID 결손 · 고유 0 ≠ 등록 194 · 상세 0 ≠ read_n) · **감사 관측 통째로 {problems · outside} = 거부** · **관측 객체 그대로 · 내부 문제만 (최상위 []) = 거부** ("최상위 import_observation_problems 에 없다") · 거부 8 모두 산출 폴더 없음 — fixed_release_gate_detailed.json |
| **observation_cli (Codex 무변경 · G2RR4-02)** — 5/5 · 파서 끝만 없음 · 파서 쌍 없음 · 워커 + 솔버만 | rc 0 · 1 · **0 · 0** (Codex 와 같음) | rc **1 · 1 · 1 · 1** — 사유 전부 "완료 시도의 실행 단계 기록이 없다" (그 합성 픽스처에 단계 기록이 없다 = 단계 증거 없이 통과시키지 않는 설계 · 5/5 도 거부) — fixed_observation_cli.json |
| **observation_cli_staged (파생 · 단계 기록만 더한 같은 픽스처)** | rc 0 · 1 · **0 · 0** · 결합 기록 없음 — pin_observation_cli_staged.json | rc **0 · 1 · 1 · 1** — 5/5 = 결합 (계획 parser · contact_bimodal · coverage · network_cli · 기대 = 관측 = 워커 1 + 단계 스크립트 넷 각 1) · 파서 끝만 없음 = 미최종 + parse_liggghts 0/1 · **파서 쌍 없음 = parse_liggghts 0/1** · **워커 + 솔버만 = parse_liggghts · analyze_contacts_bimodal · coverage_physics_vs_hertzian 0/1** — fixed_observation_cli_staged.json |
| **submitted_evidence (Codex 무변경)** | rc 0 · 경로 번역 기준선 문제 0 (Codex 와 같음) | rc 1 — 경로 번역 기준선 = "완료 시도의 실행 단계 기록이 없다" 3 (lhs00_055 · lhs00_128 · lhsx_007) 에서 탐침의 assert — 그 사본은 보충 묶음에서 worker.json 만 옮기고 **케이스 기록 out/status.json 이 없다** (보충 묶음에도 없다) — fixed_submitted_evidence.log.  실제 WSL pilot ROOT 에는 케이스 기록이 있다 → 고친 실행기 audit 로 1저자 WSL 확인 대상 |
| case15_channels (Codex 무변경) | 판 19.1455 µm · 음수 면적 2 행 · 전자 · 열 Hertz = boundary_overlap · Physics 열 ValueError · 이온 σ_ratio 0.00032635082552669387 · 0.00036224724407936984 | **같음 — JSON 전체 동일** (봉인 32 파일 무변경 · 같은 환경) |
| scope194 (Codex 무변경) | L0 130 · 64 · 겹침 0 · 접촉 행 18,111,468 + 14,694,721 · 음수 · 0 면적 0 | **같음 — JSON 바이트 동일** |
| `g2_network_reread --selftest` | 17/17 | **20/20** (G2RR4-01 상세 계약 둘 · G2RR4-03 스모크 음성 대조 S0b 하나 더) — fixed_reread.log |
| `test_gen2_publication_handover` · `test_gen2_role_contract` | 32/32 · 44/44 | 32/32 · 44/44 |
| `test_lhs_release_v13` | 134 PASS · 1 FAIL | **172 PASS · 1 FAIL** — FAIL = V16a 만 (git archive 사본에 `.git` 없음 · 핀 쪽과 같은 환경 차이 · 리포 checkout 에서는 173/173) — fixed_release.log |

- 요약 JSON = fixed_probe_summary.json · pin_probe_summary.json (driver 가 증거 JSON 에서 뽑은 판정 칸) · driver 출력 = driver_fixed.log · driver_pin.log.
- 고친 트리의 observation_cli 는 Codex 묶음의 evidence/submitted_evidence.json 을 **읽기만** 한다 (값을 쓰지 않는다) — 고친 트리의 submitted_evidence 탐침이 assert 로 그 파일을 못 썼으므로 driver 가 Codex 원본 사본을 둔다 (재실행 폴더에 `.FROM_CODEX.txt` 표지).

## 2. 한정

- 합성 픽스처 위의 관문 반례다 — 194 생산 · DEM · WSL 실덤프 · S3 를 돌리지 않았다.  release_gate 계열은 Codex 와 같이 상위 τ 재독해만 대역이다.
- **실제 WSL pilot ROOT 에서 단계 결합이 서는지는 아직 확인 전이다** (커밋된 보충 묶음에 케이스 기록이 없다).  관찰 (시험 아님): 10-07 14:15 WSL 스모크 기록의 같은 세 케이스 단계 목록을 고친 실행기의 표로 분류하면 분류 밖 0 · 실행 단계 = parser · contact (bimodal 2 · mono 1) · coverage · network_cli — 판정문 §3 의 케이스당 영수증 다섯 (워커 + 넷) 과 같은 모양.  pilot ROOT 의 기록은 옛 실행기 것이라 시도 사본 (stage_plan) 이 없고, 지금 케이스 기록 (봉인 판정 행의 시도) 으로 결합한다.
- 파생 탐침의 단계 목록은 손으로 넣은 것이다 (생산 워커가 싣는 꼴 · 10-07 스모크 기록과 같은 이름) — 워커가 거짓 단계 기록을 남기는 경우는 이 결합이 못 막는다 (판정문 §3 이 범위 밖으로 둔 "호스트가 모든 기록을 고친다" 부류).
- 봉인 32 파일 불변 — `code_fp` e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71 (고친 트리 · 핀 같음).  인계 도구 `scripts/g2_network_reread.py` 의 파일 지문은 바뀐다 (발사 때 manifest 에 기록).
