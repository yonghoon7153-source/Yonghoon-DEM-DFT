# R14 해제조건 10건 — 종결 기록 (2026-08-30, **제출 전**)

대상: LHS 저-φ_AM 확장 배치 v2 (64점).  판정 원문 = Codex R14 `SUBMIT HOLD`.
⚠ **아직 한 점도 돌리지 않았다.**  이 문서는 재판정을 받기 위한 것이고, 제출은 그 뒤다.

봉인:
| | |
|---|---|
| 설계 CSV | `docs/data/lhs_ext_design_v2_20260829.csv` |
| **sha256** | `bc72b8bf274842b7c54e319ceac70f5cb2804aa3635f329dfed34697bd52ea19` |
| 상자 + 출처 | `docs/data/lhs_ext_box_v2_20260829.json` (130/130 파싱 · 못 읽음 0) |
| 사전등록 | `docs/reviews/lhs_extension_prereg_v2_20260829.md` (v1 폐기) |

★ **좌표는 다시 뽑지 않았다.**  R14 가 "좌표 설계는 PASS, 재추첨 불필요" 라고 판정했고,
그 뒤 바뀐 것은 `seed` 열 하나뿐이다 (61행) — 열 단위 대조로 확인했다.

## 조건별

| # | 조건 | 무엇으로 닫혔나 | 검증 |
|---|---|---|---|
| 1 | 64개 서로 다른 소수 seed · 재봉인 · `--verify` 소수검사 | 뽑힌 값을 **그 이상의 미사용 최소 소수**로 올리는 결정론적 사상.  `rng.randint` 호출은 안 옮겼다 (옮기면 좌표가 전부 다시 뽑힌다) | 64/64 소수 · 중복 0 · 합성수 1개 심으면 `rc=1` |
| 2 | 같은 2계수 벌점우도로 profile CI | 후보 `φ_c` 를 `β=(−b·φ_c, b)` 로 제약하고 **원래 목적함수**에서 `b` 만 최적화 | `D(φ̂) = −1.1e-14` (옛 판 −0.459) · 전 구간 `D ≥ 0` · 위반 시 구간 미발행 |
| 3 | `ALL_ZERO/ONE` → `NOT_IDENTIFIED` | hard 부등식 제거.  점추정도 경계도 안 낸다 | selftest 가 반례를 **계산**한다: 참 `φ_c=0.48` 이 창 안인데도 `P(all zero)=0.062` |
| 4 | frozen 64 ID·SHA 를 적합기에 fail-closed 연결 | `--design` 이 **필수**.  결과 없는 ID 는 자동 `unresolved` → §4-4b 양극단 sensitivity | 실패행을 지운 CSV 로 재현 — 누락 ID 가 편입되고 양극단이 돈다 |
| 5 | 비수렴 시 `FIT_FAILED` | Firth 비수렴 · 프로파일 건전성 위반 둘 다 점추정·구간 없이 종료 | selftest |
| 6 | `--verify` 불변식 + **절대 cell** | ID 집합 · 층별 8행 · 층마다 6/1/1 · `ntype↔kind` · `w합 = 1−pdd` · 상별 입자수 · seed 소수·범위 · **봉인 해시 강제** · 상자로 절대 칸 복원 | R14 가 통과시킨 변이체 **5종 전부 `rc=1`**, selftest 상주 |
| 7 | 130점 source manifest | `--box-out` 이 상자와 **파일별 sha256 130건**을 함께 봉인 | 130/130 파싱 · 못 읽음 0 |
| 8 | 실제 덱 dry-run + parser 왕복검사 | `lhs_ext_materialize.py` — 실물 덱 2개를 템플릿으로, 생성분을 **본문에서** 되읽어 CSV 와 1:1 대조 | **64건 불일치 0** |
| 9 | plain mass-based PDD · 밀도 · mono 상 사상 | 실물 덱에서 확인: `particledistribution/discrete` plain · `4800`/`2000` · 가중 합 1 | 아래 §상 사상 |
| 10 | LF 규약 · package SHA | `.gitattributes` 가 csv/json/md/py/sh 를 LF 고정 | `git check-attr` = `eol: lf` |

## 상 사상 — R14 P1-06 의 답

실물 덱에는 **AM_P / AM_S 구분이 없다.**  둘 다 `density 4800` 이고 **반지름만 다르다**:

```
3-type: pts1 AM_P(4800, ${r_AM_P}) · pts2 AM_S(4800, ${r_AM_S}) · pts3 SE(2000, ${r_SE})
        가중 = w_AM_P  w_AM_S  pdd_SE
2-type: pts1 AM  (4800, ${r_AM})   · pts2 SE(2000, ${r_SE})
        가중 = w_AM_P  pdd_SE
```

⇒ CSV 가 `mono_AM_S` 를 `w_AM_P`·`rP_um` 열에 담는 것은 **"P 열 = 일반 AM 자리" 규약이
맞고**, 열 이름대로 읽는 쪽이 오해다.  왕복검사는 이름이 아니라 **밀도로 AM/SE 를 가르고
반지름으로 정렬**해 이 규약을 못박는다.  음성 대조 통과: 두 AM 가중 교환 · 반지름 하나
변조 · 본문 seed 가 헤더와 갈림 · SE 밀도를 4800 으로 — **전부 잡는다.**

## 런 전에 잡힌 것 둘 (그대로 나갔으면 사고였다)

1. **`seed=` 가 덱에 두 번 적힌다** (헤더 · `print INSERTING`).  "정확히 1번" 규칙이
   **거부**해서 멈췄다 — 안 그랬으면 헤더는 새 seed, 본문 안내는 옛 seed 인 덱이 64개.
2. **가중 합이 6건에서 `0.999999`/`1.000001`.**  6자리 반올림이 덱으로 새어 들어간 것.
   ⚠ 허용치를 늘리는 것은 오답이다 — 검사만 조용해지고 덱은 그대로다.  마이크로 단위
   정수 배분 + 잔차를 SE 로 → 찍히는 문자열이 정확히 `1.000000`.
   근거: 기존 130 덱이 전부 정확히 1 이고, 08-18 에 **비소수 seed 로 25건이 즉시 abort**
   한 전례가 있다 (`docs/lhs_design_dataset_20260818.md` §P-1).

## 아직 아닌 것 — 제출 전 남은 실무

- **`run_lhsx_*.sh` 미생성.**  지금은 `input_*.liggghts` 만 만든다.
- **`submit_chain.sh` 가 `--dependency=afterany`** 다.  08-18 에 25건이 죽었을 때 그것을
  **조용히 지나간** 구조가 이것이다.  64점 제출 시 `RUNNING+COMPLETED+CANCELLED = 총수`
  를 상시 확인할 것 (`~/lhs_watch.sh`).
- **재시작은 있다** — `restart_settling_*.bin` 이 5만 스텝마다 쓰인다.  SLURM 5일 벽에
  걸려도 잃는 것은 최대 5만 스텝이다 (완주 최장 실측 `4-02:36`).

## 재판정 요청

위 10건에 대해 **런 전** 재판정을 요청한다.  `SUBMIT GO` 로 바뀌면, R14 가 적은 해석
범위를 그대로 지킨다: *"finite-box LHS nuisance 분포의 marginal transition 탐색"*.

재현 (리포만으로):
```bash
bash scripts/check_all.sh                      # lhs_ext_design 봉인 검사 포함
python3 scripts/lhs_perc_fit.py --selftest
python3 scripts/lhs_ext_materialize.py --selftest
```
