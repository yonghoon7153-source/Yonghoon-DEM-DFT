#!/usr/bin/env python3
"""S2 검사 — **면적 cap 전환이 솔버의 `a_eff` 를 바꾸는가**.

정본 계약 = `docs/area_contract_20260913.md` (§2 · §4 의 S2) · 원장 = `AREA-12`.

★ 왜: 계약은 *"`A_surface`(상한 2πR_min²) 와 `A_transport`(상한 πR_min²) 로 쪼개면
  삭제됐던 협착 항이 되살아난다"* 를 전제했다.  그런데 솔버에는 **이미 clamp** 가 있다
  (`network_conductivity.py:395` `a_eff = min(a_contact, r_min_real)`).  clamp 는
  `a ≤ R_min` ⟺ `A ≤ πR_min²` 과 **같은 말**이다.  ⇒ 전환이 무엇을 바꾸는지 먼저 잰다.

★ **주장 (산술)** — 모든 입력에서 `a_eff` 가 같다:
      Lo   = max(A_hertz, A_ligg)                      (하한, `plastic_coverage.py:307`)
      A    = max(Lo, min(A_tabor, A_volume, 2πR²))     현행
      A'   = max(Lo, min(A_tabor, A_volume, 1πR²))     S2 전환
      a_eff = min(√(A/π), R)   ·   a'_eff = min(√(A'/π), R)
  `√(A/π) ≥ R  ⟺  A ≥ πR²` 이므로
   · `A' ≥ πR²` 이면 `a' = R`.  `A ≥ A' ≥ πR²` 이므로 `a = R`.  **같다.**
   · `A' < πR²` 이면 `Lo < πR²` 이고 `min(A_tabor, A_volume, πR²) < πR²` 라 그 min 은
     πR² 항이 아닌 데서 나온다 ⇒ `= min(A_tabor, A_volume)`.  그 값이 πR² 보다 작으니
     2πR² 보다도 작아 현행 min 과 같다 ⇒ `A' = A`.  **같다.**
  ⇒ **clamp 가 이미 수송 원판 상한을 강제하고 있다.**

⚠ **이것이 뜻하는 것**: S2 는 `network_conductivity` 의 σ 에 대해 **항등 변환**이다.
   *"협착 복원 → σ 하향"* 은 이 축에서 나오지 않는다.  ⛔ 그러나 **`A_physics` 자체는
   바뀐다** — coverage·반응면적·B3 가 그것을 읽으므로 **S2 는 표면 지표 쪽에서만** 효과가 있다
   (그리고 `AREA-03` 대로 그쪽은 **동결**해야 하므로, S2 는 결국 **아무 데도 안 남는다**).
⚠ **답하지 않는 것**: ψ 배치(`S3`) · flux-tube `b` · 이종쌍 σ 분할 — 전부 별개 축이다.

사용:
  python3 scripts/audit_transport_cap_equivalence.py            # 무작위 스윕
  python3 scripts/audit_transport_cap_equivalence.py --selftest
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import pathlib
import subprocess
import sys
import types

import numpy as np

SCRIPTS = pathlib.Path(__file__).resolve().parent
PC_SRC = SCRIPTS / 'plastic_coverage.py'

CAP_LINE = 'A_geom = 2.0 * np.pi * (r_min_eff ** 2)'
CAP_LINE_S2 = 'A_geom = 1.0 * np.pi * (r_min_eff ** 2)'


def _load(name: str, subs=()):
    """`plastic_coverage.py` 를 **격리 메모리에서** 로드한다 (필요하면 소스 치환).

    ⚠ 디스크의 생산 파일은 건드리지 않는다.
    """
    src = PC_SRC.read_text(encoding='utf-8')
    for old, new in subs:
        if src.count(old) != 1:
            raise SystemExit(f'치환 대상이 유일하지 않다 ({src.count(old)}건): {old!r}')
        src = src.replace(old, new, 1)
    mod = types.ModuleType(name)
    mod.__file__ = str(PC_SRC)
    exec(compile(src, str(PC_SRC), 'exec'), mod.__dict__)
    return mod


def a_eff_from(mod, delta, R_star, R_min, ligg_area):
    """생산 사슬 그대로: `A_physics` → `a = √(A/π)` → `a_eff = min(a, R_min)`.

    (`network_conductivity.py:323` · `:386` · `:395`)
    """
    A, _regime, _comp = mod.film_area_from_overlap(
        delta, R_star, R_min=R_min, ligg_area=ligg_area,
        mode='physics', return_components=True)
    a = math.sqrt(A / math.pi) if A > 0 else 0.0
    return A, min(a, R_min)


def sample(n, seed=0):
    """무작위 접촉 (µm 단위 아님 — `film_area_from_overlap` 은 단위 무관 스케일)."""
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        r1 = float(10.0 ** rng.uniform(-0.6, 0.9))      # 0.25 ~ 8
        r2 = float(10.0 ** rng.uniform(-0.6, 0.9))
        R_star = r1 * r2 / (r1 + r2)
        R_min = min(r1, r2)
        # δ/R* 를 탄성·전이·소성 전 구간에 걸쳐 뿌린다 (0 과 음수도 넣는다)
        dr = float(10.0 ** rng.uniform(-4.0, 0.3))
        delta = dr * R_star
        # LIGGGHTS 면적: 없음 / 0 / 교차 원판 근처 / 과대
        pick = rng.integers(0, 4)
        if pick == 0:
            ligg = None
        elif pick == 1:
            ligg = 0.0
        elif pick == 2:
            ligg = float(math.pi * max(delta, 0.0) * (2 * R_min - max(delta, 0.0)) / 2.0)
        else:
            ligg = float(rng.uniform(0.5, 4.0) * math.pi * R_min ** 2)
        out.append((delta, R_star, R_min, ligg))
    return out


def run(n, seed, verbose=True):
    """스윕 1회 → `classify` 결과.  ⚠ **selftest 와 같은 판정기를 쓴다** — 두 경로가
    서로 다른 문턱을 쓰면 한쪽이 거짓 빨간불/초록을 낸다 (규율 ⑤)."""
    st = classify(n, seed)
    if verbose:
        print(f'접촉 {n}건 (seed {seed})')
        print(f'  A_physics 가 **바뀐** 접촉   : {st["n_A_diff"]} / {n} '
              f'({100.0 * st["n_A_diff"] / n:.2f} % · 최대 상대차 {st["dA_max"]:.6g})')
        print(f'  a_eff 비트 동일              : {st["n_same"]} / {n}')
        print(f'  a_eff 가 clamp 에서 ULP 차   : {st["n_ulp"]} (최대 {st["max_ulp"]:.3g} ULP)')
        print(f'  **설명 안 되는 a_eff 차이**  : {st["n_bad"]}')
        print(f'  ψ 분기가 갈린 접촉           : {st["n_psi_branch_diff"]}')
        if st['worst']:
            (d, Rs, Rm, lg), A0, A1, a0, a1 = st['worst']
            print(f'    최대 차 사례: δ={d:.6g} R*={Rs:.6g} R_min={Rm:.6g} ligg={lg}')
            print(f'          A {A0:.12g} → {A1:.12g} · a_eff {a0:.17g} → {a1:.17g}')
    return st


NC_SRC = SCRIPTS / 'network_conductivity.py'
PC_ONLY_ANCHOR = "from plastic_coverage import film_area_from_overlap"


def _load_nc(name: str, pc_mod, nc_subs=()):
    """`network_conductivity.py` 를 격리 로드하되 그 안의 `_film_area` 를 **주어진 plastic 모듈**의
    함수로 바꿔 끼운다 → cap 을 바꾼 plastic 판을 실제 솔버에 물릴 수 있다.  (P2-R2-06: 감사가
    clamp/ψ 를 다시 구현하면 솔버 호출부의 변이를 못 본다 — 그래서 **솔버 자신**을 부른다.)"""
    src = NC_SRC.read_text(encoding='utf-8')
    for old_, new_ in nc_subs:
        if src.count(old_) != 1:
            raise SystemExit(f'솔버 치환 대상이 유일하지 않다 ({src.count(old_)}건): {old_!r}')
        src = src.replace(old_, new_, 1)
    mod = types.ModuleType(name)
    mod.__file__ = str(NC_SRC)
    sys.path.insert(0, str(SCRIPTS))
    exec(compile(src, str(NC_SRC), 'exec'), mod.__dict__)
    mod._film_area = pc_mod.film_area_from_overlap          # 솔버가 쓰는 이름
    return mod


#: 픽스처가 쓰는 상 라벨.  ⚠ **정본 `input_params` 규약과 같은 이름**이어야 한다 —
#: `sigma_AM_relative` 가 라벨 문자열로 분기하기 때문이다 (`AM_S` = 단결정 · `AM_P` = 다결정).
FIXTURE_TYPE_MAP = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}


def real_solver_edges(nc_mod, r1_um=0.5, r2_um=6.0, delta_um=0.2, native_um2=0.04, scale=1000.0,
                      psi_placement=None, t1=1, t2=3, mode='thermal'):
    """실제 `build_network` 한 쌍 — Codex 대조 조건 (r .5/6 µm · δ .2 µm · native A .04 µm²).

    `psi_placement=None` 이면 솔버의 **기본값**을 쓴다 (인자를 아예 넘기지 않는다 — 옛 판
    소스로도 이 함수가 돌아야 하므로).

    ★★ `t1·t2·mode` 신설 2026-09-15 (`AREA5-06`).  옛 판은 **열 채널 · `AM_P`–`SE` ·
      `r1 < r2`** 한 점뿐이라 두 축이 자유로웠다:
        · `r_min_real = min(r1, r2)` 를 `r1` 로 바꿔도 `r1` 이 늘 작은 쪽이라 **우연히 일치**
        · `sigma_rel_contact = min(σ₁, σ₂)` 를 `σ₁` 로 바꿔도 열 채널이라 둘 다 1.0
      ⇒ Codex 의 유해 변이 둘이 18/18 초록이었다 (내 재현: **기준을 안 옮겨도** 초록).
    """
    atoms = {1: {'type': t1, 'radius': r1_um / scale, 'x': 0.0, 'y': 0.0, 'z': 0.0},
             2: {'type': t2, 'radius': r2_um / scale, 'x': (r1_um + r2_um - delta_um) / scale, 'y': 0.0, 'z': 0.0}}
    rows = [{'id1': 1, 'id2': 2, 'contact_area': native_um2 / scale ** 2, 'delta': delta_um / scale}]
    kw = {} if psi_placement is None else {'psi_placement': psi_placement}
    n = nc_mod.build_network(atoms, rows, {t1, t2}, scale, 10.0, box_x=1e3, box_y=1e3,
                             mode=mode, type_map=dict(FIXTURE_TYPE_MAP), contact_mode='physics', **kw)
    return n['edges'] if isinstance(n, dict) else n[1]


def _psi(a_eff, r_min):
    """`network_conductivity.py:396` 과 같은 식."""
    return max(1.0 - a_eff / r_min, 0.0) ** 1.5


# ── S3 (`L2-01` ψ 배치) 보조 ────────────────────────────────────────────────────
#   픽스처는 `real_solver_edges` 기본과 같은 쌍이다 (r 0.5 / 6.0 µm · native A 0.04 µm²).
_FX_R1, _FX_R2, _FX_NATIVE = 0.5, 6.0, 0.04


def _a_from_delta(pc_mod, delta_um, r1=_FX_R1, r2=_FX_R2, native=_FX_NATIVE):
    """그 픽스처에서 `a_contact = √(A_physics/π)` (clamp **전**) — µm.

    ⚠ 기본 인자는 옛 픽스처 그대로다 (기존 호출부의 값이 바뀌지 않는다).
    """
    R_star = r1 * r2 / (r1 + r2)
    A, a_eff = a_eff_from(pc_mod, delta_um, R_star, R_min=min(r1, r2), ligg_area=native)
    return math.sqrt(A / math.pi) if A > 0 else 0.0


# ══ 동결 격자 + 고정 기준 (`AREA5-05`) ═════════════════════════════════════════
#   ⛔⛔ **기준을 `HEAD` 로 삼지 않는다.**  옛 ⑦f 는 working source 를
#   `git show HEAD:scripts/network_conductivity.py` 와 댔는데 — **커밋하면 둘이 같아진다.**
#   기준이 함께 이동하므로 커밋 뒤의 ⑦f 는 *"도입 전과 같다"* 를 고정하지 못한다.
#   ⇒ 깃발 도입 **직전 커밋**을 못박고, 그 소스의 **내용 SHA256** 까지 확인한다
#     (커밋 해시는 rebase 로 움직일 수 있지만 내용 해시는 안 움직인다).
PREFLAG_NC_COMMIT = '2d9ce3e87'
PREFLAG_NC_SHA256 = 'a2e73718bc0e6e9e659c30402ec49b35c196b3d1e701cb2155fee6713426c047'
#: 그 소스로 만든 **봉인된 기대값**.  얕은 클론·git 밖에서도 기준이 있어야 하므로 커밋한다.
BASELINE_PATH = SCRIPTS.parent / 'docs' / 'data' / 's3_preflag_baseline.json'
#: 그 파일 자신의 지문 — ⛔ 파일을 고치면 **여기도 고쳐야** 하고 그것은 리뷰에 보인다.
BASELINE_SHA256 = '495d65d0bb49b389b0bb1aa8c9d58961019b1b82afb1667fb7ba202796bad1e3'

#: 봉인·대조하는 필드.  ⚠ **전부 0 을 비교하면 공허하다** — 호출부가 `n_nonzero_rc` 를 요구한다.
BASELINE_FIELDS = ('R_constriction', 'R_bulk', 'R_total', 'R_Maxwell', 'R_film',
                   'A_contact', 'A_physics', 'A_hertzian', 'd_ij', 'regime')

#: ★★ 동결해야 하는 축을 **전부** 건드리는 격자 (`AREA5-05` 처방: *"동결 재료·분기·상 조합을
#:   포함한다"*).  채널 3 × 상쌍 8 × 반지름 순서 4 × δ 8 = 768 픽스처.
#:   ⛔ `(3, 1)`·`(2, 1)` 처럼 **순서를 뒤집은 쌍**과 `(6.0, 0.5)` 처럼 **큰 쪽이 먼저**인
#:     반지름이 들어 있는 것이 핵심이다 — 그것이 없으면 `min` 을 `첫째` 로 바꿔도 안 걸린다.
FROZEN_MODES = ('ionic', 'electronic', 'thermal')
FROZEN_PAIRS = ((1, 3), (3, 1), (2, 3), (3, 2), (1, 2), (2, 1), (3, 3), (1, 1))
FROZEN_RADII = ((0.5, 6.0), (6.0, 0.5), (1.0, 1.0), (2.0, 0.5))
FROZEN_DELTAS = (0.002, 0.01, 0.02, 0.05, 0.1, 0.1025, 0.2, 0.8)


def _frozen_key(mode, t1, t2, r1, r2, d) -> str:
    return f'{mode}|{t1}-{t2}|{r1!r}/{r2!r}|{d!r}'


def _frozen_matrix(nc_mod):
    """동결 격자 위의 **기본값 경로** 관측 → `{키: {필드: 값}}`.

    ⚠ `psi_placement` 를 **넘기지 않는다** — 기본값(legacy) 경로를 재는 것이 목적이고,
      깃발이 없던 옛 소스로도 같은 함수가 돌아야 한다.
    """
    out = {}
    for mode in FROZEN_MODES:
        for (t1, t2) in FROZEN_PAIRS:
            for (r1, r2) in FROZEN_RADII:
                for d in FROZEN_DELTAS:
                    e = real_solver_edges(nc_mod, r1_um=r1, r2_um=r2, delta_um=d,
                                          t1=t1, t2=t2, mode=mode)[0]
                    out[_frozen_key(mode, t1, t2, r1, r2, d)] = {
                        k: e.get(k) for k in BASELINE_FIELDS}
    return out


def _preflag_source():
    """도입 전 소스를 **고정 지문**으로 가져온다 → `(bytes, 출처)` 또는 `(None, 사유)`."""
    try:
        r = subprocess.run(['git', 'show', f'{PREFLAG_NC_COMMIT}:scripts/network_conductivity.py'],
                           cwd=str(SCRIPTS.parent), capture_output=True, check=True, timeout=120)
    except Exception as e:                                          # noqa: BLE001
        return None, f'git 으로 {PREFLAG_NC_COMMIT} 를 못 읽었다 ({type(e).__name__})'
    if not r.stdout.strip():
        return None, f'{PREFLAG_NC_COMMIT} 의 소스가 비었다'
    got = hashlib.sha256(r.stdout).hexdigest()
    if got != PREFLAG_NC_SHA256:
        return None, (f'도입 전 소스의 지문이 다르다 — 못박은 {PREFLAG_NC_SHA256[:12]} '
                      f'≠ 실제 {got[:12]}')
    return r.stdout, f'git:{PREFLAG_NC_COMMIT}'


def _exec_nc(src_text: str, name: str, pc_mod):
    mod = types.ModuleType(name)
    mod.__file__ = str(NC_SRC)
    sys.path.insert(0, str(SCRIPTS))
    exec(compile(src_text, str(NC_SRC), 'exec'), mod.__dict__)
    mod._film_area = pc_mod.film_area_from_overlap
    return mod


def _load_baseline():
    """봉인된 기대값 → `(matrix, 메타)` 또는 `(None, 사유)`.  ⛔ 못 읽으면 **실패**다."""
    if not BASELINE_PATH.is_file():
        return None, f'봉인 기준 파일이 없다: {BASELINE_PATH}'
    raw = BASELINE_PATH.read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    if got != BASELINE_SHA256:
        return None, (f'봉인 기준 파일의 지문이 다르다 — 못박은 {BASELINE_SHA256[:12]} '
                      f'≠ 실제 {got[:12]} (기준을 고쳤으면 소스의 핀도 같이 고쳐야 한다)')
    try:
        doc = json.loads(raw.decode('utf-8'))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        return None, f'봉인 기준을 JSON 으로 못 읽는다: {e}'
    if doc.get('preflag_commit') != PREFLAG_NC_COMMIT or \
            doc.get('preflag_sha256') != PREFLAG_NC_SHA256:
        return None, ('봉인 기준이 가리키는 도입 전 소스가 이 감사기의 핀과 다르다 — '
                      f"파일 {doc.get('preflag_commit')}/{str(doc.get('preflag_sha256'))[:12]}")
    return doc.get('matrix') or {}, doc


def _bitwise_vs_baseline(pc_mod):
    """기본값(legacy)이 **도입 전 소스**와 비트 동일한지 — 동결 격자 전체에서.

    세 갈래로 답한다:
      · `n_bad`      봉인된 기대값과 다른 (키, 필드) 수
      · `n_cross`    고정 커밋에서 **재생성**한 값이 봉인과 다른 수 (기준 자체의 위조 검사)
      · `cross_src`  그 교차검증이 실제로 돌았는지 (`''` 면 git 을 못 읽었다)
    ⛔ 봉인 기준을 못 읽으면 `n_cmp = 0` 을 돌려주고 호출부가 **실패**시킨다.
    """
    exp, meta = _load_baseline()
    if exp is None:
        return dict(n_cmp=0, n_bad=0, worst=0.0, n_nonzero_rc=0, n_cross=0,
                    cross_src='', why=meta)
    cur = _frozen_matrix(_load_nc('_nc_cur_bit', pc_mod))
    n_cmp = n_bad = n_nonzero_rc = 0
    worst = 0.0
    missing = sorted(set(exp) ^ set(cur))
    for key, want in exp.items():
        got = cur.get(key) or {}
        if (want.get('R_constriction') or 0) > 0:
            n_nonzero_rc += 1
        for k in BASELINE_FIELDS:
            n_cmp += 1
            va, vb = want.get(k), got.get(k)
            if va == vb:
                continue
            n_bad += 1
            try:
                worst = max(worst, abs(float(va) - float(vb)))
            except (TypeError, ValueError):
                worst = float('inf')
    #  ── 교차검증: 고정 커밋을 읽을 수 있으면 **거기서 재생성**해 봉인과 비트 대조한다.
    #     이것이 "봉인 파일만 고쳐서 초록을 만드는" 길을 막는다 (CI 는 fetch-depth: 0).
    src, why = _preflag_source()
    n_cross, cross_src = 0, ''
    if src is not None:
        regen = _frozen_matrix(_exec_nc(src.decode('utf-8'), '_nc_preflag', pc_mod))
        cross_src = why
        for key, want in exp.items():
            g = regen.get(key) or {}
            n_cross += sum(1 for k in BASELINE_FIELDS if want.get(k) != g.get(k))
        n_cross += len(set(exp) ^ set(regen))
    return dict(n_cmp=n_cmp, n_bad=n_bad + len(missing), worst=worst,
                n_nonzero_rc=n_nonzero_rc, n_cross=n_cross, cross_src=cross_src,
                why=('' if src is not None else why))


def emit_baseline() -> int:
    """고정 커밋의 소스로 봉인 기준 파일을 만든다 (`--emit-baseline`).

    ⛔ 생산 경로가 아니다 — 기준을 **다시 만드는** 유일한 길이고, 만들고 나면 출력된 지문을
      `BASELINE_SHA256` 에 손으로 박아야 한다 (그 편집이 리뷰에 보인다).
    """
    src, why = _preflag_source()
    if src is None:
        print(f'⛔ 도입 전 소스를 확정할 수 없다 — {why}')
        return 2
    pc = _load('_pc_emit')
    mod = _exec_nc(src.decode('utf-8'), '_nc_emit', pc)
    doc = {'what': 'S3 ψ 배치 깃발 **도입 전** 솔버의 동결 격자 관측 (AREA5-05 기준)',
           'preflag_commit': PREFLAG_NC_COMMIT, 'preflag_sha256': PREFLAG_NC_SHA256,
           'fields': list(BASELINE_FIELDS),
           'axes': {'modes': list(FROZEN_MODES), 'type_pairs': [list(p) for p in FROZEN_PAIRS],
                    'radii_um': [list(r) for r in FROZEN_RADII], 'deltas_um': list(FROZEN_DELTAS),
                    'type_map': {str(k): v for k, v in FIXTURE_TYPE_MAP.items()}},
           'matrix': _frozen_matrix(mod)}
    blob = json.dumps(doc, ensure_ascii=False, indent=1, sort_keys=True).encode('utf-8')
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    BASELINE_PATH.write_bytes(blob)
    print(f'→ {BASELINE_PATH}  ({len(doc["matrix"])} 픽스처 × {len(BASELINE_FIELDS)} 필드)')
    print(f'   BASELINE_SHA256 = {hashlib.sha256(blob).hexdigest()!r}')
    return 0


def _psi_sweep(nc_mod):
    """δ 를 키우며 두 배치의 `R_constriction` 을 나란히 — `L2-01` 의 비단조·절벽 재현.

    ⚠ *"접촉을 키운다"* 를 δ 로 대리한다 — 이 픽스처에서 `a_contact` 는 δ 에 단조 증가다
      (`⑦g` 의 전제이므로 같은 함수가 그것도 확인한다).
    """
    ds = [0.002 * (1.06 ** i) for i in range(80)]          # 0.002 → ~0.2
    div, mul, a_prev = [], [], -1.0
    div_last_pos = mul_last_pos = 0.0
    mono_a = True
    for d in ds:
        a = _a_from_delta(_PC_SWEEP[0], d)
        if a < a_prev:
            mono_a = False
        a_prev = a
        ro = real_solver_edges(nc_mod, delta_um=d, psi_placement=nc_mod.PSI_DIVIDE)[0]['R_constriction']
        rn = real_solver_edges(nc_mod, delta_um=d, psi_placement=nc_mod.PSI_MULTIPLY)[0]['R_constriction']
        div.append(ro)
        mul.append(rn)
        if ro > 0:
            div_last_pos = ro
        if rn > 0:
            mul_last_pos = rn
    return dict(div=div, mul=mul, div_last_pos=div_last_pos, mul_last_pos=mul_last_pos,
                a_monotone=mono_a)


#: `_psi_sweep` 이 쓰는 plastic 모듈 (호출부가 채운다 — 감사가 면적을 재구현하지 않게).
_PC_SWEEP = [None]

#: oracle 이 못박는 두 상수.  ⛔ 계약 §C·§⑥ 이 **동결**한 값이다 — 여기를 바꿔서 초록을
#: 만들면 그 순간 이 검사가 무의미해진다 (`R4-08` 이 정확히 그 부류를 보고했다).
PSI_EXPONENT_ORACLE = 1.5
PSI_FLOOR_ORACLE = 1e-4


#: ⛔⛔ **동결된 재료 상수** — 솔버에서 import 하지 **않는다**.  import 하면 상수 변이가
#:   기대값과 **같이 움직여** 통과한다 (`R4-08` 이 ψ 축에서 보고한 바로 그 부류).
#:   출처는 솔버 본문과 같다: `K_AM 4 W/m·K` (NCM) · `K_SE 0.7` (LPSCl, Ketter 2025) ·
#:   `r0 = 2 µm` · GB 지수 `β = 1.5` (코퍼스 적합, Trevisanello 방향).
MAT_ORACLE = {'NCM_AM_REF_R': 2.0, 'NCM_AM_GB_EXPONENT': 1.5,
              'K_AM_THERMAL': 4.0e-2, 'K_SE_THERMAL': 0.7e-2}


def _mat_oracle(mode, lbl1, lbl2, r1, r2):
    """`(k_weight, σ_rel_1, σ_rel_2)` 를 **독립 계산** — `AREA5-06` 의 "계수 동결" 축.

    ★ 왜 별도인가: Codex 가 열 AM–SE 조화평균을 `1` 로 바꿔도 ψ oracle 이
      `bad_div = bad_mul = bad_floor = 0` 임을 보였다 ⇒ **ψ 배치가 맞는 것과 재료계수가
      맞는 것은 다른 주장**이고, 전자를 못박아도 후자는 자유롭게 남는다.
    ⚠ 전자 판정 게이트까지 그대로 옮긴다 — 솔버는 `mode == 'electronic'` **또는**
      "타깃이 전부 AM 이고 SE 가 없다" 일 때 GB 보정을 건다 (`mode` 인자를 못 믿기 때문).
    """
    kr = MAT_ORACLE['K_AM_THERMAL'] / MAT_ORACLE['K_SE_THERMAL']
    se1, se2 = lbl1 == 'SE', lbl2 == 'SE'
    if mode == 'thermal':
        k_w = kr if (not se1 and not se2) else (1.0 if (se1 and se2) else 2 * kr / (1 + kr))
    else:
        k_w = 1.0
    targets = {lbl1, lbl2}
    electronic = (mode == 'electronic') or (all('AM' in t for t in targets) and 'SE' not in targets)

    def srel(r, lbl):
        if not electronic or lbl != 'AM_P':
            return 1.0
        return 1.0 / (1.0 + (max(r, 0.1) / MAT_ORACLE['NCM_AM_REF_R'])
                      ** MAT_ORACLE['NCM_AM_GB_EXPONENT'])

    return k_w, srel(r1, lbl1), srel(r2, lbl2)


def _material_oracle(nc_mod):
    """★★ `AREA5-06` — 재료계수 primitive 를 **동결 격자 전체**에서 못박는다.

    간선이 이미 돌려주는 `A_contact · d_ij · r1 · r2` 로부터
        `R_Maxwell = 1/(min(σ₁,σ₂)·k·2·a_contact)`     ← `min` 규약 + `k_weight`
        `R_bulk    = (d/2)/(σ₁·k·π r₁²) + (d/2)/(σ₂·k·π r₂²)`  ← **면별** σ 배정
    을 각각 확인한다.  두 식이 `min(σ)→σ₁` 과 `조화평균→1` 을 동시에 잡는다.
    ⚠ 면적은 재구현하지 않는다 (간선의 `A_contact` 를 쓴다) — 이 파일의 오래된 교훈이다.
    """
    n = bad_max = bad_bulk = 0
    for mode in FROZEN_MODES:
        for (t1, t2) in FROZEN_PAIRS:
            for (r1, r2) in FROZEN_RADII:
                for d in (0.002, 0.02, 0.1, 0.2):
                    e = real_solver_edges(nc_mod, r1_um=r1, r2_um=r2, delta_um=d,
                                          t1=t1, t2=t2, mode=mode)[0]
                    lbl1 = FIXTURE_TYPE_MAP[e['type1']]
                    lbl2 = FIXTURE_TYPE_MAP[e['type2']]
                    k_w, s1, s2 = _mat_oracle(mode, lbl1, lbl2, e['r1'], e['r2'])
                    a = math.sqrt(e['A_contact'] / math.pi) if e['A_contact'] > 0 else 0.0
                    if a <= 0:
                        continue
                    n += 1
                    want_rm = 1.0 / (min(s1, s2) * k_w * 2 * a)
                    if abs(e['R_Maxwell'] - want_rm) > 1e-12 * abs(want_rm):
                        bad_max += 1
                    want_rb = ((e['d_ij'] / 2) / (s1 * k_w * math.pi * e['r1'] ** 2)
                               + (e['d_ij'] / 2) / (s2 * k_w * math.pi * e['r2'] ** 2))
                    if abs(e['R_bulk'] - want_rb) > 1e-12 * abs(want_rb):
                        bad_bulk += 1
    return dict(n=n, bad_maxwell=bad_max, bad_bulk=bad_bulk)


def _psi_oracle(nc_mod, pc_mod):
    """★★ `R4-08` — ψ 를 **기하에서 독립 계산**해 두 배치의 식을 각각 못박는다.

    `R_Maxwell = 1/(σ·k·2·a_contact)` 는 솔버가 이미 돌려주므로 재료·채널 계수를 다시
    구현할 필요가 없다.  활성 간선에서는 clamp 가 안 걸려 `a_eff == a_contact` 이므로
        legacy : `Rc·ψ_oracle == R_Maxwell`
        곱셈   : `Rc == R_Maxwell·ψ_oracle`
    이고, 이 두 식은 **ψ 의 지수와 floor 를 같이 못박는다** — 솔버의 ψ 를 빌리지 않기 때문이다.

    ★★ **2026-09-15 (`AREA5-06`) — 격자를 상·채널·반지름 순서로 넓혔다.**  옛 판은
      `r1 = 0.5 < r2 = 6` 한 순서뿐이라 `r_min_real = min(r1, r2)` 를 `r1` 로 바꿔도
      **우연히 일치**해 통과했다.  이제 `(6.0, 0.5)` 와 같은 반지름을 같이 돌린다.
    """
    n = bad_div = bad_mul = bad_floor = 0
    for mode in FROZEN_MODES:
        for (t1, t2) in FROZEN_PAIRS:
            for (r1, r2) in FROZEN_RADII:
                r_min = min(r1, r2)
                for d in (0.002, 0.005, 0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.1025, 0.12, 0.2):
                    a = _a_from_delta(pc_mod, d, r1=r1, r2=r2)
                    a_eff = min(a, r_min)
                    psi_o = max(1.0 - a_eff / r_min, 0.0) ** PSI_EXPONENT_ORACLE
                    eo = real_solver_edges(nc_mod, r1_um=r1, r2_um=r2, delta_um=d, t1=t1, t2=t2,
                                           mode=mode, psi_placement=nc_mod.PSI_DIVIDE)[0]
                    en = real_solver_edges(nc_mod, r1_um=r1, r2_um=r2, delta_um=d, t1=t1, t2=t2,
                                           mode=mode, psi_placement=nc_mod.PSI_MULTIPLY)[0]
                    rm = eo.get('R_Maxwell')
                    ro, rn = eo.get('R_constriction') or 0.0, en.get('R_constriction') or 0.0
                    active = psi_o > PSI_FLOOR_ORACLE
                    #  ⓐ floor 판정 자체 — oracle 이 "활성" 이라 한 곳에서만 솔버가 양수를 낸다.
                    if active != (ro > 0.0) or active != (rn > 0.0):
                        bad_floor += 1
                        continue
                    if not active:
                        continue
                    n += 1
                    #  ⓑ 두 식.  `a_eff == a_contact` 를 쓰므로 clamp 간선은 활성이 아니다.
                    if rm is None or rm <= 0 or abs(ro * psi_o - rm) > 1e-12 * max(1.0, rm):
                        bad_div += 1
                    if rm is None or rm <= 0 or abs(rn - rm * psi_o) > 1e-12 * max(1.0, rm * psi_o):
                        bad_mul += 1
    return dict(n=n, bad_div=bad_div, bad_mul=bad_mul, bad_floor=bad_floor,
                exponent=PSI_EXPONENT_ORACLE, floor=PSI_FLOOR_ORACLE)


def _floor_cliff(nc_mod, pc_mod, r1=1.0, r2=1.0):
    """floor 절단면을 **실제 솔버로 이분**해 양쪽 배치의 좌극한을 잰다 (`AREA5-07`).

    ⛔⛔ **옛 ⑦h 의 이름이 거짓이었다.**  거기 적힌 *"곱셈은 그 자리가 연속이다"* 는 과장이다 —
      계약 §C 가 floor 를 **유한한 `1e-4`** 로 동결했으므로 곱셈판의 좌극한은
      `ψ_floor/(2·σ·k·a*) > 0` 이고 그 **다음 값이 0** 이다.  작은 불연속이 남는다.
    ★ 바른 문장: *"곱셈 배치는 legacy 의 큰 급락을 크게 줄이지만, 동결된 finite floor 때문에
      작은 불연속은 남는다.  floor 복원은 본 S3 와 분리한다."*
    """
    def rc(d, place):
        return real_solver_edges(nc_mod, r1_um=r1, r2_um=r2, delta_um=d,
                                 psi_placement=place)[0]['R_constriction']

    lo, hi = 1e-4, 1.0                   # lo: Rc>0 (겹침 얕음) · hi: Rc==0 (floor 아래)
    if not (rc(lo, nc_mod.PSI_MULTIPLY) > 0 and rc(hi, nc_mod.PSI_MULTIPLY) == 0):
        return None
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if mid <= lo or mid >= hi:
            break
        if rc(mid, nc_mod.PSI_MULTIPLY) > 0:
            lo = mid
        else:
            hi = mid
    e_lo = real_solver_edges(nc_mod, r1_um=r1, r2_um=r2, delta_um=lo,
                             psi_placement=nc_mod.PSI_MULTIPLY)[0]
    d_lo = real_solver_edges(nc_mod, r1_um=r1, r2_um=r2, delta_um=lo,
                             psi_placement=nc_mod.PSI_DIVIDE)[0]['R_constriction']
    a = _a_from_delta(pc_mod, lo, r1=r1, r2=r2)
    psi_star = max(1.0 - min(a, min(r1, r2)) / min(r1, r2), 0.0) ** PSI_EXPONENT_ORACLE
    return dict(delta_last_pos=lo, delta_first_zero=hi, psi_star=psi_star,
                mul_left=e_lo['R_constriction'], div_left=d_lo,
                R_Maxwell=e_lo['R_Maxwell'],
                mul_next=rc(hi, nc_mod.PSI_MULTIPLY), div_next=rc(hi, nc_mod.PSI_DIVIDE))


def classify(n, seed):
    """`a_eff` 차이를 **비트 동일 / clamp ULP / 설명 안 됨** 으로 가른다.

    ⚠ 느슨한 허용오차 대신 이렇게 가르는 이유: 허용오차는 **무엇이 달랐는지**를 숨긴다.
    """
    base = _load('_pc_c_base')
    s2 = _load('_pc_c_s2', [(CAP_LINE, CAP_LINE_S2)])
    st = dict(n_same=0, n_ulp=0, n_bad=0, max_ulp=0.0, n_A_diff=0,
              dA_max=0.0, da_max=0.0, n_psi_branch_diff=0, worst=None)
    for c in sample(n, seed):
        _delta, _Rs, R_min, _lg = c
        A0, a0 = a_eff_from(base, *c)
        A1, a1 = a_eff_from(s2, *c)
        dA = abs(A1 - A0) / max(A0, 1e-300)
        if dA > 1e-15:
            st['n_A_diff'] += 1
        st['dA_max'] = max(st['dA_max'], dA)
        da = abs(a1 - a0) / max(a0, 1e-300)
        if da > st['da_max']:
            st['da_max'], st['worst'] = da, (c, A0, A1, a0, a1)
        if a0 == a1:
            st['n_same'] += 1
        else:
            u = max(abs(a0 - R_min), abs(a1 - R_min)) / math.ulp(R_min)
            st['max_ulp'] = max(st['max_ulp'], u)
            if u <= 2.0:
                st['n_ulp'] += 1
            else:
                st['n_bad'] += 1
        # ψ 분기 (≤ 1e-4 이면 R_c = 0) 가 갈리는가
        if (_psi(a0, R_min) > 1e-4) != (_psi(a1, R_min) > 1e-4):
            st['n_psi_branch_diff'] += 1
    return st


def _selftest() -> int:
    ok = True

    def chk(name, cond, extra=''):
        nonlocal ok
        print(('  ✓ ' if cond else '  ✗ ') + name + (f'   {extra}' if extra else ''))
        ok = ok and bool(cond)

    print('수송 cap 동치 (S2 전제 검사)')

    # ① 본 주장 — a_eff 는 안 바뀐다.
    #    ⚠ **비트 동일을 요구하지 않는다** — `√(πR²/π)` 가 `R` 과 1 ULP 어긋날 수 있다.
    #      느슨한 허용오차로 초록을 만드는 대신 **더 구체적인 주장**을 검사한다:
    #      다른 건은 전부 **양쪽 다 clamp 값(R_min) 에서 2 ULP 이내** 여야 한다.
    st = classify(4000, 0)
    chk('① S2 전환에서 `a_eff` 가 바뀌지 않는다 (비트 동일 · 또는 양쪽 다 clamp 2 ULP 이내)',
        st['n_bad'] == 0,
        f'비트 동일 {st["n_same"]} · clamp ULP 차 {st["n_ulp"]} (최대 {st["max_ulp"]:.3g} ULP) · '
        f'설명 안 되는 차이 {st["n_bad"]}')

    # ①b 그 1 ULP 가 **하류에서 같은 분기로 간다** (ψ ≤ 1e-4 → R_c = 0)
    chk('①b 그 ULP 차는 ψ 분기를 안 바꾼다 (둘 다 ψ ≤ 1e-4)', st['n_psi_branch_diff'] == 0,
        f'분기가 갈린 접촉 {st["n_psi_branch_diff"]}건')
    dA, da, nA = st['dA_max'], st['da_max'], st['n_A_diff']

    # ② 검사가 공허하지 않다 — A 자체는 실제로 바뀌어야 한다
    chk('② 대조: `A_physics` 자체는 바뀐다 (검사가 공허하지 않다)', nA > 0 and dA > 0.1,
        f'{nA}건 · 최대 {dA:.4g}')

    # ③ 판별력 — clamp 를 없애면 `a_eff` 가 **반드시** 달라진다
    base = _load('_pc_b3')
    s2 = _load('_pc_s3', [(CAP_LINE, CAP_LINE_S2)])
    diff = 0
    for c in sample(4000, 0):
        A0, _ = a_eff_from(base, *c)
        A1, _ = a_eff_from(s2, *c)
        # clamp 없는 세계: a = √(A/π) 그대로
        if abs(math.sqrt(A1 / math.pi) - math.sqrt(A0 / math.pi)) > 1e-15 * max(
                math.sqrt(A0 / math.pi), 1e-300):
            diff += 1
    chk('③ 판별력: clamp 를 빼면 `a` 가 달라진다 (동치는 clamp 덕분이다)', diff > 0,
        f'{diff}/4000 건이 달라진다')

    # ④ 다른 seed 에서도 같다
    st2 = classify(4000, 12345)
    chk('④ 다른 seed 에서도 같은 결론', st2['n_bad'] == 0 and st2['n_psi_branch_diff'] == 0,
        f'비트 동일 {st2["n_same"]} · clamp ULP {st2["n_ulp"]} · 설명 안 됨 {st2["n_bad"]}')

    # ⑤ 손으로 짚은 경계 — geom 결속이 되는 깊은 겹침
    r = 1.0
    c = (0.5 * r, r / 2.0, r, None)          # δ/R* = 1.0, 깊게
    A0, a0 = a_eff_from(base, *c)
    A1, a1 = a_eff_from(s2, *c)
    chk('⑤ geom 결속 경계: A 는 2πR²→πR² 로 절반, `a_eff` 는 R 로 동일',
        abs(A0 - 2 * math.pi * r * r) < 1e-12 and abs(A1 - math.pi * r * r) < 1e-12
        and a0 == a1 == r,
        f'A {A0:.10g} → {A1:.10g} · a_eff {a0:.10g} = {a1:.10g}')

    # ══ S3 대조 (R3-02, Codex 3라운드 §3.1 · 계약 §5-v4 C) ══════════════════════════
    #   등록된 음성 대조 둘(coverage 셀 불변 · hertzian Rc bitwise 불변)은 **no-op 도 통과**한다.
    #   통과 자체가 결함은 아니지만 **전환을 안 해도 통과**하므로 전환을 잡지 못한다.
    #   ⇒ 실제 build_network 의 활성 간선에서 Rc_new/Rc_old = ψ² 를 요구하는 **양성 대조**를
    #     두고, **no-op 변이는 반드시 실패**하게 한다.  ⛔ "전 코호트 σ 가 반드시 달라야 한다"
    #     는 게이트는 만들지 않는다 (활성 간선이 없는 망에서는 무변화가 정상이다).
    #   ★★ **2026-09-15 — 전환이 소스 문자열 치환에서 `psi_placement` 깃발로 옮겨졌다.**
    #      왜: 치환판으로는 **실제 런을 돌릴 수 없다** (감사 프로세스 안에서만 존재한다).
    #      S3 는 코호트 130 × 3 채널을 두 팔로 돌려야 하므로 생산 솔버에 인자가 있어야 한다.
    #      ⛔ 기본값은 `legacy_divide` 로 **비트 동일**이다 (아래 ⑦f 가 고정한다).
    S3_MUL = ('                    R_constriction = psi / '
              '(sigma_rel_contact * k_weight * 2 * a_eff)')
    S3_DIV = ('                    R_constriction = 1.0 / '
              '(sigma_rel_contact * k_weight * 2 * a_eff * psi)')
    #   ⚠ 기본 픽스처(δ .2 µm)는 **floor 아래**라 Rc = 0 이다 — 양성 대조는 활성 분기가
    #     필요하므로 겹침을 줄여 ψ > 1e-4 인 쌍을 쓴다 (δ .02 µm, 실측으로 고른 값).
    _pc = _load('_pc_s3')
    _PC_SWEEP[0] = _pc          # 스윕이 면적을 재구현하지 않고 이 모듈을 쓴다
    #   세 좌표: 활성(ψ>1e-4) · floor_only(s<1 인데 ψ≤1e-4) · clamp_zero(s_raw≥1 ⇒ ψ=0).
    #   ⚠ floor_only 띠는 **0.102338~0.102633 뿐**이다 (R2-08 실측) — 이 값을 넓히지 말 것.
    _D_ACT, _D_FLOOR_ONLY, _D_CLAMP = 0.02, 0.1025, 0.2
    _nc = _load_nc('_nc_s3_flag', _pc)
    e_old = real_solver_edges(_nc, delta_um=_D_ACT, psi_placement=_nc.PSI_DIVIDE)[0]
    e_s3 = real_solver_edges(_nc, delta_um=_D_ACT, psi_placement=_nc.PSI_MULTIPLY)[0]
    #   no-op 변이 = 곱셈 가지를 **legacy 식으로 되돌린다** ⇒ 깃발을 켜도 아무 일이 없다.
    #   음성 대조(coverage 셀 · hertzian bitwise)는 이것을 **통과시킨다** — 그래서 이 대조가 있다.
    _nc_nop = _load_nc('_nc_s3_nop', _pc, [(S3_MUL, S3_DIV)])
    e_nop = real_solver_edges(_nc_nop, delta_um=_D_ACT, psi_placement=_nc_nop.PSI_MULTIPLY)[0]
    #   ⚠ ψ 를 감사가 **다시 구현하면 안 된다** (이 파일 §_load_nc 의 교훈).  그렇다고 비의
    #     제곱근으로 읽으면 `ratio == sqrt(ratio)²` 라는 **항등식**이 되어 판별력이 0 이다.
    #     ⇒ 세 번째 변이로 **솔버가 ψ 를 직접 돌려주게** 해서 그 값과 비교한다.
    S3_PSI = '                    R_constriction = psi'
    _nc_psi = _load_nc('_nc_s3_psi', _pc, [(S3_MUL, S3_PSI)])
    psi_probe = real_solver_edges(_nc_psi, delta_um=_D_ACT,
                                 psi_placement=_nc_psi.PSI_MULTIPLY)[0]['R_constriction']
    ratio = e_s3['R_constriction'] / e_old['R_constriction']
    chk('⑦ ★ S3 양성 대조: 실제 build_network 에서 Rc_new/Rc_old = ψ² (ψ 는 솔버가 돌려준 값)',
        e_old['R_constriction'] > 0 and 0.0 < psi_probe < 1.0
        and abs(ratio - psi_probe ** 2) < 1e-12,
        f'비 = {ratio!r} · ψ(솔버) = {psi_probe!r} · ψ² = {psi_probe ** 2!r}')
    nop_ratio = e_nop['R_constriction'] / e_old['R_constriction']
    chk('⑦b ★ no-op 변이는 이 대조에서 **반드시 실패**한다 (음성 대조만으로는 못 잡던 자리)',
        nop_ratio == 1.0 and abs(nop_ratio - psi_probe ** 2) > 1e-6,
        f'no-op 비 = {nop_ratio!r} ≠ ψ² {psi_probe ** 2!r}')
    chk('⑦c σ 는 비감소 — 활성 분기에서 Rc_new ≤ Rc_old 이므로 R_total 이 안 늘어난다',
        e_s3['R_total'] <= e_old['R_total'],
        f"R_total {e_old['R_total']!r} → {e_s3['R_total']!r}")
    #   floor 아래(ψ ≤ 1e-4)는 **0 → 0** 이다 — floor 복원은 이 시험이 아니다 (R3-02).
    _fo_old = real_solver_edges(_nc, delta_um=_D_FLOOR_ONLY, psi_placement=_nc.PSI_DIVIDE)[0]
    _fo_s3 = real_solver_edges(_nc, delta_um=_D_FLOOR_ONLY, psi_placement=_nc.PSI_MULTIPLY)[0]
    chk('⑦d floor 아래(floor_only, s<1)는 전환해도 0 → 0 (복원은 별도 축)',
        _fo_old['R_constriction'] == 0.0 and _fo_s3['R_constriction'] == 0.0,
        f"{_fo_old['R_constriction']!r} / {_fo_s3['R_constriction']!r}")
    #   ★★ 계약 §C 가 등록한 **세 번째 핀 = clamp 경계** (2026-09-15 에 추가).  등록은
    #      *"floor 위·아래·clamp 경계를 각각 핀한다"* 인데 위 둘만 있었다.
    #      clamp 경계 = `a_contact ≥ r_min` ⇒ `a_eff = r_min` **정확히** ⇒ `ψ = 0`.
    #      ⇒ **양쪽 배치 모두 0** 이고 S3 는 여기서 항등이다.
    #      ★ 이것이 크기를 말한다 — 삭제 973,137 중 **99.436 %가 clamp_zero** (R2-08) 이므로
    #        S3 는 "협착이 삭제된 접촉" 의 거의 전부를 **건드리지 않는다**.  그 접촉들의 참값은
    #        `A` 의 정의(`AREA-03`/`AREA-09` STEP 2)가 정해져야 나온다.
    _cz_old = real_solver_edges(_nc, delta_um=_D_CLAMP, psi_placement=_nc.PSI_DIVIDE)[0]
    _cz_s3 = real_solver_edges(_nc, delta_um=_D_CLAMP, psi_placement=_nc.PSI_MULTIPLY)[0]
    _a_eff_cz = min(_a_from_delta(_pc, _D_CLAMP), 0.5)
    chk('⑦e ★ clamp 경계(clamp_zero, s_raw≥1 ⇒ ψ=0): 양쪽 다 0 — S3 는 삭제분의 99.436 % 를 안 건드린다',
        _cz_old['R_constriction'] == 0.0 and _cz_s3['R_constriction'] == 0.0
        and _a_eff_cz == 0.5,
        f"Rc {_cz_old['R_constriction']!r} / {_cz_s3['R_constriction']!r} · a_eff = r_min = {_a_eff_cz!r}")
    #   ★ ⑦f — **기본값이 도입 전 코드와 비트 동일**하다.  깃발을 넣은 것이 세대 1 의 σ 를
    #     조용히 움직였다면 봉인 전에 이미 오염된 것이다.
    #     ⛔⛔ **기준을 `HEAD` 에서 고정 커밋으로 옮겼다** (`AREA5-05`, 2026-09-15).  옛 판은
    #       working 을 `git show HEAD:` 와 댔는데 **커밋하면 둘이 같아진다** = 기준이 함께
    #       이동한다.  이제 깃발 도입 **직전 커밋**(내용 SHA256 까지 확인)과 그것으로 만든
    #       **봉인된 기대값 파일**을 기준으로 삼고, 기준을 못 읽으면 **실패**한다.
    _bl = _bitwise_vs_baseline(_pc)
    chk('⑦f ★ 기본값(legacy_divide)은 **도입 전 고정 SHA** 와 비트 동일 — 기준이 HEAD 와 함께 '
        '움직이지 않는다 (AREA5-05)',
        _bl['n_bad'] == 0 and _bl['n_cmp'] >= 5000 and _bl['n_nonzero_rc'] >= 20
        and _bl['n_cross'] == 0 and _bl['cross_src'] != '',
        f"대조 (픽스처×필드) {_bl['n_cmp']} · Rc>0 픽스처 {_bl['n_nonzero_rc']} · 다른 것 "
        f"{_bl['n_bad']} · 최대차 {_bl['worst']!r} · 고정커밋 재생성 대조 {_bl['cross_src'] or '못함'}"
        f" (어긋남 {_bl['n_cross']}) {_bl['why']}")
    #   ★ ⑦g — `L2-01` 이 보고한 **비단조·절벽**을 생산 코드에서 재현하고, 곱셈 배치가
    #     둘 다 없앤다는 것을 같은 스윕에서 보인다 (규율 ②: 재현 먼저, 그 다음 수리).
    _sw = _psi_sweep(_nc)
    _legacy_nonmono = any(_sw['div'][i + 1] > _sw['div'][i] > 0 for i in range(len(_sw['div']) - 1))
    _mul_mono = all(_sw['mul'][i + 1] <= _sw['mul'][i] for i in range(len(_sw['mul']) - 1))
    chk('⑦g ★ 재현: legacy 는 접촉을 키우는데 저항이 **오르는** 구간이 있고(비단조) 곱셈은 단조 비증가',
        _legacy_nonmono and _mul_mono and _sw['a_monotone'],
        f"legacy 최대 {max(_sw['div'])!r} (비단조 {_legacy_nonmono}) · 곱셈 단조 {_mul_mono} "
        f"· 전제 a(δ) 단조 {_sw['a_monotone']}")
    #   ★★ ⑦h — **이름과 단언을 사실에 맞춘다** (`AREA5-07`, 2026-09-15).  옛 이름은
    #      *"곱셈은 그 자리가 연속이다"* 였는데 **거짓**이다: 계약 §C 가 floor 를 유한한
    #      `1e-4` 로 동결했으므로 곱셈판의 좌극한은 `ψ_floor·R_Maxwell > 0` 이고 다음이 0 이다.
    #      ⇒ 이제 절단면을 **이분으로 찾아** 좌극한을 실제로 재고, 그 값이 이론값과 같은지와
    #        legacy 대비 비가 `1/ψ*²` 인지를 단언한다.  ⛔ floor 를 바꾸라는 뜻이 아니다.
    _cl = _floor_cliff(_nc, _pc)
    _cl_ok = bool(_cl) and (
        _cl['mul_left'] > 0.0 and _cl['div_left'] > 0.0
        and _cl['mul_next'] == 0.0 and _cl['div_next'] == 0.0
        and PSI_FLOOR_ORACLE < _cl['psi_star'] < 1.05 * PSI_FLOOR_ORACLE
        and abs(_cl['mul_left'] - _cl['R_Maxwell'] * _cl['psi_star'])
        <= 1e-9 * _cl['R_Maxwell'] * _cl['psi_star']
        and abs(_cl['div_left'] / _cl['mul_left'] - 1.0 / _cl['psi_star'] ** 2)
        <= 1e-6 / _cl['psi_star'] ** 2)
    chk('⑦h ★ 절벽의 **크기**: legacy 는 floor 직전 큰 양수에서 0 으로 떨어지고, 곱셈은 같은 '
        '자리에서 1/ψ*² 배 작은 불연속만 남긴다 (동결된 finite floor 라 0 이 아니다 — AREA5-07)',
        _cl_ok,
        (f"ψ* = {_cl['psi_star']!r} · 좌극한 legacy {_cl['div_left']!r} vs 곱셈 "
         f"{_cl['mul_left']!r} (= R_M·ψ*) · 다음 값 {_cl['div_next']!r}/{_cl['mul_next']!r} · "
         f"비 {_cl['div_left'] / _cl['mul_left']:.6g} vs 1/ψ*² "
         f"{1.0 / _cl['psi_star'] ** 2:.6g}") if _cl else '절단면을 못 찾았다')
    #   스윕 쪽 거친 지표도 남긴다 (같은 사실의 이산 관측).
    chk('⑦h-b 스윕에서도 floor 직전 마지막 양수는 legacy 가 곱셈보다 100배 이상 크다',
        _sw['div_last_pos'] > 1e2 * _sw['mul_last_pos'] and _sw['mul_last_pos'] > 0.0,
        f"floor 직전 Rc — legacy {_sw['div_last_pos']!r} vs 곱셈 {_sw['mul_last_pos']!r}")
    #   ★★ ⑦i — **독립 oracle** (`R4-08` 이 요구한 것).  위 ⑦ 은 ψ 를 **솔버에서 받아**
    #      기대식에도 쓰므로, ψ 가 잘못 바뀌면 기대값이 **같이 움직여** 통과한다 — 실제로
    #      `floor 1e-4 → 0` 과 `ψ 지수 1.5 → 1.0` 두 변이가 13/13 초록이었다.
    #      ⇒ 고정 기하에서 s 와 ψ 를 **독립 계산**해 두 배치의 식을 각각 못박는다.
    #      ⚠ 면적은 재구현하지 않는다 (생산 `plastic_coverage` 에서 받는다) — ψ 만 oracle 이다.
    _or = _psi_oracle(_nc, _pc)
    chk('⑦i ★★ 독립 oracle: ψ 를 기하에서 따로 계산해 legacy = R_M/ψ · 곱셈 = R_M·ψ 를 각각 못박는다 '
        '(채널 3 × 상쌍 8 × 반지름 순서 4 — 순서 대칭 포함)',
        _or['n'] >= 100 and _or['bad_div'] == 0 and _or['bad_mul'] == 0 and _or['bad_floor'] == 0,
        f"활성 {_or['n']}건 · legacy 어긋남 {_or['bad_div']} · 곱셈 어긋남 {_or['bad_mul']} "
        f"· floor 판정 어긋남 {_or['bad_floor']} (ψ 지수 {_or['exponent']} · floor {_or['floor']})")
    #   ★★ ⑦j — **재료계수는 따로 못박는다** (`AREA5-06`).  Codex: 열 AM–SE 조화평균을
    #      1 로 바꿔도 ψ oracle 이 전부 초록이다 ⇒ *"ψ 배치가 맞다"* 와 *"계수가 맞다"* 는
    #      **다른 주장**이다.  `min(σ)` 규약과 면별 σ 배정을 R_Maxwell·R_bulk 로 각각 확인한다.
    _mo = _material_oracle(_nc)
    chk('⑦j ★★ 재료계수 oracle: k_weight(열 조화평균)·σ_rel 의 min 규약·면별 배정을 '
        'R_Maxwell 과 R_bulk 로 각각 못박는다',
        _mo['n'] >= 200 and _mo['bad_maxwell'] == 0 and _mo['bad_bulk'] == 0,
        f"픽스처 {_mo['n']}건 · R_Maxwell 어긋남 {_mo['bad_maxwell']} · R_bulk 어긋남 {_mo['bad_bulk']}")
    #   ⑦k — oracle 이 쓰는 상수가 솔버의 동결값과 같은가.  ⛔ import 하지 않고 **대조**한다:
    #      import 하면 상수 변이가 기대값과 같이 움직여 이 검사가 무의미해진다.
    _const_bad = {k: (v, getattr(_nc, k, None)) for k, v in MAT_ORACLE.items()
                  if getattr(_nc, k, None) != v}
    chk('⑦k oracle 이 못박은 재료 상수 = 솔버의 동결값 (K_AM·K_SE·r0·β)',
        not _const_bad, f'어긋남 {_const_bad or "없음"}')

    # ⑥ ★ P2-R2-06 — **실제 솔버**로 대조한다 (감사의 ψ 재구현이 아니라 build_network 자신).
    #    cap 2π→π 를 plastic 에 물린 솔버와 원판 솔버가 같은 Rc·R_total 을 내야 한다.
    pc_base = _load('_pc_s6b'); pc_s2 = _load('_pc_s6s', [(CAP_LINE, CAP_LINE_S2)])
    e0 = real_solver_edges(_load_nc('_nc_base', pc_base))[0]
    e1 = real_solver_edges(_load_nc('_nc_s2', pc_s2))[0]
    chk('⑥ 실제 build_network: cap 전환 전후 Rc·R_total 동일 (Codex 대조 조건 r .5/6 · δ .2 · A .04)',
        e0['R_constriction'] == e1['R_constriction'] and e0['R_total'] == e1['R_total'],
        f"Rc {e0['R_constriction']!r} → {e1['R_constriction']!r} · R_total {e0['R_total']!r} → {e1['R_total']!r}")
    chk('⑥b 그러나 진단 필드는 변한다 — A_physics 절반 · R_Maxwell 은 √2배 (σ 불변 ≠ 전 출력 불변)',
        abs(e1['A_physics'] / e0['A_physics'] - 0.5) < 1e-12
        and abs(e1['R_Maxwell'] / e0['R_Maxwell'] - math.sqrt(2.0)) < 1e-12,
        f"A {e0['A_physics']!r} → {e1['A_physics']!r} · R_Maxwell {e0['R_Maxwell']!r} → {e1['R_Maxwell']!r}")
    # ⑥c 판별력 — 솔버 호출부(Rc=0 분기)를 변이시키면 **이 대조가** 반드시 빨간불이 된다.
    #     Codex: 옛 감사는 이 변이에도 n_bad=0 이었다 (감사가 ψ 를 다시 구현했으므로).
    mut = [('                R_constriction = 0.0\n', '                R_constriction = R_Maxwell\n')]
    m0 = real_solver_edges(_load_nc('_nc_mb', pc_base, mut))[0]
    m1 = real_solver_edges(_load_nc('_nc_ms', pc_s2, mut))[0]
    chk('⑥c 판별력: 솔버의 Rc=0 분기를 R_Maxwell 로 바꾸면 cap 전환이 **실제로** 값을 움직인다 '
        '(Codex: Rc 0.7071 → 1.0)',
        m0['R_constriction'] != m1['R_constriction'],
        f"변이판 Rc {m0['R_constriction']!r} → {m1['R_constriction']!r}")

    print('수송 cap 동치 SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description='S2 면적 cap 전환의 솔버 영향 (AREA-12)')
    ap.add_argument('-n', type=int, default=20000)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--emit-baseline', action='store_true',
                    help='⑦f 의 **봉인 기준**을 고정 커밋 소스로 다시 만든다 (AREA5-05).  '
                         '⛔ 만든 뒤 출력된 지문을 BASELINE_SHA256 에 손으로 박아야 한다')
    a = ap.parse_args()
    if a.emit_baseline:
        return emit_baseline()
    if a.selftest:
        return _selftest()
    st = run(a.n, a.seed)
    print()
    if st['n_bad'] == 0 and st['n_psi_branch_diff'] == 0:
        print('⇒ **S2 는 솔버 `a_eff` 에 대해 항등 변환이다** (clamp 가 이미 하고 있다).')
        print(f'   차이가 난 {st["n_ulp"]} 건은 전부 `√(πR²/π) ≠ R` 의 **1 ULP 반올림**이고')
        print('   ψ 분기(≤ 1e-4 → R_c = 0)를 넘지 않는다.')
        print('⚠ `A_physics` 자체는 바뀐다 ⇒ coverage·반응면적·B3 쪽에서만 효과가 있고,')
        print('  `AREA-03` 대로 그쪽을 동결하면 **아무 데도 안 남는다**.')
        return 0
    print(f'⇒ ⚠ `a_eff` 가 실제로 움직인다 (설명 안 되는 차이 {st["n_bad"]} · '
          f'ψ 분기 차 {st["n_psi_branch_diff"]}) — 위 산술 주장을 재검토할 것.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
