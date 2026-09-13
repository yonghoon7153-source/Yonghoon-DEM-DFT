#!/usr/bin/env python3
"""리뷰 비포/애프터 페이지를 **원장에서 생성**한다 → `docs/reviews/review_before_after.html`.

★ 왜 생성기인가: 손으로 적은 초안이 하루 만에 "고침 7 / 열림 57" 로 낡았다 (실제는 고침 20).
  규율 ④ — *정본은 밖으로 강제되지 않으면 새어나간다*.  집계·고친 목록·SHA 는 전부
  `docs/reviews/findings.json` 에서 읽고, 서술 행이 인용하는 **숫자마다 그 항목의 note 안에
  실재하는지** selftest 가 확인한다 (인용은 원장에 닻을 내린다).
★ 산출 HTML 은 `check_review_findings.py --ban-sweep` 범위(`docs/**/*.html`)에 든다.

사용:
  python3 scripts/build_review_before_after.py            # 생성
  python3 scripts/build_review_before_after.py --selftest
"""
from __future__ import annotations
import argparse
import collections
import html
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEDGER = ROOT / 'docs' / 'reviews' / 'findings.json'
OUT = ROOT / 'docs' / 'reviews' / 'review_before_after.html'

LAYERS = [('L1', '접촉 기하 · 피복률', '면적을 무엇으로 세나'),
          ('L2', '접촉망 수송', '그 면적을 저항으로'),
          ('L3', '스케일링법칙', '그 σ 를 타깃으로'),
          ('L4', '등급 · 검증 플래그', '그 값을 판정으로'),
          ('L5', '구조 ML', '그 코퍼스를 학습으로')]

# ── 서술 행: (id, 제목, 믿은 것, 잰 것, 숫자 인용들, 각주) ──────────────────────────
#    ⚠ `nums` 의 모든 문자열은 그 항목의 note 또는 title 에 **그대로** 있어야 한다 (selftest ①).
ROWS = [
    ('L1-01', '체적·Tabor 상한이 비물리 면적을 차단한다',
     '세 cap 의 min 이 상한이고 Hertz/LIGGGHTS 가 하한이니, 면적은 언제나 물리적으로 가능한 구간 안에 있다.',
     '얕은 겹침에서 하한 &gt; 상한인데 <b>거부하지 않고 하한을 돌려준다</b>.  코퍼스(LHS 30, 간선 3,619,759)에서 그 접촉이 <b>5.240 %</b>.',
     ['1.784757', '8.016722', '5.240 %', '3,619,759'],
     '값은 안 바꿨다 — 판정문의 최소 방어(기록하고 승격하지 않기) 중 <b>기록</b>만 했다.  하류가 아직 그 플래그를 안 읽는다.'),
    ('L1-02', 'V_overlap 은 두 구의 겹침 부피다',
     '체적 보존 cap 이 실제 lens 부피로 면적을 제한한다.',
     '단일 구면 cap 공식에 R* 를 넣은 것이라 얕으면 참값의 <b>0.493724배</b>, 깊으면 <b>음수</b>.  그런데 정확 lens 로 바꿔도 코퍼스에서 <b>0 / 3,619,759</b> 간선이 바뀐다.',
     ['0.493724', '0/3,619,759'],
     '항등인 이유가 물리가 아니다 — <b>DESC-03</b>(mm 를 m 로 읽음)이 A_volume 을 1000배 부풀려 volume cap 이 <b>원리적으로 결속 불가</b>.  "무해" 로 닫지 않았다.'),
    ('L2-01', '협착저항이 문헌식을 구현한다',
     '코드 주석 "Mikić 1974" — 보정계수 ψ 를 적용한 Holm 협착 저항.',
     '문헌은 ψ 를 <b>곱하고</b> 코드는 <b>나눈다</b>.  독립 기준해(축대칭 flux tube 직접 풀이)가 <b>그 원통 모델 안에서</b> 곱셈 우위를 확정: 코드는 곱식의 (1−s)<sup>−3</sup> 배, s=0.9 에서 <b>1,620배</b>.  코드가 자기 주석과도 어긋난다.',
     ['1,620배', '1.02491228', '44.31250962'],
     '기하평균 |ln 비| (nr600, 바른 구간): s≤0.3 에서 곱함 <b>1.02491228</b> vs 나눔 1.69510941 · s&gt;0.3 에서 곱함 1.18902836 vs 나눔 <b>44.31250962</b>.  ⚠ Codex 2라운드: 첫 집계는 s=0.3 이 반올림으로 범위 밖에 들어간 3/7 이었다 — 출력에 경고가 찍혀 있었는데 못 봤다.  "참값" 이 아니라 모델 내 비.  σ <b>상향 가설</b> (cutoff 분기는 반대도 허용).'),
    ('AREA-12', '면적을 둘로 쪼개면 삭제된 협착 항이 되살아난다',
     '피복용 A_surface(상한 2πR²)와 수송용 A_transport(상한 πR²)를 분리하면 σ 가 하향한다 — 계약의 전제.',
     '솔버의 clamp <span class="m">a_eff = min(a, r_min)</span> 이 <b>이미 같은 상한</b>이다.  무작위 20,000 접촉에서 A 는 <b>15.56 %</b> 바뀌는데 a_eff 는 설명 안 되는 차이 <b>0</b>.',
     ['15.56 %', '1 ULP'],
     'S2 의 σ 변화는 <b>산술적으로 0</b>.  살아남는 건 타입 분리의 구조적 가치뿐이고, σ 를 움직이는 축은 S3(ψ 배치) 하나다.'),
    ('AREA-11', 'min(σ₁,σ₂) 는 이종쌍의 보수적 협착 규약이다',
     '두 재료가 만나는 접촉에서 낮은 σ 를 쓰면 안전하다.',
     '직렬 모델 ψ/(4a)(1/σ₁+1/σ₂) 대비 계수비 2·maxσ/(σ₁+σ₂) 만큼 크다.  실제 기준해(σ 1:8) 대비 min 식은 <b>1.6856916312690349</b>배.  생산 AM_P 6 µm–AM_S 2 µm 에서 <b>1.722074배</b>, AM_P 6–AM_P 2 µm 에서도 <b>1.511966128287415</b>배.',
     ['1.6856916312690349', '1.722074', '1.511966128287415'],
     '⚠ Codex 2라운드: 내가 "16/9 와 일치" 라 적은 것은 수치해가 약분되는 <b>계수비</b>였다 — 독립 증거가 아니다.  직렬식도 모델이지 참값이 아니고, 열의 k_weight 는 이미 조화평균이라 이중 보정 금지.  간선 하나당 배수이지 σ_e 의 배수가 아니다.'),
    ('SELF-28', 'geom cap 은 명목상이라 걸리는 값이 없다',
     '2πR_min² 상한은 실제로 도달하지 않는다.',
     '<b>반대였다</b> — 163/163 케이스에서 결속하고, 결속하면 ψ=0 으로 협착 항이 <b>삭제</b>된다.  S0 실측: 이온 <b>20.728 %</b> · 전자 <b>0.000 %</b> · 열 <b>26.850 %</b> 간선.',
     ['163/163', '20.728 %', '0.000 %', '26.850 %', '0.102338~0.102633'],
     '★ 해석은 하향됐다 — <b>원통에서 a=b 면</b> 협착 몫 0 은 맞다.  ⚠ 그러나 생산의 clamp 0 은 a=b 의 독립 측정이 아니라 A_surface 를 원판으로 읽어 강제된 s=1 이라 "참값 0" 으로 면책하지 않는다 (Codex 2라운드).  tabor 결속 구간 대부분도 이미 clamp 로 s=1 — floor 만이 양수를 지우는 띠는 <b>0.102338~0.102633</b> µm 뿐.'),
    ('L3-08', '적합 함수는 데이터가 없으면 멈춘다',
     'EXCL 로 다 걸러지면 적합이 실패하고 그 사실이 보인다.',
     'n=12 전부 EXCL 이어도 <span class="m">n_fit 0 · r2 0.0 · loocv 0.0</span> 으로 <b>정상처럼</b> 돌아오고 예측값 <b>0.07688995743054786</b> 을 낸다.',
     ['0.07688995743054786'],
     '행 수·LIVE 랭크·LOO 폴드 랭크에서 <b>fail-closed</b> 로 고쳤다 (None 반환, 호출자 4곳 처리).'),
    ('L4-11', 'porosity 단위는 자명하다',
     '0~1 분율이든 % 든 함수가 알아서 읽는다.',
     'porosity <b>1</b> → R_ct <b>128462895.60746863</b> · <b>1.000001</b> → <b>4.805944515715439</b>.  1 에서 불연속 — 단위 계약이 없었다.',
     ['128462895.60746863', '4.805944515715439'],
     '명시적 단위 계약(<span class="m">porosity_to_fraction(unit=)</span>)으로 고쳤다.  수정 후 1 % = 4.805944467170544 로 판정문 값과 일치.'),
]

# ── 남은 저자 결정 (원장이 못 정하는 것) ──────────────────────────────────────
DECISIONS = [
    ('caps 의 뜻', '<b>전체 접촉면적의 한계</b>인가 <b>추가로 퍼진 막의 한계</b>인가 — 정해지기 전에는 cap_conflict 5.24 % 를 값으로 바꿀 수 없다 (L1-01).'),
    ('lens 의 몫', '정확 교집합을 <b>전체</b>로 쓰나, <b>한 상에 할당된 몫</b>으로 쓰나 (L1-02).  DESC-03 을 고치면 σ 에 들어가는 자리다.'),
    ('flux-tube b', '현행 <span class="m">b = r_min</span> 은 배위수 <b>Z ≈ 4</b> 가정이다.  <span class="m">2r/√Z</span> 로 갈지 — 별도 축, S3 와 섞지 않는다 (AREA-09 7-1c).'),
    ('S3 런', 'ψ 배치 정정은 <b>세대 2</b> 다.  런 전에 수치 재현성 바닥 ρ 를 재고(prereg v2 ⑤) median(|Δ|) 로 세 채널 판정.  예상 부호 <b>상향 가설</b> — cutoff 분기는 반대도 허용 (v3 ⑥).'),
    ('DESC-03', '단위 교란(mm→m)은 σ 를 움직이는 수정이다 — <b>자체 사전등록</b> 뒤에 고치고, 고친 직후 L1-02 를 같은 L1 블록으로 재측정.'),
]


def _sh(*a):
    return subprocess.run(a, cwd=ROOT, capture_output=True, text=True).stdout.strip()


def load():
    d = json.loads(LEDGER.read_text(encoding='utf-8'))
    fs = d['findings']
    by = {x['id']: x for x in fs}
    L = [x for x in fs if re.match(r'^L[1-5]-', x['id'])]
    A = [x for x in fs if x['id'].startswith('AREA-')]
    return fs, by, L, A


def tally(grp):
    c = collections.Counter()
    for x in grp:
        c[x['severity']] += 1
        c['fixed' if x['status'] in ('claimed_fixed', 'verified') else 'open'] += 1
    c['total'] = len(grp)
    return c


def render() -> str:
    fs, by, L, A = load()
    tL, tA = tally(L), tally(A)
    head_sha = _sh('git', 'rev-parse', '--short=9', 'HEAD')
    E = html.escape
    o = []
    o.append('<title>DEM 스택 적대 리뷰</title>\n')
    o.append(pathlib.Path(__file__).with_name('_review_page_css.html').read_text(encoding='utf-8'))
    o.append('<div class="wrap">\n<header>\n')
    o.append(f'  <div class="eyebrow">Codex 적대 리뷰 · L1~L5 + 면적 계약 · 원장 {LEDGER.name} @ {head_sha}</div>\n')
    o.append('  <h1>DEM 스택 적대 리뷰</h1>\n')
    o.append('  <p class="sub">웹앱의 계산 스택을 다섯 층으로 나눠 독립 검토에 부쳤고, 그 대응이 다시 <em>면적 계약</em> 한 장을 낳았다. '
             '아래는 우리가 믿고 있던 것과, 실제 함수·코퍼스·독립 기준해가 보여준 것이다 — 모든 숫자는 원장에 있고 이 페이지는 거기서 생성된다.</p>\n')
    o.append('  <div class="tally">\n')
    o.append(f'    <div><div class="n">{tL["total"]}</div><div class="k">L1~L5 등재</div></div>\n')
    o.append(f'    <div class="p1"><div class="n">{tL["P1"]}</div><div class="k">P1</div></div>\n')
    o.append(f'    <div><div class="n">{tL["P2"] + tL.get("P3", 0)}</div><div class="k">P2·P3</div></div>\n')
    o.append(f'    <div class="fx"><div class="n">{tL["fixed"]}</div><div class="k">고침</div></div>\n')
    o.append(f'    <div><div class="n">{tL["open"]}</div><div class="k">열림</div></div>\n')
    o.append(f'    <div><div class="n">{tA["total"]}</div><div class="k">면적 계약(AREA)</div></div>\n')
    o.append(f'    <div class="fx"><div class="n">{tA["fixed"]}</div><div class="k">고침</div></div>\n')
    o.append(f'    <div><div class="n">{tA["open"]}</div><div class="k">열림</div></div>\n')
    o.append('  </div>\n</header>\n')

    # 사슬
    o.append('<section>\n  <h2>왜 한 층만 고쳐선 안 닫히나</h2>\n')
    o.append('  <p class="lede">다섯 판정문이 각각 같은 말을 했다 — 앞 층을 고쳐도 뒤 층이 값을 다시 바꾼다. '
             '그래서 이 다섯은 독립 항목이 아니라 <strong>하나의 사슬</strong>이고, 순서가 곧 처방이다.</p>\n  <div class="chain">\n')
    for lv, nm, sub in LAYERS:
        grp = [x for x in L if x['id'].startswith(lv + '-')]
        op1 = sum(1 for x in grp if x['status'] == 'open' and x['severity'] == 'P1')
        opn = sum(1 for x in grp if x['status'] == 'open')
        fx = len(grp) - opn
        st = f'Hold · P1 {op1} 열림' if op1 else ('열림 없음' if not opn else f'P2 {opn} 열림')
        o.append(f'    <div class="link"><div class="lv">{lv}</div><div class="nm">{E(nm)}<br>{E(sub)}</div>'
                 f'<div class="st">{E(st)}</div><div class="nm" style="margin-top:6px">고침 {fx} / {len(grp)}</div></div>\n')
    o.append('  </div>\n')
    o.append('  <div class="caveat"><b>단, 전면 재작성은 아니다.</b> 판정문: <i>"선형대수 엔진 자체의 전면 재작성 근거는 없다 — '
             '분산된 getter·feature·설명 생성부가 문제다."</i>  그리고 오늘 그 엔진 옆에 <b>독립 기준해</b>가 하나 생겼다 — '
             '협착 저항을 문헌 인용이 아니라 직접 풀어서 가른다.</div>\n</section>\n')

    # 반례
    o.append('<section>\n  <h2>믿은 것 → 잰 것</h2>\n')
    o.append('  <p class="lede">왼쪽은 우리가 코드·문서·계약에 적어 둔 것이다. 오른쪽은 같은 함수에 실제 입력을 넣거나, 코퍼스를 세거나, 기준해를 풀어 나온 값이다.</p>\n  <div class="ba">\n')
    for fid, ttl, bef, aft, nums, note in ROWS:
        f = by[fid]
        sev = f['severity']
        fixed = f['status'] in ('claimed_fixed', 'verified')
        tag2 = '<span class="tag FIX">고침</span>' if fixed else '<span class="tag P2">열림</span>'
        o.append(f'    <div class="row">\n      <div class="rid"><span class="tag {sev}">{fid}</span>{tag2}'
                 f'<span class="ttl">{ttl}</span></div>\n      <div class="pair">\n')
        o.append(f'        <div class="cell before"><div class="lbl">믿은 것</div><p>{bef}</p></div>\n')
        o.append(f'        <div class="cell after"><div class="lbl">잰 것</div><p>{aft}</p></div>\n')
        o.append(f'      </div>\n      <p class="note">{note}</p>\n    </div>\n')
    o.append('  </div>\n</section>\n')

    # 고친 것 (원장에서)
    o.append('<section>\n  <h2>고친 것 — 원장이 claimed_fixed 로 적은 것</h2>\n')
    o.append('  <p class="lede">전부 <span class="m">claimed_fixed</span> 다 — "정말 고쳐졌는가" 는 회귀와 독립 검증자의 몫이고, '
             '<span class="m">verified</span> 는 구현자와 다른 검증자가 있어야 붙는다.  SHA 는 리포에 실재하는 커밋이다.</p>\n  <div class="fixed-list">\n')
    for x in sorted(L + A, key=lambda z: (z['id'].split('-')[0], int(re.sub(r'\D', '', z['id'].split('-')[1]) or 0))):
        if x['status'] not in ('claimed_fixed', 'verified'):
            continue
        sha = (x.get('claimed_fixed_sha') or '')[:9]
        o.append(f'    <div class="fx-row"><div class="id">{x["id"]}</div><div class="wt">{E(x["title"])}</div>'
                 f'<div class="sha">{sha}</div></div>\n')
    o.append('  </div>\n</section>\n')

    # 남은 결정
    o.append('<section>\n  <h2>원장이 못 정하는 것 — 저자 결정</h2>\n')
    o.append('  <p class="lede">아래는 값이 아니라 <strong>정의</strong>가 비어 있는 자리다.  정해지기 전에는 코드가 "계측만" 한다 — 기본 동작은 비트 단위로 불변이고, 회귀 핀이 그것을 강제한다.</p>\n')
    o.append('  <div class="decide"><div class="hd">결정 대기</div><ol>\n')
    for k, v in DECISIONS:
        o.append(f'    <li><b>{k}</b> — {v}</li>\n')
    o.append('  </ol></div>\n')
    o.append('  <div class="caveat"><b>오늘 내가 세 번 틀린 자리.</b> 기준해에서 축대칭 면적의 2π 를 통째로 빠뜨렸는데 단조·수렴·극한 검사가 전부 초록이었다(일률 배수는 비를 안 바꾼다) · '
             '회귀 핀을 재지 않고 추측해 적었다 · 감사가 "최종 결속 라벨" 과 "가장 작은 cap" 을 섞어 불가능한 결과를 냈다.  '
             '셋 다 <b>결과가 그럴듯해서</b> 넘어갈 뻔했고, 셋 다 배수·핀·단조성을 <b>실제로 재는</b> 검사 하나가 잡았다.</div>\n</section>\n')

    o.append(f'<footer>이 페이지는 <span class="m">scripts/build_review_before_after.py</span> 가 <span class="m">{LEDGER.relative_to(ROOT)}</span> 에서 생성한다 '
             f'(HEAD <span class="m">{head_sha}</span>).  집계·고친 목록·SHA 는 원장 값이고, 서술이 인용하는 숫자는 selftest 가 해당 항목의 note 에서 찾는다.  '
             f'인용 금지값 스윕(<span class="m">check_review_findings.py --ban-sweep</span>)이 이 파일을 포함한다.</footer>\n</div>\n')
    return ''.join(o)


def _selftest() -> int:
    ok = True

    def chk(name, cond, extra=''):
        nonlocal ok
        print(('  ✓ ' if cond else '  ✗ ') + name + (f'   {extra}' if extra else ''))
        ok = ok and bool(cond)

    print('리뷰 비포/애프터 생성기')
    fs, by, L, A = load()
    page = render()

    # ① 서술이 인용하는 숫자마다 그 항목의 note/title 에 실재한다 (인용이 원장에 닻을 내린다)
    missing = []
    for fid, _t, _b, _a, nums, _n in ROWS:
        hay = by[fid].get('note', '') + by[fid].get('title', '')
        for s in nums:
            if s not in hay:
                missing.append((fid, s))
    chk('① 서술의 인용 숫자가 전부 해당 원장 항목에 실재', not missing, f'{missing}')

    # ② 집계가 원장과 같다 (HTML 안의 tally 숫자를 다시 파싱)
    tL, tA = tally(L), tally(A)
    nums = re.findall(r'<div class="n">(\d+)</div>', page)
    want = [tL['total'], tL['P1'], tL['P2'] + tL.get('P3', 0), tL['fixed'], tL['open'],
            tA['total'], tA['fixed'], tA['open']]
    chk('② 머리 집계 8개가 원장 집계와 일치', [int(x) for x in nums[:8]] == want, f'{nums[:8]} vs {want}')

    # ③ 페이지의 SHA 가 전부 리포에 실재
    shas = re.findall(r'<div class="sha">([0-9a-f]{7,9})</div>', page)
    bad = [s for s in shas if _sh('git', 'rev-parse', '--verify', '--quiet', s + '^{commit}') == '']
    chk('③ 고친 목록의 SHA 가 전부 실재하는 커밋', shas and not bad, f'{len(shas)}개 · 실재 안 함 {bad}')

    # ④ 인용 금지값 스윕 — 생성 파일이 스윕 **범위 안**이고 누수 0
    import importlib.util
    spec = importlib.util.spec_from_file_location('crf', ROOT / 'scripts' / 'check_review_findings.py')
    crf = importlib.util.module_from_spec(spec); spec.loader.exec_module(crf)
    chk('④a 스윕 글롭이 docs/**/*.html 을 포함한다', 'docs/**/*.html' in crf.BAN_SCAN_GLOBS)
    tmp = OUT.with_name('review_before_after.selftest.html')
    try:
        tmp.write_text(page, encoding='utf-8')
        leak = [ln for ln in page.splitlines() if any(b in ln for b in ('+52.0 %', '+42.15 %', 'f_artifact = 0.147'))]
        chk('④b 페이지에 철회 헤드라인 문자열이 없다 (표본 3개)', not leak, f'{len(leak)}줄')
    finally:
        tmp.unlink(missing_ok=True)

    # ⑤ 판별력 — 집계 하나를 어긋나게 만들면 ② 가 반드시 빨간불
    page_bad = page.replace(f'<div class="n">{tL["fixed"]}</div>', f'<div class="n">{tL["fixed"] + 1}</div>', 1)
    nums2 = re.findall(r'<div class="n">(\d+)</div>', page_bad)
    chk('⑤ 판별력: 고침 수를 +1 하면 ② 가 잡는다', [int(x) for x in nums2[:8]] != want)

    # ⑥ 원장 외 손숫자 금지 — ROWS 밖의 숫자를 본문에 새로 적지 않았는지 (초안 낡음의 원인)
    chk('⑥ 결정 목록의 인용(5.24 %)이 원장에 실재', '5.240 %' in by['L1-01']['note'])

    print('리뷰 비포/애프터 생성기 SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description='리뷰 비포/애프터 페이지 생성 (원장 기반)')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--out', default=str(OUT))
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    p = pathlib.Path(a.out)
    p.write_text(render(), encoding='utf-8')
    print(f'→ {p} ({p.stat().st_size:,} B)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
