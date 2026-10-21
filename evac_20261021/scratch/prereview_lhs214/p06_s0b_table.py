#!/usr/bin/env python3
"""P06 — S0b 상태 표 · 지문 닮은꼴 (함수 수준 · 빠름).
도구 파일 (HEAD) 의 _selftest 안 fp_state · s0b_fp 를 AST 로 그대로 떼어 (글자 그대로 · 고치지 않음) 실행하고, 도구의 registration_values 로 읽은
등록 사본 쌍 (보충 · 194) 마다 판정을 손 기대와 비교한다.  사본은 이 탐침이 직접 만든다 (도구의 reg_variant 를 쓰지 않음 — 독립 변환).
비교: 옛 S0b 식 (a69963967 판 619–623 줄: R startswith e8b2496b and (P None or startswith 2149f873)) 의 판정도 함께.
재실행: cd <worktree> && python3 -I p06_s0b_table.py <worktree> <out.json>"""
import ast, hashlib, json, re, subprocess, sys, tempfile, textwrap
from pathlib import Path
WT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
sys.path.insert(0, str(WT / 'scripts'))
import run_network_194_parallel as N      # noqa: E402
import supp20_input_receipt as S          # noqa: E402

SUPP = 'docs/reviews/lhs_network_batch_registration_20261012_supp20.md'
B194 = 'docs/reviews/lhs_network_batch_registration_20261007_g2.md'
fp_now = N.code_fp(N.code_hashes())
OLD = 'e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71'
X1 = hashlib.sha256(b'prereview lhs214 x1').hexdigest()
X2 = hashlib.sha256(b'prereview lhs214 x2').hexdigest()

# ── 도구의 nested 함수 둘을 글자 그대로 떼어 실행 ──
src = (WT / 'scripts/supp20_input_receipt.py').read_text(encoding='utf-8')
tree = ast.parse(src)
st = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == '_selftest'][0]
want = {}
for n in st.body:
    if isinstance(n, ast.FunctionDef) and n.name in ('fp_state', 's0b_fp'):
        want[n.name] = ast.get_source_segment(src, n)
assert set(want) == {'fp_state', 's0b_fp'}, want.keys()
ns = dict(fp_now=fp_now)
exec(textwrap.dedent(want['fp_state']), ns)
exec(textwrap.dedent(want['s0b_fp']), ns)
fp_state, s0b_fp = ns['fp_state'], ns['s0b_fp']


def git_show(rev, f):
    return subprocess.run(['git', 'show', f'{rev}:{f}'], cwd=WT, capture_output=True, check=True).stdout.decode('utf-8')


RAT = {SUPP: git_show('HEAD', SUPP), B194: git_show('HEAD', B194)}            # 비준 (registered)
PEN = {SUPP: git_show('fe23f2b83', SUPP), B194: git_show('fe23f2b83', B194)}  # 비준 전 (pending · 커밋된 실물)


def s3_bounds(t):
    """독립 §3 경계 — '\n## 3.' 줄부터 다음 '\n## ' 앞까지 (이 탐침의 사본 만들기용 · 판정은 도구가)."""
    i = t.find('\n## 3.')
    j = t.find('\n## ', i + 1)
    return i, (j if j >= 0 else len(t))


def s3_sub(t, new_token_text):
    """활성 §3 안의 첫 `code_fp <64hex>` 토큰 (백틱 포함) 을 new_token_text 로."""
    i, j = s3_bounds(t)
    m = re.search(r'`code_fp [0-9a-f]{64}`', t[i:j])
    assert m, 'no §3 token'
    a = i + m.start()
    return t[:a] + new_token_text + t[a + len(m.group(0)):]


def s3_append(t, line):
    i, j = s3_bounds(t)
    return t[:j] + '\n' + line + '\n' + t[j:]


def s9_append(t, line):
    return t + '\n' + line + '\n'


tmp = Path(tempfile.mkdtemp(prefix='p06_', dir=str(OUT.parent)))
k = 0


def rv(text):
    global k
    k += 1
    p = tmp / f'doc_{k}.md'
    p.write_text(text, encoding='utf-8')
    return S.registration_values(reg_doc=str(p))


def old_s0b(v):
    R, P = v.get('code_fp'), v.get('code_fp_pending')
    return str(R or '').startswith('e8b2496b') and (P is None or str(P).startswith('2149f873'))


rows = []


def case(name, supp_txt, b194_txt, expect, note=''):
    vs, ps = rv(supp_txt)
    vb, pb = rv(b194_txt)
    ok, why = s0b_fp(vs, vb, pb)
    rows.append(dict(case=name, expect=expect, got=bool(ok), match=(bool(ok) == expect), why=why, note=note,
                     state_supp=fp_state(vs, fp_now)[0], state_194=fp_state(vb, fp_now)[0],
                     supp=(vs.get('code_fp'), vs.get('code_fp_pending')), supp_fp_problems=[x for x in ps if x.startswith('등록 문서 code_fp')],
                     b194=(vb.get('code_fp'), vb.get('code_fp_pending')), b194_fp_problems=[x for x in pb if x.startswith('등록 문서 code_fp')],
                     old_s0b=old_s0b(vs)))


R_, P_ = RAT, PEN
# ── 1. 상태 표 ──
case('T01 둘 다 registered (HEAD 실물)', R_[SUPP], R_[B194], True)
case('T02 둘 다 pending (비준 전 실물 fe23f2b83)', P_[SUPP], P_[B194], True)
case('T03 보충 registered · 194 pending', R_[SUPP], P_[B194], False, '한 문서만 비준')
case('T04 보충 pending · 194 registered', P_[SUPP], R_[B194], False, '한 문서만 비준 (S11g 에 없는 꼴)')
case('T05 둘 다 registered + 남은 대기 X1 (둘 다)', s9_append(R_[SUPP], f'| 대기 | `code_fp_pending {X1}` |'),
     s9_append(R_[B194], f'| 대기 | `code_fp_pending {X1}` |'), False, '둘 다 (등록 + 대기)')
case('T06 보충 registered + 남은 대기 X1 · 194 깨끗', s9_append(R_[SUPP], f'| 대기 | `code_fp_pending {X1}` |'), R_[B194], False)
case('T07 보충 깨끗 · 194 registered + 남은 대기 X1', R_[SUPP], s9_append(R_[B194], f'| 대기 | `code_fp_pending {X1}` |'), False)
case('T08 보충 registered + 대기 둘 (X1 · X2 · 상충) · 194 깨끗', s9_append(s9_append(R_[SUPP], f'| 대기 | `code_fp_pending {X1}` |'), f'| 대기 | `code_fp_pending {X2}` |'),
     R_[B194], False, '보충 쪽 상충 대기 (S11g 는 194 쪽만)')
case('T09 보충 깨끗 · 194 registered + 대기 둘 (상충)', R_[SUPP], s9_append(s9_append(R_[B194], f'| 대기 | `code_fp_pending {X1}` |'), f'| 대기 | `code_fp_pending {X2}` |'),
     False, '= S11g base_pending_conflict')
case('T10 보충 registered + 대기 = 등록 (모순) · 194 깨끗', s9_append(R_[SUPP], f'| 대기 | `code_fp_pending {fp_now}` |'), R_[B194], False, '보충 쪽 모순 대기')
case('T11 보충 깨끗 · 194 registered + 대기 = 등록 (모순)', R_[SUPP], s9_append(R_[B194], f'| 대기 | `code_fp_pending {fp_now}` |'), False)
case('T12 둘 다 아님 — 둘 다 §3 = X1 · 대기 없음', s3_sub(R_[SUPP], f'`code_fp {X1}`'), s3_sub(R_[B194], f'`code_fp {X1}`'), False, 'undeclared')
case('T13 둘 다 아님 — 둘 다 §3 = X1 · 대기 X2 (≠ 체크아웃)', s9_append(s3_sub(R_[SUPP], f'`code_fp {X1}`'), f'| 대기 | `code_fp_pending {X2}` |'),
     s9_append(s3_sub(R_[B194], f'`code_fp {X1}`'), f'| 대기 | `code_fp_pending {X2}` |'), False, 'undeclared')
case('T14 pending · 194 §3 다름 (보충 §3 e8b · 194 §3 X1 · 대기 둘 다 체크아웃)', P_[SUPP], s9_append(s3_sub(R_[B194], f'`code_fp {X1}`'), f'| 대기 | `code_fp_pending {fp_now}` |'), False)
case('T15 pending · 같은 엉뚱한 §3 X1 (둘 다) · 대기 = 체크아웃', s9_append(s3_sub(R_[SUPP], f'`code_fp {X1}`'), f'| 대기 | `code_fp_pending {fp_now}` |'),
     s9_append(s3_sub(R_[B194], f'`code_fp {X1}`'), f'| 대기 | `code_fp_pending {fp_now}` |'), True, '요청서 §6 이 적은 한정 (pending 은 발사 대조가 막음)')
case('T16 194 문서 없음', R_[SUPP], '', False, '194 를 못 읽음 → 값 None (문제 사유 = 다른 접두)')
case('T17 194 §3 제목 없음', R_[SUPP], R_[B194].replace('\n## 3.', '\n## 삼.', 1), False)
case('T18 194 §3 제목 둘', R_[SUPP], R_[B194] + f'\n## 3. 중복\n\n- `code_fp {fp_now}`\n', False)
case('T19 보충 문서 없음 (빈 글)', '', R_[B194], False)
# ── 2. 지문 닮은꼴 (보충 활성 §3 토큰 자리) — 기대: 도구 문법 (`code_fp <64 소문자 hex>`) 밖 = 값 아님 ──
look = {
    'L01 63 자리': f'`code_fp {fp_now[:63]}`', 'L02 65 자리': f'`code_fp {fp_now}0`', 'L03 대문자 hex': f'`code_fp {fp_now.upper()}`',
    'L04 백틱 안 앞 공백': f'` code_fp {fp_now}`', 'L05 백틱 안 뒤 공백': f'`code_fp {fp_now} `', 'L06 code_fp 뒤 공백 둘': f'`code_fp  {fp_now}`',
    'L07 NBSP 구분': f'`code_fp {fp_now}`', 'L08 전각 숫자': '`code_fp ' + fp_now.translate({ord(c): ord(c) + 0xFEE0 for c in '0123456789'}) + '`',
    'L09 탭 구분': f'`code_fp\t{fp_now}`', 'L10 백틱 없음': f'code_fp {fp_now}',
}
for nm, tok in look.items():
    case(f'{nm} (보충 §3 토큰만 · 194 정상)', s3_sub(R_[SUPP], tok), R_[B194], False, '보충 §3 값 없음 → undeclared 이어야')
case('L11 같은 칸 두 줄 같은 값 (보충 §3 끝에 같은 토큰 한 줄 더)', s3_append(R_[SUPP], f'- 다시 적음: `code_fp {fp_now}`'), R_[B194], True, '값 하나 (같음)')
case('L12 §3 안 둘째 값 = 역사 e8b (기계 구문)', s3_append(R_[SUPP], f'- 역사: `code_fp {OLD}`'), R_[B194], False, '값 둘 → None')
case('L13 §3 안 코드 블록 속 다른 값 + 정상 토큰', s3_append(R_[SUPP], f'```text\n`code_fp {X1}`\n```'), R_[B194], True, '코드 블록 값 = 읽지 않음')
case('L14 §3 정상 토큰을 코드 블록 안으로만', s3_sub(R_[SUPP], f'\n```text\n`code_fp {fp_now}`\n```\n'), R_[B194], False, '활성 값 없음')
case('L15 다른 절 (§9) 의 `code_fp <체크아웃>` + §3 = X1', s9_append(s3_sub(R_[SUPP], f'`code_fp {X1}`'), f'- `code_fp {fp_now}`'), R_[B194], False, '§3 밖은 읽지 않음')
case('L16 다른 절 (§9) 의 `code_fp X1` + §3 정상', s9_append(R_[SUPP], f'- `code_fp {X1}`'), R_[B194], True, '§3 밖은 읽지 않음')
case('L17 대기 선언 닮은꼴 (대문자 hex) — registered', s9_append(R_[SUPP], f'| 대기 | `code_fp_pending {X1.upper()}` |'), R_[B194], True, '도구 문법 밖 = 선언 아님 (사람 눈엔 남은 대기)')
case('L18 대기 선언 닮은꼴 (63 자리) — registered', s9_append(R_[SUPP], f'| 대기 | `code_fp_pending {X1[:63]}` |'), R_[B194], True, '같음')
case('L19 대기 선언이 코드 블록 안 — registered', s9_append(R_[SUPP], f'```text\n`code_fp_pending {X1}`\n```'), R_[B194], False,
     '대기는 문서 전체 (코드 블록 포함) 를 읽는다 → 남은 대기 (도구 receipt 는 rc 0)')
case('L20 194 §3 토큰 63 자리 (보충 정상)', R_[SUPP], s3_sub(R_[B194], f'`code_fp {fp_now[:63]}`'), False, '194 §3 값 없음 → 문제 → 거짓')
case('L21 194 §3 대문자 (보충 정상)', R_[SUPP], s3_sub(R_[B194], f'`code_fp {fp_now.upper()}`'), False)
case('L22 194 §3 안 둘째 값 역사 e8b', R_[SUPP], s3_append(R_[B194], f'- 역사: `code_fp {OLD}`'), False)

res = dict(fp_now=fp_now, extracted=sorted(want), n=len(rows), mismatches=[r['case'] for r in rows if not r['match']], rows=rows)
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
for r in rows:
    print(f"{'OK ' if r['match'] else 'XX '} {r['case']:<70.70} expect={r['expect']!s:5} got={r['got']!s:5} old={r['old_s0b']!s:5} "
          f"st={r['state_supp']}/{r['state_194']} supp_fp_probs={len(r['supp_fp_problems'])} why={r['why'][:70]}")
print('mismatches:', res['mismatches'])
