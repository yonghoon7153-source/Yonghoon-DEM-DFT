#!/usr/bin/env python3
"""P1 G2c' 초안 A — PFA-01 (마지막 사전 공격 · 내부 · Codex 아님) 고침 규칙을 작은 반례로 다시 확인한다 (임시 폴더 · 읽기만 · 리포 무관).

뿌리 = 심볼릭 (<HOME> -> <LUSTRE_HOME> 꼴 · 근거 = RJ 323957 잡 기록 19 행 verdict= ↔ run_dir= · ul_reader.py 1509 행 realpath).
러너는 잡 폴더를 링크 꼴 글자 ($WORK_ROOT/$BED/$JOB) 로 쓴다 (run_unload.sh 36 · 141 행) · 판독기는 받은 루트로 잡 폴더를 만든다 (1561 행).

고친 규칙 (키트 15-5 · 잡):
  (i)  글자 같음 — 같은 러너가 쓴 기록 · 로그끼리: rt1_bin= 경로 = rt2_ckpt= 경로 = RT2 로그 치환 줄 경로 = job_dir + '/RT1/rt.bin'
  (ii) 실제 경로 같음 — 양쪽 realpath: realpath(job_dir) = realpath(판독기가 받은 잡 폴더)
고친 규칙 (RT 문법 fixture 검사 4 · 5 · 13 · 런):
  4·5  realpath(ckpt.txt 글자) = realpath(<런>/P/fixture.bin) · realpath(<런>/RT1/rt.bin)   (지금 문법 fixture `_same` 꼴)
  13   RT2 로그 치환 줄 경로 글자 = RT2 ckpt.txt 글자 (같은 생산자)  ∧  realpath(그 글자) = realpath(<런>/RT1/rt.bin)
2 회차 판 (고치기 전): 잡 = (i) + realpath(job_dir) = 받은 잡 폴더 **글자** (한쪽만) · fixture = 글자 같음 (ckpt.txt = <런>/… 글자).
쓰는 법: python3 -I f3_path_rule.py
"""
import os
import sys
import tempfile


def new_job(rec, reader_folder):
    exp = rec['job_dir'] + '/RT1/rt.bin'
    chars = rec['rt1_bin'] == exp and rec['rt2_ckpt'] == exp and rec['log'] == exp
    return chars and os.path.realpath(rec['job_dir']) == os.path.realpath(reader_folder)


def old_job(rec, reader_folder):
    exp = rec['job_dir'] + '/RT1/rt.bin'
    chars = rec['rt1_bin'] == exp and rec['rt2_ckpt'] == exp and rec['log'] == exp
    return chars and os.path.realpath(rec['job_dir']) == reader_folder


def new_fix(ck1, ck2, log2, run):
    s = lambda a, b: bool(a) and bool(b) and os.path.realpath(a) == os.path.realpath(b)
    return (s(ck1, os.path.join(run, 'P', 'fixture.bin')) and s(ck2, os.path.join(run, 'RT1', 'rt.bin'))
            and log2 == ck2 and s(log2, os.path.join(run, 'RT1', 'rt.bin')))


def old_fix(ck1, ck2, log2, run):
    return (ck1 == os.path.join(run, 'P', 'fixture.bin') and ck2 == os.path.join(run, 'RT1', 'rt.bin')
            and log2 == ck2 and log2 == os.path.join(run, 'RT1', 'rt.bin'))


rows = []
with tempfile.TemporaryDirectory(prefix='f3_path_', dir=os.path.dirname(os.path.abspath(__file__))) as td:
    real = os.path.join(td, 'LUSTRE_HOME')
    link = os.path.join(td, 'HOME')
    os.makedirs(os.path.join(real, 'ps45', 'bed', 'RJ', 'RT1'))
    os.makedirs(os.path.join(real, 'ps45', 'bed', 'RJ.try1', 'RT1'))
    os.makedirs(os.path.join(real, 'other', 'bed', 'RJ', 'RT1'))
    os.makedirs(os.path.join(real, 'hist', 'rtg_1', 'RT1'))
    os.makedirs(os.path.join(real, 'hist', 'rtg_0', 'RT1'))
    os.symlink(real, link)
    L, R = link + '/ps45', real + '/ps45'

    def rec(job_dir, path=None):
        p = path or job_dir + '/RT1/rt.bin'
        return {'job_dir': job_dir, 'rt1_bin': job_dir + '/RT1/rt.bin', 'rt2_ckpt': p, 'log': p}

    cases = [
        ('잡 · 정직 · 판독 루트 = 링크 꼴 (러너 안 판독)', rec(L + '/bed/RJ'), L + '/bed/RJ', True),
        ('잡 · 정직 · 판독 루트 = realpath 꼴 (다시 읽기)', rec(L + '/bed/RJ'), R + '/bed/RJ', True),
        ('잡 · 정직 · WORK_ROOT 에 // (세 글자 같음)', rec(link + '//ps45/bed/RJ'), L + '/bed/RJ', True),
        ('잡 · RT2 가 이름 바꾼 앞 시도 RJ.try1/RT1/rt.bin 을 읽음', rec(L + '/bed/RJ', L + '/bed/RJ.try1/RT1/rt.bin'), L + '/bed/RJ', False),
        ('잡 · RT2 가 다른 폴더 같은 이름 파일 (realpath 꼴 글자)', rec(L + '/bed/RJ', real + '/other/bed/RJ/RT1/rt.bin'), L + '/bed/RJ', False),
        ('잡 · RT2 가 같은 파일을 realpath 꼴 글자로 (러너 글자 아님)', rec(L + '/bed/RJ', R + '/bed/RJ/RT1/rt.bin'), L + '/bed/RJ', False),
        ('잡 · 기록이 서로 맞지만 job_dir = 다른 폴더', rec(link + '/other/bed/RJ'), L + '/bed/RJ', False),
        ('잡 · 이름 바꾼 폴더 RJ.try1 다시 읽기 (기록 job_dir = …/RJ)', rec(L + '/bed/RJ'), L + '/bed/RJ.try1', False),
    ]
    for label, r, folder, want in cases:
        rows.append((label, want, new_job(r, folder), old_job(r, folder)))

    run_l, run_r = link + '/hist/rtg_1', os.path.dirname(os.path.realpath(link + '/hist/rtg_1/rt_grammar_verdict.json'))
    ck1, ck2 = run_l + '/P/fixture.bin', run_l + '/RT1/rt.bin'
    fcases = [
        ('fixture · 정직 · 첫 판독 (런 폴더 = 링크 꼴)', (ck1, ck2, ck2, run_l), True),
        ('fixture · 정직 · 사전 점검 다시 읽기 (런 폴더 = realpath 꼴 · ul_reader 1509 꼴)', (ck1, ck2, ck2, run_r), True),
        ('fixture · RT2 가 다른 런 rtg_0/RT1/rt.bin 을 읽음', (ck1, link + '/hist/rtg_0/RT1/rt.bin', link + '/hist/rtg_0/RT1/rt.bin', run_r), False),
        ('fixture · 로그 글자 ≠ ckpt.txt 글자 (같은 파일 realpath 꼴)', (ck1, ck2, real + '/hist/rtg_1/RT1/rt.bin', run_r), False),
    ]
    for label, (a, b, c, run), want in fcases:
        rows.append((label, want, new_fix(a, b, c, run), old_fix(a, b, c, run)))

    # 한정 (참고): 잡 폴더 자체를 다른 잡 폴더의 심볼릭으로 바꾼 손 조작 — 같은 물리 폴더라 (ii) 통과 · 읽은 파일도 같은 파일
    os.rename(os.path.join(real, 'ps45', 'bed', 'RJ'), os.path.join(real, 'ps45', 'bed', 'RJ.moved'))
    os.symlink(os.path.join(real, 'ps45', 'bed', 'RJ.try1'), os.path.join(real, 'ps45', 'bed', 'RJ'))
    alias = new_job(rec(L + '/bed/RJ'), L + '/bed/RJ.try1')

ok = all(w == n for _, w, n, _ in rows)
for label, want, new, old in rows:
    print(f'{"✓" if want == new else "✗"} {label}: 기대 {"통과" if want else "거부"} · 고친 규칙 {"통과" if new else "거부"} · 2 회차 판 {"통과" if old else "거부"}')
print(f'한정 · 잡 폴더 = 다른 시도 폴더의 심볼릭 (손 조작 · 같은 물리 폴더): 고친 규칙 {"통과" if alias else "거부"} (같은 파일을 읽었다 · 막지 않음 = 한정)')
print('결과:', '고친 규칙 = 기대와 모두 같음' if ok else '어긋남 있음')
sys.exit(0 if ok else 1)
