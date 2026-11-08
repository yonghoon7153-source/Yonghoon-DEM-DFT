"""PC12-01 – 05 고침을 scripts/rint_r_chain.py 에 정확한 글 바꿈 (각각 꼭 한 번) 으로 적용한다 — 원자적 쓰기."""
import os
import pathlib
import sys

p = pathlib.Path(sys.argv[1])
src = p.read_text(encoding='utf-8')
edits = []


def rep(old, new, label):
    edits.append((old, new, label))


# ── F1 (a) stop_trace — check_trace 뒤 ──────────────────────────────────────────────────────────────────────────────────────────────
rep('''            return True
    return False


def words_cause(txt, default):
''', '''            return True
    return False


def stop_trace(folder, run, od):
    """★ 11-08 PC12-01 (사전 공격 12 회차 F1 · 1저자 11-06 규칙) — 멈춘 런의 검사 실패 흔적 (`check_trace`) = 기록의 출력 폴더 od + 디스크에 있는 그 런의 출력 폴더 꼴
    (<런> · <런>_arm… = `Runner._prepare` · `run_traces` 의 런 폴더 규칙) **전부** 의 .unchecked/ → True 면 재실행 자격 없음.  옛 = od 하나 → 요청 칸 (범위 안 arms 2) 과
    outdir 를 함께 고친 옆 이름 <런>_arm2 가 진짜 폴더 <런>_arm1/.unchecked/ 의 흔적을 비켰다 (요청 칸 없는 기록의 옆 이름 <런>_arm9 도 같다).  od 없음 (런 기록 없음 ·
    outdir 칸 없음) = 시도 폴더 전부 (옛 그대로) · 폴더 목록을 못 읽음 = True (보수 · `run_traces` 와 같음)."""
    if od is None:
        return check_trace(folder)
    if check_trace(folder, od):
        return True
    if not isinstance(run, str):
        return False
    try:
        names = os.listdir(str(folder))
    except OSError:
        return True
    return any(check_trace(folder, Path(folder) / nm) for nm in names if nm == run or nm.startswith(run + '_arm'))


def words_cause(txt, default):
''', 'F1a stop_trace')

# ── F3 stop_record_problem 끝 — prior_runs_problem ─────────────────────────────────────────────────────────────────────────────────
rep('''    why = stopped_record_problem(s, folder, code, run, rr)    # ★ 11-06 PC10 확장 P2-B — 기록 안 대조 (runs 마지막 · outdir · arms_read · GU 끝 기록)
    if why:
        return why
    return None


def stopped_record_problem(s, folder, code, run, rr):
''', '''    why = stopped_record_problem(s, folder, code, run, rr)    # ★ 11-06 PC10 확장 P2-B — 기록 안 대조 (runs 마지막 · outdir · 요청 칸 · arms_read · 사슬 쪽 끝 기록)
    if why:
        return why
    return prior_runs_problem(s, code, run, rr)              # ★ 11-08 PC12-03 — 멈춘 런 앞의 런 기록 전부 = 끝난 런 (런 기록 없는 TIME_LIMIT 도 runs 를 본다)


def stopped_record_problem(s, folder, code, run, rr):
''', 'F3 call')

# ── stopped_record_problem 설명 ④ · 한정 줄 ────────────────────────────────────────────────────────────────────────────────────────
rep('''      ④ GROUP_UNCONFIRMED = 그 런 끝 기록의 사슬 쪽 확인 False (`chain_confirmed` · 읽힐 때만 — 시작 기록 없음 · 결합 안 됨 · chain_end 없는 옛 recover 끝 기록 =
         이 대조 안 함 · 옛 = 끝 기록 확인 True 인 런에 멈춤 이름만 GROUP_UNCONFIRMED · GU 기록 rc 1 → 0 = 재실행 자격).
    런 기록 없음 (런 전 TIME_LIMIT · 'none') = None (이 대조 밖).  ⚠ 한정 (고치지 않음): 런 기록 ↔ 그룹 끝 기록 (원인 · rc) 교차 대조 · 같은 이름 런 기록 둘 ·
    다른 칸 (copied_from · seconds · machine …) · 런 전 TIME_LIMIT 이름 차례."""
''', '''      ④ 그 런 끝 기록의 사슬 쪽 (원인 · rc · 확인 = `chain_side` · 읽힐 때만 — 시작 기록 없음 · 결합 안 됨 · chain_end 없는 옛 recover 끝 기록 = 이 대조 안 함) ↔ 멈춤 코드 ·
         런 기록 꼴 = 생산자 대응표 (`chain_side_problem` · `CHAIN_SIDE_SHAPES` · `STOP_CONFIRMED` · ★ 11-08 PC12-02 — 옛 = GROUP_UNCONFIRMED 의 확인 칸만 → 정직 GU 의 런 기록
         rc 1 → 0 한 칸 = 재실행 자격).
      ②′ ★ 11-08 PC12-01 — 요청 칸 (arms · arm_list) 자체가 생산자 범위 (`request_fields_problem`) 가 아니면 사유 (옛 = 꼴만 → arms 9 + outdir <런>_arm9 함께 고침 = 통과).
    런 기록 없음 (런 전 TIME_LIMIT · 'none') = None (이 대조 밖 · 앞 런 기록은 `prior_runs_problem`).  ⚠ 한정 (고치지 않음): 같은 이름 런 기록 둘 · 다른 칸 (copied_from ·
    seconds · machine …) · 런 전 TIME_LIMIT 이름 차례 · 디스크에 그 런의 다른 출력 폴더 (옆 이름) 가 있다는 것 자체 (흔적이 없으면 받음)."""
''', 'docstring ④')

# ── F1 (b) 요청 칸 범위 — record_outdir 앞 ─────────────────────────────────────────────────────────────────────────────────────────
rep('''    want = record_outdir(rr)                                 # 요청 칸이 정하는 정확한 이름 (접두만 맞춘 옆 이름 <런>_arm9 = 검사 실패 흔적 비킴)
    if want is not None and od != want:
''', '''    rq = request_fields_problem(rr)                          # ★ 11-08 PC12-01 — 요청 칸 = 생산자 범위 (arms 1–8 · arm_list 정렬 · 중복 없음 · 0–7 · 접두 아님 · 길이 = arms)
    if rq:
        return f'멈춤 {code} 의 런 {run!r} 기록 요청 칸 {rq} = 생산자가 쓰지 않는 값 (`run_request` · 러너 ARMS · ARM_LIST · ★ 11-08 PC12-01)'
    want = record_outdir(rr)                                 # 요청 칸이 정하는 정확한 이름 (접두만 맞춘 옆 이름 <런>_arm9 = 검사 실패 흔적 비킴)
    if want is not None and od != want:
''', 'F1b request fields in stopped_record_problem')

# ── F2 ④ 교체 ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────
rep('''    if code == 'GROUP_UNCONFIRMED':
        cf = chain_confirmed(folder, run)
        if cf is not None and cf is not False:
            return f'멈춤 GROUP_UNCONFIRMED 인데 런 {run!r} 끝 기록의 사슬 쪽 확인 = {cf!r} (생산자 = 확인 False 일 때만 이 멈춤 · ★ 11-06 PC10 P2-B)'
    return None


def chain_confirmed(folder, run):
''', '''    side = chain_side(folder, run)                           # ★ 11-08 PC12-02 — 사슬 쪽 끝 기록 (원인 · rc · 확인) ↔ 런 기록 꼴 · 멈춤 코드 (옛 = GU 의 확인 칸만)
    if side == 'bad':
        return f'멈춤 {code} 인데 런 {run!r} 끝 기록의 사슬 쪽이 생산자 꼴이 아니다 (by 가 chain · recover 아님 · chain_end 가 객체 아님 · ★ 11-06 PC10 P2-B)'
    if side is not None:
        why = chain_side_problem(code, run, rr, run_record_shape(rr), side)
        if why:
            return why
    return None


def chain_confirmed(folder, run):
''', 'F2 ④ replace')

# ── F2 chain_confirmed → chain_side + 표 + chain_side_problem + F3 prior_runs_problem ───────────────────────────────────────────
new_cc = '''def chain_side(folder, run):
    """★ 11-08 PC12-02 (사전 공격 12 회차 F2 · 1저자 11-06 규칙) — 그 런 그룹 끝 기록 (시작 기록에 결합 · `group_pair`) 의 **사슬 쪽** (원인 · rc · 확인) → dict (그 세 칸 ·
    없는 칸 = None) · None (못 읽음 = 이름 RUN_DIR_RE 밖 · 시작 기록 없음 · 결합 안 됨 · chain_end 칸 없는 recover 끝 기록 = 옛 판 · 대조 안 함) · 'bad' (읽었는데 생산자
    꼴 아님 = by 가 chain · recover 아님 · chain_end 가 객체 아님).  사슬 쪽 = by chain 끝 기록 자신 (`run_in_group` 이 디스크에 쓴 cause · rc · confirmed) · by recover
    끝 기록의 chain_end (`recover_group` 이 옮긴 같은 세 칸 · recover 는 확인 안 된 끝 기록만 갈아 쓴다).  옛 `chain_confirmed` 는 확인 칸만 돌려줬다 (그 자리 그대로 =
    아래 wrapper)."""
    if not (isinstance(run, str) and RUN_DIR_RE.fullmatch(run)):
        return None
    lp = Path(folder) / GROUPS_DIR / f'{run}.launch.json'
    if not os.path.lexists(str(lp)):
        return None
    _L, er, bound = group_pair(lp)
    if not bound:
        return None
    by = er.get('by')
    if by == 'chain':
        return {k: er.get(k) for k in ('cause', 'rc', 'confirmed')}
    if by == 'recover':
        if 'chain_end' not in er:
            return None
        ce = er['chain_end']
        return {k: ce.get(k) for k in ('cause', 'rc', 'confirmed')} if isinstance(ce, dict) else 'bad'
    return 'bad'


def chain_confirmed(folder, run):
    """★ 11-06 PC10 확장 P2-B — 그 런 끝 기록의 사슬 쪽 종료 확인 → True | False (그 값) · None (못 읽음) · 'bad' (확인 값이 bool 아님 · 사슬 쪽 꼴 틀림) = `chain_side` 의
    확인 칸 (★ 11-08 PC12-02 — 대조 자체는 `chain_side_problem` 이 원인 · rc 까지 본다 · 이 함수 = 같은 읽기의 확인 칸 wrapper)."""
    side = chain_side(folder, run)
    if side is None or side == 'bad':
        return side
    v = side.get('confirmed')
    return v if type(v) is bool else 'bad'


#: ★ 11-08 PC12-02 (사전 공격 12 회차 F2) — 멈춘 런 기록 꼴 (`run_record_shape`) → 사슬 쪽 끝 기록의 (디스크 원인, rc 규칙) 생산자 대응.  생산자 = `Runner._execute`
#:   (rec.rc = 원인 None 일 때만 `run_in_group` 이 돌려준 rc = 디스크 끝 기록의 rc 그대로 · 그 밖 = None · rec.group_cause = 돌려준 원인) · `run_in_group` (디스크 끝 기록
#:   cause = None · timeout · signal · exception · rc = 회수한 정수 | null (SIGKILL 뒤 회수 못 함) · 정리 중 신호 = 돌려준 원인 signal_after · 디스크 원인 None 그대로 ·
#:   rc = 러너 스스로의 정수).  rc 규칙 = 'same' (정확히 런 기록의 rc · 정수) · 'int' (정수 · null 아님) · 'any' (정수 | null = `end_record_known` 의 사슬이 죽인 런 행).
CHAIN_SIDE_SHAPES = {'exit_ok': (None, 'same'), 'exit_fail': (None, 'same'), 'killed:signal_after': (None, 'int'),
                     'killed:timeout': ('timeout', 'any'), 'killed:signal': ('signal', 'any')}
#: ★ 11-08 PC12-02 — 멈춤 코드 → 사슬 쪽 확인 (`Runner._execute`: 확인 False ⇒ GROUP_UNCONFIRMED 가 먼저 · TIME_LIMIT (timeout) · RUNNER_RC (signal · signal_after ·
#:   rc ≠ 0) = 확인 True 뒤에만).
STOP_CONFIRMED = {'GROUP_UNCONFIRMED': False, 'TIME_LIMIT': True, 'RUNNER_RC': True}


def chain_side_problem(code, run, rr, shape, side):
    """★ 11-08 PC12-02 — 멈춤 code · 멈춘 런 기록 rr (꼴 shape = `run_record_shape`) ↔ 사슬 쪽 side (`chain_side` 의 dict) → 사유 | None.  옛 = GROUP_UNCONFIRMED 의 확인
    칸만 → 정직 GU (러너 스스로 rc 1 · 끝 기록 rc 1 · 확인 False) 의 런 기록 rc 1 → 0 한 칸 · {timeout · null} 두 칸이 group_unconfirmed · 재실행 자격을 얻었다."""
    cf = side.get('confirmed')
    if type(cf) is not bool:
        return f'멈춤 {code} 인데 런 {run!r} 끝 기록의 사슬 쪽 확인 = {cf!r} (bool 아님 · ★ 11-06 PC10 P2-B)'
    want_cf = STOP_CONFIRMED.get(code)
    if want_cf is not None and cf is not want_cf:
        return (f'멈춤 {code} 인데 런 {run!r} 끝 기록의 사슬 쪽 확인 = {cf!r} (생산자 = 확인 {want_cf} 일 때만 이 멈춤 — 확인 False 면 GROUP_UNCONFIRMED 먼저 · '
                f'★ 11-06 PC10 P2-B · ★ 11-08 PC12-02)')
    exp = CHAIN_SIDE_SHAPES.get(shape)
    if exp is None:
        return None                                        # 'none' · 'bad' = 다른 대조 몫 (`stop_record_problem`)
    cause, rule = exp
    sc, rc = side.get('cause'), side.get('rc')
    if sc != cause:
        return (f'멈춤 {code} 의 런 {run!r} 기록 꼴 {shape} 인데 끝 기록의 사슬 쪽 원인 = {sc!r} (생산자 = {cause!r} · signal_after 는 디스크 원인 None · '
                f'`run_in_group` · ★ 11-08 PC12-02)')
    k = rc_kind(rc)
    if ((rule == 'same' and not (k in ('ok', 'fail') and rc == rr.get('rc'))) or (rule == 'int' and k not in ('ok', 'fail'))
            or (rule == 'any' and k == 'bad')):
        what = '러너 스스로의 rc 그대로' if rule == 'same' else ('러너 스스로의 정수' if rule == 'int' else '회수한 정수 | null')
        return (f'멈춤 {code} 의 런 {run!r} 기록 rc {rr.get("rc")!r} (꼴 {shape}) ↔ 끝 기록의 사슬 쪽 rc {rc!r} (생산자 = {what} · `Runner._execute` · '
                f'★ 11-08 PC12-02)')
    return None


def prior_runs_problem(s, code, run, rr):
    """★ 11-08 PC12-03 (사전 공격 12 회차 F3 · F3b) — 멈춘 런 앞의 런 기록 전부 (런 기록 없는 멈춤 'none' = 런 전 TIME_LIMIT 는 runs 전부) 가 끝난 런인가: 꼴 exit_ok
    (`run_record_shape` · group_cause None · rc 정확한 정수 0) + arms_read = 비지 않은 목록 → 아니면 사유.  생산자 (`Runner._execute`) = rc 0 → `read_run` → arms_read =
    팔 기록 (비지 않음) 뒤에만 다음 런 · 실패 (rc ≠ 0 · 시간 초과 · 신호 · 그룹 미확인 · 팔 읽기 멈춤) = 그 자리에서 Stop = 그 뒤 런 기록 없음 (`ResumeRunner._copy` 의
    복사 기록 = rc 0 · group_cause None · 팔 기록 = 같은 꼴 · 합치기 `MergeFetch` 의 사본 기록 = 채택 시도의 끝난 런).  옛 = 멈춘 런 기록만 봤다 → 정직 RUNNER_RC (L01 rc 1 ·
    Traceback) 요약의 stop 두 칸 (TIME_LIMIT · run = 다음 이름 L02_ceiling · 생산자 이름 꼴도 아닌 'zzz') 만 바꾸면 timeout · 재실행 자격 · 재실행이 그 rc 1 런을 다시
    돌았다 (`ResumeRunner._src_done` False) · [L01 rc 1, 위조 L02 {timeout · null}] + 빈 L02 로그 · [L01 rc 1, L02 {None · 0}] + GU 도 같았다.  멈춘 런 기록 = runs 의
    마지막 (`stopped_record_problem` ①) 뒤에 부른다 · runs 가 목록이 아님 = None (`summary_shape_problem` 몫)."""
    runs = s.get('runs')
    if not isinstance(runs, list):
        return None
    prior = runs if rr is None else runs[:-1]
    for i, r in enumerate(prior):
        sh = run_record_shape(r)
        ar = r.get('arms_read') if isinstance(r, dict) else None
        if sh != 'exit_ok' or not (type(ar) is list and ar):
            nm = r.get('name') if isinstance(r, dict) else None
            return (f'멈춤 {code} · 런 {run!r} 앞의 런 기록 runs[{i}] ({nm!r}) = 꼴 {sh} · arms_read {"비지 않은 목록" if type(ar) is list and ar else repr(ar)[:40]} ≠ '
                    f'끝난 런 (생산자 = 앞 런이 rc 0 · 팔을 읽은 뒤에만 다음 런 · 실패 런 = 그 자리 멈춤 · ★ 11-08 PC12-03)')
    return None'''

# ── F1 (b) request_fields_problem + record_outdir ─────────────────────────────────────────────────────────────────────────────────
rep('''def record_outdir(rr):
    """★ 11-06 PC10 확장 P2-B — 런 기록 rr 의 요청 칸 (name · arms · arm_list = `run_request` 가 쓴 꼴) → 생산자의 출력 폴더 이름 (name + `run_outdir_suffix`) ·
    None (arms 칸 없음 = 요청 칸 없는 기록 · 시험 고정물 꼴 · ⚠ 한정 = 이때는 outdir 접두 규칙만 — 생산자 기록에는 늘 있다) · '' (칸 꼴 틀림 = 어떤
    outdir 와도 다름 · name 글 아님 · arms 정수 아님 (bool 포함) · arm_list 가 null · 정수 목록 아님)."""
    if 'arms' not in rr:
        return None
    n, al, name = rr.get('arms'), rr.get('arm_list'), rr.get('name')
    if not (isinstance(name, str) and type(n) is int and (al is None or (isinstance(al, list) and all(type(i) is int for i in al)))):
        return ''
    return name + run_outdir_suffix(n, al)
''', '''#: ★ 11-08 PC12-01 (사전 공격 12 회차 F1 · 1저자 11-06 규칙) — 요청 칸 (arms · arm_list) 의 생산자 범위 = `run_request` (arm_list = 정렬 · 비지 않음 · 중복 없음 · 0–7 ·
#:   접두 0..N−1 아님 (그건 ARMS=N) · arms = 그 길이 · 아니면 int(arms)) + 러너 `scripts/sdcp_gain_vox015_8arm.sh` (ARMS 1..8 · ARM_LIST 0–7 한 자리).  옛 = 꼴 (정수 ·
#:   정수 목록) 만 → arms 9 · 0 · −1 · 10**30 · arm_list [] · [0] · [9] · [3,3] · [3,1] · 길이 ≠ arms 로 지은 outdir 이 "요청 칸이 정하는 이름" 과 같아 받았다.
ARMS_RANGE = (1, 8)
ARM_INDEX_RANGE = (0, 7)


def request_fields_problem(rr):
    """★ 11-08 PC12-01 — 런 기록 rr 의 요청 칸 (arms · arm_list) 이 `run_request` 가 쓰는 값인가 → 사유 | None.  arms 칸 없음 = None (요청 칸 없는 기록 = 시험 고정물 꼴 ·
    한정 그대로 · `record_outdir` 의 None 자리)."""
    if 'arms' not in rr:
        return None
    n, al = rr.get('arms'), rr.get('arm_list')
    if type(n) is not int or not (ARMS_RANGE[0] <= n <= ARMS_RANGE[1]):
        return f'arms {n!r} (생산자 = 정수 {ARMS_RANGE[0]}–{ARMS_RANGE[1]})'
    if al is None:
        return None
    if not (isinstance(al, list) and al and all(type(i) is int for i in al)):
        return f'arm_list {al!r} (생산자 = null 또는 비지 않은 정수 목록)'
    if (al != sorted(al) or len(set(al)) != len(al) or al[0] < ARM_INDEX_RANGE[0] or al[-1] > ARM_INDEX_RANGE[1] or al == list(range(len(al)))
            or len(al) != n):
        return f'arm_list {al!r} · arms {n} (생산자 = 정렬 · 중복 없음 · {ARM_INDEX_RANGE[0]}–{ARM_INDEX_RANGE[1]} · 접두 0..N−1 아님 · arms = 길이)'
    return None


def record_outdir(rr):
    """★ 11-06 PC10 확장 P2-B — 런 기록 rr 의 요청 칸 (name · arms · arm_list = `run_request` 가 쓴 꼴) → 생산자의 출력 폴더 이름 (name + `run_outdir_suffix`) ·
    None (arms 칸 없음 = 요청 칸 없는 기록 · 시험 고정물 꼴 · ⚠ 한정 = 이때는 outdir 접두 규칙만 — 생산자 기록에는 늘 있다) · '' (칸 꼴 · 값 틀림 = 어떤
    outdir 와도 다름 · name 글 아님 · ★ 11-08 PC12-01 요청 칸이 생산자 범위 밖 = `request_fields_problem` 사유 있음 — arms 정수 아님 (bool 포함) · 1–8 밖 · arm_list 가
    null · 정수 목록 아님 · 정렬 · 중복 · 0–7 · 접두 · 길이 ≠ arms)."""
    if 'arms' not in rr:
        return None
    n, al, name = rr.get('arms'), rr.get('arm_list'), rr.get('name')
    if not isinstance(name, str) or request_fields_problem(rr) is not None:
        return ''
    return name + run_outdir_suffix(n, al)
''', 'F1b request_fields_problem + record_outdir')

# ── F1 (a) result_fields 흔적 ─────────────────────────────────────────────────────────────────────────────────────────────────────
rep('''        _rr, od = _stopped_run(s, folder)
        trace = False if done else (check_trace(folder, od) if od is not None else check_trace(folder))
''', '''        _rr, od = _stopped_run(s, folder)
        trace = False if done else stop_trace(folder, sr.get('run'), od)   # ★ 11-08 PC12-01 — 그 런의 출력 폴더 꼴 전부 (옛 = 기록의 outdir 하나)
''', 'F1a result_fields trace')

# ── F4 read_summary_state ─────────────────────────────────────────────────────────────────────────────────────────────────────────
rep('''    try:
        v = json.loads(raw.decode('utf-8'))
    except (UnicodeDecodeError, ValueError, RecursionError):
        return None, None, 'unreadable'
    if not isinstance(v, dict):
''', '''    try:
        v = _json_strict(raw)                                # ★ 11-08 PC12-04 — 거부 기록 · 계획 · 원장과 같은 읽기 (중복 칸 · NaN · ±Infinity = 못 읽음 · 옛 = json.loads = 뒤 값 · NaN 받음)
    except (UnicodeDecodeError, ValueError, RecursionError):
        return None, None, 'unreadable'
    if not isinstance(v, dict):
''', 'F4 strict json')
rep('''    읽기 = `read_regular_file` (한 번 연 fd · FIFO 에 막히지 않음).  옛 `read_summary` = 못 읽음도 없음과 같이 None (결과 줄 · 다시 셈이 요약 없는 시도로 읽어
    parent_dead · 재실행 자격) · 객체 아닌 JSON 은 그대로 돌려줌 (받는 쪽에서 AttributeError)."""
''', '''    읽기 = `read_regular_file` (한 번 연 fd · FIFO 에 막히지 않음) · JSON = `_json_strict` (★ 11-08 PC12-04 — 중복 칸 · NaN · ±Infinity = unreadable · 옛 = 느슨한
    json.loads 라 같은 바이트를 사람 = 앞 값 · 코드 = 뒤 값으로 읽었다 · 생산자 바이트 = `canon_bytes` (sort_keys · allow_nan False) 라 영향 없음).  옛 `read_summary` =
    못 읽음도 없음과 같이 None (결과 줄 · 다시 셈이 요약 없는 시도로 읽어 parent_dead · 재실행 자격) · 객체 아닌 JSON 은 그대로 돌려줌 (받는 쪽에서 AttributeError)."""
''', 'F4 docstring')

# ── F5 rejected_form_problem ──────────────────────────────────────────────────────────────────────────────────────────────────────
rep('''    if not (type(rec['code']) is str and STOP_CODE_RE.fullmatch(rec['code'])):
        return f'code {rec["code"]!r} (멈춤 이름 꼴 아님)'
''', '''    if not (type(rec['code']) is str and STOP_CODE_RE.fullmatch(rec['code']) and rec['code'] in STOPS):
        return f'code {rec["code"]!r} (멈춤 이름 아님 — `STOPS` 밖 · ★ 11-08 PC12-05 · 옛 = 글자 꼴만)'
''', 'F5 code in STOPS')

# ── 머리말 ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
rep('''  runs · outdir 꼴 틀림 = 폴더마다 멈춤 · 뒤 폴더 계속 · 옛 = traceback)
"""
''', '''  runs · outdir 꼴 틀림 = 폴더마다 멈춤 · 뒤 폴더 계속 · 옛 = traceback)
★ 11-08 PC12-01 – 05 (독립 사전 공격 12 회차 · 같은 규칙 · 보고 `docs/reviews/rint2_rr2_fix_evidence_20261105/pc12_fix/REPORT.md`): 멈춘 런 기록의 요청 칸 = 생산자
  범위 (`request_fields_problem` — `run_request` · 러너 ARMS 1–8 · ARM_LIST 0–7 · 정렬 · 중복 없음 · 접두 아님 · arms = 길이) · 검사 실패 흔적 = 그 런의 출력 폴더 꼴
  전부 (`stop_trace` · 옛 = 기록의 outdir 하나) · 멈춘 런 기록 꼴 ↔ 사슬 쪽 끝 기록 (원인 · rc · 확인) 생산자 대응표 (`chain_side` · `CHAIN_SIDE_SHAPES` ·
  `STOP_CONFIRMED` · `chain_side_problem` · 옛 = GU 의 확인 칸만) · 멈춘 런 앞의 런 기록 전부 = 끝난 런 (`prior_runs_problem` · 런 기록 없는 TIME_LIMIT 도) · 결과 줄
  길의 단계 요약 읽기 = `_json_strict` (중복 칸 · NaN · ±Infinity = unreadable) · 거부 기록 code ∈ `STOPS`.
"""
''', 'module docstring')

for old, new, label in edits:
    n = src.count(old)
    assert n == 1, f'{label}: {n} matches'
    src = src.replace(old, new)
# ── chain_confirmed 통째 교체 (앵커 편집 뒤 — ④ 편집의 끝 앵커가 옛 이름이라) ──
start = src.index('def chain_confirmed(folder, run):\n')
end = src.index('\n\n\ndef stop_record_readable(s, folder):')
old_cc = src[start:end]
assert old_cc.count('\ndef ') == 0 and "return v if type(v) is bool else 'bad'" in old_cc, old_cc[:200]
src = src[:start] + new_cc + src[end:]
compile(src, str(p), 'exec')
tmp = p.with_name(p.name + '.tmp')
tmp.write_text(src, encoding='utf-8')
os.replace(tmp, p)
print('applied', len(edits) + 1, 'edits;', len(src.splitlines()), 'lines')
