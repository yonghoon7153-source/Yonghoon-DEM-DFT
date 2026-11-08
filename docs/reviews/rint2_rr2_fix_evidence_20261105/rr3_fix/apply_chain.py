#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RR3-01 고침 — scripts/rint_r_chain.py: 구조 계약 하나 (생성 `arms_read_record` · 분류 `arms_read_kind`) · 세 생산자 (Runner._execute · ResumeRunner._copy ·
MergeFetch.run) = 생성 함수 · 자격 소비자 `prior_runs_problem` = 분류 함수 (판독 완료 꼴만 끝난 런) · 머리말 문단.  바꿈마다 옛 글이 정확히 한 번 있어야 한다
(아니면 아무것도 쓰지 않고 멈춤) · 원자적 쓰기.

  python3 docs/reviews/rint2_rr2_fix_evidence_20261105/rr3_fix/apply_chain.py <리포 뿌리>
"""
import os
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
C = ROOT / 'scripts' / 'rint_r_chain.py'

NEW_FUNCS = '''    return sorted(out, key=lambda x: (x['index'], x['file']))


#: ★ 11-08 RR3-01 (Codex 회차 ③ · 1저자 11-08 Q1 · Q2 (가)) — 판독 실패 때 남기는 파일 신원 칸 (`arm_file_shas` · 계약 판정 안 함) · 판독 완료 칸 = `ARM_PUBLIC`
#:   (두 꼴은 칸 집합이 겹치지 않는다 — `arms_read_kind` 가 가른다) · sha256 꼴 = hashlib hexdigest (64 자리 소문자 hex)
ARM_FILE_ID_KEYS = ('file', 'index', 'sha256')
ARM_SHA256_RE = re.compile(r'[0-9a-f]{64}')


def arms_read_record(arms_=None, outdir=None):
    """★ 11-08 RR3-01 (Codex 회차 ③ · 판정문 §2 · 1저자 11-08 "권고대로" = 수정 계획 Q1 · Q2 (가) = 구조 계약 하나) 런 기록 arms_read 생성 — 세 생산자
    (`Runner._execute` · `ResumeRunner._copy` · `MergeFetch.run`) 가 같은 함수: 판독 완료 (arms_ = `read_run` 결과 · 요청 팔 차례) = 팔마다 `ARM_PUBLIC` 칸
    정확히 · 판독 실패 (arms_ None · outdir = 그 런 폴더) = 파일 신원 목록 (`arm_file_shas` · 칸 `ARM_FILE_ID_KEYS` · 판정 아님 · 판정이 원 팔에서 다시 계산할 수
    있게).  읽는 쪽 = `arms_read_kind` (자격 소비자 = `prior_runs_problem` 하나 · `_src_done` · 복사 다시 읽기 · want_sha 소비자 = 그대로)."""
    if arms_ is None:
        return arm_file_shas(outdir)
    return [{k: a[k] for k in ARM_PUBLIC} for a in arms_]


def arm_file_prefix(kit):
    """팔 파일 이름 앞자리 — `read_run` 의 킷 대조와 같은 식 (킷 'kit_<줄기>' → 'p2_<줄기>_' · 성공 판독의 팔 파일 = 모두 이 앞자리 · read_run 자리 글은 그대로)."""
    return f'p2_{kit[len("kit_"):]}_'


def arms_read_kind(ar, rec):
    """★ 11-08 RR3-01 — 런 기록 rec 의 arms_read 값 ar → (꼴, 사유): 'verified' (판독 완료 = `arms_read_record` 성공 꼴 — 비지 않은 목록 · 원소마다 객체 · 칸
    집합 = `ARM_PUBLIC` 정확히 · 그 기록의 요청 팔 (`arm_indices` · 요청 칸 arms · arm_list = `request_fields_problem` 통과 · 칸 없음 = 요청 팔을 모름) 과 일대일 =
    수 · 차례대로 번호 (정수 · bool 아님) · 파일 = 이름만 (경로 아님) · `arm_file_prefix` (그 기록의 kit) 앞자리 · 끝 _a<번호>.json · sha256 = 64 자리 소문자 hex ·
    사유 None) · 'file_ids' (판독 실패 때 남긴 파일 신원 목록 = 원소마다 칸 `ARM_FILE_ID_KEYS` 정확히 · 생산자 = `read_run` 실패 뒤) · 'empty' ([] = 팔을 읽기 전) ·
    'bad' (그 밖 — 목록 아님 · 섞인 칸 · 요청 팔 모름 · 대응 틀림).  옛 (`prior_runs_problem`) = "비지 않은 목록" → 판독 실패 기록의 파일 신원 목록도 끝난 런
    (Codex 회차 ③ RR3-01 · 요약 두 칸 = 재실행 자격).  ⚠ 한정: 값 (sha256 ↔ 디스크 파일 · 다른 런에서 옮겨 붙인 판독 완료 기록) 은 대조하지 않는다 (실제 재개
    복사는 원 팔을 다시 읽는다 · 여러 칸을 일관되게 고친 위조 = 판정문 §5 끝 · 새 요구 아님)."""
    if type(ar) is not list:
        return 'bad', f'목록 아님 ({type(ar).__name__})'
    if not ar:
        return 'empty', None
    if any(type(a) is not dict for a in ar):
        return 'bad', '원소가 객체가 아님'
    if all(set(a) == set(ARM_FILE_ID_KEYS) for a in ar):
        return 'file_ids', f'파일 신원 {len(ar)} = 판독 실패 때 남긴 꼴'
    if any(set(a) != set(ARM_PUBLIC) for a in ar):
        return 'bad', '칸 집합 ≠ ARM_PUBLIC (판독 완료 꼴) · ≠ 파일 신원'
    if type(rec) is not dict or 'arms' not in rec or request_fields_problem(rec):
        return 'bad', '요청 칸 (arms · arm_list) 없음 · 생산자 범위 밖 = 요청 팔을 모른다'
    kit = rec.get('kit')
    if type(kit) is not str:
        return 'bad', f'kit {kit!r}'
    idx = arm_indices(rec)
    if len(ar) != len(idx):
        return 'bad', f'팔 {len(ar)} ≠ 요청 팔 {len(idx)}'
    pref = arm_file_prefix(kit)
    for j, (a, i) in enumerate(zip(ar, idx)):
        f, x, h = a['file'], a['index'], a['sha256']
        if type(x) is not int or x != i:
            return 'bad', f'[{j}].index {x!r} ≠ 요청 팔 {i}'
        if not (type(f) is str and os.path.basename(f) == f and f.startswith(pref) and f.endswith(f'_a{i}.json')):
            return 'bad', f'[{j}].file {f!r} ≠ 이름 {pref}…_a{i}.json'
        if not (type(h) is str and ARM_SHA256_RE.fullmatch(h)):
            return 'bad', f'[{j}].sha256 = 64 자리 소문자 hex 아님'
    return 'verified', None


def sv_graph_state('''

EDITS = [
    ("    return sorted(out, key=lambda x: (x['index'], x['file']))\n\n\ndef sv_graph_state(", NEW_FUNCS),
    #  Runner._execute
    ("            #  읽기가 멈춰도 팔 파일 sha256 은 남긴다 — 등록 결과 (NOT_COMPUTED) 로 끝난 사다리를 판정이 원 팔에서 다시 계산할 수 있게.\n"
     "            rec['arms_read'] = arm_file_shas(outdir)\n"
     "            raise\n"
     "        rec['arms_read'] = [{k: a[k] for k in ARM_PUBLIC} for a in arms_]\n"
     "        a0 = arms_[0]\n",
     "            #  읽기가 멈춰도 팔 파일 sha256 은 남긴다 — 등록 결과 (NOT_COMPUTED) 로 끝난 사다리를 판정이 원 팔에서 다시 계산할 수 있게.  ★ 11-08 RR3-01 — 생성 =\n"
     "            #    `arms_read_record` 한 함수 (실패 = 파일 신원 · 성공 = ARM_PUBLIC · 두 꼴 칸 집합 다름 → 자격 소비자 `prior_runs_problem` 이 가른다)\n"
     "            rec['arms_read'] = arms_read_record(outdir=outdir)\n"
     "            raise\n"
     "        rec['arms_read'] = arms_read_record(arms_)\n"
     "        a0 = arms_[0]\n"),
    #  ResumeRunner._copy
    ("        except Stop:\n"
     "            rec['arms_read'] = arm_file_shas(outdir)\n"
     "            raise\n"
     "        rec['arms_read'] = [{k: a[k] for k in ARM_PUBLIC} for a in arms_]\n"
     "        self.resume['copied'].append(name)\n",
     "        except Stop:\n"
     "            rec['arms_read'] = arms_read_record(outdir=outdir)    # ★ 11-08 RR3-01 — 생성 한 함수 (복사 다시 읽기 실패 = 파일 신원)\n"
     "            raise\n"
     "        rec['arms_read'] = arms_read_record(arms_)\n"
     "        self.resume['copied'].append(name)\n"),
    #  MergeFetch.run
    ("        except Stop:\n"
     "            rec['arms_read'] = arm_file_shas(outdir)\n"
     "            raise\n"
     "        if stop0.get('run') == iname:",
     "        except Stop:\n"
     "            rec['arms_read'] = arms_read_record(outdir=outdir)    # ★ 11-08 RR3-01 — 생성 한 함수 (사본 다시 읽기 실패 = 파일 신원)\n"
     "            raise\n"
     "        if stop0.get('run') == iname:"),
    ("        rec['arms_read'] = [{k: a[k] for k in ARM_PUBLIC} for a in arms_]\n"
     "        print(f'  {name}: {role} · R_j {disp_rj(rj)} · {law} · c {c or \"-\"} · 팔 {arm_indices(req)} → {target} attempt_{u[\"n\"]} 의 {iname} '\n",
     "        rec['arms_read'] = arms_read_record(arms_)\n"
     "        print(f'  {name}: {role} · R_j {disp_rj(rj)} · {law} · c {c or \"-\"} · 팔 {arm_indices(req)} → {target} attempt_{u[\"n\"]} 의 {iname} '\n"),
    #  prior_runs_problem — 독스트링 끝 + 몸
    ("    마지막 (`stopped_record_problem` ①) 뒤에 부른다 · runs 가 목록이 아님 = None (`summary_shape_problem` 몫).\"\"\"\n",
     "    마지막 (`stopped_record_problem` ①) 뒤에 부른다 · runs 가 목록이 아님 = None (`summary_shape_problem` 몫).\n"
     "    ★ 11-08 RR3-01 (Codex 회차 ③ · 판정문 §2 · 1저자 11-08 \"권고대로\" = 수정 계획 Q1 · Q2 (가)) — 끝난 런 = exit_ok + arms_read 판독 완료 꼴\n"
     "    (`arms_read_kind` verified = `ARM_PUBLIC` 칸 정확히 + 요청 팔 일대일 + sha256 꼴) · 옛 = 비지 않은 목록 → 실제 판독 실패 (`read_run` ARM_JSON_COUNT) 때 생산자가\n"
     "    남긴 파일 신원 목록 ({file, index, sha256} · `arm_file_shas`) 도 끝난 런 → 요약 두 칸 (stop.code → TIME_LIMIT · stop.run → 다음 이름 L02_ceiling) 만 바꾸면\n"
     "    timeout · 재실행 자격 · 다음 --resume 원장 항목 허용 (실제 재개 복사 `ResumeRunner._copy` 는 다시 읽어 거부 = 원장 자격의 거짓 양성).  사유 글 = 분류 이름\n"
     "    (file_ids · empty · bad · verified).\"\"\"\n"),
    ("        sh = run_record_shape(r)\n"
     "        ar = r.get('arms_read') if isinstance(r, dict) else None\n"
     "        if sh != 'exit_ok' or not (type(ar) is list and ar):\n"
     "            nm = r.get('name') if isinstance(r, dict) else None\n"
     "            return (f'멈춤 {code} · 런 {run!r} 앞의 런 기록 runs[{i}] ({nm!r}) = 꼴 {sh} · arms_read {\"비지 않은 목록\" if type(ar) is list and ar else repr(ar)[:40]} ≠ '\n"
     "                    f'끝난 런 (생산자 = 앞 런이 rc 0 · 팔을 읽은 뒤에만 다음 런 · 실패 런 = 그 자리 멈춤 · ★ 11-08 PC12-03)')\n",
     "        sh = run_record_shape(r)\n"
     "        kind, why = arms_read_kind(r.get('arms_read') if isinstance(r, dict) else None, r)   # ★ 11-08 RR3-01 — 판독 완료 꼴만 (옛 = 비지 않은 목록)\n"
     "        if sh != 'exit_ok' or kind != 'verified':\n"
     "            nm = r.get('name') if isinstance(r, dict) else None\n"
     "            return (f'멈춤 {code} · 런 {run!r} 앞의 런 기록 runs[{i}] ({nm!r}) = 꼴 {sh} · arms_read {kind}{\" (\" + why + \")\" if why else \"\"} ≠ 끝난 런 '\n"
     "                    f'(생산자 = 앞 런이 rc 0 · 팔을 판독한 뒤에만 다음 런 = arms_read 판독 완료 꼴 (`arms_read_record` · ARM_PUBLIC · 요청 팔 일대일) · 판독 실패 '\n"
     "                    f'때 남긴 파일 신원 목록 (file_ids) = 끝난 런 아님 · 실패 런 = 그 자리 멈춤 · ★ 11-08 PC12-03 · RR3-01)')\n"),
    #  머리말 문단 (CT08 = 이름 붙인 함수 · 상수가 모듈에 있다)
    ("  길의 단계 요약 읽기 = `_json_strict` (중복 칸 · NaN · ±Infinity = unreadable) · 거부 기록 code ∈ `STOPS`.\n\"\"\"\n",
     "  길의 단계 요약 읽기 = `_json_strict` (중복 칸 · NaN · ±Infinity = unreadable) · 거부 기록 code ∈ `STOPS`.\n"
     "★ 11-08 RR3-01 (Codex 회차 ③ · 판정문 docs/reviews/codex_review_rint2_rr_round3_20261108.md §2 · 1저자 11-08 \"권고대로\" = 수정 계획\n"
     "  docs/reviews/rint2_rr3_fix_plan_20261108.md Q1–Q7 (가) · 실행 기록 = 그 계획 §9 · 증거 docs/reviews/rint2_rr2_fix_evidence_20261105/rr3_fix/): 앞 런 = 판독 완료 꼴만 끝난 런 —\n"
     "  구조 계약 하나 (생성 `arms_read_record` = 세 생산자 공용 · 성공 = `ARM_PUBLIC` 투영 · 실패 = 파일 신원 `arm_file_shas` (`ARM_FILE_ID_KEYS`) · 분류\n"
     "  `arms_read_kind` = verified (ARM_PUBLIC 칸 정확히 + 요청 팔 일대일 = 수 · 번호 · 파일 이름 (`arm_file_prefix` · _a<번호>.json) + sha256 꼴) · file_ids · empty ·\n"
     "  bad · 자격 소비자 = `prior_runs_problem` 하나 · 옛 = 비지 않은 목록 → 판독 실패 때 남긴 파일 신원 목록 + 요약 두 칸 = 재실행 자격 · 다음 원장 항목).\n"
     "\"\"\"\n"),
]


def main():
    src = C.read_text(encoding='utf-8')
    for old, new in EDITS:
        n = src.count(old)
        if n != 1:
            print(f'STOP — 옛 글이 {n} 번 (정확히 한 번이어야): {old[:100]!r}')
            return 2
        src = src.replace(old, new)
    tmp = C.with_name(C.name + '.tmp_rr3')
    tmp.write_text(src, encoding='utf-8')
    os.replace(tmp, C)
    print(f'바꿈 {len(EDITS)} → {C}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
