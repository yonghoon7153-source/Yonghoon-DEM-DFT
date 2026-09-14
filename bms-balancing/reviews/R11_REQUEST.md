# 적대적 리뷰 요청 — 11차 · α·β 검증 하네스 (`bms-balancing/`)

10차(대상 `bd6ba47`, 코드 정본 `554dad6`)는 **NO-GO** (P1 8 · P2 7, `reviews/R10_CODEX.md` · 패키지 `reviews/r10_repros/codex/`
sha256 10/10). 열다섯 건 전부 수정 전 clean 트리에서 재현 → RED(`tests/test_r10_codex.py` d10_01~16) → 수정 → GREEN 으로
닫았다 (`reviews/R6_LEDGER.md` "Codex R10"). 목표는 같다: **"정본이 우리 새 모델의 설계 근거로 쓸 만한가"**.
GO 기준: R3 §5 + R5 §4 + R6 출처 결속 + R7 §6 + R8 §6 + R9 최소 조건 6 항 + R10 최소 조건 7 항.

## 0. 대상

| 항목 | 값 |
|---|---|
| 커밋 | 이 파일이 든 커밋 (`git log -1`). 직전 리뷰 대상 `bd6ba47` |
| 브랜치 | `claude/bms-alpha-beta-verify` — `bms-balancing/` 만 |
| 정본 | `FINDINGS.md` + `out/` (+ `.meta.json`). **현행 out/ 12 개는 provenance-incomplete** (§4) |
| 저장소에 없는 것 | 원본 MATLAB · 원자료 xlsx · 문헌 OCP → `BMS_DATA_ROOT` |
| 10차 대비 새것 | P1-1~8 · P2-1~7 닫음 · 게시 전 완전성 판정(matrix·profile·ne_shape typed status) · 역할을 묶는 receipt · U18 gate 에 env/control/독립성 · `reviews/evidence_gate.py`(러너 공용 봉인) · `D.HALF_CELL_ABSENT` |
| 증거 커밋 규약 | 러너는 **expected commit 을 materialize** 해서 돈다. 도구 자신도 그 커밋의 blob 이어야 `evidence_eligible: true` 이므로, 증거는 **코드 커밋 `665c87e` 에서** 만들어 그 다음 커밋들에 얹는다. `git diff 665c87e HEAD --name-only -- '*.py' '*.sh'` 는 **0 개** — 코드는 그대로이고 뒤 커밋은 증거 파일과 그 결과를 적은 문서(`R6_LEDGER.md` · `WORKING_STATE.md` · 이 파일)뿐이다 |

```bash
git clone -b claude/bms-alpha-beta-verify https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT
cd Yonghoon-DEM-DFT/bms-balancing && git checkout <이 파일이 든 커밋>
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python3 -m pytest tests/ -q                # 183 passed 기대. 원자료 불필요
bash matlab/tests/run_all.sh               # Octave 없으면 4·5 단계만

git archive --format=tar bfc4623^ bms-balancing/out | tar -x -C /tmp/r11base      # 과거 baseline
export R6_OLD_OUT=/tmp/r11base/bms-balancing/out
HEAD=$(git rev-parse HEAD)

python3 reviews/r6_repros/codex_r6_mutation_audit.py            # 8/8 CAUGHT · MISSED 0
python3 reviews/r6_repros/codex/replay_codex_r6_adapted.py --target .   # R6 적응판 "mode": "full" 6/6
python3 reviews/r6_repros/codex/mutation_adapted.py             # 5/5 CAUGHT
python3 reviews/r7_repros/replay_codex_r7.py --target . --expected-head "$HEAD"   # 6/6 · 격리 snapshot
python3 reviews/r9_repros/replay_codex_r9.py --target . --expected-head "$HEAD"   # 12/12 · 격리 snapshot
# 10차 패키지 그대로 (수정 **전** 을 재려면 bd6ba47 worktree 에서):
python3 reviews/r10_repros/codex/r10_snapshot_repros.py  --target . --case all
python3 reviews/r10_repros/codex/r10_u18_shape_repros.py --target . --output /tmp/r11_u18.json
python3 reviews/r10_repros/codex/r10_evidence_repros.py  --target . --case all
python3 scripts/check_u14.py --new out --schema-only            # rc 2: provenance-incomplete (§4)
```

⚠ 두 러너는 이제 **격리 snapshot** 에서 돈다 (`--allow-dirty` 는 개발용이고 결과에 `evidence_eligible: false` 가 박힌다).
`python -O` 에서는 아예 증거를 만들지 않는다 (보관 probe 의 반례가 `assert` 라서).

## 1. 검증 — 방금 실행

| 검사 | 명령 | 출력 |
|---|---|---|
| 전체 회귀 | `python3 -m pytest tests/ -q` | `183 passed in 146.56s` (이 컨테이너, `replay_ours_after_fixes/pytest_full.txt`) |
| MATLAB 스모크 (Octave) | `bash matlab/tests/run_all.sh` | `PASS — 실패 0: []` · `전부 통과` (`replay_ours_after_fixes/matlab_smoke.txt`) |
| 변이 감사 (우리 테스트) | `codex_r6_mutation_audit.py` | `8/8 CAUGHT · MISSED: 0` · 복구 뒤 `7 passed` (`replay_ours_after_fixes/codex_r6_mutation_audit.txt`) |
| 적응판 변이 감사 | `mutation_adapted.py` | `5/5 CAUGHT · MISSED: 0` · baseline·복구 6/6 닫힘 (`replay_ours_after_fixes/mutation_adapted.txt`) |
| R6 적응판 재생 | `replay_codex_r6_adapted.py` | `"mode": "full"` 6/6 닫힘 (`replay_ours_after_fixes/replay_codex_r6_adapted.json`) |
| R7 닫힘 재생 | `replay_codex_r7.py --expected-head <코드 커밋>` | 6/6 **도달 True · 반례 소멸** · `evidence_eligible: true` · `instrument_sealed: true` · `ran_in: 격리 snapshot` |
| R9 닫힘 재생 | `replay_codex_r9.py --expected-head <코드 커밋>` | 12/12 **도달 True · 반례 소멸** · `evidence_eligible: true` · `instrument_sealed: true` · `ran_in: 격리 snapshot` |
| **10차 패키지 재실행 (수정 뒤)** | 위 세 스크립트 | `reviews/r10_repros/replay_codex_r10.py` 로 22/22 닫힘 — snapshot 6 + u18 5 는 **자기 반례 assertion** 에서 멈추고, evidence 7 은 flag(`false_positive`·`false_clean`·`false_identity`×2·`mutant_survived`·`corrupt_package_accepted`·`claim_gap`)가 전부 False, 적응 2 는 positive closure. `snapshot:argv` 는 bash `$*` 의미 자체라 **우리 코드 밖**, `u18:shape_duplicates` 는 중복이 이제 거부돼 게시가 없으므로 **전제 변경**(적응 probe 가 닫는다) |
| 현행 정본 점검 | `check_u14 --new out --schema-only` | rc 2 — 출처 열 24 · profile `gamma_roster` 4 · **내용 4**(degeneracy 의 옛 `inputs_sha` 가 새 역할 결속 digest 로 재계산되지 않는다, §4) · `PROMOTION {"promotion_eligible": false, …}` |

## 2. R10 열다섯 건 — 재현과 수정

| ID | 수정 전 관측 | 수정 | 회귀 |
|---|---|---|---|
| **P1-1** | `--out X --compare X` 가 근거 X 를 제 출력으로 덮고 자기대조로 `complete` rc 0 | 쓰기 **전에** snapshot 을 읽어 그것만 비교기에; 같은 object(realpath/samefile)면 rc 2 | `test_d10_01` |
| **P1-2** | `--states 100` 이 2 행 canonical 을 1 행 `complete` 로 교체; `100,100` 은 2/2 | authority = `D.declared_states(source)`; `--states` 는 부분집합만, 그 실행은 `subset`·rc 3·canonical 금지; 중복·미선언 rc 2 | `test_d10_02` |
| **P1-3** | γ 하나 실패 → 1 행이 canonical 교체, rc 0, 실제 wrapper 서명·검증까지 통과 | γ roster 를 먼저 고정, `gamma_roster` 를 행에 봉인, complete 만 canonical, 부분 rc 3 | `test_d10_03` |
| **P1-4** | 전 조합 실패 → error 행 16 개가 canonical 교체, rc 0 | 기대 조합 roster 를 게시 전에, typed status, complete 만 canonical, rc 0/3/1 | `test_d10_04` |
| **P1-5** | `error=skip` 한 칸이 필수 셀·숫자·receipt 검사를 전부 끔 | success/error exact tagged union + 모르는 열 거부 | `test_d10_05` |
| **P1-6** | 역할 swap 이 같은 digest, decoy 하나가 provenance 로 통과 | `REQUIRED_ROLES` exact + `(역할, sha256)` 버전 digest | `test_d10_06` |
| **P1-7** | env 는 존재만, control 은 지우면 검사가 잠듦 | env 를 값으로 대고 필수 control 은 양쪽에 있어야 함 | `test_d10_07` |
| **P1-8** | 같은 디렉터리 자기대조가 승격 판정 | samefile/realpath 로 거부 rc 2 | `test_d10_08` |
| **P2-1** | subset 이 rc 0 | rc 3 + `PROMOTION {promotion_eligible…}` | `test_d10_09` |
| **P2-2** | stdout 모드 invalid 가 rc 0 | sink 무관 rc 2 + typed diagnostic | `test_d10_10` |
| **P2-3** | `$*` 평탄화 · 회귀가 `run()` 을 안 돎 | `"$@"` → JSON array, 회귀가 실제 `run()` + shim producer 통과 | `test_d10_11` |
| **P2-4** | `-O` 에서 모든 판정이 사라짐 | `-O` 자체를 거부, 판정은 `gate.need`, delegated rc 를 값으로 | `test_d10_12` |
| **P2-5** | status rc·assume-unchanged·ignored pyc | `evidence_gate`: git rc · skip flag 거부 · pycache 격리 · expected commit 의 sparse worktree · 도구 봉인 | `test_d10_13` |
| **P2-6** | digest 집행 삭제 변이가 회귀를 통과 | 회귀가 **실제 byte 를 손상**시켜 probe 미실행을 확인 | `test_d10_14` |
| **P2-7** | typed status 를 쓰는 caller 0 개 | `run_states.sh` 의 `shape_step` (production) + 회귀가 그 함수를 실행 | `test_d10_15` |

## 3. 10차 질문에 대한 답

| Q | 답 |
|---|---|
| 1 `--subset` | rc 3 + `promotion_eligible: false` + roster 를 `PROMOTION` 줄에 담았다. subset manifest 서명은 아직 — §5 |
| 2 degeneracy stdout | 우회로였다. 이제 sink 와 무관하게 invalid 는 rc 2 이고 bare artifact 대신 typed diagnostic 을 낸다. 시험용 objective 는 receipt 를 갖추도록 fixture 를 고쳤다 |
| 3 `ne_shape --states` | `requested_from` 기록만으로 부족하다는 데 동의. authority 는 `D.declared_states(source)` 이고 `--states` 는 좁히기만 하며 그 실행은 `subset`·비승격. 알려진 부재는 `D.HALF_CELL_ABSENT` allowlist (실측 근거는 원장) |
| 4 dirty runner | `--allow-dirty` 는 `evidence_eligible: false` 로 구조화했다. 기본은 **거부가 아니라 materialize** — 실행 bytes 를 commit 에서 가져오므로 worktree 상태가 오염원이 되지 않는다. status rc 비영은 즉시 오류 |
| 5 export 계약 | 방향(build 경계 typed snapshot, role-keyed manifest, sensitivity 는 A/B digest)에 동의. **아직 미구현** — §5·§6 Q3 |

## 4. 정본 범위 — 현행 `out/` 은 provenance-incomplete (+ 이번 라운드가 더한 digest 규칙 변경)

숫자는 그대로이고, 새 검사(명부·역할 receipt·조건·환경·중복·tagged union)에서 빠지는 것은 matrix/profile 8 개의 출처 열
24 건 + profile 4 개의 `gamma_roster` 4 건 + **degeneracy 4 개의 옛 digest** 다. 마지막 것은 이번 라운드가 만든 것이다:
`inputs_digest` 가 역할을 묶으면서 값이 달라져(그래서 `RECEIPT_SCHEMA_VERSION`) 옛 `inputs_sha` 가 재계산과 안 맞는다.
**숫자는 하나도 안 움직였고 바뀐 것은 규칙이다** — 소급해서 값을 고쳐 넣지 않는다 (그러면 그 digest 가 무엇을 증명하는지
사라진다). U18 재실행이 새 규칙으로 서명한다. 보강은 **U18** (사용자 기계 재실행, 별도 `OUT=`; 이제 gate 가 명부 12/12 ·
receipt 역할 · 조건 · 환경 · candidate/baseline 독립성 · exact equality 를 그 순서로 강제한 뒤에만 승격). 자기 점검
(`--new out --old out`)은 이제 rc 2 로 거부된다 (P1-8) — 현행 점검은 `--schema-only` 다.

## 5. 닫지 않은 것 — 신뢰 경계

| # | 무엇 | 왜 열어 두나 |
|---|---|---|
| export 계약 (R9 Q3 · R10 Q5) | 공유 workbook·문헌의 **공통 snapshot** 을 build 경계에서 강제 | 설계는 합의됐고 이번 라운드에는 안 넣었다. 패키지의 `shared_full_cell_mismatch_accepted` 는 여전히 `true` 다 (숨기지 않는다) |
| receipt digest 의 경로 | `(역할, sha256)` 만 해시하고 경로는 뺐다 | R6 내부 F4("같은 bytes 면 같은 실행", `test_i6p_04`)와 정면 충돌하기 때문. 근거는 원장, 판단은 §6 Q1 |
| subset manifest 서명 | `--subset` 의 기대 부분집합을 서명해 봉인 | 지금은 `PROMOTION` 줄에 roster 만 담는다 |
| typed `(root, state, si)` identity | 문자열 `state\|si` 유지 | R9 Q1 이후 그대로 |
| U16 · U17 · U18 | 사용자 기계 실측 | 전과 같음 |
| F01b · F08 · F2 · V6-09 · U2~U10 | 전과 같음 | — |

## 6. 질문

1. **receipt digest 와 경로**: 역할은 묶었고 경로는 뺐다 (`test_i6p_04` 와 충돌하므로). 경로까지 묶으라면 그 시험의
   전제("byte 가 같은 재-export 는 같은 실행")를 함께 바꿔야 하는데, 그 전제를 버리는 것이 맞는가.
2. **알려진 부재 allowlist**: `HALF_CELL_ABSENT` 를 코드 상수로 두고 근거를 원장에 적었다. 이것을 데이터 쪽(예: 원자료
   옆의 선언 파일)으로 옮겨야 하는가, 아니면 코드 상수가 정본으로 맞는가.
3. **export 계약의 범위**: build 경계에서 공유 입력을 한 번 읽어 주입할 때, `pristine`(기준)과 대상이 **다른 상태**라
   반쪽전지는 애초에 다른 파일이다. 공통 snapshot 을 강제할 대상은 풀셀 워크북 + 문헌 gr/si 셋으로 한정하면 되는가.
4. **`evidence_eligible` 의 정의**: 격리 snapshot + 패키지 digest + **도구 자신의 봉인** 세 가지를 요구한다. 도구 봉인을
   요구하면 "수정한 커밋의 증거는 그 커밋을 만든 뒤에만 만들 수 있다" 가 되는데(그래서 코드/증거 두 커밋), 이 규약이
   맞는가 아니면 도구는 별도 축으로 빼야 하는가.
5. **partial namespace 의 수명**: `partial/` 에 쌓이는 산출을 언제 지우는가 — 지금은 아무도 안 지운다. 같은 이름의 다음
   부분 실행이 그 자리를 덮는다 (canonical 은 안 건드린다). 이 정도로 충분한가.

## 7. 실측 첨부

- `reviews/R10_CODEX.md` · `reviews/r10_repros/codex/` (패키지 10 파일) · `reviews/r10_repros/replay_ours_bd6ba47_before/`
  (수정 전 재현 — 세 스크립트 rc 0) · `reviews/r10_repros/replay_ours_after_fixes/` (수정 뒤).
- `reviews/evidence_gate.py` (러너 공용 봉인) · `bms_balancing/schema.py` (스키마·역할·환경 정본) · `reviews/R6_LEDGER.md`
  "Codex R10" 절.

## 8. 이후

GO 면 새 모델 설계 요구서(`docs/`) 초안 — §5 다섯 행 + R8 Q6 의 열 구조 (다섯 관측은 provenance-incomplete 잠정 관측으로
표시). U16·U17·U18 은 사용자 기계 실측. export 계약(Q3)은 합의 뒤 구현.
