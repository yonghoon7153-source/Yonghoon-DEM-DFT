#!/usr/bin/env python
"""run_anneal.py — Pipeline Step 3: Li-selective thermal annealing.

Takes champion candidate structures from screening and runs MLIP MD at
500 K for tens of ps. At 500 K Li⁺ hops actively (Eₐ ≈ 0.2 eV << kT = 0.043
eV) while PS₄ framework (P-S ≈ 3.5 eV) and the Cl⁻ cage stay rigid — i.e.,
we re-optimize only the Li sublattice while keeping the anion arrangement
fixed (D'Amore 2022, Pustorino 2025 ordering ↔ B0 evidence).

After MD, a final UMA relax (FIRE) gives the post-anneal energy. Compare
to the pre-anneal energy from screening to see whether the deeper basin
shifted the candidate ranking — Pipeline doc cites a Li6PS5Cl example
where screening 4th → anneal 1st.

Usage:
  # Anneal a hand-picked list of xyz files (one per champion).
  python3 run_anneal.py \\
      --xyz path/to/Nd2O3_x050_s00.xyz path/to/La2O3_x050_s00.xyz ... \\
      --out runs/anneal_top5_2026_05_15/ \\
      --temperature 500 --time_ps 50

  # Or pull the top-N candidates straight from analyze_screening output.
  python3 run_anneal.py \\
      --top_candidates runs/.../top_candidates_v2.json \\
      --top 5 --out runs/anneal_top5_2026_05_15/
"""
import argparse
import json
import zlib
import sys
import time
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.optimize import FIRE
from ase import units

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance

try:
    from ase.filters import FrechetCellFilter as CellFilter
except ImportError:
    try:
        from ase.constraints import ExpCellFilter as CellFilter
    except ImportError:
        from ase.constraints import UnitCellFilter as CellFilter


def load_uma_calc(device: str = 'cuda', task: str = 'omat'):
    """Load UMA-s-1p1 calculator (FAIRChem)."""
    from fairchem.core import pretrained_mlip, FAIRChemCalculator
    predictor = pretrained_mlip.get_predict_unit('uma-s-1p1', device=device)
    return FAIRChemCalculator(predictor, task_name=task)


def _struct_hash(atoms) -> str:
    """구조의 **종 인식** 해시 — 원소 순서·좌표·셀을 다 담는다. 앞 16자만 쓴다.

    ⛔ 못 하는 것: 대칭 등가 구조를 같다고 하지 않는다 (좌표 그대로 본다) ·
       부동소수 표현에 민감하므로 **1e-6 Å 로 반올림**해서 잰다.
    """
    import hashlib
    import numpy as _np
    parts = [",".join(atoms.get_chemical_symbols()),
             _np.round(_np.asarray(atoms.get_positions()), 6).tobytes(),
             _np.round(_np.asarray(atoms.cell.array), 6).tobytes()]
    h = hashlib.sha256()
    for x in parts:
        h.update(x.encode() if isinstance(x, str) else x)
    return h.hexdigest()[:16]


def winner_name(xyz_path):
    """v4.5.18 NEW-D defensive fix: cascade outputs share stem
    'post_relax' or 'post_md' across winners. Use parent dir name in
    that case. Same pattern as bvse_proxy/run_mlip_postproc (v4.5.17)
    + combine_rankings.py CR-A (v4.5.8). Round 3 reviewer flagged this
    as 'conditional hole — safe in current cascade flow but manual
    re-anneal of post_relax.xyz would collide'. Defensive patch."""
    p = Path(xyz_path)
    if p.stem in ('post_relax', 'post_md'):
        return p.parent.name
    return p.stem


def anneal_one(xyz_path: Path, calc, out_dir: Path,
              temperature_K: float = 500, time_ps: float = 50,
              dt_fs: float = 2.0, friction: float = 0.01,
              relax_steps: int = 1500, relax_fmax: float = 0.05,
              cell_relax: bool = True, log_every: int = 500,
              seed: int = 0) -> dict:
    """Run Langevin NVT MD at ``temperature_K`` for ``time_ps``, then a final
    cell+positions relax. Records pre-anneal, post-MD, and post-relax energies
    so you can see how much extra binding the thermal sampling found.

    ⛔⛔ 2026-08-30 (회신 AL P0-3) — **이 함수는 seed 를 안 받았다.**
      `MaxwellBoltzmannDistribution` 과 `Langevin` 이 전역 numpy 상태를 쓰는데
      그걸 고정하지도 기록하지도 않아서, **같은 입력을 다시 돌리면 다른 endpoint** 로 갔다.
      정본 CSV 실측: 같은 설계의 복제본 삼중쌍 227개 중 anneal **후** 에너지가
      1e-4 안에서 일치하는 것이 **0개** (상대산포 중앙 6.0e-3 · 최대 2.8e-2).
      예 Ag2O: E_post = −4.1964 / −4.1888 / −4.1113 eV/atom, ΔV = −7.97 / −3.69 / −2.85 %.
      그 위에서 계산된 BVS·탄성 G 가 Pareto front 와 사전등록 순위를 정하고 있었다.
      ⇒ 이제 `seed` 를 **받아서 두 곳에 다 주입하고 결과에 기록한다.**

    ⛔ 이 함수가 못 하는 것
      · seed 를 고정해도 **비트 단위 재현을 보장하지 못한다** — GPU 커널 비결정성·
        ASE/torch 버전·장치가 바뀌면 달라진다. seed 는 재현의 **필요조건**이지 충분조건이 아니다.
      · 결과 구조가 물리적으로 옳은지 판정하지 않는다 (수렴 플래그만 낸다).
    """
    name = winner_name(xyz_path)
    work = out_dir / name
    work.mkdir(parents=True, exist_ok=True)

    atoms = read(str(xyz_path))
    atoms.calc = calc
    E_pre = float(atoms.get_potential_energy())
    n_atoms = len(atoms)

    # ⛔ seed 를 **두 곳 다** 준다 — 초기속도와 Langevin 잡음은 서로 다른 난수원이다.
    #   하나만 고정하면 여전히 비결정적이다 (회신 AL P0-3).
    rng_v = np.random.default_rng(seed)
    rng_md = np.random.default_rng(seed + 1_000_003)      # 서로 다른 스트림
    MaxwellBoltzmannDistribution(atoms, temperature_K=temperature_K, rng=rng_v)

    n_steps = int(time_ps * 1000 / dt_fs)
    print(f"  [{name}] MD: T={temperature_K}K, dt={dt_fs}fs, "
          f"steps={n_steps} ({time_ps}ps), {n_atoms} atoms")

    md_log = work / 'md.log'
    md_traj = work / 'md.traj'
    dyn = Langevin(atoms, dt_fs * units.fs,
                   temperature_K=temperature_K,
                   friction=friction,
                   logfile=str(md_log),
                   trajectory=str(md_traj),
                   rng=rng_md,
                   loginterval=log_every)

    t0 = time.time()
    try:
        dyn.run(n_steps)
    finally:                      # 2026-11-09 (Codex DV P2): 예외 경로에서도 md.log · md.traj 를 닫는다 (Windows 임시폴더 정리 실패)
        if hasattr(dyn, 'close'):
            dyn.close()
    t_md = time.time() - t0
    # ⛔ 2026-11-09 (Codex DW P1-2): 궤적 파일 · 저장 간격을 결과 기록에 남긴다 — 옛 판은 md.traj 를 쓰고도 기록에
    #   없어서 파일럿 판독이 저장 간격을 명령줄에서 받았다 (틀린 간격을 주면 2 · 5 · 10 ps 프레임을 20 · 50 · 100 ps 로 읽었다).
    from ase.io.trajectory import Trajectory as _Traj
    with _Traj(str(md_traj)) as _T:
        n_frames = len(_T)
    md_traj_rec = {'rel': f'{name}/md.traj', 'sha256': _file_sha256(md_traj), 'n_frames': int(n_frames),
                   'log_every_steps': int(log_every), 'dt_fs': float(dt_fs), 'n_steps': int(n_steps)}
    E_md_final = float(atoms.get_potential_energy())
    print(f"  [{name}] MD done ({t_md:.1f}s) "
          f"E_pre={E_pre/n_atoms:.4f} → E_md={E_md_final/n_atoms:.4f} eV/atom")

    # Save post-MD snapshot
    write(work / 'post_md.xyz', atoms)

    # Final relax
    target = CellFilter(atoms) if cell_relax else atoms
    opt = FIRE(target, logfile=str(work / 'relax.log'))
    t0 = time.time()
    try:
        opt_ret = opt.run(fmax=relax_fmax, steps=relax_steps)
    finally:
        if hasattr(opt, 'close'):
            opt.close()
    t_relax = time.time() - t0
    n_relax_steps = opt.get_number_of_steps()
    # ⛔ 2026-11-09 (Codex DU P2): 옛 판정 `n_relax_steps < relax_steps` 는 **마지막 허용 걸음에서 수렴**하면
    #   미수렴으로 적었다 (ASE 3.29 LJ 재현: 17 걸음 상한 · 17 걸음째 fmax 0.0093 < 0.01 · 옛 판정 False).
    #   이제 실제 최종 힘으로 판정한다 (ASE 와 같은 기준: max_i |F_i| < fmax · 셀 필터면 셀 자유도 포함) ·
    #   opt.run() 반환값은 대조로 기록한다.
    fvec = np.asarray(target.get_forces())
    fmax_final = float(np.sqrt((fvec ** 2).sum(axis=1).max())) if len(fvec) else 0.0
    converged = bool(fmax_final < relax_fmax)
    opt_returned = opt_ret if isinstance(opt_ret, bool) else None
    E_post = float(atoms.get_potential_energy())
    write(work / 'post_relax.xyz', atoms)

    delta_E_per_atom = (E_post - E_pre) / n_atoms
    print(f"  [{name}] relax {n_relax_steps} steps ({t_relax:.1f}s) "
          f"E_post={E_post/n_atoms:.4f} eV/atom, "
          f"ΔE_anneal={delta_E_per_atom*1000:+.1f} meV/atom, "
          f"conv={converged}")

    return {
        'name': name,
        # ⛔ 계보 3종 — 이게 없으면 "같은 구조인가" 를 나중에 되물을 수 없다 (회신 AL P0-3)
        'seed': int(seed),
        'rng_streams': {'velocities': int(seed), 'langevin': int(seed) + 1_000_003},
        'struct_sha256': {
            'input': _struct_hash(read(str(xyz_path))),
            'post_md': _struct_hash(read(str(work / 'post_md.xyz'))),
            'post_relax': _struct_hash(atoms),
        },
        '⚠_재현': ('seed 고정은 재현의 **필요조건**이지 충분조건이 아니다 — GPU 커널 '
                   '비결정성·ASE/torch 버전·장치가 바뀌면 달라진다'),
        'xyz_input': str(xyz_path),
        'n_atoms': n_atoms,
        'temperature_K': temperature_K,
        'time_ps': time_ps,
        'dt_fs': dt_fs,
        'E_pre_anneal': E_pre,
        'E_md_final': E_md_final,
        'E_post_relax': E_post,
        'delta_E_anneal_meV_per_atom': delta_E_per_atom * 1000,
        'cell_pre': read(str(xyz_path)).cell.array.tolist(),
        'cell_post': atoms.cell.array.tolist(),
        'volume_pre': float(read(str(xyz_path)).get_volume()),
        'volume_post': float(atoms.get_volume()),
        't_md_s': t_md,
        't_relax_s': t_relax,
        'n_relax_steps': n_relax_steps,
        'relax_steps_max': int(relax_steps),
        'relax_fmax': float(relax_fmax),
        'fmax_final': fmax_final,
        'opt_run_returned': opt_returned,
        **({'⚠_수렴_판정_불일치': f'opt.run() {opt_returned} · 최종 힘 판정 {converged}'}
           if opt_returned is not None and opt_returned != converged else {}),
        'converged': converged,
        'post_md_xyz': str(work / 'post_md.xyz'),
        'post_relax_xyz': str(work / 'post_relax.xyz'),
        # ⛔ 2026-11-09 (Codex DV P1-2): 실제로 저장한 결과 파일의 해시 · 조성 — 재개 생략과 결과 검사가
        #   verify_outputs() 한 함수로 존재 · 판독 · 해시 · 조성을 확인한다 (옛 판: 지우거나 바꿔도 통과)
        'outputs': {**{k: {'rel': f'{name}/{k}.xyz', 'sha256': _file_sha256(work / f'{k}.xyz')}
                       for k in ('post_md', 'post_relax')},
                    'md_traj': md_traj_rec},
        'log_every_steps': int(log_every),
        'composition': _composition(atoms),
    }


# ----------------------------------------------------------------------
# 재개 정체성 · 상태 · 결과 검사                       (2026-11-09 · Codex DU P1-4)
# ----------------------------------------------------------------------
#   ⛔ 옛 재개는 **이름만** 봤다 — 0 ps 이완 기록을 만든 뒤 좌표 · seed 를 바꾸고 20 ps 를 요청해도
#     'To process: 0/1' 로 건너뛰었고, 파일이 없어 실패한 기록도 끝난 것으로 셌다 (복구해도 다시 안 돌림 ·
#     첫 실패 때도 종료코드 0). 이제:
#     · 기록마다 정체성 (입력 파일 sha256 · 구조 해시 · 단계 · 온도 · 시간 · dt · 마찰 · 이완 걸음 · fmax ·
#       셀 이완 · seed · 모델) 과 그 sha256 을 남긴다.
#     · 같은 이름의 기존 기록이 **정체성이 다르면 멈춘다** (같은 폴더에 섞지 않는다 — 새 --out 을 쓴다).
#     · 상태를 나눈다: converged · unconverged · failed. **failed 는 끝난 것이 아니다** — 다음 실행에서 다시 돈다.
#     · 실패가 하나라도 있으면 종료코드 1.
#     · 정체성이 없는 옛 기록은 받지 않는다 (--accept_legacy_records 로만 · 표시해 둔다).
#   ⛔ 못 하는 것: 결과가 물리적으로 맞는지 · GPU 비결정성 (seed 는 필요조건) · 다른 묶음 기록의 정체성 검사
#     (이번에 넘긴 구조만 본다).
def _file_sha256(p) -> str:
    import hashlib
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _composition(atoms) -> dict:
    c = {}
    for s in atoms.get_chemical_symbols():
        c[s] = c.get(s, 0) + 1
    return dict(sorted(c.items()))


def geometry_problems(atoms) -> list:
    """기하 유효성 → 문제 목록. 좌표 · 셀이 유한하고 (NaN · inf 없음) 세 방향 주기 셀이면 부피가 0 이 아니어야 한다.

    2026-11-09 (Codex DW P2): 옛 판은 NaN 좌표가 든 결과도 sha256 만 맞으면 통과했고, 판독기 끝 꼴 분류가 그 구조를
    F_free 로 셌다 (NaN 거리는 모든 비교가 거짓 → 결합 0 · 최소 거리 inf). 이제 결과 검사에서 막는다.
    ⛔ 못 하는 것: 원자가 겹쳤는지 · 셀이 물리적으로 말이 되는지는 보지 않는다 (유한성 · 특이성까지).
    """
    p = []
    pos = np.asarray(atoms.get_positions(), dtype=float)
    cell = np.asarray(atoms.cell.array, dtype=float)
    if not np.isfinite(pos).all():
        p.append('좌표에 NaN · inf')
    if not np.isfinite(cell).all():
        p.append('셀에 NaN · inf')
    elif all(atoms.pbc) and abs(float(np.linalg.det(cell))) < 1e-6:
        p.append('주기 셀 부피 0 (특이 셀)')
    return p


def verify_outputs(rec: dict, out_dir) -> list:
    """완료 기록의 결과 파일 결속 검사 → 문제 목록 (빈 목록이면 통과). 재개 생략 · check_results 가 같이 쓴다.

    본다: 'outputs' 기록 유무 · 파일 존재 · sha256 일치 · ASE 로 읽힘 · 원자 수 · 조성 (기록 = 입력 정체성의 원자 수) ·
    기하 유효성 (유한 좌표 · 셀 · 특이 셀 아님 — DW P2) · md_traj 기록이 있으면 궤적도 (존재 · sha256 · 프레임 수 =
    걸음 수 // 저장 간격 + 1 · 프레임마다 원자 수 · 조성 · 기하 — DW P1-2).
    ⛔ 못 하는 것: 에너지가 그 구조의 것인지 다시 계산하지 않는다 (해시 결속까지) · md_traj 가 없는 옛 기록은
       궤적을 안 본다 (궤적이 필요한 판독 — 파일럿 — 은 판독기가 md_traj 기록을 따로 요구한다).
    """
    out_dir = Path(out_dir)
    probs = []
    outs = rec.get('outputs')
    if not outs:
        return [f"{rec.get('name')}: 결과 파일 해시 기록이 없다 (2026-11-09 이전 판 기록)"]
    n_id = (rec.get('identity') or {}).get('n_atoms')
    for k in ('post_md', 'post_relax'):
        e = outs.get(k)
        if not e:
            probs.append(f"{rec.get('name')}: {k} 기록 없음")
            continue
        f = out_dir / e['rel']
        if not f.is_file():
            probs.append(f"{rec.get('name')}: {k} 파일 없음 ({e['rel']})")
            continue
        if _file_sha256(f) != e['sha256']:
            probs.append(f"{rec.get('name')}: {k} 파일이 기록 뒤 바뀌었다 (sha256 불일치)")
            continue
        try:
            a = read(str(f))
        except Exception as ex:
            probs.append(f"{rec.get('name')}: {k} 를 못 읽는다 ({type(ex).__name__})")
            continue
        if n_id is not None and len(a) != int(n_id):
            probs.append(f"{rec.get('name')}: {k} 원자 수 {len(a)} ≠ 입력 {n_id}")
        if rec.get('composition') and _composition(a) != rec['composition']:
            probs.append(f"{rec.get('name')}: {k} 조성 {_composition(a)} ≠ 기록 {rec['composition']}")
        probs += [f"{rec.get('name')}: {k} {g}" for g in geometry_problems(a)]
    e = outs.get('md_traj')
    if e is not None:
        probs += _verify_md_traj(rec, e, out_dir, n_id)
    return probs


def _verify_md_traj(rec, e, out_dir, n_id) -> list:
    nm = rec.get('name')
    f = Path(out_dir) / e.get('rel', '')
    if not f.is_file():
        return [f"{nm}: md_traj 파일 없음 ({e.get('rel')})"]
    if _file_sha256(f) != e.get('sha256'):
        return [f"{nm}: md_traj 가 기록 뒤 바뀌었다 (sha256 불일치)"]
    try:
        le, ns, nf = int(e['log_every_steps']), int(e['n_steps']), int(e['n_frames'])
    except (KeyError, TypeError, ValueError):
        return [f"{nm}: md_traj 기록에 저장 간격 · 걸음 수 · 프레임 수가 없다"]
    p = []
    if le <= 0 or nf != ns // le + 1:
        p.append(f"{nm}: md_traj 프레임 수 {nf} ≠ 걸음 {ns} // 간격 {le} + 1")
    idn = rec.get('identity') or {}
    if idn.get('dt_fs') is not None and abs(float(idn['dt_fs']) - float(e.get('dt_fs', -1))) > 1e-12:
        p.append(f"{nm}: md_traj dt {e.get('dt_fs')} ≠ 정체성 dt {idn['dt_fs']}")
    if idn.get('time_ps') is not None and float(e.get('dt_fs', 0)) > 0 \
            and ns != int(round(float(idn['time_ps']) * 1000 / float(e['dt_fs']))):
        p.append(f"{nm}: md_traj 걸음 {ns} ≠ 정체성 시간 {idn['time_ps']} ps / dt")
    from ase.io.trajectory import Trajectory as _Traj
    try:
        with _Traj(str(f)) as T:
            if len(T) != nf:
                p.append(f"{nm}: md_traj 실제 프레임 {len(T)} ≠ 기록 {nf}")
            for i, a in enumerate(T):
                if n_id is not None and len(a) != int(n_id):
                    p.append(f"{nm}: md_traj 프레임 {i} 원자 수 {len(a)} ≠ 입력 {n_id}"); break
                if rec.get('composition') and _composition(a) != rec['composition']:
                    p.append(f"{nm}: md_traj 프레임 {i} 조성이 기록과 다르다"); break
                g = geometry_problems(a)
                if g:
                    p.append(f"{nm}: md_traj 프레임 {i} {g[0]}"); break
    except Exception as ex:
        p.append(f"{nm}: md_traj 를 못 읽는다 ({type(ex).__name__})")
    return p


def run_identity(xyz_path, *, temperature_K, time_ps, dt_fs, friction, relax_steps,
                 relax_fmax, cell_relax, seed, model, purpose=None) -> dict:
    """재개 정체성. purpose (실행 목적) 는 **줄 때만** 넣는다 — 안 주면 옛 정체성 · identity_sha 가 그대로다.

    2026-11-09 (Codex DX P1-1): 같은 시작 파일 · 시간 · 온도로 도는 두 실행 (b2o3 파일럿 런 · 8 단계 어닐) 을
    단계 · 설정만으로는 가를 수 없었다 — 파일럿 런 기록을 8 단계 결과로 끼워 넣어도 판독이 통과했다.
    실행기가 계획 manifest 의 purpose 를 --purpose 로 넘기고, 판독기가 단계마다 요구하는 목적과 대조한다.
    """
    a = read(str(xyz_path))
    idn = {'input_file_sha256': _file_sha256(xyz_path), 'input_struct': _struct_hash(a),
           'n_atoms': len(a), 'stage': 'relax_only' if float(time_ps) == 0.0 else 'anneal_relax',
           'temperature_K': float(temperature_K), 'time_ps': float(time_ps), 'dt_fs': float(dt_fs),
           'friction': float(friction), 'relax_steps': int(relax_steps), 'relax_fmax': float(relax_fmax),
           'cell_relax': bool(cell_relax), 'seed': int(seed), 'model': str(model)}
    if purpose is not None:
        idn['purpose'] = str(purpose)
    return idn


def identity_sha(idn: dict) -> str:
    import hashlib
    return hashlib.sha256(json.dumps(idn, sort_keys=True).encode()).hexdigest()


def _write_atomic(path: Path, text: str):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(text)
    tmp.replace(path)


def derive_seed(base_seed: int, name: str) -> int:
    # 구조마다 **다른** seed — 이름에서 결정론적으로 (같은 구조를 다시 돌리면 같은 seed)
    return int(base_seed) + (zlib.crc32(name.encode()) & 0xFFFF)


def run_batch(xyz_paths, out, P: dict, calc, model: str, accept_legacy: bool = False,
              anneal_fn=None, rerun_mismatched: bool = False):
    """구조 묶음을 어닐 · 이완한다 → (종료코드, 이번에 돈 수). P = anneal_one 설정 + 'seed'.

    재개: 같은 이름 · 같은 정체성 · 상태 converged/unconverged 인 기록만 건너뛴다.
    """
    anneal_fn = anneal_fn or anneal_one
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    results_path = out / 'anneal_results.json'
    names = [winner_name(p) for p in xyz_paths]
    dup = sorted({n for n in names if names.count(n) > 1})
    if dup:
        raise SystemExit(f"⛔ 같은 이름의 입력이 둘 이상 {dup} — 출력 폴더가 겹친다")
    old = {}
    if results_path.exists():
        for r in json.loads(results_path.read_text()).get('results', []):
            old[r['name']] = r
    keep, todo, n_retry, legacy = dict(old), [], 0, []
    for p in xyz_paths:
        n = winner_name(p)
        seed = derive_seed(P['seed'], n)
        try:
            idn = run_identity(p, temperature_K=P['temperature_K'], time_ps=P['time_ps'],
                               dt_fs=P['dt_fs'], friction=P['friction'], relax_steps=P['relax_steps'],
                               relax_fmax=P['relax_fmax'], cell_relax=P['cell_relax'], seed=seed,
                               model=model, purpose=P.get('purpose'))
            isha = identity_sha(idn)
        except Exception as e:                       # 입력을 못 읽음 → 실패 기록 (끝난 것 아님)
            idn, isha = None, None
            todo.append((p, n, seed, idn, isha, f'입력을 못 읽음: {e}'))
            continue
        r = old.get(n)
        if r is None:
            todo.append((p, n, seed, idn, isha, None))
            continue
        if r.get('status') == 'failed' or 'error' in r:      # 옛 판 실패 기록 ('error' 만 있음) 도 실패다
            n_retry += 1
            todo.append((p, n, seed, idn, isha, None))
            continue
        if 'identity_sha' not in r:
            if not accept_legacy:
                raise SystemExit(f"⛔ {n}: 기존 기록에 정체성이 없다 (옛 판 결과) — 새 --out 을 쓰거나 "
                                 f"--accept_legacy_records 로 명시하라 (그대로 끝난 것으로 셀 수 없다)")
            r = dict(r)
            r['⚠_legacy_accepted'] = '정체성 없는 옛 기록을 --accept_legacy_records 로 받았다'
            keep[n] = r
            legacy.append(n)
            continue
        if r['identity_sha'] != isha:
            ro = r.get('identity') or {}
            diff = sorted(k for k in set(idn) | set(ro) if idn.get(k) != ro.get(k))
            raise SystemExit(f"⛔ {n}: 같은 이름의 기존 기록과 입력 · 설정이 다르다 (다른 칸 {diff}) — "
                             f"새 --out 을 쓰라 (같은 폴더에 섞지 않는다)")
        vo = verify_outputs(r, out)                 # 정체성이 같아도 결과 파일이 그 기록의 것이어야 건너뛴다
        if vo:
            if not rerun_mismatched:
                raise SystemExit(f"⛔ {n}: 완료 기록의 결과 파일이 결속을 못 넘는다 ({vo[0]}) — 새 --out 을 쓰거나 "
                                 f"--rerun_mismatched 로 명시해 다시 돌린다")
            n_retry += 1
            todo.append((p, n, seed, idn, isha, None))
            continue
    print(f"To process: {len(todo)}/{len(xyz_paths)} (실패 재시도 {n_retry} · 옛 기록 받음 {len(legacy)})")

    def _save():
        res = list(keep.values())
        st = [r.get('status') for r in res]
        _write_atomic(results_path, json.dumps({
            'provenance': get_provenance(),
            'temperature_K': P['temperature_K'], 'time_ps': P['time_ps'], 'model': model,
            'n_done': sum(s in ('converged', 'unconverged') for s in st),
            'n_converged': st.count('converged'), 'n_unconverged': st.count('unconverged'),
            'n_failed': st.count('failed'),
            'results': res,
        }, indent=2, default=str))

    n_ran = 0
    for i, (p, n, seed, idn, isha, pre_err) in enumerate(todo):
        print(f"\n[{i+1}/{len(todo)}] {n}")
        if pre_err is not None:
            rec = {'name': n, 'xyz_input': str(p), 'error': pre_err, 'status': 'failed',
                   'identity': idn, 'identity_sha': isha}
            print(f"  ❌ FAILED: {pre_err}")
        else:
            try:
                rec = anneal_fn(p, calc, out, temperature_K=P['temperature_K'], time_ps=P['time_ps'],
                                dt_fs=P['dt_fs'], friction=P['friction'], relax_steps=P['relax_steps'],
                                relax_fmax=P['relax_fmax'], cell_relax=P['cell_relax'],
                                log_every=P.get('log_every', 500), seed=seed)
                rec['status'] = 'converged' if rec['converged'] else 'unconverged'
            except Exception as e:
                print(f"  ❌ FAILED: {e}")
                rec = {'name': n, 'xyz_input': str(p), 'error': str(e), 'status': 'failed'}
            rec['identity'] = idn
            rec['identity_sha'] = isha
            n_ran += 1
        keep[n] = rec
        _save()
    if not todo and not results_path.exists():
        _save()
    batch = [keep[n] for n in names if n in keep]
    n_fail = sum(r.get('status') == 'failed' for r in batch)
    n_unc = sum(r.get('status') == 'unconverged' for r in batch)
    print(f"이번 묶음: {len(batch)} 기록 · 실패 {n_fail} · 미수렴 {n_unc}")
    return (1 if n_fail else 0), n_ran


def check_results(path, expect_n=None, expect_time_ps=None, expect_temperature=None,
                  require_converged=False, expect_purpose=None) -> list:
    """anneal_results.json 검사 → 문제 목록. 실행기가 '요청한 단계가 실제로 전달됐나' 를 여기서 본다.

    본다: 상태 (failed · 상태 없음 = 문제) · 정체성 유무 · time_ps · 온도가 요청과 같은가 · 끝난 기록 수 ·
    (require_converged 면) 미수렴 · 결과 파일 결속 (verify_outputs — 존재 · sha256 · 판독 · 조성).
    ⛔ 못 하는 것: 에너지가 그 구조의 것인지 다시 계산하지 않는다.
    """
    p = Path(path)
    if not p.exists():
        return [f"결과 없음: {p}"]
    res = json.loads(p.read_text()).get('results', [])
    out_dir = p.parent
    prob = []
    ok = 0
    for r in res:
        n = r.get('name', '?')
        st = r.get('status')
        if st not in ('converged', 'unconverged'):
            prob.append(f"{n}: 상태 {st!r} (failed 또는 옛 판 기록)")
            continue
        idn = r.get('identity')
        if not idn:
            prob.append(f"{n}: 정체성 없음")
            continue
        if expect_time_ps is not None and abs(float(idn['time_ps']) - float(expect_time_ps)) > 1e-9:
            prob.append(f"{n}: time_ps {idn['time_ps']} ≠ 요청 {expect_time_ps}")
        if expect_temperature is not None and abs(float(idn['temperature_K']) - float(expect_temperature)) > 1e-9:
            prob.append(f"{n}: 온도 {idn['temperature_K']} ≠ 요청 {expect_temperature}")
        if expect_purpose is not None and idn.get('purpose') != expect_purpose:
            prob.append(f"{n}: 실행 목적 {idn.get('purpose')} ≠ 요청 {expect_purpose}")
        if require_converged and st != 'converged':
            prob.append(f"{n}: 미수렴 (fmax_final {r.get('fmax_final')})")
        vo = verify_outputs(r, out_dir)             # 2026-11-09 (Codex DV P1-2) — 재개와 같은 함수
        if vo:
            prob.extend(vo)
            continue
        ok += 1
    if expect_n is not None and ok != int(expect_n):
        prob.append(f"끝난 기록 {ok} ≠ 기대 {expect_n}")
    return prob


def _check_results_cli(argv) -> int:
    ap = argparse.ArgumentParser(prog='run_anneal.py --check_results')
    # ⚠ required=True 를 쓰지 않는다 — tools/convention_check.py 가 이 파일의 required 플래그를
    #   '모든 셸 호출이 넘겨야 하는 인자' 로 읽는다 (2026-11-09 tier_cascade.sh 오탐).
    ap.add_argument('--check_results')
    ap.add_argument('--expect_n', type=int)
    ap.add_argument('--expect_time_ps', type=float)
    ap.add_argument('--expect_temperature', type=float)
    ap.add_argument('--require_converged', action='store_true')
    ap.add_argument('--expect_purpose')
    a = ap.parse_args(argv)
    if not a.check_results:
        ap.error("--check_results <anneal_results.json> 가 필요하다")
    prob = check_results(a.check_results, a.expect_n, a.expect_time_ps, a.expect_temperature,
                         a.require_converged, a.expect_purpose)
    for x in prob:
        print("  ✗", x)
    print(f"check_results {'OK' if not prob else 'FAIL'} — 문제 {len(prob)} 건 ({a.check_results})")
    return 1 if prob else 0



def _selftest() -> int:
    """seed 배관 검사 — **음성 경로가 핵심**이다 (양성만 있으면 아무것도 보증 못 한다)."""
    ok = [0, 0]

    def chk(c, m):
        ok[0] += 1; ok[1] += bool(c)
        print(("  ✔ " if c else "  ✘ ") + m)

    import inspect
    src = inspect.getsource(anneal_one)
    chk("rng=rng_v" in src,
        "① 초기속도(MaxwellBoltzmann)에 rng 를 준다")
    chk("rng=rng_md" in src,
        "① Langevin 에도 rng 를 준다 (하나만 고정하면 여전히 비결정적)")
    chk(src.count("default_rng") == 2,
        "① 두 난수원이 **서로 다른 스트림**이다")
    chk("'seed': int(seed)" in src and "struct_sha256" in src,
        "② seed 와 구조 해시 3종(input·post_md·post_relax)을 결과에 남긴다")
    # ⛔음성 — seed 는 required 다. 안 주면 argparse 가 거부해야 한다.
    import subprocess
    r = subprocess.run([sys.executable, __file__, "--help"],
                       capture_output=True, text=True)
    chk("--seed" in r.stdout and "필수" in r.stdout,
        "⛔음성: --seed 가 **필수**로 노출된다 (기본값을 두면 안 준 것과 구분이 안 된다)")

    # ③ 구조 해시 — 좌표가 1e-6 넘게 다르면 갈라져야 하고, 그 아래면 같아야 한다
    class _A:
        def __init__(self, pos, sym=("Li", "Ni")):
            self._p, self._s = pos, list(sym)
            self.cell = type("C", (), {"array": [[5, 0, 0], [0, 5, 0], [0, 0, 5]]})()

        def get_chemical_symbols(self): return self._s
        def get_positions(self): return self._p

    a = _A([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]])
    b = _A([[0.0, 0.0, 0.0], [1.0 + 1e-9, 0.0, 0.0]])
    c = _A([[0.0, 0.0, 0.0], [1.001, 0.0, 0.0]])
    d = _A([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]], sym=("Ni", "Li"))
    chk(_struct_hash(a) == _struct_hash(b),
        "③ 1e-6 Å 아래 차이는 같은 구조로 본다 (부동소수 잡음에 안 흔들린다)")
    chk(_struct_hash(a) != _struct_hash(c),
        "③ [음성] 0.001 Å 차이는 다른 구조다")
    chk(_struct_hash(a) != _struct_hash(d),
        "③ [음성] **종 순서가 다르면 다른 구조다** (좌표만 보면 놓친다)")

    # ④–⑦ 2026-11-09 (Codex DU P1-4 · P2) — 수렴 판정 · 재개 정체성 · 실패 · 결과 검사.
    #   UMA 없이 LJ (ASE 내장) 로 실제 anneal_one · run_batch 경로를 돈다.
    import tempfile
    from ase import Atoms
    from ase.calculators.lj import LennardJones
    from ase.calculators.calculator import Calculator, all_changes

    def lj():
        return LennardJones(sigma=3.4, epsilon=0.0104, rc=6.0)

    def ar4(shift=0.0):
        return Atoms("Ar4", positions=[[0, 0, 0], [3.9 + shift, 0.2, 0], [0.1, 3.7, 0.3], [3.6, 3.8, 0.1]],
                     cell=[12, 12, 12], pbc=True)

    class _Boom(Calculator):
        implemented_properties = ['energy', 'forces']

        def calculate(self, atoms=None, properties=('energy',), system_changes=all_changes):
            raise RuntimeError("일부러 실패")

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        x = td / "ar4.xyz"
        write(x, ar4())
        r_full = anneal_one(x, lj(), td / "o0", time_ps=0, relax_steps=2000, relax_fmax=0.01,
                            cell_relax=False, seed=1)
        k = r_full['n_relax_steps']
        r_k = anneal_one(x, lj(), td / "o1", time_ps=0, relax_steps=k, relax_fmax=0.01, cell_relax=False, seed=1)
        chk(r_k['converged'] and r_k['n_relax_steps'] == k and r_k['fmax_final'] < 0.01,
            f"④ ⛔음성: **마지막 허용 걸음 ({k}) 에서 수렴**하면 수렴이다 (옛 판정 n < 상한 이면 False · Codex DU P2)")
        r_k1 = anneal_one(x, lj(), td / "o2", time_ps=0, relax_steps=k - 1, relax_fmax=0.01,
                          cell_relax=False, seed=1)
        chk(not r_k1['converged'] and r_k1['fmax_final'] >= 0.01,
            "④ [음성] 한 걸음 모자라면 미수렴이다 (위 시험이 늘 True 를 내는 게 아니다)")

        P0 = dict(temperature_K=500, time_ps=0, dt_fs=2.0, friction=0.01, relax_steps=500,
                  relax_fmax=0.01, cell_relax=False, seed=7)
        ob = td / "batch"
        rc1, n1 = run_batch([x], ob, P0, lj(), model="fake-lj")
        rc2, n2 = run_batch([x], ob, P0, lj(), model="fake-lj")
        chk(rc1 == 0 and n1 == 1 and rc2 == 0 and n2 == 0,
            "⑤ [양성] 같은 정체성이면 재개가 건너뛴다 (첫 실행 1 · 둘째 0)")
        for label, P_, xx in (("시간 0 → 20 ps", dict(P0, time_ps=0.004), x),
                              ("seed", dict(P0, seed=8), x),
                              ("이완 fmax", dict(P0, relax_fmax=0.02), x)):
            try:
                run_batch([xx], ob, P_, lj(), model="fake-lj")
                ok_ = False
            except SystemExit:
                ok_ = True
            chk(ok_, f"⑤ ⛔음성: 같은 이름 · **{label}** 이 다르면 건너뛰지 않고 멈춘다 (옛 판: 'To process 0/1')")
        write(x, ar4(shift=0.05))
        try:
            run_batch([x], ob, P0, lj(), model="fake-lj")
            ok_ = False
        except SystemExit:
            ok_ = True
        chk(ok_, "⑤ ⛔음성: 같은 이름 · **입력 좌표가 바뀌면** 멈춘다")
        write(x, ar4())

        of = td / "fail"
        rcf, _ = run_batch([x], of, P0, _Boom(), model="fake-lj")
        st = json.loads((of / "anneal_results.json").read_text())["results"][0]["status"]
        rcg, ng = run_batch([x], of, P0, lj(), model="fake-lj")
        st2 = json.loads((of / "anneal_results.json").read_text())["results"][0]["status"]
        chk(rcf == 1 and st == "failed" and rcg == 0 and ng == 1 and st2 == "converged",
            "⑥ ⛔음성: 실패는 종료코드 1 · 'failed' 로 남고 **다음 실행에서 다시 돈다** (옛 판: 끝난 것으로 셈 · 종료 0)")
        om = td / "missing"
        rcm, _ = run_batch([td / "nope.xyz"], om, P0, lj(), model="fake-lj")
        chk(rcm == 1, "⑥ ⛔음성: 입력 파일이 없으면 실패로 기록하고 종료코드 1")
        ol = td / "legacy"
        ol.mkdir()
        (ol / "anneal_results.json").write_text(json.dumps({"results": [
            {"name": "ar4", "E_post_relax": -1.0, "n_atoms": 4, "converged": True}]}))
        try:
            run_batch([x], ol, P0, lj(), model="fake-lj")
            ok_ = False
        except SystemExit:
            ok_ = True
        rcl, nl = run_batch([x], ol, P0, lj(), model="fake-lj", accept_legacy=True)
        chk(ok_ and rcl == 0 and nl == 0,
            "⑥ ⛔음성: 정체성 없는 옛 기록은 멈춘다 · --accept_legacy_records 로만 받는다 (표시)")
        (ol / "anneal_results.json").write_text(json.dumps({"results": [
            {"name": "ar4", "xyz_input": str(x), "error": "옛 실패"}]}))
        rce, ne = run_batch([x], ol, P0, lj(), model="fake-lj", accept_legacy=True)
        chk(rce == 0 and ne == 1, "⑥ ⛔음성: 옛 판 실패 기록 ('error' 만) 은 --accept_legacy_records 여도 다시 돈다")

        chk(not check_results(ob / "anneal_results.json", expect_n=1, expect_time_ps=0, expect_temperature=500),
            "⑦ [양성] 결과 검사: 요청 (n 1 · 0 ps · 500 K) 과 같으면 문제 0")
        chk(any("time_ps" in p_ for p_ in check_results(ob / "anneal_results.json", expect_time_ps=20)),
            "⑦ ⛔음성: 요청 20 ps 인데 기록이 0 ps 면 잡는다 (실행기 시간 전달 검사 · Codex DU P1-4)")
        chk(any("기대" in p_ for p_ in check_results(ob / "anneal_results.json", expect_n=2)),
            "⑦ ⛔음성: 끝난 기록 수가 기대와 다르면 잡는다")
        chk(any("failed" in p_ for p_ in check_results(om / "anneal_results.json")),
            "⑦ ⛔음성: failed 기록이 있으면 잡는다")
        # ⑧ 2026-11-09 (Codex DV P1-2) — 완료 구조를 바꾸거나 지우면 결과 검사 · 재개가 잡는다
        rp = ob / "ar4" / "post_relax.xyz"
        keep_bytes = rp.read_bytes()
        write(rp, Atoms("He", positions=[[0, 0, 0]], cell=[5, 5, 5], pbc=True))
        pr = check_results(ob / "anneal_results.json", expect_n=1, require_converged=True)
        try:
            run_batch([x], ob, P0, lj(), model="fake-lj"); ok_ = False
        except SystemExit:
            ok_ = True
        chk(any("sha256" in q for q in pr) and ok_,
            "⑧ ⛔음성: post_relax.xyz 를 다른 조성으로 바꾸면 결과 검사 문제 · 재개는 멈춘다 (Codex 재현: [] · 실행 0 · 종료 0)")
        rp.unlink()
        pr2 = check_results(ob / "anneal_results.json", expect_n=1)
        try:
            run_batch([x], ob, P0, lj(), model="fake-lj"); ok2 = False
        except SystemExit:
            ok2 = True
        rc_r, n_r = run_batch([x], ob, P0, lj(), model="fake-lj", rerun_mismatched=True)
        chk(any("파일 없음" in q for q in pr2) and ok2 and rc_r == 0 and n_r == 1
            and not check_results(ob / "anneal_results.json", expect_n=1),
            "⑧ ⛔음성: 지우면 잡고 멈춘다 · --rerun_mismatched 로만 다시 돌아 결속이 회복된다")
        del keep_bytes
        # ⑨ 2026-11-09 (Codex DW P1-2 · P2) — 궤적 기록 · 기하 유효성
        ot = td / "traj"
        rc_t, _ = run_batch([x], ot, dict(P0, time_ps=0.004, log_every=1), lj(), model="fake-lj")
        rt = json.loads((ot / "anneal_results.json").read_text())["results"][0]
        mt = rt["outputs"].get("md_traj") or {}
        chk(rc_t == 0 and mt.get("n_frames") == 3 and mt.get("log_every_steps") == 1 and mt.get("n_steps") == 2
            and not verify_outputs(rt, ot),
            "⑨ [양성] 0.004 ps · dt 2 fs · 매 걸음 저장 → md_traj 기록 (프레임 3 = 2 // 1 + 1 · sha256) · 결과 검사 통과")
        bad_le = json.loads(json.dumps(rt)); bad_le["outputs"]["md_traj"]["log_every_steps"] = 2
        chk(any("프레임 수" in q for q in verify_outputs(bad_le, ot)),
            "⑨ ⛔음성: 기록의 저장 간격을 바꾸면 (1 → 2) 프레임 수가 안 맞아 잡는다 (간격을 명령줄로 받던 판독의 거울)")
        trp = ot / "ar4" / "md.traj"
        tb = trp.read_bytes()
        trp.write_bytes(tb + b"\0")
        chk(any("md_traj" in q and "sha256" in q for q in verify_outputs(rt, ot)),
            "⑨ ⛔음성: md.traj 를 바꾸면 sha256 으로 잡는다")
        trp.write_bytes(tb)
        rpx = ot / "ar4" / "post_relax.xyz"
        a_nan = read(str(rpx)); a_nan.positions[0, 0] = np.nan
        write(str(rpx), a_nan)
        rn = json.loads(json.dumps(rt)); rn["outputs"]["post_relax"]["sha256"] = _file_sha256(rpx)
        chk(any("NaN" in q for q in verify_outputs(rn, ot)),
            "⑨ ⛔음성: NaN 좌표 결과는 sha256 을 맞춰 줘도 잡는다 (Codex DW P2 — 옛 판독은 F_free 로 셌다)")
        a_sg = read(str(rpx)); a_sg.positions[0, 0] = 0.0; a_sg.cell[2] = [0.0, 0.0, 0.0]
        write(str(rpx), a_sg)
        rs_ = json.loads(json.dumps(rt)); rs_["outputs"]["post_relax"]["sha256"] = _file_sha256(rpx)
        chk(any("특이" in q for q in verify_outputs(rs_, ot)), "⑨ ⛔음성: 주기 셀 부피 0 (특이 셀) 결과도 잡는다")
        # ⑩ 2026-11-09 (Codex DX P1-1) — 실행 목적 (purpose): 줄 때만 정체성에 · 다르면 재개가 멈춤 · 결과 검사 대조
        kw = dict(temperature_K=500, time_ps=0, dt_fs=2.0, friction=0.01, relax_steps=500, relax_fmax=0.01,
                  cell_relax=False, seed=7, model="fake-lj")
        i0, i1 = run_identity(x, **kw), run_identity(x, purpose="b2o3_bo/stage8_anneal", **kw)
        chk("purpose" not in i0 and i1.get("purpose") == "b2o3_bo/stage8_anneal"
            and identity_sha(i0) == identity_sha({k: v for k, v in i1.items() if k != "purpose"}),
            "⑩ [양성] purpose 는 줄 때만 정체성에 들어간다 (안 주면 옛 정체성 · identity_sha 그대로)")
        op = td / "purp"
        rc_p, _ = run_batch([x], op, dict(P0, purpose="b2o3_bo/pilot_run"), lj(), model="fake-lj")
        try:
            run_batch([x], op, dict(P0, purpose="b2o3_bo/stage8_anneal"), lj(), model="fake-lj"); ok_ = False
        except SystemExit:
            ok_ = True
        chk(rc_p == 0 and ok_, "⑩ ⛔음성: 같은 이름 · 같은 입력이라도 실행 목적이 다르면 재개가 건너뛰지 않고 멈춘다")
        cp_ = op / "anneal_results.json"
        chk(not check_results(cp_, expect_n=1, expect_purpose="b2o3_bo/pilot_run")
            and any("실행 목적" in q for q in check_results(cp_, expect_purpose="b2o3_bo/stage8_anneal")),
            "⑩ ⛔음성: 결과 검사가 요청한 실행 목적과 기록을 대조한다 (같으면 문제 0 · 다르면 잡는다)")
        try:
            run_batch([x, td / "sub" / "ar4.xyz"], td / "dup", P0, lj(), model="fake-lj")
            ok_ = False
        except SystemExit:
            ok_ = True
        chk(ok_, "⑦ ⛔음성: 같은 이름 입력 둘은 출력 폴더가 겹쳐 멈춘다")
    r = subprocess.run([sys.executable, __file__, "--check_results", str(Path("/nonexistent/x.json"))],
                       capture_output=True, text=True)
    chk(r.returncode == 1, "⑦ ⛔음성: --check_results 실패는 종료코드 1 (실행기가 rc 로 본다)")
    print("  " + ("✅ selftest 통과" if ok[1] == ok[0] else
                  f"⛔ selftest 실패 {ok[0]-ok[1]}/{ok[0]}"))
    return 0 if ok[1] == ok[0] else 1


def main():
    # ⚠ `--selftest` 는 parse_args() **앞에서** 가로챈다 — `--out`/`--seed` 가 required 라
    #   그대로 두면 selftest 를 돌릴 수 없다 (watch_all.py 가 `-h` 로 똑같이 걸렸다).
    if "--selftest" in sys.argv[1:]:
        return _selftest()
    if "--check_results" in sys.argv[1:]:
        return _check_results_cli(sys.argv[1:])

    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--xyz', nargs='+',
                       help='xyz files to anneal (one or more)')
    parser.add_argument('--xyz_dir',
                       help='Directory of xyz files to anneal — recursive '
                            'glob "**/*.xyz". Use for "anneal ALL screening '
                            'candidates" mode since UMA pre-anneal ranking is '
                            'a heuristic and Pipeline Step 3 docs note '
                            'screening can re-order under anneal.')
    parser.add_argument('--summary_json',
                       help='Structures summary JSON (substitute_compound '
                            "output); pulls xyz_file from each entry's "
                            "'xyz_file' field. Alternative to --xyz_dir for "
                            'a specific batch.')
    parser.add_argument('--top_candidates',
                       help='analyze_screening top_candidates JSON; pulls '
                            'xyz_file path from each record')
    parser.add_argument('--top', type=int, default=5,
                       help='If --top_candidates: number of top entries to anneal')
    parser.add_argument('--per_compound_top', type=int, default=None,
                       help='Per-compound stratified Top-N anneal: groups the '
                            'input (from --summary_json or --uma_results) by '
                            "dopant, anneals the lowest-ΔE/atom N entries of "
                            "each group. Recommended for compound batches "
                            "where ranking is heavy-tailed (one strong cation "
                            "family dominates the global Top-N otherwise).")
    parser.add_argument('--uma_results',
                       help='UMA screening results JSON (has uma_relaxed.'
                            'de_per_atom_vs_baseline per record). Used as '
                            'sort key when --per_compound_top is set.')
    parser.add_argument('--light', action='store_true',
                       help='Light anneal preset (300K, 20 ps, 500 relax '
                            'steps) — for stratified per-compound Top-N to '
                            'cheaply relieve unphysical Li placement before '
                            'reranking. Override individual flags as needed.')
    parser.add_argument('--out', required=True, help='Output base directory')
    parser.add_argument('--temperature', type=float, default=500,
                       help='Annealing temperature in K (default 500; pipeline '
                            'doc cites Li hop Eₐ~0.2 eV, kT@500K=0.043 eV; '
                            'avoid >800K — Cl cage starts to break)')
    parser.add_argument('--time_ps', type=float, default=50,
                       help='MD duration in ps (default 50; 25 ps minimum '
                            'for Li sub-lattice equilibration)')
    parser.add_argument('--dt_fs', type=float, default=2.0,
                       help='MD time step in fs')
    parser.add_argument('--friction', type=float, default=0.01,
                       help='Langevin friction (ase units)')
    parser.add_argument('--relax_steps', type=int, default=1500,
                       help='Post-MD FIRE max steps (default 1500 to match '
                            'compound-substitution screening)')
    parser.add_argument('--relax_fmax', type=float, default=0.05)
    parser.add_argument('--no_cell_relax', action='store_true',
                       help='Position-only final relax (fix cell)')
    parser.add_argument('--device', default='cuda')
    parser.add_argument('--task', default='omat')
    parser.add_argument('--log_every', type=int, default=500,
                       help='MD log interval (steps)')
    # ⛔ 회신 AL P0-3 — seed 는 **필수**다. 기본값을 두면 안 준 것과 준 것이 구분 안 되고,
    #   정본 CSV 가 정확히 그 상태(seed 미기록)라 복제본이 서로 다른 endpoint 로 갔다.
    parser.add_argument('--seed', type=int, required=True,
                       help='Langevin·초기속도 RNG seed. **필수** — 이게 없으면 '
                            'anneal 이 비결정적이라 같은 입력이 다른 endpoint 로 간다 '
                            '(2026-08-30 회신 AL P0-3). 결과 json 에 기록된다.')
    parser.add_argument('--rerun_mismatched', action='store_true',
                       help='완료 기록의 결과 파일이 없거나 바뀌었으면 다시 돌린다 (기본은 멈춤 · 2026-11-09)')
    parser.add_argument('--accept_legacy_records', action='store_true',
                       help='정체성 없는 옛 결과 기록을 끝난 것으로 받는다 (표시됨 · 기본은 멈춤 · 2026-11-09)')
    parser.add_argument('--purpose', default=None,
                        help='실행 목적 (예 b2o3_bo/pilot_run · b2o3_bo/stage8_anneal) — 정체성에 기록하고 판독기가 '
                             '단계마다 대조한다 (2026-11-09 Codex DX P1-1 · 안 주면 정체성에 넣지 않는다)')
    parser.add_argument('--selftest', action='store_true')
    parser.add_argument('--check_results', help='결과 json 검사만 (--expect_n · --expect_time_ps · '
                                               '--expect_temperature · --require_converged · --expect_purpose) — 먼저 가로챈다')
    args = parser.parse_args()

    if not args.xyz and not args.top_candidates and not args.summary_json and not args.xyz_dir:
        parser.error("Provide --xyz files, --xyz_dir, --top_candidates, or --summary_json JSON")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # Build xyz list (multiple input modes)
    if args.xyz:
        xyz_paths = [Path(p) for p in args.xyz]
    elif args.xyz_dir:
        xyz_paths = sorted(Path(args.xyz_dir).rglob('*.xyz'))
        # Filter out anneal-produced (post_md.xyz, post_relax.xyz) to avoid
        # re-annealing our own outputs if --xyz_dir overlaps --out
        xyz_paths = [p for p in xyz_paths
                     if p.name not in ('post_md.xyz', 'post_relax.xyz')]
        print(f"  Discovered {len(xyz_paths)} xyz files under {args.xyz_dir}")
    elif args.summary_json:
        data = json.loads(Path(args.summary_json).read_text())
        # Accept the key conventions used by upstream tools:
        #   substitute_compound output → {'structures': [...]}
        #   run_uma_screening output   → {'results':    [...]}
        #   select_winners output      → {'winners':    [...]}  (cascade Stage 03)
        recs = (data.get('winners')
                or data.get('structures')
                or data.get('results', [])
                if isinstance(data, dict) else data)
        xyz_paths = [Path(r['xyz_file']) for r in recs
                     if 'xyz_file' in r and Path(r['xyz_file']).exists()]
        print(f"  Loaded {len(xyz_paths)} xyz from summary {args.summary_json}")
    elif args.top_candidates:
        data = json.loads(Path(args.top_candidates).read_text())
        top = data.get('top_candidates', [])[:args.top]
        xyz_paths = []
        for entry in top:
            xpath = entry.get('xyz_file')
            if xpath and Path(xpath).exists():
                xyz_paths.append(Path(xpath))
            else:
                print(f"  ⚠ skip {entry.get('name')}: xyz_file not found "
                      f"({xpath})")
    else:
        parser.error("Provide --xyz, --xyz_dir, --summary_json, or --top_candidates")
    if not xyz_paths:
        raise SystemExit("No xyz files found")

    # Per-compound stratified Top-N filter
    if args.per_compound_top:
        if not args.uma_results:
            parser.error("--per_compound_top requires --uma_results "
                        "(needs ΔE/atom for ranking within each dopant group)")
        uma = json.loads(Path(args.uma_results).read_text())['results']
        # Map xyz path → ΔE/atom + dopant
        name_to_xpath = {winner_name(p): p for p in xyz_paths}
        from collections import defaultdict
        groups = defaultdict(list)
        for rec in uma:
            name = rec.get('name')
            if name in name_to_xpath:
                groups[rec.get('dopant', 'unknown')].append((
                    rec['uma_relaxed']['de_per_atom_vs_baseline'],
                    name_to_xpath[name],
                ))
        filtered: list = []
        for dop, items in groups.items():
            items.sort()  # ascending ΔE → most stable first
            keep = items[:args.per_compound_top]
            filtered.extend(p for _, p in keep)
            print(f"  per-compound Top-{args.per_compound_top}: {dop} → "
                  f"{len(keep)}/{len(items)}")
        xyz_paths = filtered
        print(f"  Stratified Top-{args.per_compound_top}: "
              f"{len(xyz_paths)} structures across {len(groups)} dopants")

    # --light preset
    if args.light:
        args.temperature = min(args.temperature, 300)
        args.time_ps = min(args.time_ps, 20)
        args.relax_steps = min(args.relax_steps, 500)
        print(f"  --light preset: T={args.temperature}K, "
              f"t={args.time_ps}ps, relax steps={args.relax_steps}")

    print(f"Loading UMA-s-1p1 ({args.device})...")
    calc = load_uma_calc(args.device, args.task)

    P = dict(temperature_K=args.temperature, time_ps=args.time_ps, dt_fs=args.dt_fs,
             friction=args.friction, relax_steps=args.relax_steps, relax_fmax=args.relax_fmax,
             cell_relax=not args.no_cell_relax, log_every=args.log_every, seed=args.seed,
             purpose=args.purpose)
    t_start = time.time()
    rc, n_ran = run_batch(xyz_paths, out, P, calc, model=f'uma-s-1p1/{args.task}',
                          accept_legacy=args.accept_legacy_records, rerun_mismatched=args.rerun_mismatched)
    results_path = out / 'anneal_results.json'
    results = json.loads(results_path.read_text()).get('results', [])

    # Final summary
    print(f"\n{'='*78}")
    print(f"{'Champion':<35}{'E_pre':>10}{'E_post':>10}{'ΔE meV/at':>12}{'status':>11}")
    print('-' * 78)
    for r in sorted([x for x in results if x.get('status') in ('converged', 'unconverged')],
                   key=lambda x: x.get('delta_E_anneal_meV_per_atom', 0)):
        nat = r.get('n_atoms', 1)
        ep = r.get('E_pre_anneal', 0) / nat
        epo = r.get('E_post_relax', 0) / nat
        de = r.get('delta_E_anneal_meV_per_atom', 0)
        print(f"{r['name']:<35}{ep:>+10.4f}{epo:>+10.4f}{de:>+10.1f}{r['status']:>13}")
    for r in results:
        if r.get('status') == 'failed' or 'error' in r:
            print(f"{r['name']:<35}  ❌ failed — {str(r.get('error'))[:60]}")
    print('=' * 78)
    print(f"Total: {time.time() - t_start:.1f}s · 이번에 돈 구조 {n_ran} · 종료코드 {rc}")
    print(f"Results: {results_path}")
    return rc


if __name__ == '__main__':
    sys.exit(main())
