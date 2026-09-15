#!/usr/bin/env python3
"""S3 런 — ψ 배치 두 팔을 돌려 채널별 상대차와 등록된 판정을 낸다 (`L2-01`).

정본 계약 = `docs/area_contract_20260913.md` §A(정의역) · §B(ρ 판정) · §C(변경 범위) · §D(코호트).

★★ **왜 이 파일이 있나 — `R4-10` 이 남긴 구멍.**
  `seal_s3_prerun.py` 는 **봉인 발행**을 막는다.  그런데 *"봉인을 요구하는 러너가 없어서
  그 도구는 발행만 막고 S3 **시작**은 못 막는다"* 가 그 항목의 결론이었다.  즉 마감 규칙
  전체가 **산문**이었다 (규율 ④ — 밖으로 강제되지 않으면 새어나간다).
  ⇒ 이 러너는 **봉인 파일 없이는 아무것도 하지 않는다**.  그것이 존재 이유다.

거부 규약 (전부 rc=2, 아무것도 안 쓴다):
  · `--seal` 이 없다 / 파일이 없다 / JSON 이 아니다 / 필수 키가 없다
  · 봉인 시각이 허용 창 **밖**이다 (있어서는 안 되는 봉인은 런을 허가하지 못한다)
  · 봉인이 적은 `rho_rule` 이 이 판정기의 규칙과 다르다
  · 어느 채널이든 `B_ch` 가 0개다 (baseline 이 없다)
  · **ρ 증서가 없다/깨졌다/봉인된 `B_ch` 를 안 덮는다** (`AREA5-04`)
  · `--limit` 를 `--diagnostic` 없이 줬다, 또는 음수다 (`AREA5-02`)

rc=3 (판정을 발행하지 않는다 — 결과를 쓰지 않는다):
  · `ERROR` 가 있다 · baseline 재현 실패 · 계약/범위 위반
    (`BASELINE_REPRODUCTION_FAILED` · `BASELINE_STATE_CHANGED` · `SOLVER_ERROR` ·
     `ACTIVE_SET_CHANGED` · `NEW_NEGATIVE`)
  · 활성 간선이 0인데 **유효 관측도 아니다**
    ⚠ 활성 0 이어도 두 팔이 같은 유효 σ 를 냈으면 그것은 **정상 무변화**다 (`AREA5-08`) —
      no-op 배선 오류와 섞지 않는다.

★★ **미정값은 지우지 않는다** (`AREA5-01` · 계약 `A-4`).  `old` 는 유효한데 `new` 만 미정인
  행은 **하한 0 · 상한 +∞** 로 두고 중앙값의 두 경계를 내며, 두 라벨이 다르면
  `UNDETERMINED_COHORT` 다.  분모는 **봉인된 `B_ch` 크기**이지 처리한 수가 아니다.

사용 (공식):
  python3 scripts/run_s3_psi.py --seal docs/data/s3_seal.json \\
      --rho-certificate docs/data/s3_rho_cert.json \\
      --cases-root /home/yonghoon71/lhs_local --deck-dir /home/yonghoon71/lhs_local \\
      --out docs/data/s3_run.json
사용 (진단 — 공식 h0/h1 을 내지 않는다):
  python3 scripts/run_s3_psi.py --seal … --rho 1.17 --diagnostic --limit 3
  python3 scripts/run_s3_psi.py --selftest
"""
from __future__ import annotations
import argparse
import datetime as _dt
import json
import math
import pathlib
import statistics
import sys

SCRIPTS = pathlib.Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

#: 허용 창·마감·판정 규칙 — 봉인 도구가 **정본**이고 여기서는 import 만 한다.
#: ⛔ **사본을 만들지 않는다.**  import 가
#:   실패하면 조용한 기본값으로 돌지 말고 **죽는다**: 규칙이 갈리면 봉인과 다른 판정이 나오고
#:   그것이 사전등록을 무의미하게 만든다 (실제로 두 사본이 이미 갈라져 있었다).
from seal_s3_prerun import KST, RHO_RULE, SEAL_DEADLINE, SEAL_NOT_BEFORE

IN_DOMAIN = 'B_ch'
REQUIRED_SEAL_KEYS = ('sealed_at_kst', 'seal_deadline', 'generation_git_sha', 'channels')

#: 등록된 판정표 (계약 §B).  ⛔ 문턱 3 %/10 % 고정 — ρ 는 문턱을 못 움직이고 **상태만** 바꾼다.
VERDICT_RULE = RHO_RULE


def verdict(d: float, rho: float) -> str:
    """계약 §B 의 표를 **그 순서 그대로**.  순서를 바꾸면 라벨이 바뀐다."""
    if not (math.isfinite(d) and math.isfinite(rho)) or d < 0 or rho < 0:
        return 'NONFINITE'
    if d >= 10.0 and d >= 2.0 * rho:
        return 'h1'
    if rho > 3.0:
        return 'UNRESOLVED_NUMERIC'
    if d < 3.0:
        return 'h0'
    return 'BOTH_REJECTED'


def seal_window_ok(sealed_at_kst: str) -> tuple[bool, str]:
    """봉인 시각이 **양쪽으로 닫힌 창** 안인가 (`R4-07` 저자 결정 = 09-17 23:59 KST 고정)."""
    try:
        ts = _dt.datetime.fromisoformat(sealed_at_kst)
    except (TypeError, ValueError):
        return False, f'sealed_at_kst 를 시각으로 읽을 수 없다: {sealed_at_kst!r}'
    if ts.tzinfo is None:
        return False, 'sealed_at_kst 에 시간대가 없다 — KST 로 가정하지 않는다'
    if ts.astimezone(KST).date() < SEAL_NOT_BEFORE:
        return False, f'봉인이 허용 시작({SEAL_NOT_BEFORE}) 전이다: {ts.isoformat()}'
    if ts > SEAL_DEADLINE:
        return False, f'봉인이 마감({SEAL_DEADLINE.isoformat()}) 뒤다: {ts.isoformat()}'
    return True, ''


def load_seal(path: pathlib.Path) -> tuple[dict | None, str]:
    """봉인을 읽고 **런을 허가할 수 있는지**까지 본다.  허가 못 하면 `(None, 이유)`."""
    if not path.is_file():
        return None, f'봉인 파일이 없다: {path}'
    try:
        seal = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as e:
        return None, f'봉인을 JSON 으로 읽을 수 없다: {e}'
    if not isinstance(seal, dict):
        return None, '봉인이 객체가 아니다'
    miss = [k for k in REQUIRED_SEAL_KEYS if not seal.get(k)]
    if miss:
        return None, f'봉인에 없는 키 {miss} — 무엇을 baseline 으로 삼는지 복원할 수 없다'
    ok, why = seal_window_ok(seal['sealed_at_kst'])
    if not ok:
        return None, f'있어서는 안 되는 봉인은 런을 허가하지 못한다 — {why}'
    chans = seal['channels']
    if not isinstance(chans, dict) or not chans:
        return None, '봉인에 채널이 없다'
    empty = [ch for ch, d in chans.items()
             if not (d.get('ids') or {}).get(IN_DOMAIN)]
    if empty:
        return None, f'`B_ch` 가 0개인 채널 {sorted(empty)} — baseline 이 없다 (빈 봉인)'
    #  ★★ 봉인이 **어떤 규칙으로** 만들어졌는지 확인한다.  봉인이 적은 규칙과 이 판정기가
    #     구현한 규칙이 다르면 사전등록이 무의미하다 — 문구가 곧 문턱이기 때문이다.
    #     ⚠ 이것은 가상의 위험이 아니다: 러너 초판이 규칙을 **따로 적었고** 꼬리가 갈라져
    #       있었다 (2026-09-15 에 발견해 `RHO_RULE` 하나로 묶었다).
    if seal.get('rho_rule') and seal['rho_rule'] != RHO_RULE:
        return None, ('봉인이 적은 판정 규칙이 이 판정기의 규칙과 다르다 — 다른 규칙으로 만들어진 '
                      f'봉인은 이 판정기가 쓸 수 없다.\n      봉인: {seal["rho_rule"]!r}'
                      f'\n      판정기: {RHO_RULE!r}')
    return seal, ''


def load_rho_certificate(path, seal, channels_hint=None):
    """ρ **수치-QC 증서** — 공식 판정의 유일한 ρ 입력 (`AREA5-04`).

    증서는 그 ρ 가 **무엇에서 나왔는지**를 들고 있어야 한다: 대상 코호트·채널·비교 세대·
    실제 정지 기준·집계식·산출값.  그리고 **이 봉인과 같은 코호트**여야 한다 —
    ⛔ 계약이 *"기존 mono 30 의 ρ 를 새 130 이나 S3 망의 보편 상한으로 대입하지 않는다"* 고
    금지했고, 2026-09-15 현재 리포의 사다리 셋이 정확히 그 mono 30 이다.
    ⚠ 현행 봉인기는 ρ 수치 필드를 **내지 않는다** — 증서는 아직 만들어야 하는 산출물이다.
    """
    need = ('cohort_ids', 'channels', 'generation', 'stop_criterion', 'aggregation', 'rho')
    if not path.is_file():
        return None, f'증서 파일이 없다: {path}'
    try:
        c = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as e:
        return None, f'증서를 JSON 으로 읽을 수 없다: {e}'
    if not isinstance(c, dict):
        return None, '증서가 객체가 아니다'
    #  ⚠ **존재**와 **참값**을 가른다 — `not c.get(k)` 로 보면 정당한 `rho: 0.0` 이
    #    "키 없음" 으로 읽힌다 (실제로 그렇게 짰다가 잡았다).  0 은 결측이 아니다.
    miss = [k for k in need if k not in c]
    empty = [k for k in need if k in c and k != 'rho' and not c[k]]
    if miss or empty:
        return None, (f'증서에 없는 키 {miss} · 빈 키 {empty} — '
                      'ρ 가 무엇에서 나왔는지 복원할 수 없다')
    try:
        rho = float(c['rho'])
    except (TypeError, ValueError):
        return None, f"증서의 ρ 를 수로 읽을 수 없다: {c['rho']!r}"
    if not (math.isfinite(rho) and rho >= 0):
        return None, f'증서의 ρ 가 유한 비음수가 아니다: {rho!r}'
    #  ★ 코호트가 봉인과 같아야 한다 — 다른 코호트의 ρ 는 이 판정의 입력이 아니다.
    sealed = {i for ch in seal['channels'].values()
              for i in (ch.get('ids') or {}).get(IN_DOMAIN, [])}
    cert_ids = set(c['cohort_ids'])
    if not sealed:
        return None, '봉인에서 B_ch 를 못 읽었다'
    if not sealed <= cert_ids:
        missing = sorted(sealed - cert_ids)[:5]
        return None, (f'증서가 봉인된 B_ch 를 다 덮지 않는다 — 빠진 ID {len(sealed - cert_ids)}건 '
                      f'(예: {missing}).  ⛔ 다른 코호트의 ρ 를 대입하지 않는다.')
    if channels_hint and not set(channels_hint) <= set(c['channels']):
        return None, f"증서가 채널 {sorted(set(channels_hint) - set(c['channels']))} 를 안 덮는다"
    return rho, ''


def sigma_of(net, solve) -> tuple[float | None, int, str]:
    """한 망 → `(σ_eff/σ_bulk, 활성 간선 수, 실패 사유)`.

    활성 간선 = `R_constriction > 0` 인 간선 = **ψ > 1e-4 인 간선**.  두 팔이 다를 수 있는
    자리는 정확히 여기뿐이다 (계약 §C: floor 아래·clamp 경계는 0 → 0).

    ⛔⛔ **예외를 `None` 으로 삼키지 않는다** (`AREA5-01`).  옛 판은
    `except Exception: return None` 이라 솔버 내부 예외가 **수치 미정과 구별되지 않았고**,
    그래서 바깥 `errors` 게이트에 **도달하지 않았다** — 내가 커밋 메시지에 적은
    *"ERROR 가 있으면 판정을 발행하지 않는다"* 가 거짓이 된 자리다.
    ⇒ 세 번째 값으로 사유를 돌려준다: `''`(정상) · `NUMERIC`(비유한/None = 등록된 수치 미정)
      · `EXC:<타입>`(계약/프로그래밍 오류 — 판정을 발행하지 않는다).
    """
    n_active = sum(1 for e in net['edges'] if (e.get('R_constriction') or 0) > 0)
    try:
        _g, ratio = solve(net, mode='full')
    except Exception as e:                                     # noqa: BLE001
        return None, n_active, f'EXC:{type(e).__name__}: {e}'
    if ratio is None or not math.isfinite(float(ratio)):
        return None, n_active, 'NUMERIC'
    return float(ratio), n_active, ''


def bound_medians(values, n_domain, rho):
    """계약 `A-4` — 미정값을 **하한 0 · 상한 +∞** 로 두고 중앙값의 두 경계를 낸다.

    `values` = 확정된 `|Δ|` 들.  `n_domain` = **봉인된** `B_ch` 크기 (처리한 수가 아니다).
    ⛔ 실패를 지워 분모를 바꾸지 않는다 — 그것이 complete-case 편향이고 `AREA5-01` 이다.
    ⚠ `+∞` 는 **경계 계산용**이지 관측값이 아니다 — scalar 판정기에 넣지 않는다.
    """
    k = n_domain - len(values)
    if k < 0:
        return None, None, 'DOMAIN_SHRANK'
    lo = statistics.median(sorted(values) + [0.0] * k) if n_domain else None
    hi_sorted = sorted(values)
    #  상한: 미정을 +∞ 로 두면 정렬의 **오른쪽 끝**에 붙는다.  중앙값 자리가 확정값 안에
    #  들어오면 유한, 넘어가면 +∞ 다 (관측값을 만들지 않고 자리만 센다).
    mid = (n_domain - 1) // 2
    if n_domain % 2:
        hi = hi_sorted[mid] if mid < len(hi_sorted) else float('inf')
    else:
        a = hi_sorted[mid] if mid < len(hi_sorted) else float('inf')
        b = hi_sorted[mid + 1] if mid + 1 < len(hi_sorted) else float('inf')
        hi = float('inf') if math.isinf(a) or math.isinf(b) else (a + b) / 2.0
    v_lo = verdict(lo, rho) if lo is not None else 'NO_DATA'
    #  상한이 +∞ 면 고정 ρ 에서 `d → ∞` 의 극한이므로 h1 이다 (계약 A-4).
    v_hi = 'h1' if (hi is not None and math.isinf(hi)) else (
        verdict(hi, rho) if hi is not None else 'NO_DATA')
    return (lo, hi), (v_lo, v_hi), ('' if v_lo == v_hi else 'UNDETERMINED_COHORT')


def run_case(case_dir, deck_dir, channels, case_networks, solve):
    """한 케이스 두 팔 → 채널별 기록.

    ★ 두 팔은 **같은 원자료**에서 나와야 한다 (`AREA5-03`) — 옛 판은 raw 를 각각 재발견하고
      두 번째 `prov` 를 **버렸다**.  이제 두 provenance 를 대조하고 다르면 올린다.
    """
    import network_conductivity as nc
    out = {}
    nets_old, prov = case_networks(case_dir, contact_mode='physics', channels=channels,
                                   deck_dir=deck_dir, psi_placement=nc.PSI_DIVIDE)
    nets_new, prov2 = case_networks(case_dir, contact_mode='physics', channels=channels,
                                    deck_dir=deck_dir, psi_placement=nc.PSI_MULTIPLY)
    _keys = ('atom_file', 'contact_file', 'atom_step', 'contact_step', 'n_contact_rows',
             'plate_z', 'scale', 'deck')
    _drift = {k: (prov.get(k), prov2.get(k)) for k in _keys if prov.get(k) != prov2.get(k)}
    if _drift:
        raise ValueError(f'{case_dir.name}: 두 팔이 다른 원자료를 읽었다 (실행 중 파일이 바뀌었다) — '
                         f'{_drift}')
    for ch in channels:
        s_old, n_act, why_o = sigma_of(nets_old[ch], solve)
        s_new, n_act2, why_n = sigma_of(nets_new[ch], solve)
        #  ⚠ 활성 간선 수는 **팔에 무관**해야 한다 — 곱셈이 양수를 0 으로 만들지 않기 때문이다.
        #    ⛔ 갈리면 §C 의 ψ-only 전환 범위 위반이므로 **거부**한다 (`AREA5-08`).
        #      옛 판은 `status=ok` 로 발행했다 — "기록했다" 가 검증을 대신하지 못한다.
        rec = {'sigma_old': s_old, 'sigma_new': s_new,
               'n_active_old': n_act, 'n_active_new': n_act2,
               'n_edges': len(nets_old[ch]['edges']),
               'why_old': why_o, 'why_new': why_n}
        if n_act != n_act2:
            rec['status'], rec['delta_pct'] = 'ACTIVE_SET_CHANGED', None
        elif why_o.startswith('EXC:') or why_n.startswith('EXC:'):
            #  계약/프로그래밍 오류는 **수치 미정이 아니다** — A-4 로 세탁하지 않는다.
            rec['status'], rec['delta_pct'] = 'SOLVER_ERROR', None
        elif s_old is None or s_old <= 0.0:
            #  봉인은 이 ID 를 `B_ch`(σ_old > 0) 로 분류했는데 재계산이 다르다.
            #  ⚠ `None` 은 원자료 변경의 증명이 아니다 (재계산 수치 실패일 수도 있다) —
            #    그래서 사유를 갈라 적는다 (`AREA5-08` 처방).
            rec['status'] = ('BASELINE_REPRODUCTION_FAILED' if why_o == 'NUMERIC'
                             else 'BASELINE_STATE_CHANGED')
            rec['delta_pct'] = None
        elif s_new is None:
            #  old 는 살아 있고 new 만 미정 ⇒ **등록된 수치 미정** = A-4 경계 대상이다.
            rec['status'], rec['delta_pct'] = 'NEW_UNDETERMINED', None
        elif s_new < 0.0:
            rec['status'], rec['delta_pct'] = 'NEW_NEGATIVE', None
        else:
            rec['status'] = 'ok'
            rec['delta_pct'] = (s_new - s_old) / s_old * 100.0
        out[ch] = rec
    return out, prov


def main() -> int:
    ap = argparse.ArgumentParser(description='S3 런 — ψ 배치 두 팔 (봉인 필수)')
    ap.add_argument('--seal', default='', help='`seal_s3_prerun.py` 가 낸 봉인 JSON (필수)')
    ap.add_argument('--rho', default=None,
                    help='ρ 집계값.  ⛔ 기본값 없음.  ★ 공식 판정에는 --rho-certificate 가 '
                         '필요하고, 맨 --rho 는 --diagnostic 에서만 쓴다 (AREA5-04)')
    ap.add_argument('--rho-certificate', default='',
                    help='ρ 수치-QC 증서 JSON — 채널별 ρ 와 그 출처(코호트·세대·정지기준·'
                         '집계식)를 묶은 것.  공식 판정의 유일한 ρ 입력이다')
    ap.add_argument('--diagnostic', action='store_true',
                    help='진단 모드.  --limit 와 맨 --rho 를 허용하되 **공식 h0/h1 을 발행하지 '
                         '않는다** (AREA5-02)')
    ap.add_argument('--cases-root', default='')
    ap.add_argument('--deck-dir', default='')
    ap.add_argument('--out', default='')
    ap.add_argument('--limit', type=int, default=0,
                    help='⛔ 진단 전용 — 정의역을 자르므로 --diagnostic 없이는 거부한다')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()

    if not a.seal:
        print('⛔ `--seal` 이 필요하다 — 봉인 없이 S3 를 돌리지 않는다 (계약 §D-3 · R4-10).')
        return 2
    seal, why = load_seal(pathlib.Path(a.seal))
    if seal is None:
        print(f'⛔ 봉인이 런을 허가하지 않는다 — {why}')
        return 2
    #  ── ρ (`AREA5-04`) ──  공식 판정의 ρ 는 **증서**에서만 온다.
    #    ⚠ 옛 판은 아무 CLI 수치나 받아 `--rho 7 → UNRESOLVED_NUMERIC` / `--rho 0 → h1` 로
    #      같은 데이터의 라벨이 뒤집혔다.  "필수" 는 "봉인됨" 이 아니다.
    rho_src = ''
    if a.rho_certificate:
        rho, why = load_rho_certificate(pathlib.Path(a.rho_certificate), seal, channels_hint=None)
        if rho is None:
            print(f'⛔ ρ 증서가 판정에 쓸 수 없다 — {why}')
            return 2
        rho_src = f'certificate:{a.rho_certificate}'
    elif a.rho is not None:
        if not a.diagnostic:
            print('⛔ 맨 `--rho` 는 **진단 전용**이다 (AREA5-04) — 공식 판정에는 '
                  '`--rho-certificate` 를 쓴다.  진단이면 `--diagnostic` 을 붙일 것.')
            return 2
        try:
            rho = float(a.rho)
        except ValueError:
            print(f'⛔ ρ 를 수로 읽을 수 없다: {a.rho!r}')
            return 2
        rho_src = 'cli(diagnostic)'
    else:
        print('⛔ ρ 가 필요하다 — 기본값 0 을 쓰면 `d ≥ 10` 이 전부 h1 이 된다.')
        return 2
    if not (math.isfinite(rho) and rho >= 0):
        print(f'⛔ ρ 가 유한 비음수가 아니다: {rho!r}')
        return 2
    #  ── limit (`AREA5-02`) ──  정의역을 자르는 것은 판정 집합을 고르는 것이다.
    if a.limit and not a.diagnostic:
        print('⛔ `--limit` 는 정의역을 자른다 — 진단 전용이다 (AREA5-02).  '
              '`--diagnostic` 없이는 거부한다.')
        return 2
    if a.limit < 0:
        print(f'⛔ 음수 limit 는 거부한다: {a.limit}')
        return 2

    import network_conductivity as nc
    from audit_constriction_deleted import case_networks

    channels = sorted(seal['channels'])
    root = pathlib.Path(a.cases_root) if a.cases_root else None
    if root is None or not root.is_dir():
        print(f'⛔ `--cases-root` 가 디렉터리가 아니다: {a.cases_root!r}')
        return 2

    per_channel: dict[str, list] = {ch: [] for ch in channels}
    rows, errors = [], []
    ids = sorted({i for ch in channels for i in seal['channels'][ch]['ids'][IN_DOMAIN]})
    if a.limit:
        ids = ids[:a.limit]
    print(f'봉인 {a.seal} · 채널 {channels} · B_ch 합집합 {len(ids)} 케이스 · ρ = {rho}')
    for cid in ids:
        cdir = root / cid
        try:
            res, prov = run_case(cdir, a.deck_dir or None, channels, case_networks,
                                 nc.solve_network)
        except Exception as e:                                 # noqa: BLE001
            errors.append({'case': cid, 'error': f'{type(e).__name__}: {e}'})
            print(f'  {cid}: ERROR {type(e).__name__}: {e}')
            continue
        rows.append({'case': cid, 'prov': prov, 'channels': res})
        for ch in channels:
            if cid in seal['channels'][ch]['ids'][IN_DOMAIN]:
                per_channel[ch].append((cid, res[ch]))
        print('  ' + cid + ' ' + ' · '.join(
            f"{ch}: Δ{('%+.3f%%' % res[ch]['delta_pct']) if res[ch]['delta_pct'] is not None else res[ch]['status']}"
            f" (활성 {res[ch]['n_active_old']}/{res[ch]['n_edges']})" for ch in channels))

    summary = {}
    n_contradicted = n_active_total = n_blocking = 0
    #  ⛔ **봉인이 정한 N 을 쓴다** — 처리한 수가 아니다 (`AREA5-02`).  실패를 지워 분모를
    #    바꾸는 것이 complete-case 편향이고, 그것이 `AREA5-01` 의 본체다.
    for ch in channels:
        n_domain = len(seal['channels'][ch]['ids'][IN_DOMAIN])
        deltas = [abs(r['delta_pct']) for _c, r in per_channel[ch] if r['delta_pct'] is not None]
        #  baseline 이 재현 안 된 것과 **계약/범위 위반**은 판정을 멈춘다 (A-4 대상 아님).
        blocking = sorted(c for c, r in per_channel[ch] if r['status'] in (
            'BASELINE_REPRODUCTION_FAILED', 'BASELINE_STATE_CHANGED',
            'SOLVER_ERROR', 'ACTIVE_SET_CHANGED', 'NEW_NEGATIVE'))
        #  old 는 살아 있고 new 만 미정 ⇒ A-4 의 0/+∞ 경계로 센다.
        undet = sorted(c for c, r in per_channel[ch] if r['status'] == 'NEW_UNDETERMINED')
        n_contradicted += len(blocking)
        n_blocking += len(blocking)
        n_active_total += sum(r['n_active_old'] for _c, r in per_channel[ch])
        bounds, verds, undet_label = bound_medians(deltas, n_domain, rho)
        if a.diagnostic:
            v = 'DIAGNOSTIC_PARTIAL'
        elif blocking:
            v = 'BLOCKED'
        elif undet_label:
            v = undet_label
        elif verds:
            v = verds[0]
        else:
            v = 'NO_DATA'
        summary[ch] = {
            'n_in_domain_sealed': n_domain,
            'n_processed': len(per_channel[ch]),
            'n_used': len(deltas),
            'undetermined_new': undet,
            'blocking': blocking,
            'median_abs_delta_pct_lower': None if bounds is None else bounds[0],
            'median_abs_delta_pct_upper': (None if bounds is None else
                                           (None if math.isinf(bounds[1]) else bounds[1])),
            'upper_is_infinite': bool(bounds and math.isinf(bounds[1])),
            'verdict_lower': None if verds is None else verds[0],
            'verdict_upper': None if verds is None else verds[1],
            'verdict': v,
        }

    out = {'contract': 'docs/area_contract_20260913.md §A·§B·§C·§D',
           'seal_path': str(a.seal), 'seal_sealed_at_kst': seal['sealed_at_kst'],
           'seal_generation_git_sha': seal['generation_git_sha'],
           'rho': rho, 'rho_source': rho_src, 'diagnostic': bool(a.diagnostic),
           'limit': a.limit, 'verdict_rule': VERDICT_RULE,
           'psi_arms': [nc.PSI_DIVIDE, nc.PSI_MULTIPLY],
           'channels': summary, 'cases': rows, 'errors': errors}

    #  ── ⛔ **무결성 게이트를 판정 인쇄보다 앞에 둔다** (`AREA5-08` 처방).
    #     옛 판은 거부하기 전에 요약에 `h1` 을 인쇄해, 종료코드를 무시한 로그 소비자가
    #     오인할 수 있었다.  실패면 실패 증거만 남긴다.
    _stop = ''
    if errors:
        _stop = f'ERROR {len(errors)}건 — 기술 실패를 물리 상태로 두지 않는다'
    elif n_blocking:
        _stop = (f'baseline 재현 실패·계약 위반 {n_blocking}건 — 조용히 재분류하지 않는다 '
                 '(BASELINE_REPRODUCTION_FAILED / BASELINE_STATE_CHANGED / SOLVER_ERROR / '
                 'ACTIVE_SET_CHANGED / NEW_NEGATIVE)')
    if _stop:
        print(f'\n⛔ 판정을 발행하지 않는다 — {_stop}')
        for ch in channels:
            s = summary[ch]
            if s['blocking']:
                print(f"    {ch}: {s['blocking'][:8]}")
        for e in errors[:8]:
            print(f"    ERROR {e['case']}: {e['error']}")
        return 3

    print('\n── 요약 ──')
    for ch in channels:
        s = summary[ch]
        _hi = '+∞' if s['upper_is_infinite'] else s['median_abs_delta_pct_upper']
        print(f"  {ch}: 봉인 정의역 {s['n_in_domain_sealed']} · 확정 {s['n_used']} · "
              f"new 미정 {len(s['undetermined_new'])} · "
              f"median|Δ| [{s['median_abs_delta_pct_lower']}, {_hi}] % · "
              f"판정 {s['verdict']} ({s['verdict_lower']}/{s['verdict_upper']})")
    if a.diagnostic:
        print('  ⚠ 진단 모드 — **공식 h0/h1 이 아니다** (DIAGNOSTIC_PARTIAL)')

    #  ── 공허한 측정을 성공으로 내지 않는다 (R4-01 과 같은 부류) ──
    #     ⚠ 그러나 **정상 전체 무변화**(d=0)와 no-op 배선 오류를 섞지 않는다 (`AREA5-08`).
    #       활성 간선이 0인데 두 팔이 같은 유효 σ 를 냈다면 그것은 **유효 관측**이다.
    if n_active_total == 0:
        _all_ok = all(r['status'] == 'ok' for ch in channels for _c, r in per_channel[ch])
        if not _all_ok:
            print('\n⛔ 활성 간선(ψ > 1e-4)이 **한 건도 없고** 유효 관측도 아니다 — 아무것도 안 쟀다.')
            return 3
        print('\n⚠ 활성 간선이 0이지만 두 팔이 같은 **유효 σ** 를 냈다 — 정해진 개입이 이 고정 망을 '
              '바꾸지 않았다는 관측이다 (NO_ACTIVE_EDGES).  등록된 일반 효과는 식별하지 못한다.')
        for ch in channels:
            summary[ch]['no_active_edges'] = True
    if a.out:
        pathlib.Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                       encoding='utf-8')
        print(f'\n→ {a.out}')
    return 0


# ══════════════════════════════════════════════════════════════════════════════
def _selftest() -> int:
    fail = []

    def chk(name, ok, detail=''):
        print(f'  {"✓" if ok else "✗"} {name}' + (f'   {detail}' if detail else ''))
        if not ok:
            fail.append(name)

    import tempfile
    import network_conductivity as nc

    # ① 판정표 — 계약 §B 의 **순서**를 고정한다.
    chk('① d=12 · ρ=1 → h1', verdict(12.0, 1.0) == 'h1')
    chk('①b d=12 · ρ=7 → UNRESOLVED_NUMERIC (h1 의 2ρ 조건을 못 넘고 ρ>3)',
        verdict(12.0, 7.0) == 'UNRESOLVED_NUMERIC', verdict(12.0, 7.0))
    chk('①c d=1 · ρ=1 → h0', verdict(1.0, 1.0) == 'h0')
    chk('①d d=5 · ρ=1 → BOTH_REJECTED (3 ≤ d < 10)', verdict(5.0, 1.0) == 'BOTH_REJECTED')
    chk('①e d=20 · ρ=11 → UNRESOLVED_NUMERIC — ρ 가 문턱을 낮추지 못한다',
        verdict(20.0, 11.0) == 'UNRESOLVED_NUMERIC', verdict(20.0, 11.0))
    chk('①f 비유한은 표에 안 들어온다', verdict(float('nan'), 1.0) == 'NONFINITE')
    #   ★ 판별력: ρ 를 0 으로 **기본값 처리하면** ①b 가 h1 로 뒤집힌다 = 거부해야 하는 이유.
    chk('①g ★ ρ=0 이면 ①b 가 h1 로 뒤집힌다 (그래서 ρ 기본값을 금지한다)',
        verdict(12.0, 0.0) == 'h1' and verdict(12.0, 7.0) != 'h1')

    # ② 창 — 양쪽으로 닫혀 있다 (R4-07).
    chk('② 09-16 봉인은 이르다', not seal_window_ok('2026-09-16T10:00:00+09:00')[0])
    chk('②b 09-17 12:00 KST 는 창 안', seal_window_ok('2026-09-17T12:00:00+09:00')[0])
    chk('②c 09-17 23:59:01 KST 는 마감 뒤', not seal_window_ok('2026-09-17T23:59:01+09:00')[0])
    chk('②d 09-18 은 마감 뒤', not seal_window_ok('2026-09-18T00:00:00+09:00')[0])
    chk('②e 시간대 없는 시각은 KST 로 가정하지 않고 거부',
        not seal_window_ok('2026-09-17T12:00:00')[0])

    # ③ 봉인 게이트 — **없거나 비었거나 창 밖이면 허가하지 않는다**.
    with tempfile.TemporaryDirectory() as td:
        tdp = pathlib.Path(td)
        good = {'sealed_at_kst': '2026-09-17T12:00:00+09:00',
                'seal_deadline': SEAL_DEADLINE.isoformat(),
                'generation_git_sha': 'deadbeef',
                'channels': {'ionic': {'ids': {IN_DOMAIN: ['lhs00_001']}}}}
        p_good = tdp / 'good.json'
        p_good.write_text(json.dumps(good), encoding='utf-8')
        chk('③ 정상 봉인은 허가', load_seal(p_good)[0] is not None, load_seal(p_good)[1])
        chk('③b 없는 파일은 거부', load_seal(tdp / 'nope.json')[0] is None)
        p_bad = tdp / 'bad.json'
        p_bad.write_text('{ not json', encoding='utf-8')
        chk('③c JSON 이 아니면 거부', load_seal(p_bad)[0] is None)
        for miss in REQUIRED_SEAL_KEYS:
            d = dict(good)
            d.pop(miss)
            p = tdp / f'miss_{miss}.json'
            p.write_text(json.dumps(d), encoding='utf-8')
            chk(f'③d 키 {miss} 가 없으면 거부', load_seal(p)[0] is None)
        d = json.loads(json.dumps(good))
        d['sealed_at_kst'] = '2026-09-16T12:00:00+09:00'
        p = tdp / 'early.json'
        p.write_text(json.dumps(d), encoding='utf-8')
        chk('③e ★ 창 **밖에서 만들어진** 봉인은 런을 허가하지 못한다',
            load_seal(p)[0] is None, load_seal(p)[1])
        d = json.loads(json.dumps(good))
        d['channels']['ionic']['ids'][IN_DOMAIN] = []
        p = tdp / 'empty.json'
        p.write_text(json.dumps(d), encoding='utf-8')
        chk('③f ★ `B_ch` 가 빈 봉인은 거부 (baseline 이 없다)', load_seal(p)[0] is None)
        #  ★★ 봉인이 **다른 규칙**으로 만들어졌으면 거부 (사본이 실제로 갈라져 있었다).
        d = json.loads(json.dumps(good))
        d['rho_rule'] = RHO_RULE
        p = tdp / 'rule_ok.json'
        p.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
        chk('③g 같은 규칙이 적힌 봉인은 허가', load_seal(p)[0] is not None, load_seal(p)[1])
        d['rho_rule'] = RHO_RULE.replace('d < 3', 'd < 5')      # 문턱 한 글자
        p = tdp / 'rule_bad.json'
        p.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
        chk('③h ★★ 문턱 한 글자가 다른 규칙으로 만들어진 봉인은 **거부**한다',
            load_seal(p)[0] is None)
        #  ⚠ 꼬리 한 구절 차이도 잡는다 — 실제로 갈라졌던 자리가 정확히 그 꼬리였다.
        d['rho_rule'] = RHO_RULE.replace('  (d = median(|Δ|) %, 둘 다 유한 비음수)',
                                         '  (d = median(|Δ|) %)')
        p = tdp / 'rule_tail.json'
        p.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
        chk('③i ★ 갈라졌던 그 꼬리 차이도 거부한다 (2026-09-15 실제 사례)',
            load_seal(p)[0] is None)

    # ④ ★★ 양성 대조 — 합성 케이스 두 팔이 **실제로 다른 σ** 를 내고 비가 등록식과 맞는가.
    #    거부만 시험하면 아무것도 못 재는 러너도 초록이 된다 (R4-01 이 정확히 그 모양이었다).
    atoms, rows_c, tm = _fixture()
    net_o = nc.build_network(atoms, rows_c, {3}, 1000.0, 12.0, box_x=40.0, box_y=40.0,
                             mode='ionic', type_map=tm, contact_mode='physics',
                             psi_placement=nc.PSI_DIVIDE)
    net_n = nc.build_network(atoms, rows_c, {3}, 1000.0, 12.0, box_x=40.0, box_y=40.0,
                             mode='ionic', type_map=tm, contact_mode='physics',
                             psi_placement=nc.PSI_MULTIPLY)
    s_o, n_act_o, _w = sigma_of(net_o, nc.solve_network)
    s_n, n_act_n, _w2 = sigma_of(net_n, nc.solve_network)
    chk('④ 합성 픽스처에 활성 간선이 있다 (없으면 이 대조가 공허하다)',
        n_act_o > 0 and n_act_o == n_act_n, f'활성 {n_act_o} / {n_act_n}')
    chk('④b 두 팔이 양수 σ 를 낸다', (s_o or 0) > 0 and (s_n or 0) > 0, f'{s_o!r} → {s_n!r}')
    chk('④c ★ 곱셈 팔의 σ 가 **더 크다** (활성 간선에서 Rc 가 작아지므로) — 등록된 상향 가설',
        s_o is not None and s_n is not None and s_n > s_o,
        f'σ {s_o!r} → {s_n!r} (Δ {(s_n - s_o) / s_o * 100:+.4f} %)')
    chk('④d 간선별로 Rc_new = ψ²·Rc_old (계약 §C 의 등록된 관계식)',
        _edgewise_psi2(net_o, net_n), '활성 간선 전부에서 1e-12 이내')

    #   ★★ ④e — `R4-08` 이 요구한 **여러 채널 대조**.  ④ 는 이온 한 채널이라 채널 dispatch ·
    #      k_weight 경로 · 정규화를 보증하지 못한다.  같은 기하를 **열 채널**로 다시 푼다
    #      (열은 모든 접촉을 쓰고 `k_weight` 가 다르다).
    #      ⛔ 전자 채널은 이 픽스처에 **없다** — SE 전용 침대라 AM–AM 간선이 0 이다.  그것이
    #        결함이 아니라 S0 실측(전자 삭제율 0.000 %)과 같은 구조다 (`SELF-28`).
    net_to = nc.build_network(atoms, rows_c, {3}, 1000.0, 12.0, box_x=40.0, box_y=40.0,
                              mode='thermal', type_map=tm, contact_mode='physics',
                              psi_placement=nc.PSI_DIVIDE)
    net_tn = nc.build_network(atoms, rows_c, {3}, 1000.0, 12.0, box_x=40.0, box_y=40.0,
                              mode='thermal', type_map=tm, contact_mode='physics',
                              psi_placement=nc.PSI_MULTIPLY)
    st_o, nt_act, _w3 = sigma_of(net_to, nc.solve_network)
    st_n, _nt2, _w4 = sigma_of(net_tn, nc.solve_network)
    #      ⚠ **값이 이온과 같게 나오는 것이 정상이다** — SE 전용 침대에서 SE–SE 의
    #        `k_weight` 는 1 이라 망이 같다.  ⇒ 이것은 **독립 측정이 아니고** 채널 경로
    #        (target_ids 전체 · k_weight 분기 · 단상 guard 완화)를 지나는지를 보는 것이다.
    chk('④e ★ 두 번째 채널(열)에서도 두 팔이 갈리고 곱셈이 더 크다 — 채널 dispatch 까지 본다',
        nt_act > 0 and (st_o or 0) > 0 and (st_n or 0) > 0 and st_n > st_o,
        f'활성 {nt_act} · σ_thermal {st_o!r} → {st_n!r} '
        f'(⚠ SE 전용이라 k_weight 1 ⇒ 이온과 같은 값 = 독립 측정 아님)')
    chk('④f 열 채널도 간선별 관계식을 지킨다', _edgewise_psi2(net_to, net_tn))

    # ⑤ 판별력 — 깃발을 무시하는 변이판은 ④c 를 **통과하지 못한다**.
    chk('⑤ ★ 두 팔이 같은 배치면 Δ = 0 이라 ④c 가 실패한다 (검사가 공허하지 않다)',
        not _arms_differ(nc, atoms, rows_c, tm, nc.PSI_DIVIDE, nc.PSI_DIVIDE),
        'legacy↔legacy 는 Δ 0')
    chk('⑤b 그리고 진짜 두 팔은 다르다', _arms_differ(nc, atoms, rows_c, tm,
                                                 nc.PSI_DIVIDE, nc.PSI_MULTIPLY))

    # ── ⑦ ★★ Codex R5 반례 회귀 (`AREA5-01`·`02`·`04`) ─────────────────────────
    #    판정문 §2 가 낸 세 반례를 **그대로** 박는다.  고친 뒤에도 같은 입력이 같은 답을
    #    내는지 보는 것이 이 시험의 전부다.  ⛔ 하나라도 초록으로 돌아가면 수리가 풀린 것이다.
    chk('⑦ ★ A-4 경계: |Δ|=[2,20] · 미정 1 · N=3 · ρ=0 → 하한 h0 / 상한 h1',
        bound_medians([2.0, 20.0], 3, 0.0)[1] == ('h0', 'h1'))
    chk('⑦b ★★ 그래서 라벨이 **UNDETERMINED_COHORT** 다 (옛 판은 complete-case median 11.0 → h1)',
        bound_medians([2.0, 20.0], 3, 0.0)[2] == 'UNDETERMINED_COHORT',
        str(bound_medians([2.0, 20.0], 3, 0.0)))
    chk('⑦c 미정이 없으면 두 경계가 같고 라벨이 비어 있다 (검사가 공허하지 않다)',
        bound_medians([2.0, 20.0, 20.0], 3, 0.0)[2] == '')
    chk('⑦d 상한이 +∞ 면 고정 ρ 에서 h1 (경계 전용 — 관측값이 아니다)',
        math.isinf(bound_medians([2.0], 3, 0.0)[0][1])
        and bound_medians([2.0], 3, 0.0)[1][1] == 'h1')
    #    ★ 판별력 — 실패를 **지우면** (complete-case) 옛 답이 돌아온다.
    chk('⑦e ★ 판별력: 미정을 분모에서 지우면 옛 `h1` 이 돌아온다 (그래서 봉인 N 을 쓴다)',
        bound_medians([2.0, 20.0], 2, 0.0)[1] == ('h1', 'h1'))

    # ⑧ ρ 증서 (`AREA5-04`) — 공식 판정의 유일한 ρ 입력
    _seal3 = {'sealed_at_kst': '2026-09-17T12:00:00+09:00',
              'seal_deadline': SEAL_DEADLINE.isoformat(), 'generation_git_sha': 'x',
              'rho_rule': RHO_RULE,
              'channels': {'ionic': {'ids': {IN_DOMAIN: ['c1', 'c2', 'c3']}}}}
    _cert = {'cohort_ids': ['c1', 'c2', 'c3'], 'channels': ['ionic'], 'generation': 'g1',
             'stop_criterion': 'rtol=1e-8, atol=0', 'aggregation': 'max |Δσ|/σ ×100',
             'rho': 0.0}
    with tempfile.TemporaryDirectory() as _td:
        _t = pathlib.Path(_td)

        def _cert_rho(d):
            _p = _t / 'c.json'
            _p.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
            return load_rho_certificate(_p, _seal3)

        chk('⑧ 온전한 증서는 ρ 를 준다', _cert_rho(_cert)[0] == 0.0, _cert_rho(_cert)[1])
        #    ★★ 이것이 내가 방금 넣었다가 잡은 버그다 — `not c.get(k)` 로 보면 `rho: 0.0` 이
        #       "키 없음" 으로 읽힌다.  **0 은 결측이 아니다** (`GAP2-05` 의 거울).
        chk('⑧b ★★ ρ = 0.0 을 "키 없음" 으로 읽지 않는다 (0 은 결측이 아니다)',
            _cert_rho(dict(_cert, rho=0.0))[0] == 0.0)
        for _k in ('cohort_ids', 'channels', 'generation', 'stop_criterion', 'aggregation', 'rho'):
            _d = {k: v for k, v in _cert.items() if k != _k}
            chk(f'⑧c 키 {_k} 가 없으면 거부', _cert_rho(_d)[0] is None)
        chk('⑧d ★ 봉인된 B_ch 를 다 안 덮는 증서는 거부 (mono 30 을 새 130 에 대입 금지)',
            _cert_rho(dict(_cert, cohort_ids=['zz1', 'zz2']))[0] is None)
        chk('⑧e 더 넓은 코호트는 받는다 (덮기만 하면 된다)',
            _cert_rho(dict(_cert, cohort_ids=['c1', 'c2', 'c3', 'c4']))[0] == 0.0)
        chk('⑧f 비유한 ρ 는 거부', _cert_rho(dict(_cert, rho='nan'))[0] is None)

    # ⑥ 러너 자신의 거부 — `main()` 을 인자로 불러 rc 를 본다.
    _argv = sys.argv[:]
    try:
        sys.argv = ['run_s3_psi.py']
        chk('⑥ `--seal` 없이 부르면 rc=2', main() == 2)
        sys.argv = ['run_s3_psi.py', '--seal', '/nonexistent/seal.json', '--rho', '1.0']
        chk('⑥b 없는 봉인이면 rc=2', main() == 2)
        with tempfile.TemporaryDirectory() as td:
            p = pathlib.Path(td) / 's.json'
            p.write_text(json.dumps({'sealed_at_kst': '2026-09-17T12:00:00+09:00',
                                     'seal_deadline': SEAL_DEADLINE.isoformat(),
                                     'generation_git_sha': 'x',
                                     'channels': {'ionic': {'ids': {IN_DOMAIN: ['a']}}}}),
                          encoding='utf-8')
            sys.argv = ['run_s3_psi.py', '--seal', str(p)]
            chk('⑥c ★ 봉인은 정상인데 ρ 가 없으면 rc=2 (기본값 0 을 쓰지 않는다)', main() == 2)
            sys.argv = ['run_s3_psi.py', '--seal', str(p), '--rho', '1.0']
            chk('⑥d 코호트 루트가 없으면 rc=2', main() == 2)
    finally:
        sys.argv = _argv

    print('S3 런 SELFTEST ' + ('FAIL' if fail else 'PASS'))
    return 1 if fail else 0


def _fixture():
    """합성 SE 사슬 — 벽까지 z 를 잇고 **활성 간선(ψ > 1e-4)** 을 갖는다.

    ⚠ 활성이려면 겹침이 얕아야 한다 (깊으면 clamp 로 ψ = 0).  δ/r 을 작게 둔다.
    """
    scale = 1000.0
    r = 0.5 / scale                      # 0.5 µm
    delta = 0.02 / scale                 # 활성 구간 (감사 픽스처와 같은 좌표)
    step = 2 * r - delta
    atoms, rows_c = {}, []
    n = 7
    for i in range(n):
        atoms[i + 1] = {'type': 3, 'radius': r, 'x': 0.0, 'y': 0.0, 'z': i * step}
        if i:
            rows_c.append({'id1': i, 'id2': i + 1,
                           'contact_area': 0.0, 'delta': delta})
    return atoms, rows_c, {3: 'SE'}


def _edgewise_psi2(net_o, net_n) -> bool:
    """활성 간선마다 `Rc_new / Rc_old == ψ²` — ψ 는 `a_eff/r_min` 에서 솔버식으로 다시 얻지 않고
    **비 자체가 ψ² 인지**를 두 팔의 `R_Maxwell` 로 교차 확인한다.

    `Rc_old = R_M/ψ` · `Rc_new = ψ·R_M` (같은 `a_eff`) ⇒ `Rc_old·Rc_new = R_M²`.
    ⇒ ψ 를 감사가 재구현하지 않고도 관계를 검사할 수 있다 (감사 재구현 금지 교훈).
    """
    n_seen = 0
    for eo, en in zip(net_o['edges'], net_n['edges']):
        ro, rn = eo.get('R_constriction') or 0.0, en.get('R_constriction') or 0.0
        if ro <= 0 or rn <= 0:
            continue
        rm = eo.get('R_Maxwell')
        if rm is None or rm <= 0:
            return False
        #  ⚠ `R_Maxwell` 은 clamp **전** a 로 계산된다 — 활성 간선은 clamp 가 안 걸리므로
        #    (걸리면 ψ=0 이라 비활성) 같은 a 이고 이 항등식이 성립한다.
        if abs(ro * rn - rm * rm) > 1e-12 * max(1.0, rm * rm):
            return False
        n_seen += 1
    return n_seen > 0


def _arms_differ(nc, atoms, rows_c, tm, p1, p2) -> bool:
    kw = dict(box_x=40.0, box_y=40.0, mode='ionic', type_map=tm, contact_mode='physics')
    a = nc.build_network(atoms, rows_c, {3}, 1000.0, 12.0, psi_placement=p1, **kw)
    b = nc.build_network(atoms, rows_c, {3}, 1000.0, 12.0, psi_placement=p2, **kw)
    sa, _na, _wa = sigma_of(a, nc.solve_network)
    sb, _nb, _wb = sigma_of(b, nc.solve_network)
    if sa is None or sb is None:
        return False
    return sa != sb


if __name__ == '__main__':
    sys.exit(main())
