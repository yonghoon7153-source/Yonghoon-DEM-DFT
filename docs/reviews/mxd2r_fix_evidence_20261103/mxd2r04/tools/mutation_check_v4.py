"""Mutation check v4 (11-03 밤 · MXD2R-04 범위 넓힘 = neighbor skin 도 생성기 꼴) — v3 의 M01–M54 그대로, 단 M31 만 바꾼다
(v3 M31 '자유 칸 skin 수 검사 끔' 은 그 검사가 없어져 대상 문자열이 없다 → 'skin 기대 토큰을 덱 자신에서 복사') · M55 를 더한다
(skin 계수 0.5 → 0.6 = tighten, 양성 시험이 잡아야 함).  v3 파일과 그 결과는 첫 판 기록 그대로 둔다.

Usage: python3 -I mutation_check_v4.py <scratch scripts dir> <out.json> [mutant-id-prefix …]
"""
import importlib.util
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
_spec = importlib.util.spec_from_file_location('mutation_check_v3', os.path.join(_HERE, 'mutation_check_v3.py'))
_v3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_v3)
R = _v3.R
SKIN_M31 = ('M31 weaken form: skin value from deck', R, "['neighbor', f6(min(d.values()) * 0.5), 'bin']",
            "next(t for t in commands if t[0] == 'neighbor')")
SKIN_M55 = ('M55 tighten form: skin factor 0.5 → 0.6', R, "f6(min(d.values()) * 0.5)", "f6(min(d.values()) * 0.6)")
MUTANTS = [SKIN_M31 if m[0].startswith('M31 ') else m for m in _v3.MUTANTS] + [SKIN_M55]
assert sum(m[0].startswith('M31 ') for m in MUTANTS) == 1 and len(MUTANTS) == len(_v3.MUTANTS) + 1


def main(scripts, out, *prefixes):
    import json
    _v3.MUTANTS = MUTANTS                    # v3.main 은 모듈 전역 MUTANTS 를 돈다
    _v3.main(scripts, out, *prefixes)
    with open(out, encoding='utf-8') as f:
        report = json.load(f)
    report['tool'] = 'mutation_check_v4.py (v3.main · M31 바꿈 · M55 더함)'
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
        f.write('\n')


if __name__ == '__main__':
    main(*sys.argv[1:])
