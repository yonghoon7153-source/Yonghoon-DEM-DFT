#!/usr/bin/env python3
"""build_comsol_mph.py — comsol_pkg(스키마 v1.0) → COMSOL 모델 생성기 (Track-B 하이브리드).

이 컨테이너/일반 개발머신에는 COMSOL 이 없다 — .mph 는 COMSOL 라이선스 없이 만들 수 없으므로
1차 산출물은 "라이선스 머신에서 1커맨드로 .mph 를 낳는" model_build.java + README_run.md 다.
--mph 는 MPh(pymph) 런타임 경로(= COMSOL 설치 머신에서 java 텍스트와 같은 빌드 스텝을 라이브
재생) — mph 미설치면 명확한 안내 후 java 경로를 권고하고 정상 종료한다(크래시 금지).

물리 결정(2026-08-05 사용자 확정 — 변경 금지):
  · AM 구 = 해상 기하 / SE = 연속체(κ_dom) / VGCF = 1D Edge(단면 π(0.075µm)²) /
    AM-AM 넥 = DEM δ → form UNION 렌즈 (목반경 √(2R*δ)=√2·a_hertz, 면적 2×Hertz) /
    PTFE = 기하 금지(차단 효과는 κ_dom·f_cov 에 이미 반영).
  · ★ single-ion: LPSCl t⁺≈1 → 농도분극이 물리적으로 없다.  DFN 류 인터페이스 금지.
  · κ_dom 이중계상 가드: 하이브리드는 AM 을 기하로 해상하므로 SE 연속체 전도도는
    σ_bulk·(φ_full/τ_full)/(φ_geo/τ_geo) = κ_dom 이어야 한다 (τ 선형 관례 —
    build_tau_regime_db 의 √=τ² 관례와 혼동 금지).

설계:
  · 모든 수치는 python 이 java 에 직접 굽는다 — COMSOL 이 CSV 를 읽게 하지 않는다(이식성).
  · 빌드는 IR(스텝 리스트) 하나로 표현 → java 텍스트 방출과 --mph 라이브 재생이 같은
    소스에서 나온다(이중 구현 드리프트 방지).
  · §F1 날조 금지: 패키지에 null 인 값은 파라미터를 만들지 않고 java 주석
    "TODO(trackb): <이름> — 패키지에 null, reason: ..." 로 남긴다.  'null 문자열'(None/nan)이
    java 로 새면 생성 단계에서 즉시 실패한다.

CLI:
  python3 scripts/build_comsol_mph.py <pkg_dir> [--out DIR] [--mph]
  python3 scripts/build_comsol_mph.py --selftest
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import re
import sys
import datetime as _dt
from pathlib import Path

SCHEMA_VERSION = '1.0'          # comsol_pkg 계약 버전 (익스포터와 공유)
GENERATOR = 'build_comsol_mph.py'
TAU_CONVENTION = 'linear: sigma_eff = sigma_bulk*phi/tau'

# VGCF 물성 기본값 — vgcf_fibres.csv 헤더 주석(diameter_um=, sigma_S_cm=)이 있으면 그 값이
# 우선한다.  0.15µm/100 S/cm 는 step3_sigma.py 의 생산 정본과 같은 축.
VGCF_DIAMETER_UM_DEFAULT = 0.15
VGCF_SIGMA_S_CM_DEFAULT = 100.0

# electrochem.json 필드 → (java 파라미터명, 단위 접미사, 설명) — 스키마 v1.0 계약 그대로.
# T_C 는 K 파생까지 따로 처리.
_ECHEM_PARAM_MAP = [
    ('i0_A_m2',        'i0',        '[A/m^2]',    'exchange current density (BV, B2)'),
    ('alpha_a',        'alpha_a',   '',           'anodic transfer coefficient'),
    ('alpha_c',        'alpha_c',   '',           'cathodic transfer coefficient'),
    ('D_s_m2_s',       'D_s',       '[m^2/s]',    'solid diffusivity (B2 sphere diffusion)'),
    ('c_max_mol_m3',   'c_max',     '[mol/m^3]',  'max Li concentration in AM'),
    ('x0',             'x0',        '',           'stoichiometry at 0% SOC'),
    ('x100',           'x100',      '',           'stoichiometry at 100% SOC'),
    ('asr_film_ohm_m2', 'ASR_film', '[ohm*m^2]',  'interfacial film ASR'),
    ('r_int_ohm_cm2',  'R_int',     '[ohm*cm^2]', 'cell-level internal resistance'),
]


# ───────────────────────────── 패키지 로더 (스키마 v1.0 계약) ─────────────────────────────

def _read_csv_rows(path: Path):
    """'#' 주석 헤더를 걷어낸 DictReader 행 + 주석 라인 원문을 함께 돌려준다.

    스키마가 CSV 헤더 주석에 물성(예: vgcf diameter_um=0.15)을 싣는 계약이라 주석도 데이터다.
    """
    comments, body = [], []
    for line in path.read_text(encoding='utf-8').splitlines():
        (comments if line.lstrip().startswith('#') else body).append(line)
    rows = []
    if body:
        rdr = csv.DictReader(io.StringIO('\n'.join(body)))
        rows = [r for r in rdr if r and any((v or '').strip() for v in r.values())]
    return rows, comments


def _fnum(v, ctx):
    """CSV 문자열 → float.  빈 값/파싱 불가는 §F1 위반 데이터이므로 즉시 실패."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        raise ValueError(f'comsol_pkg 계약 위반: {ctx} 값 {v!r} 을 숫자로 읽을 수 없음')
    if not math.isfinite(f):
        raise ValueError(f'comsol_pkg 계약 위반: {ctx} 가 비유한값({v!r})')
    return f


def _comment_kv(comments, key):
    """헤더 주석에서 key=value 를 찾는다 (없으면 None)."""
    pat = re.compile(re.escape(key) + r'\s*=\s*([0-9.eE+-]+)')
    for line in comments:
        m = pat.search(line)
        if m:
            return float(m.group(1))
    return None


def load_pkg(pkg_dir: Path) -> dict:
    """comsol_pkg 디렉토리를 스키마 v1.0 그대로 읽는다.  파일·필드명은 익스포터와의 계약."""
    pkg_dir = Path(pkg_dir)
    if not pkg_dir.is_dir():
        raise FileNotFoundError(f'패키지 디렉토리가 아님: {pkg_dir}')
    warnings = []

    man_p = pkg_dir / 'manifest.json'
    manifest = json.loads(man_p.read_text(encoding='utf-8')) if man_p.exists() else {}
    if not man_p.exists():
        warnings.append('manifest.json 없음 — case 명은 디렉토리명에서 유추')
    if manifest.get('schema_version') not in (None, SCHEMA_VERSION):
        warnings.append(f"manifest schema_version {manifest.get('schema_version')!r} ≠ "
                        f'{SCHEMA_VERSION} — 필드 어긋남 가능, 계속 진행')
    case = manifest.get('case') or pkg_dir.name.replace('comsol_pkg_', '') or 'case'

    # am_spheres.csv — 필수
    sph_p = pkg_dir / 'am_spheres.csv'
    if not sph_p.exists():
        raise FileNotFoundError(f'am_spheres.csv 없음 (스키마 필수): {sph_p}')
    rows, _ = _read_csv_rows(sph_p)
    spheres = []
    for r in rows:
        cls = (r.get('cls') or '').strip()
        if cls not in ('AM_P', 'AM_S'):
            raise ValueError(f"am_spheres.csv cls={cls!r} — 스키마는 AM_P|AM_S 만 허용 (id={r.get('id')})")
        spheres.append({
            'id': str(r.get('id')).strip(),
            'x': _fnum(r.get('x_um'), 'am_spheres.x_um'),
            'y': _fnum(r.get('y_um'), 'am_spheres.y_um'),
            'z': _fnum(r.get('z_um'), 'am_spheres.z_um'),
            'r': _fnum(r.get('r_um'), 'am_spheres.r_um'),
            'cls': cls,
            'sigma_e_S_cm': _fnum(r.get('sigma_e_S_cm'), 'am_spheres.sigma_e_S_cm'),
            'f_cov_reaction': _fnum(r.get('f_cov_reaction'), 'am_spheres.f_cov_reaction'),
            'f_cov_carbon': _fnum(r.get('f_cov_carbon'), 'am_spheres.f_cov_carbon'),
            'f_cov_block': _fnum(r.get('f_cov_block'), 'am_spheres.f_cov_block'),
            'f_cov_source': (r.get('f_cov_source') or '').strip(),
        })
    if not spheres:
        raise ValueError('am_spheres.csv 에 데이터 행이 없음 — 하이브리드 기하를 만들 수 없다')

    # am_am_contacts.csv — README 교차대조용 (기하 넥은 union 이 만든다)
    contacts = []
    con_p = pkg_dir / 'am_am_contacts.csv'
    if con_p.exists():
        crow, _ = _read_csv_rows(con_p)
        for r in crow:
            contacts.append({'i': str(r.get('i')).strip(), 'j': str(r.get('j')).strip(),
                             'delta_um': _fnum(r.get('delta_um'), 'contacts.delta_um'),
                             'a_hertz_um': _fnum(r.get('a_hertz_um'), 'contacts.a_hertz_um'),
                             'g_holm_S': _fnum(r.get('g_holm_S'), 'contacts.g_holm_S'),
                             # v1.1 추가 — 없으면 None (구 pkg 호환).  repair tol 판단에 필수.
                             'gap_um': (_fnum(r.get('gap_um'), 'contacts.gap_um')
                                        if r.get('gap_um') not in (None, '') else None)})
    else:
        warnings.append('am_am_contacts.csv 없음 — Holm g 교차대조 표는 생략')

    # vgcf_fibres.csv — 데이터 없으면 헤더만 (manifest.notes 에 사유) 이 계약
    fibres, vgcf_meta = {}, {'diameter_um': VGCF_DIAMETER_UM_DEFAULT,
                             'sigma_S_cm': VGCF_SIGMA_S_CM_DEFAULT, 'from_header': False}
    vg_p = pkg_dir / 'vgcf_fibres.csv'
    if vg_p.exists():
        vrows, vcomments = _read_csv_rows(vg_p)
        d = _comment_kv(vcomments, 'diameter_um')
        s = _comment_kv(vcomments, 'sigma_S_cm')
        if d is not None:
            vgcf_meta.update(diameter_um=d, from_header=True)
        if s is not None:
            vgcf_meta.update(sigma_S_cm=s, from_header=True)
        for r in vrows:
            fid = str(r.get('fibre_id')).strip()
            fibres.setdefault(fid, []).append((
                int(float(r.get('seq'))),
                _fnum(r.get('x_um'), 'vgcf.x_um'),
                _fnum(r.get('y_um'), 'vgcf.y_um'),
                _fnum(r.get('z_um'), 'vgcf.z_um')))
        for fid in fibres:
            fibres[fid] = [p[1:] for p in sorted(fibres[fid])]
    else:
        warnings.append('vgcf_fibres.csv 없음 — VGCF 절은 전부 주석 처리')

    # se_domain.json — 필수 (SE 연속체 = 하이브리드의 반쪽)
    se_p = pkg_dir / 'se_domain.json'
    if not se_p.exists():
        raise FileNotFoundError(f'se_domain.json 없음 (스키마 필수): {se_p}')
    se = json.loads(se_p.read_text(encoding='utf-8'))
    if se.get('tau_convention') not in (None, TAU_CONVENTION):
        warnings.append(f"se_domain.tau_convention {se.get('tau_convention')!r} ≠ 선형 관례 — "
                        'κ_dom 해석이 √=τ² 관례와 섞였는지 확인 필요')

    # electrochem.json — null 허용 (§F1: null + provenance.reason)
    ec_p = pkg_dir / 'electrochem.json'
    echem = json.loads(ec_p.read_text(encoding='utf-8')) if ec_p.exists() else {}
    if not ec_p.exists():
        warnings.append('electrochem.json 없음 — B2(BV) 파라미터 전부 TODO 처리')

    return {'dir': pkg_dir, 'case': case, 'manifest': manifest, 'spheres': spheres,
            'contacts': contacts, 'fibres': fibres, 'vgcf_meta': vgcf_meta,
            'se': se, 'echem': echem, 'warnings': warnings}


# ───────────────────────────── IR: 빌드 스텝 (java 방출 + mph 재생 공용) ─────────────────────────────
# step 종류:
#   ('comment', text)                — java // 주석.  mph 재생은 건너뜀.
#   ('blank',)                       — 빈 줄.
#   ('call', [(method, args), ...])  — model.<m1>(a1).<m2>(a2)...;  체인 각 원소가 순서대로 호출.
#   ('tryblock', label, [steps])     — java try/catch, mph 재생 try/except (솔브 실패에도 .mph 저장).

def _jstr(s: str) -> str:
    """java 문자열 리터럴 — 비ASCII 는 \\uXXXX 로 (컴파일 인코딩 사고 방지: 코드 문자열은 ASCII 만)."""
    out = []
    for ch in str(s):
        if ch == '\\':
            out.append('\\\\')
        elif ch == '"':
            out.append('\\"')
        elif 32 <= ord(ch) < 127:
            out.append(ch)
        else:
            out.append('\\u%04x' % ord(ch))
    return '"' + ''.join(out) + '"'


def _jnum(v) -> str:
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, int):
        return str(v)
    f = float(v)
    if not math.isfinite(f):
        raise ValueError(f'비유한 수치를 java 로 방출하려 함: {v!r}')
    return f'{f:.9g}'


def _jarg(a) -> str:
    if isinstance(a, str):
        return _jstr(a)
    if isinstance(a, bool) or isinstance(a, (int, float)):
        return _jnum(a)
    if isinstance(a, tuple) and len(a) == 2 and a[0] == 'S[]':
        return 'new String[]{' + ', '.join(_jstr(x) for x in a[1]) + '}'
    if isinstance(a, tuple) and len(a) == 2 and a[0] == 'D[]':
        return 'new double[]{' + ', '.join(_jnum(x) for x in a[1]) + '}'
    if isinstance(a, tuple) and len(a) == 2 and a[0] == 'S[][]':
        inner = ', '.join('{' + ', '.join(_jstr(x) for x in row) + '}' for row in a[1])
        return 'new String[][]{' + inner + '}'
    raise TypeError(f'java 인자 타입 미지원: {a!r}')


def _emit_call(chain) -> str:
    parts = ['model']
    for method, args in chain:
        parts.append(f'{method}(' + ', '.join(_jarg(a) for a in args) + ')')
    return '.'.join(parts) + ';'


#: 한 part 메서드가 담을 최대 "문장" 수 (주석/공백은 바이트코드 0 이라 세지 않는다).
#  JVM 은 메서드당 Code 속성을 65,535 바이트로 제한한다 (JVMS §4.7.3).  이 생성기의 문장은
#  대략 40–90 B/문장(배열 인자가 있는 set 이 제일 큼) → 300 문장 ≈ 12–27 KB 로 넉넉히 안쪽.
#  ★ 왜 필요한가: real_14(스피어 457) 는 한 메서드에 9,737 문장이 되어 javac 이
#  "code too large" 로 거부한다 — comsol batch 는 java 를 내부 컴파일하므로 모델이 아예
#  안 열린다.  스피어 수에 선형으로 늘어나므로 분할은 선택이 아니라 필수.
_MAX_STMTS_PER_PART = 300

#: 클래스 하나의 constant pool 은 65,535 엔트리다 (JVMS §4.1).  실측(real_14, 스피어 457):
#  CP 12,349 = 스피어당 ≈ 27 엔트리 → 한 클래스에 담을 수 있는 스피어는 약 2,400 개.
#  (예전 수동 모델 ≈1,767 구는 아슬아슬하게 그 아래였다.)  넘어가면 javac 이
#  "too many constants" 로 거부한다 — part 분할로는 못 푼다(CP 는 클래스 단위).
_CP_ENTRIES_PER_SPHERE = 27.0
_SPHERE_SOFT_CAP = 1800          # 경고 (CP ≈ 74 %)
_SPHERE_HARD_CAP = int(65535 / _CP_ENTRIES_PER_SPHERE)   # ≈ 2427 — 이 위는 컴파일 실패 예상


def _split_steps(steps, limit: int = _MAX_STMTS_PER_PART):
    """IR 스텝을 part 별로 쪼갠다.  주석/공백 경계에서 끊어 문맥이 흩어지지 않게 하고,
    tryblock 은 통째로 한 part 안에 둔다 (블록 중간 분할은 문법이 깨진다)."""
    parts, cur, cost = [], [], 0
    for st in steps:
        boundary = st[0] in ('comment', 'blank')
        if cur and ((cost >= limit and boundary) or cost >= 2 * limit):
            parts.append(cur)
            cur, cost = [], 0
        cur.append(st)
        if st[0] == 'call':
            cost += 1
        elif st[0] == 'tryblock':
            cost += 2 + sum(1 for s in st[2] if s[0] == 'call')
    if cur:
        parts.append(cur)
    return parts


def render_java(steps, header_comment: str, class_name: str = 'model_build') -> str:
    """IR → COMSOL java model file 텍스트.

    골격: `public static Model run()` 이 모델을 만들고 `partN(model)` 들을 순서대로 호출.
    분할 이유는 _MAX_STMTS_PER_PART 주석 참조 (메서드 64 KB 한도)."""
    L = []
    L.append('/*')
    for ln in header_comment.splitlines():
        # '*/' 는 블록주석 조기 종료, 백슬래시는 주석 안 \uXXXX 해석 사고 — 둘 다 무해화
        L.append(' * ' + ln.replace('*/', '* /').replace('\\', '/'))
    L.append(' */')
    L.append('')
    L.append('import com.comsol.model.*;')
    L.append('import com.comsol.model.util.*;')
    L.append('')
    L.append(f'public class {class_name} ' + '{')
    L.append('')

    parts = _split_steps(steps)
    L.append('  // 모델 조립은 partN(model) 로 쪼개져 있다 — JVM 메서드 Code 한도(64 KB) 때문.')
    L.append(f'  // 문장 {sum(1 for s in steps if s[0] == "call")} 개 → part {len(parts)} 개.')
    L.append('  // 순서가 곧 빌드 순서다 (기하 → 선택 → 재료 → 물리 → 메시 → 스터디).')
    L.append('  public static Model run() {')
    L.append('    Model model = ModelUtil.create("Model");')
    for i in range(len(parts)):
        L.append(f'    part{i}(model);')
    L.append('    return model;')
    L.append('  }')
    L.append('')

    def emit(sts, ind):
        for st in sts:
            if st[0] == 'blank':
                L.append('')
            elif st[0] == 'comment':
                for ln in st[1].splitlines():
                    # javac 은 주석 안에서도 \uXXXX 를 해석한다 — 외부 유입 텍스트(reason 등)의
                    # 백슬래시가 illegal unicode escape 컴파일 에러를 만들 수 있어 무해화
                    L.append(ind + '// ' + ln.replace('\\', '/'))
            elif st[0] == 'call':
                L.append(ind + _emit_call(st[1]))
            elif st[0] == 'tryblock':
                L.append(ind + 'try {')
                emit(st[2], ind + '  ')
                L.append(ind + '} catch (Exception e) {')
                L.append(ind + f'  System.out.println("[trackb] {st[1]} failed: " + e.getMessage());')
                L.append(ind + '}')
            else:
                raise ValueError(f'IR 스텝 미지원: {st[0]}')

    for i, part in enumerate(parts):
        L.append(f'  private static void part{i}(Model model) ' + '{')
        emit(part, '    ')
        L.append('  }')
        L.append('')

    L.append('  public static void main(String[] args) {')
    L.append('    run();')
    L.append('  }')
    L.append('}')
    text = '\n'.join(L) + '\n'

    # 생성 단계 자기검수 (§F1 가드): null 문자열 누출·중괄호 불균형은 여기서 즉시 실패
    for bad in ('None', 'NaN', 'nan'):
        if re.search(r'(?<![A-Za-z_])' + bad + r'(?![A-Za-z_])', text):
            raise ValueError(f'java 산출물에 {bad!r} 누출 — 생성기 버그 (§F1)')
    bal = 0
    for ch in text:
        bal += (ch == '{') - (ch == '}')
        if bal < 0:
            raise ValueError('java 중괄호 균형 붕괴 (닫힘 과잉)')
    if bal != 0:
        raise ValueError(f'java 중괄호 불균형: {bal}')
    return text


# ───────────────────────────── 빌드 스텝 구성 (모델 본체) ─────────────────────────────

def _pname(sid: str) -> str:
    """스피어 id → 파라미터명에 안전한 토큰 (java/COMSOL 파라미터명 제약)."""
    return re.sub(r'[^0-9A-Za-z]', '_', sid)


def _protrusion(spheres, Lx, Ly, Lz):
    """박스 밖으로 삐져나온 스피어 통계 (클립 판단·README 표용).

    구형 캡 체적 = π·h²·(3r−h)/3, h = 평면 밖으로 나간 깊이.  두 면을 동시에 넘는
    극단(작은 박스)은 캡을 단순 합산해 과대평가하나, 판단(=0 인가 아닌가)에는 영향 없다."""
    n_lat = n_z = n_any = 0
    v_out = v_tot = 0.0
    for s in spheres:
        r = float(s['r'])
        d = (r - float(s['x']), float(s['x']) + r - Lx,
             r - float(s['y']), float(s['y']) + r - Ly,
             r - float(s['z']), float(s['z']) + r - Lz)
        lat, zz = any(v > 0 for v in d[:4]), any(v > 0 for v in d[4:])
        n_lat += lat; n_z += zz; n_any += (lat or zz)
        for h in d:
            h = min(max(h, 0.0), 2.0 * r)
            v_out += math.pi * h * h * (3.0 * r - h) / 3.0
        v_tot += 4.0 / 3.0 * math.pi * r ** 3
    box = Lx * Ly * Lz
    return {'n_lat': n_lat, 'n_z': n_z, 'n_any': n_any, 'v_out_um3': v_out,
            'pct_of_am': 100.0 * v_out / v_tot if v_tot > 0 else 0.0,
            'pct_of_box': 100.0 * v_out / box if box > 0 else 0.0}


def build_steps(pkg: dict, clip: str = 'auto'):
    """패키지 → (IR 스텝, TODO(trackb) 목록, 컨텍스트).  모든 수치는 여기서 java 로 구워진다.

    clip: 'auto'(삐져나온 구가 있으면 클립) | 'on' | 'off' — RVE 클립 절 참조."""
    steps, todos = [], []
    se, echem, spheres = pkg['se'], pkg['echem'], pkg['spheres']

    def C(text):
        steps.append(('comment', text))

    def CALL(*chain):
        steps.append(('call', list(chain)))

    def BLANK():
        steps.append(('blank',))

    def TODO(text):
        todos.append(text)
        C('TODO(trackb): ' + text)

    # ── 기하 박스: box_um 이 정본, thickness_um 은 대조용 ──
    box = se.get('box_um')
    if not (isinstance(box, (list, tuple)) and len(box) == 3):
        raise ValueError(f'se_domain.box_um 이 [x,y,z] 가 아님: {box!r}')
    Lx, Ly, Lz = (float(v) for v in box)
    thickness = se.get('thickness_um')

    # ── SE 연속체 전도도 결정 (κ_dom 우선; §F1 — 없으면 날조 대신 명시적 폴백/TODO) ──
    kdom_S_m = se.get('kappa_dom_S_m')
    if kdom_S_m is None and se.get('kappa_dom_S_cm') is not None:
        kdom_S_m = float(se['kappa_dom_S_cm']) * 100.0   # S/cm → S/m (×100)
    sigma_bulk = se.get('sigma_bulk_ion_S_cm')
    se_sigma_S_m, se_sigma_origin = None, None
    if kdom_S_m is not None:
        se_sigma_S_m, se_sigma_origin = float(kdom_S_m), 'kappa_dom'
    elif sigma_bulk is not None:
        se_sigma_S_m, se_sigma_origin = float(sigma_bulk) * 100.0, 'sigma_bulk_fallback'

    # ── 클래스별 AM σ_e (S/cm → S/m ×100).  스피어별 편차는 주석으로 정직하게 ──
    cls_sigma = {}
    for cls in ('AM_P', 'AM_S'):
        vals = [s['sigma_e_S_cm'] for s in spheres if s['cls'] == cls]
        if vals:
            cls_sigma[cls] = {'mean_S_cm': sum(vals) / len(vals),
                              'min': min(vals), 'max': max(vals), 'n': len(vals)}

    # ═══════════ Parameters ═══════════
    C('══ Parameters — 모든 수치는 comsol_pkg 에서 python 이 구웠다 (CSV 직접 읽기 금지) ══')
    CALL(('param', ()), ('set', ('V_app', '1[V]', 'applied plate potential (B1 sigma probe)')))
    CALL(('param', ()), ('set', ('L_x', f'{Lx:.9g}[um]', 'electrode box x (se_domain.box_um)')))
    CALL(('param', ()), ('set', ('L_y', f'{Ly:.9g}[um]', 'electrode box y')))
    CALL(('param', ()), ('set', ('L_z', f'{Lz:.9g}[um]', 'electrode box z = plate-to-plate')))
    CALL(('param', ()), ('set', ('A_xy', 'L_x*L_y', 'plate area')))
    if thickness is not None and abs(float(thickness) - Lz) > 1e-6:
        C(f'주의: se_domain.thickness_um = {float(thickness):.6g} ≠ box z {Lz:.6g} — 상단 void 캡'
          '\n포함 여부 차이.  σ_eff 정의는 plate-to-plate(L_z) 기준; STEP3 과 대조 시 두께 규약 통일 필요.')

    if se_sigma_S_m is not None:
        origin_txt = ('kappa_dom (= sigma_bulk*(phi_full/tau_full)/(phi_geo/tau_geo), '
                      'AM-장애물 굴곡도 이중계상 제거 완료)' if se_sigma_origin == 'kappa_dom'
                      else 'sigma_bulk 폴백')
        if se.get('sigma_bulk_source'):
            # 심화리뷰: 25°C 상수 폴백 출처가 java/README 에서 소실되던 것 — 킷 측정값 아님을 명시
            origin_txt += f" [σ_bulk={se['sigma_bulk_source']} — 킷 측정값 아님]"
        C('SE 연속체 이온 전도도 [S/m] — 출처: ' + origin_txt)
        C(f'tau 관례: {TAU_CONVENTION}  (√=τ² 관례와 혼동 금지 — 같은 해가 τ=4 ↔ 2 로 갈린다)')
        if se_sigma_origin == 'sigma_bulk_fallback':
            TODO('kappa_dom 이 패키지에 null → sigma_bulk 를 임시 사용.  AM-장애물 굴곡도는 기하가'
                 '\n  스스로 만들지만 SE 내부 pore 희석(phi_full/tau_full)이 빠져 σ_ion 과대예측 —'
                 '\n  익스포터에서 kdom_calibration 채워 재생성 권장')
        CALL(('param', ()), ('set', ('kdom_S_m', f'{se_sigma_S_m:.9g}[S/m]',
                                     'SE continuum ionic conductivity')))
    else:
        # 리뷰 minor: 익스포터는 실제 사유를 se_domain 최상위 'reason' 문자열에 기록한다
        # (trackb 부재/의도적 null 경로) — 일반문구로 대체하면 사유 충실도가 유실된다
        _ser = se.get('reason')
        reason = (_ser if isinstance(_ser, str) and _ser
                  else 'se_domain.kappa_dom_*/sigma_bulk_ion_S_cm 모두 null')
        mp = se.get('mixed_phase')
        if isinstance(mp, dict) and mp.get('reason'):
            reason += f" (mixed_phase.reason: {mp['reason']})"
        TODO('kdom_S_m — 패키지에 null, reason: '
             + __import__('re').sub(r'\b(None|NaN|nan)\b', 'null', str(reason))
             + '.  SE 재료가 비어 ec2 는 솔브 불가')
    if se.get('kdom_ratio') is not None and float(se['kdom_ratio']) > 1.0:
        C(f"경고: kdom_ratio = {float(se['kdom_ratio']):.4g} > 1 — 규약/입력 불일치 신호"
          '\n(AM-장애물 굴곡도보다 좋은 유효전도?).  익스포터 로그 확인.')

    for cls, tag in (('AM_P', 'sigma_e_AMP_S_m'), ('AM_S', 'sigma_e_AMS_S_m')):
        if cls in cls_sigma:
            cs = cls_sigma[cls]
            C(f'{cls} 전자 전도도: am_spheres.sigma_e_S_cm 클래스 평균 {cs["mean_S_cm"]:.6g} S/cm'
              f' × 100 = S/m  (n={cs["n"]}, 범위 {cs["min"]:.4g}..{cs["max"]:.4g} S/cm)')
            if cs['max'] > cs['min'] * 1.01:
                TODO(f'{cls} 스피어별 σ_e 가 균일하지 않음 — 필요 시 per-sphere 재료 분리 (지금은 클래스 평균)')
            CALL(('param', ()), ('set', (tag, f'{cs["mean_S_cm"] * 100.0:.9g}[S/m]',
                                         f'{cls} electronic conductivity (class mean)')))
    BLANK()

    # electrochem.json — null 은 파라미터를 만들지 않는다 (§F1)
    C('── electrochem.json (B2 BV 준비 파라미터; null 은 §F1 에 따라 파라미터 미생성) ──')
    prov = echem.get('provenance') if isinstance(echem.get('provenance'), dict) else {}

    def _pkg_text(txt):
        # 심화리뷰 critical 벨트: 패키지-유래 문자열(reason 등)에 bare None/NaN 토큰이 있으면
        # java 주석에 실린 뒤 §F1 누출가드가 생성기 버그로 오인해 전체 빌드가 죽는다
        # (실증: exporter 의 "부재/None 항목" 문구 → SDCP 킷 전부 mph 생성 불가).
        # 가드의 목적은 **값** 누출 검출이므로 인용문의 토큰은 무해화해 전달한다.
        import re as _re
        return _re.sub(r'\b(None|NaN|nan)\b', 'null', str(txt))

    def _reason_for(key):
        # ★ 익스포터 실형태 최우선 (리뷰 critical): comsol_export build_electrochem 은 사유를
        #   provenance['reason'] = {필드명: str} 서브딕트로 기록한다.  이 경로가 빠지면 실제
        #   패키지의 §F1 TODO 전부가 "사유 없음" 으로 나가 java 가 패키지에 대한 거짓 진술을 한다.
        rd = prov.get('reason')
        if isinstance(rd, dict) and rd.get(key):
            return _pkg_text(rd[key])
        ent = prov.get(key)
        if isinstance(ent, dict) and ent.get('reason'):
            return str(ent['reason'])
        if isinstance(ent, str):
            return ent
        if isinstance(rd, str):
            return rd
        return 'provenance 에 사유 없음'

    for key, pname, unit, descr in _ECHEM_PARAM_MAP:
        v = echem.get(key)
        if v is None:
            TODO(f'{pname} ({key}) — 패키지에 null, reason: {_reason_for(key)}')
        else:
            CALL(('param', ()), ('set', (pname, f'{float(v):.9g}{unit}', descr)))
    if echem.get('T_C') is not None:
        t_c = float(echem['T_C'])
        CALL(('param', ()), ('set', ('T_cell', f'{t_c + 273.15:.9g}[K]',
                                     f'cell temperature (electrochem.T_C = {t_c:.6g} degC)')))
        C('파라미터는 제작압 P·위 온도에 갇힌 값 — 다른 (P,T) 로 외삽 금지 (conventions.md)')
        C('★ kdom_S_m/σ_bulk 는 **이미 선언 온도의 값** (payload 가 T-스케일 후 solve) —'
          '\nCOMSOL 재료에 σ(T) Arrhenius 를 다시 걸면 이중적용 (60°C 재적용 = ×22.9 오류).'
          '\nse_domain.sigma_declared_at_T_C 가 선언 온도 (없으면 T_ref 25°C 규약).')
    else:
        TODO(f'T_cell — 패키지에 T_C null, reason: {_reason_for("T_C")}')
    if echem.get('ocp_csv'):
        TODO(f"E_eq(soc) — ocp 파일 {echem['ocp_csv']} 을 Interpolation 함수로 굽기 (B2;"
             '\n  포인트를 java 에 직접 내장, COMSOL 이 CSV 를 읽게 하지 말 것)')
    BLANK()

    # 스피어별 f_cov — B2 BV 경계 스케일 인자 (ballB<k> 선택과 1:1)
    C('── 스피어별 f_cov (MPM face-walk; BV 반응면 스케일: i_loc ∝ f_cov_reaction) ──')
    fb = [s for s in spheres if s['f_cov_source'] == 'class_mean_fallback']
    if fb:
        C(f'주의: {len(fb)}/{len(spheres)} 스피어의 f_cov_source = class_mean_fallback (개별값 아님)')
    for k, s in enumerate(pkg['spheres']):
        pid = _pname(s['id'])
        CALL(('param', ()), ('set', (f'fcov_r_{pid}', f'{s["f_cov_reaction"]:.6g}',
                                     f'sphere {s["id"]} reaction-face fraction')))
        CALL(('param', ()), ('set', (f'fcov_c_{pid}', f'{s["f_cov_carbon"]:.6g}',
                                     f'sphere {s["id"]} carbon-face fraction')))
        CALL(('param', ()), ('set', (f'fcov_b_{pid}', f'{s["f_cov_block"]:.6g}',
                                     f'sphere {s["id"]} blocked-face fraction')))
    BLANK()

    # ═══════════ Component / Geometry ═══════════
    CALL(('component', ()), ('create', ('comp1', True)))
    CALL(('component', ('comp1',)), ('geom', ()), ('create', ('geom1', 3)))
    CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('lengthUnit', ('µm',)))
    BLANK()
    C('══ Geometry — 전극 박스 + AM 해상 스피어 ══')
    CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('create', ('blk1', 'Block')))
    CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', ('blk1',)),
         ('set', ('size', ('D[]', [Lx, Ly, Lz]))))
    CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', ('blk1',)),
         ('set', ('pos', ('D[]', [0.0, 0.0, 0.0]))))
    for k, s in enumerate(spheres):
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('create', (f'sph{k}', 'Sphere')))
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', (f'sph{k}',)),
             ('set', ('pos', ('D[]', [s['x'], s['y'], s['z']]))))
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', (f'sph{k}',)),
             ('set', ('r', s['r'])))
    BLANK()

    # ── RVE 클립: 박스 밖으로 삐져나온 구 잘라내기 ──
    # STEP3 복셀 래스터화는 박스를 벗어난 구 재료를 그냥 버린다(크롭).  java 기하가 그대로
    # 두면 (a) 박스 밖 AM 캡이 별도 도메인으로 남아 재료/물리 미배정 + 메시 낭비, (b) z 로
    # 관통한 구는 플레이튼 면(selTop/selBot)을 뚫어 adjAM∩selTop 이 비어 AM-집전체 접촉이
    # 통째로 누락된다.  → 박스와 교집합을 취해 STEP3 크롭 규약과 같은 RVE 로 맞춘다.
    prot = _protrusion(spheres, Lx, Ly, Lz)
    do_clip = (clip == 'on') or (clip == 'auto' and prot['n_any'] > 0)
    if do_clip and spheres:
        C(f"★ RVE 클립 (STEP3 크롭 규약 일치): 박스 밖 스피어 {prot['n_any']}개"
          f"(측면 {prot['n_lat']} / z {prot['n_z']}) · 밖 체적 {prot['v_out_um3']:.1f} µm³ ="
          f" AM 총체적의 {prot['pct_of_am']:.2f}% (박스체적 대비 {prot['pct_of_box']:.2f}%)."
          '\nz 관통 구를 안 자르면 플레이튼 면이 뚫려 adjAM∩selTop 이 비고 AM-집전체 BC 가'
          '\n통째로 누락된다.  intbnd=on → 겹침 렌즈 분할(넥)은 클립 후에도 보존.'
          '\n⚠ 주기 킷이면 박스를 넘어간 부분의 반대편 이미지는 복원하지 않는다 (java Block ='
          '\n절연벽 — se_domain.periodic_xy 경고와 같은 한계).  --clip off 로 끌 수 있다.')
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('create', ('blkc', 'Block')))
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', ('blkc',)),
             ('set', ('size', ('D[]', [Lx, Ly, Lz]))))
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', ('blkc',)),
             ('set', ('pos', ('D[]', [0.0, 0.0, 0.0]))))
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', ('blkc',)),
             ('label', ('clip box (RVE) — intersected away, blk1 이 SE 모체',)))
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('create', ('uniAM', 'Union')))
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', ('uniAM',)),
             ('set', ('input', ('S[]', [f'sph{k}' for k in range(len(spheres))]))))
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', ('uniAM',)),
             ('set', ('intbnd', True)))
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('create', ('clipAM', 'Intersection')))
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', ('clipAM',)),
             ('set', ('input', ('S[]', ['uniAM', 'blkc']))))
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', ('clipAM',)),
             ('set', ('intbnd', True)))
        BLANK()
    elif prot['n_any'] > 0:
        C(f"⚠ 클립 꺼짐(--clip off) — 박스 밖 스피어 {prot['n_any']}개가 그대로 남는다:"
          f" AM 체적 {prot['pct_of_am']:.2f}% 가 전극 밖 도메인이 되고, z 관통 {prot['n_z']}개는"
          '\n플레이튼 면을 뚫어 AM-집전체 접촉(adjAM∩selTop)이 누락된다.  STEP3(크롭)과 비교 불가.')
        BLANK()

    C('★ form UNION (기본 finalize): 겹치는 AM 구의 합집합이 DEM δ 렌즈 넥을 기하로 생성.'
      '\n⚠ 기하 정밀화(심화리뷰): 렌즈 목(waist) 반경 = √(2R*δ) = **√2 × a_hertz** (면적 2×)'
      '\n— Holm 표(g=2σa_hertz) 대비 넥 전류 ~×1.4 상회가 기하적 기대값 (real_14 587접촉'
      '\n실측 a_lens/a_hertz 평균 1.405).  g_holm 표는 검증 전용, 소자 추가 금지 (conventions §8).'
      '\n(구 표현 "= Hertz 탄성 넥" 은'
      '\n기하로 자연 생성한다 (2026-08-05 결정 — NCM 140 GPa ≫ SE 1.35 GPa 라 AM 소성 미미,'
      '\nAM-AM 은 DEM δ 탄성 그대로).  union 은 겹침 렌즈를 별도 도메인으로 분할해 컨포멀'
      '\n메시를 만든다 — assembly 로 바꾸면 넥이 끊긴다(금지).')
    if pkg['contacts']:
        gsum = sum(c['g_holm_S'] for c in pkg['contacts'])
        C(f"교차대조: am_am_contacts.csv n={len(pkg['contacts'])}, Σg_holm = {gsum:.6g} S —"
          '\n기하 넥 해상도 검증용 (README 표).  넥 면적은 Hertz a=√(R*δ) 탄성 밴드;')
    TODO('Stage-E 소성-면적(Tabor) 옵션 — 지금은 탄성 δ 렌즈만.  소성 넥이 필요하면 접촉별'
         '\n  a_plastic 으로 스피어 반경/렌즈를 재구성하는 별도 옵션 (am_am_contacts.csv 헤더 참조)')
    CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', ('fin',)),
         ('set', ('action', 'union')))
    BLANK()

    # ── Selections (기하 셀렉션 — 물리/재료가 named 로 참조) ──
    C('── Selections: 스피어별 Ball(도메인/경계) → 클래스 Union → SE = Complement ──')
    C('BallSelection r 은 +1e-3 µm 인플레이션 — 접면 수치오차 대비.  condition:'
      '\n도메인 = inside (union 분할 후 렌즈 조각도 원구 내부), 경계 = intersects.')
    ballD_by_cls = {'AM_P': [], 'AM_S': []}
    for k, s in enumerate(spheres):
        r_sel = s['r'] + max(1e-3, 1e-4 * s['r'])
        for tag, dim, cond in ((f'ballD{k}', 3, 'inside'), (f'ballB{k}', 2, 'intersects')):
            CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('create', (tag, 'BallSelection')))
            CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', (tag,)),
                 ('set', ('entitydim', dim)))
            for ax, v in (('posx', s['x']), ('posy', s['y']), ('posz', s['z']), ('r', r_sel)):
                CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', (tag,)),
                     ('set', (ax, v)))
            CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', (tag,)),
                 ('set', ('condition', cond)))
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', (f'ballB{k}',)),
             ('label', (f'AM sphere {s["id"]} boundary ({s["cls"]})',)))
        ballD_by_cls[s['cls']].append(f'ballD{k}')

    union_inputs = []
    for cls, tag in (('AM_P', 'selAMP'), ('AM_S', 'selAMS')):
        if ballD_by_cls[cls]:
            CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('create', (tag, 'UnionSelection')))
            CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', (tag,)),
                 ('set', ('entitydim', 3)))
            CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', (tag,)),
                 ('set', ('input', ('S[]', ballD_by_cls[cls]))))
            union_inputs.append(tag)
    CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('create', ('selAM', 'UnionSelection')))
    CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', ('selAM',)),
         ('set', ('entitydim', 3)))
    CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', ('selAM',)),
         ('set', ('input', ('S[]', union_inputs))))
    C('SE = 박스에서 AM 을 뺀 여집합 연속체.  PTFE 는 기하 금지 — 차단 효과는 κ_dom·f_cov 에'
      '\n이미 반영 (기하로 또 넣으면 이중계상).  pore 도 기하 없음 — κ_dom 이 φ/τ 로 흡수.')
    CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('create', ('selSE', 'ComplementSelection')))
    CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', ('selSE',)),
         ('set', ('entitydim', 3)))
    CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', ('selSE',)),
         ('set', ('input', ('S[]', ['selAM']))))
    BLANK()
    C('플레이트(z 양단) 경계 + 상별 교집합 — σ_eff 적분/BC 용')
    eps = 1e-3
    for tag, zmin, zmax in (('selTop', Lz - eps, Lz + eps), ('selBot', -eps, eps)):
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('create', (tag, 'BoxSelection')))
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', (tag,)),
             ('set', ('entitydim', 2)))
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', (tag,)),
             ('set', ('zmin', zmin)))
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', (tag,)),
             ('set', ('zmax', zmax)))
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', (tag,)),
             ('set', ('condition', 'inside')))
    for src, adj in (('selAM', 'adjAM'), ('selSE', 'adjSE')):
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('create', (adj, 'AdjacentSelection')))
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', (adj,)),
             ('set', ('input', ('S[]', [src]))))
    for tag, a, b in (('selAMtop', 'adjAM', 'selTop'), ('selAMbot', 'adjAM', 'selBot'),
                      ('selSEtop', 'adjSE', 'selTop'), ('selSEbot', 'adjSE', 'selBot')):
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('create', (tag, 'IntersectionSelection')))
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', (tag,)),
             ('set', ('entitydim', 2)))
        CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', (tag,)),
             ('set', ('input', ('S[]', [a, b]))))
    BLANK()

    # ── VGCF: InterpolationCurve (데이터 있을 때만 기하 생성; 물리 결합은 TODO) ──
    if pkg['fibres']:
        vm = pkg['vgcf_meta']
        C(f'── VGCF 1D 섬유 {len(pkg["fibres"])}개 — 단면 π({vm["diameter_um"]/2:.4g}[um])^2,'
          f' σ = {vm["sigma_S_cm"]:.6g} S/cm = {vm["sigma_S_cm"]*100.0:.6g} S/m'
          + (' (vgcf_fibres.csv 헤더값)' if vm['from_header'] else ' (기본값 — 헤더에 명시 없음)')
          + ' ──')
        CALL(('param', ()), ('set', ('vgcf_diam', f'{vm["diameter_um"]:.9g}[um]', 'VGCF diameter')))
        CALL(('param', ()), ('set', ('vgcf_area', 'pi*(vgcf_diam/2)^2', 'VGCF cross-section (exact)')))
        CALL(('param', ()), ('set', ('sigma_vgcf_S_m', f'{vm["sigma_S_cm"]*100.0:.9g}[S/m]',
                                     'VGCF axial conductivity')))
        for n, (fid, pts) in enumerate(sorted(pkg['fibres'].items())):
            tab = [[f'{p[0]:.9g}', f'{p[1]:.9g}', f'{p[2]:.9g}'] for p in pts]
            CALL(('component', ('comp1',)), ('geom', ('geom1',)),
                 ('create', (f'vgcf{n}', 'InterpolationCurve')))
            CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', (f'vgcf{n}',)),
                 ('set', ('table', ('S[][]', tab))))
            CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('feature', (f'vgcf{n}',)),
                 ('label', (f'VGCF fibre {fid}',)))
        TODO('VGCF 물리 결합 — Edge Current 계열 feature 명은 COMSOL 버전/모듈 의존 — 첫 실행 시'
             '\n  확정.  후보: ec 의 edge 전류 보존 feature 또는 mef/wire.  단면적 vgcf_area ·'
             '\n  σ sigma_vgcf_S_m 를 edge 에 부여해 전자망(ec)에 병렬 연결하는 것이 목표.'
             '\n  InterpolationCurve 의 table/property 명도 버전 의존 — 실패 시 Polygon 폴백.')
    else:
        C('── VGCF 절 전체 주석 처리: vgcf_fibres.csv 에 데이터 행 없음'
          '\n(manifest.notes 사유 참조).  섬유가 생기면 이 자리에 InterpolationCurve 루프 +'
          '\nEdge Current 결합이 들어온다 — build_comsol_mph.py 가 자동 생성. ──')
    BLANK()
    CALL(('component', ('comp1',)), ('geom', ('geom1',)), ('run', ()))
    BLANK()

    # ═══════════ Mesh ═══════════
    C('Mesh — 기본 physics-controlled, autoMeshSize=4 (Normal).  δ 렌즈(넥) 근방은 곡률'
      '\n세분이 자동으로 잡지만, 넥 병목 해상이 부족하면 4→3(→2) 로 낮춘다 (README 디버깅 절).'
      '\n★ 선례 (2026-08-05 사용자): 좌표→java 생성 + 겹침 repair + fine mesh 로 오류 없이'
      '\n완주한 AM-메시 워크플로가 이미 있다 — sliver(겹침 이음새)는 그 절차가 실증 해결.'
      '\nTODO(trackb): 그 스크립트의 repair tolerance·메시 설정을 수확해 여기 기본값으로 (T15).')
    CALL(('component', ('comp1',)), ('mesh', ()), ('create', ('mesh1',)))
    CALL(('component', ('comp1',)), ('mesh', ('mesh1',)), ('autoMeshSize', (4,)))
    BLANK()

    # ═══════════ Materials ═══════════
    C('══ Materials — S/cm → S/m 는 ×100 (conventions.md 단위표) ══')
    mat_defs = []
    if 'AM_P' in cls_sigma:
        mat_defs.append(('matAMP', 'AM_P (poly NCM)', 'geom1_selAMP', 'sigma_e_AMP_S_m'))
    if 'AM_S' in cls_sigma:
        mat_defs.append(('matAMS', 'AM_S (single-crystal NCM)', 'geom1_selAMS', 'sigma_e_AMS_S_m'))
        # 리뷰 minor: AM_P∩AM_S 이종-접촉 렌즈 도메인은 두 BallSelection 에 모두 들어 재료가
        # 이중 배정된다 — COMSOL 은 트리에서 나중 재료(matAMS, σ 2×)가 우선.  넥 스프레딩
        # 저항은 양쪽 구 벌크가 각자 σ 로 조화-직렬을 재현하므로 2차 효과지만, 패키지의
        # Holm 표가 이종 접촉에 조화평균 σ_c 를 쓰는 것과 관례가 다름을 기록해 둔다.
        # TODO(trackb): 렌즈 전용 선택(ballD_P ∩ ballD_S DifferenceSelection) 분리 옵션
    if se_sigma_S_m is not None:
        mat_defs.append(('matSE', 'SE continuum (kappa_dom)', 'geom1_selSE', 'kdom_S_m'))
    else:
        C('SE 재료 미생성 — kdom_S_m 파라미터가 null (위 TODO).  ec2 솔브 전 반드시 채울 것.')
    for mtag, mlabel, sel, sparam in mat_defs:
        CALL(('component', ('comp1',)), ('material', ()), ('create', (mtag, 'Common')))
        CALL(('component', ('comp1',)), ('material', (mtag,)), ('label', (mlabel,)))
        CALL(('component', ('comp1',)), ('material', (mtag,)), ('selection', ()), ('named', (sel,)))
        CALL(('component', ('comp1',)), ('material', (mtag,)), ('propertyGroup', ('def',)),
             ('set', ('electricconductivity', ('S[]', [sparam]))))
        CALL(('component', ('comp1',)), ('material', (mtag,)), ('propertyGroup', ('def',)),
             ('set', ('relpermittivity', ('S[]', ['1']))))
    BLANK()

    # ═══════════ Physics ═══════════
    C('══ Physics v1 (B1 검증 범위): 정상해 σ 교차대조 — z 양단 1V/접지 2회 ══')
    C('ec (전자): AM 도메인만.  주의 — 양 플레이트에 닿지 않는 고립 AM 클러스터는 특이계를'
      '\n만든다 (부동 전위).  DEM 퍼콜 네트워크가 z-관통이면 문제 없음.')
    TODO('고립 AM 클러스터 특이계 대응 — 첫 실행에서 singular 나면: (a) 고립 클러스터를 ec'
         '\n  선택에서 제외(STEP3 퍼콜 라벨 재사용) 또는 (b) 미소 컨덕턴스 안정화.  자동화는 B2.')
    CALL(('component', ('comp1',)), ('physics', ()), ('create', ('ec', 'ConductiveMedia', 'geom1')))
    CALL(('component', ('comp1',)), ('physics', ('ec',)), ('label', ('Electronic - AM network',)))
    CALL(('component', ('comp1',)), ('physics', ('ec',)), ('selection', ()), ('named', ('geom1_selAM',)))
    CALL(('component', ('comp1',)), ('physics', ('ec',)), ('create', ('gnd1', 'Ground', 2)))
    CALL(('component', ('comp1',)), ('physics', ('ec',)), ('feature', ('gnd1',)), ('selection', ()),
         ('named', ('geom1_selAMbot',)))
    CALL(('component', ('comp1',)), ('physics', ('ec',)), ('create', ('pot1', 'ElectricPotential', 2)))
    CALL(('component', ('comp1',)), ('physics', ('ec',)), ('feature', ('pot1',)), ('selection', ()),
         ('named', ('geom1_selAMtop',)))
    CALL(('component', ('comp1',)), ('physics', ('ec',)), ('feature', ('pot1',)),
         ('set', ('V0', 'V_app')))
    BLANK()
    C('★ single-ion 경고 (LPSCl t+ ~ 1): 전해질 농도분극이 물리적으로 없다.  일반 리튬이온/DFN'
      '\n인터페이스(Nernst-Planck/tds, Battery Design Module 의 Lithium-Ion Battery 등)를 쓰면'
      '\n가짜 확산분극이 생긴다 — 전류분포(1차/2차) + 우리 kappa_dom 만 쓴다 (사용자 확정).')
    CALL(('component', ('comp1',)), ('physics', ()), ('create', ('ec2', 'ConductiveMedia', 'geom1')))
    CALL(('component', ('comp1',)), ('physics', ('ec2',)),
         ('label', ('Ionic - SE continuum (single-ion, kappa_dom)',)))
    CALL(('component', ('comp1',)), ('physics', ('ec2',)), ('selection', ()), ('named', ('geom1_selSE',)))
    CALL(('component', ('comp1',)), ('physics', ('ec2',)), ('create', ('gnd1', 'Ground', 2)))
    CALL(('component', ('comp1',)), ('physics', ('ec2',)), ('feature', ('gnd1',)), ('selection', ()),
         ('named', ('geom1_selSEbot',)))
    CALL(('component', ('comp1',)), ('physics', ('ec2',)), ('create', ('pot1', 'ElectricPotential', 2)))
    CALL(('component', ('comp1',)), ('physics', ('ec2',)), ('feature', ('pot1',)), ('selection', ()),
         ('named', ('geom1_selSEtop',)))
    CALL(('component', ('comp1',)), ('physics', ('ec2',)), ('feature', ('pot1',)),
         ('set', ('V0', 'V_app')))
    BLANK()
    C('── TODO(trackb) B2: Butler-Volmer AM|SE 계면 결합 (v1 은 σ 교차대조까지) ──'
      '\n준비된 조각: 스피어별 경계 선택 ballB<k> + 파라미터 fcov_r_<id>/fcov_c_<id>/fcov_b_<id>.'
      '\n결합식(정확): i_loc = fcov_r_i * i0 * ( exp(alpha_a*F_const*eta/(R_const*T_cell))'
      '\n                                      - exp(-alpha_c*F_const*eta/(R_const*T_cell)) )'
      '\n  eta = V(ec, AM측) - V(ec2, SE측) - E_eq(soc);  E_eq 는 ocp_*.csv 를 Interpolation 으로.'
      '\n  f_cov 물리: reaction 면만 BV, carbon 면은 전자 소스, block(PTFE) 면은 불활성 —'
      '\n  PTFE 를 기하로 넣지 않는 대신 여기 면분율로 반영한다 (이중계상 금지).'
      '\n구현 후보: ec/ec2 경계 Boundary Current Source 쌍(±i_loc) 또는 전기화학 모듈'
      '\nElectrodeSurface.  asr_film/R_int 는 직렬 막저항으로 같은 경계에.'
      '\n현재 electrochem.json 의 null 항목(위 TODO 목록)이 채워져야 실행 가능.')
    todos.append('B2 — BV 계면 결합 배선 (ballB<k>+fcov 파라미터는 준비됨; i0 등 null 채우기 선행)')
    BLANK()

    # ═══════════ Integration couplings + Studies + Results ═══════════
    C('적분 연산자 — 플레이트 전류 → σ_eff = |I|·L_z/(V_app·A_xy)')
    for tag, opname, sel in (('intop1', 'int_am_top', 'geom1_selAMtop'),
                             ('intop2', 'int_se_top', 'geom1_selSEtop')):
        CALL(('component', ('comp1',)), ('cpl', ()), ('create', (tag, 'Integration')))
        CALL(('component', ('comp1',)), ('cpl', (tag,)), ('set', ('opname', opname)))
        CALL(('component', ('comp1',)), ('cpl', (tag,)), ('selection', ()), ('named', (sel,)))
    BLANK()
    C('Study 2개: std1 = 전자(ec), std2 = 이온(ec2).'
      '\n⚠ setSolveFor 의 try 는 **런타임 인자 오류만** 방어한다 — 메서드가 버전 API 에 아예'
      '\n없으면 javac 컴파일 에러라 try 이전에 실패한다.  NoSuchMethod 컴파일 실패 시 이'
      '\ntry 블록 두 개를 통째로 삭제 — 두 물리는 비결합이라 같이 풀려도 σ_eff 는 동일.')
    todos.append('setSolveFor / activate — COMSOL 버전에 따라 study step API 확인 (첫 실행)')
    todos.append('TODO(trackb) T2 — 브릿지 실린더: am_am_contacts.csv 의 각 접촉에 '
                 'r=max(a_hertz, 1.2·vox상당) Cylinder 를 UNION.  근접-비접촉(gap>0) 접촉이 '
                 '매끈 기하에서 개회로가 되는 것을 닫고(rasterize 1.2vox 브릿지와 같은 회로), '
                 '점접촉-스냅의 메시-의존 σ 대신 물리적 넥 면적으로 수렴시킨다')
    CALL(('study', ()), ('create', ('std1',)))
    CALL(('study', ('std1',)), ('create', ('stat1', 'Stationary')))
    steps.append(('tryblock', 'std1 setSolveFor', [
        ('call', [('study', ('std1',)), ('feature', ('stat1',)),
                  ('setSolveFor', ('/physics/ec2', False))])]))
    CALL(('study', ()), ('create', ('std2',)))
    CALL(('study', ('std2',)), ('create', ('stat1', 'Stationary')))
    steps.append(('tryblock', 'std2 setSolveFor', [
        ('call', [('study', ('std2',)), ('feature', ('stat1',)),
                  ('setSolveFor', ('/physics/ec', False))])]))
    BLANK()
    C('Global Evaluation — 터미널 전류 적분 → σ_eff 표 export.  |·| 는 법선 방향 부호 정리.'
      '\ndset1/dset2 는 study 생성 순서를 따른다 (안 맞으면 Results 노드에서 재지정).')
    CALL(('result', ()), ('table', ()), ('create', ('tbl1', 'Table')))
    CALL(('result', ()), ('table', ()), ('create', ('tbl2', 'Table')))
    CALL(('result', ()), ('numerical', ()), ('create', ('gevE', 'Global')))
    CALL(('result', ()), ('numerical', ('gevE',)), ('set', ('data', 'dset1')))
    CALL(('result', ()), ('numerical', ('gevE',)),
         ('set', ('expr', ('S[]', ['abs(int_am_top(ec.nJ))*L_z/(V_app*A_xy)']))))
    CALL(('result', ()), ('numerical', ('gevE',)),
         ('set', ('unit', ('S[]', ['S/m']))))
    CALL(('result', ()), ('numerical', ('gevE',)),
         ('set', ('descr', ('S[]', ['sigma_e_eff (electronic, AM network)']))))
    CALL(('result', ()), ('numerical', ('gevE',)), ('set', ('table', 'tbl1')))
    CALL(('result', ()), ('numerical', ()), ('create', ('gevI', 'Global')))
    CALL(('result', ()), ('numerical', ('gevI',)), ('set', ('data', 'dset2')))
    CALL(('result', ()), ('numerical', ('gevI',)),
         ('set', ('expr', ('S[]', ['abs(int_se_top(ec2.nJ))*L_z/(V_app*A_xy)']))))
    CALL(('result', ()), ('numerical', ('gevI',)),
         ('set', ('unit', ('S[]', ['S/m']))))
    CALL(('result', ()), ('numerical', ('gevI',)),
         ('set', ('descr', ('S[]', ['sigma_ion_eff (ionic, SE continuum)']))))
    CALL(('result', ()), ('numerical', ('gevI',)), ('set', ('table', 'tbl2')))
    BLANK()
    C('솔브 + 표 저장 — 실패해도 모델은 반환되어 .mph 로 저장된다 (기하/설정 검사 가능).')
    steps.append(('tryblock', 'std1 solve + sigma_e table', [
        ('call', [('study', ('std1',)), ('run', ())]),
        ('call', [('result', ()), ('numerical', ('gevE',)), ('setResult', ())]),
        ('call', [('result', ()), ('table', ('tbl1',)), ('save', ('comsol_sigma_e_eff.txt',))])]))
    steps.append(('tryblock', 'std2 solve + sigma_ion table', [
        ('call', [('study', ('std2',)), ('run', ())]),
        ('call', [('result', ()), ('numerical', ('gevI',)), ('setResult', ())]),
        ('call', [('result', ()), ('table', ('tbl2',)), ('save', ('comsol_sigma_ion_eff.txt',))])]))
    BLANK()
    CALL(('label', (f"comsol_pkg_{pkg['case']} (trackb hybrid v1)",)))

    # ── 규모 가드: java 클래스 constant-pool 한도 (part 분할로는 못 푸는 벽) ──
    n_sph = len(spheres)
    if n_sph >= _SPHERE_SOFT_CAP:
        est_cp = int(n_sph * _CP_ENTRIES_PER_SPHERE)
        msg = (f'AM 스피어 {n_sph} 개 → java 클래스 constant pool 추정 {est_cp:,}/65,535 '
               f'({100 * est_cp / 65535:.0f} %).  ')
        if n_sph >= _SPHERE_HARD_CAP:
            msg += (f'★ 한도 초과 예상 — javac 이 "too many constants" 로 거부한다. '
                    f'클래스 분할(part 로는 못 푼다 — CP 는 클래스 단위) 또는 MPh 경로'
                    f'(--mph, java 컴파일 없음)를 써야 한다.')
        else:
            msg += f'한도({_SPHERE_HARD_CAP:,} 스피어)에 근접 — 더 큰 침대는 MPh 경로 권장.'
        pkg['warnings'].append(msg)
        C('⚠ ' + msg.replace('  ', ' '))
        TODO('스피어 수가 CP 한도를 넘으면 model_build_partN.java 로 클래스를 쪼개거나 '
             'MPh(--mph) 런타임 경로로 우회 — 지금은 경고만 (T16)')

    ctx = {'Lx': Lx, 'Ly': Ly, 'Lz': Lz, 'se_sigma_S_m': se_sigma_S_m,
           'se_sigma_origin': se_sigma_origin, 'cls_sigma': cls_sigma,
           'clip_mode': clip, 'clipped': bool(do_clip and spheres), 'protrusion': prot,
           'n_spheres': n_sph, 'cp_est': int(n_sph * _CP_ENTRIES_PER_SPHERE)}
    return steps, todos, ctx


# ───────────────────────────── 산출물: java / README ─────────────────────────────

def _md5(path: Path) -> str:
    h = hashlib.md5()
    h.update(path.read_bytes())
    return h.hexdigest()


def _header_comment(pkg: dict) -> str:
    man = pkg['manifest']
    lines = [
        'model_build.java — COMSOL java model file (Track-B 하이브리드: AM 해상구 + SE 연속체)',
        f"case: {pkg['case']}   source: {man.get('source', '?')}   schema: "
        f"{man.get('schema_version', SCHEMA_VERSION)}",
        f'generator: {GENERATOR}   created_utc: '
        f"{_dt.datetime.now(_dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        f"pkg git_commit: {man.get('git_commit') or '(null)'}",
        f'tau convention: {TAU_CONVENTION}',
        '빌드: comsol batch -inputfile model_build.java -outputfile <case>.mph  (README_run.md)',
        '이 파일의 모든 수치는 comsol_pkg 에서 생성 시점에 구워졌다 — 원본 수정은 패키지에서.',
    ]
    for w in pkg['warnings']:
        lines.append('경고: ' + w)
    return '\n'.join(lines)


def write_readme(pkg: dict, ctx: dict, todos, out_dir: Path, java_name: str = 'model_build.java'):
    man, se = pkg['manifest'], pkg['se']
    case = pkg['case']
    now = _dt.datetime.now(_dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    n_p = sum(1 for s in pkg['spheres'] if s['cls'] == 'AM_P')
    n_s = len(pkg['spheres']) - n_p

    # STEP3 대조값 재구성 (τ 선형 관례) — 없으면 '—' (§F1)
    sig_ion_step3 = None
    if se.get('sigma_bulk_ion_S_cm') is not None and se.get('phi_full') is not None \
            and se.get('tau_full') not in (None, 0):
        sig_ion_step3 = float(se['sigma_bulk_ion_S_cm']) * float(se['phi_full']) / float(se['tau_full'])

    def fmt(v, unit=''):
        return '—' if v is None else f'{float(v):.6g}{unit}'

    md = []
    md.append(f'# README_run — comsol_pkg_{case} → COMSOL 모델')
    md.append('')
    md.append(f'- 생성: `{GENERATOR}` · {now} · pkg git_commit `{man.get("git_commit") or "null"}`')
    md.append(f'- 구성: AM 스피어 {len(pkg["spheres"])} (P {n_p} / S {n_s}) · AM-AM 접촉 '
              f'{len(pkg["contacts"])} · VGCF 섬유 {len(pkg["fibres"])} · '
              f'box {ctx["Lx"]:.4g}×{ctx["Ly"]:.4g}×{ctx["Lz"]:.4g} µm')
    _sbsrc = (se or {}).get('sigma_bulk_source')
    md.append(f'- SE 연속체 σ: {fmt(ctx["se_sigma_S_m"], " S/m")} (출처 '
              f'{ctx["se_sigma_origin"] or "null — TODO"}'
              + (f'; σ_bulk={_sbsrc} — 킷 측정값 아님' if _sbsrc else '')
              + f') · τ 관례 `{TAU_CONVENTION}`')
    for w in pkg['warnings']:
        md.append(f'- ⚠ {w}')
    md.append('')

    # ── §0: 예전 수동 .mph 에서 실제로 터졌던 두 함정 (실행 전에 읽는다) ──
    _np_ = len(pkg['spheres'])
    md.append('## 0) 먼저 읽을 것 — 예전 수동 모델에서 실제로 터진 두 함정')
    md.append('')
    md.append('### 0-1) 길이 단위 — 이 java 는 이미 맞춰져 있다 (수동 스케일다운 금지)')
    md.append('')
    md.append('예전 수동 모델은 LIGGGHTS dump 값을 그대로 넣어 `sph.set("r","0.0025")` 처럼 '
              '**단위 없는 수**를 썼다.  COMSOL 은 그것을 기하 길이단위(기본 **m**)로 읽으므로 '
              '2.5 mm 구가 50 mm 박스에 놓인 **1000× 확대 모델**이 된다.  물리는 스케일-불변이 '
              '아니다 — 확산·BV·시간상수가 전부 어긋난다.')
    md.append('')
    md.append('이 파일은 그 문제를 **생성 시점에 닫아 두었다**:')
    md.append('')
    md.append('- `geom1.lengthUnit("µm")` 를 **어떤 기하 feature 보다 먼저** 선언 → 이후 모든 '
              '`pos`/`r`/`size` 의 맨수는 µm.')
    md.append(f'- 좌표·반지름은 python 이 LU(=mm)×1000 → µm 로 변환해 구웠다 '
              f'(박스 {ctx["Lx"]:.4g}×{ctx["Ly"]:.4g}×{ctx["Lz"]:.4g} µm, '
              f'반지름 실측 범위 그대로).')
    md.append('- `L_x`/`L_y`/`L_z` 등 파라미터는 `"50[um]"` 처럼 **단위를 명시**해 기하 단위와 '
              '무관하게 안전하다.')
    md.append('')
    md.append('⇒ **손으로 다시 스케일다운하지 말 것.**  값을 고칠 일이 생기면 java 가 아니라 '
              '`comsol_pkg` 에서 고치고 재생성한다 (이 파일의 모든 수치는 패키지에서 구워진다).')
    md.append('')
    md.append('### 0-2) 솔버 — 스피어가 많으면 Direct/PARDISO 는 메모리로 죽는다')
    md.append('')
    md.append(f'이 모델은 AM 스피어 **{_np_}** 개를 해상한다.  예전 수동 모델(≈1767 구)은 '
              'Direct(PARDISO)에서 *"out-of-core 불가"* 로 실패했다 — 3D 전도 문제의 '
              'LU 분해는 메모리가 자유도에 초선형으로 늘어 수만~수십만 DOF 를 넘기면 '
              '데스크톱 RAM 을 넘긴다.')
    md.append('')
    md.append('⇒ **반복 솔버(Iterative)** 를 쓴다.  전도(라플라스형)에는 표준 처방이 있다:')
    md.append('')
    md.append('| 항목 | 권장 |')
    md.append('|---|---|')
    md.append('| Linear solver | **Iterative** (Conjugate Gradients) |')
    md.append('| Preconditioner | **AMG**(Algebraic Multigrid) — 기하 다중격자(GMG)는 이 '
              '비정형 넥 기하에서 조립이 잘 안 된다 |')
    md.append('| 상대공차 | 1e-3 (전도 σ_eff 용) → 필요시 1e-6 |')
    md.append('| Direct 를 꼭 써야 하면 | MUMPS + out-of-core, 그래도 스피어 수를 줄여야 함 |')
    md.append('')
    md.append('COMSOL GUI: Study ▸ Solver Configurations ▸ Stationary Solver ▸ '
              '(우클릭) Iterative → Preconditioner 를 AMG 로.  '
              '`ec`/`ec2` 는 서로 결합돼 있지 않으니 각각 따로 반복 솔버로 두면 된다.')
    md.append('')
    md.append('_참고_: 예전 모델의 `Error 1` 은 무시해도 되는 것으로 확인됨(사용자 확인) — '
              '위 두 항목이 실제 병목이었다.')
    md.append('')
    md.append('### 0-3) java 컴파일 한도 — 이미 분할해 두었다')
    md.append('')
    _cp = ctx.get('cp_est') or 0
    md.append(f'`comsol batch` 는 이 java 를 **내부에서 javac 으로 컴파일**한다.  스피어를 '
              f'해상하면 문장이 수천 개가 되어 JVM 의 두 한도에 걸린다:')
    md.append('')
    md.append('| 한도 | 값 | 이 모델 | 대응 |')
    md.append('|---|---|---|---|')
    md.append(f'| 메서드당 바이트코드 (JVMS §4.7.3) | 65,535 B | 최대 part ≈ 25 KB (38 %) | '
              f'**해결됨** — `run()` 이 `partN(model)` 로 분할 (실측: 미분할이면 '
              f'`code too large` 로 컴파일 실패) |')
    md.append(f'| 클래스당 constant pool (JVMS §4.1) | 65,535 | 추정 **{_cp:,}** '
              f'({100 * _cp / 65535:.0f} %) | 스피어당 ≈ 27 엔트리 → 한 클래스 상한 '
              f'≈ **{_SPHERE_HARD_CAP:,} 스피어**.  그 위는 클래스 분할 또는 `--mph` 경로 |')
    md.append('')
    md.append('⇒ 지금 규모(스피어 ' + f'{ctx.get("n_spheres", 0)}' + ')는 두 한도 모두 안쪽이다. '
              'java 를 손으로 합치지 말 것 (분할이 곧 컴파일 가능 조건).')
    md.append('')
    md.append('## 1) .mph 생성 (라이선스 머신, 1커맨드)')
    md.append('')
    md.append('```bash')
    md.append(f'cd <이 패키지 디렉토리>')
    md.append(f'comsol batch -inputfile {java_name} -outputfile {case}.mph')
    md.append('```')
    md.append('')
    md.append('- `comsol` 은 COMSOL 설치의 bin (Windows 는 `comsolbatch.exe`).  java 를 내부'
              ' 컴파일→`run()` 실행→모델을 `-outputfile` 로 저장한다.')
    md.append('- 필요 모듈: AC/DC (Electric Currents `ec`).  B2(BV) 확장 시 전기화학 모듈 검토.')
    md.append('- 솔브가 실패해도 모델 저장은 진행되도록 study run 이 try 로 감싸져 있다 — .mph 를'
              ' 열어 기하/선택/재료를 먼저 검수할 수 있다.')
    md.append('')
    md.append('## 2) MPh(pymph) 런타임 경로 (COMSOL 설치 + python 머신)')
    md.append('')
    md.append('```bash')
    md.append('pip install mph   # JPype 로 COMSOL 서버에 붙는 라이브러리')
    md.append(f'python3 scripts/build_comsol_mph.py <pkg_dir> --mph   # 같은 빌드 스텝을 라이브 재생 → {case}.mph')
    md.append('```')
    md.append('')
    md.append('- mph 미설치 머신에서는 안내만 출력하고 정상 종료한다 (java 경로 권장).')
    md.append('')
    md.append('## 3) 첫 실행 = feature 명 디버깅 왕복 전제')
    md.append('')
    md.append('COMSOL java API 의 feature/property 명은 버전·모듈 의존이라, 첫 `comsol batch` 는'
              ' 에러 메시지 ↔ 수정 왕복을 전제한다.  그 지점들이 전부 `TODO(trackb)` 주석이다:')
    md.append('')
    md.append('```bash')
    md.append(f'grep -n "TODO(trackb)" {java_name}')
    md.append('```')
    md.append('')
    md.append('| 리스크 지점 | 증상 | 대응 |')
    md.append('|---|---|---|')
    md.append('| `fin`.set("action","union") | Unknown property | 줄 삭제 (union 이 기본값) |')
    md.append('| `setSolveFor` | NoSuchMethod **컴파일** 에러 (try 로 못 잡음) | try 블록 두 개 삭제 — 비결합 물리라 같이 풀려도 동일 |')
    md.append('| `autoMeshSize(4)` | 넥 병목 미해상 (σ_e 과소) | 4→3(→2) 로 낮춤 — 요소수 급증 주의 |')
    md.append('| repair tolerance | 접촉 소멸 ↔ 틈 점접촉화 (아래 §3-1 표) | §3-1 의 권장값 + '
              'finalize 후 접촉 수 검산 |')
    md.append('| `BallSelection` condition/입력명 | Unknown property | inside↔somevertex 등 값 교체 |')
    md.append('| `InterpolationCurve` table | Unknown property | Polygon 폴백 (VGCF 절 주석 참조) |')
    if ctx.get('clipped'):
        md.append('| `uniAM`/`clipAM` (RVE 클립) | Unknown property `intbnd` | 그 두 줄만 삭제 '
                  '(기본값 on) — 클립 자체는 유지 (§3-0) |')
    md.append('')

    # ── §3-0: RVE 클립 (박스 밖 스피어) ──
    _pr = ctx.get('protrusion') or {}
    if _pr.get('n_any'):
        md.append('### 3-0) RVE 클립 — 박스 밖으로 삐져나온 스피어')
        md.append('')
        md.append(f'DEM 침대는 이 박스를 조금 넘는다: **{_pr["n_any"]}/{len(pkg["spheres"])}** 개가 '
                  f'박스 밖으로 나가 있다 (측면 {_pr["n_lat"]} · z {_pr["n_z"]}), '
                  f'밖 체적 {_pr["v_out_um3"]:.1f} µm³ = AM 총체적의 **{_pr["pct_of_am"]:.2f} %** '
                  f'(박스 체적 대비 {_pr["pct_of_box"]:.2f} %).')
        md.append('')
        if ctx.get('clipped'):
            md.append('→ 이 java 는 **클립했다** (`uniAM` = 스피어 합집합, `clipAM` = 박스와 '
                      '교집합; `--clip off` 로 끌 수 있다).  이유 둘:')
            md.append('')
            md.append(f'1. **STEP3 규약 일치** — 복셀 래스터화는 박스를 벗어난 재료를 버린다(크롭). '
                      f'클립하지 않으면 COMSOL 은 AM 을 {_pr["pct_of_am"]:.2f} % 더 많이 가진 '
                      '다른 물체가 되어 σ 대조(§4)가 성립하지 않는다.')
            md.append(f'2. **플레이튼 BC** — z 로 관통한 **{_pr["n_z"]}** 개가 박스 상/하면을 뚫으면 '
                      '그 자리에 AM 면이 없어 `adjAM ∩ selTop` 이 비고 **AM-집전체 접촉이 통째로 '
                      '누락**된다.  클립하면 잘린 단면이 정확히 플레이튼 평면에 놓여 접촉 패치가 된다.')
            md.append('')
            md.append('한계: 주기 킷이라면 넘어간 부분의 **반대편 이미지는 복원하지 않는다** '
                      '(java Block = 절연벽).  이는 `se_domain.periodic_xy` 경고와 같은 한계이며, '
                      '측면 절연벽 대조를 위해서는 STEP3 도 절연-벽으로 재런해야 한다.')
        else:
            md.append('→ `--clip off` 로 **클립하지 않았다**.  위 두 문제(σ 대조 불성립 · '
                      'AM-집전체 접촉 누락)가 그대로 남으니 §4 대조 전에 반드시 확인할 것.')
        md.append('')
    md.append('### 3-1) repair tolerance — 이 패키지의 실측 표 (tol 하나로는 불가능)')
    md.append('')
    _cs = pkg['contacts']
    _dv = sorted(c['delta_um'] for c in _cs if (c['delta_um'] or 0) > 0)
    _gv = sorted(c['gap_um'] for c in _cs
                 if c.get('gap_um') is not None and c['gap_um'] > 0)
    if not _dv:
        md.append('_접촉 데이터 없음 — 표 생략._')
    else:
        md.append(f'겹침 접촉 **{len(_dv)}** 개 (δ {_dv[0]*1000:.1f}~{_dv[-1]*1000:.0f} nm)'
                  + (f' · 근접-비겹침 **{len(_gv)}** 개 (gap {_gv[0]*1000:.1f}~{_gv[-1]*1000:.0f} nm)'
                     if _gv else ' · gap 컬럼 없음(구 pkg — 틈 통계 불가)'))
        md.append('')
        if _gv and _gv[-1] > _dv[0]:
            md.append(f'⚠ **δ 구간과 gap 구간이 겹친다** ({_dv[0]*1000:.1f}–{_dv[-1]*1000:.0f} nm '
                      f'vs {_gv[0]*1000:.1f}–{_gv[-1]*1000:.0f} nm) → tolerance 하나로 '
                      '"접촉 보존"과 "틈 제거"를 **동시에 만족시킬 수 없다**.')
            md.append('')
        md.append('| tol (nm) | 삼켜질 접촉 | 스냅될 틈 |')
        md.append('|---|---|---|')
        for tol_nm in (0.5, 1, 2, 5, 10, 20, 50, 100):
            t_um = tol_nm / 1000.0
            eat = sum(1 for d in _dv if d < t_um)
            snap = sum(1 for g in _gv if g < t_um)
            mark = ' ← **권장**' if tol_nm == 1 else (' ★위험' if eat > 0.15 * len(_dv) else '')
            md.append(f'| {tol_nm:g} | {eat} ({100*eat/len(_dv):.1f} %) | '
                      + (f'{snap} ({100*snap/len(_gv):.1f} %)' if _gv else '—') + f' |{mark}')
        md.append('')
        md.append('**권장**: tol 을 **≤1–2 nm** 로 두어 접촉을 보존한다 (그 위로 올리면 접촉이 '
                  '두 자릿수 % 로 소멸해 σ_e 가 통째로 낮아진다).  남는 sliver 는 tol 이 아니라 '
                  '**mesh 세분**(autoMeshSize 4→3→2)으로 다룬다.')
        if _gv:
            md.append('')
            md.append(f'**틈 {len(_gv)} 개는 tol 로 못 닫는다** — 다 닫으려면 '
                      f'tol ≥ {_gv[-1]*1000:.0f} nm 인데 그 값이면 접촉 '
                      f'{100*sum(1 for d in _dv if d < _gv[-1])/len(_dv):.0f} % 가 소멸한다.  '
                      '또 tol 로 스냅시키면 **점접촉 특이점**이 되어 컨덕턴스가 요소크기에 '
                      '비례 → mesh 를 조일수록 σ_e 가 흘러내린다(비수렴).  '
                      '⇒ **브릿지 실린더 TODO(trackb) T2 가 유일한 해법** '
                      '(r = max(a_hertz, ~1.2·vox), STEP3 rasterize 와 같은 회로 + 물리 넥 면적).')
    md.append('| VGCF Edge 전류 feature | 미정 (버전/모듈) | TODO(trackb) — 첫 실행 시 확정 |')
    md.append('| 고립 AM 클러스터 | singular matrix | ec 선택에서 고립 클러스터 제외 (TODO 주석) |')
    md.append('| dset1/dset2 매핑 | 빈 표 | Results 에서 데이터셋 재지정 |')
    md.append('')
    md.append('## 4) σ_eff 교차대조 (B1 목적) — 실행 후 이 표를 채운다')
    md.append('')
    md.append('솔브 산출: `comsol_sigma_e_eff.txt` / `comsol_sigma_ion_eff.txt` (단위 S/m; ÷100 = S/cm).')
    md.append('')
    md.append('| 채널 | COMSOL (S/cm) | STEP3 (S/cm) | 비고 |')
    md.append('|---|---|---|---|')
    _ref = (se.get('step3_reference') or {})
    _se_ref = _ref.get('sigma_e_eff_S_cm')
    md.append('| σ_e (AM 망) | _실행 후 기입_ | ' + (fmt(_se_ref) if _se_ref is not None
              else '— (metrics 에 step3.sigma_e_eff 부재)') +
              ' | ⚠ 혼입원 3: ① collector 규약(기하절단 vs STEP3 crown-band, −0.8% 하한 실측) '
              '② 근접-비겹침 72쌍류 개회로 — 브릿지(T2) 전 σ_e 대조 무효 '
              '③ 첨가제 킷은 STEP3 가 carbon 포함 — **AM-only(SBE) STEP3 런과만** 대조 |')
    md.append(f'| σ_ion (SE 연속체) | _실행 후 기입_ | {fmt(sig_ion_step3)} '
              f'(= σ_bulk·φ_full/τ_full = {fmt(se.get("sigma_bulk_ion_S_cm"))}·'
              f'{fmt(se.get("phi_full"))}/{fmt(se.get("tau_full"))}) | κ_dom 이중계상 가드 검증.  '
              f'⚠ 복셀 계단 편향으로 COMSOL 이 이 기대치를 **+10~20% 상회하는 것이 정상** '
              f'(vox {fmt(se.get("vox_um"), "µm")} 기준, conventions §7) |')
    md.append('')
    md.append('### geo-probe 2-런 재규격 (κ_dom 복셀 편향 소거 — 권장)')
    md.append('')
    md.append('1. `kdom_S_m` 파라미터에 **σ_bulk×100** (= sigma_bulk_ion_S_cm ×100 S/m) 를 넣고')
    md.append('   std2(이온) 만 재솔브 → `σ_eff_probe` 기록 (모델 자신의 AM-장애물 기하 응답).')
    md.append('2. `κ_dom\' = σ_bulk² · (φ_full/τ_full) / σ_eff_probe` 로 재설정 후 본 솔브.')
    md.append('   (선형성: σ_eff ∝ 도메인 σ.  복셀-τ_geo 대신 모델 자신의 D_geo 를 쓰므로')
    md.append('   계단 편향 +13~16%@vox0.4 가 정의상 소거된다.)')
    if se.get('periodic_xy'):
        md.append('')
        md.append('⚠ **periodic 킷**: STEP3 τ/κ 는 x,y 주기-BC 산출 — 이 java Block 은 절연벽.')
        md.append('   B1 은 절연-벽 STEP3 재런과만 비교 (D_geo 주기↔절연 +5.1% 실측).')
    md.append('')
    md.append(f'- porosity: {fmt(se.get("porosity_pct"), "%")} ({se.get("porosity_convention") or "—"})'
              f' · thickness: {fmt(se.get("thickness_um"), " µm")} · kdom_ratio: '
              f'{fmt(se.get("kdom_ratio"))} · φ_geo/τ_geo: {fmt(se.get("phi_geo"))}/'
              f'{fmt(se.get("tau_geo"))}')
    md.append('- 일치 기대치: σ_ion 은 κ_dom 정의상 STEP3 복셀해와 같은 유효값을 재현해야 한다'
              ' (차이 = 메시/기하 해상 오차).  σ_e 는 STEP3 복셀(1-voxel 넥 양자화) vs COMSOL'
              ' δ 렌즈 해상 — 차이 자체가 Track-B 의 정보다.')
    if pkg['contacts']:
        gsum = sum(c['g_holm_S'] for c in pkg['contacts'])
        dmax = max(c['delta_um'] for c in pkg['contacts'])
        md.append(f'- AM-AM Holm 교차대조: Σg = {gsum:.6g} S (n={len(pkg["contacts"])}, '
                  f'δ_max = {dmax:.4g} µm) — COMSOL 넥 전류와 차수 비교용.')
    md.append('')
    md.append('## 5) 남은 TODO(trackb)')
    md.append('')
    for t in todos:
        md.append('- [ ] ' + t.replace('\n', ' ').strip())
    md.append('')
    md.append('## 6) 입력 provenance (자기서술 — 산출물이 실행조건을 스스로 말한다)')
    md.append('')
    for fn in ('manifest.json', 'am_spheres.csv', 'am_am_contacts.csv', 'vgcf_fibres.csv',
               'se_domain.json', 'electrochem.json'):
        p = pkg['dir'] / fn
        md.append(f'- `{fn}`: ' + (f'md5 `{_md5(p)}`' if p.exists() else '(없음)'))
    notes = man.get('notes') or []
    if notes:
        md.append('- manifest.notes: ' + ' / '.join(str(n) for n in notes))
    md.append('')

    out = out_dir / 'README_run.md'
    out.write_text('\n'.join(md), encoding='utf-8')
    return out


# ───────────────────────────── --mph 재생 경로 ─────────────────────────────

def run_mph(pkg: dict, steps, out_dir: Path) -> int:
    """MPh 로 같은 IR 을 라이브 재생해 .mph 저장.  mph 없으면 안내 후 정상 종료(0)."""
    try:
        import mph  # noqa: F401
    except ImportError:
        print('MPh(pymph) 미설치 — 이 머신에서는 .mph 를 직접 만들 수 없다.')
        print('권장 경로(라이선스 머신 1커맨드):')
        print(f'  comsol batch -inputfile model_build.java -outputfile {pkg["case"]}.mph')
        print('MPh 경로를 쓰려면 COMSOL 설치 머신에서: pip install mph  →  --mph 재실행.')
        return 0
    try:
        import mph
        client = mph.start()
        pym = client.create(pkg['case'])
        model = pym.java
        fails = []
        # java 텍스트와 같은 IR 을 재생 — 각 스텝 개별 try (첫 실행 디버깅 왕복 전제)
        def replay(sts):
            for st in sts:
                if st[0] == 'call':
                    try:
                        obj = model
                        for method, args in st[1]:
                            conv = [list(a[1]) if isinstance(a, tuple) and a[0] in
                                    ('S[]', 'D[]', 'S[][]') else a for a in args]
                            obj = getattr(obj, method)(*conv)
                    except Exception as e:  # noqa: BLE001 — feature 명 확정용 수집
                        fails.append((_emit_call(st[1]), f'{type(e).__name__}: {e}'))
                elif st[0] == 'tryblock':
                    replay(st[2])
        replay(steps)
        out = out_dir / f'{pkg["case"]}.mph'
        pym.save(str(out))
        print(f'.mph 저장: {out}')
        if fails:
            print(f'⚠ 재생 중 실패 스텝 {len(fails)}개 — feature 명 확정 대상 (TODO(trackb)):')
            for call, err in fails[:20]:
                print(f'  {call}\n    → {err}')
        return 0 if not fails else 1
    except Exception as e:  # noqa: BLE001 — 크래시 금지 계약
        print(f'MPh 경로 실패 ({type(e).__name__}: {e}) — java 경로를 쓰세요:')
        print(f'  comsol batch -inputfile model_build.java -outputfile {pkg["case"]}.mph')
        return 1


# ───────────────────────────── 메인 빌드 ─────────────────────────────

def build(pkg_dir: Path, out_dir: Path | None = None, clip: str = 'auto') -> dict:
    pkg = load_pkg(Path(pkg_dir))
    out_dir = Path(out_dir) if out_dir else pkg['dir']
    out_dir.mkdir(parents=True, exist_ok=True)
    steps, todos, ctx = build_steps(pkg, clip=clip)
    java_text = render_java(steps, _header_comment(pkg))
    java_path = out_dir / 'model_build.java'
    java_path.write_text(java_text, encoding='utf-8')
    readme_path = write_readme(pkg, ctx, todos, out_dir)
    for w in pkg['warnings']:
        print(f'⚠ {w}')
    print(f'생성: {java_path}')
    print(f'생성: {readme_path}')
    print(f'다음(라이선스 머신): comsol batch -inputfile {java_path.name} '
          f'-outputfile {pkg["case"]}.mph')
    return {'pkg': pkg, 'steps': steps, 'todos': todos, 'ctx': ctx,
            'java': java_path, 'readme': readme_path, 'java_text': java_text}


# ───────────────────────────── selftest ─────────────────────────────

def _write_synth_pkg(root: Path, with_fibre: bool) -> Path:
    """합성 comsol_pkg — 스피어 3개(2개 겹침), κ_dom 지정, electrochem 일부 null (§F1 경로)."""
    d = root / ('comsol_pkg_selftest' + ('_vg' if with_fibre else ''))
    d.mkdir(parents=True, exist_ok=True)
    (d / 'manifest.json').write_text(json.dumps({
        'schema_version': '1.0', 'case': 'selftest' + ('_vg' if with_fibre else ''),
        'source': 'mpm', 'tau_convention': TAU_CONVENTION,
        'files': ['am_spheres.csv', 'am_am_contacts.csv', 'vgcf_fibres.csv',
                  'se_domain.json', 'electrochem.json'],
        'git_commit': 'deadbeef', 'notes': ['synthetic selftest package']},
        ensure_ascii=False, indent=1), encoding='utf-8')
    (d / 'am_spheres.csv').write_text(
        '# synthetic spheres — 2 overlapping AM_P (delta=0.8um) + 1 AM_S\n'
        'id,x_um,y_um,z_um,r_um,cls,sigma_e_S_cm,f_cov_reaction,f_cov_carbon,f_cov_block,f_cov_source\n'
        '0,3.0,5.0,4.0,2.0,AM_P,0.005,0.45,0.05,0.02,mpm_facewalk\n'
        '1,6.2,5.0,4.0,2.0,AM_P,0.005,0.50,0.04,0.02,mpm_facewalk\n'
        '2,5.0,5.0,9.0,1.5,AM_S,0.010,0.60,0.03,0.01,class_mean_fallback\n',
        encoding='utf-8')
    (d / 'am_am_contacts.csv').write_text(
        '# R*=ri*rj/(ri+rj); a=sqrt(R**delta); sigma_c=2*si*sj/(si+sj) [S/cm]; '
        'g=2*sigma_c*(a_um*1e-4) [S] (Holm)\n'
        'i,j,delta_um,a_hertz_um,g_holm_S\n'
        '0,1,0.8,0.894427,8.94427e-07\n', encoding='utf-8')
    if with_fibre:
        (d / 'vgcf_fibres.csv').write_text(
            '# diameter_um=0.15, sigma_S_cm=100.0\n'
            'fibre_id,seq,x_um,y_um,z_um\n'
            '0,0,1.0,1.0,0.5\n0,1,2.0,3.0,4.0\n0,2,2.5,5.0,8.0\n', encoding='utf-8')
    else:
        (d / 'vgcf_fibres.csv').write_text(
            '# diameter_um=0.15, sigma_S_cm=100.0\n'
            '# no fibre data for this case — see manifest.notes\n'
            'fibre_id,seq,x_um,y_um,z_um\n', encoding='utf-8')
    (d / 'se_domain.json').write_text(json.dumps({
        'sigma_bulk_ion_S_cm': 3.0e-3, 'kappa_dom_S_cm': 2.1e-3, 'kappa_dom_S_m': 0.21,
        'kdom_ratio': 0.7, 'tau_full': 2.0, 'tau_geo': 1.4, 'phi_full': 0.466,
        'phi_geo': 0.666, 'tau_convention': TAU_CONVENTION, 'porosity_pct': 12.3,
        'porosity_convention': 'sphere-sum', 'thickness_um': 12.0,
        'box_um': [10.0, 10.0, 12.0], 'mixed_phase': None, 'source': 'mpm'},
        indent=1), encoding='utf-8')
    (d / 'electrochem.json').write_text(json.dumps({
        'i0_A_m2': None, 'alpha_a': 0.5, 'alpha_c': 0.5, 'D_s_m2_s': None,
        'c_max_mol_m3': 49000.0, 'x0': 0.264, 'x100': 0.9084, 'asr_film_ohm_m2': None,
        'r_int_ohm_cm2': None, 'T_C': 25.0, 'ocp_csv': None,
        # ★ 익스포터 실형태 (리뷰 critical 회귀 고정): comsol_export 는 사유를
        #   provenance['reason'] = {필드명: str} 서브딕트로 쓴다 — selftest 가 자기 관례의
        #   합성 데이터로만 검사하면 이 드리프트를 못 잡는다 (실제로 못 잡았다).
        'provenance': {'reason': {'i0_A_m2': 'no SC/PC i0 anchor in literature (sweep-only)',
                                  'D_s_m2_s': 'bimodal D_s deferred to step4 flags'},
                       'note': 'synthetic selftest'}}, indent=1), encoding='utf-8')
    return d


def selftest() -> int:
    import subprocess
    import tempfile
    checks = []

    def ok(name, cond):
        checks.append((name, bool(cond)))
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    with tempfile.TemporaryDirectory(prefix='comsol_selftest_') as td:
        root = Path(td)
        pkg_a = _write_synth_pkg(root, with_fibre=False)
        pkg_b = _write_synth_pkg(root, with_fibre=True)
        res_a = build(pkg_a)
        res_b = build(pkg_b)
        ja, jb = res_a['java_text'], res_b['java_text']

        # 1) 골격
        ok('java: public class model_build + public static Model run()',
           'public class model_build {' in ja and 'public static Model run()' in ja)
        # 2) 중괄호 균형 (running non-negative 는 render_java 가 이미 보증 — 총합 재확인)
        ok('java: 중괄호 균형', ja.count('{') == ja.count('}'))
        # 3) 스피어 feature 3개
        ok('geometry: Sphere feature 3개', ja.count('"Sphere"') == 3)
        # 4) κ_dom S/m 리터럴
        ok('SE: kdom_S_m = 0.21[S/m] 리터럴',
           '"kdom_S_m"' in ja and '"0.21[S/m]"' in ja)
        # 5) null → 파라미터 미생성 + TODO 주석 (§F1)
        ok('§F1: i0 null → param 미생성', '.set("i0"' not in ja)
        ok('§F1: i0 null → TODO(trackb) 주석 + reason',
           'TODO(trackb): i0 (i0_A_m2)' in ja and 'no SC/PC i0 anchor' in ja)
        ok('§F1: D_s null → TODO 주석', 'TODO(trackb): D_s (D_s_m2_s)' in ja)
        # 6) 'None'/'nan' 미검출 (단어 경계)
        leak = any(re.search(r'(?<![A-Za-z_])' + b + r'(?![A-Za-z_])', ja)
                   for b in ('None', 'NaN', 'nan'))
        ok("null 문자열('None'/'nan') 미검출", not leak)
        # 7) single-ion 경고
        ok('single-ion 경고 문자열 (DFN 금지)', 'single-ion' in ja and 'DFN' in ja)
        # 8) form union + Hertz 넥 근거
        ok('form UNION + Hertz 넥 주석', '("action", "union")' in ja and 'Hertz' in ja)
        # 9) 선택/재료/물리 배선
        ok('BallSelection 6개 (도메인3 + 경계3)', ja.count('"BallSelection"') == 6)
        ok('materials: electricconductivity 3상 (AMP/AMS/SE)',
           ja.count('"electricconductivity"') == 3)
        ok('physics: ConductiveMedia ×2 (ec 전자 + ec2 이온)',
           ja.count('"ConductiveMedia"') == 2)
        # 10) σ_e 단위 변환 (0.010 S/cm → 1 S/m)
        ok('AM_S σ_e ×100 변환 (1[S/m])', '"sigma_e_AMS_S_m", "1[S/m]"' in ja)
        # 11) fcov 파라미터 (B2 매핑 준비)
        ok('fcov_r_<id> 파라미터', '"fcov_r_0"' in ja and '"fcov_r_2"' in ja)
        # 12) VGCF: 헤더만 → 절 전체 주석 / 데이터 → InterpolationCurve
        ok('VGCF 헤더-only → 기하 미생성 + 사유 주석',
           '"InterpolationCurve"' not in ja and 'vgcf_fibres.csv' in ja)
        ok('VGCF 데이터 → InterpolationCurve 생성', '"InterpolationCurve"' in jb
           and '"vgcf0"' in jb)
        # 13) README
        rd = res_a['readme'].read_text(encoding='utf-8')
        ok('README_run.md: comsol batch 1커맨드',
           'comsol batch -inputfile model_build.java' in rd)
        ok('README_run.md: STEP3 대조표 + TODO 목록',
           '교차대조' in rd and 'TODO(trackb)' in rd)
        # 14) --mph 가드: mph 미설치 → 안내 후 정상 종료 (별도 프로세스로 실제 CLI 경로 검증)
        proc = subprocess.run([sys.executable, os.path.abspath(__file__), str(pkg_a), '--mph'],
                              capture_output=True, text=True, timeout=120)
        guard_ok = (proc.returncode == 0 and 'comsol batch' in proc.stdout)
        try:
            import mph  # noqa: F401
            # mph 가 있는 머신에서는 가드 문구 대신 실제 빌드가 돈다 — rc 만 본다
            guard_ok = proc.returncode in (0, 1)
        except ImportError:
            guard_ok = guard_ok and ('MPh' in proc.stdout)
        ok('--mph 가드: 미설치 안내 + 비정상종료 아님', guard_ok)

        # ── 심화리뷰 회귀 3종 (2026-08-05) ─────────────────────────────────────────────
        # 15) mixed-크래시 회귀: se_domain κ/σ_bulk 모두 null + reason 에 bare 'None' 토큰
        #     (수정 전 exporter 실산출 형태) — §F1 누출가드가 오탐해 SDCP 킷 전부 빌드 불가였다.
        import shutil as _sh
        pkg_m = pkg_a.parent / 'pkg_mixed_regr'
        if pkg_m.exists():
            _sh.rmtree(pkg_m)
        _sh.copytree(pkg_a, pkg_m)
        _sed = json.loads((pkg_m / 'se_domain.json').read_text())
        _sed.update({'kappa_dom_S_cm': None, 'kappa_dom_S_m': None, 'sigma_bulk_ion_S_cm': None,
                     'kdom_ratio': None,
                     'reason': 'trackb 부분실패 | κ_dom 산출 불가 — 부재/None 항목: kdom_ratio, '
                               'tau_full (§F1: null)',
                     'mixed_phase': {'reason': 'unequal sigma_ion (MIX-R)'}})
        (pkg_m / 'se_domain.json').write_text(json.dumps(_sed, ensure_ascii=False))
        out_m = pkg_a.parent / 'mph_mixed_regr'
        try:
            build(pkg_m, out_m)
            jm = (out_m / 'model_build.java').read_text()
            ok("15) mixed-크래시 회귀: 'None' 토큰 reason 도 빌드 완주 (무해화 벨트)",
               'null 항목' in jm)                       # 토큰이 null 로 무해화되어 실림
            # 16) both-null κ: se_domain.reason 최우선 + mixed_phase.reason 병기 + matSE 미생성
            ok('16) both-null κ TODO: se_domain.reason 전달 + mixed 병기 + SE 재료 미생성',
               'trackb 부분실패' in jm and 'MIX-R' in jm and '"matSE"' not in jm)
        except Exception as _e:
            ok('15) mixed-크래시 회귀: 빌드 완주', False)
            ok('16) both-null κ TODO 전달', False)
        # 17) sigma_bulk_source 폴백 라벨이 java 출처 주석에 실린다 (25°C 상수 출처 소실 방지)
        pkg_f = pkg_a.parent / 'pkg_fallback_regr'
        if pkg_f.exists():
            _sh.rmtree(pkg_f)
        _sh.copytree(pkg_a, pkg_f)
        _sef = json.loads((pkg_f / 'se_domain.json').read_text())
        _sef.update({'kappa_dom_S_cm': None, 'kappa_dom_S_m': None, 'kdom_ratio': None,
                     'sigma_bulk_ion_S_cm': 0.003, 'sigma_bulk_source': 'default_25C_const'})
        (pkg_f / 'se_domain.json').write_text(json.dumps(_sef, ensure_ascii=False))
        out_f = pkg_a.parent / 'mph_fallback_regr'
        build(pkg_f, out_f)
        jf = (out_f / 'model_build.java').read_text()
        ok('17) sigma_bulk_source 라벨이 출처 주석에 병기 (킷 측정값 아님 명시)',
           'default_25C_const' in jf and '킷 측정값 아님' in jf)

    # ── 18) 메서드 분할: JVM 64 KB Code 한도 (미분할이면 javac 이 실제로 거부한다) ──
    big = [('call', [('component', ('comp1',)), ('geom', ('geom1',)),
                     ('feature', (f'sph{i}',)), ('set', ('pos', ('D[]', [1.0, 2.0, 3.0])))])
           for i in range(2000)]
    jbig = render_java(big, 'split test')
    n_parts = jbig.count('private static void part')
    ok(f'18) 대형 모델 자동 분할 (문장 2000 → part {n_parts} 개, run() 이 순서대로 호출)',
       n_parts >= 4 and all(f'part{i}(model);' in jbig for i in range(n_parts))
       and jbig.index('part0(model);') < jbig.index('private static void part0'))
    _mx = max(len(p) for p in _split_steps(big))
    ok(f'18b) part 당 문장 상한 준수 (최대 {_mx} ≤ {2 * _MAX_STMTS_PER_PART})',
       _mx <= 2 * _MAX_STMTS_PER_PART)
    _tb = [('call', [('param', ()), ('set', ('a', 'b'))])] * 700 + \
          [('tryblock', 'x', [('call', [('study', ('std1',)), ('run', ())])])]
    ok('18c) tryblock 은 part 중간에서 쪼개지지 않는다',
       all(sum(1 for s in p if s[0] == 'tryblock') <= 1 for p in _split_steps(_tb))
       and render_java(_tb, 't').count('try {') == 1)

    # ── 19) RVE 클립: 박스 밖 스피어 통계 + on/off ──
    _sp = [{'id': 'a', 'x': 1.0, 'y': 5.0, 'z': 5.0, 'r': 2.0, 'cls': 'AM_P'},   # x 로 삐져나감
           {'id': 'b', 'x': 5.0, 'y': 5.0, 'z': 5.0, 'r': 2.0, 'cls': 'AM_P'}]   # 안쪽
    _pr = _protrusion(_sp, 10.0, 10.0, 10.0)
    _cap_exact = math.pi * 1.0 ** 2 * (3 * 2.0 - 1.0) / 3.0        # h=1, r=2 → π·5/3
    ok(f'19) _protrusion: 삐져나온 구 {_pr["n_any"]}/2 · 캡 체적 {_pr["v_out_um3"]:.4f} '
       f'(해석해 {_cap_exact:.4f})',
       _pr['n_any'] == 1 and _pr['n_lat'] == 1 and _pr['n_z'] == 0
       and abs(_pr['v_out_um3'] - _cap_exact) < 1e-9)
    ok('19b) 박스 안에만 있으면 클립 안 함 (auto)',
       _protrusion(_sp[1:], 10.0, 10.0, 10.0)['n_any'] == 0)

    pk_clip = load_pkg(_write_synth_pkg(root, with_fibre=False))
    j_on = render_java(build_steps(pk_clip, clip='on')[0], 'clip on')
    j_off = render_java(build_steps(pk_clip, clip='off')[0], 'clip off')
    ok('19c) --clip on → uniAM/clipAM 생성, off → 미생성',
       '"clipAM", "Intersection"' in j_on and '"uniAM", "Union"' in j_on
       and 'clipAM' not in j_off)

    # ── 20) 단위 사슬: lengthUnit 이 기하 feature 보다 먼저 (맨수 = µm 보장) ──
    ok('20) lengthUnit("µm") 가 첫 기하 feature 보다 앞',
       ('lengthUnit' in j_on) and j_on.index('lengthUnit(') < j_on.index('"blk1", "Block"'))
    ok('20b) 길이 파라미터는 [um] 단위 명시 (기하 단위와 무관하게 안전)',
       'model.param().set("L_x", "' in j_on and '[um]"' in j_on)

    n_pass = sum(1 for _, c in checks if c)
    print(f'\nselftest {n_pass}/{len(checks)} PASS')
    return 0 if n_pass == len(checks) else 1


# ───────────────────────────── CLI ─────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description='comsol_pkg(스키마 v1.0) → model_build.java + README_run.md '
                    '(+ --mph: MPh 라이브 빌드)')
    ap.add_argument('pkg_dir', nargs='?', help='comsol_pkg_<case> 디렉토리')
    ap.add_argument('--out', default=None, help='산출 디렉토리 (기본: 패키지 안)')
    ap.add_argument('--mph', action='store_true',
                    help='MPh(pymph)로 같은 빌드를 라이브 재생해 .mph 저장 (COMSOL 설치 머신 전용; '
                         '미설치면 안내 후 종료)')
    ap.add_argument('--clip', choices=('auto', 'on', 'off'), default='auto',
                    help='박스 밖으로 삐져나온 AM 스피어를 RVE 로 잘라낸다 (STEP3 복셀 크롭 규약과 '
                         '일치).  auto=삐져나온 게 있으면 클립 (기본), off=원본 그대로(플레이튼 '
                         '관통 시 AM-집전체 접촉 누락 주의)')
    ap.add_argument('--selftest', action='store_true', help='합성 패키지로 자기검증')
    a = ap.parse_args()

    if a.selftest:
        sys.exit(selftest())
    if not a.pkg_dir:
        ap.error('pkg_dir 필요 (또는 --selftest)')
    res = build(Path(a.pkg_dir), Path(a.out) if a.out else None, clip=a.clip)
    if a.mph:
        sys.exit(run_mph(res['pkg'], res['steps'],
                         Path(a.out) if a.out else res['pkg']['dir']))


if __name__ == '__main__':
    main()
