"""B-min 오프라인 후보를 NORMAL480 원본 바이트에서 결정적으로 만든다 — 텍스트 치환만 (후보 코드의 import · 실행 · 컴파일 · 구문 해석 0).

  python3 tools/build_candidate.py            # 패키지 루트 (comsol_candidates/bmin_particle640_20261004) 에서 실행
  python3 tools/build_candidate.py --check    # 쓰지 않고, 지금 candidate/ 의 바이트가 이 스크립트의 결과와 같은지만 본다

입력: basis/source480/candidate/ 의 NORMAL480 원본 8 파일 (크기 · SHA-256 을 먼저 대조 — 다르면 멈춘다).
출력: candidate/ — CODE_MANIFEST · CONTRACT · COMMAND_MAP · NATIVE_APPROVAL_FIELD_SPEC · PARENT_COMMAND.ps1 (CRLF) ·
      src/Bmin640Candidate.java · src/candidate_entry.py · src/diagnostic_consumer.py (CRLF).
모든 치환은 (이전 문자열, 이후 문자열, 정확한 횟수) 로 적고 횟수가 다르면 멈춘다. 같은 표가 LITERAL_CHANGE_MAP.json 이 된다.
허용 diff 는 B-min v2 (docs/COMSOL_BMIN_SCOPE_v2_20261004.md) §3 의 ① 입자 Nel ② 끝 시각 · 요청 목록 ③ 경로 · 식별자 ④ 기준 결속 · 판정 · 예산 연결.
"""
import hashlib
import json
import pathlib
import sys

PKG = pathlib.Path(__file__).resolve().parent.parent
BASIS = PKG / "basis/source480/candidate"
OUT = PKG / "candidate"

OLD_ROOT = "C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/normal480_offline_preparation_20261001"
NEW_ROOT = "C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/bmin_particle640_offline_preparation_20261004"
BASELINE_TABLES = OLD_ROOT + "/future_run_001/tables/"
RUN_ID = "bmin_particle640_candidate_001"
PREVIOUS_MANIFEST = "7a5cc2f1717ae7a80cd7e423861965ad51c5f639272eab7f3a3c7680499ae22c"

# NORMAL480 원본 8 파일 — COMSOL_REBUILD_SPEC §45-2 / R480 ARCHIVE_AUDIT 값.
BASIS_PINS = {
    "CODE_MANIFEST.json": (1046, "7a5cc2f1717ae7a80cd7e423861965ad51c5f639272eab7f3a3c7680499ae22c"),
    "COMMAND_MAP.json": (6045, "e29109239edc0246657d41a097ea2ed369fa446c559286dad5aa5b7e3d925fec"),
    "CONTRACT.json": (125504, "58d398a663ceb35e49154c32ab04ce0ea5720f7fe0664db0e0fa09f1dfdf3b08"),
    "NATIVE_APPROVAL_FIELD_SPEC.json": (4125, "8f4c90fb13382bde3f11a307e4247a829a00f1a5caa7558b9597ffb2f5d5a327"),
    "PARENT_COMMAND.ps1": (19213, "e8a770f5908c30a981875c49d92e4e6657efc6bf0273c217001fbadb69d667c9"),
    "src/Normal480Candidate.java": (99959, "c70526cf6884eabc57b63dd43dce4b47fb0decf59af68d3f550f1b987d053797"),
    "src/candidate_entry.py": (13999, "6178a0c5b6ce79b22dc3e1a1ee717536fb8ef055834c2a28e1221c1b4b0937e5"),
    "src/diagnostic_consumer.py": (20369, "c952e7c2674efd45f31d534998a4b63629558d45ec47d03d37b3e08682ed835c"),
}

# NORMAL480 기준 표 — B-min v2 §3 (R480 ARCHIVE_AUDIT 의 ZIP member run/tables/… 크기 · SHA-256).
BASELINE_FILES = {
    "electrolyte_guard.csv": (666849, "7117e79c6d5a14414b44520431831ccf9f0dd2372df4994e8ef070953bd5d4ed"),
    "preflight_global.csv": (1595210, "ac14d0d2cd7d90dd65dd098874ea5078476fc37a2958cea527fe78a2afb1771d"),
    "preflight_boundary1.csv": (1391054, "9773647829502178f22cfc5db3c682a046aa7b26ef35d035c1ee95527df31ceb"),
    "preflight_boundary4.csv": (1448183, "bdebcf47edc3e0aa3c33fd2cfa58cbc9f3cc3bf0b405e4591451019a8af4d6f4"),
    "axes_profile_N.csv": (203575457, "acdb34debf8d7c3c1108f1215f879000d887bcb4836e558a467b21c957153442"),
    "axes_profile_P.csv": (197290767, "2c91c90047aaabf6ffe203f8b4c970b0e2850af4d7ad143cde59ebed1f3dc5be"),
    "preflight_MinLine_ce.csv": (171715, "c59462b7f1d533d80016dad19b53c65c6891adead9cf0b498ec7cf014e715c69"),
    "preflight_MaxLine_ce.csv": (171672, "8d13c3f2b38459eeb26b70e297413a5d2531c470155ededc110314b1c4a69f01"),
    "axes_runtime_settings.csv": (28190, "19f32130a461b65aca63af0f96f7e4b80a871f5256149e861f2923e7c6d758dc"),
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def stop(msg):
    raise SystemExit("✗ " + msg)


def apply(text, table, label):
    for before, after, count, _category in table:
        got = text.count(before)
        if got != count:
            stop(f"{label}: {before[:60]!r} 횟수 {got} ≠ {count}")
        text = text.replace(before, after)
    return text


def lf(raw, label, crlf):
    text = raw.decode("utf-8")
    if crlf:
        if raw.count(b"\r\n") != raw.count(b"\n") or b"\r\n" not in raw:
            stop(f"{label}: 원본이 전부 CRLF 가 아니다")
        return text.replace("\r\n", "\n")
    if b"\r" in raw:
        stop(f"{label}: 원본에 CR 이 있다")
    return text


def segment(text, start, end, label):
    if text.count(start) != 1 or (end is not None and text.count(end) != 1):
        stop(f"{label}: 경계 표식이 유일하지 않다 ({start!r} · {end!r})")
    a = text.index(start)
    b = len(text) if end is None else text.index(end)
    if b <= a:
        stop(f"{label}: 경계 순서")
    return a, b


# ---------------------------------------------------------------- Java (문자 치환만)
def java_table(old_tlist, new_tlist):
    return [
        ("Normal480Candidate", "Bmin640Candidate", 2, "③"),
        ("a 480-second transient only", "a 150-second transient only", 1, "②"),
        ("values[0][i]>480", "values[0][i]>150", 1, "②"),
        ("0..480 seconds", "0..150 seconds", 1, "②"),
        ("480 seconds only", "150 seconds only", 1, "②"),
        ('set("Nel","320")', 'set("Nel","640")', 2, "①"),
        ('set("tlist","' + old_tlist + '")', 'set("tlist","' + new_tlist + '")', 1, "②"),
        ("NORMAL480_PRODUCER_COMPLETE", "BMIN640_PRODUCER_COMPLETE", 1, "③"),
    ]


# ---------------------------------------------------------------- entry (문자 치환만)
ENTRY_TABLE = [
    ("'_normal480_existing_c2'", "'_bmin640_existing_c2'", 1, "③"),
    ("native480_one_shot", "native_bmin640_one_shot", 1, "③"),
    ("Normal480Candidate", "Bmin640Candidate", 3, "③"),
    ("'_normal480_consumer'", "'_bmin640_consumer'", 1, "③"),
    ("'NORMAL_480S_DIAGNOSTIC_COMPLETE'", "'BMIN640_150S_COMPARISON_COMPLETE'", 1, "④"),
]

# ---------------------------------------------------------------- consumer — 문자 치환 (종료 · native 표식)
CONSUMER_LITERALS = [
    ('"""UNEXECUTED candidate: normal480/protected-stop consumer. No COMSOL/import/process calls.',
     '"""UNEXECUTED candidate: bmin640 150 s/protected-stop consumer (particle Nel 640 vs NORMAL480 run/tables, 120-150 s window). No COMSOL/import/process calls.', 1, "③"),
    ("need(number(c['maximum_physical_s'])==480,'NORMAL_END_CONTRACT')", "need(number(c['maximum_physical_s'])==150,'NORMAL_END_CONTRACT')", 1, "②"),
    ("need(0<=t<=480,'GUARD_TIME_RANGE')", "need(0<=t<=150,'GUARD_TIME_RANGE')", 1, "②"),
    ("need(0<minus<plus<=480,'STOP_PAIR')", "need(0<minus<plus<=150,'STOP_PAIR')", 1, "②"),
    ("need(ts[-1]==480,'DID_NOT_REACH_480');status='NORMAL_480S_REACHED'", "need(ts[-1]==150,'DID_NOT_REACH_150');status='NORMAL_150S_REACHED'", 1, "②"),
    ("normal=pair['status']=='NORMAL_480S_REACHED'", "normal=pair['status']=='NORMAL_150S_REACHED'", 1, "②"),
    ("console.count('NORMAL480_PRODUCER_COMPLETE')==1", "console.count('BMIN640_PRODUCER_COMPLETE')==1", 1, "③"),
]

CONSUMER_HEADERS_ANCHOR = "    HEADERS[_n]='time_s coordinate_m x_surface x_particle_average Eeq_V etaMid_V phil_V domain_id'.split()\n"
CONSUMER_HEADERS_ADD = (
    "for _n in ('preflight_MinLine_ce.csv','preflight_MaxLine_ce.csv'):\n"
    "    HEADERS[_n]='time_s ce_mol_m3'.split()\n"
)

# coverage → window_coverage + extreme (기준 결속 · 판정 — ④)
NEW_WINDOW = r"""def window_coverage(c,target,baseline,minus):
    start,end=(number(c['comparison_window_s'][k]) for k in ('start','end'))
    need(start==120 and end==150 and number(c['maximum_physical_s'])==end,'WINDOW_CONTRACT')
    requested=[number(x) for x in c['requested_times_s']]
    need(len(requested)==len(set(requested))==1637 and requested[0]==0 and requested[-1]==end,'REQUEST_CONTRACT')
    primary=[t for t in requested if start<=t<=end]
    need(len(primary)==c['primary_comparison_count']==301 and [str(t) for t in primary]==c['primary_comparison_times_s'],'PRIMARY_CONTRACT')
    actual=set(target);base=set(baseline);chosen=set(primary)
    reach=[t for t in primary if t<=minus];strict=[t for t in requested if t<=minus]
    missing_target=[t for t in reach if t not in actual];missing_base=[t for t in primary if t not in base]
    missing_strict=[t for t in strict if t not in actual]
    aux=sorted(t for t in actual&base if start<=t<=min(end,minus) and t not in chosen)
    outside=[t for t in requested if t<start and t<=minus and t in actual and t in base]
    info={'status':'PASS','window_start_s':str(start),'window_end_s':str(end),'safe_prefix_end_s':str(minus),
          'primary_expected':[str(t) for t in primary],'primary_compared':[str(t) for t in reach],'primary_compared_count':len(reach),
          'primary_complete':len(reach)==len(primary),'missing_target':[str(t) for t in missing_target],'missing_baseline':[str(t) for t in missing_base],
          'auxiliary_common_stored':[str(t) for t in aux],'auxiliary_count':len(aux),'outside_window_requested_common_count':len(outside),
          'strict_requested_through_safe_end':[str(t) for t in strict],'missing_strict_requested':[str(t) for t in missing_strict],
          'policy':'Exact membership. Primary = contract requested times in [120,150] (301), judged; auxiliary = extra exact common stored times in the window, reported separately, never judged; outside-window requested times are observation only. No interpolation, nearest substitution or rounding match.'}
    need(not missing_target and not missing_base and not missing_strict,'STRICT_REQUEST_TIME_MISSING:'+json.dumps(info))
    return reach,aux,outside,info
def extreme(items):
    # First maximum |delta| in iteration order (later ties do not replace it); None for an empty set.
    best=None
    for d,t,j in items:
        if best is None or abs(d)>abs(best[0]):best=(d,t,j)
    if best is None:return None
    return {'maximum_absolute':str(abs(best[0])),'signed_delta':str(best[0]),'time_s':str(best[1]),'coordinate_index':best[2]}
"""

NEW_NUMERIC = r"""def numeric(c,folder,g,minus):
    need(number(c['limits']['voltage_V'])==D('0.001') and number(c['limits']['surface_x'])==D('0.0001'),'LIMIT_CONTRACT')
    names=['preflight_global.csv','preflight_boundary1.csv','preflight_boundary4.csv']
    data={n:timed(folder/n) for n in names};times=list(g)
    need(all(list(x)==times for x in data.values()),'NUMERIC_TIME_SET')
    base={n:timed(pinned(c['baseline_files'][n])) for n in names}
    need(all(list(x)==list(base[names[0]]) for x in base.values()),'BASELINE_TIME_SET')
    primary,aux,outside,info=window_coverage(c,times,base[names[0]],minus)
    bg=timed(pinned(c['baseline_files']['electrolyte_guard.csv']))
    need(list(bg)==list(base[names[0]]),'BASELINE_GUARD_TIME_SET')
    lines={}
    for kind in ('MinLine','MaxLine'):
        name='preflight_'+kind+'_ce.csv';lines[kind]=(timed(folder/name),timed(pinned(c['baseline_files'][name])))
        need(list(lines[kind][0])==times and list(lines[kind][1])==list(bg),'ELECTROLYTE_LINE_TIME_SET')
    glob,n,p=(data[n] for n in names);bglob,bn,bp=(base[n] for n in names)
    li_keys=('Li_N_mol_m2','Li_P_mol_m2','Li_electrolyte_mol_m2')
    L0=sum(glob[D(0)][k] for k in li_keys);need(L0>0,'LI_INITIAL')
    components={}
    for key in li_keys:
        current=glob[D(0)][key];reference=bglob[D(0)][key]
        need(current>0 and reference>0,'INITIAL_LI_COMPONENT_POSITIVE')
        delta=abs(current-reference);limit=number(c['limits']['initial_Li_absolute_mol_m2'])
        need(limit==D('1e-9'),'INITIAL_LI_LIMIT')
        need(delta<=limit,'INITIAL_LI_COMPONENT')
        components[key]={'status':'PASS','current':str(current),'baseline':str(reference),'absolute_delta':str(delta),'unit':'mol/m^2','absolute_limit':'1e-9','relative_delta_reference_only':str(delta/reference)}
    li=voltage=D(0)
    for t in times:
        v=glob[t];need(v['ocp_guard']==0,'GLOBAL_OCP_GUARD')
        for lo,hi,col in [(D(0),D('.98'),'N'),(D('.2228930343076256'),D('.983245033354389'),'P')]:
            need(lo<=v['xsurf_'+col+'_min']<=v['xsurf_'+col+'_max']<=hi and v['xsurf_'+col+'_min']>0 and v['xsurf_'+col+'_max']<1,'GLOBAL_SURFACE_RANGE')
        Lt=sum(v[k] for k in li_keys);li=max(li,abs((Lt-L0)/L0))
        V=p[t]['phis_V']-n[t]['phis_V'];parts=sum(p[t][k]-n[t][k] for k in ('Eeq_V','etamid_V','phil_V'));voltage=max(voltage,abs(V-parts))
    need(li<=number(c['limits']['relative_Li']),'LI_DRIFT');need(voltage<=number(c['limits']['voltage_identity_V']),'VOLTAGE_IDENTITY')
    ce_keys=['ce_min_all_mol_m3','ce_min_d1_mol_m3','ce_min_d2_mol_m3','ce_min_d3_mol_m3']
    sets=(('primary',primary),('auxiliary',aux),('outside_window_observation',outside));windows={}
    for key,ts in sets:
        w={'time_count':len(ts),
           'voltage_V':extreme(((p[t]['phis_V']-n[t]['phis_V'])-(bp[t]['phis_V']-bn[t]['phis_V']),t,None) for t in ts),
           'total_Li_mol_m2':extreme((sum(glob[t][k] for k in li_keys)-sum(bglob[t][k] for k in li_keys),t,None) for t in ts)}
        for k in ce_keys:w[k]=extreme((g[t][k]-bg[t][k],t,None) for t in ts)
        for kind,(cur_l,old_l) in lines.items():w['ce_'+kind]=extreme((cur_l[t]['ce_mol_m3']-old_l[t]['ce_mol_m3'],t,None) for t in ts)
        windows[key]=w
    for electrode,domain in [('N',1),('P',3)]:
        name='axes_profile_'+electrode+'.csv'
        cur=profile(folder/name,times,c['coordinates'][electrode],domain,number(c['limits']['coordinate_m']))
        old=profile(pinned(c['baseline_files'][name]),base[names[0]],c['coordinates'][electrode],domain,number(c['limits']['coordinate_m']))
        for key,ts in sets:
            m=extreme((a-b,t,j) for t in ts for j,(a,b) in enumerate(zip(cur[t],old[t])))
            if m is not None:m['coordinate_m']=c['coordinates'][electrode][m['coordinate_index']]
            windows[key]['surface_x_'+electrode]=m
    return {'status':'PASS','coverage':info,'windows':windows,'initial_Li_components':components,
            'maximum_Li_relative_drift':str(li),'maximum_voltage_identity_V':str(voltage),
            'sign_convention':'delta = candidate (particle Nel 640) minus NORMAL480 (particle Nel 320) at identical stored times; surface deltas pointwise over the 241 contract coordinates per electrode',
            'judged_window':'primary only; auxiliary and outside_window_observation are never judged',
            'observation_tolerance':None}
"""

NEW_INCOMPLETE = r"""def incomplete_result(state=None):
    state=state or {}
    return {'limited_result':'INCOMPLETE','diagnostic':'INCOMPLETE','sampled_comparison':'INCOMPLETE',
            'preservation':state.get('preservation','INCOMPLETE'),'process_cleanup':state.get('process_cleanup','INCOMPLETE'),
            'policy_preservation':state.get('policy_preservation','INCOMPLETE'),'errors':[],
            'overall':'INCOMPLETE','normal_gate':'INCOMPLETE','effective_policy':'UNVERIFIED','native_approved_by_this_result':False,
            'native_completion':'NOT_ESTABLISHED','evidence_validity':'INVALID','mesh_comparison':'INCONCLUSIVE'}

"""

NEW_ANALYZE = r"""def analyze(c,folder,batch,console,state):
    result=incomplete_result(state);folder=Path(folder)
    try:
        # Termination first, so native_completion stays a separate field from the configuration evidence (B-min v2 section 6).
        g=timed(folder/'electrolyte_guard.csv');termination=guard_evidence(c,g)
        result['termination']=termination;result['native_termination']=native_stop(c,batch,console,termination)
        result['diagnostic']=termination['status']
    except Exception as e:result['errors'].append({'axis':'termination','type':type(e).__name__,'error':str(e)});return three_fields(c,result,state)
    try:
        binding_evidence(c,folder,console);result['runtime_settings']=runtime_evidence(c,folder)
        result['mesh_readback']=mesh_evidence(c,batch,console)
    except Exception as e:result['errors'].append({'axis':'configuration','type':type(e).__name__,'error':str(e)});return three_fields(c,result,state)
    try:
        units_evidence(folder)
        with localcontext() as ctx:
            ctx.prec=50;result['numeric']=numeric(c,folder,g,number(termination['safe_prefix_end_s']))
        result['sampled_comparison']='PASS'
    except Exception as e:result['errors'].append({'axis':'numeric','type':type(e).__name__,'error':str(e)})
    accepted=(not result['errors'] and state.get('status')=='NATIVE_RETURN_READY' and state.get('errors')==[]
              and result['sampled_comparison']=='PASS' and all(result[k]=='PASS' for k in ('preservation','process_cleanup','policy_preservation')))
    if accepted:
        result['limited_result']='BMIN640_150S_COMPARISON_COMPLETE' if result['diagnostic']=='NORMAL_150S_REACHED' else 'PROTECTED_STOP_150S_INCOMPLETE'
    # Observed protection survives numeric failure in diagnostic/termination; never a normal success.
    return three_fields(c,result,state)
def three_fields(c,result,state):
    # B-min v2 section 6: three separate fields. A limit excess is a valid comparison result, never a solver failure.
    native=result.get('native_termination') or {}
    if result['diagnostic']=='NORMAL_150S_REACHED' and native.get('status')=='NATIVE_NORMAL_END_MATCHED' and state.get('status')=='NATIVE_RETURN_READY' and state.get('errors')==[]:
        result['native_completion']='NORMAL_150S_COMPLETED'
    elif result['diagnostic']=='PROTECTIVE_STOP_OBSERVED' and native.get('status')=='NATIVE_PROTECTIVE_STOP_MATCHED':
        result['native_completion']='PROTECTIVE_STOP'
    else:
        result['native_completion']='NOT_ESTABLISHED'
    result['native_completion_cause']=None if result['native_completion']=='NORMAL_150S_COMPLETED' else {
        'diagnostic':result['diagnostic'],'native_status':native.get('status'),'state_status':state.get('status'),'state_errors':state.get('errors'),
        'termination_errors':[e for e in result['errors'] if e.get('axis')=='termination']}
    valid=result['limited_result']=='BMIN640_150S_COMPARISON_COMPLETE'
    result['evidence_validity']='VALID' if valid else 'INVALID'
    result['evidence_failures']=[] if valid else list(result['errors'])+[{'stage':'native_state','status':state.get('status'),'errors':state.get('errors')}]
    if valid:
        pw=result['numeric']['windows']['primary'];lv=number(c['limits']['voltage_V']);lx=number(c['limits']['surface_x'])
        within=number(pw['voltage_V']['maximum_absolute'])<=lv and all(number(pw['surface_x_'+e]['maximum_absolute'])<=lx for e in ('N','P'))
        result['mesh_comparison']='WITHIN_LIMITS_THIS_WINDOW' if within else 'EXCEEDS_LIMITS'
    else:
        result['mesh_comparison']='INCONCLUSIVE'
    result['mesh_comparison_rule']=c['comparison_rule']
    result['mesh_comparison_scope']='This input, particle radial mesh 320 vs 640 only, 120-150 s primary window, declared sample. Not an error bound, convergence order, true-solution accuracy, physical-mesh, late-480 s or finite-sigma claim.'
    result['field_authority']='Consumer values are provisional: the parent POST_WRITE record decides the final three fields after the entry, budget, delivery and record checks.'
    return result

"""

NEW_RUNTIME = r"""def runtime_evidence(c,folder):
    settings={}
    for r in rows(folder/'axes_runtime_settings.csv'):
        need(set(r)=={'key','actual_value'} and r['key'] not in settings,'RUNTIME_SETTINGS_SCHEMA')
        settings[r['key']]=r['actual_value']
    need(settings.get('study_tlist','').split()==c['requested_times_s'],'RUNTIME_TLIST')
    for k,v in c['runtime_settings_required'].items():need(settings.get(k)==v,'RUNTIME_SETTING:'+k)
    base={}
    for r in rows(pinned(c['baseline_files']['axes_runtime_settings.csv'])):
        need(set(r)=={'key','actual_value'} and r['key'] not in base,'BASELINE_SETTINGS_SCHEMA')
        base[r['key']]=r['actual_value']
    need(set(settings)==set(base),'RUNTIME_SETTING_KEYS_VS_NORMAL480')
    need(base['study_tlist'].split()[:len(c['requested_times_s'])]==c['requested_times_s'],'BASELINE_TLIST_PREFIX')
    diff=sorted(k for k in base if k!='study_tlist' and settings[k]!=base[k]);need(not diff,'RUNTIME_SETTING_VS_NORMAL480:'+','.join(diff))
    return {'status':'PASS','requested_count':len(c['requested_times_s']),'settings':{k:settings[k] for k in c['runtime_settings_required']},
            'baseline_comparison':{'status':'PASS','keys':len(base),'allowed_difference':['study_tlist = 1637-entry prefix of the NORMAL480 list']}}
def mesh_evidence(c,batch,console):
    lines=console.splitlines()
    for expected in c['mesh_readback_required']:need(lines.count(expected)==1,'MESH_READBACK:'+expected)
    found=[{'solved':int(a),'internal':int(b)} for a,b in re.findall(r'Number of degrees of freedom solved for: (\d+) \(plus (\d+) internal DOFs\)\.',batch)]
    want={'solved':c['expected_transient_dof']['solved'],'internal':c['expected_transient_dof']['internal']}
    return {'status':'PASS','required_lines':c['mesh_readback_required'],'batch_dof_lines':found,'expected_transient_dof':want,
            'last_dof_matches_expected':bool(found) and found[-1]==want,
            'dof_policy':'Recorded only (B-min v2 I-3): a mismatch is reported with its cause in the result review and is not a gate.'}
"""


def build_consumer(raw):
    text = lf(raw, "consumer", crlf=True)
    text = apply(text, CONSUMER_LITERALS, "consumer")
    if text.count(CONSUMER_HEADERS_ANCHOR) != 1:
        stop("consumer: HEADERS 기준 줄")
    text = text.replace(CONSUMER_HEADERS_ANCHOR, CONSUMER_HEADERS_ANCHOR + CONSUMER_HEADERS_ADD)
    blocks = [
        ("def coverage(", "def profile(", NEW_WINDOW),
        ("def numeric(", "def incomplete_result(", NEW_NUMERIC),
        ("def incomplete_result(", "def analyze(", NEW_INCOMPLETE),
        ("def analyze(", "def runtime_evidence(", NEW_ANALYZE),
        ("def runtime_evidence(", "def late_summary(", NEW_RUNTIME),
        ("def late_summary(", None, ""),
    ]
    for start, end, new in blocks:
        a, b = segment(text, start, end, "consumer")
        text = text[:a] + new + text[b:]
    for token in ("_480S", "NORMAL480_PRODUCER", "==480", "<=480", "REACH_480", "240", "B020", "late_summary", "comparison_end_s", "baseline_requested_times_s"):
        if token in text:
            stop(f"consumer: 남은 {token!r}")
    return text.replace("\n", "\r\n").encode("utf-8")


# ---------------------------------------------------------------- 부모 PS1
PS1_LITERALS = [
    ("$bRoot='" + OLD_ROOT + "'", "$bRoot='" + NEW_ROOT + "'", 1, "③"),
    ("GNumber $Overall 0 11400", "GNumber $Overall 0 10500", 1, "④"),
    ("GNumber $Analysis.elapsed_seconds 0 1800", "GNumber $Analysis.elapsed_seconds 0 900", 1, "④"),
    ("'NORMAL_480S_DIAGNOSTIC_COMPLETE'", "'BMIN640_150S_COMPARISON_COMPLETE'", 1, "④"),
    ("'PROTECTED_STOP_480S_INCOMPLETE'", "'PROTECTED_STOP_150S_INCOMPLETE'", 2, "④"),
    ("@('termination','native_termination','runtime_settings','numeric','tables_manifest')",
     "@('termination','native_termination','runtime_settings','mesh_readback','numeric','tables_manifest')", 1, "④"),
    ("requested_count -ne 4937", "requested_count -ne 1637", 1, "②"),
    ("GNumber $native.reported_time 0 480", "GNumber $native.reported_time 0 150", 1, "②"),
    ("GNumber $term.final_time_s 0 480", "GNumber $term.final_time_s 0 150", 1, "②"),
    ("GNumber $term.safe_prefix_end_s 0 480", "GNumber $term.safe_prefix_end_s 0 150", 1, "②"),
    ("'NORMAL_480S_REACHED'", "'NORMAL_150S_REACHED'", 2, "②"),
    ("GNumber $term.final_time_s 480 480", "GNumber $term.final_time_s 150 150", 1, "②"),
    ("GNumber $term.safe_prefix_end_s 480 480", "GNumber $term.safe_prefix_end_s 150 150", 1, "②"),
    ("GNumber $term.t_minus 0 480", "GNumber $term.t_minus 0 150", 1, "②"),
    ("GNumber $term.t_plus 0 480", "GNumber $term.t_plus 0 150", 1, "②"),
    ("'axes_profile_N.csv','axes_profile_P.csv')\n", "'axes_profile_N.csv','axes_profile_P.csv','preflight_MinLine_ce.csv','preflight_MaxLine_ce.csv')\n", 1, "④"),
    ("'AWAITING_480S_LIMITED_EXTERNAL_ACCEPTANCE'", "'AWAITING_BMIN640_150S_EXTERNAL_ACCEPTANCE'", 1, "④"),
    ("$a.native480_one_shot", "$a.native_bmin640_one_shot", 1, "③"),
    ("budget_seconds=11400}", "budget_seconds=10500}", 1, "④"),
    ("TotalSeconds -gt 11400)", "TotalSeconds -gt 10500)", 1, "④"),
    ("@{limited=$limited;overall='INCOMPLETE';native_return=", "@{limited=$limited;fields=(GFields $limited $result);overall='INCOMPLETE';native_return=", 1, "④"),
    ("$snapshot -le 11400", "$snapshot -le 10500", 1, "④"),
    (";body_completed_without_error=(@($bErrors).Count -eq 0);limited=$limited;local_decision=",
     ";body_completed_without_error=(@($bErrors).Count -eq 0);limited=$limited;fields=(GFields $limited $result);local_decision=", 1, "④"),
    ("$postWrite -le 11400", "$postWrite -le 10500", 1, "④"),
    ("observation_phase='POST_WRITE';limited=$limited;record_errors=", "observation_phase='POST_WRITE';limited=$limited;fields=(GFields $limited $result);record_errors=", 1, "④"),
]

PS1_BLOCK_START = "    foreach ($key in @('expected_requested','common_stored','missing_target','missing_baseline','target_noncommon','full_intersection','strict_requested_through_safe_end','missing_strict_requested')) {\n        if (-not (GHas $coverage $key)"
PS1_BLOCK_END = "    $required=@("
PS1_LI_LOOP_START = "    foreach ($key in @('Li_N_mol_m2','Li_P_mol_m2','Li_electrolyte_mol_m2')) {\n"

PS1_WINDOW = r"""    foreach ($key in @('primary_expected','primary_compared','missing_target','missing_baseline','auxiliary_common_stored','strict_requested_through_safe_end','missing_strict_requested')) {
        if (-not (GHas $coverage $key) -or $coverage.$key -isnot [array]) { return 'INCOMPLETE' }
    }
    if (@($coverage.primary_expected).Count -ne 301 -or $coverage.primary_expected[0] -cne '120' -or $coverage.primary_expected[-1] -cne '150' -or @($coverage.missing_target).Count -ne 0 -or @($coverage.missing_baseline).Count -ne 0 -or @($coverage.missing_strict_requested).Count -ne 0 -or $coverage.primary_compared_count -isnot [int] -or $coverage.primary_compared_count -ne @($coverage.primary_compared).Count -or $coverage.auxiliary_count -isnot [int] -or $coverage.auxiliary_count -ne @($coverage.auxiliary_common_stored).Count) { return 'INCOMPLETE' }
    foreach ($time in $coverage.primary_compared) { if ($coverage.primary_expected -cnotcontains $time) { return 'INCOMPLETE' } }
    if ($normal -and (@($coverage.primary_compared).Count -ne 301 -or $coverage.primary_complete -isnot [bool] -or -not $coverage.primary_complete -or @($coverage.strict_requested_through_safe_end).Count -ne 1637)) { return 'INCOMPLETE' }
    $maxima=@{maximum_Li_relative_drift=0.000001;maximum_voltage_identity_V=0.00000001}
    foreach ($key in $maxima.Keys) { if (-not (GHas $numeric $key) -or -not (GNumber $numeric.$key 0 $maxima[$key])) { return 'INCOMPLETE' } }
    if (-not (GStruct $numeric.initial_Li_components) -or -not (GStruct $numeric.windows) -or $Result.mesh_readback.status -cne 'PASS' -or -not (GStruct $Result.runtime_settings.baseline_comparison) -or $Result.runtime_settings.baseline_comparison.status -cne 'PASS') { return 'INCOMPLETE' }
"""

PS1_FIELDS = r"""    if ($normal) {
        $pw=$numeric.windows.primary
        if (-not (GStruct $pw) -or $pw.time_count -ne 301) { return 'INCOMPLETE' }
        $within=$true
        foreach ($pair in @(@('voltage_V','0.001'),@('surface_x_N','0.0001'),@('surface_x_P','0.0001'))) {
            $m=$pw.($pair[0]);$v=[decimal]0
            if (-not (GStruct $m) -or -not (GHas $m 'maximum_absolute') -or -not [decimal]::TryParse([string]$m.maximum_absolute,[Globalization.NumberStyles]::Float,[Globalization.CultureInfo]::InvariantCulture,[ref]$v) -or $v -lt 0) { return 'INCOMPLETE' }
            # Equal to the limit is within (<=); strictly greater is an excess (B-min v2 section 6, SPEC section 44-2).
            if ($v -gt [decimal]::Parse($pair[1],[Globalization.CultureInfo]::InvariantCulture)) { $within=$false }
        }
        $label=$(if ($within) { 'WITHIN_LIMITS_THIS_WINDOW' } else { 'EXCEEDS_LIMITS' })
        if ($Result.native_completion -cne 'NORMAL_150S_COMPLETED' -or $Result.evidence_validity -cne 'VALID' -or $Result.mesh_comparison -cne $label) { return 'INCOMPLETE' }
    } elseif ($Result.native_completion -cne 'PROTECTIVE_STOP' -or $Result.evidence_validity -cne 'INVALID' -or $Result.mesh_comparison -cne 'INCONCLUSIVE') { return 'INCOMPLETE' }
"""

PS1_GFIELDS_ANCHOR = "    return 'PROTECTED_STOP_150S_INCOMPLETE'\n}\ntry {\n"
PS1_GFIELDS = r"""function GFields([string]$Limited,$Result) {
    # Final three fields (B-min v2 section 6). Only a parent-accepted normal result carries the consumer verdict; everything else is INCONCLUSIVE.
    if ($Limited -ceq 'AWAITING_BMIN640_150S_EXTERNAL_ACCEPTANCE') { return @{native_completion=$Result.native_completion;evidence_validity=$Result.evidence_validity;mesh_comparison=$Result.mesh_comparison} }
    $completion='NOT_ESTABLISHED'
    if ($Limited -ceq 'PROTECTED_STOP_150S_INCOMPLETE') { $completion='PROTECTIVE_STOP' }
    $seen=$(if ($null -ne $Result) { [string]$Result.native_completion } else { $null })
    return @{native_completion=$completion;evidence_validity='INVALID';mesh_comparison='INCONCLUSIVE';consumer_native_completion_unverified=$seen}
}
"""


def build_ps1(raw):
    text = lf(raw, "ps1", crlf=True)
    a, b = segment(text, PS1_BLOCK_START, PS1_BLOCK_END, "ps1 block")
    old = text[a:b]
    if old.count(PS1_LI_LOOP_START) != 1:
        stop("ps1: 초기 Li 반복 위치")
    li_a = old.index(PS1_LI_LOOP_START)
    li_lines = old[li_a:].split("\n")
    li_loop = "\n".join(li_lines[:3]) + "\n"  # foreach … { / if … / } — 원문 그대로 유지
    if not (li_lines[2] == "    }" and li_lines[3].startswith("    if ($normal -and ($numeric.late_interval.status")):
        stop("ps1: 초기 Li 반복 끝 · late_interval 줄 위치")
    if old[li_a:] != li_loop + li_lines[3] + "\n":
        stop("ps1: 블록 끝이 late_interval 한 줄이 아니다")
    text = text[:a] + PS1_WINDOW + li_loop + PS1_FIELDS + text[b:]
    text = apply(text, PS1_LITERALS, "ps1")
    if text.count(PS1_GFIELDS_ANCHOR) != 1:
        stop("ps1: GFields 삽입 위치")
    text = text.replace(PS1_GFIELDS_ANCHOR, "    return 'PROTECTED_STOP_150S_INCOMPLETE'\n}\n" + PS1_GFIELDS + "try {\n")
    for token in ("480", "11400", "4937", "2537", "B020", "b020", "secondary", "late_interval", "1800"):
        if token in text:
            stop(f"ps1: 남은 {token!r}")
    return text.replace("\n", "\r\n").encode("utf-8")


# ---------------------------------------------------------------- JSON
def dump(obj):
    return (json.dumps(obj, indent=2, ensure_ascii=True) + "\n").encode("ascii")


def ref(path, raw):
    return {"path": path, "bytes": len(raw), "sha256": sha(raw)}


def commands():
    run = NEW_ROOT + "/future_run_001"
    return {
        "compile": ["C:/Program Files/COMSOL/COMSOL63/Multiphysics/bin/win64/comsolcompile.exe", "-prefsdir", run + "/prefs",
                    "-configuration", run + "/config_compile", "-data", run + "/data_compile", run + "/Bmin640Candidate.java"],
        "batch": ["C:/Program Files/COMSOL/COMSOL63/Multiphysics/bin/win64/comsolbatch.exe", "-prefsdir", run + "/prefs",
                  "-configuration", run + "/config_batch", "-data", run + "/data_batch", "-np", "16",
                  "-inputfile", run + "/Bmin640Candidate.class", "-outputfile", run + "/result.mph", "-batchlog", run + "/batch.log"],
    }


BUDGETS = {"preflight_and_input": 180, "compile_batch": 9000, "process_cleanup_total": 120, "analysis": 900, "delivery": 300, "overall": 10500}

COMPARISON_RULE = ("WITHIN_LIMITS_THIS_WINDOW iff native_completion and evidence_validity both hold and, on the 301 primary times, "
                   "max|dV| <= 0.001 V and max|dx_surface| <= 1e-4 for both electrodes (a value equal to a limit is within); "
                   "EXCEEDS_LIMITS iff both hold and any of the three is strictly greater than its limit; INCONCLUSIVE otherwise.")


def build_contract(old, java_raw):
    c = json.loads(old)
    if c["requested_times_s"][1636] != "150" or len(c["requested_times_s"]) != 4937:
        stop("contract: 요청 목록")
    c["run_id"] = RUN_ID
    c["root"] = NEW_ROOT
    c["run_root"] = NEW_ROOT + "/future_run_001"
    c["approval_path"] = NEW_ROOT + "/future_authorizations/bmin640_001.json"
    c["release_path"] = NEW_ROOT + "/future_authorizations/VALIDATION_RELEASE.json"
    c["candidate_java"] = ref(NEW_ROOT + "/src/Bmin640Candidate.java", java_raw)
    c["baseline_files"] = {name: {"path": BASELINE_TABLES + name, "bytes": size, "sha256": h} for name, (size, h) in BASELINE_FILES.items()}
    c["requested_times_s"] = c["requested_times_s"][:1637]
    c["maximum_physical_s"] = "150"
    c["budgets_seconds"] = dict(BUDGETS)
    c["resource_proposal"]["disk_start_gib"] = 15
    c["policy"]["native_permission_status"] = (
        "Earlier native runs (1198, normal30/60/120/240/480, rtol30) completed under unchanged policy per their accepted reviews. "
        "Native B-min640 requires separate approval and current prefs binding; effective policy UNVERIFIED; no fallback.")
    c["commands"] = commands()
    c["future_native_blockers"] = [
        "150 s bounds, NORMAL480 window comparison, three-field verdict and new budget bindings not functionally validated",
        "native B-min640 user approval and accepted release absent",
        "baseline table paths/bytes on the execution machine not yet observed (pinned identity fails closed)",
        "current source/policy/path/resource review pending",
        "full Java/native B-min640 (particle Nel 640) not observed",
    ]
    for gone in ("baseline_requested_times_s", "comparison_end_s", "b020_requested_times_s"):
        del c[gone]
    win = [t for t in c["requested_times_s"] if 120 <= float(t) <= 150]
    c["baseline_run"] = {
        "run_id": "normal480_candidate_001",
        "result_zip": {"name": "COMSOL63_NORMAL480_NATIVE_RESULT_20261001.zip", "bytes": 420748594,
                       "sha256": "e991ab4c918f6576b18d6225a86ed41759ab6ee726dd6543b9a9158e581cbc30"},
        "zip_manifest": {"bytes": 2076814, "sha256": "df992301a3ce93c5e50707bd858c6fe819b89f5189499bce0e3b6c29979c164b"},
        "contract": {"bytes": 125504, "sha256": "58d398a663ceb35e49154c32ab04ce0ea5720f7fe0664db0e0fa09f1dfdf3b08"},
        "code_manifest_sha256": PREVIOUS_MANIFEST,
        "diagnostic_result": {"bytes": 726474, "sha256": "24819a3a0b891c77dc69b40e2ada86eacece0b957cc207abbf40760d250b7783"},
        "tables_source": "run/tables of the NORMAL480 result (not the shorter baseline/ inside the same ZIP); paths above assume the NORMAL480 run root future_run_001/tables",
    }
    c["comparison_window_s"] = {"start": "120", "end": "150"}
    c["primary_comparison_count"] = len(win)
    c["primary_comparison_times_s"] = win
    c["comparison_rule"] = COMPARISON_RULE
    c["changed_axis"] = {"particle_Nel_pce1": {"from": "320", "to": "640"}, "particle_Nel_pce2": {"from": "320", "to": "640"},
                         "physical_mesh": "unchanged 120/60/120 (300)"}
    c["mesh_readback_required"] = [
        "AXES_PHYSICAL_MESH_DOMAIN=1|numelem=120", "AXES_PHYSICAL_MESH_DOMAIN=2|numelem=60", "AXES_PHYSICAL_MESH_DOMAIN=3|numelem=120",
        "AXES_PARTICLE=pce1|Nel=640|Nord=1|Distribution=CubicRoot", "AXES_PARTICLE=pce2|Nel=640|Nord=1|Distribution=CubicRoot",
        "AXES_ACTUAL_MESH=mesh1|edges=300|vertices=301",
    ]
    c["expected_transient_dof"] = {"solved": 156925, "internal": 12, "status": "RECORD_ONLY",
                                   "basis": "2045 + 242*Nel matched exactly at Nel 40/80/160/320 (SPEC l.460, l.618, l.788); 640 is an extrapolation"}
    if len(win) != 301 or win[0] != "120" or win[-1] != "150":
        stop("contract: 주 비교 301")
    return dump(c)


def build_manifest(files):
    return dump({"schema": 1, "run_id": RUN_ID, "approved": False, "usable": False, "status": "OFFLINE_CANDIDATE_NOT_VALIDATED",
                 "previous_manifest_sha256": PREVIOUS_MANIFEST,
                 "files": [{"file": f, "bytes": len(b), "sha256": sha(b)} for f, b in files]})


def build_command_map(old, manifest_sha):
    m = json.loads(old)
    text = json.dumps(m, ensure_ascii=True)
    text = text.replace(OLD_ROOT, NEW_ROOT).replace("Normal480Candidate", "Bmin640Candidate").replace("normal480_001.json", "bmin640_001.json")
    m = json.loads(text)
    m["manifest_sha256"] = manifest_sha
    for k in ("execute", "analyze"):
        m[k]["argv"][-1] = manifest_sha
    m["parent"]["argv"][-1] = manifest_sha
    if m["native"]["compile"]["argv"] != commands()["compile"] or m["native"]["batch"]["argv"] != commands()["batch"]:
        stop("command map: native 명령이 계약과 다르다")
    left = [k for k in ("normal480", "Normal480", "native480", "11400", "1800") if k in json.dumps(m)]
    if left:
        stop(f"command map: 남은 {left}")
    return dump(m)


def build_field_spec(old, manifest_sha):
    s = json.loads(old)
    s["run_id"] = RUN_ID
    s["code_manifest_sha256"] = manifest_sha
    s["future_approval_path"] = NEW_ROOT + "/future_authorizations/bmin640_001.json"
    s["future_release_path"] = NEW_ROOT + "/future_authorizations/VALIDATION_RELEASE.json"
    s["activation_requires"] = [
        "separate accepted changed-branch validation bound to unchanged manifest",
        "actual user native B-min640 decision (one attempt, fresh 0 -> 150 s)",
        "current approved default prefs identity",
        "current permission/path review using accepted route; no policy change",
        "NORMAL480 run/tables identities observed on the execution machine before the run",
    ]
    f = s["required_future_fields"]
    s["required_future_fields"] = {
        "approved": f["approved"],
        "native_bmin640_one_shot": "boolean true only for separately approved one native B-min640 attempt",
        "allow_policy_changes": f["allow_policy_changes"],
        "effective_policy_unverified_accepted": f["effective_policy_unverified_accepted"],
        "commands": commands(),
        "budgets_seconds": dict(BUDGETS),
        "user_decision": f["user_decision"],
        "validation_release": f["validation_release"],
        "default_prefs_identity": f["default_prefs_identity"],
    }
    left = [k for k in ("normal480", "Normal480", "native480", "11400", "1800") if k in json.dumps(s)]
    if left:
        stop(f"field spec: 남은 {left}")
    return dump(s)


def main():
    check_only = "--check" in sys.argv[1:]
    basis = {}
    for rel, (size, h) in BASIS_PINS.items():
        b = (BASIS / rel).read_bytes()
        if len(b) != size or sha(b) != h:
            stop(f"basis 바이트 불일치: {rel}")
        basis[rel] = b
    contract_old = json.loads(basis["CONTRACT.json"])
    old_tlist = " ".join(contract_old["requested_times_s"])
    new_tlist = " ".join(contract_old["requested_times_s"][:1637])

    java = lf(basis["src/Normal480Candidate.java"], "java", crlf=False)
    java = apply(java, java_table(old_tlist, new_tlist), "java")
    if java.count("480") != 3:  # 재료 표 숫자 안의 세 자리 (원본과 같은 자리) 만 남는다
        stop("java: 480 잔여 수")
    java_raw = java.encode("ascii")
    entry = apply(lf(basis["src/candidate_entry.py"], "entry", crlf=False), ENTRY_TABLE, "entry")
    if "480" in entry:
        stop("entry: 남은 480")
    entry_raw = entry.encode("ascii")
    consumer_raw = build_consumer(basis["src/diagnostic_consumer.py"])
    ps1_raw = build_ps1(basis["PARENT_COMMAND.ps1"])
    contract_raw = build_contract(basis["CONTRACT.json"], java_raw)
    manifest_raw = build_manifest([("src/Bmin640Candidate.java", java_raw), ("src/diagnostic_consumer.py", consumer_raw),
                                   ("src/candidate_entry.py", entry_raw), ("PARENT_COMMAND.ps1", ps1_raw), ("CONTRACT.json", contract_raw)])
    manifest_sha = sha(manifest_raw)
    outputs = {
        "src/Bmin640Candidate.java": java_raw,
        "src/candidate_entry.py": entry_raw,
        "src/diagnostic_consumer.py": consumer_raw,
        "PARENT_COMMAND.ps1": ps1_raw,
        "CONTRACT.json": contract_raw,
        "CODE_MANIFEST.json": manifest_raw,
        "COMMAND_MAP.json": build_command_map(basis["COMMAND_MAP.json"], manifest_sha),
        "NATIVE_APPROVAL_FIELD_SPEC.json": build_field_spec(basis["NATIVE_APPROVAL_FIELD_SPEC.json"], manifest_sha),
    }
    literal_map = {
        "categories": {"①": "particle Nel", "②": "end time 150 s and request list", "③": "run/output paths and identifiers",
                       "④": "baseline binding, judgment and budget connection"},
        "basis": "basis/source480/candidate (NORMAL480 originals)", "target": "candidate",
        "files": {f: [{"before": b, "after": a, "count": n, "category": k} for b, a, n, k in table] for f, table in (
            ("src/Normal480Candidate.java -> src/Bmin640Candidate.java", java_table(old_tlist, new_tlist)),
            ("src/candidate_entry.py", ENTRY_TABLE), ("src/diagnostic_consumer.py", CONSUMER_LITERALS), ("PARENT_COMMAND.ps1", PS1_LITERALS))},
        "not_literal": "Block-level changes of src/diagnostic_consumer.py and PARENT_COMMAND.ps1 are declared in CHANGE_BOUNDARIES.json.",
    }
    package_outputs = {"LITERAL_CHANGE_MAP.json": (json.dumps(literal_map, indent=2, ensure_ascii=False) + "\n").encode("utf-8")}
    bad = []
    for rel, raw in list(outputs.items()) + list(package_outputs.items()):
        p = (PKG if rel in package_outputs else OUT) / rel
        if check_only:
            if not p.is_file() or p.read_bytes() != raw:
                bad.append(rel)
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(raw)
        print(f"{'=' if check_only and rel not in bad else ('✗' if rel in bad else '+')} {rel:36s} {len(raw):>9,d} B  {sha(raw)}")
    print(f"manifest {manifest_sha}")
    if bad:
        stop(f"재생성 바이트 불일치 {len(bad)}: {bad}")


if __name__ == "__main__":
    main()
