# resume_ckpt.sh — 멈춘 LIGGGHTS 런을 최신 체크포인트에서 이어받아 N MPI 로 재제출 (복사 → 재개 덱 → 정적 대조 → 짧은 시험 → 대조 → 본 제출)
# 2026-09-27 pse_r050_a · pse_r075_a (15 → 30 MPI) 건에서 확정한 표준 절차.  사용 전 원 런 폴더를 <root>/<case>.<접미사> 로 옮겨 둔다.
#   bash resume_ckpt.sh -n 30 -s stop15_0927 pse_r050_a pse_r075_a
#   -n NP   본 런 MPI 수 (기본 30)          -s SUF  멈춘 폴더 접미사 (필수)      -r ROOT 케이스 루트 (기본 ~/dem_test/lhs)
#   -x SFX  새 파일 접미사 (기본 r<NP>)      -t N    시험 step (기본 2000)
#   -T      시험만 — G0–G3 를 기록하고 본 제출은 하지 않는다 (NP 실측용)
#   -c      작업 사본의 맨 위 input*.liggghts 에서 줄 전체 주석 (첫 공백 아닌 글자 #) 만 빼고 dem_restart.py — 멈춘 폴더 그대로 · 인라인 주석은 안 뺀다
#           비주석 줄 sha256 · LIGGGHTS 명령 (& 이어 붙이기 → 주석 제거) 전후 같아야 (아니면 ⛔ 건너뜀) · 10-27 ibb: 덱 검사가 머리 주석의 다른 케이스 이름 (real_4) 도 거부
#   -C <본 덱> <재개 덱> <체크포인트> <S0> <작업 폴더>   재개 덱 정적 대조만 (손 확인용 · 종료 코드 0 = 통과)
# 2026-10-26 (원장 KG50-02 · KG50-10 · 1저자 Q2 *"50kg 권고대로해"*):
#   본 제출 = G0 ∧ G1 ∧ G2 ∧ G3 · G0 = 시험이 COMPLETED · ExitCode 0:0 · 마지막 thermo step = 기대 끝 (S0 + 시험 run) · 그 뒤 Loop time · ERROR 0.
#   G3 = 원 로그의 비교 구간 (S0, 끝] 정규 줄이 시험에 하나라도 없으면 실패 (결손) — 원 로그에 그 구간 줄이 없을 때만 생략.
#   sacct 조회 실패 · 대기 시간 초과 · 시험 로그 없음 = 제출 안 함.
#   재개 덱 정적 대조 (재삽입 · 물리 줄 · 재개 지점 상태 · 남은 step · 뒤 순서 · c_/f_ 정의) 실패 = 시험도 내지 않는다.
#   큐 검사 = 이름 정확 일치 (C · C_ins · C_<SFX> · C_<SFX>t · C_r<N> · C_r<N>t) · squeue 조회 실패 = 그 케이스 건너뜀.
NP=30; SUF=""; L=~/dem_test/lhs; SFX=""; TS=2000; TONLY=0; CHK=0; STRIP=0
while getopts "n:s:r:x:t:TCc" o; do case $o in n) NP=$OPTARG;; s) SUF=$OPTARG;; r) L=$OPTARG;; x) SFX=$OPTARG;; t) TS=$OPTARG;; T) TONLY=1;; C) CHK=1;; c) STRIP=1;; *) exit 1;; esac; done
shift $((OPTIND-1))
# 재개 덱 정적 대조 — 인자: 본 덱 · 재개 덱 · 체크포인트 경로 · S0 · 작업 폴더.  stdout = 기록 · 종료 코드 0 = 통과
#   (-c 주석 줄 빼기도 이 파이썬이 한다 — 인자 --strip-comments <작업 폴더> 둘뿐일 때 · LIGGGHTS 줄 규칙 deck() 를 같이 쓰려고)
deckcheck(){ python3 - "$@" <<'PY'
import os, re, sys
FWD = {'fix', 'pair_style', 'pair_coeff', 'compute', 'neighbor', 'neigh_modify', 'timestep', 'variable'}
GLOB = {'pair_style', 'neighbor', 'neigh_modify', 'timestep'}
SEQ = {'fix', 'unfix', 'run', 'restart', 'write_restart', 'pair_style', 'pair_coeff',
       'neighbor', 'neigh_modify', 'timestep', 'label', 'jump', 'if'}
TMPL = re.compile(r'^(particletemplate/|particledistribution/)')
INS = re.compile(r'^insert/')
MESH = {'mesh/surface/stress', 'mesh/surface'}


def uncomment(s):
    out, q = [], None
    for ch in s:
        if q:
            out.append(ch)
            if ch == q:
                q = None
        elif ch in '"\'':
            q = ch
            out.append(ch)
        elif ch == '#':
            break
        else:
            out.append(ch)
    return ''.join(out)


def deck(path):
    # '&' 이어 붙이기 = 원 줄의 마지막 글자일 때 (주석을 지우기 전 · LIGGGHTS 입력 규칙) → 그 뒤 주석 · 공백 정리
    res, buf = [], ''
    with open(path, encoding='utf-8', errors='replace') as f:
        for raw in f:
            r = raw.rstrip('\n').rstrip()
            if r.endswith('&'):
                buf += r[:-1] + ' '
                continue
            s = ' '.join(uncomment(buf + r).split())
            buf = ''
            if s:
                res.append(s)
    s = ' '.join(uncomment(buf).split())
    if s:
        res.append(s)
    return res


def num(x):
    # awk 의 $2+0 과 같은 규칙: 앞의 ASCII 숫자 부분만 (없으면 0)
    m = re.match(r'[ \t]*[+-]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][+-]?[0-9]+)?', x)
    return float(m.group(0)) if m else 0.0


def long_runs(L, start=0):
    # 시험 덱 자르기와 같은 규칙 (awk: $1=="run" && $2+0>1)
    return [i for i in range(start, len(L)) if L[i].split()[0] == 'run'
            and len(L[i].split()) > 1 and num(L[i].split()[1]) > 1]


def mesh_file(a, b):
    ta, tb = a.split(), b.split()
    if (len(ta) != len(tb) or len(ta) < 6 or ta[0] != 'fix' or ta[3] not in MESH
            or 'file' not in ta or 'file' not in tb or ta.index('file') != tb.index('file')):
        return None
    i = ta.index('file')
    if i + 1 >= len(ta) or ta[:i + 1] != tb[:i + 1] or ta[i + 2:] != tb[i + 2:]:
        return None
    return tb[i + 1]


def state(L, end):
    fixes, glob = {}, {}
    for l in L[:end]:
        t = l.split()
        if t[0] == 'fix' and len(t) >= 4:
            if TMPL.match(t[3]) or INS.match(t[3]):
                continue
            fixes[t[1]] = l
        elif t[0] == 'unfix' and len(t) >= 2:
            fixes.pop(t[1], None)
        elif t[0] in GLOB:
            glob[t[0]] = l
        elif t[0] == 'pair_coeff':
            glob[' '.join(['pair_coeff'] + t[1:3])] = l
    return fixes, glob


def same_or_mesh(a, b, W, notes, probs, what):
    if a == b:
        return
    nf = mesh_file(a, b) if (a and b) else None
    if nf is not None:
        if os.path.isfile(os.path.join(W, nf)):
            notes.append('판 메시 파일만 다름 (%s): %s' % (what, nf))
        else:
            probs.append('판 메시 파일 %s 가 작업 폴더에 없음 (%s)' % (nf, what))
        return
    if a and b:
        probs.append('%s 다름: 본 덱 [%s] ↔ 재개 덱 [%s]' % (what, a, b))
    elif a:
        probs.append('%s 가 재개 덱에 없음: 본 덱 [%s]' % (what, a))
    else:
        probs.append('%s 는 재개 덱에만 있음: [%s]' % (what, b))


def check(main, res, ckpt, s0, W):
    M, R = deck(main), deck(res)
    probs, notes = [], []
    mset = set(M)
    # A. 재삽입 금지
    for l in R:
        t = l.split()
        if t[0] == 'fix' and len(t) >= 4 and INS.match(t[3]):
            probs.append('재개 덱에 삽입 fix (재삽입): [%s]' % l)
    # B. 재개 덱의 물리 · 변수 줄 = 본 덱 줄 그대로 (판 메시 파일 이름만 예외 · 그 파일이 작업 폴더에 있을 때)
    mfix = {}
    for l in M:
        t = l.split()
        if t[0] == 'fix' and len(t) >= 2:
            mfix.setdefault(t[1], []).append(l)
    for l in R:
        t = l.split()
        if t[0] not in FWD or l in mset:
            continue
        nf = None
        if t[0] == 'fix' and len(t) >= 2:
            for a in mfix.get(t[1], []):
                nf = mesh_file(a, l)
                if nf is not None:
                    break
        if nf is not None and os.path.isfile(os.path.join(W, nf)):
            notes.append('판 메시 파일만 다름: %s' % nf)
        elif nf is not None:
            probs.append('판 메시 파일 %s 가 작업 폴더에 없음' % nf)
        else:
            probs.append('본 덱에 없는 줄: [%s]' % l)
    # F. 재개 덱에서 쓰는 c_ · f_ 이름이 재개 덱에 정의돼 있다 (compute · fix 는 restart 에 안 남는다)
    dc = set(l.split()[1] for l in R if l.split()[0] == 'compute' and len(l.split()) > 1)
    df = set(l.split()[1] for l in R if l.split()[0] == 'fix' and len(l.split()) > 1)
    for l in R:
        for kind, name in re.findall(r'\b([cf])_([A-Za-z0-9_]+)', l):
            if name not in (dc if kind == 'c' else df):
                probs.append('재개 덱이 %s_%s 를 쓰는데 정의가 없음: [%s]' % (kind, name, l))
    # 체크포인트 → 본 덱의 자리 (그 파일을 만드는 restart · write_restart 줄 하나)
    base = os.path.basename(ckpt)
    hits = []
    for i, l in enumerate(M):
        t = l.split()
        if t[0] == 'write_restart' and len(t) >= 2 and os.path.basename(t[1]) == base:
            hits.append(('write', i))
        elif t[0] == 'restart' and len(t) >= 3 and num(t[1]) > 0:
            for p in t[2:4]:
                pat = '^' + re.escape(os.path.basename(p)).replace(r'\*', '[0-9]+') + '$'
                if re.match(pat, base):
                    hits.append(('restart', i))
                    break
    if len(hits) != 1:
        probs.append('체크포인트 %s 를 만든 restart · write_restart 줄이 본 덱에 %d 개 (1 개여야 · 손으로 확인)'
                     % (base, len(hits)))
        return probs, notes
    kind, ia = hits[0]
    mr, rr = long_runs(M, ia + 1), long_runs(R)
    if not mr or not rr:
        probs.append('긴 run 을 못 찾음 (본 덱 %d · 재개 덱 %d)' % (len(mr), len(rr)))
        return probs, notes
    im, ir = mr[0], rr[0]
    # C. 재개 지점의 상태 (살아 있는 fix · 쌍 · 이웃 · timestep) — 템플릿 · 분포 · 삽입 fix 는 뺀다
    fm, gm = state(M, im)
    fr, gr = state(R, ir)
    for k in sorted(set(fm) | set(fr)):
        same_or_mesh(fm.get(k), fr.get(k), W, notes, probs, '재개 지점 fix ' + k)
    for k in sorted(set(gm) | set(gr)):
        same_or_mesh(gm.get(k), gr.get(k), W, notes, probs, '재개 지점 ' + k)
    # D. 남은 step — restart 명령이 만든 체크포인트 · 그 run 앞에 반복 · 변수 run 이 없을 때
    if kind == 'restart':
        step, known = 0, True
        for l in M[:im + 1]:
            t = l.split()
            if t[0] in ('label', 'jump'):
                known = False
            elif t[0] == 'reset_timestep' and len(t) > 1:
                step = int(num(t[1]))
            elif t[0] == 'run' and len(t) > 1:
                if not re.match(r'^[0-9]+$', t[1]):
                    known = False
                elif 'upto' in t[2:]:
                    step = int(t[1])
                else:
                    step += int(t[1])
        if known:
            t = R[ir].split()
            if not re.match(r'^[0-9]+$', t[1]):
                probs.append('재개 덱 첫 긴 run 이 숫자가 아님: [%s]' % R[ir])
            else:
                end = int(t[1]) if 'upto' in t[2:] else s0 + int(t[1])
                if end != step:
                    probs.append('남은 step 다름: 재개 끝 %d ↔ 본 덱 그 run 끝 %d ([%s])' % (end, step, R[ir]))
                else:
                    notes.append('남은 step 같음: 끝 %d' % end)
        else:
            notes.append('남은 step 확인 생략 (그 run 앞에 반복 · 변수 run)')
    else:
        notes.append('남은 step 확인 해당 없음 (write_restart 체크포인트)')
    # E. 재개 지점 뒤 순서 (fix · unfix · run · restart · if …) = 본 덱 그대로
    tm = [l for l in M[im + 1:] if l.split()[0] in SEQ]
    tr = [l for l in R[ir + 1:] if l.split()[0] in SEQ]
    if len(tm) != len(tr):
        probs.append('재개 지점 뒤 순서 줄 수 다름: 본 덱 %d ↔ 재개 덱 %d' % (len(tm), len(tr)))
    for a, b in zip(tm, tr):
        if a != b:
            same_or_mesh(a, b, W, notes, probs, '재개 지점 뒤 줄')
    return probs, notes


def strip_comments(W):
    # -c (10-27 ibb · dem_restart.py 덱 검사가 머리 주석의 다른 케이스 이름도 거부): 작업 폴더 W 의 맨 위 input*.liggghts 에서
    # 줄 전체 주석 (첫 공백 아닌 글자 '#') 만 뺀다 — 인라인 주석 · 빈 줄 · 나머지 바이트 (줄 끝 포함) 그대로.
    # 덱마다 검사: 비주석 줄 sha256 = 원 파일 ↔ 다시 읽은 새 파일 · 새 파일에 줄 전체 주석 0 · LIGGGHTS 명령 (deck()) 같음
    # ('&' 로 이어진 명령 안의 주석 줄 · '&' 로 끝나는 주석 줄은 빼면 명령이 바뀐다).  하나라도 실패 = 어느 덱도 안 바꾼다.
    # 쓰기 = 임시 파일 → 검사 → 전부 통과 뒤 os.replace (새 inode — 멈춘 폴더 · 링크 대상 파일은 안 건드린다).
    import fnmatch, hashlib, shutil

    def lines(b):
        parts = b.split(b'\n')
        return [x + b'\n' for x in parts[:-1]] + ([parts[-1]] if parts[-1] else [])

    def body(b):
        return [x for x in lines(b) if not x.lstrip().startswith(b'#')]

    names, recs, probs, tmps, done, total = [], [], [], [], [], 0
    try:
        names = sorted(n for n in os.listdir(W)
                       if fnmatch.fnmatchcase(n, 'input*.liggghts') and os.path.isfile(os.path.join(W, n)))
        if not names:
            probs.append('작업 폴더에 input*.liggghts 없음')
        for name in names:
            p = os.path.join(W, name)
            with open(p, 'rb') as f:
                old = f.read()
            keep = body(old)
            n = len(lines(old)) - len(keep)
            h0 = hashlib.sha256(b''.join(keep)).hexdigest()
            if n == 0:
                recs.append('%s: 줄 전체 주석 0 줄 뺌 (파일 그대로) · 남은 줄 %d · 비주석 줄 sha256 전 %s = 후 %s'
                            % (name, len(keep), h0, h0))
                continue
            t = p + '.cstrip'
            tmps.append((t, p))
            with open(t, 'wb') as f:
                f.write(b''.join(keep))
            with open(t, 'rb') as f:
                new = f.read()
            h1 = hashlib.sha256(b''.join(body(new))).hexdigest()
            left = len(lines(new)) - len(body(new))
            dm, dn = deck(p), deck(t)
            if h1 != h0:
                probs.append('%s: 비주석 줄 sha256 다름 — 전 %s · 후 %s' % (name, h0, h1))
            if left:
                probs.append('%s: 새 파일에 줄 전체 주석 %d 줄 남음' % (name, left))
            if dm != dn:
                i = next(j for j in range(max(len(dm), len(dn)))
                         if j >= len(dm) or j >= len(dn) or dm[j] != dn[j])
                probs.append('%s: 주석 줄을 빼면 LIGGGHTS 명령이 바뀐다 (예: & 이어 붙이기 안의 주석 줄 · & 로 끝나는 주석 줄) — '
                             '%d 번째 명령 전 [%s] ↔ 후 [%s] · 손으로 봐야 함'
                             % (name, i + 1, dm[i][:120] if i < len(dm) else '없음', dn[i][:120] if i < len(dn) else '없음'))
            total += n
            recs.append('%s: 줄 전체 주석 %d 줄 뺌 · 남은 줄 %d · 비주석 줄 sha256 전 %s = 후 %s · LIGGGHTS 명령 %d 개 같음'
                        % (name, n, len(keep), h0, h1, len(dn)))
        if not probs:
            for t, p in tmps:
                shutil.copystat(p, t)
                os.replace(t, p)
                done.append(os.path.basename(p))
    except Exception as e:
        probs.append('도구 오류: %s: %s' % (type(e).__name__, e))
    finally:
        for t, _ in tmps:
            if os.path.exists(t):
                os.remove(t)
    if probs:
        for q in probs:
            print('  ✗ ' + q)
        print('  주석 줄 빼기 (-c): 실패 — %s' % ('이미 바꾼 덱 %s (작업 폴더만)' % ' '.join(done) if done else '어느 덱도 안 바꿈'))
        return 1
    for r in recs:
        print('  · ' + r)
    print('  주석 줄 빼기 (-c): 통과 (덱 %d · 뺀 줄 %d)' % (len(names), total))
    return 0


if len(sys.argv) == 3 and sys.argv[1] == '--strip-comments':
    sys.exit(strip_comments(sys.argv[2]))
try:
    main, res, ckpt, s0, W = sys.argv[1:6]
    probs, notes = check(main, res, ckpt, int(s0), W)
except Exception as e:
    probs, notes = ['대조 도구 오류: %s: %s' % (type(e).__name__, e)], []
for n in notes:
    print('  · ' + n)
for p in probs:
    print('  ✗ ' + p)
print('  재개 덱 정적 대조: %s (문제 %d)' % ('통과' if not probs else '실패', len(probs)))
sys.exit(1 if probs else 0)
PY
}
# -c 주석 줄 빼기 — 인자: 작업 폴더 · stdout = 기록 · 종료 코드 0 = 통과 (실패면 어느 덱도 안 바꾼다)
stripc(){ deckcheck --strip-comments "$1"; }
if [ $CHK = 1 ]; then [ $# = 5 ] || { echo "사용: bash resume_ckpt.sh -C <본 덱> <재개 덱> <체크포인트> <S0> <작업 폴더>"; exit 2; }; deckcheck "$@"; exit $?; fi
CASES="$*"; SFX=${SFX:-r$NP}
[ -n "$SUF" ] && [ -n "$CASES" ] || { echo "사용: bash resume_ckpt.sh -n 30 -s stop15_0927 <케이스…>"; exit 1; }
cd $L || exit 1; mkdir -p logs; STAMP=$(date +%m%d_%H%M); REP=$L/resume_${SFX}_$STAMP.md
tl(){ awk -v s="$1" '/^ *Step +Atoms/{n=split($0,h);next} n>0 && NF==n && $1~/^[0-9]+$/ && $1==s {o=""; for(i=1;i<=NF;i++){if(h[i]=="CPU"||h[i]=="pressMPa")continue; o=o" "h[i]"="$i}; r=o} END{print r}' "$2"; }
reg(){ awk '/^ *Step +Atoms/{n=split($0,h);c=0;for(i=1;i<=n;i++)if(h[i]=="CPU")c=i;next} n>0&&NF==n&&c>0&&$1~/^[0-9]+$/&&$c+0>0{print $1}' "$1"; }
tr2(){ awk -v s="$1" '/^ *Step +Atoms/{n=split($0,h);c=0;for(i=1;i<=n;i++)if(h[i]=="CPU")c=i;next} n>0&&NF==n&&c>0&&$1~/^[0-9]+$/&&$1==s&&$c+0>0{o="";for(i=1;i<=NF;i++){if(i==c)continue;o=o" "h[i]"="$i};r=o} END{print r}' "$2"; }
same(){ awk -v a="$1" -v b="$2" -v t="$3" 'BEGIN{na=split(a,x," ");nb=split(b,y," ");if(na<3||na-nb)exit 1;for(i=1;i<=na;i++){split(x[i],p,"=");split(y[i],q,"=");if(p[1]<q[1]||p[1]>q[1])exit 1;if(match(p[2],/^[-+]?[0-9.]+([eE][-+]?[0-9]+)?$/)==0||match(q[2],/^[-+]?[0-9.]+([eE][-+]?[0-9]+)?$/)==0)exit 1;if(p[1]=="Step"||p[1]=="Atoms"){if(p[2]+0<q[2]+0||p[2]+0>q[2]+0)exit 1;continue};d=p[2]-q[2];if(d<0)d=-d;m=p[2];if(m<0)m=-m;if(d>t*m&&d>1e-12)exit 1};exit 0}'; }
# 느슨한 역학 확인: 원자 수 같고, 압력 (있으면) 아니면 KE 가 5 % 안
sane(){ awk -v a="$1" -v b="$2" 'BEGIN{na=split(a,x," ");nb=split(b,y," ");if(na<3||na-nb)exit 1;k="";for(i=1;i<=na;i++){split(x[i],p,"=");split(y[i],q,"=");A[p[1]]=p[2];B[q[1]]=q[2]};if(A["Atoms"]+0<B["Atoms"]+0||A["Atoms"]+0>B["Atoms"]+0)exit 1;k=("pressMPa" in A && A["pressMPa"]+0>1e-6)?"pressMPa":"KinEng";if((k in A)==0)exit 1;d=A[k]-B[k];if(d<0)d=-d;m=A[k];if(m<0)m=-m;exit (d>0.05*m && d>1e-12)}'; }
sel(){ awk 'NR==9{n=0;split("id type x y z radius vx vy vz",w," ");for(k=1;k<=9;k++)for(i=3;i<=NF;i++)if($i==w[k]){n++;c[n]=i-2};next} NR>9{o=$c[1];for(k=2;k<=n;k++)o=o" "$c[k];print o}' "$1" | sort -n | md5sum | cut -c1-12; }
# 시험 로그의 마지막 thermo 줄 step · 그 줄 번호 · 마지막 'Loop time of' 줄 번호
lastrun(){ awk '/^ *Step +Atoms/{q=1;next} /^Loop time of/{q=0;lp=NR;next} q&&$1~/^[0-9]+$/{s=$1;ln=NR} END{print s+0, ln+0, lp+0}' "$1"; }
rx(){ printf '%s' "$1" | sed 's/[][\.*^$(){}+?|/]/\\&/g'; }
echo "# LIGGGHTS 체크포인트 재개 기록 — $SFX ($NP MPI) · $(date '+%F %H:%M')" > $REP
echo "명령: bash resume_ckpt.sh -n $NP -s $SUF -r $L -x $SFX -t $TS$([ $TONLY = 1 ] && echo ' -T')$([ $STRIP = 1 ] && echo ' -c') $CASES" >> $REP
for C in $CASES; do
  S=$L/$C.$SUF; W=$L/$C; X=$L/$C.prev_$STAMP; D=$W/input_${C}_$SFX.liggghts; RN=$W/run_${C}_$SFX.sh
  echo; echo "████ $C"
  [ -d $S ] || { echo "  ⛔ $S 없음 (원 런 폴더를 먼저 이 이름으로 옮겨 둘 것)"; continue; }
  PH=$(grep -a '^======' $S/log.liggghts | tail -1)
  LS=$(awk '/^ *Step +Atoms/{q=1;next} q&&$1~/^[0-9]+$/{s=$1} END{print s+0}' $S/log.liggghts)
  echo "  멈춘 곳: $PH | 로그 마지막 step $LS"
  echo "  restart_$C/ 최신: $(ls $S/restart_$C/ 2>/dev/null | sort -t_ -k3 -n | tail -3 | tr '\n' ' ')"
  ls $S/restart_forced_liggghts_* 2>/dev/null | sed 's#.*/#  (강제 restart, 안 씀: #; s/$/)/'
  QL=$(squeue -u $USER -h -o %j 2>/dev/null) || { echo "  ⛔ squeue 조회 실패 — 건너뜀 (돌고 있는지 모른다)"; continue; }
  if printf '%s\n' "$QL" | grep -qxE "$(rx $C)(_ins|_$(rx $SFX)t?|_r[0-9]+t?)?"; then echo "  ⛔ $C 의 잡 (${C} · ${C}_ins · ${C}_$SFX[t] · ${C}_r<N>[t]) 이 큐에 있음 — 건너뜀"; continue; fi
  if [ -e $W ]; then
    [ -e $X ] && { echo "  ⛔ $X 이미 있음 — 건너뜀"; continue; }
    mv $W $X && echo "  같은 이름의 기존 폴더 → ${X##*/} (보존)"
  fi
  echo "  복사 중 ($(du -sh $S | cut -f1)) …"; cp -a $S $W || { echo "  ⛔ 복사 실패"; continue; }
  mv $W/log.liggghts $W/log.liggghts.$SUF
  if [ $STRIP = 1 ]; then
    stripc $W > $W/strip_$SFX.txt 2>&1; SOK=$?; cat $W/strip_$SFX.txt
    [ $SOK = 0 ] || { echo "  ⛔ 주석 줄 빼기 (-c) 실패 — 재개 덱 만들지 않고 건너뜀 (기록 strip_$SFX.txt)"; continue; }
  fi
  python3 ~/dem_test/dem_restart.py --case-list $C --root $L --suffix $SFX --skip-sacct --no-relax-detect > $W/plan_$SFX.txt 2>&1
  P=$(grep -E "^ +$C +(compress|after_settling|settling) " $W/plan_$SFX.txt | sed 's/^ *//')
  [ -n "$P" ] || { echo "  ⛔ 재개 덱 못 만듦 (체크포인트 없음 → 처음부터밖에 없음 · 보고 후 승인):"; grep -A3 '제외' $W/plan_$SFX.txt; continue; }
  M=$(echo $P | awk '{print $2}'); RR=$(awk '$1=="read_restart"{print $2}' $D)
  S0=$(echo $RR | sed -nE 's/.*_([0-9]+)\.bin$/\1/p')
  [ -z "$S0" ] && S0=$(awk '/^ *Step +Atoms +c?_?zmax/{getline; print $1; exit}' $W/log.liggghts.$SUF)
  if [ "$M" = compress ]; then TP="없음 (메시 type 1 이 첫 run 전에 생김)"; else
    awk '$1=="fix" && ($2~/^pts[0-9]+$/ || $2=="pdd_mix")' $W/input_$C.liggghts > $W/tmpl_$SFX.txt
    grep -q '&$' $W/tmpl_$SFX.txt && { echo "  ⛔ 템플릿 줄이 여러 줄 — 손으로 봐야 함"; continue; }
    awk -v f=$W/tmpl_$SFX.txt '{print} $1=="read_restart"{while((getline l < f)>0) print l}' $D > $D.tmp && mv $D.tmp $D
    TP="$(awk '{print $2}' $W/tmpl_$SFX.txt | tr '\n' ' ')(원 덱 그대로 · 삽입 fix 는 없음)"; fi
  O=$W/old_post_after${S0}_$SUF; mkdir -p $O
  (cd $W/post_$C && ls | awk -v k=$S0 '{n=$0; sub(/.*_/,"",n); sub(/\..*/,"",n); if(n~/^[0-9]+$/ && n+0>k) print}' | xargs -r mv -t $O)
  echo "  계획: $P"
  echo "  read_restart $RR (step $S0) · 뒤 덤프 $(ls $O | wc -l)개 → ${O##*/} · 템플릿 재선언: $TP"
  echo "$TP" > $W/tp_$SFX.txt
  sed -i "s/^#SBATCH -n .*/#SBATCH -n $NP/; s/mpirun \(--oversubscribe \)\{0,1\}\(--bind-to none \)\{0,1\}-np [0-9]*/mpirun --oversubscribe --bind-to none -np $NP/" $RN
  awk -v t=$TS '{if($1=="run" && $2+0>1){n=$2+0; if(n>t)n=t; print "run " n; exit} print}' $D > $W/input_${C}_${SFX}t.liggghts
  sed -e "s/${C}_$SFX/${C}_${SFX}t/g" -e "s/^#SBATCH --time=.*/#SBATCH --time=01:00:00/" $RN > $W/run_${C}_${SFX}t.sh
  EX=$(comm -13 <(awk '$1=="fix"||$1=="dump"{print $1,$2}' $W/input_$C.liggghts | sort -u) <(awk '$1=="fix"||$1=="dump"{print $1,$2}' $D | sort -u) | tr '\n' ' ')
  OK=1
  [ -s $W/$RR ] || { OK=0; echo "  ✗ $RR 없음"; }
  [ -z "$EX" ] || { OK=0; echo "  ✗ 원 덱에 없는 fix/dump ID: $EX"; }
  { grep -qE "^#SBATCH -n $NP\$" $RN && grep -q -- "--oversubscribe --bind-to none -np $NP lmp_mpi" $RN && grep -q -- "-np $NP lmp_mpi -in input_${C}_${SFX}t.liggghts" $W/run_${C}_${SFX}t.sh; } || { OK=0; echo "  ✗ 러너 $NP"; }
  NT=$(tail -1 $W/input_${C}_${SFX}t.liggghts | awk '$1=="run" && NF==2 && $2~/^[0-9]+$/{print $2}')
  { [ -n "$NT" ] && [[ "$S0" =~ ^[0-9]+$ ]]; } || { OK=0; echo "  ✗ 시험 덱 끝이 숫자 run 이 아님 또는 S0 모름 (기대 끝 step 을 못 정함)"; }
  deckcheck $W/input_$C.liggghts $D "$RR" "${S0:-0}" $W > $W/deckcheck_$SFX.txt 2>&1 || { OK=0; echo "  ✗ 재개 덱 정적 대조 실패:"; }
  cat $W/deckcheck_$SFX.txt
  echo "  $(grep '^processors' $D) | $(grep -c . $W/input_${C}_${SFX}t.liggghts)줄 시험 덱 (마지막: $(tail -1 $W/input_${C}_${SFX}t.liggghts))"
  if [ $OK = 1 ]; then
    J=$(sbatch --parsable $W/run_${C}_${SFX}t.sh)
    if [ -n "$J" ]; then echo $J > $W/job_${SFX}t.txt; EXP=$((10#$S0 + 10#$NT)); echo "$M $S0 $RR $EXP" > $W/mode_$SFX.txt; echo "  ▶ 시험 job $J ($(tail -1 $W/input_${C}_${SFX}t.liggghts) · 기대 끝 step $EXP)"
    else echo "  ⛔ 시험 제출 실패 (sbatch 출력 없음)"; fi
  else echo "  ⛔ 시험 제출 안 함"; fi
done
echo; echo "── 시험 잡 끝날 때까지 대기 (끝나면 대조 → 맞으면 본 제출)"
for C in $CASES; do
  W=$L/$C; S=$L/$C.$SUF; [ -f $W/job_${SFX}t.txt ] || continue; J=$(cat $W/job_${SFX}t.txt)
  # 끝 상태 (sacct State · ExitCode) — 조회 실패는 다시 묻고, 끝까지 못 얻으면 TO=1 (제출 안 함)
  ST=""; EC=""; TO=1; QF=0
  for i in $(seq 360); do
    if Q=$(sacct -n -X -P -j $J -o State,ExitCode 2>/dev/null) && [ -n "$Q" ]; then
      Q=$(printf '%s\n' "$Q" | head -1); ST=${Q%%|*}; EC=${Q#*|}; ST=${ST%% *}
      case "$ST" in COMPLETED|FAILED|CANCELLED|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|PREEMPTED|BOOT_FAIL|DEADLINE) [ -z "$(squeue -h -j $J 2>/dev/null)" ] && { TO=0; break; };; esac
    else QF=$((QF+1)); fi
    sleep 20
  done
  read M S0 RR EXP < $W/mode_$SFX.txt
  T=$(ls logs/output_${C}_${SFX}t_$J.out 2>/dev/null); T=${T:-/dev/null}; E=$(grep -ac ERROR $T)
  read LTS LTL LPL <<< "$(lastrun $T)"
  G0=0; [ $TO = 0 ] && [ "$ST" = COMPLETED ] && [ "$EC" = "0:0" ] && [ "$LTS" = "$EXP" ] && [ "$LPL" -gt "$LTL" ] && [ "$E" = 0 ] && [ "$T" != /dev/null ] && G0=1
  F=$(awk '/^ *Step +Atoms/{q=1;next} q&&$1~/^[0-9]+$/{print $1; exit}' $T)
  a=$(tl "$F" $W/log.liggghts.$SUF); b=$(tl "$F" $T)
  G1=0; [ -n "$F" ] && [ "$F" = "$S0" ] && [ "$E" = 0 ] && same "$a" "$b" 1e-6 && G1=1
  # G2: 체크포인트 step 의 상태를 덤프로 직접 대조 (시험이 다시 쓴 파일만 인정)
  G2=1; G2T=""
  if [ "$M" = after_settling ]; then
    x=$(grep -a '^====== PLATE HEIGHT' $W/log.liggghts.$SUF | tail -1); y=$(grep -a '^====== PLATE HEIGHT' $T | tail -1)
    [ -n "$x" ] && [ "$x" = "$y" ] && G2T="판 높이 같음 ($x)" || { G2=0; G2T="판 높이 다름/없음: 원 [$x] · 재개 [$y]"; }
  else
    nc=0
    for f in atom_$S0.liggghts mesh_$S0.stl; do
      o=$S/post_$C/$f; n=$W/post_$C/$f; [ -s $o ] || continue
      if [ -s $n ] && [ $n -nt $W/input_${C}_${SFX}t.liggghts ]; then
        case $f in atom*) u=$(sel $o); v=$(sel $n);; *) u=$(md5sum < $o | cut -c1-12); v=$(md5sum < $n | cut -c1-12);; esac
        nc=$((nc+1)); [ "$u" = "$v" ] && G2T="$G2T $f 같음 ·" || { G2=0; G2T="$G2T $f 다름 ·"; }
      else G2=0; G2T="$G2T $f 시험이 다시 안 씀 ·"; fi
    done
    [ $nc = 0 ] && [ "$M" = compress ] && { G2=0; G2T="$G2T 체크포인트 step 덤프 없음 — 손으로 확인"; }
    [ $nc = 0 ] && [ "$M" = settling ] && G2T="$G2T 체크포인트 step 덤프 없음 (G1 의 KE 일치로 대신)"
  fi
  # G3: 원 로그의 비교 구간 (S0, 기대 끝] 정규 thermo 줄 — 시험에 하나라도 없으면 실패 (결손) · 첫 줄은 원자 수 + 압력 (없으면 KE) 5 % 안
  OW=$(reg $W/log.liggghts.$SUF | sort -un | awk -v s="$S0" -v e="$EXP" '$1+0>s+0 && $1+0<=e+0')
  F2=$(printf '%s\n' $OW | head -1); MISS=""
  [ -n "$OW" ] && MISS=$(comm -23 <(printf '%s\n' $OW | sort -u) <(reg $T | sort -u) | sort -n | tr '\n' ' ')
  a2=$(tr2 "$F2" $W/log.liggghts.$SUF); b2=$(tr2 "$F2" $T)
  if [ -z "$F2" ]; then G3=1; G3T="원 로그에 비교 구간 ($S0, $EXP] 정규 줄 없음 → 생략"
  elif [ -n "$MISS" ]; then G3=0; G3T="원 로그에 있는 비교 줄이 시험에 없음 (결손): $MISS"
  elif sane "$a2" "$b2"; then G3=1; G3T="5 % 안"; else G3=0; G3T="5 % 넘음"; fi
  [ -f $W/log.liggghts ] && mv $W/log.liggghts $W/log.liggghts.${SFX}t
  { echo; echo "## $C"
    echo "- 멈춘 폴더: ${C}.$SUF (손대지 않음) · 멈춘 곳 $(grep -a '^======' $S/log.liggghts | tail -1)"
    echo "- 작업 폴더: $W (= 멈춘 폴더 cp -a) · 원 로그 → log.liggghts.$SUF · 체크포인트 뒤 덤프 → old_post_after${S0}_$SUF/"
    [ $STRIP = 1 ] && { echo "- 주석 줄 빼기 (-c · 작업 폴더 덱만): $(tail -1 $W/strip_$SFX.txt | sed 's/^ *주석 줄 빼기 (-c): //') (strip_$SFX.txt)"; sed -n 's/^  · /    /p' $W/strip_$SFX.txt; }
    echo "- 재개: $M 체크포인트 \`read_restart $RR\` (step $S0) · 덱 input_${C}_$SFX.liggghts · 러너 run_${C}_$SFX.sh (#SBATCH -n $NP · mpirun --oversubscribe --bind-to none -np $NP)"
    echo "- 템플릿 재선언: $(cat $W/tp_$SFX.txt)"
    echo "- 재개 덱 정적 대조: $(tail -1 $W/deckcheck_$SFX.txt | sed 's/^ *재개 덱 정적 대조: //') (deckcheck_$SFX.txt)"
    echo "- 시험: job $J · input_${C}_${SFX}t.liggghts · ${T##*/} · ERROR $E"
    echo "- G0 시험 정상 종료: $([ $G0 = 1 ] && echo 통과 || echo 실패) — 상태 ${ST:-없음} · ExitCode ${EC:-없음} · 마지막 step $LTS (기대 $EXP) · Loop time $([ "$LPL" -gt "$LTL" ] && echo '끝 step 뒤에 있음' || echo 없음) · 조회 실패 $QF 번 · $([ $TO = 1 ] && echo '끝 상태 못 얻음 (대기 시간 초과 · 조회 실패)' || echo '끝 상태 얻음')"
    echo "- G1 재개 첫 thermo (step $F, setup 줄, CPU·압력 열 제외, 1e-6): $([ $G1 = 1 ] && echo 통과 || echo 실패)"; echo "    원 로그 :$a"; echo "    재개    :$b"
    echo "- G2 체크포인트 상태 덤프 대조: $([ $G2 = 1 ] && echo 통과 || echo 실패) —$G2T"
    echo "- G3 원 로그 비교 구간 (step ${F2:--} 부터, 느슨한 확인): $G3T"; echo "    원 로그 :$a2"; echo "    재개    :$b2"
  } >> $REP
  if [ $G0 = 1 ] && [ $G1 = 1 ] && [ $G2 = 1 ] && [ $G3 = 1 ]; then
    if [ $TONLY = 1 ]; then echo "- 🧪 시험만 (-T) — G0–G3 통과 · 본 제출 안 함" >> $REP
    else JM=$(sbatch --parsable $W/run_${C}_$SFX.sh)
      if [ -n "$JM" ]; then echo "- ✅ 본 제출 job $JM (run_${C}_$SFX.sh, 제출 폴더 $L)" >> $REP; else echo "- ⛔ 본 제출 실패 (sbatch 출력 없음)" >> $REP; fi
    fi
  else echo "- ⛔ 본 제출 안 함 — 위 G0/G1/G2/G3 확인 후 사람이 판단" >> $REP; fi
done
cat $REP; echo; squeue -u $USER -o "%.10i %.20j %.8T %.4C %.10M %R"
