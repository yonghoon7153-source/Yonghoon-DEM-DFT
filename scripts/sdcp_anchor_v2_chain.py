#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SDCP σ_e 실험 앵커 v2 사슬 — S1 정찰 → S2 σ_VGCF* → 비교 두 런 (등록 `docs/reviews/sdcp_sigma_e_dcp_anchor_registration_v2_20261019.md` §3 · §5).

  python3 scripts/sdcp_anchor_v2_chain.py --stage sbe --runner ~/dem-anchor1019/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --out ~/sdcp/anchor_v2_1019
  python3 scripts/sdcp_anchor_v2_chain.py --stage dbe --dbe-kit kit_DBE_sdcp1um --runner … --root ~/sdcp --out ~/sdcp/anchor_v2_1019
  python3 scripts/sdcp_anchor_v2_chain.py ... --dry-run      # 명령만 찍는다 (러너를 부르지 않는다)
  python3 scripts/sdcp_anchor_v2_chain.py --selftest

단계 (1저자 10-19 — SBE 침대는 그대로 · DBE 침대만 SDCP 평균 1 µm 로 재압밀):
  --stage sbe  S1 + S2 + SBE arm 0 @ σ* + 옛 DBE 킷 (kit_DBE · SDCP Ø0.30 낱알) arm 0 @ σ* (재압밀과 독립 — 1저자 *"값을 우선 비교"*)
  --stage dbe  같은 --out 의 요약에서 σ* 를 읽어 재압밀한 DBE 킷 (--dbe-kit · SDCP 평균 1 µm) arm 0 @ σ* · 비교 칸에 킷별로 더한다

규칙 (등록 §3 그대로 — 결과 전 고정 · 바꾸려면 등록부터):
  S1  SBE arm 0 · σ_e 만 (ARMS=1 LEAN=2) · σ_VGCF 1.309 · 0.6545 · 0.3272 S/cm (= 2.618 ÷ 2 · 4 · 8)
  S2  ln σ_e ↔ ln σ_VGCF 를 목표 SBE 1.63 mS/cm 를 끼는 이웃 두 점 사이 직선 보간 · 유효숫자 3 자리.  목표가 세 점 밖이면 같은 쪽으로
      ÷2 (0.1636 → 0.0818) 또는 ×2 (2.618 → 5.236) 점을 최대 둘 더 (같은 보간).  σ_e 가 σ_VGCF 에 단조 증가가 아니면 멈춘다.
  C   σ_VGCF* 에서 SBE arm 0 · DBE arm 0 (σ_e 만 · σ_SDCP 256.6 그대로) — 비교만 (판정 아님 · 16 팔 = 1저자 결정 뒤 · 등록 §3).
  공통 env = VOX 0.15 · SDCP_SPHERE_D 0.30 · PTFE_STAMP centerline · BRIDGE_UM 0.48 · SIGMA_AM_S_OVERRIDE 0.0041 · SIGMA_SDCP_OVERRIDE 256.6 ·
  출력 폴더 = --out 아래 런마다 새 폴더 (`_arm1` 로 끝남 — 러너 접미사 규칙).  ★ 10-19 (`SELF-120`) — 이온 축 (SIGMA_ION_* · PTFE_BLOCK_*) 은 넣지 않고
  부모 셸에서 물려받은 것도 지운다: LEAN=2 (σ_e 만 · --no-ion) 런에 이온 축이 있으면 러너가 계산 전에 ABORT (rc 2) 한다 (첫 kgy 발사가 그렇게 멈췄다).
멈춤 (rc 3 · 그 자리까지의 요약은 남긴다): ★ 10-20 (Z1) 부모 셸에 다음 세대 노브 (CJUNC* · SDCP_MOD_C · STEP3_RTOL · SIGMA_FIBRE_BULK) =
  러너 부르기 전 거부 (`NEXTGEN_ENV` · 지우지 않는다) · 출력 폴더가 이미 있고 비어 있지 않음 (러너 SKIP 캐시가 옛 팔을 재사용하는 것을 막는다) · 러너 rc ≠ 0 ·
  σ_e 를 실은 팔 JSON ≠ 1 · 매니페스트 (σ_VGCF · σ_AM_S · σ_SDCP · vox · 브리지 · PTFE · SDCP 구 지름) ≠ 요청 · 수렴 (`run_contract.conv_ok`) 실패 ·
  둘 더해도 목표 밖 · 단조 아님 · 시간 상한 (--max-hours).
판정을 하지 않는다 — 요약 (`chain_summary.json`) 에 S1 점 · σ* · 비교 두 값 · 실험값 옆 비를 적을 뿐 (해석 = 1저자 · 등록 §3).
"""
import argparse
import glob
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

#: 등록 §1 · §3 (값은 등록 문서가 정본 — 여기는 그 사본 하나 · 시험 S 가 문서와 대조한다)
TARGET_SBE_MS = 1.63
EXP_DBE_MS = 4.68
EXP_RATIO = 2.86
LADDER = ('1.309', '0.6545', '0.3272')
EXT_DOWN = ('0.1636', '0.0818')
EXT_UP = ('2.618', '5.236')
MAX_EXT = 2
ENV_FIXED = {'VOX': '0.15', 'SDCP_SPHERE_D': '0.30', 'PTFE_STAMP': 'centerline', 'BRIDGE_UM': '0.48', 'ARMS': '1', 'LEAN': '2',
             'SIGMA_AM_S_OVERRIDE': '0.0041', 'SIGMA_SDCP_OVERRIDE': '256.6'}
#: LEAN=2 런에서 지우는 부모 env 접두 (러너 가드 — 이온을 안 푸는 런에 이온 축 = ABORT)
ENV_SCRUB_PREFIX = ('SIGMA_ION_', 'PTFE_BLOCK_')
#: ★ 2026-10-20 (Rint ② Z1) — **다음 세대 노브** (현 세대 사슬 = 등록 v2 · 그것 없이 돈다).  부모 셸에 있으면 **거부** (지우지 않는다 = 사람이 안다).
#   이름 = 러너 손잡이 표 정본 (`run_contract.RUNNER_CA_EXT_ENV` — CJUNC* · SDCP_MOD_C · STEP3_RTOL · SIGMA_FIBRE_BULK · 사본 없음) +
#   `CJUNC` 접두 (오타 이름까지).  ⚠ 값이 비어도 거부한다 (있기만 해도 — 셸 rc 의 흔적을 사람이 지운다).
#   안 막으면: 러너가 접합 · bulk 팔을 같은 `p2_*.json` 꼴로 내고 read_arm 은 σ_VGCF · σ_AM_S · vox … 만 대조해 받는다 (현 세대 표 오염).
import run_contract as _RC0                                     # noqa: E402 — HERE 를 sys.path 에 넣은 뒤
NEXTGEN_ENV_NAMES = tuple(n for n, _s, _k in _RC0.RUNNER_CA_EXT_ENV)
NEXTGEN_ENV_PREFIX = ('CJUNC',)


def nextgen_env_found(env):
    """env → 다음 세대 노브 이름 (정렬) — 하나라도 있으면 현 세대 사슬은 멈춘다."""
    return sorted(k for k in (env or {}) if k in NEXTGEN_ENV_NAMES or k.startswith(NEXTGEN_ENV_PREFIX))
#: 매니페스트 키 → 기대값 (env 와 같은 값 · 상대 1e-9)
MAN_EXPECT = {'sigma_am_s_S_cm': 0.0041, 'sigma_sdcp_S_cm': 256.6, 'vox_um': 0.15, 'bridge_um': 0.48, 'sdcp_sphere_d_um': 0.30}
KITS = {'SBE': 'kit_SBE', 'DBE': 'kit_DBE'}
SDCP_KEYS = ('sigma_sdcp_S_cm', 'sdcp_sphere_d_um')


class Stop(Exception):
    """등록 멈춤 조건."""


def sig3(x):
    """유효숫자 3 자리 문자열 (러너 env 에 그대로 넘긴다 · 매니페스트 대조도 이 문자열의 float)."""
    s = f'{x:.3g}'
    if 'e' in s:
        raise Stop(f'σ* {x!r} 가 지수 표기로만 3 자리가 된다 — 사다리 범위 밖 (등록 §3)')
    return s


def s2_rule(points, target):
    """points = {σ 문자열: σ_e (mS/cm)} → ('ok', σ* 문자열, (lo, hi)) | ('down', None, None) | ('up', None, None) | Stop.
    이웃 두 점 (σ 오름차순) 사이에서 목표를 끼면 ln–ln 직선 보간 · 유효숫자 3 자리."""
    xs = sorted(points, key=float)
    ys = [points[x] for x in xs]
    if any(not (isinstance(y, float) and math.isfinite(y) and y > 0) for y in ys):
        raise Stop(f'σ_e 가 유한 양수가 아니다 {dict(zip(xs, ys))}')
    if any(b <= a for a, b in zip(ys, ys[1:])):
        raise Stop(f'σ_e 가 σ_VGCF 에 단조 증가가 아니다 {dict(zip(xs, ys))} — 보간 규칙 밖 (등록 §3)')
    if target < ys[0]:
        return 'down', None, None
    if target > ys[-1]:
        return 'up', None, None
    for (xa, ya), (xb, yb) in zip(zip(xs, ys), zip(xs[1:], ys[1:])):
        if ya <= target <= yb:
            la, lb = math.log(float(xa)), math.log(float(xb))
            t = (math.log(target) - math.log(ya)) / (math.log(yb) - math.log(ya))
            return 'ok', sig3(math.exp(la + t * (lb - la))), (xa, xb)
    raise Stop('보간 구간을 찾지 못했다')                       # 단조 · 범위 검사 뒤에는 오지 않는다


def _num_eq(a, b):
    try:
        a = float(a)
    except (TypeError, ValueError):
        return False
    return math.isfinite(a) and abs(a - b) <= 1e-9 * max(1.0, abs(b))


def read_arm(outdir, sg, kit_name):
    """출력 폴더 → σ_e (mS/cm) · 수렴 · 매니페스트 대조 (어긋나면 Stop)."""
    import run_contract as rc
    rej = sorted(glob.glob(os.path.join(outdir, '.rejected_*')))
    if rej:
        raise Stop(f'{outdir}: 러너 기각 기록 {[os.path.basename(x) for x in rej]} — 봉인이 깨진 팔은 읽지 않는다')
    found = []
    for p in sorted(glob.glob(os.path.join(outdir, 'p2_*.json'))):             # 판정기 `sdcp_gain_verdict.collect` 와 같은 자리 · 같은 이름
        try:
            d = json.load(open(p, encoding='utf-8'))
        except Exception:                                        # noqa: BLE001 — JSON 아닌 것 · 깨진 것은 팔 후보가 아니다
            continue
        if not isinstance(d, dict):
            continue
        s = d.get('step3') or (d.get('mpm_metrics') or {}).get('step3') or {}
        if isinstance(s, dict) and 'sigma_e_eff_S_cm' in s:
            found.append((p, s))
    if len(found) != 1:
        raise Stop(f'{outdir}: σ_e 를 실은 팔 JSON (p2_*.json) {len(found)} 개 (1 이어야 · ARMS=1 · 한 킷) {[os.path.basename(p) for p, _ in found][:4]}')
    p, s = found[0]
    ok, why = rc.conv_ok(s.get('cg_info'), s.get('unconverged'), s.get('cg_resid'))
    if not ok:
        raise Stop(f'{p}: 수렴 실패 ({why} · cg_info {s.get("cg_info")!r} · unconverged {s.get("unconverged")!r} · resid {s.get("cg_resid")!r})')
    man = s.get('manifest') or {}
    bad = []
    if not _num_eq(man.get('sigma_vgcf_S_cm'), float(sg)):
        bad.append(f'sigma_vgcf_S_cm {man.get("sigma_vgcf_S_cm")!r} ≠ {sg}')
    for k, v in MAN_EXPECT.items():
        if kit_name == 'SBE' and k in SDCP_KEYS and man.get(k) is None:
            continue                                             # SBE 는 SDCP 상이 없다 — 기록이 없으면 넘어가고 · 있으면 같아야
        if not _num_eq(man.get(k), v):
            bad.append(f'{k} {man.get(k)!r} ≠ {v}')
    if man.get('ptfe_stamp') != 'centerline':
        bad.append(f'ptfe_stamp {man.get("ptfe_stamp")!r} ≠ centerline')
    if bad:
        raise Stop(f'{p}: 매니페스트 ≠ 등록 ({kit_name}) — ' + ' · '.join(bad))
    v = s.get('sigma_e_eff_S_cm')
    if not (isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) and v > 0):
        raise Stop(f'{p}: σ_e {v!r} 가 유한 양수가 아니다')
    return float(v) * 1000.0, os.path.basename(p)


class Chain:
    def __init__(self, runner, root, out, dry=False, max_hours=8.0, python_env=None):
        self.runner, self.root, self.out = Path(runner), Path(root), Path(out)
        self.dry, self.deadline = dry, time.time() + max_hours * 3600.0
        self.env_base = dict(os.environ if python_env is None else python_env)
        self.summary = {'registration': 'docs/reviews/sdcp_sigma_e_dcp_anchor_registration_v2_20261019.md', 'target_sbe_mScm': TARGET_SBE_MS,
                        'exp_dbe_mScm': EXP_DBE_MS, 'exp_ratio': EXP_RATIO, 'env_fixed': ENV_FIXED, 'runs': [], 's1': {}, 'stop': None}
        self.calls = []

    def run(self, name, kit, sg):
        _ng = nextgen_env_found(self.env_base)
        if _ng:                                                  # ★ Z1 — 러너를 부르기 전 · dry-run 도 (찍은 명령이 실제 런과 갈리지 않게)
            raise Stop(f'NEXTGEN_ENV| 부모 셸에 다음 세대 노브 {_ng} 가 있다 — 현 세대 사슬 (등록 v2) 은 그것 없이 돈다.  '
                       f'지우지 않고 멈춘다: `unset {" ".join(_ng)}` 하고 다시 (러너가 접합 · bulk 팔을 같은 p2_*.json 꼴로 내면 '
                       f'read_arm 이 받는다)')
        outdir = self.out / f'{name}_arm1'
        base = {k: v for k, v in self.env_base.items() if not k.startswith(ENV_SCRUB_PREFIX)}
        env = dict(base, **ENV_FIXED, KITS=KITS[kit], SIGMA_VGCF_OVERRIDE=sg, OUTDIR=str(outdir))
        cmd = ['bash', str(self.runner)]
        rec = {'name': name, 'kit': kit, 'sigma_vgcf': sg, 'outdir': str(outdir)}
        self.calls.append(rec)
        if self.dry:
            print('  env ' + ' '.join(f'{k}={env[k]}' for k in list(ENV_FIXED) + ['KITS', 'SIGMA_VGCF_OVERRIDE', 'OUTDIR']) + f' bash {self.runner}')
            return None
        if outdir.exists() and any(outdir.iterdir()):
            raise Stop(f'{outdir} 가 이미 있고 비어 있지 않다 — 러너 SKIP 캐시가 옛 팔을 재사용한다 (새 --out 을 쓸 것)')
        left = self.deadline - time.time()
        if left <= 0:
            raise Stop('시간 상한 (--max-hours) 을 넘었다')
        (self.out / 'logs').mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        with open(self.out / 'logs' / f'{name}.log', 'w', encoding='utf-8') as lf:
            try:
                r = subprocess.run(cmd, cwd=str(self.root), env=env, stdout=lf, stderr=subprocess.STDOUT, timeout=left)
            except subprocess.TimeoutExpired:
                raise Stop(f'{name}: 시간 상한 안에 끝나지 않았다')
        rec['rc'], rec['seconds'] = r.returncode, round(time.time() - t0, 1)
        if r.returncode != 0:
            raise Stop(f'{name}: 러너 rc {r.returncode} (로그 {self.out / "logs" / (name + ".log")})')
        rec['sigma_e_mScm'], rec['arm_json'] = read_arm(str(outdir), sg, kit)
        self.summary['runs'].append(rec)
        print(f'  {name}: σ_VGCF {sg} → σ_e {rec["sigma_e_mScm"]:.4f} mS/cm ({rec["seconds"]:.0f} s)')
        return rec['sigma_e_mScm']

    def _dbe(self, kit, sstar, e_s):
        """DBE 킷 하나 arm 0 @ σ* → compare['dbe'][킷]."""
        KITS['DBE'] = kit
        try:
            e_d = self.run(f'c_{kit}_sg{sstar}', 'DBE', sstar)
        finally:
            KITS['DBE'] = 'kit_DBE'
        if e_d is None:
            return
        rec = {'dbe_mScm': e_d, 'ratio': e_d / e_s, 'dbe_vs_exp_pct': (e_d / EXP_DBE_MS - 1) * 100}
        self.summary['compare'].setdefault('dbe', {})[kit] = rec
        print(f'  DBE [{kit}] {e_d:.4f} mS/cm (실험 {EXP_DBE_MS} 대비 {rec["dbe_vs_exp_pct"]:+.1f} %) · 비 {rec["ratio"]:.4f} (실험 {EXP_RATIO})')

    def go_dbe(self, dbe_kit):
        """DBE arm 0 @ σ* — σ* = 같은 --out 의 sbe 단계 요약 (사람이 옮겨 적지 않는다)."""
        prev = self.out / 'chain_summary.json'
        if not prev.is_file():
            raise Stop(f'{prev} 없음 — --stage sbe 를 먼저 (σ* 는 그 요약에서만 읽는다)')
        old = json.loads(prev.read_text(encoding='utf-8'))
        sstar = (old.get('s2') or {}).get('sigma_star')
        e_s = (old.get('compare') or {}).get('sbe_mScm')
        if old.get('stop') or not sstar or not isinstance(e_s, float):
            raise Stop(f'sbe 단계가 끝나지 않았다 (멈춤 {old.get("stop")!r} · σ* {sstar!r} · SBE {e_s!r})')
        self.summary.update({k: old[k] for k in ('s1', 's2', 'runs', 'code') if k in old})
        self.summary['runs'] = list(old.get('runs') or [])
        self.summary['compare'] = json.loads(json.dumps(old.get('compare') or {}))
        if dbe_kit in (self.summary['compare'].get('dbe') or {}):
            raise Stop(f'{dbe_kit} 비교 값이 이미 요약에 있다 — 같은 킷을 두 번 돌리지 않는다 (새 --out 또는 다른 킷)')
        print(f'C 비교 (DBE arm 0 @ σ* {sstar} · 킷 {dbe_kit} · σ_SDCP 256.6 그대로)')
        self._dbe(dbe_kit, sstar, e_s)
        return 0

    def go(self):
        pts = self.summary['s1']
        print('S1 정찰 (SBE arm 0 · σ_e 만)')
        for sg in LADDER:
            v = self.run(f's1_sbe_sg{sg}', 'SBE', sg)
            if v is not None:
                pts[sg] = v
        if self.dry:
            print('S2 = 위 점들로 보간 (등록 §3) · C = σ* 에서 SBE · DBE arm 0 — 결과가 있어야 정해진다 (dry-run 끝)')
            return 0
        ext = 0
        while True:
            how, sstar, pair = s2_rule(pts, TARGET_SBE_MS)
            if how == 'ok':
                break
            if ext >= MAX_EXT:
                raise Stop(f'둘 더해도 목표 {TARGET_SBE_MS} mS/cm 가 정찰 점 밖 ({how}) {pts} (등록 §3 — 사람이 정한다)')
            sg = (EXT_DOWN if how == 'down' else EXT_UP)[ext]
            ext += 1
            print(f'S1 + 점 {ext} ({how}) σ_VGCF {sg}')
            pts[sg] = self.run(f's1_sbe_sg{sg}', 'SBE', sg)
        self.summary['s2'] = {'sigma_star': sstar, 'bracket': list(pair), 'extensions': ext}
        print(f'S2 σ_VGCF* = {sstar} S/cm (보간 구간 {pair[0]} – {pair[1]})')
        print('C 비교 — SBE arm 0 @ σ* · 옛 DBE 킷 arm 0 @ σ* (재압밀한 DBE = --stage dbe)')
        e_s = self.run(f'c_kit_SBE_sg{sstar}', 'SBE', sstar)
        self.summary['compare'] = {'sbe_mScm': e_s, 'sbe_vs_target_pct': (e_s / TARGET_SBE_MS - 1) * 100, 'dbe': {},
                                   'note': '판정 아님 — 해석 · 다음 단계 = 1저자 (등록 §3)'}
        print(f'  SBE {e_s:.4f} mS/cm (목표 {TARGET_SBE_MS} 대비 {self.summary["compare"]["sbe_vs_target_pct"]:+.2f} %)')
        if (self.root / 'kit_DBE').exists():
            self._dbe('kit_DBE', sstar, e_s)
        return 0


def git_identity(path):
    try:
        d = str(Path(path).resolve().parent)
        head = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
        dirty = subprocess.run(['git', '-C', d, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout.strip()
        return {'head': head or None, 'dirty': bool(dirty)}
    except Exception as e:                                       # noqa: BLE001
        return {'head': None, 'error': str(e)}


def main(argv=None):
    try:                                   # ★ SELF-122 — 화면을 파일로 돌려도 (setsid nohup … > log) 줄마다 바로 쓴다 (옛 판: 끝날 때까지 빈 로그)
        sys.stdout.reconfigure(line_buffering=True)
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--runner')
    ap.add_argument('--root', help='킷 (kit_SBE · kit_DBE) 이 있는 폴더 = 러너 작업 폴더')
    ap.add_argument('--out', help='새 출력 뿌리 (런마다 그 아래 새 폴더)')
    ap.add_argument('--stage', choices=('sbe', 'dbe'))
    ap.add_argument('--dbe-kit', default='', help='--stage dbe — 재압밀한 DBE 킷 폴더 이름 (--root 아래)')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--max-hours', type=float, default=8.0)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.runner and a.root and a.out and a.stage):
        ap.error('--stage · --runner · --root · --out 이 필요하다')
    if a.stage == 'dbe' and not a.dbe_kit:
        ap.error('--stage dbe 는 --dbe-kit 이 필요하다 (재압밀한 DBE 킷)')
    if not Path(a.runner).is_file():
        ap.error(f'러너 없음: {a.runner}')
    need = [KITS['SBE']] if a.stage == 'sbe' else [a.dbe_kit]
    for k in need:
        if not (Path(a.root) / k).exists():
            ap.error(f'킷 없음: {Path(a.root) / k}')
    ch = Chain(a.runner, a.root, a.out, dry=a.dry_run, max_hours=a.max_hours)
    ch.summary['code'] = git_identity(a.runner)
    rc_ = 0
    try:
        rc_ = ch.go() if a.stage == 'sbe' else ch.go_dbe(a.dbe_kit)
    except Stop as e:
        ch.summary['stop'] = str(e)
        print(f'멈춤 (등록 §3 · §5): {e}')
        rc_ = 3
    if not a.dry_run:
        Path(a.out).mkdir(parents=True, exist_ok=True)
        Path(a.out, 'chain_summary.json').write_text(json.dumps(ch.summary, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f'요약 → {Path(a.out, "chain_summary.json")}')
    return rc_


# ══ 자기 시험 — 가짜 러너 (env 를 읽어 팔 JSON 하나를 쓴다) ═══════════════════════════════════════════════════════════════════════════
FAKE = r'''import json, os, sys, math
sg = float(os.environ['SIGMA_VGCF_OVERRIDE']); kit = os.environ['KITS']; mode = os.environ.get('FAKE_MODE', 'normal')
out = os.environ['OUTDIR']; os.makedirs(out, exist_ok=True)
if os.environ.get('LEAN') == '2' and any(os.environ.get(k) for k in os.environ if k.startswith(('SIGMA_ION_', 'PTFE_BLOCK_'))):
    print('ABORT — 이온 축(SIGMA_ION_* 또는 PTFE_BLOCK_*)을 줬는데 LEAN=2 의 조립 flags 에 --no-ion 이 있다.'); sys.exit(2)   # 실제 러너 가드 그대로
if mode == 'rc1':
    sys.exit(1)
a, b, f = 2.6, 0.55, 0.05
if mode == 'low': a = 4.0                       # 목표가 세 점 아래 → ÷2 점 하나
if mode == 'flat': a, b, f = 0.0, 0.5, 5.0      # 늘 목표 위 · 평평 → 단조 아님
if mode == 'high': a = 0.9                      # 목표가 세 점 위 → ×2 점 하나
e = (a * sg ** b + f) * (1.25 if 'DBE' in kit else 1.0) if mode != 'flat' else 5.0
man = {'sigma_vgcf_S_cm': sg, 'sigma_am_s_S_cm': 0.0041, 'sigma_sdcp_S_cm': 256.6, 'vox_um': 0.15, 'bridge_um': 0.48,
       'sdcp_sphere_d_um': 0.30, 'ptfe_stamp': 'centerline'}
if mode == 'badman' and abs(sg - 0.6545) < 1e-12: man['sigma_am_s_S_cm'] = 0.01
if mode in ('nosdcpkeys', 'nosdcpdbe') and 'SBE' in kit: man.pop('sigma_sdcp_S_cm'); man.pop('sdcp_sphere_d_um')
if mode == 'nosdcpdbe' and 'DBE' in kit: man.pop('sdcp_sphere_d_um')
if mode == 'rejected' and abs(sg - 1.309) < 1e-12: open(os.path.join(out, '.rejected_20261019T000000Z'), 'w').write('x')
s = {'sigma_e_eff_S_cm': e / 1000.0, 'cg_info': 0, 'unconverged': False, 'cg_resid': 1e-9, 'manifest': man}
if mode == 'unconv' and abs(sg - 0.6545) < 1e-12: s.update(cg_info=30000, unconverged=True)
json.dump({'step3': s}, open(os.path.join(out, 'p2_X_a0.json'), 'w'))
if mode == 'two' and abs(sg - 1.309) < 1e-12:
    json.dump({'step3': s}, open(os.path.join(out, 'p2_Y_a0.json'), 'w'))
'''


def selftest():
    ok, fail = 0, []

    def chk(name, cond, extra=''):
        nonlocal ok
        if cond:
            ok += 1
            print(f'  PASS  {name}')
        else:
            fail.append(name)
            print(f'  FAIL  {name}   {str(extra)[:400]}')

    def model(sg, a=2.6, b=0.55, f=0.05):
        return a * sg ** b + f

    td = Path(tempfile.mkdtemp(prefix='sdcp_chain_st_'))
    try:
        (td / 'fake.py').write_text(FAKE, encoding='utf-8')
        runner = td / 'runner.sh'
        runner.write_text(f'#!/bin/bash\nexec {sys.executable} -I {td / "fake.py"}\n', encoding='utf-8')
        root = td / 'root'
        (root / 'kit_SBE').mkdir(parents=True)
        (root / 'kit_DBE').mkdir()

        def go(mode, tag, prefill=False, stage='sbe', dbe_kit='kit_DBE'):
            out = td / f'out_{tag}'
            if prefill:
                (out / f's1_sbe_sg{LADDER[0]}_arm1').mkdir(parents=True)
                (out / f's1_sbe_sg{LADDER[0]}_arm1' / 'old.json').write_text('{}')
            env = dict(os.environ, FAKE_MODE=mode)
            ch = Chain(runner, root, out, python_env=env)
            try:
                rc_ = ch.go() if stage == 'sbe' else ch.go_dbe(dbe_kit)
            except Stop as e:
                ch.summary['stop'] = str(e)
                rc_ = 3
            out.mkdir(parents=True, exist_ok=True)
            (out / 'chain_summary.json').write_text(json.dumps(ch.summary, ensure_ascii=False), encoding='utf-8')
            KITS['DBE'] = 'kit_DBE'
            return rc_, ch

        # T1 정상 — σ* = 끼는 두 사다리 점의 ln–ln 보간 (독립 계산) · 비교 두 런
        rc_, ch = go('normal', 'normal')
        pts = {sg: model(float(sg)) for sg in LADDER}
        xs = sorted(pts, key=float)
        want = None
        for xa, xb in zip(xs, xs[1:]):
            if pts[xa] <= TARGET_SBE_MS <= pts[xb]:
                t = (math.log(TARGET_SBE_MS) - math.log(pts[xa])) / (math.log(pts[xb]) - math.log(pts[xa]))
                want = f'{math.exp(math.log(float(xa)) + t * (math.log(float(xb)) - math.log(float(xa)))):.3g}'
        cmp_ = ch.summary.get('compare') or {}
        chk(f'T1 sbe 단계 정상 → σ* = 독립 보간 {want} · SBE arm 0 · 옛 kit_DBE arm 0 @ σ* (비 1.25 가짜 모형) · 런 다섯', rc_ == 0 and want is not None
            and ch.summary.get('s2', {}).get('sigma_star') == want and len(ch.summary['runs']) == 5
            and abs(((cmp_.get('dbe') or {}).get('kit_DBE') or {}).get('ratio', 0) - 1.25) < 1e-9
            and abs(cmp_.get('sbe_mScm', 0) - model(float(want))) < 1e-9, (rc_, ch.summary))
        (root / 'kit_DBE_sdcp1um').mkdir(exist_ok=True)
        rc_d, ch_d = go('normal', 'normal', stage='dbe', dbe_kit='kit_DBE_sdcp1um')
        cd = (ch_d.summary.get('compare') or {}).get('dbe') or {}
        rc_d2, ch_d2 = go('normal', 'normal', stage='dbe', dbe_kit='kit_DBE_sdcp1um')
        chk('T1b dbe 단계 → 같은 --out 요약의 σ* 로 재압밀 킷 arm 0 · 옛 kit_DBE 값 보존 · 킷별 칸 둘 · 런 여섯 · 같은 킷 두 번 = 멈춤',
            rc_d == 0 and set(cd) == {'kit_DBE', 'kit_DBE_sdcp1um'} and abs(cd['kit_DBE_sdcp1um']['ratio'] - 1.25) < 1e-9
            and len(ch_d.summary['runs']) == 6 and rc_d2 == 3 and '두 번' in (ch_d2.summary.get('stop') or ''), (rc_d, ch_d.summary.get('stop'), cd))
        rc_e, ch_e = go('normal', 'nosum', stage='dbe')
        chk('T1c sbe 요약 없이 dbe 단계 → 멈춤', rc_e == 3 and '--stage sbe' in (ch_e.summary.get('stop') or ''), ch_e.summary.get('stop'))
        # T2 목표가 세 점 아래 → ÷2 점 하나 (0.1636) 더 · 보간
        rc_, ch = go('low', 'low')
        chk('T2 목표 < 세 점 → ÷2 점 0.1636 하나 더 → 보간 (확장 1)', rc_ == 0 and ch.summary.get('s2', {}).get('extensions') == 1
            and '0.1636' in ch.summary['s1'], (rc_, ch.summary.get('s2'), ch.summary.get('stop')))
        # T2b 목표가 세 점 위 → ×2 점 (2.618) 더
        rc_, ch = go('high', 'high')
        chk('T2b 목표 > 세 점 → ×2 점 2.618 더 → 보간', rc_ == 0 and '2.618' in ch.summary['s1'] and ch.summary.get('s2', {}).get('extensions', 0) >= 1,
            (rc_, ch.summary.get('s2'), ch.summary.get('stop')))
        # T3 평평 (단조 아님) → 멈춤 · 비교 런 없음
        rc_, ch = go('flat', 'flat')
        chk('T3 σ_e 단조 아님 → 멈춤 rc 3 · 비교 런 없음', rc_ == 3 and '단조' in (ch.summary.get('stop') or '') and 'compare' not in ch.summary, ch.summary.get('stop'))
        # T4 수렴 실패 → 멈춤
        rc_, ch = go('unconv', 'unconv')
        chk('T4 정찰 둘째 점 미수렴 → 멈춤 (수렴 실패)', rc_ == 3 and '수렴 실패' in (ch.summary.get('stop') or ''), ch.summary.get('stop'))
        # T5 매니페스트 어긋남 → 멈춤
        rc_, ch = go('badman', 'badman')
        chk('T5 매니페스트 σ_AM_S ≠ 0.0041 → 멈춤', rc_ == 3 and 'sigma_am_s_S_cm' in (ch.summary.get('stop') or ''), ch.summary.get('stop'))
        # T6 러너 rc 1 → 멈춤
        rc_, ch = go('rc1', 'rc1')
        chk('T6 러너 rc 1 → 멈춤', rc_ == 3 and '러너 rc 1' in (ch.summary.get('stop') or ''), ch.summary.get('stop'))
        # T7 출력 폴더가 이미 있고 비어 있지 않음 → 러너 부르기 전 멈춤
        rc_, ch = go('normal', 'prefill', prefill=True)
        chk('T7 옛 출력 폴더 (SKIP 캐시 위험) → 러너 부르기 전 멈춤', rc_ == 3 and 'SKIP' in (ch.summary.get('stop') or '') and not ch.summary['runs'],
            ch.summary.get('stop'))
        # T8 σ_e 를 실은 JSON 둘 → 멈춤
        rc_, ch = go('two', 'two')
        chk('T8 팔 JSON 둘 → 멈춤', rc_ == 3 and '2 개' in (ch.summary.get('stop') or ''), ch.summary.get('stop'))
        # T8b SBE 매니페스트에 SDCP 키 없음 = 통과 · DBE 에 없음 = 멈춤 · 러너 기각 기록 = 멈춤
        rc_a, ch_a = go('nosdcpkeys', 'nosdcp')
        go('nosdcpdbe', 'nosdcpdbe')                             # sbe 단계 (SBE 결손 = 통과) → 같은 --out 에 요약
        rc_b, ch_b = go('nosdcpdbe', 'nosdcpdbe', stage='dbe', dbe_kit='kit_DBE_sdcp1um')
        rc_c, ch_c = go('rejected', 'rejected')
        chk('T8b SBE 의 SDCP 키 결손 = 통과 (SDCP 상 없음) · DBE 의 결손 = 멈춤 · .rejected_* = 멈춤',
            rc_a == 0 and rc_b == 3 and 'sdcp_sphere_d_um' in (ch_b.summary.get('stop') or '') and rc_c == 3 and '기각' in (ch_c.summary.get('stop') or ''),
            (rc_a, ch_a.summary.get('stop'), rc_b, ch_b.summary.get('stop'), rc_c, ch_c.summary.get('stop')))
        # T9 dry-run — 러너를 부르지 않는다 · 세 정찰 명령
        ch = Chain(runner, root, td / 'out_dry', dry=True)
        buf = []
        import contextlib
        import io
        with contextlib.redirect_stdout(io.StringIO()) as so:
            ch.go()
        txt = so.getvalue()
        chk('T9 dry-run → 명령 셋만 찍고 출력 폴더 없음', len(ch.calls) == 3 and not (td / 'out_dry').exists() and txt.count('bash ') == 3
            and 'SIGMA_SDCP_OVERRIDE=256.6' in txt and 'LEAN=2' in txt, txt[:300])
        # T10 S2 규칙 단위 — 3 자리 · 경계 · 단조
        r1 = s2_rule({'1.309': 3.0, '0.6545': 2.0, '0.3272': 1.5}, 1.63)
        r2 = s2_rule({'1.309': 3.0, '0.6545': 2.0, '0.3272': 1.63}, 1.63)
        r3 = s2_rule({'1.309': 3.0, '0.6545': 2.0, '0.3272': 1.7}, 1.63)
        try:
            s2_rule({'1.309': 3.0, '0.6545': 3.5, '0.3272': 1.0}, 1.63)
            r4 = 'no stop'
        except Stop as e:
            r4 = str(e)
        lo = math.log(0.3272) + (math.log(1.63) - math.log(1.5)) / (math.log(2.0) - math.log(1.5)) * (math.log(0.6545) - math.log(0.3272))
        chk(f'T10 S2 — 보간 3 자리 {r1} (독립 {math.exp(lo):.3g}) · 끝점 = 목표면 그 점 · 위 = down · 단조 아님 = 멈춤',
            r1[0] == 'ok' and r1[1] == f'{math.exp(lo):.3g}' and r2[:2] == ('ok', '0.327') and r3[0] == 'down' and '단조' in r4, (r1, r2, r3, r4))
        # T12 ★ 부모 셸에 이온 축 (SIGMA_ION_SE) 이 export 돼 있어도 σ_e 런 (LEAN=2) 은 돈다 — 사슬이 지운다 (러너 가드 rc 2 재발 방지)
        os.environ['SIGMA_ION_SE'] = '0.0015'
        try:
            rc_12, ch_12 = go('normal', 'inherit_ion')
        finally:
            os.environ.pop('SIGMA_ION_SE', None)
        chk('T12 부모 env 의 SIGMA_ION_SE → 지우고 돈다 (LEAN=2 러너 가드 통과)', rc_12 == 0 and len(ch_12.summary['runs']) == 5, ch_12.summary.get('stop'))
        # T14 ★ (Rint ② Z1 · 10-20) 부모 셸의 **다음 세대 노브** (CJUNC* · SDCP_MOD_C · STEP3_RTOL · SIGMA_FIBRE_BULK) = 거부 (지우지 않는다 = 사람이 안다).
        #     안 막으면 러너가 접합 · bulk 팔을 같은 `p2_*.json` 꼴로 내고 read_arm 이 σ_VGCF · σ_AM_S 만 대조해 받는다 (현 세대 사슬 오염).
        bad14 = []
        for nm in ('CJUNC', 'CJUNC_RJ', 'CJUNC_BOGUS', 'SDCP_MOD_C', 'STEP3_RTOL', 'SIGMA_FIBRE_BULK'):
            os.environ[nm] = '1'
            try:
                rc14, ch14 = go('normal', f'ng_{nm}')
            finally:
                os.environ.pop(nm, None)
            st14 = ch14.summary.get('stop') or ''
            if not (rc14 == 3 and 'NEXTGEN_ENV' in st14 and nm in st14 and not ch14.summary['runs']):
                bad14.append((nm, rc14, st14[:160]))
        chk('T14 부모 env 의 다음 세대 노브 여섯 → 러너 부르기 전 멈춤 (NEXTGEN_ENV · 그 이름 · 런 0)', not bad14, bad14)
        # T13 ★ (SELF-122) 사슬 화면을 파일로 돌려도 (setsid nohup … > log) 줄이 바로 찍힌다 — 옛 판은 print 를 flush 하지 않아 첫 런이 도는 동안 로그가 비어 있었다
        #     (10-19 kgy 첫 S1 — 1저자 "들어간거야?").  첫 러너가 8 초 자는 동안 (7.5 초 안에 · 보이면 바로 끝) 'S1 정찰' 줄이 보여야 한다 · 프로세스가 아직 살아 있을 때.
        slow = td / 'runner_slow.sh'
        slow.write_text(f'#!/bin/bash\nsleep 8\nexec {sys.executable} -I {td / "fake.py"}\n', encoding='utf-8')
        logf = td / 't13.log'
        with open(logf, 'w', encoding='utf-8') as lf:
            pr = subprocess.Popen([sys.executable, '-I', str(Path(__file__).resolve()), '--stage', 'sbe', '--runner', str(slow), '--root', str(root),
                                   '--out', str(td / 'out_t13')], stdout=lf, stderr=subprocess.STDOUT)
        seen, t0 = False, time.time()
        try:
            while time.time() - t0 < 7.5 and pr.poll() is None:
                if 'S1 정찰' in logf.read_text(encoding='utf-8', errors='replace'):
                    seen = True
                    break
                time.sleep(0.1)
            alive = pr.poll() is None
        finally:
            pr.kill()
            pr.wait()
        chk('T13 화면을 파일로 돌려도 첫 런 도중 \'S1 정찰\' 줄이 이미 로그에 있다 (줄 버퍼 · 옛 판: 끝날 때까지 빈 로그)', seen and alive,
            (seen, alive, logf.read_text(encoding='utf-8', errors='replace')[:200]))
        # T11 등록 문서와 상수 대조 (있을 때만 — 리포 체크아웃)
        reg = HERE.parent / 'docs' / 'reviews' / 'sdcp_sigma_e_dcp_anchor_registration_v2_20261019.md'
        if reg.exists():
            t = reg.read_text(encoding='utf-8')
            need = [f'{TARGET_SBE_MS:.2f}', f'{EXP_DBE_MS:.2f}', *LADDER, *EXT_DOWN, *EXT_UP, '0.0041', '256.6']
            miss = [n for n in need if n not in t]
            chk(f'T11 등록 문서에 이 도구의 값 ({len(need)}) 이 다 있다', not miss, miss)
        else:
            chk('T11 등록 문서 없음 (리포 밖 실행) — 건너뜀', True)
    finally:
        shutil.rmtree(td, ignore_errors=True)
    print(f'\nsdcp_anchor_v2_chain selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 0 if not fail else 1


if __name__ == '__main__':
    sys.exit(main())
