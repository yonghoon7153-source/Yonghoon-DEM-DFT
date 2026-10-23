# ULPR 독립 코드 재확인 v2 — 2026-10-23

판정: **검토한 코드 변경과 아래 재현 범위에서 신규 차단 결함 없음**. 이전 F1 정상 재개 오거부 및 기존 G2 헤더/G2c 시점 반례가 해소되었다. 문서·봉인·발송 패키지는 작성 중이므로 이 판정에 포함하지 않는다. 본 실행·물리 검증·외부 배포 GO가 아니다.

입력은 `/workspace/.cloud-setup/nonrint/ulpr-review-v2.diff`와 실제 적용 코드뿐이다. 구현자 보고·노트는 읽지 않았다. 이전 `REPORT.md`와 검토판 증거를 수정하지 않고 `v2/` 아래에 새 증거를 보존했다. tracked 파일 수정·commit·push·외부 LIGGGHTS/GPU 실행·전체 저장소 게이트는 하지 않았다.

| 검토 사본 | SHA256 |
|---|---|
| `v2/ul_reader.reviewed.py` | `34b46ebcf4530989917493f20d2d953043209e36d89e6b8282a2d629050a078d` |
| `v2/ul_gates.reviewed.py` | `c8d45a9cf75f0806e612d810942d23adea4b40feaa5f31f7d279eb8386358de6` |

## 기존 반례 재현

이전 재현기 `deck_probe.py`, `restore_probe.py`, `edge_probe.py`를 수정하지 않고 새 OUT에서 실행했다.

| 반례/대조 | v2 관찰 |
|---|---|
| CSV 꼬리 없는 정상 재개 k=0/1/2/3 | 생성 덱 실제 RESUME 제어 분기 모두 RM_STOP, abort 없음. 실제 arm CLI 4건 모두 OK, rho=0.20260778734286913. F1 해소 |
| BOX 첫 줄 nan/inf, 한 숫자, 빈 줄 | restore VALUE_MISMATCH, UB gate rc2 |
| `ITEM: ATOMSGARBAGE` | restore VALUE_MISMATCH, UB gate rc2 |
| G2c 시험 파일 TIMESTEP만 S0+1 | restore VALUE_MISMATCH, UB gate rc2 |
| 정상 복원 | RESTORED, restore/gate rc0 |
| c26 필수 열 결손 | NOT_COMPUTED/UNCONFIRMED, restore/gate rc2 |
| G2 중복 ID, NaN, 짧은 추가 행, 양쪽 같은 오시점, 수치 같고 원 토큰만 다른 값 | 모두 거부 유지 |

증거: `v2/deck-probe/deck_probe.json`, `v2/restore-probe/restore_probe.json`, 각각 실제 CLI 로그.

## 새 resume_tail 출력과 소비 경로

`v2/downstream_probe.py`는 기존 소형 합성기로 별도 UB/UT/UVa 및 비교 침대를 구성한다. UB의 k=4에서 주 교차·확인 둘을 완료한 뒤, k=5 옛 단과 창만 남기고 k=4에서 RESUME하여 새 창을 쓰기 전에 중단한 상황이다. 새 `_unfinished_resume` 시험 helper는 사용하지 않았다.

실제 production `arm`, `select`, `report`, `gate UVa`, `gate G_UB`를 실행했다.

- UB 첫 주 값 OK/rho=0.2026077873428664 보존. `resume_tail.status=UNCONFIRMED`, 경계 k=4.
- `union_bracket_pct`, `nonmonotone`, 최종 분리·표면 관측은 미확인으로 남는다.
- 선택은 유효한 첫 주 값으로 계산하며 최종 tuple을 얻는다. UVa(실행 전) 및 G_UB 관문은 승인된 기존 RM/주값에 따라 동작한다.
- 실제 report의 B73 관련 네 쌍은 모두 UNIDENTIFIED. `rank_eligible=True`가 남아도 `pair_table`은 union 존재까지 요구하므로 순위 관계를 발행하지 않는다. `rank_eligible` 한 필드만 순위 인증으로 해석하지 않아야 한다.
- 모든 위 CLI rc0, 예외 없음. 원 CSV 3개 SHA256 불변.
- 추가 대조: 승인 경계 앞 교차 끝점 atom의 fz를 NaN으로 바꾸자 실제 arm CLI는 UNIDENTIFIED/rho=null, S3 사유 유지. 꼬리 격리가 정상 관측 검증을 우회하지 않았다.

증거: `v2/downstream/downstream.json`, `v2/downstream/bad_prefix.json`, 실제 CLI 로그. 읽은 후속 소비자는 `selection`, `selection_state`, `gate`, `_has_event`, `pair_table`, `_t3_entry`, `report`, `_aux_eps_w`, `_read_run_cont`다. 이 fixture는 일반 UB 불명확 꼬리를 검사하며 UTc 새 물리 궤적까지 실행한 것은 아니다.

## 자체 시험 및 독립 변이

v2 baseline의 실제 출력에서 reader **214개**, gates **202개**가 통과했다(각 rc0, 실패 0). 로그는 `v2/reader-baseline.log`, `v2/gates-baseline.log`.

추가 독립 변이는 tracked 파일 대신 메모리 모듈을 바꾸었다. 네 변이 모두 실행 예외 없이 해당 새 단언에서 실패했다.

| 변이 | 예상 단언 실패 수 |
|---|---:|
| `resume_uncertain` 출력 생성을 제거 | R37 1 (완료한 주 값 보존 실패) |
| 격리 뒤 전체 union/nonmonotone 미확인화를 제거 | R37 1 |
| BOX 비유한 검사 제거 | C6 36 |
| BOX 하한<상한 검사 제거 | C6 6 |

증거: `v2/focused-mutations/focused_mutations.json` 및 개별 로그. 이 네 변이는 전체 변이 공간의 완전성을 뜻하지 않는다. 이전 v1의 12종 변이 결과는 기존 보고에 보존되어 있으며 이번 판에서 재실행했다고 주장하지 않는다.

## 남는 한정

- 기존 RESUME k=`3.49` 사전 반올림은 여전히 `(3,3410000)` 승인으로 읽힌다. NaN/inf/넘침은 거부한다. 이는 v2가 변경하지 않은 `_i`/사건 파싱의 잔여이며 새 R38 시험이 소수·유니코드 입력 전체를 거부한다고 해석하면 안 된다. `edge_probe`는 승인 집합만 관찰하므로 잘못된 최종 물리값 승인을 입증한 것은 아니다.
- 덤프 검증은 완료되어 바뀌지 않는 직교 덤프를 대상으로 한다. BOX 수치나 PBC 표지를 고정하는 물리 인증, 동시 파일 갱신의 원자성, 모든 임의 파손 형식의 차단을 검증한 것은 아니다.
- 문서·봉인의 최종 보장 문장과 시험 수 정합은 별도 최종 입력으로 확인할 사항이다.

## 이식 가능한 재현

모든 재현기는 `--repo`, `--out`을 받는다. `$REVIEW`는 기존 보고서/재현기를 복사해 둔 폴더, `$OUT`은 checkout 밖 새 폴더다.

```bash
python -I "$REVIEW/deck_probe.py" --repo "$REPO" --out "$OUT/deck-probe"
python -I "$REVIEW/restore_probe.py" --repo "$REPO" --out "$OUT/restore-probe"
python -I "$REVIEW/edge_probe.py" --repo "$REPO" --out "$OUT/edge-probe" --fixtures "$OUT"
python -I "$REVIEW/v2/downstream_probe.py" --repo "$REPO" --out "$OUT/downstream"
python -I "$REVIEW/v2/focused_mutations.py" --repo "$REPO" --out "$OUT/focused-mutations"
```

변이 재현기는 v2 소스 문자열이 정확히 한 곳 존재하는지 확인한다. 이후 수정판에서 해당 문구가 바뀌면 검토 대상 불일치로 멈출 수 있다.
