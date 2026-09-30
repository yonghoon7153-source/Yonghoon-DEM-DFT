# 합리성 검사 스크립트 — `../lhs_coverage_reasonableness_20261001.md` 를 만든 것 (반입 10-01 · J20-m)

서브에이전트가 scratchpad 에서 쓴 스크립트를 경로만 리포 기준으로 바꿔 옮겼다 (계산 무변경).
입력 = `docs/data/{lhs,lhsx}_{descriptors_cov,webapp_coverage}_1e09f661d/` · 설계 CSV 둘 · `docs/data/case_master.csv` (읽기만).

```
export COV5_WORK=$(mktemp -d)          # 중간 산출 (리포 밖 · 없으면 임시 폴더/cov5_work)
python3 cr_load.py && python3 cr_checks.py && python3 cr_trends.py && python3 cr_tables.py && python3 cr_report.py
# → $COV5_WORK/cov5_reasonableness.md
```

- **재현 확인 (10-01, 이 컨테이너)**: 위 명령의 산출 `cr_checks.json` · `cr_trends.json` · 표 넷 · `cov5_reasonableness.md` 가 원 scratchpad 산출과 **바이트 동일** —
  커밋된 보고서는 그 md 에 반입 머리 인용 블록 (`> **반입 10-01 …**`) 만 더한 것이다.
- `cr_tab_order_compact.md` 는 스크립트가 만들지 않는다 (서브에이전트가 `cr_tab_order.md` 를 손으로 줄인 표) — 고정 입력으로 여기에 둔다.
- `cr_checks.json` · `cr_trends.json` = 원 산출 사본 (보고서 수치의 근거).  필요 모듈: numpy · scipy (`spearmanr`).
