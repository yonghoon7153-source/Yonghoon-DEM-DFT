# Rint ② R 운영 + 코팅 과정 DEM → agy 실무 창 (2026-11-26 · Claude 서브 세션 → agy · 한 방향 넘김)

1저자 11-26: *"Rint도 안티그래비티한테 넘기면 될듯 우선"* · *"코팅은 안티한테 맡기기로 했잖아"* · *"Rint, 코팅을 안티에서 해야지"*.
⇒ **agy 실무 창 ("DEM 실무") 의 일 = 둘** — ① **Rint ② R 운영** (명령 블록 · 판독 · 기록 · 1순위 · 기한 12-05) ② **코팅 과정 DEM 가능성 메모** (아래 §5 · 문서만).  Rint 블록을 띄우고 런을 기다리는 사이에 코팅 메모를 쓴다 — Rint 화면이 오면 Rint 먼저.
한 방향 넘김 (relay 스킬 §6-1): Claude 가 돌아와도 1저자가 정하기 전까지 두 일의 주인은 agy.  Codex 실무는 이 둘을 하지 않는다 (Codex = 수영 · 믹서 · ibb 판독).

## 0. 먼저 읽기 (차례)

1. 같은 꼴의 지난 넘김 쪽지: `docs/collab/claude_to_codex/20261121-1600_rint2-to-codex-practice.md` — §0 읽을 것 · §2 차례 (7 합치기 · 8 주 판정 · 9 감도) · §3 지킬 것 · §4 기록.  'Codex' 를 'agy' 로 읽는다.
2. 운영 기록: `docs/data/rint2_r_ops_20261121/README.md` (11-25 밤 · 11-26 절 = 바로 앞까지).
3. 부록 팔 등록: `docs/reviews/rint2_middle_arm_ptfe05_sdcp0_registration_20261124.md` (§3 ② 침대 점검 · 칸 차례).
4. 봉인 문서는 봉인 가지에만: `git show origin/claude/rint2-seal-20261118:docs/reviews/rint2_seal_20261118/registration_R_sealed.md`.
5. 편성 규칙: `.claude/skills/relay/SKILL.md` (처음 이름 orca → relay) (B 가지 · push 뒤 — 아직이면 이 쪽지와 1저자 말이 앞선다).

## 1. 지금 상태 (11-26 15 시 KST)

| 항목 | 상태 |
|---|---|
| 12 단위 | 11 끝 — kgy 4 · 6 · 10 · 11 · 14 · 15 · gabia 3 · 5 · 8 · 12 · 13.  남음 = `P1_c0_R_j0` (kgy · 시도 16 예정) |
| 원장 | **kgy** (`~/sdcp/ca1_ledger`) · gabia = `ca1_ledger.parked` · 넘김 ⑫ (11-26 09:03 KST) 끝 · 원장 끝 = `result 15 completed` |
| 시도 16 | 시작 블록 (부록 A) 을 1저자에게 줬다 · ⬜ 화면 (START_OK) 아직 못 봄 |
| 부록 팔 (gabia) | ② 압밀 끝 (07:48) · arm 1 P0 진행 (07:48 ~) → arm 1 P1 → [② 침대 점검 (부록 B) → 판독 → 1저자 `touch ~/sdcp/mid_bed2_ok`] → arm 2 P0 → arm 2 P1 · 감시 = 부록 C |
| 1저자 중간 열람 | 11-23 · 11-26 (판정 아님 · 값은 리포 · 쪽지 어디에도 없다) |
| 마감 | GPU 팔 12-05 24:00 KST = 주 판정 값 (감도는 그 뒤 · 1저자 11-19) |

## 2. 할 일 (위에서부터)

1. 시도 16 START_OK 확인 (1저자 화면) → 운영 기록 한 줄 (쪽지로).
2. 시도 16 끝 — 원장이 kgy 에 있으니 사슬이 스스로 결과 줄을 쓴다 (rc 0) · 확인 = 원장 끝 `result 16 completed`.
3. 부록 팔 — arm 1 P1 이 끝나 갈 때 ② 침대 점검 (부록 B · 읽기만) → 판독 (기대: SDCP 0 · SE 점 수 같음 · VGCF · PTFE ≈ DBE 의 −0.52 % [우리 산술] · 두께 · 기공률 = 기록) → 맞으면 1저자가 `touch ~/sdcp/mid_bed2_ok` → arm 2 칸이 이어진다.  안 맞으면 멈추고 1저자.
4. 12 단위가 다 끝나면 → 11-21 쪽지 §2 의 7 (합치기 · 112 h 규칙) → 8 (주 판정 · 다시 판정 · 값 열람 = 1저자) → 9 (감도 = 그 뒤 · 1저자).
5. 시간 — 12-05 전에 주 판정이 안 될 것 같으면 먼저 1저자에게.

## 3. 지킬 것

- 11-21 쪽지 §3 그대로 (σ 는 `verdict_results.json` 에만 · 화면 · 쪽지 · 커밋에 σ 금지 · 원본 손대지 않기 · 봉인 · 코드 핀 그대로 · push 금지 가지 · 현장 실행 = 1저자 · `--resume` 자격 · 주소 · 포트 · 계정 · 홈 경로 금지 · RJ 323957 재실행 없음 · 실행 우선).
- relay 스킬 §1 금지 다섯 — 서버에 직접 접속하지 않는다 (명령 블록만 만들고 1저자가 붙인다) · GitHub push 금지.
- 블록은 venv 를 스스로 켠다 (1저자 11-26 *"dem-venv 환경도 너가 만들고"*): `conda deactivate; source ~/dem-venv/bin/activate` + 버전 대조 (3.8.10 · 1.24.4 · 1.10.1) 를 블록 안에.
- 블록은 원본 파일로 만들고 `bash -n` 을 통과한 뒤 준다 — 화면에서 다시 베끼지 않는다 (`SELF-201`).
- 원장 넘김은 시작 기록이 원장에 남은 뒤에만 (11-24: 시작 기록 전에 넘기면 Exit 3).

## 4. 기록 · 넘기기

- 운영 기록 · 원장 · CLAUDE.md 는 고치지 않는다 — 쪽지 새 파일 `docs/collab/agy_to_claude/<UTC>_rint2-r-ops.md` 로 남기고 Claude 가 반입 때 옮긴다.
- 결과 = Claude 인계 ZIP (relay 스킬 §1).
- **교차검증 (1저자 11-26 *"각각 실무 끝나면 agy 교차검증받고 다시 받기"*)**: 한 마디 (시도 16 끝 · 부록 팔 끝 · 합치기 · 주 판정 · 코팅 메모) 가 끝나면 인계 ZIP 을 1저자에게 → 1저자가 Codex 반박 창에 숫자 교차검증 (relay 스킬 §5-4 · Rint = 원장 · 기록 대조만 · σ 는 보지 않는다) → 두 ZIP 을 함께 Claude 에 반입.

## 5. 코팅 과정 DEM — 가능성 메모 (agy 실무가 주인 · 서두르지 않음)

[믹서 · 코팅 활물질] · 1저자 11-26 *"코팅 관련해서는 지금 … 안티그래비티한테"* · *"믹서랑 함께 천천히"* · 개발 자료 · 결과 0 건 · 이 메모가 agy 실무의 첫 품질 확인을 겸한다.  (같은 내용 = B 가지 `docs/collab/claude_to_agy/20261126-0600_coating-dem-start.md` · push 뒤 보임)

```
[1저자 11-26] 할 일 = 코팅 과정 DEM (논문 밖 · 구현 시도) 의 가능성 메모. 문서만 쓴다 — 계산 · 서버 실행 없음.
- 근거: docs/collab/claude_to_codex/20261123-2330_mixer-q1-q4-direction.md 의 표 4 번 줄 · docs/reviews/mixer_direction_feedback_20261123.md (11-23 Q3) · CLAUDE.md 용훈 포메이션 Ⓒ 줄.
- 메모 = docs/reviews/coating_dem_feasibility_memo_<YYYYMMDD>.md — 넣을 것:
  1. 먼저 볼 장치 꼴 (메카노퓨전 · 텀블러 · 칼날 가운데 하나) 과 고른 이유
  2. 규모 어림 (입자 수 · Δt · 1 초를 계산하는 데 드는 시간 · 우리 기계 기준) — 산술은 [추정] 표지
  3. 충돌 → SE 파쇄 → 부착 → 소성 가운데 지금 우리 DEM (LIGGGHTS 덱) 으로 바로 되는 것 / 안 되는 것
  4. 피복률로 볼 지표 (게스트 피복률 · 충돌 에너지 분포 등)
  5. 첫 샌드박스 크기와 끝 기준
- 문헌 값 · 서지는 litdb 정본 카드 (claude/friendly-meitner-lldvar 가지의 litdb/papers/) 에서만 가져온다. 카드가 없으면 [미확인] 으로 두고 짓지 않는다.
- 끝나면 Claude 인계 ZIP (반입할 커밋의 패치 · stable patch-id · 바꾼 파일 사본 · sha256 목록 · 쪽지 docs/collab/agy_to_claude/<UTC>_coating-dem-memo.md) 을 만들어 1저자에게 준다.
```

## 부록 A · 시도 16 시작 블록 (kgy · 원장 끝 `result 15 completed` 일 때만 · 아니면 STOP)

```bash
cd ~/sdcp && umask 022 && (
L=~/sdcp/ca1_ledger; R=~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md; C=~/dem-ca1/scripts/rint_r_chain.py
lastx() { python3 -c 'import json,subprocess,sys; L=subprocess.run(["git","-C",sys.argv[1],"show","HEAD:rint_r_attempts.jsonl"],capture_output=True,text=True,check=True).stdout.splitlines(); x=json.loads(L[-1]); print(x.get("kind"), x.get("n"), x.get("status"))' "$L"; }
conda deactivate 2>/dev/null; source ~/dem-venv/bin/activate 2>/dev/null
python3 -c 'import sys,numpy,scipy; v=(sys.version.split()[0],numpy.__version__,scipy.__version__); print(*v); sys.exit(0 if v==("3.8.10","1.24.4","1.10.1") else 1)' || { echo "STOP: venv 아님 — 아무것도 안 함"; exit 1; }
test -d ca1_ledger && test ! -e ca1_ledger.parked || { echo "STOP: kgy 원장 자리가 예상 (원장 = kgy) 과 다름 — 아무것도 안 함"; exit 1; }
S=$(lastx); echo "원장 끝 = $S"; [ "$S" = "result 15 completed" ] || { echo "STOP: 원장 끝이 result 15 completed 아님 — 화면 그대로 보내 주세요"; exit 1; }
if pgrep -f 'rint_r_chain.py --stage' >/dev/null; then echo "STOP: kgy 에 R 사슬이 돈다 — 시작하지 않음"; exit 1; fi
OUT=$(python3 $C --stage ledger --ledger $L --add --ledger-target unit:P1_c0_R_j0 --machine kgy --plan ~/sdcp/ca1_plan.json --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --registration $R); echo "$OUT"
N=$(echo "$OUT" | sed -n 's/.*ATTEMPT_ADDED n=\([0-9]*\).*/\1/p'); [ -n "$N" ] || { echo "STOP: 번호 없음 (원장은 kgy 에 그대로)"; exit 1; }; echo "N=$N"
nohup python3 $C --stage predict --ladders ~/sdcp/ca1_ladder_P0/attempt_1 ~/sdcp/ca1_ladder_P1/attempt_2 --kit kit_DBE_sdcp1um_vgcf100 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --max-hours 168 --machine kgy --registration $R --ledger $L --attempt $N --unit P1_c0_R_j0 --cjunc-store ~/ca1_cjstore --out ~/sdcp/ca1_units > ~/sdcp/ca1_logs/unit_P1_c0_R_j0_a$N.log 2>&1 &
ok() { [ "$(lastx)" = "start $N None" ] && [ "$(ls ca1_units/attempt_$N/groups/ 2>/dev/null | grep -c 'launch.json$')" -ge 1 ]; }
for i in $(seq 1 60); do sleep 10; ok && break; done
ok && echo "START_OK $N (원장 = kgy · 마지막 단위 P1_c0_R_j0)" || { echo "확인 필요: 원장 끝 = $(lastx) · 로그 끝:"; tail -5 ~/sdcp/ca1_logs/unit_P1_c0_R_j0_a$N.log; }
)
```

시작 뒤 감시: `watch -n 30 bash ~/uwatch.sh P1_c0_R_j0 16`

## 부록 B · ② 침대 점검 블록 (gabia · 읽기만 · σ 칸 안 읽음 · 표지는 만들지 않음)

```bash
cd ~/sdcp && (
conda deactivate 2>/dev/null; source ~/dem-venv/bin/activate 2>/dev/null
python3 - <<'PY'
# 부록 팔 ② 새 침대 점검 (등록 §3 · 풀이 전 · 읽기만 · σ 칸은 읽지 않는다)
import glob, json, os
import numpy as np
H = os.path.expanduser('~/sdcp')
K1, K2 = 'kit_DBE_sdcp1um_vgcf100', 'kit_DBE_ptfe05_sdcp0_vgcf100'
REFNAME = 'run_VGCF3_PTFE0.5_SDCP0.5_20261023_213224_2924195'
bad = []
def runs(k):
    return sorted(d.rstrip('/') for d in glob.glob(os.path.join(H, k, 'run_*/')))
r1 = [r for r in runs(K1) if os.path.exists(os.path.join(r, 'mpm_done.marker'))]
print('K1 완료 런:', [os.path.basename(r) for r in r1])
ref = next((r for r in r1 if os.path.basename(r) == REFNAME), None)
if ref is None:
    print('STOP: 기준 DBE 런 없음 —', REFNAME); raise SystemExit(1)
lr = os.path.join(H, K2, 'latest_run')
new = os.path.realpath(lr) if os.path.islink(lr) else None
print('K2 run_* :', [os.path.basename(r) for r in runs(K2)], '· latest_run →', new and os.path.basename(new))
if not new or not os.path.isdir(new):
    print('STOP: K2 latest_run 없음'); raise SystemExit(1)
done = os.path.exists(os.path.join(new, 'mpm_done.marker'))
held = final = False; tail = []
lg = os.path.join(new, 'mpm_run.log')
if os.path.exists(lg):
    for ln in open(lg, encoding='utf-8', errors='replace'):
        held = held or ('✓ held at target' in ln)
        final = final or ln.startswith('FINAL')
        if ln.strip():
            tail = (tail + [ln.rstrip()[:110]])[-3:]
print(f'완료 마커 {done} · 판 고정 (✓ held at target) {held} · FINAL {final}')
print('로그 끝 세 줄:', ' ⏎ '.join(tail))
if not (done and held and final):
    bad.append('압밀 정상 종료 표지')
mo, mn = (json.load(open(os.path.join(r, 'mpm_metrics.json'))) for r in (ref, new))
for k in ('E_anchor', 'dt_effective', 'platen_mach_VcP', 'porosity_at_target_pct', 'porosity_settled_pct', 'thickness_um'):
    print(f'  {k:24s} DBE {mo.get(k)} · ② {mn.get(k)}')
if mn.get('porosity_at_target_pct') is None:
    bad.append('porosity_at_target_pct None')
for a in ('VGCF', 'PTFE', 'SDCP'):
    ao, an = ((m.get('additives') or {}).get(a) or {} for m in (mo, mn))
    print(f'  {a:5s} E_GPa {ao.get("E_GPa")} → {an.get("E_GPa")} · n_points {ao.get("n_points")} → {an.get("n_points")}')
co, cn = ({int(u): int(c) for u, c in zip(*np.unique(np.load(os.path.join(r, 'phase.npy')), return_counts=True))} for r in (ref, new))
print('  상별 점 수 DBE', co, '· 합', sum(co.values()))
print('  상별 점 수 ② ', cn, '· 합', sum(cn.values()))
for p in sorted(set(co) | set(cn)):
    o, n = co.get(p, 0), cn.get(p, 0)
    print(f'  상 {p}: {o} → {n} · 비 {(n / o if o else float("nan")):.5f}')
sd = (mn.get('additives') or {}).get('SDCP') or {}
if sd.get('n_points'):
    bad.append('SDCP 점 있음')
se_o, se_n = co.get(1), cn.get(1)
if se_o != se_n:
    bad.append(f'SE 점 수 다름 ({se_o} → {se_n})')
print('기대 (등록 §3): SDCP 0 · SE = DBE · VGCF · PTFE ≈ DBE 의 −0.52 % [우리 산술] · 두께 · 기공률 = 기록')
print('BED2_CHECK_FAIL: ' + ' · '.join(bad) if bad else 'BED2_PRINT_OK — 표지 파일은 아직 만들지 않음 (이 출력을 보내 주세요)')
PY
)
```

## 부록 C · 부록 팔 감시 (gabia · 읽기만)

```bash
cat > ~/mwatch.sh <<'EOF'
# 부록 팔 칸 보기 (σ 없음 · 읽기만)
echo "$(hostname)  부록 팔: arm 1 P0 → arm 1 P1 → [② 침대 점검] → arm 2 P0 → arm 2 P1"
tail -3 ~/sdcp/ca1_logs/mid_cells.log
for d in ~/sdcp/mid_units/arm*_P*; do
  [ -d "$d" ] || continue
  st=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("status"))' "$d/middle_arm_manifest.json" 2>/dev/null)
  echo "$(basename "$d")  status=${st:-?}  groups launch=$(ls "$d/groups" 2>/dev/null | grep -c 'launch.json$') end=$(ls "$d/groups" 2>/dev/null | grep -c 'end.json$')"
done
echo "멈춤 파일 $(test -e ~/sdcp/mid_STOP && echo 있음 || echo 없음) · ② 침대 표지 $(test -e ~/sdcp/mid_bed2_ok && echo 있음 || echo 없음)"
echo "gpu=$(nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader 2>/dev/null)"
EOF
watch -n 30 bash ~/mwatch.sh
```
