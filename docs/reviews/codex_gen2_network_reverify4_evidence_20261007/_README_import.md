# Codex 세대 2 재검증 4 — 증거 반입 기록 (10-07)

- 판정문 = `docs/reviews/codex_review_gen2_network_reverify4_20261007.md` (ZIP 안 같은 이름 파일 **바이트 그대로** · 24,788 B · sha256 `8dc162ac51bc606919c932ecee0d7d949d3c608b090e930c432cff4dbba4e03f` 같음 · 안에 아무것도 덧붙이지 않았다).
- 원 ZIP = 1저자 업로드 `verify_evidence.zip` (9,068,015 B · sha256 `40882981385b35526dcc1b8318c8629d493afc48a0f488fd89e33e684adf54ff` · 1,075 항목 = 파일 889 + 폴더 186 · 풀면 29,822,802 B · 절대 경로 · `..` · 심볼릭 링크 0).
- 핀 = `87f0906a2674e7d4e8ec31ca98aed5b14babc293` (재검증 4 요청서 · 사전 점검 보충 묶음이 들어간 커밋).
- 1저자 10-07 *"같이 병행해서 진행해용"* = 반입 + 수정 (반례 먼저) 병행.

## 1. 이 폴더에 넣은 것 · 뺀 것

| 넣음 (파일 480 · 2,325,396 B) | 뺌 (원 ZIP 에만 · `bundle_inventory.json` 에 경로 · 크기 · sha256 · kept 표지) |
|---|---|
| `README.md` (Codex 묶음 설명 원문) · `verify_evidence.py` · `run_checks.py` · `probes/` (다섯 탐침 — release_gate · submitted_evidence · observation_cli · case15_channels · scope194) · `source_manifest.json` (448 항목 blob · sha256 · 크기) · `bundle_inventory.json` (889 파일) | `source/` (110 파일 · 8.2 MB — 우리 git 의 핀 바이트와 같음 · 아래 §2) |
| `evidence/*.json` · `evidence/*.log` (탐침 · 시험 결과 전부 — 판정문 §1–§7 의 근거 표 · `release.log` = Codex 의 133 PASS · 2 FAIL 원 로그) | `evidence/release_gate/` 의 합성 배포 묶음 (`TEST_ONLY_NOT_A_GO` 표지의 가짜 인계 CSV · 미리보기 PNG · 변이별 reread · 감사 · manifest — 탐침이 결정적으로 다시 만든다) — **최종 실행 `run_2yz1esm0/` 의 변이별 `build.log` 여덟만** 넣었다.  같은 폴더 위의 첫 실행 사본 (변이 8 · `build.log` 전부 0 B · 판정 JSON 없음 · 산출 `out/` 이 생긴 변이 = 최종 실행과 같은 넷) 도 뺐다 |
| `evidence/observation_cli/` (G2RR4-02 반례 ROOT 넷 — 5/5 · 5/4 · 4/4 · 2/2 · 실제 audit JSON · 원 로그) | `submitted/` — 1저자 WSL 묶음 둘의 풀린 사본 = 리포에 커밋된 tar (`docs/reviews/codex_gen2_network_reverify4_precheck_20261007/g2pre_c3117438a_1007_1415.tar.gz` · `…/g2pre_extra_c3117438a_1007_1415.tar.gz`) 의 항목과 9/9 · 40/40 바이트 같음 |
| `evidence/receipt_path_translation/` · `evidence/obs_*/` (submitted_evidence 탐침의 경로 번역 사본 · 함수 수준 변이 여섯) — ⚠ **Codex 가 WSL 경로를 Windows 검토 경로로 바꾼 사본**이다 · 실행 증서가 아니다 (판정문 §3 · 원 영수증 = 커밋된 tar) | ZIP 의 submitted/request.txt (8,320 B · sha256 `cd1181644d1d…`) = 1저자가 Codex 에 붙여 넣은 요청서 렌더링 — 핀의 `docs/reviews/codex_gen2_network_reverify4_request_20261007.md` 와 Markdown 기호 · 공백을 빼면 같은 글 (4,137 자 같음) |
| `fixtures/seal_baseline/` (observation_cli 탐침의 입력 · 재검증 3 Codex 합성 1 케이스 ROOT · 탐침이 manifest `repo_root` · `worker_script` · 수확 · 코호트를 자기 자리로 고쳐 쓴다 — 우리 쪽에서 다시 만들 탐침이 없어 넣었다) | `prepare_source.py` · `source_plan.json` · `extra_plan.json` · `package_review.py` (Codex 쪽 취득 · 포장 기록) |

같이 올라온 ZIP 둘 (`lhs_descriptors_cov_1e09f661d.zip` sha256 `5150fd697055…` · `lhs_handover_20261001.zip` sha256 `7cdd2a21c36f…`) = Codex 에 준 **입력 묶음** —
파일 209 · 127 (= 336) 전부 핀 `87f0906a2` 의 리포 파일 (`docs/data/…` · `docs/reviews/…` · `docs/area_contract_20260913.md`) 과 바이트 같음 ⇒ 반입하지 않는다.

## 2. 우리 트리 재현 (10-07 · Linux · Python 3.11.15 · numpy 2.4.6 · scipy 1.17.1 · networkx 3.6.1)

- 소스 = `source_manifest.json` 의 448 항목을 우리 git 에서 `git archive 87f0906a2` — ⚠ 448 = **고유 경로 446 + 중복 2** (`docs/data/lhs_perc_audit_20261001/{lhs,lhsx}_20261001_d1ec42fba/perc_audit.tsv` 가 두 번 · Codex 판정문 §1-1 의 "448파일" 은 항목 수) ·
  blob sha1 · sha256 · 크기 448/448 같음.  ZIP 의 `source/` 사본 110 (scripts 86 · webapp 22 · AGENTS.md · CLAUDE.md) 도 sha256 110/110 같음 (docs 338 은 ZIP 에 없었다 — 우리 git 에서).
- `submitted/` = 핀의 사전 점검 tar 둘을 우리가 풀어 만든 것 (`prepare_source.py` 와 같은 규칙 · 경로 · 타입 검사) · `fixtures/` = ZIP 그대로 · 탐침 원본 무변경.
- 실행 = 재현 묶음 (스크래치) 밖 CWD 에서 `python3 -I <R>/run_checks.py submitted_evidence scope194 case15_channels release_gate` → `… observation_cli` → `… reread publication role release` (Codex README 순서) ·
  `python3 -I <R>/verify_evidence.py`.  `evidence/wsl_code_identity.json` 은 Codex 탐침이 없어 우리 git 으로 직접 다시 만들었다 (WSL `c3117438a` ↔ 핀의 다섯 도구 blob).
- 결과 = **판정값 차이 0** (정규화 = 경로 문자열만 · Codex Windows 묶음 뿌리 ↔ 우리 재현 뿌리):

| 탐침 · 시험 | 대조 | Codex | 우리 |
|---|---|---|---|
| release_gate (**G2RR4-01**) | 실제 `build_v13` → `check_v13` 8 변이 (상위 τ 재독해만 대역) | control 생성 · 문제 0 · reread 없음 · n_fail null · 감사 input_problems · manifest_sha256 다름 = 거부 · **meta M2 ok=false (n_fail 0) · cases=[] · meta=[] · 감사 내부 관측 truncated/outside = 생성 · 문제 0** | 같음 (거부 메시지 문자열 · manifest sha256 앞자리 `ecea559da6f258d1` 까지 같음 · 다른 것 = artifact_root 경로만) |
| submitted_evidence | WSL manifest ↔ reread manifest sha256 · 봉인 32 · 인계 도구 · 훅 사본 · 영수증 15 = 15 · 완료 시도 3 · 모듈 30 ⊆ 32 · reread 상세 3 · 함수 수준 변이 여섯 | 같음 · 끝만 소실 = 문제 · **파서 쌍 소실 = 문제 0 (14/14)** · 솔버 쌍 소실 = network_solver 문제 · 빈 끝 = 문제 · 신원 = 문제 · 실패 시도 미최종 = 문제 0 (16/15) | 같음 (차이 0 · code_fp `e8b2496b…`) |
| observation_cli (**G2RR4-02**) | 실제 audit CLI · 합성 1 케이스 ROOT + 번역 영수증 | all5 rc 0 (5/5) · 파서 끝만 없음 rc 1 (5/4) · **파서 쌍 없음 rc 0 (4/4) · 워커 + 솔버만 rc 0 (2/2)** | 같음 (차이 0) |
| case15_channels | 원 gzip · STL 직접 6 조합 | 판 19.1455 µm · 100 × 100 µm² · 원자 65,970 · 접촉 182,995 · 음수 면적 **2 행** (31–29241 −0.186036 · 38–29241 −0.186264 µm²) · 전자 둘 · Hertz 열 B∩T `[24, 40, 57, 103]` · Physics 열 ValueError · 이온 σ_ratio H0 0.0003263508259103751 · physics 0.00036224724452177176 | 기하 · 행 · ID · 오류 같음 · 이온 σ_ratio 0.00032635082552669387 · 0.00036224724407936984 (상대 1.2e-9 · 8 자리 같음) · 보존 잔차 1.90e-9 · 5.09e-9 (Codex 3.00e-9 · 6.32e-9 · 둘 다 문턱 1e-6 안) — CG 끝자리 · **비트 동일 주장 안 함** |
| scope194 | 194 기존 감사 · 수확 기록 재집계 | L0 130 · 64 · 겹침 0 · 접촉 행 18,111,468 + 14,694,721 = 32,806,189 · 음수 · 0 · 고아 · 비유한 0 · 교차대조 불일치 0 · 최소 L−4r_max +1.4697 (lhs00_075) · −6.0611 µm (lhsx_045) | 같음 (차이 0) |
| `g2_network_reread --selftest` | — | rc 0 · 17 | rc 0 · 17/17 |
| `test_gen2_publication_handover` · `test_gen2_role_contract` | — | 32/32 · 44/44 | 32/32 · 44/44 |
| `test_lhs_release_v13` | — | 133 PASS · 2 FAIL (V10a Windows `/H/lhsx` 표기 · V16a `.git` 없는 사본) | **134 PASS · 1 FAIL** (V16a 만 — git archive 사본에 `.git` 없음 · V10a 는 Linux 에서 통과) |
| `verify_evidence.py` | 증거 ↔ 서술 일관성 | 25/25 | 24 PASS · 1 FAIL — FAIL = "release regression reports exactly two qualified fails" (위 줄의 환경 차이 그대로) |

- ⚠ 이 재현은 **Codex 탐침이 핀 코드에서 같은 판정을 낸다**는 확인이다 — 194 생산 · WSL 실덤프 · S3 를 다시 돌린 것이 아니다 (판정문 §1-1 의 한정 그대로).
- 원장: `G2RR3-01` = verified (원 반례 · 범위 = `verified_scope`) · `G2RR3-02` = 재개방 (부분 — 닫는 조건 = G2RR4-02 검증) · 새 `G2RR4-01` · `G2RR4-02` (P2 · open) · `G2RR4-03` (P3 · open) ·
  `SELF-92` · `GEN2-04` 메모 (음수 면적 **두 행** · Physics 는 첫 행에서 멈춘다) · 새 `SELF-94` (요청서 §4 · 사전 점검 README 의 "전체 출력" 과잉 일반화 — 판정문 §5) — `docs/reviews/findings.json`.
